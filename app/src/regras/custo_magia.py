"""Lote R5 — Motor de custo de magia (T20 JdA, Capítulo 4).

Regras oficiais implementadas:
- Base = Tabela 4-1 por círculo (1/3/6/10/15 PM)
- Aprimoramentos somam PM (cumulativos "aumenta" até o limite de PM = nível)
- Truque: custo 0 e não combina com outros aprimoramentos
- Reduções multiplicativas (Alta Arcana ×0.5, arredonda p/ baixo)
- Reduções fixas por magia (reducao_custo_magia racial)
- Custo mínimo 1 PM (0 apenas para Truque)
- CD = 10 + metade do nível + atributo-chave (exposta p/ tooltip)
"""
import math
import logging
from typing import Optional

from ..models import Personagem, StatCalculado, FonteBonus

logger = logging.getLogger("RegrasT20")

CUSTO_POR_CIRCULO = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}


def _circulo_int(magia) -> int:
    try:
        return int(magia.circulo)
    except Exception:
        return 1


def calcular_cd_magia(ficha: Personagem, magia) -> int:
    """CD = 10 + metade do nível + modificador do atributo-chave + bônus de escola.

    Se a magia tiver 'escola' preenchida, soma o bônus específico dessa escola
    (ex.: Especialista em Escola +2). Bônus por resistência (Familiar) NÃO entra
    aqui — vai nos testes de resistência, não na CD da magia.
    """
    from .utils import calcular_modificador
    attr = (magia.atributo_chave or "").lower()
    mapa = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
    val = getattr(ficha.atributos, mapa.get(attr, ''), 0) or 0
    cd_base = 10 + math.floor((ficha.cabecalho.nivel_total or 1) / 2) + calcular_modificador(val)
    escola = (magia.escola or "").strip()
    cd_escola = (getattr(ficha.combate, "cd_por_escola", None) or {}).get(escola, 0)

    # Arte Mágica (Bardo, T20 p.43): sob efeito de Inspiração, CD das habilidades de bardo +2
    cd_inspiracao = 0
    condicoes = getattr(ficha, "condicoes_ativas", None) or []
    if "inspiracao" in condicoes:
        for hab in ficha.habilidades:
            efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
            v_cd = efeitos.get("cd_bardo_inspiracao")
            if v_cd:
                cd_inspiracao += int(v_cd)
            elif (hab.nome or "") == "Arte Mágica":
                cd_inspiracao += 2

    # Liturgia Mágica (Clérigo, T20 p.58): +2 CD na próxima habilidade de clérigo
    cd_liturgia = 0
    if "liturgia_magica" in condicoes:
        for hab in ficha.habilidades:
            v_lit = (hab.efeitos or {}).get("cd_clerigo_liturgia")
            if v_lit:
                cd_liturgia += int(v_lit)
            elif (hab.nome or "") == "Liturgia Mágica":
                cd_liturgia += 2

    # Força da Natureza (Druida 20º, T20 p.62): +2 CD (+4 em terrenos naturais)
    cd_forca_nat = 0
    for hab in ficha.habilidades:
        if (hab.efeitos or {}).get("forca_da_natureza") or (hab.nome or "") == "Força da Natureza":
            cd_forca_nat += 4 if "terreno_natural" in condicoes else 2
            break

    return cd_base + cd_escola + cd_inspiracao + cd_liturgia + cd_forca_nat


def calcular_custo_magia(ficha: Personagem, magia,
                         aprimoramentos_pm: int = 0,
                         eh_truque: bool = False) -> StatCalculado:
    circulo = _circulo_int(magia)
    base = CUSTO_POR_CIRCULO.get(circulo, 1)
    calc = StatCalculado(base=base, total=base)
    calc.fontes.append(FonteBonus(
        fonte=f"Custo do {circulo}º círculo (Tabela 4-1)", categoria="Base", valor=base))

    # Truque: custo zero, sem outros aprimoramentos
    if eh_truque:
        calc.adicionar_bonus("Truque (versão simples)", "Truque", -base)
        calc.total = 0
        return calc

    total = base
    if aprimoramentos_pm:
        total += aprimoramentos_pm
        calc.adicionar_bonus("Aprimoramentos", "Aprimoramento", aprimoramentos_pm)

    # Reduções multiplicativas (Alta Arcana ×0.5) — arredonda p/ baixo
    for hab in ficha.habilidades:
        efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
        mult = efeitos.get("reducao_custo_magia_global")
        if isinstance(mult, (int, float)) and 0 < mult < 1:
            antes = total
            total = math.floor(total * mult)
            calc.adicionar_bonus(f"{hab.nome} (×{mult})", "Multiplicativo", total - antes)

    # Reduções fixas por magia (racial: reducao_custo_magia {"nomes": [...], "valor": N})
    for hab in ficha.habilidades:
        rc = (hab.efeitos or {}).get("reducao_custo_magia")
        if isinstance(rc, dict) and magia.nome in (rc.get("nomes") or []):
            valor = int(rc.get("valor", 1))
            total -= valor
            calc.adicionar_bonus(f"{hab.nome} (−{valor} PM)", "Redução", -valor)

    # Reduções se a magia já é conhecida de outra fonte (Qareen/Sereia/Bardo)
    for hab in ficha.habilidades:
        efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
        for chave in ("reducao_custo_se_conhecida", "reducao_custo_reaprendizado"):
            valor = efeitos.get(chave)
            if isinstance(valor, (int, float)) and valor and _ja_conhecida_de_outra_fonte(ficha, magia, f"Racial: {hab.nome}"):
                total -= int(valor)
                calc.adicionar_bonus(f"{hab.nome} (−{int(valor)} PM, reaprendizado)", "Reaprendizado", -int(valor))

    # Redução por tipo de dano (Linhagem Draconica Aprimorada: -1 PM em magias
    # do tipo escolhido, ex.: fogo, frio, eletricidade, acido).
    tipo_magia = (magia.tipo or "").strip().lower()
    reducoes_tipo = getattr(ficha.combate, "reducao_pm_tipo", None) or {}
    if tipo_magia and tipo_magia in reducoes_tipo:
        red = reducoes_tipo[tipo_magia]
        total -= red
        calc.adicionar_bonus(
            f"Linhagem Draconica ({tipo_magia}, -{red} PM)", "Reducao", -red)

    # Bônus por escola (Mestre em Escola: -1 PM na escola escolhida)
    escola = (magia.escola or "").strip()
    reducao_escola = (getattr(ficha.combate, "custo_por_escola", None) or {}).get(escola, 0)
    if reducao_escola:
        total += reducao_escola  # valores negativos em custo_por_escola
        calc.adicionar_bonus(
            f"Poder: Mestre em Escola ({escola})", "Poder", reducao_escola)

    # Símbolo Sagrado Energizado (Clérigo, T20 p.58): -1 PM em magias divinas
    condicoes = getattr(ficha, "condicoes_ativas", None) or []
    if "simbolo_energizado" in condicoes:
        eh_divina = (
            "divin" in tipo_magia
            or "universal" in tipo_magia
            or (not tipo_magia and any((c.nome or "") == "Clérigo" for c in (ficha.classes or [])))
        )
        if eh_divina:
            for hab in ficha.habilidades:
                red_simb = (hab.efeitos or {}).get("reducao_pm_magias_divinas_energizado")
                if red_simb:
                    total -= int(red_simb)
                    calc.adicionar_bonus(
                        f"Símbolo Sagrado Energizado (−{int(red_simb)} PM)", "Poder", -int(red_simb)
                    )
                    break

    # Força da Natureza (Druida 20º, T20 p.62): -2 PM (-4 PM em terrenos naturais)
    for hab in ficha.habilidades:
        if (hab.efeitos or {}).get("forca_da_natureza") or (hab.nome or "") == "Força da Natureza":
            red_fn = 4 if "terreno_natural" in condicoes else 2
            total -= red_fn
            calc.adicionar_bonus(f"Força da Natureza (−{red_fn} PM)", "Poder", -red_fn)
            break

    # Artista Completo (Bardo 20º, T20 p.44): sob Inspiração, custo em PM reduzido
    # pela metade APÓS aplicar aprimoramentos e quaisquer outras reduções.
    if "inspiracao" in condicoes:
        tem_artista = any(
            (hab.efeitos or {}).get("reducao_custo_inspiracao_metade")
            or (hab.efeitos or {}).get("artista_completo")
            or (hab.nome or "") == "Artista Completo"
            for hab in ficha.habilidades
        )
        if tem_artista and total > 0:
            antes = total
            total = math.floor(total / 2)
            calc.adicionar_bonus("Artista Completo (×0.5 sob Inspiração)", "Multiplicativo", total - antes)

    # Mínimo 1 PM (regra confirmada); limite de gasto por magia = nível
    total = max(1, total)
    limite_pm = max(1, ficha.cabecalho.nivel_total or 1)
    if total > limite_pm:
        antes_limite = total
        total = limite_pm
        calc.adicionar_bonus(
            f"Limite de PM por magia (nível {limite_pm})",
            "Limite",
            total - antes_limite,
        )
    calc.total = total
    return calc


# 🆕 Regras complementares (T20 JdA, cap. 4): redução se magia já é conhecida
# - reducao_custo_magia: sempre aplica (ex.: Dahllan, Suraggel, Dhampir)
# - reducao_custo_se_conhecida: aplica se a magia já está no Grimório
#   (ex.: Qareen/Sereia — "se aprender novamente, custo −1 PM")
# - reducao_custo_reaprendizado: idem (ex.: Bardo — reaprender reduz custo)
def _ja_conhecida_de_outra_fonte(ficha: Personagem, magia, fonte_atual: str) -> bool:
    """Verifica se a magia já existe no Grimório com uma fonte diferente."""
    for m in ficha.combate.magias:
        if m.nome == magia.nome and (m.fonte_origem or "") != fonte_atual:
            return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# CAPÍTULO 4 — MAGIA (T20 JdA, p.170–172)
# ══════════════════════════════════════════════════════════════════════════════

ESCOLAS_MAGIA = {
    "Abjuração": {
        "sigla": "Abjur",
        "tipo_efeito": None,
        "descricao": "Magias de proteção, que anulam outras magias ou expulsam criaturas invocadas de volta a seus planos de existência nativos.",
    },
    "Adivinhação": {
        "sigla": "Adiv",
        "tipo_efeito": None,
        "descricao": "Magias de detecção ou que vasculham passado e futuro.",
    },
    "Convocação": {
        "sigla": "Conv",
        "tipo_efeito": None,
        "descricao": "Magias que transportam matéria através do Éter Entre Mundos. Criaturas convocadas surgem em superfície desocupada.",
    },
    "Encantamento": {
        "sigla": "Encan",
        "tipo_efeito": "mental",
        "descricao": "Magias que afetam a mente. Todas as magias de encantamento são efeitos mentais.",
    },
    "Evocação": {
        "sigla": "Evoc",
        "tipo_efeito": None,
        "energias": ["Ácido", "Eletricidade", "Fogo", "Frio", "Luz", "Essência"],
        "descricao": "Magias que manipulam ou geram energia pura (ácido, eletricidade, fogo, frio, luz e essência).",
    },
    "Ilusão": {
        "sigla": "Ilusão",
        "tipo_efeito": "mental",
        "descricao": "Magias que fazem outros perceberem algo que não existe ou ignorarem algo real. Todas são efeitos mentais.",
    },
    "Necromancia": {
        "sigla": "Necro",
        "tipo_efeito": "trevas",
        "descricao": "Magias que canalizam energia negativa, criando escuridão, drenando força vital e criando mortos-vivos. São efeitos de trevas.",
    },
    "Transmutação": {
        "sigla": "Trans",
        "tipo_efeito": None,
        "descricao": "Magias que alteram as propriedades físicas de uma criatura ou objeto.",
    },
}

# T20 JdA p.170: Atributo-chave por classe/subclasse conjuradora
ATRIBUTO_CHAVE_POR_CLASSE = {
    "Arcanista": "inteligencia",  # Bruxo e Mago (Feiticeiro usa carisma)
    "Bruxo": "inteligencia",
    "Mago": "inteligencia",
    "Feiticeiro": "carisma",
    "Bardo": "carisma",
    "Clérigo": "sabedoria",
    "Druida": "sabedoria",
}

CLASSES_CONJURADORAS_ARCANAS = {"Arcanista", "Bardo", "Bruxo", "Mago", "Feiticeiro"}
CLASSES_CONJURADORAS_DIVINAS = {"Clérigo", "Druida"}


def obter_atributo_chave_magia(ficha: Personagem, classe_nome: Optional[str] = None) -> Optional[str]:
    """Retorna o atributo-chave de magia da classe conjuradora (T20 JdA p.170)."""
    for c in (ficha.classes or []):
        nome = (c.nome or "").strip()
        if classe_nome and nome != classe_nome:
            continue
        sub = (c.subclasse or "").strip()
        if nome == "Arcanista":
            return "carisma" if sub == "Feiticeiro" else "inteligencia"
        if nome in ATRIBUTO_CHAVE_POR_CLASSE:
            return ATRIBUTO_CHAVE_POR_CLASSE[nome]
    return None


def calcular_cd_magias_ficha(ficha: Personagem) -> Optional[int]:
    """Calcula e grava ficha.combate.cd_magias e cd_magias_calc para TODAS as
    classes conjuradoras (Arcanista, Bardo, Clérigo, Druida) — T20 JdA p.172.

    Fórmula: 10 + metade do nível do personagem + atributo-chave + bônus.
    """
    from .utils import calcular_modificador

    attr_chave = obter_atributo_chave_magia(ficha)
    if not attr_chave:
        return None

    cd_calc = StatCalculado(base=10, total=10)
    nivel_pers = int(ficha.cabecalho.nivel_total or 1)
    metade_nivel = math.floor(nivel_pers / 2)
    if metade_nivel:
        cd_calc.adicionar_bonus(
            fonte=f"Nível ({metade_nivel})", categoria="Nível", valor=metade_nivel
        )

    mod_attr = calcular_modificador(getattr(ficha.atributos, attr_chave, 0))
    if mod_attr:
        cd_calc.adicionar_bonus(
            fonte=f"Atributo: {attr_chave.upper()}", categoria="Atributo", valor=mod_attr
        )

    condicoes = getattr(ficha, "condicoes_ativas", None) or []

    # Fortalecimento Arcano (Arcanista)
    if any((h.nome or "") == "Fortalecimento Arcano" for h in ficha.habilidades):
        cd_calc.adicionar_bonus(
            fonte="Poder: Fortalecimento Arcano",
            categoria="Poder",
            valor=2 if (ficha.combate.circulo_maximo or 0) >= 4 else 1,
        )

    # Magia Pungente (buff ativo)
    for b in ficha.status.buffs:
        if b.origem == "Magia Pungente" and b.atributo == "cd_magias":
            cd_calc.adicionar_bonus(
                fonte="Magia Pungente (ativa)", categoria="Poder", valor=b.valor
            )

    # Arte Mágica (Bardo sob Inspiração): +2 CD
    if "inspiracao" in condicoes:
        for hab in ficha.habilidades:
            efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
            v_cd = efeitos.get("cd_bardo_inspiracao")
            if v_cd:
                cd_calc.adicionar_bonus(fonte=f"Poder: {hab.nome}", categoria="Poder", valor=int(v_cd))
            elif (hab.nome or "") == "Arte Mágica":
                cd_calc.adicionar_bonus(fonte="Poder: Arte Mágica", categoria="Poder", valor=2)

    # Liturgia Mágica (Clérigo): +2 CD
    if "liturgia_magica" in condicoes:
        for hab in ficha.habilidades:
            v_lit = (hab.efeitos or {}).get("cd_clerigo_liturgia")
            if v_lit:
                cd_calc.adicionar_bonus(fonte=f"Poder: {hab.nome}", categoria="Poder", valor=int(v_lit))
            elif (hab.nome or "") == "Liturgia Mágica":
                cd_calc.adicionar_bonus(fonte="Poder: Liturgia Mágica", categoria="Poder", valor=2)

    # Força da Natureza (Druida 20º): +2 CD (+4 em terrenos naturais)
    for hab in ficha.habilidades:
        if (hab.efeitos or {}).get("forca_da_natureza") or (hab.nome or "") == "Força da Natureza":
            val_fn = 4 if "terreno_natural" in condicoes else 2
            cd_calc.adicionar_bonus(fonte="Poder: Força da Natureza", categoria="Poder", valor=val_fn)
            break

    ficha.combate.cd_magias_calc = cd_calc
    ficha.combate.cd_magias = cd_calc.total
    return cd_calc.total


def calcular_cd_concentracao(custo_pm: int, situacao: str, dano: int = 0) -> int:
    """Calcula a CD do teste de Vontade para Concentração (T20 JdA p.170).

    situacao:
      - 'ferido': CD igual ao dano sofrido durante a execução
      - 'ruim': CD 15 + custo em PM (montado a galope, caído, tempestade)
      - 'terrivel': CD 20 + custo em PM (carroça desgovernada, agarrado, terremoto)
    """
    sit = (situacao or "").strip().lower()
    if sit == "ferido":
        return max(0, int(dano or 0))
    if sit == "ruim":
        return 15 + max(0, int(custo_pm or 0))
    if sit in ("terrivel", "terrível"):
        return 20 + max(0, int(custo_pm or 0))
    raise ValueError(f"Situação de concentração inválida: {situacao!r}")


def verificar_armadura_magia_arcana(ficha: Personagem, magia, custo_pm: Optional[int] = None) -> dict:
    """Verifica se lançar a magia exige teste de Misticismo por armadura (T20 JdA p.170).

    Regra: Lançar magia arcana usando armadura exige teste de Misticismo
    (CD 20 + custo em PM da magia), sofrendo penalidade de armadura.
    Magias lançadas por habilidades de raça, poderes ou itens mágicos não sofrem
    esta limitação (isento_armadura=True). Bardo pode lançar magias arcanas com
    armadura leve sem teste (T20 JdA p.43).
    """
    from ..dados_equipamentos import DADOS_ARMADURAS

    custo = int(custo_pm) if custo_pm is not None else CUSTO_POR_CIRCULO.get(_circulo_int(magia), 1)
    fonte_txt = f"{getattr(magia, 'fonte', '') or ''} {getattr(magia, 'fonte_origem', '') or ''}".lower()

    if getattr(magia, "isento_armadura", False) or any(
        tag in fonte_txt for tag in ("racial:", "habilidade:", "poder:", "item:")
    ):
        return {"exige_teste": False, "pericia": "Misticismo", "cd": 0, "motivo": "Isento (raça, poder ou item mágico)"}

    tipo_magia = (getattr(magia, "tipo", "") or "").strip().lower()
    if tipo_magia == "divina":
        return {"exige_teste": False, "pericia": "Misticismo", "cd": 0, "motivo": "Magia divina"}

    # Verifica se está vestindo alguma armadura equipada (escudos não atrapalham)
    armadura_equipada = None
    for item in (ficha.inventario.equipamentos or []):
        if not getattr(item, "equipado", False):
            continue
        dados_arm = DADOS_ARMADURAS.get(item.nome)
        if dados_arm and dados_arm.get("tipo_armadura") in ("Leve", "Pesada"):
            armadura_equipada = dados_arm
            break

    if not armadura_equipada:
        return {"exige_teste": False, "pericia": "Misticismo", "cd": 0, "motivo": "Sem armadura equipada"}

    # Bardo pode lançar magias arcanas com armadura leve sem teste (T20 JdA p.43)
    eh_bardo = any((c.nome or "") == "Bardo" for c in (ficha.classes or []))
    if eh_bardo and armadura_equipada.get("tipo_armadura") == "Leve":
        return {"exige_teste": False, "pericia": "Misticismo", "cd": 0, "motivo": "Bardo com armadura leve"}

    return {
        "exige_teste": True,
        "pericia": "Misticismo",
        "cd": 20 + custo,
        "motivo": f"Magia arcana com armadura {armadura_equipada.get('tipo_armadura', '').lower()}",
    }


def pode_usar_aprimoramento(ficha: Personagem, magia, circulo_requerido: int) -> bool:
    """Verifica pré-requisito de círculo de um aprimoramento (T20 JdA p.171).

    Para magias de classe, o personagem deve conseguir lançar o círculo exigido.
    Para magias utilizadas de outra forma (raça/poder/item), não cumpre pré-requisitos
    de círculo (salvo exceções explícitas no poder).
    """
    req = int(circulo_requerido or 1)
    if req <= 1:
        return True
    fonte_txt = f"{getattr(magia, 'fonte', '') or ''} {getattr(magia, 'fonte_origem', '') or ''}".lower()
    if getattr(magia, "isento_armadura", False) or any(
        tag in fonte_txt for tag in ("racial:", "habilidade:", "poder:", "item:")
    ):
        return False
    return (ficha.combate.circulo_maximo or 0) >= req


PARES_OPOSTOS_CONTRAMAGICA = {
    ("luz", "escuridão"),
    ("escuridão", "luz"),
}


def pode_anular_magia(magia_contra, magia_alvo) -> dict:
    """Avalia se magia_contra pode ser usada como contramágica de magia_alvo (T20 JdA p.172).

    - Dissipar Magia anula qualquer magia (mesmo de círculo maior) com teste oposto
      de Misticismo vs Misticismo/Vontade.
    - Uma magia igual (ou par oposto como Luz/Escuridão) anula automaticamente se
      seu círculo for >= ao da magia alvo (uma magia nunca anula outra de círculo maior).
    """
    nome_c = (getattr(magia_contra, "nome", "") or "").strip().lower()
    nome_a = (getattr(magia_alvo, "nome", "") or "").strip().lower()
    circ_c = _circulo_int(magia_contra)
    circ_a = _circulo_int(magia_alvo)

    if nome_c == "dissipar magia":
        return {
            "pode_anular": True,
            "exige_teste_oposto": True,
            "motivo": "Dissipar Magia (Misticismo oposto por Misticismo ou Vontade)",
        }

    if circ_c < circ_a:
        return {
            "pode_anular": False,
            "exige_teste_oposto": False,
            "motivo": "Uma magia nunca pode anular outra de círculo maior",
        }

    if nome_c == nome_a or (nome_c, nome_a) in PARES_OPOSTOS_CONTRAMAGICA:
        return {
            "pode_anular": True,
            "exige_teste_oposto": False,
            "motivo": "Mesma magia ou magia oposta",
        }

    return {
        "pode_anular": False,
        "exige_teste_oposto": False,
        "motivo": "Magias incompatíveis (sujeito a julgamento do mestre)",
    }

