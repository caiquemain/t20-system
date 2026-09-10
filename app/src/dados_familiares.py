# -*- coding: utf-8 -*-
"""Familiares Arcanos (T20) — benefícios estruturados para o motor de regras."""

FAMILIARES_ARCANOS = {
    "Borboleta": {"cd_resistencia": {"Vontade": 1},
                  "descricao": "A CD dos testes de Vontade para resistir a suas magias aumenta em +1."},
    "Cobra": {"cd_resistencia": {"Fortitude": 1},
              "descricao": "A CD dos testes de Fortitude para resistir a suas magias aumenta em +1."},
    "Coruja": {"ativavel": True,
               "descricao": "Pague 1 PM para mudar alcance de toque para curto."},
    "Corvo": {"ativavel": True,
              "descricao": "Pague 1 PM para rolar dois dados em Misticismo/Vontade e usar o melhor."},
    "Falcão": {"imunidades": ["Não pode ser surpreendido", "Não fica desprevenido"],
               "descricao": "Você não pode ser surpreendido e nunca fica desprevenido."},
    "Gato": {"sentidos": ["Visão no Escuro"], "pericia_bonus": {"Furtividade": 2},
             "descricao": "Visão no escuro e +2 em Furtividade."},
    "Lagarto": {"cd_resistencia": {"Reflexos": 1},
                "descricao": "A CD dos testes de Reflexos para resistir a suas magias aumenta em +1."},
    "Morcego": {"sentidos": ["Percepção às cegas (curto)"],
                "descricao": "Percepção às cegas em alcance curto."},
    "Rato": {"nota": "Atributo-chave em Fortitude no lugar de Constituição",
             "descricao": "Você pode usar seu atributo-chave em Fortitude."},
    "Sapo": {"pv_atributo_chave": True,
             "descricao": "Soma seu atributo-chave ao total de pontos de vida (cumulativo)."},
}
