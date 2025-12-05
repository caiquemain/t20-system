# src/dados_habilidades_classe.py

# ==============================================================================
# BANCO DE DADOS DE HABILIDADES E PODERES DE CLASSE (T20 JdA)
# Estrutura unificada para facilitar classes variantes.
#
# Chave: CLASSE_NOME_HABILIDADE (Upper Snake Case)
# nome: Nome oficial (Display)
# tipo: "Habilidade de Classe" (Fixa) ou "Poder de [Classe]" (Escolha)
# classe: Nome da classe principal associada (para filtros)
# nivel: Nível em que a habilidade fixa é ganha (0 se for poder de escolha)
# descricao: Texto de regras
# requisitos: Lista de strings (ex: ["For 1", "Treinado em Luta"])
# efeitos: Dicionário de automação
# ==============================================================================

DADOS_HABILIDADES_CLASSE = {

    # ==========================================================================
    # ARCANISTA
    # ==========================================================================
    "ARCANISTA_CAMINHO": {
        "nome": "Caminho do Arcanista",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 1,
        "descricao": "Escolha um caminho: Bruxo (foco, Int), Feiticeiro (linhagem, Car) ou Mago (grimório, Int). Define seu atributo-chave e mecânica de magia. ",
        "efeitos": {"escolha_subclasse": ["Bruxo", "Feiticeiro", "Mago"]}
    },
    "ARCANISTA_MAGIAS": {
        "nome": "Magias (Arcanista)",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 1,
        "descricao": "Você pode lançar magias arcanas. Começa com 3 magias de 1º círculo (mais se for Mago). ",
        "efeitos": {"habilita_magia": {"tipo": "Arcana", "circulo_max": 1}}
    },
    "ARCANISTA_ALTA_ARCANA": {
        "nome": "Alta Arcana",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 20,
        "descricao": "O custo em PM de suas magias arcanas é reduzido à metade. ",
        "efeitos": {"reducao_custo_magia_global": 0.5}
    },
    # --- PODERES DE ARCANISTA ---
    "ARCANISTA_ARCANO_BATALHA": {
        "nome": "Arcano de Batalha",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você soma seu atributo-chave nas rolagens de dano de suas magias. ",
        "efeitos": {"dano_magia_soma_atributo": True}
    },
    "ARCANISTA_CALDEIRAO_BRUXO": {
        "nome": "Caldeirão do Bruxo",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Bruxo", "Treinado em Ofício (alquimista)"],
        "descricao": "Você pode criar poções como se tivesse o poder Preparar Poção. Se tiver ambos, cria até 5º círculo. ",
        "efeitos": {}
    },
    "ARCANISTA_CONHECIMENTO_MAGICO": {
        "nome": "Conhecimento Mágico",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você aprende duas magias de qualquer círculo que possa lançar. ",
        "efeitos": {"magias_adicionais": 2}
    },
    "ARCANISTA_ESPECIALISTA_ESCOLA": {
        "nome": "Especialista em Escola",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Bruxo ou Mago"],
        "descricao": "Escolha uma escola. A CD para resistir a suas magias dessa escola aumenta em +2. ",
        "efeitos": {"cd_magia_escola_bonus": 2}
    },
    "ARCANISTA_FAMILIAR": {
        "nome": "Familiar",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você possui um animal mágico que concede bônus (Ex: Sapo +PV, Coruja +Alcance). ",
        "efeitos": {"familiar_escolha": True}
    },
    "ARCANISTA_PODER_MAGICO": {
        "nome": "Poder Mágico",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Recebe +1 PM por nível de arcanista. ",
        "efeitos": {"pm_max_nivel": 1}
    },
    "ARCANISTA_RAIO_ARCANO": {
        "nome": "Raio Arcano",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Ação padrão: causa 1d8 (dano essência) em alcance curto. +1d8 por círculo máximo. Reflexos reduz metade. ",
        "efeitos": {}
    },

    # ==========================================================================
    # BÁRBARO
    # ==========================================================================
    "BARBARO_FURIA": {
        "nome": "Fúria",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 1,
        "descricao": "Gaste 2 PM: +2 ataque e dano corpo a corpo. Não pode concentrar. +1/+1 a cada 5 níveis. ",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "ataque_bonus": 2, "dano_bonus": 2, "escala_nivel": 5}
        }
    },
    "BARBARO_INSTINTO_SELVAGEM": {
        "nome": "Instinto Selvagem",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 3,
        "descricao": "Recebe +1 em Percepção, Reflexos e rolagens de dano. Aumenta a cada 6 níveis. ",
        "efeitos": {
            "bonus_pericia": {"Percepção": 1, "Reflexos": 1},
            "dano_bonus": 1
        }
    },
    "BARBARO_REDUCAO_DANO": {
        "nome": "Redução de Dano",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 5,
        "descricao": "Recebe RD 2. Aumenta em +2 a cada 3 níveis. ",
        "efeitos": {"rd_fixa": 2}
    },
    "BARBARO_FURIA_TITANICA": {
        "nome": "Fúria Titânica",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 20,
        "descricao": "O bônus de ataque e dano da Fúria é dobrado. ",
        "efeitos": {}
    },
    # --- PODERES DE BÁRBARO ---
    "BARBARO_ALMA_BRONZE": {
        "nome": "Alma de Bronze",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Ao entrar em Fúria, ganha PV temporários (Nível + Força). ",
        "efeitos": {}
    },
    "BARBARO_CRITICO_BRUTAL": {
        "nome": "Crítico Brutal",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Nível 6"],
        "descricao": "Multiplicador de crítico com armas corpo a corpo/arremesso aumenta em +1. ",
        "efeitos": {"multiplicador_critico_bonus": 1}
    },
    "BARBARO_ESQUIVA_SOBRENATURAL": {
        "nome": "Esquiva Sobrenatural",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Você nunca fica surpreendido. ",
        "efeitos": {"imunidade": ["surpreendido"]}
    },
    "BARBARO_FRENESI": {
        "nome": "Frenesi",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Em Fúria, gaste 2 PM para fazer um ataque extra por rodada. ",
        "efeitos": {}
    },
    "BARBARO_PELE_ACO": {
        "nome": "Pele de Aço",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Pele de Ferro", "Nível 8"],
        "descricao": "O bônus de Pele de Ferro aumenta para +8. ",
        "efeitos": {"defesa_bonus": 8}  # Substitui o anterior
    },
    "BARBARO_PELE_FERRO": {
        "nome": "Pele de Ferro",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Recebe +4 na Defesa (sem armadura pesada). ",
        "efeitos": {"defesa_bonus": 4}
    },
    "BARBARO_TOTEM_ESPIRITUAL": {
        "nome": "Totem Espiritual",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Sab 1", "Nível 4"],
        "descricao": "Soma Sabedoria aos PM. Escolha um animal totêmico para aprender uma magia (pode lançar em fúria). ",
        "efeitos": {"pm_soma_atributo": "sab", "escolha_totem": True}
    },

    # ==========================================================================
    # BARDO
    # ==========================================================================
    "BARDO_INSPIRACAO": {
        "nome": "Inspiração",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 1,
        "descricao": "Ação padrão, 2 PM: Aliados em alcance curto ganham +1 em perícias pela cena. Aumenta a cada 4 níveis. ",
        "efeitos": {"acao_ativavel": {"custo_pm": 2, "bonus_pericias_aliados": 1, "escala_nivel": 4}}
    },
    "BARDO_MAGIAS": {
        "nome": "Magias (Bardo)",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 1,
        "descricao": "Lança magias arcanas (atributo Car). Escolha 3 escolas. ",
        "efeitos": {"habilita_magia": {"tipo": "Arcana", "atributo": "car", "escolas_restritas": 3}}
    },
    "BARDO_ECLETICO": {
        "nome": "Eclético",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 2,
        "descricao": "Gaste 1 PM para receber benefícios de treino em uma perícia por um teste. ",
        "efeitos": {}
    },
    # --- PODERES DE BARDO ---
    "BARDO_ARTE_MAGICA": {
        "nome": "Arte Mágica",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Sob Inspiração, a CD de suas habilidades de bardo aumenta em +2. ",
        "efeitos": {}
    },
    "BARDO_AUMENTAR_REPERTORIO": {
        "nome": "Aumentar Repertório",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Aprende duas magias (arcanas ou divinas) das escolas conhecidas. ",
        "efeitos": {"magias_adicionais": 2}
    },
    "BARDO_DANCA_LAMINAS": {
        "nome": "Dança das Lâminas",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Esgrima Mágica", "Nível 10"],
        "descricao": "Ao lançar magia (padrão), gaste 1 PM para fazer ataque corpo a corpo (livre). ",
        "efeitos": {}
    },
    "BARDO_ESGRIMA_MAGICA": {
        "nome": "Esgrima Mágica",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Sob Inspiração, usa Atuação no lugar de Luta para armas leves/uma mão. ",
        "efeitos": {"ataque_pericia_troca": {"origem": "Luta", "destino": "Atuação"}}
    },
    "BARDO_GOLPE_ELEMENTAL": {
        "nome": "Golpe Elemental",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Golpe Mágico"],
        "descricao": "Sob Inspiração, ao acertar ataque, gaste 1 PM para +1d6 dano elemental. ",
        "efeitos": {}
    },
    "BARDO_PRESTIDIGITACAO": {
        "nome": "Prestidigitação",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Nível 6"],
        "descricao": "Ao fazer ação padrão, pode lançar magia (completa/menor) como livre com teste de Atuação. ",
        "efeitos": {}
    },

    # ==========================================================================
    # BUCANEIRO
    # ==========================================================================
    "BUCANEIRO_AUDACIA": {
        "nome": "Audácia",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 1,
        "descricao": "Gaste 2 PM para somar Carisma em um teste de perícia (exceto ataque). ",
        "efeitos": {}
    },
    "BUCANEIRO_INSOLENCIA": {
        "nome": "Insolência",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 1,
        "descricao": "Soma Carisma na Defesa (limitado pelo nível). Exige liberdade mov. ",
        "efeitos": {"defesa_soma_atributo": {"atributo": "car", "limite_por_nivel": True}}
    },
    "BUCANEIRO_EVASAO": {
        "nome": "Evasão",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 2,
        "descricao": "Não sofre dano se passar em Reflexos contra área. ",
        "efeitos": {"evasao": True}
    },
    "BUCANEIRO_ESQUIVA_SAGAZ": {
        "nome": "Esquiva Sagaz",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 3,
        "descricao": "+1 Defesa e Reflexos. Aumenta a cada 4 níveis. ",
        "efeitos": {"defesa_bonus": 1, "bonus_pericia": {"Reflexos": 1}}
    },
    "BUCANEIRO_PANACHE": {
        "nome": "Panache",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 5,
        "descricao": "Recupera 1 PM ao fazer crítico ou reduzir inimigo a 0 PV. ",
        "efeitos": {}
    },
    # --- PODERES DE BUCANEIRO ---
    "BUCANEIRO_APARAR": {
        "nome": "Aparar",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Esgrimista"],
        "descricao": "Reação (1 PM): Teste de ataque para bloquear ataque inimigo. ",
        "efeitos": {}
    },
    "BUCANEIRO_AVENTUREIRO_AVIDO": {
        "nome": "Aventureiro Ávido",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Gaste 5 PM para ação padrão ou movimento extra. ",
        "efeitos": {}
    },
    "BUCANEIRO_BRAVATA_AUDAZ": {
        "nome": "Bravata Audaz",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Jura façanha. Se cumprir, +2 PM por nível até fim da aventura. ",
        "efeitos": {}
    },
    "BUCANEIRO_EN_GARDE": {
        "nome": "En Garde",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Esgrimista"],
        "descricao": "Movimento (1 PM): +2 Defesa e margem de ameaça com armas leves/ágeis. ",
        "efeitos": {}
    },
    "BUCANEIRO_ESGRIMISTA": {
        "nome": "Esgrimista",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Int 1"],
        "descricao": "Soma Inteligência no dano com armas leves/ágeis (limitado por nível). ",
        "efeitos": {"dano_soma_atributo_extra": {"atributo": "int", "tipo_arma": ["leve", "ágil"]}}
    },
    "BUCANEIRO_PISTOLEIRO": {
        "nome": "Pistoleiro",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Proficiência em armas de fogo e +2 dano com elas. ",
        "efeitos": {"proficiencia_adicional": ["armas de fogo"], "dano_bonus_condicional": {"tipo": "arma_fogo", "valor": 2}}
    },

    # ==========================================================================
    # CAÇADOR
    # ==========================================================================
    "CACADOR_MARCA_PRESA": {
        "nome": "Marca da Presa",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 1,
        "descricao": "Movimento (1 PM): +1d4 dano contra criatura (cena). Aumenta dado a cada 4 níveis. ",
        "efeitos": {"dano_bonus_dado": "1d4"}
    },
    "CACADOR_RASTREADOR": {
        "nome": "Rastreador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 1,
        "descricao": "+2 Sobrevivência. Move normal rastreando. ",
        "efeitos": {"bonus_pericia": {"Sobrevivência": 2}}
    },
    "CACADOR_EXPLORADOR": {
        "nome": "Explorador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 3,
        "descricao": "Escolha terreno. +Sab em Defesa e perícias físicas nesse terreno. ",
        "efeitos": {"terreno_predileto_escolha": 1}
    },
    # --- PODERES DE CAÇADOR ---
    "CACADOR_AMBIDESTRIA": {
        "nome": "Ambidestria",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Des 2"],
        "descricao": "Ataca com duas armas com -2 de penalidade. ",
        "efeitos": {}
    },
    "CACADOR_ARQUEIRO": {
        "nome": "Arqueiro",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Sab 1"],
        "descricao": "Soma Sabedoria no dano à distância. ",
        "efeitos": {"dano_distancia_soma_atributo": "sab"}
    },
    "CACADOR_COMPANHEIRO_ANIMAL": {
        "nome": "Companheiro Animal",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Car 1", "Treinado em Adestramento"],
        "descricao": "Recebe parceiro animal. ",
        "efeitos": {"parceiro_adicional": 1}
    },
    "CACADOR_EMBOSCAR": {
        "nome": "Emboscar",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "Gaste 2 PM na primeira rodada para ação padrão extra. ",
        "efeitos": {}
    },
    "CACADOR_ESCARAMUCA": {
        "nome": "Escaramuça",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Des 2", "Nível 6"],
        "descricao": "Se mover 6m, ganha +2 Defesa/Reflexos e +1d8 dano. ",
        "efeitos": {}
    },
    "CACADOR_INIMIGO": {
        "nome": "Inimigo de (Tipo)",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Escolha tipo de criatura. Dobra dados da Marca da Presa contra ela. ",
        "efeitos": {"inimigo_predileto_escolha": 1}
    },

    # ==========================================================================
    # CAVALEIRO
    # ==========================================================================
    "CAVALEIRO_CODIGO_HONRA": {
        "nome": "Código de Honra",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 1,
        "descricao": "Não pode flanquear, atacar caído/desprevenido. Violação perde PM. ",
        "efeitos": {}
    },
    "CAVALEIRO_BALUARTE": {
        "nome": "Baluarte",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 1,
        "descricao": "1 PM (Reação): +2 Defesa e Resistência. Aumenta com nível. ",
        "efeitos": {}
    },
    "CAVALEIRO_DUELO": {
        "nome": "Duelo",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 2,
        "descricao": "2 PM: +2 ataque/dano contra alvo (x1). Bônus aumenta com nível. ",
        "efeitos": {}
    },
    # --- PODERES DE CAVALEIRO ---
    "CAVALEIRO_ARMADURA_HONRA": {
        "nome": "Armadura da Honra",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Início da cena: Ganha PV temporários (Nível + Car). ",
        "efeitos": {}
    },
    "CAVALEIRO_DESPREZAR_COVARDES": {
        "nome": "Desprezar os Covardes",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Recebe RD 5 se estiver caído, desprevenido ou flanqueado. ",
        "efeitos": {}
    },
    "CAVALEIRO_ESCUDEIRO": {
        "nome": "Escudeiro",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Parceiro que dá +1 Dano, +1 Defesa e ações auxiliares. ",
        "efeitos": {"dano_bonus": 1, "defesa_bonus": 1}
    },
    "CAVALEIRO_ESTANDARTE": {
        "nome": "Estandarte",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Título", "Nível 14"],
        "descricao": "Início da cena: Aliados ganham PM temporários igual Car. ",
        "efeitos": {}
    },
    "CAVALEIRO_POSTURA_PROVOCACAO": {
        "nome": "Postura: Provocação Petulante",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Inimigos em alcance curto devem atacar você (Vontade CD Car). ",
        "efeitos": {}
    },
    "CAVALEIRO_SOLIDEZ": {
        "nome": "Solidez",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Escudo"],
        "descricao": "Soma bônus do escudo nos testes de resistência. ",
        "efeitos": {}
    },

    # ==========================================================================
    # CLÉRIGO
    # ==========================================================================
    "CLERIGO_DEVOTO": {
        "nome": "Devoto Fiel",
        "tipo": "Habilidade de Classe",
        "classe": "Clérigo",
        "nivel": 1,
        "descricao": "Escolha divindade. Ganha 2 Poderes Concedidos (ou Panteão). ",
        "efeitos": {"escolha_divindade": True, "poderes_concedidos_bonus": 1}
    },
    "CLERIGO_MAGIAS": {
        "nome": "Magias (Clérigo)",
        "tipo": "Habilidade de Classe",
        "classe": "Clérigo",
        "nivel": 1,
        "descricao": "Lança magias divinas (Sab). Começa com 3 de 1º círculo. ",
        "efeitos": {"habilita_magia": {"tipo": "Divina", "atributo": "sab", "circulo_max": 1}}
    },
    # --- PODERES DE CLÉRIGO ---
    "CLERIGO_ABENCOAR_ARMA": {
        "nome": "Abençoar Arma",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Proficiência arma divindade. 3 PM: Arma mágica, +dano, usa Sab no ataque/dano. ",
        "efeitos": {}
    },
    "CLERIGO_CANALIZAR": {
        "nome": "Canalizar Energia",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Libera onda de Luz (cura/dano) ou Trevas (dano/cura). ",
        "efeitos": {}
    },
    "CLERIGO_CONHECIMENTO_MAGICO": {
        "nome": "Conhecimento Mágico",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Aprende duas magias divinas. ",
        "efeitos": {"magias_adicionais": 2}
    },
    "CLERIGO_MISSA_ESCUDO": {
        "nome": "Missa: Escudo Divino",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa concede +1 Defesa e Resistência por 1 dia. ",
        "efeitos": {}
    },
    "CLERIGO_PRECE_COMBATE": {
        "nome": "Prece de Combate",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Lança magia (padrão) como movimento pagando +2 PM. ",
        "efeitos": {}
    },
    "CLERIGO_SIMBOLO_ENERGIZADO": {
        "nome": "Símbolo Sagrado Energizado",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Movimento (1 PM): Símbolo brilha, reduz custo de magias em -1 PM. ",
        "efeitos": {}
    },

    # ==========================================================================
    # DRUIDA
    # ==========================================================================
    "DRUIDA_DEVOTO": {
        "nome": "Devoto Fiel (Druida)",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Devoto de Allihanna, Megalokk ou Oceano. Ganha 2 Poderes Concedidos. ",
        "efeitos": {"escolha_divindade": {"restrito": ["Allihanna", "Megalokk", "Oceanus"]}, "poderes_concedidos_bonus": 1}
    },
    "DRUIDA_EMPATIA": {
        "nome": "Empatia Selvagem",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Comunica com animais. Usa Adestramento para diplomacia. ",
        "efeitos": {"pericia_adestramento_persuasao": True}
    },
    "DRUIDA_MAGIAS": {
        "nome": "Magias (Druida)",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Lança magias divinas (Sab). Escolha 3 escolas. ",
        "efeitos": {"habilita_magia": {"tipo": "Divina", "atributo": "sab", "escolas_restritas": 3}}
    },
    "DRUIDA_CAMINHO_ERMOS": {
        "nome": "Caminho dos Ermos",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 2,
        "descricao": "Ignora terreno difícil natural. ",
        "efeitos": {"imunidade_terreno_dificil_natural": True}
    },
    # --- PODERES DE DRUIDA ---
    "DRUIDA_ASPECTO_VERAO": {
        "nome": "Aspecto do Verão",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende magia Transmutação. Gaste 1 PM para arma flamejante (+1d6 fogo). ",
        "efeitos": {"magia_adicional_escola": "Transmutação"}
    },
    "DRUIDA_COMPANHEIRO_ANIMAL": {
        "nome": "Companheiro Animal",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Car 1", "Treinado em Adestramento"],
        "descricao": "Recebe parceiro animal. ",
        "efeitos": {"parceiro_adicional": 1}
    },
    "DRUIDA_FORCA_PENHASCOS": {
        "nome": "Força dos Penhascos",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Nível 4"],
        "descricao": "+2 Fortitude. Gaste PM para reduzir dano (RD 10/PM). ",
        "efeitos": {"bonus_pericia": {"Fortitude": 2}}
    },
    "DRUIDA_FORMA_SELVAGEM": {
        "nome": "Forma Selvagem",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "3 PM: Transforma em animal (bônus físicos variados). ",
        "efeitos": {"forma_selvagem": True}
    },
    "DRUIDA_MAGIA_NATURAL": {
        "nome": "Magia Natural",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Forma Selvagem"],
        "descricao": "Lança magias em forma selvagem. ",
        "efeitos": {}
    },
    "DRUIDA_SEGREDOS_NATUREZA": {
        "nome": "Segredos da Natureza",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende duas magias (arcanas ou divinas) das escolas conhecidas. ",
        "efeitos": {"magias_adicionais": 2}
    },

    # ==========================================================================
    # GUERREIRO
    # ==========================================================================
    "GUERREIRO_ATAQUE_ESPECIAL": {
        "nome": "Ataque Especial",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 1,
        "descricao": "1 PM: +4 ataque ou dano. Escala a cada 4 níveis. ",
        "efeitos": {}
    },
    "GUERREIRO_DURAO": {
        "nome": "Durão",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 3,
        "descricao": "Ao sofrer dano, gaste 3 PM para reduzir à metade. ",
        "efeitos": {}
    },
    "GUERREIRO_ATAQUE_EXTRA": {
        "nome": "Ataque Extra",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 6,
        "descricao": "Ao agredir, gaste 2 PM para ataque extra. ",
        "efeitos": {}
    },
    # --- PODERES DE GUERREIRO ---
    "GUERREIRO_AMBIDESTRIA": {
        "nome": "Ambidestria",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Des 2"],
        "descricao": "Ataca com duas armas com -2 de penalidade. ",
        "efeitos": {}
    },
    "GUERREIRO_ARQUEIRO": {
        "nome": "Arqueiro",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Sab 1"],
        "descricao": "Soma Sabedoria no dano à distância. ",
        "efeitos": {"dano_distancia_soma_atributo": "sab"}
    },
    "GUERREIRO_BATER_CORRER": {
        "nome": "Bater e Correr",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Move após investida. 2 PM: investida em terreno difícil sem penalidade defesa. ",
        "efeitos": {}
    },
    "GUERREIRO_ESGRIMISTA": {
        "nome": "Esgrimista",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Int 1"],
        "descricao": "Soma Inteligência no dano com armas leves/ágeis. ",
        "efeitos": {"dano_soma_atributo_extra": {"atributo": "int", "tipo_arma": ["leve", "ágil"]}}
    },
    "GUERREIRO_GOLPE_PESSOAL": {
        "nome": "Golpe Pessoal",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Nível 5"],
        "descricao": "Cria ataque especial com efeitos variados (Impactante, Brutal, Elemental, etc). ",
        "efeitos": {"golpe_pessoal_slot": 1}
    },
    "GUERREIRO_VALENTAO": {
        "nome": "Valentão",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "+2 ataque/dano contra caídos, desprevenidos, flanqueados. ",
        "efeitos": {}
    },

    # ==========================================================================
    # INVENTOR
    # ==========================================================================
    "INVENTOR_ENGENHOSIDADE": {
        "nome": "Engenhosidade",
        "tipo": "Habilidade de Classe",
        "classe": "Inventor",
        "nivel": 1,
        "descricao": "2 PM: Soma Inteligência em teste de perícia (exceto ataque). ",
        "efeitos": {}
    },
    "INVENTOR_PROTOTIPO": {
        "nome": "Protótipo",
        "tipo": "Habilidade de Classe",
        "classe": "Inventor",
        "nivel": 1,
        "descricao": "Começa com item superior ou alquímicos (T$ 500). ",
        "efeitos": {}
    },
    # --- PODERES DE INVENTOR ---
    "INVENTOR_AGITE_ANTES": {
        "nome": "Agite Antes de Usar",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Ofício (alquimista)"],
        "descricao": "Gaste PM para aumentar dano de alquímicos (+1d/PM). ",
        "efeitos": {}
    },
    "INVENTOR_ALQUIMISTA_INICIADO": {
        "nome": "Alquimista Iniciado",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Int 1", "Sab 1", "Treinado em Ofício (alquimista)"],
        "descricao": "Recebe livro de fórmulas, faz poções (1º e 2º círculo). ",
        "efeitos": {"fabricar_pocao": True}
    },
    "INVENTOR_ARMEIRO": {
        "nome": "Armeiro",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Luta", "Treinado em Ofício (armeiro)"],
        "descricao": "Proficiência armas marciais corpo a corpo. Usa Int no ataque/dano. ",
        "efeitos": {"proficiencia_adicional": ["marciais"], "ataque_atributo_troca": "int"}
    },
    "INVENTOR_BALISTICA": {
        "nome": "Balística",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Pontaria", "Treinado em Ofício (armeiro)"],
        "descricao": "Proficiência armas marciais distância/fogo. Usa Int no ataque. ",
        "efeitos": {"proficiencia_adicional": ["marciais distância", "fogo"], "ataque_atributo_troca": "int"}
    },
    "INVENTOR_ENGENHOQUEIRO": {
        "nome": "Engenhoqueiro",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Int 3", "Treinado em Ofício (engenhoqueiro)"],
        "descricao": "Pode fabricar engenhocas que simulam magias. ",
        "efeitos": {"fabricar_engenhoca": True}
    },
    "INVENTOR_MAESTRIA_PERICIA": {
        "nome": "Maestria em Perícia",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "descricao": "Escolha perícias igual Int. Pode gastar 1 PM para escolher 10 nelas. ",
        "efeitos": {"maestria_escolhas": "int"}
    },

    # ==========================================================================
    # LADINO
    # ==========================================================================
    "LADINO_ATAQUE_FURTIVO": {
        "nome": "Ataque Furtivo",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 1,
        "descricao": "+1d6 dano em desprevenidos/flanqueados (1/rodada). Aumenta a cada 2 níveis. ",
        "efeitos": {"dano_furtivo_base": "1d6"}
    },
    "LADINO_ESPECIALISTA": {
        "nome": "Especialista",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 1,
        "descricao": "1 PM: Dobra bônus de treino em perícias escolhidas (Qtd = Int). ",
        "efeitos": {"especialista_slots": "int"}
    },
    "LADINO_EVASAO": {
        "nome": "Evasão",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 2,
        "descricao": "Não sofre dano se passar em Reflexos contra área. ",
        "efeitos": {"evasao": True}
    },
    "LADINO_ESQUIVA_SOBRENATURAL": {
        "nome": "Esquiva Sobrenatural",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 4,
        "descricao": "Nunca fica surpreendido. ",
        "efeitos": {"imunidade": ["surpreendido"]}
    },
    # --- PODERES DE LADINO ---
    "LADINO_ASSASSINAR": {
        "nome": "Assassinar",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Nível 5"],
        "descricao": "3 PM: Analisa alvo. Dobra dados de ataque furtivo. ",
        "efeitos": {}
    },
    "LADINO_EMBOSCAR": {
        "nome": "Emboscar",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "2 PM: Ação padrão extra na primeira rodada. ",
        "efeitos": {}
    },
    "LADINO_MENTE_CRIMINOSA": {
        "nome": "Mente Criminosa",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Int 1"],
        "descricao": "Soma Inteligência em Ladinagem e Furtividade. ",
        "efeitos": {"pericia_soma_atributo": {"Ladinagem": "int", "Furtividade": "int"}}
    },
    "LADINO_ROLAMENTO_DEFENSIVO": {
        "nome": "Rolamento Defensivo",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Reflexos"],
        "descricao": "Reação (2 PM): Reduz dano à metade. Fica caído. ",
        "efeitos": {}
    },
    "LADINO_SOMBRA": {
        "nome": "Sombra",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "+2 Furtividade. Sem penalidade por mover. ",
        "efeitos": {"bonus_pericia": {"Furtividade": 2}}
    },
    "LADINO_TRUQUE_MAGICO": {
        "nome": "Truque Mágico",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Int 1"],
        "descricao": "Aprende uma magia arcana de 1º círculo (Int). ",
        "efeitos": {"magia_adicional_arcana": 1}
    },
    "LADINO_VELOCIDADE_LADINA": {
        "nome": "Velocidade Ladina",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Des 2", "Treinado em Iniciativa"],
        "descricao": "2 PM: Ação de movimento extra. ",
        "efeitos": {}
    },

    # ==========================================================================
    # LUTADOR
    # ==========================================================================
    "LUTADOR_BRIGA": {
        "nome": "Briga",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 1,
        "descricao": "Dano desarmado 1d6. Aumenta com nível. ",
        "efeitos": {"dano_desarmado_base": "1d6"}
    },
    "LUTADOR_GOLPE_RELAMPAGO": {
        "nome": "Golpe Relâmpago",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 1,
        "descricao": "1 PM: Ataque desarmado extra ao agredir. ",
        "efeitos": {}
    },
    "LUTADOR_CASCA_GROSSA": {
        "nome": "Casca Grossa",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 3,
        "descricao": "Soma Constituição na Defesa (se sem armadura pesada). ",
        "efeitos": {"defesa_soma_atributo": "con"}
    },
    # --- PODERES DE LUTADOR ---
    "LUTADOR_ATE_ACERTAR": {
        "nome": "Até Acertar",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "Se errar, recebe +2 cumulativo no próximo ataque. ",
        "efeitos": {}
    },
    "LUTADOR_BRACOS_CALEJADOS": {
        "nome": "Braços Calejados",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "Soma Força na Defesa (se sem armadura). ",
        "efeitos": {"defesa_soma_atributo": "for"}
    },
    "LUTADOR_GOLPE_BAIXO": {
        "nome": "Golpe Baixo",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "2 PM: Acerto exige Fortitude ou atordoa alvo. ",
        "efeitos": {}
    },
    "LUTADOR_LINGUA_BECOS": {
        "nome": "Língua dos Becos",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "requisitos": ["For 1", "Treinado em Intimidação"],
        "descricao": "1 PM: Usa Força em vez de Carisma em perícia social. ",
        "efeitos": {}
    },
    "LUTADOR_TROCACAO": {
        "nome": "Trocação",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "requisitos": ["Nível 6"],
        "descricao": "Ao acertar, paga PM (1, 2, 3...) para atacar de novo. ",
        "efeitos": {}
    },
    "LUTADOR_VOADORA": {
        "nome": "Voadora",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "2 PM: Investida causa +1d6 dano a cada 3m deslocado. ",
        "efeitos": {}
    },

    # ==========================================================================
    # NOBRE
    # ==========================================================================
    "NOBRE_AUTOCONFIANCA": {
        "nome": "Autoconfiança",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Usa Carisma na Defesa em vez de Destreza. ",
        "efeitos": {"defesa_atributo_troca": "car"}
    },
    "NOBRE_ESPOLIO": {
        "nome": "Espólio",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Recebe item de até T$ 2.000. ",
        "efeitos": {"item_inicial_extra_valor": 2000}
    },
    "NOBRE_ORGULHO": {
        "nome": "Orgulho",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Gaste PM para ganhar +2 em perícia por PM. ",
        "efeitos": {}
    },
    "NOBRE_RIQUEZA": {
        "nome": "Riqueza",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 3,
        "descricao": "Recebe dinheiro (Teste Carisma x Nível) uma vez por aventura. ",
        "efeitos": {}
    },
    # --- PODERES DE NOBRE ---
    "NOBRE_ARMADURA_BRILHANTE": {
        "nome": "Armadura Brilhante",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Nível 8"],
        "descricao": "Soma Carisma na Defesa com armadura pesada (substitui Des). ",
        "efeitos": {}
    },
    "NOBRE_GRITO_TIRANICO": {
        "nome": "Grito Tirânico",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Nível 8"],
        "descricao": "Palavras Afiadas vira ação completa, d8 dano e atinge área. ",
        "efeitos": {}
    },
    "NOBRE_INSPIRAR_CONFIANCA": {
        "nome": "Inspirar Confiança",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "descricao": "2 PM: Aliado rerola teste recém realizado. ",
        "efeitos": {}
    },
    "NOBRE_INSPIRAR_GLORIA": {
        "nome": "Inspirar Glória",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Inspirar Confiança", "Nível 8"],
        "descricao": "5 PM: Aliado ganha ação padrão extra. ",
        "efeitos": {}
    },
    "NOBRE_LINGUA_PRATA": {
        "nome": "Língua de Prata",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "descricao": "2 PM: Soma metade do nível em perícia de Carisma. ",
        "efeitos": {}
    },

    # ==========================================================================
    # PALADINO
    # ==========================================================================
    "PALADINO_ABENCOADO": {
        "nome": "Abençoado",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "Soma Carisma aos PM. Devoto ganha 2 poderes concedidos. ",
        "efeitos": {"pm_soma_atributo": "car", "poderes_concedidos_bonus": 1}
    },
    "PALADINO_CODIGO_HEROI": {
        "nome": "Código do Herói",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "Deve manter palavra, proteger inocentes, não mentir/roubar. Violação perde PM. ",
        "efeitos": {}
    },
    "PALADINO_GOLPE_DIVINO": {
        "nome": "Golpe Divino",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "2 PM: Soma Car no ataque e +1d8 dano. Aumenta com nível. ",
        "efeitos": {}
    },
    "PALADINO_CURA_MAOS": {
        "nome": "Cura pelas Mãos",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 2,
        "descricao": "Movimento (1 PM): Cura 1d8+1 PV (toque). Aumenta com nível. ",
        "efeitos": {}
    },
    "PALADINO_AURA_SAGRADA": {
        "nome": "Aura Sagrada",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 3,
        "descricao": "1 PM (Sustentada): +Carisma em testes de resistência para aliados em 9m. ",
        "efeitos": {}
    },
    "PALADINO_BENCAO_JUSTICA": {
        "nome": "Bênção da Justiça",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 5,
        "descricao": "Escolha: Égide Sagrada (Bônus Defesa) ou Montaria Sagrada. ",
        "efeitos": {"escolha_bencao": ["Égide Sagrada", "Montaria Sagrada"]}
    },
    # --- PODERES DE PALADINO ---
    "PALADINO_ARMA_SAGRADA": {
        "nome": "Arma Sagrada",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "Golpe Divino com arma da divindade usa d12. ",
        "efeitos": {}
    },
    "PALADINO_AURA_CURA": {
        "nome": "Aura de Cura",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "requisitos": ["Nível 6"],
        "descricao": "Aura cura 5 + Carisma no início do turno. ",
        "efeitos": {}
    },
    "PALADINO_AURA_PODEROSA": {
        "nome": "Aura Poderosa",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "requisitos": ["Nível 6"],
        "descricao": "Raio da aura aumenta para 30m. ",
        "efeitos": {}
    },
    "PALADINO_JULGAMENTO_VINDICACAO": {
        "nome": "Julgamento: Vindicação",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "2 PM: Marca inimigo. +1 ataque / +1d8 dano contra ele. ",
        "efeitos": {}
    },
    "PALADINO_VIRTUDE_TEMPERANCA": {
        "nome": "Virtude: Temperança",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "Itens consumíveis (poções/comida) rendem o dobro. +PM passivo. ",
        "efeitos": {"pm_bonus_virtude": True}
    }
}
