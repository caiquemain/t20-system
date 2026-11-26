from datetime import datetime
from functools import lru_cache
from io import BytesIO
import logging
import math
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

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


def _construir_campos_ficha(personagem: Personagem) -> dict[str, str]:
    """Recalcula a ficha em cópia isolada e monta o dicionário de campos do template oficial T20."""
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

    return fields_to_fill


def gerar_pdf_bytes(personagem: Personagem) -> bytes:
    """Preenche o template oficial da ficha T20 com PyMuPDF e retorna os bytes do PDF."""
    fields_to_fill = _construir_campos_ficha(personagem)

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


# ── EXPORTAÇÃO LIBREOFFICE DRAW (.ODG) BASEADA NO TEMPLATE PDF ──
_ODG_MIMETYPE = "application/vnd.oasis.opendocument.graphics"
_PT_TO_CM = 2.54 / 72.0
_PDF_FLAG_MULTILINE = 4096

_CAMPOS_ALINHADOS_ESQUERDA = {
    "NOME DO PERSONAGEM",
    "JOGADOR",
    "RAÇA",
    "ORIGEM",
    "CLASSE",
    "DIVINDADE",
    "Armadura",
    "Escudo",
    "Proficiências",
    "Ofício 1",
    "Ofício_2",
    "HabRaçasOrigem",
    "HabClassePoderes",
    "Magias",
    "Descrição",
    "Anotações",
}


def _pt_cm(val: float) -> str:
    return f"{val * _PT_TO_CM:.4f}cm"


@lru_cache(maxsize=1)
def _carregar_template_odg_layout() -> list[dict]:
    """Renderiza as páginas do PDF oficial em PNG (150 DPI, sem widgets) e extrai coordenadas dos campos."""
    template_bytes = _carregar_template_bytes()
    paginas: list[dict] = []
    with pymupdf.open(stream=template_bytes, filetype="pdf") as doc:
        for idx, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=150, annots=False)
            png_bytes = pix.tobytes("png")

            vistos: set[str] = set()
            widgets_info: list[dict] = []
            for w in page.widgets():
                nome = w.field_name
                if not nome or nome in vistos:
                    continue
                vistos.add(nome)
                widgets_info.append({
                    "name": nome,
                    "type": w.field_type_string or "Text",
                    "x0": float(w.rect.x0),
                    "y0": float(w.rect.y0),
                    "x1": float(w.rect.x1),
                    "y1": float(w.rect.y1),
                    "fontsize": float(w.text_fontsize or 0.0),
                    "multiline": bool((w.field_flags or 0) & _PDF_FLAG_MULTILINE),
                })

            paginas.append({
                "index": idx,
                "width_pt": float(page.rect.width),
                "height_pt": float(page.rect.height),
                "png": png_bytes,
                "widgets": widgets_info,
            })
    return paginas


def gerar_odg_bytes(personagem: Personagem) -> bytes:
    """Gera arquivo LibreOffice Draw (.odg) ODF 1.2 usando o PDF oficial como fundo e caixas editáveis."""
    fields_to_fill = _construir_campos_ficha(personagem)
    paginas = _carregar_template_odg_layout()

    w_cm = _pt_cm(paginas[0]["width_pt"])
    h_cm = _pt_cm(paginas[0]["height_pt"])

    # Namespaces ODF 1.2
    NS_OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    NS_STYLE = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    NS_TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    NS_DRAW = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    NS_FO = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    NS_SVG = "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    NS_XLINK = "http://www.w3.org/1999/xlink"
    NS_DC = "http://purl.org/dc/elements/1.1/"
    NS_META = "urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    NS_MANIFEST = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"

    for prefix, uri in [
        ("office", NS_OFFICE),
        ("style", NS_STYLE),
        ("text", NS_TEXT),
        ("draw", NS_DRAW),
        ("fo", NS_FO),
        ("svg", NS_SVG),
        ("xlink", NS_XLINK),
        ("dc", NS_DC),
        ("meta", NS_META),
        ("manifest", NS_MANIFEST),
    ]:
        ET.register_namespace(prefix, uri)

    def q(ns: str, tag: str) -> str:
        return f"{{{ns}}}{tag}"

    # ── 1. manifest.xml ──
    manifest = ET.Element(q(NS_MANIFEST, "manifest"), {q(NS_MANIFEST, "version"): "1.2"})
    manifest_entries = [
        ("/", _ODG_MIMETYPE),
        ("content.xml", "text/xml"),
        ("styles.xml", "text/xml"),
        ("meta.xml", "text/xml"),
    ]
    for pag in paginas:
        manifest_entries.append((f"Pictures/page_{pag['index']}.png", "image/png"))
    for full_path, media_type in manifest_entries:
        ET.SubElement(manifest, q(NS_MANIFEST, "file-entry"), {
            q(NS_MANIFEST, "full-path"): full_path,
            q(NS_MANIFEST, "media-type"): media_type,
        })
    manifest_xml = ET.tostring(manifest, encoding="utf-8", xml_declaration=True)

    # ── 2. meta.xml ──
    meta_doc = ET.Element(q(NS_OFFICE, "document-meta"), {q(NS_OFFICE, "version"): "1.2"})
    meta_el = ET.SubElement(meta_doc, q(NS_OFFICE, "meta"))
    ET.SubElement(meta_el, q(NS_DC, "title")).text = f"Ficha T20 - {personagem.cabecalho.nome or 'Personagem'}"
    ET.SubElement(meta_el, q(NS_META, "generator")).text = "T20 System Exporter"
    ET.SubElement(meta_el, q(NS_META, "creation-date")).text = datetime.now().isoformat(timespec="seconds")
    meta_xml = ET.tostring(meta_doc, encoding="utf-8", xml_declaration=True)

    # ── 3. styles.xml ──
    styles_doc = ET.Element(q(NS_OFFICE, "document-styles"), {q(NS_OFFICE, "version"): "1.2"})
    auto_styles_s = ET.SubElement(styles_doc, q(NS_OFFICE, "automatic-styles"))

    pm1 = ET.SubElement(auto_styles_s, q(NS_STYLE, "page-layout"), {q(NS_STYLE, "name"): "PM1"})
    ET.SubElement(pm1, q(NS_STYLE, "page-layout-properties"), {
        q(NS_FO, "margin-top"): "0cm",
        q(NS_FO, "margin-bottom"): "0cm",
        q(NS_FO, "margin-left"): "0cm",
        q(NS_FO, "margin-right"): "0cm",
        q(NS_FO, "page-width"): w_cm,
        q(NS_FO, "page-height"): h_cm,
        q(NS_STYLE, "print-orientation"): "portrait",
    })

    dp1 = ET.SubElement(auto_styles_s, q(NS_STYLE, "style"), {
        q(NS_STYLE, "name"): "dp1",
        q(NS_STYLE, "family"): "drawing-page",
    })
    ET.SubElement(dp1, q(NS_STYLE, "drawing-page-properties"), {
        q(NS_DRAW, "background-size"): "full",
        q(NS_DRAW, "fill"): "none",
    })

    master_styles = ET.SubElement(styles_doc, q(NS_OFFICE, "master-styles"))
    layer_set = ET.SubElement(master_styles, q(NS_DRAW, "layer-set"))
    ET.SubElement(layer_set, q(NS_DRAW, "layer"), {
        q(NS_DRAW, "name"): "background",
        q(NS_DRAW, "protected"): "true",
    })
    ET.SubElement(layer_set, q(NS_DRAW, "layer"), {
        q(NS_DRAW, "name"): "layout",
    })
    ET.SubElement(master_styles, q(NS_STYLE, "master-page"), {
        q(NS_STYLE, "name"): "Default",
        q(NS_STYLE, "page-layout-name"): "PM1",
        q(NS_DRAW, "style-name"): "dp1",
    })
    styles_xml = ET.tostring(styles_doc, encoding="utf-8", xml_declaration=True)

    # ── 4. content.xml ──
    content_doc = ET.Element(q(NS_OFFICE, "document-content"), {q(NS_OFFICE, "version"): "1.2"})
    font_decls = ET.SubElement(content_doc, q(NS_OFFICE, "font-face-decls"))
    ET.SubElement(font_decls, q(NS_STYLE, "font-face"), {
        q(NS_STYLE, "name"): "Liberation Sans",
        q(NS_SVG, "font-family"): "'Liberation Sans', Arial, sans-serif",
        q(NS_STYLE, "font-family-generic"): "swiss",
        q(NS_STYLE, "font-pitch"): "variable",
    })

    auto_styles_c = ET.SubElement(content_doc, q(NS_OFFICE, "automatic-styles"))

    # Estilo gráfico do fundo (imagem sem borda)
    gr_bg = ET.SubElement(auto_styles_c, q(NS_STYLE, "style"), {
        q(NS_STYLE, "name"): "gr_bg",
        q(NS_STYLE, "family"): "graphic",
    })
    ET.SubElement(gr_bg, q(NS_STYLE, "graphic-properties"), {
        q(NS_DRAW, "stroke"): "none",
        q(NS_DRAW, "fill"): "none",
    })

    # Estilo gráfico para campos de 1 linha (centralizado verticalmente)
    gr_single = ET.SubElement(auto_styles_c, q(NS_STYLE, "style"), {
        q(NS_STYLE, "name"): "gr_single",
        q(NS_STYLE, "family"): "graphic",
    })
    ET.SubElement(gr_single, q(NS_STYLE, "graphic-properties"), {
        q(NS_DRAW, "stroke"): "none",
        q(NS_DRAW, "fill"): "none",
        q(NS_FO, "padding-top"): "0.01cm",
        q(NS_FO, "padding-bottom"): "0.01cm",
        q(NS_FO, "padding-left"): "0.03cm",
        q(NS_FO, "padding-right"): "0.03cm",
        q(NS_DRAW, "textarea-vertical-align"): "middle",
    })

    # Estilo gráfico para campos multilinha (alinhado no topo)
    gr_multi = ET.SubElement(auto_styles_c, q(NS_STYLE, "style"), {
        q(NS_STYLE, "name"): "gr_multi",
        q(NS_STYLE, "family"): "graphic",
    })
    ET.SubElement(gr_multi, q(NS_STYLE, "graphic-properties"), {
        q(NS_DRAW, "stroke"): "none",
        q(NS_DRAW, "fill"): "none",
        q(NS_FO, "padding-top"): "0.04cm",
        q(NS_FO, "padding-bottom"): "0.04cm",
        q(NS_FO, "padding-left"): "0.06cm",
        q(NS_FO, "padding-right"): "0.06cm",
        q(NS_DRAW, "textarea-vertical-align"): "top",
    })

    # Cache dinâmico de estilos de parágrafo/texto por (tamanho_pt, alinhamento, negrito)
    text_styles_criados: dict[tuple[str, str, bool], str] = {}

    def _obter_estilo_texto(font_pt: float, align: str, bold: bool = False) -> str:
        size_key = f"{font_pt:.1f}pt"
        chave = (size_key, align, bold)
        if chave in text_styles_criados:
            return text_styles_criados[chave]
        nome_estilo = f"P_{len(text_styles_criados) + 1}"
        st = ET.SubElement(auto_styles_c, q(NS_STYLE, "style"), {
            q(NS_STYLE, "name"): nome_estilo,
            q(NS_STYLE, "family"): "paragraph",
        })
        ET.SubElement(st, q(NS_STYLE, "paragraph-properties"), {
            q(NS_FO, "text-align"): align,
            q(NS_FO, "line-height"): "110%",
        })
        text_props = {
            q(NS_STYLE, "font-name"): "Liberation Sans",
            q(NS_FO, "font-size"): size_key,
            q(NS_FO, "color"): "#111111",
        }
        if bold:
            text_props[q(NS_FO, "font-weight")] = "bold"
        ET.SubElement(st, q(NS_STYLE, "text-properties"), text_props)
        text_styles_criados[chave] = nome_estilo
        return nome_estilo

    body = ET.SubElement(content_doc, q(NS_OFFICE, "body"))
    drawing = ET.SubElement(body, q(NS_OFFICE, "drawing"))

    for pag in paginas:
        page_el = ET.SubElement(drawing, q(NS_DRAW, "page"), {
            q(NS_DRAW, "name"): f"page{pag['index']}",
            q(NS_DRAW, "style-name"): "dp1",
            q(NS_DRAW, "master-page-name"): "Default",
        })

        # Camada de fundo: imagem fiel do template oficial
        bg_frame = ET.SubElement(page_el, q(NS_DRAW, "frame"), {
            q(NS_DRAW, "name"): f"Fundo_Pagina_{pag['index']}",
            q(NS_DRAW, "layer"): "background",
            q(NS_DRAW, "style-name"): "gr_bg",
            q(NS_SVG, "x"): "0cm",
            q(NS_SVG, "y"): "0cm",
            q(NS_SVG, "width"): _pt_cm(pag["width_pt"]),
            q(NS_SVG, "height"): _pt_cm(pag["height_pt"]),
        })
        ET.SubElement(bg_frame, q(NS_DRAW, "image"), {
            q(NS_XLINK, "href"): f"Pictures/page_{pag['index']}.png",
            q(NS_XLINK, "type"): "simple",
            q(NS_XLINK, "show"): "embed",
            q(NS_XLINK, "actuate"): "onLoad",
        })

        # Camada editável: caixas de texto nas coordenadas exatas dos campos AcroForm
        for w in pag["widgets"]:
            nome = w["name"]
            if nome not in fields_to_fill:
                continue
            val = fields_to_fill[nome]
            if val is None or val == "" or val == "/Off":
                continue

            rect_w = max(4.0, w["x1"] - w["x0"])
            rect_h = max(4.0, w["y1"] - w["y0"])
            eh_checkbox = (val == "/Yes") or (w["type"] == "CheckBox")

            if eh_checkbox:
                if val != "/Yes":
                    continue
                texto = "✕"
                font_pt = max(6.5, min(11.0, rect_h * 0.85))
                align = "center"
                bold = True
                gr_style = "gr_single"
            else:
                texto = str(val)
                multiline = w["multiline"] or ("\n" in texto) or rect_h > 36.0
                if w["fontsize"] > 0:
                    font_pt = max(6.5, min(16.0, w["fontsize"]))
                elif multiline:
                    font_pt = 7.5
                else:
                    font_pt = max(6.5, min(12.0, rect_h * 0.62))

                eh_esquerda = (
                    multiline
                    or nome in _CAMPOS_ALINHADOS_ESQUERDA
                    or nome.startswith(("Ataque ", "Item"))
                )
                align = "start" if eh_esquerda else "center"
                bold = nome in ("NOME DO PERSONAGEM", "CA", "PVs Totais", "PMs Totais") or nome.startswith("Mod")
                gr_style = "gr_multi" if multiline else "gr_single"

            p_style = _obter_estilo_texto(font_pt, align, bold)

            frame = ET.SubElement(page_el, q(NS_DRAW, "frame"), {
                q(NS_DRAW, "name"): nome,
                q(NS_DRAW, "layer"): "layout",
                q(NS_DRAW, "style-name"): gr_style,
                q(NS_SVG, "x"): _pt_cm(w["x0"]),
                q(NS_SVG, "y"): _pt_cm(w["y0"]),
                q(NS_SVG, "width"): _pt_cm(rect_w),
                q(NS_SVG, "height"): _pt_cm(rect_h),
            })
            tbox = ET.SubElement(frame, q(NS_DRAW, "text-box"))
            for linha in texto.split("\n"):
                p = ET.SubElement(tbox, q(NS_TEXT, "p"), {q(NS_TEXT, "style-name"): p_style})
                p.text = linha

    content_xml = ET.tostring(content_doc, encoding="utf-8", xml_declaration=True)

    # ── 5. Empacotamento ZIP ODF 1.2 (mimetype sem compressão em 1º lugar) ──
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", _ODG_MIMETYPE.encode("ascii"), compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/manifest.xml", manifest_xml)
        zf.writestr("meta.xml", meta_xml)
        zf.writestr("styles.xml", styles_xml)
        zf.writestr("content.xml", content_xml)
        for pag in paginas:
            zf.writestr(f"Pictures/page_{pag['index']}.png", pag["png"], compress_type=zipfile.ZIP_STORED)

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


@router.get("/{personagem_id}/odg")
async def gerar_odg(personagem_id: str, db=Depends(get_db)):
    """Gera ficha editável no formato LibreOffice Draw (.odg) usando o PDF oficial como base."""
    try:
        try:
            oid = ObjectId(personagem_id)
        except Exception:
            raise HTTPException(status_code=404, detail="ID inválido")

        personagem_doc = await db.personagens.find_one({"_id": oid})
        if not personagem_doc:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")

        personagem = Personagem(**personagem_doc)
        odg_bytes = gerar_odg_bytes(personagem)
        nome_slug = _sanitizar_nome_arquivo(personagem.cabecalho.nome)

        return Response(
            content=odg_bytes,
            media_type=_ODG_MIMETYPE,
            headers={"Content-Disposition": f"attachment; filename=ficha-{nome_slug}.odg"},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar ODG: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ODG: {str(e)}")
