"""Motor de Condições (Apêndice, T20 Jogo do Ano, p.394–395).

Regras oficiais:
- Condições com os mesmos efeitos não se acumulam; aplica-se apenas o mais severo
  (ex.: Desprevenido –5 e Vulnerável –2 → –5 na Defesa, não –7).
- Exceção explícita: Caído (–5 Defesa corpo a corpo, +5 à distância) é cumulativo.
- Sub-condições implícitas são expandidas recursivamente (ex.: Petrificado → Inconsciente → Indefeso → Desprevenido).
- Condições repetidas escalam conforme o texto oficial (Abalado → Apavorado, Fatigado → Exausto, etc.).
- Lento reduz o deslocamento à metade arredondando para baixo para o incremento de 1,5m.
"""
import math
import unicodedata
from typing import Iterable, List, Set

from ..dados_condicoes import DADOS_CONDICOES


def _norm(txt: str) -> str:
    s = unicodedata.normalize("NFD", (txt or "").strip().lower())
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn").replace("_", " ")


_MAPA_CONDICOES_NORM = {_norm(k): k for k in DADOS_CONDICOES}


def normalizar_nome_condicao(nome: str):
    """Resolve um nome/slug de condição para o nome canônico em DADOS_CONDICOES, ou None."""
    return _MAPA_CONDICOES_NORM.get(_norm(nome))


def expandir_condicoes(condicoes: Iterable[str]) -> Set[str]:
    """Expande todas as condições oficiais presentes e suas sub-condições implícitas."""
    resultado: Set[str] = set()
    pilha: List[str] = []
    for c in (condicoes or []):
        canon = normalizar_nome_condicao(c)
        if canon:
            pilha.append(canon)
    while pilha:
        atual = pilha.pop()
        if atual in resultado:
            continue
        resultado.add(atual)
        for sub in DADOS_CONDICOES[atual].get("inclui", []):
            if sub not in resultado:
                pilha.append(sub)
    return resultado


def aplicar_condicao_com_escalonamento(condicoes_atuais: Iterable[str], nova_condicao: str) -> List[str]:
    """Adiciona uma condição aplicando o escalonamento oficial quando repetida (T20 JdA p.394–395)."""
    lista = list(condicoes_atuais or [])
    canon = normalizar_nome_condicao(nova_condicao)
    if not canon:
        if nova_condicao not in lista:
            lista.append(nova_condicao)
        return lista

    ja_tem = any(normalizar_nome_condicao(c) == canon for c in lista)
    escala = DADOS_CONDICOES[canon].get("escala_para")
    if ja_tem and escala:
        lista = [c for c in lista if normalizar_nome_condicao(c) != canon]
        if not any(normalizar_nome_condicao(c) == escala for c in lista):
            lista.append(escala)
    elif not ja_tem:
        lista.append(canon)
    return lista


def calcular_deslocamento_lento(deslocamento: float) -> float:
    """Metade do deslocamento arredondado para baixo para o primeiro incremento de 1,5m (p.395)."""
    metade = max(0.0, float(deslocamento or 0.0)) / 2.0
    return math.floor(metade / 1.5) * 1.5


def calcular_efeitos_condicoes(condicoes: Iterable[str], deslocamento_base: float = 9.0) -> dict:
    """Consolida os efeitos mecânicos das condições ativas respeitando não-acúmulo (p.394–395)."""
    ativas = expandir_condicoes(condicoes)
    defesa = 0
    defesa_cac = 0
    defesa_dist = 0
    pericias_todas = 0
    pericias_fisicas = 0
    pericias_mentais = 0
    pericias_for_des = 0
    pericias_especificas = {}
    ataque = 0
    ataque_cac = 0
    custo_pm_extra = 0
    penalidade_armadura = 0
    rd = 0
    falha_reflexos = False
    deslocamento_fixo = None
    tem_lento = False
    deslocamento_bonus = 0.0

    for nome in ativas:
        ef = DADOS_CONDICOES[nome].get("efeitos", {})
        if "defesa" in ef:
            defesa = min(defesa, ef["defesa"])
        if "defesa_cac" in ef:
            defesa_cac += ef["defesa_cac"]  # Caído é cumulativo
        if "defesa_dist" in ef:
            defesa_dist += ef["defesa_dist"]
        if "pericias_todas" in ef:
            pericias_todas = min(pericias_todas, ef["pericias_todas"])
        if "pericias_fisicas" in ef:
            pericias_fisicas = min(pericias_fisicas, ef["pericias_fisicas"])
        if "pericias_mentais" in ef:
            pericias_mentais = min(pericias_mentais, ef["pericias_mentais"])
        if "pericias_for_des" in ef:
            pericias_for_des = min(pericias_for_des, ef["pericias_for_des"])
        for p_nome, p_val in (ef.get("pericias_especificas") or {}).items():
            prev = pericias_especificas.get(p_nome, 0)
            pericias_especificas[p_nome] = min(prev, p_val)
        if "ataque" in ef:
            ataque = min(ataque, ef["ataque"])
        if "ataque_cac" in ef:
            ataque_cac = min(ataque_cac, ef["ataque_cac"])
        if "custo_pm_extra" in ef:
            custo_pm_extra = max(custo_pm_extra, ef["custo_pm_extra"])
        if "penalidade_armadura" in ef:
            penalidade_armadura = max(penalidade_armadura, ef["penalidade_armadura"])
        if "rd" in ef:
            rd = max(rd, ef["rd"])
        if ef.get("falha_automatica_reflexos"):
            falha_reflexos = True
        if "deslocamento_fixo" in ef:
            val_fixo = float(ef["deslocamento_fixo"])
            deslocamento_fixo = val_fixo if deslocamento_fixo is None else min(deslocamento_fixo, val_fixo)
        if ef.get("deslocamento_metade"):
            tem_lento = True
        if "deslocamento_bonus" in ef:
            deslocamento_bonus = min(deslocamento_bonus, float(ef["deslocamento_bonus"]))

    # Deslocamento final sob condições
    desl = float(deslocamento_base)
    if deslocamento_fixo is not None:
        desl = min(desl, deslocamento_fixo)
    else:
        if deslocamento_bonus:
            desl = max(0.0, desl + deslocamento_bonus)
        if tem_lento:
            desl = calcular_deslocamento_lento(desl)

    return {
        "condicoes_efetivas": sorted(ativas),
        "defesa": defesa,
        "defesa_cac": defesa_cac,
        "defesa_dist": defesa_dist,
        "pericias_todas": pericias_todas,
        "pericias_fisicas": pericias_fisicas,
        "pericias_mentais": pericias_mentais,
        "pericias_for_des": pericias_for_des,
        "pericias_especificas": pericias_especificas,
        "ataque": ataque,
        "ataque_cac": ataque_cac,
        "custo_pm_extra": custo_pm_extra,
        "penalidade_armadura": penalidade_armadura,
        "rd": rd,
        "falha_automatica_reflexos": falha_reflexos,
        "deslocamento": desl,
    }
