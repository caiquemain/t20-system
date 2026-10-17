import requests

API_URL = "http://localhost:8000/ameacas/"

ameacas_lote4 = [
    {
        "nome": "Acólito da Agonia",
        "nd": "5", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 8, "percepcao": 8, "sentidos": [],
        "defesa": 20, "fortitude": 5, "reflexos": 8, "vontade": 13,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["efeitos mentais", "medo"], "resistencias": ["magia divina +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 28, "pontos_de_mana": 28, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Adaga", "modalidade": "corpo a corpo", "bonus_ataque": 16, "dano": "1d4+7", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Júbilo na Dor", "tipo_acao": "passiva", "descricao": "Ao causar ou sofrer dano, recebe RD 2 (cumulativo até 10) e recupera 1d4 PM. Reseta se passar 1 rodada sem dano.", "rolls": ["1d4"]},
            {"nome": "Magias (clérigo 5º)", "tipo_acao": "passiva", "descricao": "CD 17. Arma Espiritual, Infligir Ferimentos, Perdição.", "rolls": []}
        ],
        "atributos": {"forca": 1, "destreza": 3, "constituicao": 2, "inteligencia": -1, "sabedoria": 3, "carisma": -1},
        "pericias": [{"nome": "Intimidação", "bonus": 7}, {"nome": "Religião", "bonus": 6}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 52}
    },
    {
        "nome": "Sacerdote da Agonia",
        "nd": "9", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 15, "percepcao": 19, "sentidos": ["não pode ser flanqueado"],
        "defesa": 32, "fortitude": 9, "reflexos": 15, "vontade": 21,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["efeitos mentais", "medo"], "resistencias": ["magia divina +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 192, "pontos_de_mana": 61, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Adaga da Tormenta", "modalidade": "corpo a corpo", "bonus_ataque": 22, "dano": "1d4+16", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques, +1d8 de trevas"}
        ],
        "habilidades": [
            {"nome": "Apetite por Destruição", "tipo_acao": "completa", "custo_pm": 10, "descricao": "Esfera de 6m ao redor: 6d10 trevas e ganha PV temporários iguais ao dano total (Fort CD 32 reduz à metade).", "rolls": ["6d10"]},
            {"nome": "Júbilo na Dor", "tipo_acao": "passiva", "descricao": "Ao causar ou sofrer dano, recebe RD 2 (cumulativo até 20) e recupera 2d4 PM. Reseta se passar 1 rodada sem dano.", "rolls": ["2d4"]},
            {"nome": "Magias (clérigo 9º)", "tipo_acao": "passiva", "descricao": "CD 32. Arma Espiritual, Enxame Rubro, Infligir Ferimentos, Miasma Mefítico, Perdição.", "rolls": []}
        ],
        "atributos": {"forca": 1, "destreza": 3, "constituicao": 2, "inteligencia": -1, "sabedoria": 5, "carisma": -1},
        "pericias": [{"nome": "Intimidação", "bonus": 11}, {"nome": "Religião", "bonus": 15}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 52}
    },
    {
        "nome": "Aspecto de Aharadak",
        "nd": "10", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 10, "percepcao": 25, "sentidos": ["percepção às cegas"],
        "defesa": 38, "fortitude": 22, "reflexos": 10, "vontade": 20,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 472, "pontos_de_mana": None, "deslocamento": "9m (6q), voo 9m (6q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 30, "dano": "4d8+22", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 30, "dano": "3d8+22", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Mordida (teste +32).", "rolls": []},
            {"nome": "Cuspir Enxame", "tipo_acao": "completa", "descricao": "Enxame rubro Grande em alcance curto. 4d12 ácido a quem estiver no espaço.", "rolls": ["4d12"]},
            {"nome": "Engolir", "tipo_acao": "padrão", "descricao": "Criatura engolida sofre 4d6+11 impacto e 4d6+11 ácido no início do turno. Escapar causando 25 de dano (Def 15).", "rolls": ["4d6+11", "4d6+11"]},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d12 PM (Von CD 30 evita).", "rolls": ["2d12"]},
            {"nome": "Sangue Ácido", "tipo_acao": "passiva", "descricao": "Quando sofre dano por ataque corpo a corpo, o atacante sofre 10 de ácido.", "rolls": []}
        ],
        "atributos": {"forca": 10, "destreza": 1, "constituicao": 7, "inteligencia": 2, "sabedoria": 5, "carisma": -4},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 54}
    },
    {
        "nome": "Fanático Lefou",
        "nd": "5", "tipo": "Monstro", "subtipo": "lefou", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 5, "percepcao": 4, "sentidos": [],
        "defesa": 23, "fortitude": 16, "reflexos": 11, "vontade": 6,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": ["efeitos mentais +3", "lefeu e Tormenta +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 55, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 22, "dano": "2d6+10", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 22, "dano": "1d6+10", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Frenesi Insano", "tipo_acao": "passiva", "descricao": "Ao causar ou sofrer dano, ganha +2 cumulativo em ataques e dano até o fim da cena.", "rolls": []},
            {"nome": "Mente Aberrante", "tipo_acao": "reação", "descricao": "Ao resistir com Vontade, causa 3d6 psíquico no gerador.", "rolls": ["3d6"]},
            {"nome": "Sangue Ácido", "tipo_acao": "passiva", "descricao": "Quando sofre dano por ataque corpo a corpo, o atacante sofre 5 de ácido.", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 1, "constituicao": 2, "inteligencia": -1, "sabedoria": 0, "carisma": -2},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 55}
    },
    {
        "nome": "Líder Fanático Lefou",
        "nd": "7", "tipo": "Monstro", "subtipo": "lefou", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 9, "percepcao": 8, "sentidos": ["visão no escuro"],
        "defesa": 33, "fortitude": 20, "reflexos": 15, "vontade": 9,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["acertos críticos"], "resistencias": ["lefeu, Tormenta e mentais +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 90, "pontos_de_mana": None, "deslocamento": "9m (6q), voo 21m (14q)",
        "ataques": [
            {"nome": "Tacape", "modalidade": "corpo a corpo", "bonus_ataque": 27, "dano": "3d10+20", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 27, "dano": "1d4+10", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Patas Insetoides", "modalidade": "corpo a corpo", "bonus_ataque": 27, "dano": "1d4+10", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas patas"}
        ],
        "habilidades": [
            {"nome": "Frenesi Insano", "tipo_acao": "passiva", "descricao": "Ao causar ou sofrer dano, ganha +2 cumulativo em ataques e dano até o fim da cena.", "rolls": []},
            {"nome": "Mente Aberrante", "tipo_acao": "reação", "descricao": "Ao resistir com Vontade, causa 5d6 psíquico no gerador.", "rolls": ["5d6"]},
            {"nome": "Sangue Ácido", "tipo_acao": "passiva", "descricao": "Quando sofre dano por ataque corpo a corpo, o atacante sofre 9 de ácido.", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 1, "constituicao": 2, "inteligencia": -1, "sabedoria": 0, "carisma": -2},
        "pericias": [{"nome": "Intimidação", "bonus": 11}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 55}
    },
    {
        "nome": "Reishid",
        "nd": "10", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 17, "percepcao": 19, "sentidos": ["visão no escuro"],
        "defesa": 37, "fortitude": 19, "reflexos": 21, "vontade": 10,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 295, "pontos_de_mana": None, "deslocamento": "9m (6q), escalada 9m (6q), voo 15m (10q)",
        "ataques": [
            {"nome": "Adaga da Tormenta", "modalidade": "corpo a corpo", "bonus_ataque": 30, "dano": "1d4+18", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "+1d8 trevas"},
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 30, "dano": "1d6+18", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 30, "dano": "1d6+18", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "mais veneno"}
        ],
        "habilidades": [
            {"nome": "Ataque em Movimento", "tipo_acao": "passiva", "descricao": "Pode mover antes e depois de agredir (até seu deslocamento total).", "rolls": []},
            {"nome": "Ataque Reflexo", "tipo_acao": "reação", "descricao": "1x/rodada: ataque contra alvo desprevenido ou que saia do alcance.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d6 PM (Von CD 26 evita).", "rolls": ["2d6"]},
            {"nome": "Sombra Rubra", "tipo_acao": "passiva", "descricao": "Rola dois dados e usa o melhor em Iniciativa e Furtividade.", "rolls": []},
            {"nome": "Veneno", "tipo_acao": "passiva", "descricao": "Paralisado por 1d6 horas (Fort CD 26 reduz para lento por 1d6 rodadas).", "rolls": ["1d6"]}
        ],
        "atributos": {"forca": 4, "destreza": 7, "constituicao": 4, "inteligencia": 4, "sabedoria": 4, "carisma": 1},
        "pericias": [{"nome": "Furtividade", "bonus": 20}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 56}
    },
    {
        "nome": "Reishid Líder de Culto",
        "nd": "13", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 19, "percepcao": 23, "sentidos": ["visão no escuro"],
        "defesa": 47, "fortitude": 20, "reflexos": 27, "vontade": 13,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 483, "pontos_de_mana": 66, "deslocamento": "9m (6q), escalada 9m (6q), voo 15m (10q)",
        "ataques": [
            {"nome": "Adaga da Tormenta", "modalidade": "corpo a corpo", "bonus_ataque": 40, "dano": "1d4+21", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "+1d8 trevas"},
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 40, "dano": "2d6+21", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 40, "dano": "2d6+21", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "mais veneno"}
        ],
        "habilidades": [
            {"nome": "Ataque em Movimento", "tipo_acao": "passiva", "descricao": "Pode mover antes e depois de agredir.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "3d6 PM (Von CD 35 evita).", "rolls": ["3d6"]},
            {"nome": "Magia Acelerada", "tipo_acao": "livre", "custo_pm": 4, "descricao": "1x/rodada: muda execução de magia para livre.", "rolls": []},
            {"nome": "Sombra Rubra", "tipo_acao": "passiva", "descricao": "Rola dois dados e usa o melhor em Iniciativa e Furtividade.", "rolls": []},
            {"nome": "Veneno", "tipo_acao": "passiva", "descricao": "Paralisado por 1d6 horas (Fort CD 35 reduz para lento).", "rolls": ["1d6"]},
            {"nome": "Magias (clérigo 12º)", "tipo_acao": "passiva", "descricao": "CD 35. Anular a Luz, Comando, Marca da Obediência.", "rolls": []}
        ],
        "atributos": {"forca": 4, "destreza": 7, "constituicao": 5, "inteligencia": 4, "sabedoria": 6, "carisma": 1},
        "pericias": [{"nome": "Furtividade", "bonus": 27}, {"nome": "Intimidação", "bonus": 11}, {"nome": "Religião", "bonus": 21}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 56}
    },
    {
        "nome": "Senhor do Gigante Rubro (Forma Inicial)",
        "nd": "9", "tipo": "Monstro", "subtipo": None, "tamanho": "Grande", "papel": "solo",
        "iniciativa": 13, "percepcao": 15, "sentidos": ["percepção às cegas", "não pode ser flanqueado"],
        "defesa": 34, "fortitude": 21, "reflexos": 15, "vontade": 9,
        "defesas_especiais": {"reducao_dano": ["ácido, eletricidade, fogo, frio, luz e trevas 10"], "imunidades": ["acertos críticos", "cansaço", "metabolismo", "paralisia", "veneno"], "resistencias": ["magia +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 340, "pontos_de_mana": None, "deslocamento": "12m (8q), escalada 9m (6q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 28, "dano": "1d8+11", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 3, "pericia": "Luta", "descricao": "quatro garras"}
        ],
        "habilidades": [
            {"nome": "Carapaça Espinhosa", "tipo_acao": "passiva", "descricao": "Causa 11 de perfuração ao agarrar ou ser agarrado e no início do turno agarrado.", "rolls": []},
            {"nome": "Desembarcar", "tipo_acao": "completa", "descricao": "O piloto pode sair do simbionte (fica fatigado a cada hora até morrer).", "rolls": []}
        ],
        "atributos": {"forca": 11, "destreza": 3, "constituicao": 9, "inteligencia": -1, "sabedoria": 2, "carisma": -2},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 58}
    },
    {
        "nome": "Senhor do Gigante Rubro (Forma Final)",
        "nd": "14", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 20, "percepcao": 21, "sentidos": ["percepção às cegas", "não pode ser flanqueado"],
        "defesa": 55, "fortitude": 30, "reflexos": 26, "vontade": 16,
        "defesas_especiais": {"reducao_dano": ["15"], "imunidades": ["acertos críticos", "cansaço", "metabolismo", "paralisia", "veneno"], "resistencias": ["magia +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 850, "pontos_de_mana": None, "deslocamento": "12m (8q), escalada 9m (6q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 43, "dano": "1d12+18", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 3, "pericia": "Luta", "descricao": "quatro garras, +1d6 matéria vermelha, sangramento"},
            {"nome": "Tentáculo", "modalidade": "corpo a corpo", "bonus_ataque": 43, "dano": "1d12+18", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois tentáculos, +1d6 matéria vermelha, deixa fraco"}
        ],
        "habilidades": [
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Tentáculo (teste +45).", "rolls": []},
            {"nome": "Carapaça Espinhosa", "tipo_acao": "passiva", "descricao": "Causa 14 de perfuração ao agarrar/ser agarrado e no início do turno.", "rolls": []},
            {"nome": "Dilacerar", "tipo_acao": "passiva", "descricao": "Para cada dois ataques de garra que acertar no mesmo turno, causa +6d8+18.", "rolls": ["6d8+18"]},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d12 PM (Von CD 42 evita).", "rolls": ["2d12"]},
            {"nome": "Morte dos Céus", "tipo_acao": "movimento", "descricao": "Salta para espaço em alcance médio. Se aterrissar adjacente, ganha +2 no ataque e +2d8 de dano.", "rolls": ["2d8"]},
            {"nome": "Teia Corrosiva", "tipo_acao": "movimento", "descricao": "Alvo em alcance curto sofre 8d6 ácido e fica imóvel (Ref CD 42 reduz e evita).", "rolls": ["8d6"]},
            {"nome": "Varrer", "tipo_acao": "livre", "descricao": "1x/rodada: ao reduzir a 0 PV, ataque adicional contra outra criatura.", "rolls": []}
        ],
        "atributos": {"forca": 14, "destreza": 4, "constituicao": 11, "inteligencia": -2, "sabedoria": 2, "carisma": -4},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 58}
    },
    {
        "nome": "Zyrrinaz",
        "nd": "5", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 10, "percepcao": 13, "sentidos": ["visão no escuro"],
        "defesa": 24, "fortitude": 11, "reflexos": 19, "vontade": 7,
        "defesas_especiais": {"reducao_dano": ["5"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 41, "pontos_de_mana": None, "deslocamento": "12m (8q), escalada 12m (8q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 19, "dano": "2d6+13", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Arco longo", "modalidade": "à distância", "bonus_ataque": 23, "dano": "1d12+19", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 3, "pericia": "Pontaria", "descricao": "+1d6 matéria vermelha"}
        ],
        "habilidades": [
            {"nome": "Flechas da Anticriação", "tipo_acao": "passiva", "descricao": "Ignora cobertura, camuflagem, RD e evasões. Rola dois dados e usa o melhor no ataque de arco.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d4 PM (Von CD 20 evita).", "rolls": ["2d4"]}
        ],
        "atributos": {"forca": 2, "destreza": 6, "constituicao": 2, "inteligencia": -1, "sabedoria": 4, "carisma": -3},
        "pericias": [{"nome": "Acrobacia", "bonus": 10}, {"nome": "Furtividade", "bonus": 10}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 59}
    },
    {
        "nome": "Avatar de Aharadak",
        "nd": "S", "tipo": "Monstro", "subtipo": "lefeu", "tamanho": "Colossal", "papel": "solo",
        "iniciativa": 18, "percepcao": 30, "sentidos": ["percepção às cegas (longo)"],
        "defesa": 70, "fortitude": 36, "reflexos": 31, "vontade": 31,
        "defesas_especiais": {"reducao_dano": ["20"], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 2804, "pontos_de_mana": None, "deslocamento": "voo 18m (12q)",
        "ataques": [
            {"nome": "Tentáculos", "modalidade": "corpo a corpo", "bonus_ataque": 58, "dano": "4d12+47", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "quatro tentáculos"},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 58, "dano": "6d12+47", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Tentáculo (teste +68). Mantém até 4 criaturas Enormes ou menores.", "rolls": []},
            {"nome": "Centelha Divina", "tipo_acao": "passiva", "descricao": "Lança qualquer magia divina como clérigo de 20º nível sem gastar PM (CD 52).", "rolls": []},
            {"nome": "Devorar a Existência", "tipo_acao": "passiva", "descricao": "Criatura atingida perde 1d4 PM. Se não tiver PM, fica fascinada.", "rolls": ["1d4"]},
            {"nome": "Engolir", "tipo_acao": "padrão", "descricao": "Criatura engolida faz Von CD 52. Se falhar, perde todos os PM ou é transportada para o Reino de Aharadak.", "rolls": []},
            {"nome": "Insanidade da Tormenta", "tipo_acao": "passiva", "descricao": "2d20 PM (Von CD 52 evita). Afeta até quem já foi afetado no dia.", "rolls": ["2d20"]},
            {"nome": "Presença da Tormenta", "tipo_acao": "passiva", "descricao": "Aura de 30m. Criaturas ficam esmorecidas (CD 25 +2/turno). Custo de PM +2. Efeitos aleatórios de 1d6 a cada turno (Definhamento, Tempestade, Ácido, Labaredas, Pesadelos, Magia Caótica).", "rolls": ["1d6"]}
        ],
        "atributos": {"forca": 20, "destreza": -2, "constituicao": 12, "inteligencia": 4, "sabedoria": 10, "carisma": -1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 62}
    }
]

print(f"Iniciando importação de {len(ameacas_lote4)} monstros (Lote 4)...")
sucessos = 0
for ameaca in ameacas_lote4:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        sucessos += 1
        print(f"✅ {ameaca['nome']} importado.")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")

print(f"\nImportação concluída: {sucessos}/{len(ameacas_lote4)} monstros.")
