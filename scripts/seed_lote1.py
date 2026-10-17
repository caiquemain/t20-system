import requests
import json

API_URL = "http://localhost:8000/ameacas/"

ameacas_lote1 = [
    {
        "nome": "Alma Acorrentada",
        "nd": "8", "tipo": "Morto-vivo", "subtipo": None, "tamanho": "Médio", "papel": "especial",
        "iniciativa": 14, "percepcao": 9, "sentidos": ["visão no escuro"],
        "defesa": 26, "fortitude": 14, "reflexos": 19, "vontade": 8,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 56, "pontos_de_mana": None, "deslocamento": "voo 9m (6q)",
        "ataques": [{"nome": "Toque cáustico", "modalidade": "corpo a corpo", "bonus_ataque": 26, "dano": "2d6+10", "tipo_dano": "ácido", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}],
        "habilidades": [
            {"nome": "Agarrar Oportunista", "tipo_acao": "livre", "descricao": "Ao acertar um ataque, faz manobra agarrar (teste +28). Contra criatura agarrada, a alma é corpórea. Se matar, ambas desaparecem.", "rolls": []},
            {"nome": "Aura Cáustica", "tipo_acao": "automática", "descricao": "Início do turno: 6d6 de ácido em todas as criaturas adjacentes. Quem morre na aura não ressuscita.", "rolls": ["6d6"]},
            {"nome": "Invisibilidade Rubra", "tipo_acao": "passiva", "descricao": "Camuflagem total em áreas de Tormenta; vira leve até o próximo turno após atacar.", "rolls": []}
        ],
        "atributos": {"forca": None, "destreza": 7, "constituicao": 2, "inteligencia": 1, "sabedoria": 0, "carisma": -2},
        "pericias": [{"nome": "Furtividade", "bonus": 15, "observacao": "+25 em áreas de Tormenta"}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 18}
    },
    {
        "nome": "Bruxo da Tormenta",
        "nd": "8", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 5, "percepcao": 6, "sentidos": [],
        "defesa": 27, "fortitude": 6, "reflexos": 12, "vontade": 18,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 142, "pontos_de_mana": 41, "deslocamento": "9m (6q)",
        "ataques": [],
        "habilidades": [
            {"nome": "Cuspir Enxame", "tipo_acao": "completa", "custo_pm": 2, "descricao": "Enxame rubro Médio em alcance curto. No fim do turno, 4d6 ácido a quem estiver no espaço. Mover: ação de movimento, 9m.", "rolls": ["4d6"]},
            {"nome": "Mente Aberrante", "tipo_acao": "reação", "descricao": "Ao fazer teste de Vontade, causa 5d6 psíquico em quem gerou o efeito.", "rolls": ["5d6"]},
            {"nome": "Raio Arcano", "tipo_acao": "padrão", "custo_pm": 1, "descricao": "2d12 trevas em alcance médio, sem cura de PV por 1 rodada (Ref CD 24 reduz à metade).", "rolls": ["2d12"]},
            {"nome": "Magias (bruxo 6º)", "tipo_acao": "passiva", "descricao": "CD 24. Inclui: Névoa, Raio do Enfraquecimento, Sussurros Insanos, Velocidade.", "rolls": []}
        ],
        "atributos": {"forca": -1, "destreza": 0, "constituicao": 2, "inteligencia": 5, "sabedoria": 1, "carisma": -2},
        "pericias": [{"nome": "Conhecimento", "bonus": 12}, {"nome": "Misticismo", "bonus": 15}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 20}
    },
    {
        "nome": "Arquibruxo da Tormenta",
        "nd": "15", "tipo": "Monstro", "subtipo": "lefou", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 13, "percepcao": 16, "sentidos": ["visão no escuro"],
        "defesa": 45, "fortitude": 14, "reflexos": 22, "vontade": 28,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": ["magia +2"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 486, "pontos_de_mana": 105, "deslocamento": "9m (6q), voo 12m (8q)",
        "ataques": [],
        "habilidades": [
            {"nome": "Abominar a Realidade", "tipo_acao": "passiva", "descricao": "Ignora terreno difícil; efeitos contra ele têm 50% de falha.", "rolls": []},
            {"nome": "Arcano de Batalha", "tipo_acao": "passiva", "descricao": "Soma Int nas rolagens de dano de magias e Raio Arcano.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d10 PM (Von CD 40 evita).", "rolls": ["2d10"]},
            {"nome": "Magia Acelerada", "tipo_acao": "livre", "custo_pm": 4, "descricao": "1x/rodada: muda execução de magia para livre.", "rolls": []},
            {"nome": "Mente Aberrante", "tipo_acao": "reação", "descricao": "Ao resistir com Vontade, causa 12d6 psíquico no gerador.", "rolls": ["12d6"]},
            {"nome": "Raio Arcano", "tipo_acao": "padrão", "custo_pm": 1, "descricao": "4d12+7 trevas, sem cura por 1 rodada (Ref CD 40).", "rolls": ["4d12+7"]},
            {"nome": "Magias (bruxo 14º)", "tipo_acao": "passiva", "descricao": "CD 40. Desintegrar, Dissipar Magia, Momento de Tormenta, Seta Infalível, Sussurros Insanos, Velocidade.", "rolls": []}
        ],
        "atributos": {"forca": -1, "destreza": 2, "constituicao": 5, "inteligencia": 7, "sabedoria": 0, "carisma": -2},
        "pericias": [{"nome": "Conhecimento", "bonus": 20}, {"nome": "Intimidação", "bonus": 19}, {"nome": "Misticismo", "bonus": 28}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 20}
    },
    {
        "nome": "Enxame Infernal",
        "nd": "11", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Grande", "papel": "especial",
        "iniciativa": 8, "percepcao": 7, "sentidos": ["visão no escuro"],
        "defesa": 33, "fortitude": 15, "reflexos": 23, "vontade": 8,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["enxame"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 350, "pontos_de_mana": None, "deslocamento": "3m (2q), voo 15m (10q)",
        "ataques": [],
        "habilidades": [
            {"nome": "Enxame", "tipo_acao": "automática", "descricao": "5d12 pontos de dano de perfuração.", "rolls": ["5d12"]},
            {"nome": "Drenar Existência", "tipo_acao": "passiva", "descricao": "Dano causado só pode ser curado após 24h ou após o enxame ser destruído.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d6 PM (Von CD 26 evita).", "rolls": ["2d6"]},
            {"nome": "Zumbido Repugnante", "tipo_acao": "passiva", "descricao": "Criatura que comece o turno em alcance curto fica alquebrada e surda (Fort CD 26 evita).", "rolls": []}
        ],
        "atributos": {"forca": None, "destreza": None, "constituicao": None, "inteligencia": None, "sabedoria": None, "carisma": None},
        "pericias": [{"nome": "Furtividade", "bonus": 9}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 21}
    },
    {
        "nome": "Esmagador Coletivo",
        "nd": "15", "tipo": "Construto", "subtipo": None, "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 12, "percepcao": 13, "sentidos": ["visão no escuro", "não pode ser flanqueado"],
        "defesa": 46, "fortitude": 28, "reflexos": 22, "vontade": 14,
        "defesas_especiais": {"reducao_dano": ["15"], "imunidades": ["acertos críticos", "metabolismo", "metamorfose", "paralisia"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 800, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Pancada", "modalidade": "corpo a corpo", "bonus_ataque": 39, "dano": "4d10+28", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "três pancadas"}],
        "habilidades": [
            {"nome": "Absorver", "tipo_acao": "completa", "descricao": "Absorve criatura Média ou menor agarrada há 3 rodadas. Vítima morre; esmagador ganha 20 PV temporários por nível dela.", "rolls": []},
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Pancada (teste +44).", "rolls": []},
            {"nome": "Arranhar", "tipo_acao": "livre", "descricao": "Início do turno: 4d10+28 de corte em criatura agarrada.", "rolls": ["4d10+28"]},
            {"nome": "Arremessar Corpos", "tipo_acao": "padrão", "descricao": "Arremessa 1d4+2 corpos em alcance longo, 4d8+15 impacto cada (Ref CD 40 evita).", "rolls": ["1d4+2", "4d8+15"]},
            {"nome": "Forma Horrenda", "tipo_acao": "passiva", "descricao": "Início do turno em alcance médio: apavorado 1d4 rodadas depois abalado (Von CD 40 muda para abalado).", "rolls": ["1d4"]},
            {"nome": "Pancada Estonteante", "tipo_acao": "passiva", "descricao": "Vítima da pancada fica atordoada 1 rodada (Fort CD 40 evita; 1x por cena).", "rolls": []}
        ],
        "atributos": {"forca": 14, "destreza": -1, "constituicao": 15, "inteligencia": None, "sabedoria": 0, "carisma": None},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 22}
    },
    {
        "nome": "Infecto",
        "nd": "2", "tipo": "Morto-vivo", "subtipo": None, "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 4, "percepcao": 4, "sentidos": ["visão no escuro"],
        "defesa": 20, "fortitude": 14, "reflexos": 4, "vontade": 4,
        "defesas_especiais": {"reducao_dano": ["5/corte"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 30, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 16, "dano": "1d8+9", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "mais doença"}],
        "habilidades": [
            {"nome": "Doença", "tipo_acao": "passiva", "descricao": "Mordida expõe à infecção escarlate.", "rolls": []},
            {"nome": "Parasitas Famintos", "tipo_acao": "passiva", "descricao": "Criatura que comece o turno adjacente ou ataque corpo a corpo é exposta à infecção escarlate (Ref CD 17 evita).", "rolls": []}
        ],
        "atributos": {"forca": 4, "destreza": 1, "constituicao": 3, "inteligencia": None, "sabedoria": 1, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 23}
    },
    {
        "nome": "Turba de Infectos",
        "nd": "6", "tipo": "Morto-vivo", "subtipo": None, "tamanho": "Grande", "papel": "lacaio",
        "iniciativa": 6, "percepcao": 6, "sentidos": ["visão no escuro"],
        "defesa": 30, "fortitude": 16, "reflexos": 6, "vontade": 6,
        "defesas_especiais": {"reducao_dano": ["5/corte"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 80, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Mordida (bandos)", "modalidade": "corpo a corpo", "bonus_ataque": 26, "dano": "2d8+26", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "mais doença"}],
        "habilidades": [
            {"nome": "Doença", "tipo_acao": "passiva", "descricao": "Mordida expõe à infecção escarlate.", "rolls": []},
            {"nome": "Parasitas Famintos", "tipo_acao": "passiva", "descricao": "Criatura que comece o turno adjacente ou ataque corpo a corpo contra a turba é exposta à infecção escarlate (Ref CD 24 evita).", "rolls": []}
        ],
        "atributos": {"forca": 4, "destreza": 1, "constituicao": 3, "inteligencia": None, "sabedoria": 1, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 23}
    },
    {
        "nome": "Lefeu, Veridak",
        "nd": "10", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 12, "percepcao": 15, "sentidos": ["visão no escuro"],
        "defesa": 34, "fortitude": 9, "reflexos": 22, "vontade": 15,
        "defesas_especiais": {"reducao_dano": ["5"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 264, "pontos_de_mana": None, "deslocamento": "9m (6q), voo 36m (24q)",
        "ataques": [
            {"nome": "Lâmina", "modalidade": "corpo a corpo", "bonus_ataque": 29, "dano": "2d6+13", "tipo_dano": "corte", "margem_critico": 18, "multiplicador_critico": 3, "pericia": "Luta", "descricao": "duas lâminas"},
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 29, "dano": "1d6+13", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Garra (teste +31).", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d6 PM (Von CD 26 evita).", "rolls": ["2d6"]},
            {"nome": "Relâmpago Rubro", "tipo_acao": "completa", "descricao": "Investida com 2 lâminas + 2 garras contra o mesmo alvo, +2 de investida; pode continuar se movendo.", "rolls": []}
        ],
        "atributos": {"forca": 6, "destreza": 4, "constituicao": 3, "inteligencia": -1, "sabedoria": 2, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 24}
    },
    {
        "nome": "Lefeu, Hurobakk",
        "nd": "11", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 16, "percepcao": 14, "sentidos": ["visão no escuro"],
        "defesa": 35, "fortitude": 21, "reflexos": 16, "vontade": 9,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 380, "pontos_de_mana": None, "deslocamento": "15m (10q)",
        "ataques": [
            {"nome": "Pinça", "modalidade": "corpo a corpo", "bonus_ataque": 28, "dano": "2d8+13", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas pinças"},
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 28, "dano": "1d8+13", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d8 PM (Von CD 28 evita).", "rolls": ["2d8"]},
            {"nome": "Investida Rubra", "tipo_acao": "completa", "descricao": "Investida com duas pinças, +4d8 de dano em cada; pode continuar se movendo.", "rolls": ["4d8"]},
            {"nome": "Passar por Cima", "tipo_acao": "completa", "descricao": "Percorre até dobro do deslocamento: 6d8+30 impacto e caída (Ref CD 28 reduz e evita).", "rolls": ["6d8+30"]},
            {"nome": "Pinças Destruidoras", "tipo_acao": "passiva", "descricao": "Pinça avaria armadura/escudo do alvo, ou +2d8 se sem armadura (Ref CD 28 evita).", "rolls": ["2d8"]}
        ],
        "atributos": {"forca": 8, "destreza": 3, "constituicao": 5, "inteligencia": 1, "sabedoria": 2, "carisma": -2},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 25}
    },
    {
        "nome": "Lefeu, Burodron",
        "nd": "11", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 9, "percepcao": 15, "sentidos": ["percepção às cegas (médio)", "visão no escuro"],
        "defesa": 42, "fortitude": 24, "reflexos": 19, "vontade": 12,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 550, "pontos_de_mana": None, "deslocamento": "15m (10q), escalada 15m (10q), escavação 15m (10q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 35, "dano": "3d8+23", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 35, "dano": "2d8+14", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Dilacerar", "tipo_acao": "passiva", "descricao": "Se acerta as duas garras na mesma criatura no mesmo turno, causa +8d6+8.", "rolls": ["8d6+8"]},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d8 PM (Von CD 31 evita).", "rolls": ["2d8"]},
            {"nome": "Morte que Vem da Terra", "tipo_acao": "completa", "descricao": "Mergulha no solo e emerge em alcance médio: 8d8+32 impacto e caídas em alcance curto (Ref CD 31 reduz e evita).", "rolls": ["8d8+32"]}
        ],
        "atributos": {"forca": 10, "destreza": 0, "constituicao": 6, "inteligencia": -1, "sabedoria": 1, "carisma": -3},
        "pericias": [{"nome": "Atletismo", "bonus": 19}, {"nome": "Furtividade", "bonus": 9, "observacao": "+19 quando enterrado"}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 26}
    },
    {
        "nome": "Lefeu, Morgadrel",
        "nd": "13", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 10, "percepcao": 18, "sentidos": ["visão no escuro"],
        "defesa": 47, "fortitude": 18, "reflexos": 13, "vontade": 26,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 670, "pontos_de_mana": None, "deslocamento": "15m (10q), natação 15m (10q)",
        "ataques": [{"nome": "Pinça", "modalidade": "corpo a corpo", "bonus_ataque": 40, "dano": "4d10+19", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas pinças"}],
        "habilidades": [
            {"nome": "Disparar Espinhos", "tipo_acao": "padrão", "descricao": "Esfera de 9m ao redor: 12d8+24 perfuração e fica fatigado por veneno (cumulativo) (Ref CD 35 reduz e evita).", "rolls": ["12d8+24"]},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d10 PM (Von CD 35 evita).", "rolls": ["2d10"]},
            {"nome": "Investida Surpresa", "tipo_acao": "passiva", "descricao": "Investida contra alvo surpreendido: dois ataques de pinça contra ele.", "rolls": []},
            {"nome": "Jato de Ácido", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Linha de 15m: 8d12 ácido, cobre com muco, +3d12 ácido no início dos próximos 2 turnos (Ref CD 35 reduz e evita muco).", "rolls": ["8d12", "3d12"]}
        ],
        "atributos": {"forca": 10, "destreza": 0, "constituicao": 7, "inteligencia": 1, "sabedoria": 3, "carisma": -1},
        "pericias": [{"nome": "Furtividade", "bonus": 10, "observacao": "+20 submerso"}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 26}
    },
    {
        "nome": "Lefeu, Ezzayn",
        "nd": "15", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 15, "percepcao": 18, "sentidos": ["visão no escuro"],
        "defesa": 46, "fortitude": 27, "reflexos": 25, "vontade": 16,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["bando"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 650, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Garra (bandos)", "modalidade": "corpo a corpo", "bonus_ataque": 49, "dano": "4d8+29", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}],
        "habilidades": [
            {"nome": "Enxame", "tipo_acao": "automática", "descricao": "14d8 corte.", "rolls": ["14d8"]},
            {"nome": "Anarquia Lacerante", "tipo_acao": "padrão", "descricao": "Ataque de garra contra cada criatura adjacente; um único teste contra a Defesa de cada alvo.", "rolls": []},
            {"nome": "Distorção Temporal", "tipo_acao": "passiva", "descricao": "Ação padrão ou de movimento adicional por turno.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "4d6 PM (Von CD 44 evita).", "rolls": ["4d6"]},
            {"nome": "Subjugar", "tipo_acao": "livre", "descricao": "Fim do turno: derrubar (teste +54) contra cada criatura em seu espaço; quem perder por 5+ sofre 8d8 corte.", "rolls": ["8d8"]}
        ],
        "atributos": {"forca": 12, "destreza": 5, "constituicao": 3, "inteligencia": 0, "sabedoria": 3, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 27}
    },
    {
        "nome": "Ezzayn: Batalhão Burodron",
        "nd": "18", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 15, "percepcao": 18, "sentidos": ["visão no escuro"],
        "defesa": 46, "fortitude": 27, "reflexos": 25, "vontade": 16,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["bando"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 650, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Garra (bandos)", "modalidade": "corpo a corpo", "bonus_ataque": 54, "dano": "4d8+34", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "+5 em testes de ataque e rolagens de dano com garras"}],
        "habilidades": [
            {"nome": "Emboscada Subterrânea", "tipo_acao": "completa", "descricao": "Escava um túnel até uma criatura em alcance curto, abre um fosso e tenta agarrá-la (+54). Se vencer, puxa 3m para baixo, 4d8+23 corte e agarrada. Atletismo CD 44 para sair.", "rolls": ["4d8+23"]},
            {"nome": "Enxame", "tipo_acao": "automática", "descricao": "14d8 corte.", "rolls": ["14d8"]},
            {"nome": "Distorção Temporal", "tipo_acao": "passiva", "descricao": "Ação padrão ou de movimento adicional por turno.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "4d6 PM (Von CD 44 evita).", "rolls": ["4d6"]}
        ],
        "atributos": {"forca": 12, "destreza": 5, "constituicao": 3, "inteligencia": 0, "sabedoria": 3, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 27}
    },
    {
        "nome": "Ezzayn: Cavalaria Hurobakk",
        "nd": "18", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 15, "percepcao": 18, "sentidos": ["visão no escuro"],
        "defesa": 46, "fortitude": 27, "reflexos": 25, "vontade": 16,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["bando"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 750, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [{"nome": "Garra (bandos)", "modalidade": "corpo a corpo", "bonus_ataque": 49, "dano": "4d8+29", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "bônus extra de PV"}],
        "habilidades": [
            {"nome": "Carga Terrível", "tipo_acao": "padrão", "descricao": "Quadrado de 6m à frente: 4d10+19 impacto e caídas (Fort CD 44 reduz e evita). Se falhar por 5+, avaria armadura ou +2d8.", "rolls": ["4d10+19", "2d8"]},
            {"nome": "Enxame", "tipo_acao": "automática", "descricao": "14d8 corte.", "rolls": ["14d8"]},
            {"nome": "Distorção Temporal", "tipo_acao": "passiva", "descricao": "Ação padrão ou de movimento adicional por turno.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "4d6 PM (Von CD 44 evita).", "rolls": ["4d6"]}
        ],
        "atributos": {"forca": 12, "destreza": 5, "constituicao": 3, "inteligencia": 0, "sabedoria": 3, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 27}
    },
    {
        "nome": "Ezzayn: Esquadrão Veridak",
        "nd": "18", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 20, "percepcao": 23, "sentidos": ["visão no escuro"],
        "defesa": 46, "fortitude": 27, "reflexos": 30, "vontade": 16,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["bando"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 650, "pontos_de_mana": None, "deslocamento": "9m (6q), voo 18m (12q)",
        "ataques": [{"nome": "Garra (bandos)", "modalidade": "corpo a corpo", "bonus_ataque": 54, "dano": "4d8+34", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "+5 Iniciativa e Reflexos, deslocamento de voo 18m"}],
        "habilidades": [
            {"nome": "Ataque Rasante", "tipo_acao": "padrão", "descricao": "Quadrado de 6m à frente: 4d6+31 corte (Ref CD 44 reduz). Quem falhar faz teste de agarrar CD 44 ou é erguido e largado de 12m de altura.", "rolls": ["4d6+31"]},
            {"nome": "Enxame", "tipo_acao": "automática", "descricao": "14d8 corte.", "rolls": ["14d8"]},
            {"nome": "Distorção Temporal", "tipo_acao": "passiva", "descricao": "Ação padrão ou de movimento adicional por turno.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "4d6 PM (Von CD 44 evita).", "rolls": ["4d6"]}
        ],
        "atributos": {"forca": 12, "destreza": 5, "constituicao": 3, "inteligencia": 0, "sabedoria": 3, "carisma": -3},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 27}
    },
    {
        "nome": "Gatzvalith, Lorde da Tormenta",
        "nd": "S+", "tipo": "Monstro", "subtipo": "lekael", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 28, "percepcao": 39, "sentidos": ["percepção perfeita"],
        "defesa": 69, "fortitude": 34, "reflexos": 36, "vontade": 24,
        "defesas_especiais": {"reducao_dano": ["25"], "imunidades": ["medo", "maior que a morte"], "resistencias": ["magia +10"], "vulnerabilidades": [], "cura_acelerada": "50"},
        "pontos_de_vida": 3700, "pontos_de_mana": None, "deslocamento": "15m (10q), voo 36m (24q)",
        "ataques": [{"nome": "Rompedor da Realidade", "modalidade": "corpo a corpo", "bonus_ataque": 64, "dano": "4d12+31", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 3, "pericia": "Luta", "descricao": "x4, +2d8 contra não lefeu"}],
        "habilidades": [
            {"nome": "Carapaça Suprema", "tipo_acao": "passiva", "descricao": "Sofre metade do dano de fontes mundanas, exceto aço-rubi.", "rolls": []},
            {"nome": "Estrategista Perfeito", "tipo_acao": "passiva", "descricao": "Rola dois dados e usa o melhor em ataques; lefeu em alcance longo também recebem.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d20 PM (Von CD 55 evita). Pode afetar quem já foi afetado no dia.", "rolls": ["2d20"]},
            {"nome": "Raio da Anticriação", "tipo_acao": "padrão", "descricao": "18d12 essência em alcance médio (Fort CD 55 reduz à metade). Vítima a 0 PV morre, sem ressurreição.", "rolls": ["18d12"]},
            {"nome": "Reescrever a Realidade", "tipo_acao": "completa", "descricao": "Esfera de 15m: dissipa magias, encerra habilidades mundanas, inimigos alquebrados por 1d4 rodadas.", "rolls": ["1d4"]},
            {"nome": "Sedução", "tipo_acao": "movimento", "descricao": "Alvo a 1km: perde 1d10 PM, pasmo, vulnerável (Von CD 55 evita). Falhas acumulam até transformar em lefeu.", "rolls": ["1d10"]},
            {"nome": "Varrer", "tipo_acao": "livre", "descricao": "1x/rodada: ao reduzir alvo a 0 PV, ataque adicional contra outra criatura no alcance.", "rolls": []}
        ],
        "atributos": {"forca": 18, "destreza": 12, "constituicao": 19, "inteligencia": 15, "sabedoria": 8, "carisma": 14},
        "pericias": [{"nome": "Conhecimento", "bonus": 36}, {"nome": "Diplomacia", "bonus": 35}, {"nome": "Enganação", "bonus": 35}, {"nome": "Guerra", "bonus": 41}, {"nome": "Intimidação", "bonus": 40}, {"nome": "Intuição", "bonus": 34}, {"nome": "Misticismo", "bonus": 31}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 29}
    }
]

print(f"Iniciando importação de {len(ameacas_lote1)} monstros...")
sucessos = 0
for ameaca in ameacas_lote1:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        sucessos += 1
        print(f"✅ {ameaca['nome']} importado (ID: {r.json()['_id']})")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")

print(f"\nImportação concluída: {sucessos}/{len(ameacas_lote1)} monstros.")
