# -*- coding: utf-8 -*-
"""Poderes de Arcanista (T20) com efeitos estruturados para o motor de regras.

Formato compatível com dados_habilidades_classe (nome/tipo/classe/descricao/
requisitos/efeitos). Gatilhos de escolha usam sufixo '_escolha' (convenção
que o AbilityConfigModal já detecta).
"""

PODERES_ARCANISTA = {
    "Arcano de Batalha": {
        "nome": "Arcano de Batalha", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Quando lança uma magia, você soma seu atributo-chave na rolagem de dano.",
        "requisitos": [], "efeitos": {"dano_magia_atributo_chave": True},
    },
    "Aumento de Atributo": {
        "nome": "Aumento de Atributo", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Você recebe +1 em um atributo. Pode escolher várias vezes, mas apenas uma vez por patamar para o mesmo atributo.",
        "requisitos": [], "efeitos": {"aumento_atributo": 1, "atributo_escolha": 1},
    },
    "Caldeirão do Bruxo": {
        "nome": "Caldeirão do Bruxo", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Cria poções como se tivesse Preparar Poção; com ambos, até 5º círculo.",
        "requisitos": ["Bruxo", "Ofício (alquimista)"], "efeitos": {"criar_pocoes": True},
    },
    "Conhecimento Mágico": {
        "nome": "Conhecimento Mágico", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Aprende duas magias de qualquer círculo que possa lançar. Pode escolher quantas vezes quiser.",
        "requisitos": [], "efeitos": {"magias_extras": 2},
    },
    "Contramágica Aprimorada": {
        "nome": "Contramágica Aprimorada", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Uma vez por rodada, faz contramágica como reação.",
        "requisitos": ["Dissipar Magia"], "efeitos": {"contramagica_reacao": True},
    },
    "Envolto em Mistério": {
        "nome": "Envolto em Mistério", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "+5 em Enganação e Intimidação contra pessoas não treinadas em Conhecimento ou Misticismo.",
        "requisitos": [],
        "efeitos": {"bonus_pericia_condicional": {
            "pericias": ["Enganação", "Intimidação"], "valor": 5,
            "condicao": "vs não treinados em Conhecimento/Misticismo"}},
    },
    "Escriba Arcano": {
        "nome": "Escriba Arcano", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Aprende magias copiando de pergaminhos/grimórios (1 dia + T$ 250 por PM).",
        "requisitos": ["Mago", "Ofício (escriba)"], "efeitos": {"copiar_magias": True},
    },
    "Especialista em Escola": {
        "nome": "Especialista em Escola", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Escolha uma escola; a CD para resistir a suas magias dessa escola aumenta em +2.",
        "requisitos": ["Bruxo ou Mago"], "efeitos": {"cd_escola_bonus": 2, "escola_escolha": 1},
    },
    "Familiar": {
        "nome": "Familiar", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Você possui um animal de estimação mágico (veja a lista de familiares).",
        "requisitos": [], "efeitos": {"familiar_escolha": 1},
    },
    "Fluxo de Mana": {
        "nome": "Fluxo de Mana", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Mantém dois efeitos sustentados com uma ação livre.",
        "requisitos": ["Arcanista 10"], "efeitos": {"sustentados_duplos": True},
    },
    "Foco Vital": {
        "nome": "Foco Vital", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Seu foco absorve dano que o levaria a 0 PV.",
        "requisitos": ["Bruxo"], "efeitos": {"foco_vital": True},
    },
    "Fortalecimento Arcano": {
        "nome": "Fortalecimento Arcano", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "A CD para resistir a suas magias aumenta em +1 (+2 se você lançar magias de 4º círculo).",
        "requisitos": ["Arcanista 5"], "efeitos": {"cd_magias_bonus": 1, "cd_magias_bonus_4circulo": 2},
    },
    "Herança Aprimorada": {
        "nome": "Herança Aprimorada", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Recebe a herança aprimorada de sua linhagem sobrenatural.",
        "requisitos": ["Feiticeiro", "Arcanista 6"], "efeitos": {"heranca_nivel": "aprimorada"},
    },
    "Herança Superior": {
        "nome": "Herança Superior", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Recebe a herança superior de sua linhagem sobrenatural.",
        "requisitos": ["Herança Aprimorada", "Arcanista 11"], "efeitos": {"heranca_nivel": "superior"},
    },
    "Magia Pungente": {
        "nome": "Magia Pungente", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Pague 1 PM para aumentar em +2 a CD de uma magia.",
        "requisitos": [], "efeitos": {"cd_ativavel": 2, "custo_ativavel": 1},
    },
    "Mestre em Escola": {
        "nome": "Mestre em Escola", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "O custo para lançar magias da escola escolhida diminui em -1 PM.",
        "requisitos": ["Especialista em Escola (mesma escola)", "Arcanista 8"],
        "efeitos": {"custo_escola_reducao": 1, "escola_escolha": 1},
    },
    "Poder Mágico": {
        "nome": "Poder Mágico", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "+1 PM por nível de arcanista (retroativo).",
        "requisitos": [], "efeitos": {"pm_por_nivel_classe": 1},
    },
    "Raio Arcano": {
        "nome": "Raio Arcano", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Ação padrão: 1d8 dano de essência (curto); +1d8 por círculo acima do 1º; Refl reduz à metade.",
        "requisitos": [],
        "efeitos": {"ataque_magico": {"dano_base": "1d8", "dano_por_circulo_acima_1": "1d8",
                                      "alcance": "curto", "resistencia": "Reflexos", "tipo_dano": "essência"}},
    },
    "Raio Elemental": {
        "nome": "Raio Elemental", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "+1 PM: raio causa dano de tipo à sua escolha e aplica condição.",
        "requisitos": ["Raio Arcano"], "efeitos": {"raio_elemental": True},
    },
    "Raio Poderoso": {
        "nome": "Raio Poderoso", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Raio Arcano sobe para d12 e alcance médio.",
        "requisitos": ["Raio Arcano"], "efeitos": {"raio_poderoso": True},
    },
    "Tinta do Mago": {
        "nome": "Tinta do Mago", "tipo": "Poder de Arcanista", "classe": "Arcanista",
        "descricao": "Cria pergaminhos; com Escrever Pergaminho, custo à metade.",
        "requisitos": ["Mago", "Ofício (escriba)"], "efeitos": {"criar_pergaminhos": True},
    },
}
