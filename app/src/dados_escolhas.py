# -*- coding: utf-8 -*-
"""Catálogo ÚNICO de opções de escolha do sistema (fonte de verdade).

O frontend NÃO duplica estas listas: tudo vem de GET /dados/escolhas.
"""

ATRIBUTOS = [
    {"valor": "forca", "rotulo": "Força"},
    {"valor": "destreza", "rotulo": "Destreza"},
    {"valor": "constituicao", "rotulo": "Constituição"},
    {"valor": "inteligencia", "rotulo": "Inteligência"},
    {"valor": "sabedoria", "rotulo": "Sabedoria"},
    {"valor": "carisma", "rotulo": "Carisma"},
]

ESCOLAS_MAGIA = [
    "Abjuração", "Adivinhação", "Convocação", "Encantamento",
    "Evocação", "Ilusão", "Necromancia", "Transmutação",
]

FAMILIARES_ARCANOS = [
    "Borboleta", "Cobra", "Coruja", "Corvo", "Falcão",
    "Gato", "Lagarto", "Morcego", "Rato", "Sapo",
]

TIPOS_DANO_ELEMENTAL = ["ácido", "eletricidade", "fogo", "frio", "trevas"]

CAMINHOS_ARCANISTA_INFO = {
    "Bruxo": "Atributo-chave: Inteligência. Lança magias empunhando um foco (RD 10, PV = metade dos seus); sem foco, teste de Misticismo (CD 20 + PM).",
    "Feiticeiro": "Atributo-chave: Carisma. Poder inato por linhagem sobrenatural; aprende 1 magia nova a cada nível ímpar (3º, 5º, 7º...).",
    "Mago": "Atributo-chave: Inteligência. Memoriza metade das magias após 1h de estudo (1×/dia); +1 magia inicial e +1 a cada círculo novo.",
}

# Poderes com escolha secundária -> chave salva em escolhas_aplicadas + catálogo de opções
PODERES_COM_ESCOLHA = {
    "Aumento de Atributo": [{"chave": "atributo", "rotulo": "Atributo", "catalogo": "ATRIBUTOS"}],
    "Especialista em Escola": [{"chave": "escola", "rotulo": "Escola de Magia", "catalogo": "ESCOLAS_MAGIA"}],
    "Mestre em Escola": [{"chave": "escola", "rotulo": "Escola de Magia", "catalogo": "ESCOLAS_MAGIA"}],
    "Familiar": [{"chave": "familiar", "rotulo": "Familiar Arcano", "catalogo": "FAMILIARES_ARCANOS"}],
}

# Escolhas fixas de classe (UI futura: Bardo/Druida escolhem 3 escolas)
ESCOLHAS_DE_CLASSE = {
    "Bardo": {"escolas_de_magia": 3},
    "Druida": {"escolas_de_magia": 3},
}


def montar_catalogo_escolhas() -> dict:
    """Resolve os catálogos e devolve o payload pronto p/ frontend."""
    poderes = {
        poder: [
            {"chave": g["chave"], "rotulo": g["rotulo"], "opcoes": globals()[g["catalogo"]]}
            for g in gatilhos
        ]
        for poder, gatilhos in PODERES_COM_ESCOLHA.items()
    }
    return {
        "ATRIBUTOS": ATRIBUTOS,
        "ESCOLAS_MAGIA": ESCOLAS_MAGIA,
        "FAMILIARES_ARCANOS": FAMILIARES_ARCANOS,
        "TIPOS_DANO_ELEMENTAL": TIPOS_DANO_ELEMENTAL,
        "CAMINHOS_ARCANISTA_INFO": CAMINHOS_ARCANISTA_INFO,
        "PODERES_COM_ESCOLHA": poderes,
        "ESCOLHAS_DE_CLASSE": ESCOLHAS_DE_CLASSE,
    }
