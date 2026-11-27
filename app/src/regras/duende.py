# -*- coding: utf-8 -*-
"""Criação Aleatória de Duende — Sonhos Malucos (Heróis de Arton, p. 9–11).

Regra oficial:
  Role 1d3 (Natureza), 1d4 (Tamanho), 2d6 (dois atributos diferentes: 1=For..6=Car)
  e 3d12 (três poderes distintos da lista oficial de 12 Presentes).
  Duendes criados de forma aleatória começam com +2 PM (presente de Nimb).
"""
import random
from typing import Any, Dict, List, Optional

NATUREZAS_D3 = {
    1: ("Natureza_Animal_Duende", "Animal"),
    2: ("Natureza_Vegetal_Duende", "Vegetal"),
    3: ("Natureza_Mineral_Duende", "Mineral"),
}

TAMANHOS_D4 = {
    1: ("Tamanho_Minusculo_Duende", "Minúsculo"),
    2: ("Tamanho_Pequeno_Duende", "Pequeno"),
    3: ("Tamanho_Medio_Duende", "Médio"),
    4: ("Tamanho_Grande_Duende", "Grande"),
}

ATRIBUTOS_D6 = {
    1: "forca",
    2: "destreza",
    3: "constituicao",
    4: "inteligencia",
    5: "sabedoria",
    6: "carisma",
}

# Os 12 Presentes oficiais (Heróis de Arton, p. 9–10).
# Afinidade Elemental (1) tem 3 sub-opções (Água, Fogo, Vegetação).
PRESENTES_D12 = {
    1: ("Afinidade_Elemental", "Afinidade Elemental"),
    2: ("Encantar_Objetos_Duende", "Encantar Objetos"),
    3: ("Enfeiticar_Duende", "Enfeitiçar"),
    4: ("Invisibilidade_Duende", "Invisibilidade"),
    5: ("Lingua_Natureza_Duende", "Língua da Natureza"),
    6: ("Maldicao_Duende", "Maldição"),
    7: ("Mais_La_Duende", "Mais Lá do que Aqui"),
    8: ("Metamorfose_Duende", "Metamorfose Animal"),
    9: ("Sonhos_Profeticos_Duende", "Sonhos Proféticos"),
    10: ("Velocidade_Duende", "Velocidade do Pensamento"),
    11: ("Visao_Feerica_Duende", "Visão Feérica"),
    12: ("Voo_Duende", "Voo"),
}

AFINIDADES_ELEMENTAIS_DUENDE = [
    ("Afinidade_Agua_Duende", "Água"),
    ("Afinidade_Fogo_Duende", "Fogo"),
    ("Afinidade_Veg_Duende", "Vegetação"),
]

TABUS_EXEMPLOS_DUENDE: List[str] = [
    "Sempre remenda as roupas de qualquer mortal que esteja dormindo sob o mesmo teto que ele.",
    "Come apenas carne crua.",
    "Nunca pode ouvir um agradecimento.",
    "Sempre entra em qualquer lugar de costas.",
    "Não revela o próprio nome.",
    "Compõe um pequeno poema para todos que encontra, descrevendo a morte de cada um.",
    "Não pode ver crianças em noites de lua cheia.",
    "Nunca senta em cadeiras.",
    "Carrega sempre consigo um pote fechado. Diz que ali dentro está seu coração.",
    "Usa sapatos muito pequenos e reclama de dor nos pés o tempo todo.",
    "Age como se estivesse paralisado se qualquer quantidade de sal tocar sua pele.",
    "Um dia por semana, atende por um nome diferente e demonstra personalidade um pouco diferente.",
    "Varre qualquer cômodo onde esteja.",
    "Tem pavor do próprio reflexo.",
    "Nunca pode aceitar um favor sem pagar pelo menos uma moeda.",
    "Ao passar na frente de qualquer templo, cobre os olhos com uma venda.",
    "Rouba um garfo de qualquer casa na qual entre.",
    "Precisa atravessar todos os espinheiros que encontra em seu caminho.",
    "Sempre responde uma pergunta com outra pergunta.",
    "Não pode falar a verdade durante um dia inteiro por mês (sem avisar ninguém).",
    "Em intervalos aleatórios, lembra que está atrasado para um compromisso importante e some por horas.",
    "Não pode olhar pessoas feridas nos olhos.",
]


def gerar_duende_aleatorio(seed: Optional[int] = None) -> Dict[str, Any]:
    """Rola 1d3, 1d4, 2d6 (sem repetição) e 3d12 (sem repetição) conforme Sonhos Malucos (p. 9)."""
    rng = random.Random(seed)

    # 1d3 Natureza
    d3 = rng.randint(1, 3)
    nat_id, nat_nome = NATUREZAS_D3[d3]

    # 1d4 Tamanho
    d4 = rng.randint(1, 4)
    tam_id, tam_nome = TAMANHOS_D4[d4]

    # 2d6 Dons (dois atributos diferentes)
    dons_dados: List[int] = []
    while len(dons_dados) < 2:
        r = rng.randint(1, 6)
        if r not in dons_dados:
            dons_dados.append(r)
    dons_atributos = [ATRIBUTOS_D6[r] for r in dons_dados]

    # 3d12 Presentes (três poderes diferentes entre os 12 oficiais)
    pres_dados: List[int] = []
    while len(pres_dados) < 3:
        r = rng.randint(1, 12)
        if r not in pres_dados:
            pres_dados.append(r)

    presentes_ids: List[str] = []
    presentes_nomes: List[str] = []
    for r in pres_dados:
        pid, pnome = PRESENTES_D12[r]
        if pid == "Afinidade_Elemental":
            sub_id, sub_nome = rng.choice(AFINIDADES_ELEMENTAIS_DUENDE)
            presentes_ids.append(sub_id)
            presentes_nomes.append(f"Afinidade Elemental ({sub_nome})")
        else:
            presentes_ids.append(pid)
            presentes_nomes.append(pnome)

    tabu_sugerido = rng.choice(TABUS_EXEMPLOS_DUENDE)

    return {
        "regra": "Sonhos Malucos",
        "pm_bonus": 2,
        "rolagens": {
            "natureza_1d3": d3,
            "tamanho_1d4": d4,
            "dons_2d6": dons_dados,
            "presentes_3d12": pres_dados,
        },
        "natureza": {"id": nat_id, "nome": nat_nome},
        "tamanho": {"id": tam_id, "nome": tam_nome},
        "dons": {"atributo_1": dons_atributos[0], "atributo_2": dons_atributos[1]},
        "presentes": [
            {"id": pid, "nome": pnome}
            for pid, pnome in zip(presentes_ids, presentes_nomes)
        ],
        "tabu_sugerido": tabu_sugerido,
    }
