# -*- coding: utf-8 -*-
"""Catálogo oficial da classe Treinador — Heróis de Arton (Cap. 1, p. 16–21).

Inclui:
- Habilidades de Classe (Tabela 1-1, nv 1–20)
- 21 Poderes de Treinador (p. 18–19)
- 8 Mascotes (p. 19)
- 5 Tipos de Melhor Amigo (p. 20)
- 22 Truques do Melhor Amigo (p. 21)
"""
from typing import Dict, Any
from .dados_suplementos import FONTE_HEROIS


# =====================================================================
# 1. HABILIDADES E PODERES DE CLASSE DO TREINADOR
# =====================================================================

DADOS_HABILIDADES_TREINADOR: Dict[str, Dict[str, Any]] = {
    # --- HABILIDADES FIXAS (Tabela 1-1) ---
    "TREINADOR_DIRECIONAR": {
        "nome": "Direcionar",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 1,
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Se o seu melhor amigo estiver em alcance curto e fizer um teste de perícia, você pode gastar 2 PM para somar seu Carisma no teste dele.",
        "efeitos": {"direcionar": True},
    },
    "TREINADOR_MELHOR_AMIGO": {
        "nome": "Melhor Amigo",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 1,
        "fonte": FONTE_HEROIS,
        "descricao": "Você recebe um melhor amigo, um parceiro especial com ficha própria (p. 20). Começa com 2 truques e recebe +1 truque a cada 3 níveis seguintes (4º, 7º, 10º, 13º, 16º, 19º). Se ele morrer, você fica atordoado por 1d4 rodadas (1 mês para treinar outro).",
        "efeitos": {"melhor_amigo": True},
    },
    "TREINADOR_DOMAR_CRIATURA": {
        "nome": "Domar Criatura",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 2,
        "custo_pm": 1,
        "fonte": FONTE_HEROIS,
        "descricao": "Ação de movimento e 1 PM: teste de Adestramento oposto a Vontade de uma criatura não inteligente em alcance curto. Se vencer, causa 2d8 de dano psíquico não letal (metade se perder). A 0 PV ela se rende. A cada 4 níveis (+1 PM) aumenta em +2d8 (4d8 nv6, 6d8 nv10, 8d8 nv14, 10d8 nv18). Nv 5: gasta PM = ND (≤ nível) para controlar pela cena; Nv 8: ND ≤ nível -3 fica até o fim do dia.",
        "efeitos": {"domar_criatura": True},
    },
    "TREINADOR_TREINO_ESPECIALIZADO": {
        "nome": "Treino Especializado",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 5,
        "fonte": FONTE_HEROIS,
        "descricao": "Escolha entre Conquistar pelos Números (recebe um 2º melhor amigo; 3 PM para ação padrão extra com o outro) ou Treino Intensivo (+4 PV/nível, RD 5/10/15 nos níveis 5/11/17 e +1 truque no 5º e 11º).",
        "efeitos": {"treino_especializado": True},
    },
    "TREINADOR_SINCRONIA_COMBATE": {
        "nome": "Sincronia de Combate",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 6,
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Uma vez por rodada, quando seu melhor amigo acerta um ataque usando a ação agredir, você pode gastar 2 PM para fazer um ataque contra o mesmo alvo.",
        "efeitos": {"sincronia_combate": True},
    },
    "TREINADOR_SINCRONIA_PERFEITA": {
        "nome": "Sincronia Perfeita",
        "tipo": "Classe",
        "classe": "Treinador",
        "nivel": 20,
        "custo_pm": 6,
        "fonte": FONTE_HEROIS,
        "descricao": "Ação de movimento e 6 PM: entra em sincronia perfeita com um melhor amigo até o fim da cena. O tamanho dele aumenta em uma categoria e, uma vez por rodada, quando você usa uma ação padrão consigo mesmo, recebe uma ação padrão extra para usar com ele.",
        "efeitos": {"sincronia_perfeita": True},
    },

    # --- 21 PODERES DE TREINADOR (p. 18–19) ---
    "TREINADOR_AMIGO_DIVINO": {
        "nome": "Amigo Divino",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Seu melhor amigo vive em um mundo divino; ação de movimento e 2 PM para invocá-lo em alcance curto pela cena (livre para dispensar). No mundo divino com menos da metade dos PV, tem Cura Acelerada 10.",
        "efeitos": {"amigo_divino": True},
    },
    "TREINADOR_ASAS_ALIADAS": {
        "nome": "Asas Aliadas",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 1,
        "fonte": FONTE_HEROIS,
        "descricao": "Uma vez por rodada, se estiver em alcance curto de seu melhor amigo e ele usar deslocamento de voo, pague 1 PM para ser alçado aos céus para um quadrado no trajeto dele; seu próximo ataque nesse turno conta como investida.",
        "efeitos": {"asas_aliadas": True},
    },
    "TREINADOR_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Você recebe +1 em um atributo. Pode escolher várias vezes, mas apenas uma vez por patamar para o mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1},
    },
    "TREINADOR_BOM_GAROTO": {
        "nome": "Bom Garoto",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["11º nível de treinador"],
        "fonte": FONTE_HEROIS,
        "descricao": "Uma vez por rodada, quando seu melhor amigo faz um acerto crítico ou reduz um inimigo a 0 PV em seu turno, você recebe uma ação padrão adicional que só pode usar consigo mesmo.",
        "efeitos": {"bom_garoto": True},
    },
    "TREINADOR_COMANDO_DEFENSIVO": {
        "nome": "Comando Defensivo",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Quando seu melhor amigo sofre dano, gaste 2 PM para fazer um teste de Adestramento e reduzir o dano pelo resultado do teste (1×/rodada por melhor amigo).",
        "efeitos": {"comando_defensivo": True},
    },
    "TREINADOR_COMANDOS_DISTANTES": {
        "nome": "Comandos Distantes",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "O alcance de suas habilidades de treinador aumenta em uma categoria (curto → médio, médio → longo).",
        "efeitos": {"comandos_distantes": True},
    },
    "TREINADOR_CONVOCAR_ENXAME": {
        "nome": "Convocar Enxame",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["5º nível de treinador"],
        "fonte": FONTE_HEROIS,
        "descricao": "Você aprende e pode lançar Enxame de Pestes (atributo-chave Carisma), usando aprimoramentos como um clérigo de seu nível (habilidade não mágica / magia simulada).",
        "efeitos": {
            "magias_conhecidas": ["Enxame de Pestes"],
            "atributo_magia_fixo": "car",
            "circulos_como_clerigo": True,
            "magia_simulada": True,
        },
    },
    "TREINADOR_CORACAO_GRANDE": {
        "nome": "Coração Grande",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Seu limite de parceiros aumenta em +1. No 11º nível, esse limite aumenta em mais +1.",
        "efeitos": {"coracao_grande": True},
    },
    "TREINADOR_DIRECIONAMENTO_MARCIAL": {
        "nome": "Direcionamento Marcial",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Quando usa Direcionar em um teste de ataque, você também soma seu Carisma na rolagem de dano desse ataque.",
        "efeitos": {"direcionamento_marcial": True},
    },
    "TREINADOR_DOMADOR_CATIVANTE": {
        "nome": "Domador Cativante",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Você soma seu Carisma no dano de Domar Criatura, e os dados de dano dessa habilidade aumentam para d10.",
        "efeitos": {"domador_cativante": True},
    },
    "TREINADOR_DOMADOR_LENDARIO": {
        "nome": "Domador Lendário",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["Domador Cativante", "17º nível de treinador"],
        "fonte": FONTE_HEROIS,
        "descricao": "Quando usa Domar Criatura, pode gastar +2 PM para mudar os dados de dano para d12 e atingir todos os alvos dentro do alcance.",
        "efeitos": {"domador_lendario": True},
    },
    "TREINADOR_ENSINAR_TRUQUE": {
        "nome": "Ensinar Truque",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Um de seus melhores amigos aprende um truque adicional (pode escolher uma vez por patamar por amigo).",
        "efeitos": {"ensinar_truque": 1},
    },
    "TREINADOR_INVESTIDA_CONJUNTA": {
        "nome": "Investida Conjunta",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 2,
        "requisitos": ["Melhor amigo montaria"],
        "fonte": FONTE_HEROIS,
        "descricao": "Uma vez por rodada, quando um melhor amigo no qual você está montado faz uma investida, gaste 2 PM para fazer um ataque corpo a corpo (que também conta como investida).",
        "efeitos": {"investida_conjunta": True},
    },
    "TREINADOR_LIDER_MATILHA": {
        "nome": "Líder da Matilha",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["Conquistar pelos Números"],
        "fonte": FONTE_HEROIS,
        "descricao": "Quando usa Direcionar, pode aplicar o bônus ao próximo teste de perícia de outros melhores amigos com a mesma ação por +1 PM por amigo adicional (até o fim do turno).",
        "efeitos": {"lider_matilha": True},
    },
    "TREINADOR_LINGUA_CRIATURAS": {
        "nome": "Língua das Criaturas",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Pode se comunicar com criaturas não inteligentes (Int -4 ou -5) e usar Adestramento para mudar atitude e persuasão com elas.",
        "efeitos": {"lingua_criaturas": True},
    },
    "TREINADOR_MASCOTE": {
        "nome": "Mascote",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Você tem um mascote (parceiro especial que não conta no limite de parceiros; fornece seus benefícios a você e seus melhores amigos). Pode escolher várias vezes para mascotes diferentes.",
        "efeitos": {"mascote": True},
    },
    "TREINADOR_PETISCO_MERECIDO": {
        "nome": "Petisco Merecido",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Gaste 2 PM para conceder +2 em Força e Destreza a um melhor amigo em alcance curto até o fim da cena.",
        "efeitos": {"petisco_merecido": True},
    },
    "TREINADOR_PROTECAO_FRATERNA": {
        "nome": "Proteção Fraterna",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "custo_pm": 2,
        "fonte": FONTE_HEROIS,
        "descricao": "Quando você e/ou seu melhor amigo em alcance curto sofre efeito com teste de resistência, gaste 2 PM para ambos rolarem e usarem o melhor resultado (habilidades como Evasão afetam ambos).",
        "efeitos": {"protecao_fraterna": True},
    },
    "TREINADOR_TRABALHO_EQUIPE": {
        "nome": "Trabalho em Equipe",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["5º nível de treinador"],
        "fonte": FONTE_HEROIS,
        "descricao": "Uma vez por rodada, quando você faz uma ação de movimento, seus melhores amigos recebem uma ação de movimento.",
        "efeitos": {"trabalho_equipe": True},
    },
    "TREINADOR_ECLETICO": {
        "nome": "Treinador Eclético",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "requisitos": ["6º nível de treinador"],
        "fonte": FONTE_HEROIS,
        "descricao": "Seus melhores amigos usam seu nível de personagem (em vez de nível de treinador) para calcular PV, modificadores de perícias e Defesa.",
        "efeitos": {"treinador_ecletico": True},
    },
    "TREINADOR_VETERINARIO_CAMPO": {
        "nome": "Veterinário de Campo",
        "tipo": "Poder de Treinador",
        "classe": "Treinador",
        "fonte": FONTE_HEROIS,
        "descricao": "Ação completa: teste de Adestramento em um melhor amigo adjacente para curar PV iguais ao resultado do teste (1×/dia por alvo).",
        "efeitos": {"veterinario_campo": True},
    },
}


# =====================================================================
# 2. MASCOTES (p. 19)
# =====================================================================

DADOS_MASCOTES_TREINADOR: Dict[str, Dict[str, Any]] = {
    "Águia Real": {
        "nome": "Águia Real",
        "descricao": "Uma vez por rodada, fornece +1d6 em uma rolagem de dano com arma.",
        "efeitos": {"dano_extra_rodada": "1d6"},
        "fonte": FONTE_HEROIS,
    },
    "Bicho Preguiça": {
        "nome": "Bicho Preguiça",
        "descricao": "Ocupa o espaço de 1 item vestido, mas fornece ataque natural de garra (1d6, x2, corte; 1 PM para ataque extra ao agredir com outra arma).",
        "efeitos": {
            "arma_natural": {
                "nome": "Garra (Bicho Preguiça)",
                "dano": "1d6",
                "critico": "x2",
                "tipo": "Corte",
                "alcance": "Corpo a corpo",
            },
            "ataque_extra": {"custo_pm": 1, "gatilho": "agredir_outra_arma"},
        },
        "fonte": FONTE_HEROIS,
    },
    "Camundongo Espiritual": {
        "nome": "Camundongo Espiritual",
        "descricao": "Aumenta a CD para resistir a habilidades mágicas em +1.",
        "efeitos": {"cd_magias_bonus": 1},
        "fonte": FONTE_HEROIS,
    },
    "Fada-Borboleta": {
        "nome": "Fada-Borboleta",
        "descricao": "Diminui o custo de habilidades mágicas em -1 PM.",
        "efeitos": {"reducao_custo_habilidade_magica": 1},
        "fonte": FONTE_HEROIS,
    },
    "Gekko Malhado": {
        "nome": "Gekko Malhado",
        "descricao": "Fornece +2 na Defesa e em Reflexos.",
        "efeitos": {"defesa_bonus": 2, "bonus_pericia": {"Reflexos": 2}},
        "fonte": FONTE_HEROIS,
    },
    "Mico-Leão Dourado": {
        "nome": "Mico-Leão Dourado",
        "descricao": "Permite usar Ladinagem para punga em alcance curto.",
        "efeitos": {"punga_alcance_curto": True},
        "fonte": FONTE_HEROIS,
    },
    "Minivaca": {
        "nome": "Minivaca",
        "descricao": "Fornece +1 em testes de ataque (dobra para +2 em investidas).",
        "efeitos": {"ataque_bonus": 1, "ataque_investida_bonus": 2},
        "fonte": FONTE_HEROIS,
    },
    "Ossinhos": {
        "nome": "Ossinhos",
        "descricao": "Esqueleto reanimado. Fornece redução de corte, frio e perfuração 2.",
        "efeitos": {"resistencia_rd": {"Corte": 2, "Frio": 2, "Perfuração": 2}},
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 3. TIPOS DE MELHOR AMIGO (p. 20)
# =====================================================================

DADOS_TIPOS_MELHOR_AMIGO: Dict[str, Dict[str, Any]] = {
    "Animal": {
        "nome": "Animal",
        "mod_atributos": {"forca": 1, "destreza": 1, "sabedoria": 1},
        "sentidos": ["Faro", "Visão na penumbra"],
        "pericias_treinadas": ["Percepção", "Sobrevivência"],
        "margem_ameaca_bonus": 1,
        "imunidades": [],
        "armas_naturais_extras": 0,
        "descricao": "+1 For, Des e Sab; faro, visão na penumbra, treinado em Percepção e Sobrevivência e +1 na margem de ameaça com armas naturais.",
        "fonte": FONTE_HEROIS,
    },
    "Construto": {
        "nome": "Construto",
        "mod_atributos": {"constituicao": 2},
        "sentidos": ["Visão no escuro"],
        "pericias_treinadas": [],
        "margem_ameaca_bonus": 0,
        "imunidades": ["Cansaço", "Metabolismo", "Veneno"],
        "armas_naturais_extras": 0,
        "descricao": "+2 Con, visão no escuro, imune a cansaço, metabolismo e veneno. Não respira/come/dorme; curado com Ofício (artesão).",
        "fonte": FONTE_HEROIS,
    },
    "Espírito": {
        "nome": "Espírito",
        "mod_atributos": {"sabedoria": 1, "carisma": 1},
        "sentidos": [],
        "pericias_treinadas": [],
        "margem_ameaca_bonus": 0,
        "imunidades": [],
        "armas_naturais_extras": 0,
        "forma_incorporea": True,
        "descricao": "+1 Sab e Car. Ação de movimento para forma incorpórea Minúscula (voo 9m) concedendo +2 em perícias de Sab (positiva) ou Car (negativa).",
        "fonte": FONTE_HEROIS,
    },
    "Monstro": {
        "nome": "Monstro",
        "mod_atributos": {"forca": 1, "destreza": 1},
        "sentidos": ["Visão no escuro"],
        "pericias_treinadas": [],
        "margem_ameaca_bonus": 0,
        "imunidades": [],
        "armas_naturais_extras": 1,
        "descricao": "+1 For e Des, visão no escuro e uma segunda arma natural (1 PM para ataque extra ao agredir com outra arma).",
        "fonte": FONTE_HEROIS,
    },
    "Morto-Vivo": {
        "nome": "Morto-Vivo",
        "mod_atributos": {"constituicao": 2},
        "sentidos": ["Visão no escuro"],
        "pericias_treinadas": [],
        "margem_ameaca_bonus": 0,
        "imunidades": ["Cansaço", "Metabolismo", "Trevas", "Veneno"],
        "armas_naturais_extras": 0,
        "descricao": "+2 Con, visão no escuro, imune a cansaço, metabolismo, trevas e veneno. Sofre dano de cura de luz e recupera PV com dano de trevas.",
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 4. TRUQUES DO MELHOR AMIGO (22 truques, p. 21)
# =====================================================================

DADOS_TRUQUES_MELHOR_AMIGO: Dict[str, Dict[str, Any]] = {
    "Alado": {
        "nome": "Alado",
        "requisitos": ["Asas", "5º nível de treinador"],
        "descricao": "Ganha deslocamento de voo 15m.",
        "efeitos": {"deslocamento_voo": 15},
    },
    "Amigão": {
        "nome": "Amigão",
        "requisitos": ["Melhor amigo Grande", "7º nível de treinador"],
        "descricao": "Recebe +1 em Força e tamanho muda para Enorme (+1 passo de dano nas armas naturais).",
        "efeitos": {"mod_atributos": {"forca": 1}, "tamanho": "Enorme", "passo_dano": 1},
    },
    "Amigo Feroz": {
        "nome": "Amigo Feroz",
        "requisitos": [],
        "descricao": "Recebe +2 em testes de ataque e na margem de ameaça com armas naturais, e o dano aumenta em +1 passo.",
        "efeitos": {"ataque_bonus": 2, "margem_ameaca_bonus": 2, "passo_dano": 1},
    },
    "Amigo Protetor": {
        "nome": "Amigo Protetor",
        "requisitos": [],
        "descricao": "Quando você sofre dano com o amigo em alcance curto, gaste 2 PM para dividir o dano pela metade entre vocês.",
        "efeitos": {"custo_pm": 2},
    },
    "Amigo Veterano": {
        "nome": "Amigo Veterano",
        "requisitos": ["5º nível de treinador"],
        "descricao": "Seu melhor amigo vira um parceiro veterano de seu tipo.",
        "efeitos": {"grau_parceiro": "Veterano"},
    },
    "Amigo Mestre": {
        "nome": "Amigo Mestre",
        "requisitos": ["Amigo Veterano", "11º nível de treinador"],
        "descricao": "Seu melhor amigo veterano vira um parceiro mestre de seu tipo.",
        "efeitos": {"grau_parceiro": "Mestre"},
    },
    "Anatomia Humanoide": {
        "nome": "Anatomia Humanoide",
        "requisitos": ["Construto ou Morto-Vivo", "Apenas na criação"],
        "descricao": "Forma humanoide, Int -2 (em vez de -4), sem arma natural inicial, proficiência com armas simples e armaduras leves, empunha 2 itens, veste +1 item, carga 10 espaços.",
        "efeitos": {"inteligencia_base": -2, "limite_vestidos_bonus": 1, "carga": 10},
    },
    "Arma Natural Adicional": {
        "nome": "Arma Natural Adicional",
        "requisitos": ["Animal ou Monstro"],
        "descricao": "Recebe uma arma natural adicional (1 PM para ataque extra ao agredir com outra arma).",
        "efeitos": {"armas_naturais_extras": 1},
    },
    "Asas": {
        "nome": "Asas",
        "requisitos": [],
        "descricao": "Paira a 1,5m do chão (desl. 12m, ignora terreno difícil, imune a queda consciente); 1 PM/rodada para voar 12m.",
        "efeitos": {"imunidade_queda": True, "deslocamento_voo_pm": 12},
    },
    "Bote": {
        "nome": "Bote",
        "requisitos": ["Duas armas naturais"],
        "descricao": "Em investida, ataca com todas as armas naturais contra o mesmo alvo (+2 em todas).",
        "efeitos": {"bote": True},
    },
    "Condicionamento Especial": {
        "nome": "Condicionamento Especial",
        "requisitos": ["1× por patamar"],
        "descricao": "Recebe +2 em um atributo e +1 em outro atributo, exceto Inteligência.",
        "efeitos": {"condicionamento_especial": True},
    },
    "Deslocamento Especial": {
        "nome": "Deslocamento Especial",
        "requisitos": [],
        "descricao": "Recebe deslocamento de escalada ou natação igual ao base (pode escolher 2ª vez para ambos).",
        "efeitos": {"deslocamento_especial": True},
    },
    "Magia Inata": {
        "nome": "Magia Inata",
        "requisitos": ["Espírito"],
        "descricao": "Aprende e pode lançar uma magia de 1º círculo (arcana ou divina, atributo-chave Carisma do treinador).",
        "efeitos": {"magia_inata": True},
    },
    "Manobra Ensaiada": {
        "nome": "Manobra Ensaiada",
        "requisitos": [],
        "descricao": "+2 em testes de ataque para uma manobra escolhida; 1×/rodada ao acertar arma natural, 1 PM para executar a manobra como ação livre.",
        "efeitos": {"manobra_bonus": 2},
    },
    "Reanimação Sombria": {
        "nome": "Reanimação Sombria",
        "requisitos": ["Morto-Vivo"],
        "descricao": "1×/cena, com 0 PV ou menos, gaste 3 PM por patamar para reerguer com metade dos PV máximos.",
        "efeitos": {"reanimacao_sombria": True},
    },
    "Redução de Dano": {
        "nome": "Redução de Dano",
        "requisitos": ["5º nível de treinador"],
        "descricao": "Recebe redução de dano 5.",
        "efeitos": {"rd_fixa": 5},
    },
    "Sopro": {
        "nome": "Sopro",
        "requisitos": ["Construto, Espírito ou Monstro"],
        "descricao": "Ação padrão + PM (até Car do treinador): cone 6m de ácido, fogo, frio ou eletricidade causando 2d8/PM (Ref CD Car reduz à metade).",
        "efeitos": {"sopro": True},
    },
    "Táticas de Matilha": {
        "nome": "Táticas de Matilha",
        "requisitos": [],
        "descricao": "Ao flanquear, recebe +2 em ataque (total +4) e +2 em dano (você também recebe ao flanquear com ele).",
        "efeitos": {"flanquear_ataque_bonus": 2, "flanquear_dano_bonus": 2},
    },
    "Treinamento de Companhia": {
        "nome": "Treinamento de Companhia",
        "requisitos": ["Animal"],
        "descricao": "Recebe uma ação de movimento adicional nos seus turnos (apenas para se deslocar).",
        "efeitos": {"movimento_extra": True},
    },
    "Treinamento Defensivo": {
        "nome": "Treinamento Defensivo",
        "requisitos": [],
        "descricao": "Recebe bônus na Defesa igual ao seu nível (em vez de metade do nível).",
        "efeitos": {"defesa_nivel_cheio": True},
    },
    "Treinamento Marcial": {
        "nome": "Treinamento Marcial",
        "requisitos": [],
        "descricao": "+2 em ataque e dano (+1 por patamar acima de iniciante). Com Anatomia Humanoide, recebe proficiência com armas marciais, armaduras pesadas e escudos.",
        "efeitos": {"treinamento_marcial": True},
    },
    "Veloz": {
        "nome": "Veloz",
        "requisitos": [],
        "descricao": "+2 na Defesa, +3m em seus deslocamentos e treinado em Atletismo (ou +2 se já for).",
        "efeitos": {"defesa_bonus": 2, "deslocamento_bonus": 3, "pericia_treino": "Atletismo"},
    },
}


def obter_catalogo_treinador() -> Dict[str, Any]:
    """Retorna o catálogo completo do Treinador para o frontend / API."""
    return {
        "fonte": FONTE_HEROIS,
        "habilidades": DADOS_HABILIDADES_TREINADOR,
        "mascotes": DADOS_MASCOTES_TREINADOR,
        "tipos_melhor_amigo": DADOS_TIPOS_MELHOR_AMIGO,
        "truques": DADOS_TRUQUES_MELHOR_AMIGO,
    }
