from datetime import datetime
from functools import lru_cache
from io import BytesIO
import logging
import math
import os
import re
import unicodedata

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response, Depends
import pymupdf

from ..dados_equipamentos import DADOS_ARMADURAS
from ..dados_pericias import DADOS_PERICIAS
from ..dependencies import get_db
from ..models import Personagem
from ..regras import atualizar_ficha
from ..regras.custo_magia import obter_atributo_chave_magia
from ..regras.utils import calcular_modificador

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/personagens", tags=["PDF"])

# Mapa completo de cada linha de perícia no template oficial:
# nome -> (prefixo, checkbox_treino, combo_atrib, campo_mod_atrib)
SKILL_WIDGETS = {
    "Acrobacia": ("01", "Mar Trei acro", "SeleAtribAcro", "ModAtribAcro"),
    "Adestramento": ("02", "Mar Trei ades", "SeleAtribAdes", "ModAtribAdes"),
    "Atletismo": ("03", "Mar Trei atle", "SeleAtribAtle", "ModAtribAtle"),
    "Atuação": ("04", "Mar Trei atua", "SeleAtribAtua", "ModAtribAtua"),
    "Cavalgar": ("05", "Mar Trei caval", "SeleAtribCava", "ModAtribCava"),
    "Conhecimento": ("06", "Mar Trei conhe", "SeleAtribConh", "ModAtribConh"),
    "Cura": ("07", "Mar Trei cura", "SeleAtribCura", "ModAtribCura"),
    "Diplomacia": ("08", "Mar Trei dipl", "SeleAtribDipl", "ModAtribDipl"),
    "Enganação": ("09", "Mar Trei enga", "SeleAtribEnga", "ModAtribEnga"),
    "Fortitude": ("10", "Mar Trei forti", "SeleAtribFort", "ModAtribFort"),
    "Furtividade": ("11", "Mar Trei furti", "SeleAtribFurt", "ModAtribFurt"),
    "Guerra": ("12", "Mar Trei guerra", "SeleAtribGuer", "ModAtribGuer"),
    "Iniciativa": ("13", "Mar Trei ini", "SeleAtribInic", "ModAtribInic"),
    "Intimidação": ("14", "Mar Trei inti", "SeleAtribInti", "ModAtribInti"),
    "Intuição": ("15", "Mar Trei intu", "SeleAtribIntu", "ModAtribIntu"),
    "Investigação": ("16", "Mar Trei inve", "SeleAtribInve", "ModAtribInve"),
    "Jogatina": ("17", "Mar Trei joga", "SeleAtribJoga", "ModAtribJoga"),
    "Ladinagem": ("18", "Mar Trei ladi", "SeleAtribLadi", "ModAtribLadi"),
    "Luta": ("19", "Mar Trei luta", "SeleAtribLuta", "ModAtribLuta"),
    "Misticismo": ("20", "Mar Trei misti", "SeleAtribMist", "ModAtribMist"),
    "Pilotagem": ("21", "Mar Trei pilo", "SeleAtribPilo", "ModAtribPilo"),
    "Nobreza": ("22", "Mar Trei nobre", "SeleAtribNobr", "ModAtribNobr"),
    "Ofício 1": ("23", "Mar Trei ofi1", "SeleAtribOfi1", "ModAtribOfi1"),
    "Ofício 2": ("24", "Mar Trei ofi2", "SeleAtribOfi2", "ModAtribOfi2"),
    "Percepção": ("25", "Mar Trei perce", "SeleAtribPerc", "ModAtribPerc"),
    "Pontaria": ("26", "Mar Trei ponta", "SeleAtribPont", "ModAtribPont"),
    "Reflexos": ("27", "Mar Trei refle", "SeleAtribRefl", "ModAtribRefl"),
    "Religião": ("28", "Mar Trei reli", "SeleAtribReli", "ModAtribReli"),
    "Sobrevivência": ("29", "Mar Trei sobre", "SeleAtribSobr", "ModAtribSobr"),
    "Vontade": ("30", "Mar Trei vonta", "SeleAtribVont", "ModAtribVont"),
}

_ATTR_FULL_TO_SHORT = {
    "forca": "For",
    "destreza": "Des",
    "constituicao": "Con",
    "inteligencia": "Int",
    "sabedoria": "Sab",
    "carisma": "Car",
    "for": "For",
    "des": "Des",
    "con": "Con",
    "int": "Int",
    "sab": "Sab",
    "car": "Car",
}

_SHORT_TO_ATTR_FULL = {
    "For": "forca",
    "Des": "destreza",
    "Con": "constituicao",
    "Int": "inteligencia",
    "Sab": "sabedoria",
    "Car": "carisma",
}

_MOD_TAMANHO = {
    "Minúsculo": (5, -5),
    "Pequeno": (2, -2),
    "Médio": (0, 0),
    "Grande": (-2, 2),
    "Enorme": (-5, 5),
    "Colossal": (-10, 10),
}


def _sanitizar_nome_arquivo(nome: str | None) -> str:
    """Converte o nome do personagem em slug ASCII seguro para Content-Disposition."""
    if not nome:
        return "personagem"
    ascii_nome = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode("ASCII")
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", ascii_nome).strip("-").lower()
    return slug or "personagem"


def _truncar_texto(texto: str, limite: int) -> str:
    """Trunca texto longo de forma inteligente na última quebra de linha ou espaço."""
    if not texto or len(texto) <= limite:
        return texto or ""
    corte = texto[: limite - 3]
    ultima_quebra = max(corte.rfind("\n"), corte.rfind(" "))
    if ultima_quebra > limite * 0.6:
        corte = corte[:ultima_quebra]
    return corte.rstrip() + "..."


@lru_cache(maxsize=1)
def _carregar_template_bytes() -> bytes:
    """Carrega e valida o template PDF em memória uma única vez (evita reler 4.6MB por request)."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    template_path = os.path.join(base_dir, "assets", "ficha-t20-template.pdf")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template PDF não encontrado em: {template_path}")
    with open(template_path, "rb") as f:
        data = f.read()
    if not data.startswith(b"%PDF"):
        raise ValueError(f"Arquivo de template inválido: {template_path}")
    return data


def _formatar_classes_cabecalho(personagem: Personagem) -> str:
    classes = personagem.classes or []
    if not classes:
        return ""
    if len(classes) == 1:
        c = classes[0]
        return f"{c.nome} ({c.subclasse})" if c.subclasse else str(c.nome)
    return " / ".join(f"{c.nome} {c.nivel}" for c in classes)


def _formatar_descricao_pagina2(personagem: Personagem) -> str:
    desc = personagem.descricao
    partes = []
    meta = []
    if desc.idade:
        faixa = f" ({desc.faixa_etaria})" if desc.faixa_etaria else ""
        meta.append(f"Idade: {desc.idade}{faixa}")
    if desc.alinhamento:
        meta.append(f"Alinhamento: {desc.alinhamento}")
    if meta:
        partes.append(" | ".join(meta))
    if desc.aparencia:
        partes.append(f"Aparência: {desc.aparencia}")
    if desc.personalidade:
        partes.append(f"Personalidade: {desc.personalidade}")
    if desc.historia:
        partes.append(f"História: {desc.historia}")
    return "\n\n".join(partes)


def gerar_pdf_bytes(personagem: Personagem) -> bytes:
    """Preenche o template oficial da ficha T20 com PyMuPDF e retorna os bytes do PDF."""
    # Trabalha numa cópia para não mutar a instância original e preserva PV/PM atuais
    ficha = personagem.model_copy(deep=True)
    pv_atual_orig = ficha.status.pv.atual
    pm_atual_orig = ficha.status.pm.atual

    try:
        atualizar_ficha(ficha)
        if 0 < pv_atual_orig <= ficha.status.pv.maximo:
            ficha.status.pv.atual = pv_atual_orig
        if 0 < pm_atual_orig <= ficha.status.pm.maximo:
            ficha.status.pm.atual = pm_atual_orig
    except Exception as e:
        logger.warning(f"Não foi possível recalcular a ficha completa para o PDF: {e}")

    def safe_str(val):
        return str(val) if val is not None else ""

    def format_mod(val):
        if val is None:
            return "0"
        v = int(val)
        return f"+{v}" if v > 0 else str(v)

    nivel_total = max(1, int(ficha.cabecalho.nivel_total or 1))
    metade_nivel = math.floor(nivel_total / 2)
    bonus_treino_nivel = 2 if nivel_total <= 6 else (4 if nivel_total <= 14 else 6)

    fields_to_fill = {}

    # ── CABEÇALHO ──
    fields_to_fill["NOME DO PERSONAGEM"] = safe_str(ficha.cabecalho.nome)
    fields_to_fill["JOGADOR"] = safe_str(ficha.cabecalho.jogador)
    fields_to_fill["RAÇA"] = safe_str(ficha.cabecalho.raca)
    fields_to_fill["ORIGEM"] = safe_str(ficha.cabecalho.origem)
    fields_to_fill["CLASSE"] = _formatar_classes_cabecalho(ficha)
    fields_to_fill["Lv"] = safe_str(nivel_total)
    fields_to_fill["DIVINDADE"] = safe_str(ficha.cabecalho.deus)
    fields_to_fill["Exp"] = safe_str(ficha.cabecalho.xp.atual)

    # ── ATRIBUTOS & MODIFICADORES ──
    # O template usa For/Des/... na escala 10+2*mod para o JS do Acrobat,
    # e exibe o modificador real (JdA) em ModFor/ModDes/...
    campos_atributos = [
        ("forca", "For", "ModFor"),
        ("destreza", "Des", "ModDes"),
        ("constituicao", "Con", "ModCon"),
        ("inteligencia", "Int", "ModInt"),
        ("sabedoria", "Sab", "ModSab"),
        ("carisma", "Car", "ModCar"),
    ]
    for attr, field_val, field_mod in campos_atributos:
        modifier = int(getattr(ficha.atributos, attr) or 0)
        fields_to_fill[field_val] = safe_str(10 + (2 * modifier))
        fields_to_fill[field_mod] = format_mod(modifier)

    # ── STATUS, DEFESA DETALHADA, ARMADURA & ESCUDO ──
    fields_to_fill["PVs Totais"] = safe_str(ficha.status.pv.maximo)
    fields_to_fill["PVs Atuais"] = safe_str(ficha.status.pv.atual)
    fields_to_fill["PMs Totais"] = safe_str(ficha.status.pm.maximo)
    fields_to_fill["PMs Atuais"] = safe_str(ficha.status.pm.atual)
    fields_to_fill["Desloc"] = f"{ficha.status.deslocamento}m"

    armadura_nome = ""
    b_arm = 0
    pa = 0
    usa_pesada = False
    escudo_nome = ""
    b_esc = 0
    pe = 0
    for it in (ficha.inventario.equipamentos or []):
        if not it.equipado:
            continue
        dados_arm = DADOS_ARMADURAS.get(it.nome)
        if not dados_arm:
            continue
        tipo_arm = dados_arm.get("tipo_armadura")
        if tipo_arm in ("Leve", "Pesada") and not armadura_nome:
            armadura_nome = it.nome
            b_arm = int(dados_arm.get("bonus_defesa", 0) or 0)
            pa = abs(int(dados_arm.get("penalidade_armadura", 0) or 0))
            usa_pesada = tipo_arm == "Pesada"
        elif tipo_arm == "Escudo" and not escudo_nome:
            escudo_nome = it.nome
            b_esc = int(dados_arm.get("bonus_defesa", 0) or 0)
            pe = abs(int(dados_arm.get("penalidade_armadura", 0) or 0))

    mod_des = calcular_modificador(ficha.atributos.destreza)
    defesa_total = int(ficha.status.defesa.total or 10)
    des_na_ca = 0 if usa_pesada else mod_des
    outros_ca = defesa_total - 10 - des_na_ca - b_arm - b_esc

    fields_to_fill["CA"] = safe_str(defesa_total)
    fields_to_fill["Base CA"] = "10"
    fields_to_fill["arm pesa"] = "/Off" if usa_pesada else "/Yes"
    fields_to_fill["SeleAtribDefe"] = "Des"
    fields_to_fill["ModAtribDefe"] = format_mod(mod_des)
    fields_to_fill["Armadura"] = armadura_nome
    fields_to_fill["B.Arm1"] = safe_str(b_arm)
    fields_to_fill["B.Arm"] = safe_str(b_arm)
    fields_to_fill["Pa"] = safe_str(pa)
    fields_to_fill["Escudo"] = escudo_nome
    fields_to_fill["B.Esc2"] = safe_str(b_esc)
    fields_to_fill["B.Esc"] = safe_str(b_esc)
    fields_to_fill["Pe"] = safe_str(pe)
    fields_to_fill["PArmTotal"] = safe_str(int(ficha.status.penalidade_armadura or (pa + pe)))
    fields_to_fill["Outros B.CA"] = safe_str(outros_ca)

    # ── PROFICIÊNCIAS & TAMANHO ──
    fields_to_fill["Proficiências"] = safe_str(ficha.status.proficiencias)
    tam_raw = getattr(ficha.descricao.tamanho, "value", ficha.descricao.tamanho) or "Médio"
    tam_str = str(tam_raw) if str(tam_raw) in _MOD_TAMANHO else "Médio"
    mod_furt_tam, mod_man_tam = _MOD_TAMANHO[tam_str]
    fields_to_fill["SeleTamanho"] = tam_str
    fields_to_fill["ModFurtTam"] = format_mod(mod_furt_tam)
    fields_to_fill["ModManTam"] = format_mod(mod_man_tam)

    # ── PERÍCIAS (TODAS AS COLUNAS + OFÍCIOS CUSTOMIZADOS) ──
    oficios_ficha = sorted(
        [(k, v) for k, v in (ficha.pericias or {}).items() if k.startswith("Ofício")],
        key=lambda kv: (
            "(" not in kv[0],
            not bool(kv[1].treino and kv[1].treino > 0),
            kv[0],
        ),
    )
    for nome_slot, (prefixo, cb_field, sele_field, mod_field) in SKILL_WIDGETS.items():
        pericia = None
        if nome_slot == "Ofício 1":
            if len(oficios_ficha) >= 1:
                nome_ofi, pericia = oficios_ficha[0]
                fields_to_fill["Ofício 1"] = nome_ofi.replace("Ofício (", "").rstrip(")") if "(" in nome_ofi else nome_ofi
        elif nome_slot == "Ofício 2":
            if len(oficios_ficha) >= 2:
                nome_ofi, pericia = oficios_ficha[1]
                fields_to_fill["Ofício_2"] = nome_ofi.replace("Ofício (", "").rstrip(")") if "(" in nome_ofi else nome_ofi
        else:
            pericia = ficha.pericias.get(nome_slot)

        meta_padrao = DADOS_PERICIAS.get(nome_slot, {})
        attr_short = _ATTR_FULL_TO_SHORT.get(
            (getattr(pericia, "atributo_usado", None) or meta_padrao.get("atributo") or "int").lower(),
            "Int",
        )
        attr_full = _SHORT_TO_ATTR_FULL.get(attr_short, "inteligencia")
        mod_attr = int(getattr(ficha.atributos, attr_full) or 0)

        fields_to_fill[f"{prefixo}1"] = safe_str(metade_nivel)
        fields_to_fill[sele_field] = attr_short
        fields_to_fill[mod_field] = format_mod(mod_attr)

        if pericia:
            treinado = bool(pericia.treino and pericia.treino > 0)
            bonus_tr = bonus_treino_nivel if treinado else 0
            outros = int(pericia.outros or 0) + int(pericia.bonus_automatico or 0)
            fields_to_fill[cb_field] = "/Yes" if treinado else "/Off"
            fields_to_fill[f"{prefixo}3"] = safe_str(bonus_tr)
            fields_to_fill[f"{prefixo}4"] = format_mod(outros) if outros != 0 else ""
            fields_to_fill[f"{prefixo}0"] = safe_str(int(pericia.total or 0))
        else:
            fields_to_fill[cb_field] = "/Off"
            fields_to_fill[f"{prefixo}3"] = "0"
            fields_to_fill[f"{prefixo}4"] = ""
            fields_to_fill[f"{prefixo}0"] = safe_str(metade_nivel + mod_attr)

    # ── ATAQUES ──
    for i, ataque in enumerate((ficha.combate.ataques or [])[:5], 1):
        fields_to_fill[f"Ataque {i}"] = safe_str(ataque.nome)
        fields_to_fill[f"Bônus Atq {i}"] = safe_str(ataque.bonus_ataque)
        fields_to_fill[f"Dano {i}"] = safe_str(ataque.dano)
        fields_to_fill[f"Crítico {i}"] = safe_str(ataque.critico)
        fields_to_fill[f"Tipo {i}"] = safe_str(ataque.tipo)
        fields_to_fill[f"Alcance {i}"] = safe_str(ataque.alcance)

    # ── DINHEIRO & EQUIPAMENTO ──
    fields_to_fill["T"] = safe_str(ficha.inventario.dinheiro.tp)
    fields_to_fill["TO"] = safe_str(ficha.inventario.dinheiro.to)
    for i, item in enumerate((ficha.inventario.equipamentos or [])[:15], 1):
        nome_item = f"{item.nome} (x{item.qtd})" if (item.qtd or 1) > 1 else safe_str(item.nome)
        fields_to_fill[f"Item{i}"] = nome_item
        peso_item = (item.espaco or 0) * (item.qtd or 1)
        fields_to_fill[f"PesoItem{i}"] = safe_str(int(peso_item) if float(peso_item).is_integer() else peso_item)

    carga_max = int(ficha.inventario.carga_maxima or 0)
    fields_to_fill["CargaTotal"] = safe_str(ficha.inventario.carga_total)
    fields_to_fill["CargaMax"] = safe_str(carga_max)
    fields_to_fill["Levantar"] = safe_str(carga_max * 2)

    # ── PÁGINA 2: HABILIDADES, MAGIAS, DESCRIÇÃO E ANOTAÇÕES ──
    habs_raca_origem = "\n".join([
        f"• {h.nome}: {h.descricao}"
        for h in (ficha.habilidades or [])
        if h.tipo and any(t in h.tipo.lower() for t in ["racial", "origem"])
    ])
    habs_classe = "\n".join([
        f"• {h.nome}: {h.descricao}"
        for h in (ficha.habilidades or [])
        if not (h.tipo and any(t in h.tipo.lower() for t in ["racial", "origem"]))
    ])

    fields_to_fill["HabRaçasOrigem"] = _truncar_texto(habs_raca_origem, 3500)
    fields_to_fill["HabClassePoderes"] = _truncar_texto(habs_classe, 3500)

    # Atributo-chave e CD de Magias (Página 2)
    attr_magia_full = obter_atributo_chave_magia(ficha) or "inteligencia"
    attr_magia_short = _ATTR_FULL_TO_SHORT.get(attr_magia_full, "Int")
    mod_magia = int(getattr(ficha.atributos, attr_magia_full) or 0)
    fields_to_fill["SeleAtribMagia"] = attr_magia_short
    fields_to_fill["ModAtribMagia"] = format_mod(mod_magia)
    fields_to_fill["TesteResist"] = safe_str(ficha.combate.cd_magias or (10 + metade_nivel + mod_magia))

    # Magias formatadas com aprimoramentos
    blocos_magia = []
    for m in (ficha.combate.magias or []):
        alvo_txt = m.alvo or "-"
        linhas = [
            f"• {m.nome} ({m.circulo}º Círculo | {m.custo_pm} PM)",
            f"  {m.tipo} • {m.escola} | Exec: {m.execucao} | Alc: {m.alcance} | Alvo: {alvo_txt} | Dur: {m.duracao} | Res: {m.resistencia or '-'}",
            f"  {m.descricao}",
        ]
        if m.aprimoramentos:
            for ap in m.aprimoramentos:
                c = ap.get("custo", "") if isinstance(ap, dict) else getattr(ap, "custo", "")
                d = ap.get("descricao", "") if isinstance(ap, dict) else getattr(ap, "descricao", "")
                linhas.append(f"    - {c}: {d}")
        blocos_magia.append("\n".join(linhas))

    fields_to_fill["Magias"] = _truncar_texto("\n\n".join(blocos_magia), 4500)
    fields_to_fill["Descrição"] = _truncar_texto(_formatar_descricao_pagina2(ficha), 3000)

    anotacoes_txt = safe_str(ficha.descricao.anotacoes).strip()
    rodape_data = f"Gerado em {datetime.now().strftime('%d/%m/%Y')}"
    anotacoes_final = f"{anotacoes_txt}\n\n{rodape_data}" if anotacoes_txt else rodape_data
    fields_to_fill["Anotações"] = _truncar_texto(anotacoes_final, 3000)

    # ── PREENCHIMENTO COM PYMUPDF (template em cache de memória) ──
    template_bytes = _carregar_template_bytes()
    output = BytesIO()
    with pymupdf.open(stream=template_bytes, filetype="pdf") as doc:
        for page in doc:
            for widget in page.widgets():
                if widget.field_name in fields_to_fill:
                    val = fields_to_fill[widget.field_name]
                    if val == "/Yes":
                        widget.field_value = True
                    elif val == "/Off":
                        widget.field_value = False
                    else:
                        widget.field_value = str(val)
                    widget.update()
        doc.save(output, garbage=4, deflate=True)

    return output.getvalue()


@router.get("/{personagem_id}/pdf")
async def gerar_pdf(personagem_id: str, db=Depends(get_db)):
    """Gera PDF da ficha de personagem preenchida usando PyMuPDF."""
    try:
        try:
            oid = ObjectId(personagem_id)
        except Exception:
            raise HTTPException(status_code=404, detail="ID inválido")

        personagem_doc = await db.personagens.find_one({"_id": oid})
        if not personagem_doc:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")

        personagem = Personagem(**personagem_doc)
        pdf_bytes = gerar_pdf_bytes(personagem)
        nome_slug = _sanitizar_nome_arquivo(personagem.cabecalho.nome)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=ficha-{nome_slug}.pdf"},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")
