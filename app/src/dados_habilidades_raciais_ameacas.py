# -*- coding: utf-8 -*-
"""Habilidades de Raça do suplemento Ameaças de Arton (T20 JdA).

Estritamente baseado no texto oficial do livro Ameaças de Arton.
"""

_F = "Ameaças de Arton"

DADOS_HABILIDADES_RACIAIS_AMEACAS = {
    # ── BUGBEAR ──
    "Empunhadura_Poderosa_Bugbear": {
        "nome": "Empunhadura Poderosa",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Ao usar uma arma feita para uma categoria de tamanho maior que a sua, a penalidade "
            "que você sofre nos testes de ataque diminui para –2. Caso receba esta habilidade "
            "novamente, a penalidade diminui para 0 e você pode também usar armas de até duas "
            "categorias de tamanho maiores que a sua com uma penalidade de –5 nos testes de ataque."
        ),
        "efeitos": {"empunhadura_poderosa": True},
    },
    "Saborear_Pavor_Bugbear": {
        "nome": "Saborear Pavor",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode usar Força como atributo-chave de Intimidação (em vez de Carisma). "
            "Além disso, se estiver em alcance curto de outra criatura abalada ou apavorada, "
            "você recebe um bônus em testes de ataque igual à penalidade causada pela condição."
        ),
        "efeitos": {"pericia_atributo_opcao": {"Intimidação": "for"}},
    },
    "Sentidos_Predador_Bugbear": {
        "nome": "Sentidos de Predador",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe faro e visão no escuro.",
        "efeitos": {"faro": True, "visao_escuro": True},
    },

    # ── CENTAURO ──
    "Avantajado_Centauro": {
        "nome": "Avantajado",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Seu tamanho é Grande e seu deslocamento é 12m.",
        "efeitos": {"deslocamento": 12},
    },
    "Cascos_Centauro": {
        "nome": "Cascos",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de cascos (dano 1d8, crítico x2, impacto). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com os cascos."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Cascos", "dano": "1d8", "critico": "x2", "tipo": "Impacto"},
            "ataque_extra_pm": 1,
        },
    },
    "Ginete_Natural_Centauro": {
        "nome": "Ginete Natural",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é considerado montado para efeito de fazer investidas e para benefícios das armas "
            "que empunha, e pode escolher o poder Carga de Cavalaria mesmo sem cumprir seus pré-requisitos. "
            "Entretanto, não pode se beneficiar de uma montaria e, se estiver carregando um cavaleiro, "
            "sofre –2 em testes (além das penalidades de sobrecarga, se houver) e é considerado em "
            "condição ruim para lançar magias."
        ),
        "efeitos": {"ginete_natural": True},
    },
    "Medo_Altura_Ameacas": {
        "nome": "Medo de Altura",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Se estiver adjacente a uma queda de 3m ou mais (como um buraco ou penhasco), você fica abalado.",
        "efeitos": {"medo_de_altura": True},
    },

    # ── CERATOPS ──
    "Chifres_Ceratops": {
        "nome": "Chifres",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de chifres (dano 1d8, crítico x2, perfuração). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com os chifres."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Chifres", "dano": "1d8", "critico": "x2", "tipo": "Perfuração"},
            "ataque_extra_pm": 1,
        },
    },
    "Paquidermico_Ceratops": {
        "nome": "Paquidérmico",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Seu tamanho é Grande. Você recebe +1 na Defesa e pode usar Força como atributo-chave de Intimidação (em vez de Carisma).",
        "efeitos": {"defesa_bonus": 1, "pericia_atributo_opcao": {"Intimidação": "for"}},
    },
    "Papel_Tribal_Ceratops": {
        "nome": "Papel Tribal",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é treinado em uma perícia a sua escolha entre Cura, Intimidação, Ofício ou Sobrevivência.",
        "efeitos": {
            "pericia_escolha": 1,
            "pericia_opcoes": ["Cura", "Intimidação", "Ofício", "Sobrevivência"],
        },
    },

    # ── ELFO-DO-MAR ──
    "Arsenal_Oceano_ElfoMar": {
        "nome": "Arsenal do Oceano",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você recebe proficiência em arpão, rede e tridente e +2 em testes de ataque com essas armas. "
            "Se receber proficiência em uma dessas armas novamente, pode considerá-la uma arma leve."
        ),
        "efeitos": {
            "proficiencia_simples": ["arpão", "rede", "tridente"],
            "bonus_ataque_arma": {"arpão": 2, "rede": 2, "tridente": 2},
        },
    },
    "Cria_Aguas_ElfoMar": {
        "nome": "Cria das Águas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui deslocamento de natação igual a seu deslocamento em terra e visão na penumbra. "
            "Quando dentro d'água, você recebe percepção às cegas e +2 na Defesa, em Furtividade e Sobrevivência."
        ),
        "efeitos": {
            "visao_penumbra": True,
            "deslocamento_natacao_igual": True,
            "bonus_pericia_condicional": {"Furtividade": 2, "Sobrevivência": 2},
        },
    },
    "Dependencia_Agua_ElfoMar": {
        "nome": "Dependência de Água",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Se permanecer mais de um dia sem contato com água, você não recupera PM com descanso "
            "até voltar para a água (ou, pelo menos, tomar um bom banho!)."
        ),
        "efeitos": {},
    },

    # ── FINNTROLL ──
    "Corpo_Vegetal_Finntroll": {
        "nome": "Corpo Vegetal",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é uma criatura do tipo monstro e recebe natureza vegetal e visão no escuro.",
        "efeitos": {"tipo_criatura": "Monstro", "visao_escuro": True},
    },
    "Presenca_Arcana_Finntroll": {
        "nome": "Presença Arcana",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Misticismo e resistência a magia +2.",
        "efeitos": {"bonus_pericia": {"Misticismo": 2}, "resistencia_magia_bonus": 2},
    },
    "Regeneracao_Vegetal_Finntroll": {
        "nome": "Regeneração Vegetal",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Uma vez por rodada, você pode gastar 1 PM para recuperar 5 PV. Esta habilidade não cura dano de ácido ou fogo.",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Livre",
                "alcance": "Pessoal",
                "duracao": "Instantânea",
                "efeito": "Recupera 5 PV (não cura ácido ou fogo)",
            }
        },
    },
    "Intolerancia_Luz_Finntroll": {
        "nome": "Intolerância a Luz",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe sensibilidade a luz e, quando exposto à luz do sol ou similar, não consegue ativar sua Regeneração Vegetal.",
        "efeitos": {"sensibilidade_luz": True},
    },

    # ── GNOLL ──
    "Faro_Ameacas": {
        "nome": "Faro",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você tem olfato apurado. Contra inimigos em alcance curto que não possa ver, "
            "você não fica desprevenido e camuflagem total lhe causa apenas 20% de chance de falha."
        ),
        "efeitos": {"faro": True},
    },
    "Mordida_1d6_Perf_Ameacas": {
        "nome": "Mordida",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de mordida (dano 1d6, crítico x2, perfuração). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com a mordida."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Mordida", "dano": "1d6", "critico": "x2", "tipo": "Perfuração"},
            "ataque_extra_pm": 1,
        },
    },
    "Mordida_1d8_Perf_Ameacas": {
        "nome": "Mordida",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de mordida (dano 1d8, crítico x2, perfuração). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com a mordida."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Mordida", "dano": "1d8", "critico": "x2", "tipo": "Perfuração"},
            "ataque_extra_pm": 1,
        },
    },
    "Oportunista_Gnoll": {
        "nome": "Oportunista",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 nas rolagens de dano contra criaturas que tenham sofrido dano de outras criaturas desde seu último turno.",
        "efeitos": {},
    },
    "Rendicao_Gnoll": {
        "nome": "Rendição",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Quando um inimigo se rende, você recebe 1d4 PM temporários cumulativos. Da mesma forma, "
            "quando é reduzido a um quarto de seus PV ou menos, seu instinto é se render. Caso continue lutando, fica alquebrado."
        ),
        "efeitos": {},
    },

    # ── HARPIA ──
    "Asas_Abutre_Harpia": {
        "nome": "Asas de Abutre",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui asas no lugar dos braços e das mãos. Você pode pairar a 1,5m do chão com deslocamento 12m. "
            "Isso permite que você ignore terreno difícil e o torna imune a dano por queda (a menos que esteja inconsciente). "
            "Se não estiver usando armadura pesada, você pode gastar 1 PM por rodada para voar com deslocamento de 12m."
        ),
        "efeitos": {"deslocamento": 12, "deslocamento_voo": 12},
    },
    "Cria_Masmorra_Harpia": {
        "nome": "Cria de Masmorra",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é uma criatura do tipo monstro e recebe visão no escuro e +2 em Intimidação e Sobrevivência.",
        "efeitos": {
            "tipo_criatura": "Monstro",
            "visao_escuro": True,
            "bonus_pericia": {"Intimidação": 2, "Sobrevivência": 2},
        },
    },
    "Grito_Aterrorizante_Harpia": {
        "nome": "Grito Aterrorizante",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você pode gastar uma ação padrão e 1 PM para emitir um grito estridente. Criaturas em alcance curto ficam abaladas (Von CD Car evita).",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Padrão",
                "alcance": "Curto",
                "duracao": "Cena",
                "resistencia": "Vontade CD Car evita",
                "efeito": "Criaturas em alcance curto ficam abaladas",
            }
        },
    },
    "Pes_Rapinantes_Ameacas": {
        "nome": "Pés Rapinantes",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Seus pés podem ser usados como mãos ou como duas armas naturais de garras (dano 1d6 cada, crítico x2, corte). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com uma arma, você pode gastar 1 PM para fazer um "
            "ataque corpo a corpo extra com uma das garras, desde que ela esteja livre e não tenha sido usada para atacar neste turno."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Garras", "dano": "1d6", "critico": "x2", "tipo": "Corte"},
            "ataque_extra_pm": 1,
        },
    },

    # ── HOBGOBLIN ──
    "Arte_Guerra_Hobgoblin": {
        "nome": "Arte da Guerra",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é treinado em Guerra e recebe proficiência em armas marciais. "
            "Se receber essa proficiência novamente, recebe +2 em rolagens de dano com essas armas."
        ),
        "efeitos": {"pericia_treino": ["Guerra"], "proficiencia_marciais": True},
    },
    "Metalurgia_Hobgoblin": {
        "nome": "Metalurgia Hobgoblin",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você recebe +2 em Ofício (armeiro) e, se for treinado nesta perícia, pode fabricar armas e armaduras "
            "superiores com uma melhoria. Se aprender a fabricar itens superiores desses tipos por outra habilidade, "
            "gasta apenas 1/4 do preço das melhorias que aplica nesses itens (em vez de 1/3)."
        ),
        "efeitos": {"bonus_pericia": {"Ofício (Armeiro)": 2}},
    },
    "Taticas_Guerrilha_Hobgoblin": {
        "nome": "Táticas de Guerrilha",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em Furtividade.",
        "efeitos": {"visao_escuro": True, "bonus_pericia": {"Furtividade": 2}},
    },

    # ── KALLYANACH ──
    "Heranca_Draconica_Kallyanach": {
        "nome": "Herança Dracônica",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é uma criatura do tipo monstro e recebe redução 5 contra um tipo de dano a sua escolha "
            "entre ácido, eletricidade, fogo, frio, luz ou trevas."
        ),
        "efeitos": {"tipo_criatura": "Monstro", "resistencia_rd_escolha": 5},
    },
    "Bencao_Kallyadranoch_Kallyanach": {
        "nome": "Bênção de Kallyadranoch",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Escolha dois poderes entre: Armamento Kallyanach (arma natural 1d6 cauda/chifres/mordida), "
            "Asas Dracônicas (1 PM/rodada voar 9m, vulnerável), Escamas Elementais (+2 Defesa e RD 10 da Herança), "
            "Prática Arcana (magia arcana 1º círculo do elemento, Int), Sentidos Dracônicos (faro e visão no escuro) "
            "ou Sopro de Dragão (ação padrão, 1 PM, cone 6m 1d12 do elemento, Ref CD Con metade). "
            "Uma vez por patamar, você pode escolher uma bênção no lugar de um poder de classe."
        ),
        "efeitos": {},
    },

    # ── KAIJIN ──
    "Couraca_Rubra_Kaijin": {
        "nome": "Couraça Rubra",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe redução de dano 2. Sua couraça conta como um poder da Tormenta, exceto para perda de Carisma.",
        "efeitos": {"rd": 2, "conta_poder_tormenta_sem_perda_car": True},
    },
    "Cria_Tormenta_Kaijin": {
        "nome": "Cria da Tormenta",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é uma criatura do tipo monstro e recebe +5 em testes de resistência contra efeitos causados "
            "por lefeu e pela Tormenta. Além disso, efeitos da Tormenta que não afetem lefou também não afetam você."
        ),
        "efeitos": {"tipo_criatura": "Monstro", "resistencia_tormenta": 5},
    },
    "Disforme_Kaijin": {
        "nome": "Disforme",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Por sua anatomia anômala, você não pode empunhar nem vestir itens, a menos que sejam mágicos ou "
            "especialmente adaptados para você (+50% do preço, 1 dia). Seus itens iniciais já são adaptados. "
            "Esta habilidade conta como um poder da Tormenta, exceto para perda de Carisma."
        ),
        "efeitos": {"conta_poder_tormenta_sem_perda_car": True},
    },
    "Terror_Vivo_Kaijin": {
        "nome": "Terror Vivo",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode usar Força como atributo-chave de Intimidação (em vez de Carisma) e recebe um poder "
            "da Tormenta a sua escolha, que não conta para perda de Carisma."
        ),
        "efeitos": {"pericia_atributo_opcao": {"Intimidação": "for"}},
    },

    # ── KAPPA ──
    "Alma_Agua_Kappa": {
        "nome": "Alma da Água",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é uma criatura do tipo espírito e tem deslocamento de natação igual ao seu deslocamento terrestre.",
        "efeitos": {"tipo_criatura": "Espírito", "deslocamento_natacao_igual": True},
    },
    "Carapaca_Kappa": {
        "nome": "Carapaça Kappa",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você não pode ser flanqueado e recebe cobertura leve se estiver submerso ou caído. "
            "Você soma sua Constituição na Defesa, limitado pelo seu nível, mas apenas se não estiver usando "
            "armaduras pesadas (se já faz isso, como por Casca Grossa, em vez disso recebe +2 na Defesa)."
        ),
        "efeitos": {
            "defesa_soma_atributo": {
                "atributo": "con",
                "limite_por_nivel": True,
                "sem_armadura_pesada": True,
            },
            "imune_flanqueado": True,
        },
    },
    "Cura_Aguas_Kappa": {
        "nome": "Cura das Águas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode lançar a magia Curar Ferimentos (atributo-chave Sabedoria). Caso aprenda novamente essa magia, "
            "seu custo diminui em –1 PM. Você não pode usar esta habilidade se a água de sua cabeça estiver derramada."
        ),
        "efeitos": {
            "magia_adicional": {"nome": "Curar Ferimentos", "atributo": "Sab"},
            "reducao_custo_magia": {"nomes": ["Curar Ferimentos"], "valor": 1},
        },
    },
    "Tigela_Dagua_Kappa": {
        "nome": "Tigela D'água",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Sempre que falhar por 5 ou mais em um teste para evitar ser agarrado, derrubado ou empurrado, "
            "você derrama a água de sua cabeça. Você fica enjoado até encher a tigela novamente (ação padrão em fonte de água)."
        ),
        "efeitos": {},
    },

    # ── KOBOLDS ──
    "Ajuntamento_Escamoso_Kobolds": {
        "nome": "Ajuntamento Escamoso",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Para todos os efeitos vocês são uma única criatura Média com dois braços. Contam como Pequenos "
            "para espaços por onde podem passar, rolam dois dados e usam o melhor resultado em testes de "
            "resistência contra efeitos de alvo único sem dano, e têm vulnerabilidade a dano de área."
        ),
        "efeitos": {},
    },
    "Praga_Monstruosa_Kobolds": {
        "nome": "Praga Monstruosa",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Vocês são criaturas do tipo monstro e recebem visão no escuro e +2 em Sobrevivência.",
        "efeitos": {"tipo_criatura": "Monstro", "visao_escuro": True, "bonus_pericia": {"Sobrevivência": 2}},
    },
    "Sensibilidade_Luz_Ameacas": {
        "nome": "Sensibilidade a Luz",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Quando exposto à luz do sol ou similar, você fica ofuscado.",
        "efeitos": {"sensibilidade_luz": True},
    },
    "Talentos_Bando_Kobolds": {
        "nome": "Talentos do Bando",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Escolham dois poderes entre: Amontoados, Armadilha Terrível, Diferentão, Ex-Familiar (+2 PM e familiar), "
            "O Ousado, Os do Fundo, Organizadinhos (Des p/ carga +1 item vestido), Pestes Oportunistas (+1d6 dano), "
            "Somos Explosivos ou Tática de Enxame. Uma vez por patamar, podem escolher outro no lugar de um poder de classe."
        ),
        "efeitos": {},
    },

    # ── MASHIN (CHASSI DE GOLEM) ──
    "Chassi_Mashin": {
        "nome": "Mashin (Chassi)",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Golens especiais criados com técnicas tamuranianas. +1 em dois atributos a sua escolha, "
            "sempre Médio. Você se torna treinado em duas perícias a sua escolha e pode substituir uma "
            "dessas perícias por uma Maravilha Mecânica."
        ),
        "efeitos": {"tipo_criatura": "Construto", "visao_escuro": True, "pericia_escolha": 2},
    },
    "Maravilha_Mecanica_Mashin": {
        "nome": "Maravilha Mecânica",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Poderes exclusivos de Mashin (uma vez por patamar pode escolher um no lugar de um poder de classe): "
            "Adaptação Elemental, Arma Acoplada, Arma Elemental, Auxílio de Mira, Caminho da Perfeição, "
            "Canalizar Reparos, Canhão Energético, Dínamo de Mana, Pernas Aprimoradas ou Reservatório Alquímico."
        ),
        "efeitos": {},
    },

    # ── NEZUMI ──
    "Pequeno_Mas_Nao_Metade_Nezumi": {
        "nome": "Pequeno, Mas Não Metade",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Seu tamanho é Pequeno, mas seu deslocamento se mantém 9m e você recebe resistência a medo +5 "
            "contra criaturas maiores que você e +2 em Intimidação."
        ),
        "efeitos": {"deslocamento": 9, "bonus_pericia": {"Intimidação": 2}},
    },
    "Roedor_Nezumi": {
        "nome": "Roedor",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de mordida (dano 1d6, crítico x2, corte). Uma vez por rodada, "
            "quando usa a ação agredir para atacar com outra arma, pode gastar 1 PM para fazer um ataque "
            "corpo a corpo extra com a mordida. Em um acerto crítico com a mordida, avaria a armadura da "
            "vítima ou aumenta em +1 o multiplicador do crítico se ela estiver sem armadura."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Mordida", "dano": "1d6", "critico": "x2", "tipo": "Corte"},
            "ataque_extra_pm": 1,
        },
    },
    "Sentidos_Murideos_Nezumi": {
        "nome": "Sentidos Murídeos",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe faro e visão na penumbra.",
        "efeitos": {"faro": True, "visao_penumbra": True},
    },

    # ── MEIO-ORC ──
    "Adaptavel_MeioOrc": {
        "nome": "Adaptável",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Intimidação e se torna treinado em uma perícia a sua escolha.",
        "efeitos": {"bonus_pericia": {"Intimidação": 2}, "pericia_escolha": 1},
    },
    "Criatura_Profundezas_MeioOrc": {
        "nome": "Criatura das Profundezas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em testes de Percepção e Sobrevivência realizados no subterrâneo.",
        "efeitos": {"visao_escuro": True, "bonus_pericia_condicional": {"Percepção": 2, "Sobrevivência": 2}},
    },
    "Sangue_Orc_MeioOrc": {
        "nome": "Sangue Orc",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +1 em rolagens de dano com armas corpo a corpo e de arremesso e é considerado um orc para efeitos relacionados a raça.",
        "efeitos": {"bonus_dano_corpo_a_corpo": 1},
    },

    # ── ORC ──
    "Feroz_Orc": {
        "nome": "Feroz",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você recebe +2 em rolagens de dano com armas corpo a corpo e de arremesso. "
            "Quando sofre dano de um inimigo, esse bônus se torna +4 até o fim de seu próximo turno."
        ),
        "efeitos": {"bonus_dano_corpo_a_corpo": 2},
    },
    "Habitante_Cavernas_Orc": {
        "nome": "Habitante das Cavernas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em testes de Percepção e Sobrevivência realizados no subterrâneo. Entretanto, recebe sensibilidade a luz.",
        "efeitos": {
            "visao_escuro": True,
            "sensibilidade_luz": True,
            "bonus_pericia_condicional": {"Percepção": 2, "Sobrevivência": 2},
        },
    },
    "Vigor_Brutal_Orc": {
        "nome": "Vigor Brutal",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Fortitude e soma sua Força em seu total de pontos de vida.",
        "efeitos": {"bonus_pericia": {"Fortitude": 2}, "pv_soma_atributo": "forca"},
    },

    # ── MINAURO ──
    "Mente_Aberta_Minauro": {
        "nome": "Mente Aberta",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Diplomacia e Investigação.",
        "efeitos": {"bonus_pericia": {"Diplomacia": 2, "Investigação": 2}},
    },
    "Plurivalente_Minauro": {
        "nome": "Plurivalente",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe um poder geral a sua escolha.",
        "efeitos": {"poder_geral_escolha": 1},
    },

    # ── MOREAU (12 HERANÇAS) ──
    "Heranca_Moreau_Base": {
        "nome": "Herança",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Sua herança animal determina suas habilidades de raça. Além disso, você é considerado também um humano para quaisquer fins.",
        "efeitos": {},
    },
    "Espreitador_Moreau_Coruja": {
        "nome": "Espreitador",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em Percepção e Vontade.",
        "efeitos": {"visao_escuro": True, "bonus_pericia": {"Percepção": 2, "Vontade": 2}},
    },
    "Garras_1d6_Corte_Ameacas": {
        "nome": "Garras",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você tem duas armas naturais de garra (dano 1d6, crítico x2, corte), uma em cada mão. "
            "Uma vez por rodada, quando usa a ação agredir para atacar com uma arma, você pode gastar 1 PM "
            "para fazer um ataque corpo a corpo extra com uma das garras livre."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Garras", "dano": "1d6", "critico": "x2", "tipo": "Corte"},
            "ataque_extra_pm": 1,
        },
    },
    "Sapiencia_Moreau_Coruja": {
        "nome": "Sapiência",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você pode lançar uma magia de 1º círculo de adivinhação a sua escolha (atributo-chave Sabedoria). Caso aprenda novamente essa magia, seu custo diminui em –1 PM.",
        "efeitos": {},
    },
    "Destemor_Moreau_Hiena": {
        "nome": "Destemor",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em rolagens de dano e em testes de resistência contra criaturas maiores que você.",
        "efeitos": {},
    },
    "Agarra_Me_Se_Puderes_Moreau_Raposa": {
        "nome": "Agarra-me Se Puderes",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Seu deslocamento é 12m (em vez de 9m) e você tem visão na penumbra.",
        "efeitos": {"deslocamento": 12, "visao_penumbra": True},
    },
    "Esperteza_Vulpina_Moreau_Raposa": {
        "nome": "Esperteza Vulpina",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em duas perícias originalmente baseadas em Inteligência ou Carisma, a sua escolha.",
        "efeitos": {},
    },
    "Arboricola_Moreau_Serpente": {
        "nome": "Arborícola",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe deslocamento de escalada 6m e +2 em Furtividade.",
        "efeitos": {"deslocamento_escalada": 6, "bonus_pericia": {"Furtividade": 2}},
    },
    "Constritor_Moreau_Serpente": {
        "nome": "Constritor",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em testes para agarrar e em rolagens de dano contra criaturas que estiver agarrando.",
        "efeitos": {},
    },
    "Instintos_Traicoeiros_Moreau_Serpente": {
        "nome": "Instintos Traiçoeiros",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em Diplomacia e na CD de seus efeitos mentais.",
        "efeitos": {"visao_escuro": True, "bonus_pericia": {"Diplomacia": 2}},
    },
    "Chifres_1d6_Moreau_Bufalo": {
        "nome": "Chifres",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de chifres (dano 1d6, crítico x2, perfuração). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com os chifres."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Chifres", "dano": "1d6", "critico": "x2", "tipo": "Perfuração"},
            "ataque_extra_pm": 1,
        },
    },
    "Marrada_Impressionante_Moreau_Bufalo": {
        "nome": "Marrada Impressionante",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em ataques em investida e em testes para empurrar, e pode usar Força como atributo-chave de Intimidação (em vez de Carisma).",
        "efeitos": {"pericia_atributo_opcao": {"Intimidação": "for"}},
    },
    "Patas_Ligeiras_Moreau_Coelho": {
        "nome": "Patas Ligeiras",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Seu deslocamento é 12m e, quando faz uma investida ou um teste de Atletismo para correr, você não precisa percorrer uma linha reta.",
        "efeitos": {"deslocamento": 12},
    },
    "Pe_Coelho_Moreau_Coelho": {
        "nome": "Pé de Coelho",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Quando faz um teste de uma perícia baseada em Destreza (exceto testes de ataque), você pode gastar 1 PM para rolar dois dados e usar o melhor resultado.",
        "efeitos": {},
    },
    "Senso_Preservacao_Moreau_Coelho": {
        "nome": "Senso de Preservação",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra e +2 em Percepção e Reflexos.",
        "efeitos": {"visao_penumbra": True, "bonus_pericia": {"Percepção": 2, "Reflexos": 2}},
    },
    "Mordida_Poderosa_Moreau_Crocodilo": {
        "nome": "Mordida Poderosa",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de mordida (dano 1d6, crítico x2, perfuração), com a qual recebe +2 em testes de agarrar. "
            "Uma vez por rodada, quando usa a ação agredir com outra arma, pode gastar 1 PM para um ataque extra com a mordida."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Mordida", "dano": "1d6", "critico": "x2", "tipo": "Perfuração"},
            "ataque_extra_pm": 1,
        },
    },
    "Predador_Aquatico_Moreau_Crocodilo": {
        "nome": "Predador Aquático",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você tem deslocamento de natação 6m e recebe +1 na Defesa e +2 em Furtividade.",
        "efeitos": {"deslocamento_natacao": 6, "defesa_bonus": 1, "bonus_pericia": {"Furtividade": 2}},
    },
    "Surto_Reptiliano_Moreau_Crocodilo": {
        "nome": "Surto Reptiliano",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Uma vez por cena, você pode gastar 1 PM para realizar uma ação de movimento adicional em seu turno.",
        "efeitos": {},
    },
    "Muitas_Vidas_Gato_Moreau_Gato": {
        "nome": "As Muitas Vidas de um Gato",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você soma seu Carisma em testes de Constituição para estabilizar sangramento e em Acrobacia e, se estiver consciente em uma queda, reduz o dano dela em 3d6.",
        "efeitos": {},
    },
    "Sentidos_Felinos_Moreau_Gato": {
        "nome": "Sentidos Felinos",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra e +2 em Furtividade e Percepção.",
        "efeitos": {"visao_penumbra": True, "bonus_pericia": {"Furtividade": 2, "Percepção": 2}},
    },
    "Rugido_Imponente_Moreau_Leao": {
        "nome": "Rugido Imponente",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você pode gastar uma ação de movimento e 1 PM para emitir um rugido assustador. Todos os inimigos em alcance curto sofrem –2 em rolagens de dano por 1 rodada. Medo.",
        "efeitos": {},
    },
    "Sentidos_Realeza_Moreau_Leao": {
        "nome": "Sentidos da Realeza",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra e +2 em Intimidação e Percepção.",
        "efeitos": {"visao_penumbra": True, "bonus_pericia": {"Intimidação": 2, "Percepção": 2}},
    },
    "Taticas_Matilha_Moreau_Lobo": {
        "nome": "Táticas de Matilha",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 nas rolagens de dano e na margem de ameaça em ataques contra oponentes que esteja flanqueando.",
        "efeitos": {},
    },
    "Asas_Moreau_Morcego": {
        "nome": "Asas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode pairar a 1,5m do chão com deslocamento 9m (ignora terreno difícil, imune a queda). "
            "Sem armadura pesada, pode gastar 1 PM/rodada para voar 12m. Ao pairar/voar ocupa espaço de 1 tamanho maior."
        ),
        "efeitos": {"deslocamento_voo": 12},
    },
    "Criatura_Noite_Moreau_Morcego": {
        "nome": "Criatura da Noite",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão no escuro e +2 em Furtividade e Percepção.",
        "efeitos": {"visao_escuro": True, "bonus_pericia": {"Furtividade": 2, "Percepção": 2}},
    },
    "Ecolocalizacao_Moreau_Morcego": {
        "nome": "Ecolocalização",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você pode gastar 1 PM para receber percepção às cegas em alcance médio por 1 rodada.",
        "efeitos": {},
    },
    "Abraco_Urso_Moreau_Urso": {
        "nome": "Abraço de Urso",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é Grande e pode usar Constituição como atributo-chave de Intimidação (em vez de Carisma).",
        "efeitos": {"pericia_atributo_opcao": {"Intimidação": "con"}},
    },

    # ── NAGAH ──
    "Cauda_Nagah": {
        "nome": "Cauda",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você possui uma arma natural de cauda (dano 1d6, crítico x2, impacto). "
            "Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, "
            "pode gastar 1 PM para fazer um ataque corpo a corpo extra com a cauda."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Cauda", "dano": "1d6", "critico": "x2", "tipo": "Impacto"},
            "ataque_extra_pm": 1,
        },
    },
    "Inocencia_Dissimulada_Nagah": {
        "nome": "Inocência Dissimulada",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Enganação e pode gastar 2 PM para substituir um teste de perícia originalmente baseada em Inteligência, Sabedoria ou Carisma por Enganação.",
        "efeitos": {"bonus_pericia": {"Enganação": 2}},
    },
    "Presentes_Sszzaas_Nagah": {
        "nome": "Presentes de Sszzaas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra, +1 na Defesa e resistência a veneno +5.",
        "efeitos": {"visao_penumbra": True, "defesa_bonus": 1, "resistencia_veneno": 5},
    },
    "Fraquezas_Ofidicas_Nagah": {
        "nome": "Fraquezas Ofídicas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você sofre 1 ponto de dano adicional para cada dado de dano de frio e –5 em testes de resistência contra Músicas de bardo.",
        "efeitos": {"vulnerabilidade_dado": {"frio": 1}},
    },

    # ── OGRO ──
    "Quanto_Maior_Tamanho_Ogro": {
        "nome": "Quanto Maior o Tamanho…",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é um humanoide do subtipo gigante; seu tamanho é Grande e você recebe visão na penumbra.",
        "efeitos": {"visao_penumbra": True},
    },
    "Maior_Porrada_Ogro": {
        "nome": "…Maior a Porrada!",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Quando acerta um ataque corpo a corpo, você pode gastar 1 PM para causar +1d8 pontos de dano do mesmo tipo.",
        "efeitos": {},
    },
    "Camada_Ingenuidade_Ogro": {
        "nome": "Camada de Ingenuidade",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você sofre –5 em Intuição e Vontade.",
        "efeitos": {"bonus_pericia": {"Intuição": -5, "Vontade": -5}},
    },

    # ── PTEROS ──
    "Ligacao_Natural_Pteros": {
        "nome": "Ligação Natural",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você possui uma ligação mental com uma criatura inteligente (Int –3 ou mais) em alcance longo, sabendo direção e distância. Pode trocar no início de cada aventura.",
        "efeitos": {},
    },
    "Maos_Rudimentares_Pteros": {
        "nome": "Mãos Rudimentares",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Suas mãos não permitem empunhar itens, a menos que sejam mágicos ou adaptados (+50% preço, 1 dia). Itens iniciais já são adaptados.",
        "efeitos": {},
    },
    "Senhor_Ceus_Pteros": {
        "nome": "Senhor dos Céus",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode pairar a 1,5m do chão com deslocamento 9m (ignora terreno difícil, imune a queda). "
            "Sem armadura pesada, pode gastar 1 PM/rodada para voar 12m. Ao pairar/voar ocupa espaço de 1 tamanho maior."
        ),
        "efeitos": {"deslocamento_voo": 12},
    },
    "Sentidos_Rapinantes_Pteros": {
        "nome": "Sentidos Rapinantes",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra e +2 em Percepção e Sobrevivência.",
        "efeitos": {"visao_penumbra": True, "bonus_pericia": {"Percepção": 2, "Sobrevivência": 2}},
    },

    # ── VELOCIS ──
    "Atraves_Espinheiros_Velocis": {
        "nome": "Através de Espinheiros",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe resistência a corte e perfuração 2 e não sofre redução em seu deslocamento por terreno difícil natural.",
        "efeitos": {"rd_tipo": {"corte": 2, "perfuração": 2}, "imunidade_terreno_dificil_natural": True},
    },
    "Sentidos_Selvagens_Ameacas": {
        "nome": "Sentidos Selvagens",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em Sobrevivência, visão na penumbra e faro.",
        "efeitos": {"bonus_pericia": {"Sobrevivência": 2}, "visao_penumbra": True, "faro": True},
    },
    "Velocista_Planicie_Velocis": {
        "nome": "Velocista da Planície",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Seu deslocamento é 12m. Você pode usar Destreza como atributo-chave de Atletismo (em vez de Força) e rola dois dados em Atletismo para correr ou saltar.",
        "efeitos": {"deslocamento": 12, "pericia_atributo_opcao": {"Atletismo": "des"}},
    },

    # ── VORACIS ──
    "Rainha_Selva_Voracis": {
        "nome": "Rainha da Selva",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe deslocamento de escalada 9m, +2 em Atletismo e recupera +1 PV por nível quando descansa.",
        "efeitos": {"deslocamento_escalada": 9, "bonus_pericia": {"Atletismo": 2}},
    },

    # ── SOTERRADO (VARIANTE DE OSTEON) ──
    "Abraco_Gelido_Soterrado": {
        "nome": "Abraço Gélido",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +2 em testes para agarrar. Além disso, seus ataques desarmados e com armas naturais causam 2 pontos de dano de frio extras.",
        "efeitos": {},
    },
    "Esquife_Gelo_Soterrado": {
        "nome": "Esquife de Gelo",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe redução de corte e perfuração 5 e redução de frio 10. Entretanto, sofre 1 ponto de dano adicional por dado de dano de fogo.",
        "efeitos": {
            "rd_tipo": {"corte": 5, "perfuração": 5, "frio": 10},
            "vulnerabilidade_dado": {"fogo": 1},
        },
    },

    # ── TABRACHI ──
    "Batraquio_Tabrachi": {
        "nome": "Batráquio",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe visão na penumbra e deslocamento de natação igual ao seu deslocamento terrestre.",
        "efeitos": {"visao_penumbra": True, "deslocamento_natacao_igual": True},
    },
    "Linguarudo_Tabrachi": {
        "nome": "Linguarudo",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Sua língua é uma arma natural que pode atacar inimigos a até 3m (dano 1d4, crítico x2, impacto). "
            "É versátil (+2 em testes para desarmar e derrubar). Uma vez por rodada, ao usar agredir com outra arma, "
            "pode gastar 1 PM para fazer um ataque extra com a língua."
        ),
        "efeitos": {
            "arma_natural": {"nome": "Língua", "dano": "1d4", "critico": "x2", "tipo": "Impacto", "alcance": "3m"},
            "ataque_extra_pm": 1,
        },
    },
    "Saltador_Tabrachi": {
        "nome": "Saltador",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você recebe +10 em testes de Atletismo para saltar.",
        "efeitos": {},
    },

    # ── TROG ANÃO (VARIANTE DE TROG) ──
    "Quase_Anao_TrogAnao": {
        "nome": "Quase Anão",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é uma criatura do tipo monstro e recebe visão no escuro e +1 PV por nível. "
            "Além disso, seu deslocamento é 6m (em vez de 9m), mas não é reduzido por uso de armadura ou excesso de carga."
        ),
        "efeitos": {
            "tipo_criatura": "Monstro",
            "visao_escuro": True,
            "pv_max_nivel": 1,
            "deslocamento": 6,
            "imunidade_penalidade_mov": ["armadura", "carga"],
        },
    },

    # ── TENGU ──
    "Asas_Desorientadoras_Tengu": {
        "nome": "Asas Desorientadoras",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Se não estiver usando as asas para voar, você recebe os benefícios de Finta Aprimorada (ou +5 em Enganação para fintar se já tiver o poder).",
        "efeitos": {},
    },
    "Caminhante_Ceu_Tengu": {
        "nome": "Caminhante do Céu",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você pode pairar a 1,5m do chão com deslocamento 9m (ignora terreno difícil, imune a queda). "
            "Pode gastar 1 PM/rodada para voar 12m. Ao pairar/voar ocupa espaço de 1 tamanho maior."
        ),
        "efeitos": {"deslocamento_voo": 12},
    },
    "Espirito_Corvino_Tengu": {
        "nome": "Espírito Corvino",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "Você é uma criatura do tipo espírito e recebe visão no escuro e +2 em Percepção.",
        "efeitos": {"tipo_criatura": "Espírito", "visao_escuro": True, "bonus_pericia": {"Percepção": 2}},
    },

    # ── YIDISHAN ──
    "Hibrido_Mecanico_Yidishan": {
        "nome": "Híbrido Mecânico",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você é uma criatura do tipo construto. Recebe visão no escuro e imunidade a cansaço, efeitos metabólicos "
            "e veneno. Não precisa respirar, alimentar-se ou dormir (cura mundana reduzida à metade; recarrega inerte por 8h)."
        ),
        "efeitos": {"tipo_criatura": "Construto", "visao_escuro": True},
    },
    "Natureza_Organica_Yidishan": {
        "nome": "Natureza Orgânica",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": (
            "Você se torna treinado em uma perícia (não precisa ser da classe) ou recebe um poder geral a sua escolha. "
            "Como alternativa, pode ser um yidishan de outra raça humanoide e ganhar uma habilidade dessa raça."
        ),
        "efeitos": {"pericia_ou_poder_escolha": 1},
    },
    "Pecas_Metalicas_Yidishan": {
        "nome": "Peças Metálicas",
        "tipo": "Racial",
        "fonte": _F,
        "descricao": "As partes mecânicas que complementam seu corpo fornecem +2 na Defesa, mas impõem uma penalidade de armadura de –2.",
        "efeitos": {"defesa_bonus": 2, "penalidade_armadura": -2},
    },
}
