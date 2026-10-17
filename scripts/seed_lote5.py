import requests

API_URL = "http://localhost:8000/ameacas/"

ameacas_lote5 = [
    {
        "nome": "Dragão Filhote do Bosque",
        "nd": "4", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 8, "percepcao": 6, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 21, "fortitude": 14, "reflexos": 3, "vontade": 10,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["ácido"], "resistencias": ["magia +1"], "vulnerabilidades": ["eletricidade"], "cura_acelerada": None},
        "pontos_de_vida": 120, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 18m (12q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 14, "dano": "2d6+4", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 14, "dano": "1d6+4", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Bote", "tipo_acao": "completa", "descricao": "Investida com mordida e duas garras contra o mesmo alvo (+2 de investida).", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Esfera de 3m em alcance curto: 2d12 ácido e vulnerável por 1d4 rodadas (Ref CD 18 reduz à metade e evita a condição).", "rolls": ["2d12", "1d4"]}
        ],
        "atributos": {"forca": 3, "destreza": 3, "constituicao": 2, "inteligencia": -1, "sabedoria": 1, "carisma": 0},
        "pericias": [{"nome": "Furtividade", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 64}
    },
    {
        "nome": "Dragão Filhote dos Rios",
        "nd": "4", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 9, "percepcao": 6, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 22, "fortitude": 12, "reflexos": 6, "vontade": 10,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["eletricidade"], "resistencias": ["magia +1"], "vulnerabilidades": ["ácido"], "cura_acelerada": None},
        "pontos_de_vida": 120, "pontos_de_mana": None, "deslocamento": "12m (8q), natação 18m (12q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 13, "dano": "2d6+4", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 13, "dano": "1d6+4", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Sopro", "tipo_acao": "completa", "recarga": "movimento", "descricao": "Cone de 6m: 2d12 eletricidade e ofuscado por 1d4 rodadas (Ref CD 18 reduz à metade e evita a condição).", "rolls": ["2d12", "1d4"]}
        ],
        "atributos": {"forca": 3, "destreza": 4, "constituicao": 3, "inteligencia": 0, "sabedoria": 0, "carisma": 0},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 64}
    },
    {
        "nome": "Ninhada de Dragões Filhotes",
        "nd": "7", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 9, "percepcao": 7, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 25, "fortitude": 14, "reflexos": 8, "vontade": 12,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["fogo"], "resistencias": ["magia +1", "bando"], "vulnerabilidades": ["frio"], "cura_acelerada": None},
        "pontos_de_vida": 240, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 18m (12q)",
        "ataques": [
            {"nome": "Mordida (Bando)", "modalidade": "corpo a corpo", "bonus_ataque": 18, "dano": "4d6+8", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras (Bando)", "modalidade": "corpo a corpo", "bonus_ataque": 18, "dano": "2d6+8", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Avalanche de Escamas", "tipo_acao": "passiva", "descricao": "Se acertar as duas garras em criatura Grande ou menor, ela cai e fica agarrada.", "rolls": []},
            {"nome": "Sopro Duplo", "tipo_acao": "completa", "recarga": "movimento", "descricao": "Dois cones de 6m em direções diferentes: 4d12 fogo e em chamas (Ref CD 21 reduz à metade e evita).", "rolls": ["4d12"]}
        ],
        "atributos": {"forca": 4, "destreza": 3, "constituicao": 3, "inteligencia": 0, "sabedoria": 0, "carisma": 0},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 65}
    },
    {
        "nome": "Dragão Jovem da Proteção",
        "nd": "7", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 11, "percepcao": 11, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 32, "fortitude": 20, "reflexos": 9, "vontade": 12,
        "defesas_especiais": {"reducao_dano": ["5"], "imunidades": ["eletricidade"], "resistencias": ["magia +2"], "vulnerabilidades": ["ácido"], "cura_acelerada": None},
        "pontos_de_vida": 320, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 18m (12q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 25, "dano": "2d6+14", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 25, "dano": "1d8+14", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Asas Guardiãs", "tipo_acao": "movimento", "descricao": "Aliados adjacentes ganham RD 5 até o fim da cena.", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Linha de 12m: 6d12 eletricidade e ofuscado (Ref CD 25 reduz e evita). Cada '12' no dano rola um dado extra.", "rolls": ["6d12"]}
        ],
        "atributos": {"forca": 7, "destreza": 2, "constituicao": 6, "inteligencia": 2, "sabedoria": 2, "carisma": 2},
        "pericias": [{"nome": "Diplomacia", "bonus": 11}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 66}
    },
    {
        "nome": "Dragão Jovem do Ocaso",
        "nd": "7", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 11, "percepcao": 12, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 31, "fortitude": 20, "reflexos": 9, "vontade": 15,
        "defesas_especiais": {"reducao_dano": ["5"], "imunidades": ["frio"], "resistencias": ["magia +2"], "vulnerabilidades": ["fogo"], "cura_acelerada": None},
        "pontos_de_vida": 320, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 18m (12q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 24, "dano": "2d6+14", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "Mordida Definhante"},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 24, "dano": "1d8+14", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Mordida Definhante", "tipo_acao": "passiva", "descricao": "Criatura atingida pela mordida fica alquebrada (Von CD 25 evita).", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Cone de 9m: 6d12 frio e lento por 1d4 rodadas (Ref CD 25 reduz e evita).", "rolls": ["6d12", "1d4"]},
            {"nome": "Ver o Fim", "tipo_acao": "passiva", "descricao": "Percebe presença, posição e status de criaturas em alcance médio.", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 3, "constituicao": 5, "inteligencia": 3, "sabedoria": 3, "carisma": 2},
        "pericias": [{"nome": "Intimidação", "bonus": 11}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 66}
    },
    {
        "nome": "Dragão Adulto da Tirania",
        "nd": "11", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 12, "percepcao": 15, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 42, "fortitude": 24, "reflexos": 11, "vontade": 20,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["dano de luz"], "resistencias": ["magia +3"], "vulnerabilidades": ["trevas"], "cura_acelerada": None},
        "pontos_de_vida": 614, "pontos_de_mana": 77, "deslocamento": "12m (8q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 34, "dano": "4d10+25", "tipo_dano": "perfuração", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 34, "dano": "3d10+25", "tipo_dano": "corte", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 32 evita.", "rolls": []},
            {"nome": "Imposição Avassaladora", "tipo_acao": "livre", "descricao": "1x/rodada, ao reduzir inimigo a 0 PV, outros em alcance médio sofrem 4d12 psíquico (Von CD 32 reduz).", "rolls": ["4d12"]},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Linha de 18m: 12d12 luz e cego (Ref CD 32 reduz e evita).", "rolls": ["12d12"]},
            {"nome": "Magias (arcano 11º)", "tipo_acao": "passiva", "descricao": "CD 32. Campo de Força, Desespero Esmagador, Dissipar Magia, Enfeitiçar, Luz, Tempestade Divina.", "rolls": []}
        ],
        "atributos": {"forca": 11, "destreza": 1, "constituicao": 8, "inteligencia": 4, "sabedoria": 4, "carisma": 4},
        "pericias": [{"nome": "Atletismo", "bonus": 32}, {"nome": "Intimidação", "bonus": 15}, {"nome": "Misticismo", "bonus": 15}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 68}
    },
    {
        "nome": "Dragão Adulto dos Segredos",
        "nd": "11", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 14, "percepcao": 17, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 40, "fortitude": 13, "reflexos": 17, "vontade": 25,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["trevas"], "resistencias": ["magia +3"], "vulnerabilidades": ["luz"], "cura_acelerada": None},
        "pontos_de_vida": 522, "pontos_de_mana": 90, "deslocamento": "12m (8q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 33, "dano": "3d12+20", "tipo_dano": "perfuração", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "modalidade": "corpo a corpo", "bonus_ataque": 35, "dano": "2d12+20", "tipo_dano": "corte", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 32 evita.", "rolls": []},
            {"nome": "Enxergar as Farsas", "tipo_acao": "passiva", "descricao": "Sempre sob efeito básico de Visão da Verdade.", "rolls": []},
            {"nome": "Esmiuçar a Alma", "tipo_acao": "passiva", "descricao": "Quando uma criatura fica abalada, vê seus segredos. +2 em testes e passa automático em Intuição contra ela.", "rolls": []},
            {"nome": "Magia Ampliada", "tipo_acao": "livre", "custo_pm": 2, "descricao": "Aumenta alcance de magia em um passo ou dobra área.", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Esfera de 9m em alcance médio: 12d12 trevas e enjoado (Ref CD 38 reduz e evita).", "rolls": ["12d12"]},
            {"nome": "Magias (arcano 11º)", "tipo_acao": "passiva", "descricao": "CD 35. Campo de Força, Compreensão, Criar Ilusão, Desespero Esmagador, Dissipar Magia, Escuridão, Marca da Obediência.", "rolls": []}
        ],
        "atributos": {"forca": 7, "destreza": 1, "constituicao": 6, "inteligencia": 8, "sabedoria": 6, "carisma": 6},
        "pericias": [{"nome": "Conhecimento", "bonus": 19}, {"nome": "Enganação", "bonus": 17}, {"nome": "Intimidação", "bonus": 17}, {"nome": "Intuição", "bonus": 25}, {"nome": "Misticismo", "bonus": 19}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 69}
    },
    {
        "nome": "Dragão Venerável da Equidade",
        "nd": "15", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 16, "percepcao": 22, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 52, "fortitude": 28, "reflexos": 15, "vontade": 22,
        "defesas_especiais": {"reducao_dano": ["15"], "imunidades": ["dano de luz"], "resistencias": ["magia +4"], "vulnerabilidades": ["trevas"], "cura_acelerada": None},
        "pontos_de_vida": 800, "pontos_de_mana": 97, "deslocamento": "12m (8q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "tipo": "corpo a corpo", "bonus_ataque": 44, "dano": "4d12+40", "tipo_dano": "perfuração", "margem_critico": 17, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "tipo": "corpo a corpo", "bonus_ataque": 44, "dano": "3d12+40", "tipo_dano": "corte", "margem_critico": 17, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 40 evita.", "rolls": []},
            {"nome": "Equalizar", "tipo_acao": "reação", "custo_pm": 3, "descricao": "Ao ver um aliado ou inimigo fazer um teste, pode refazê-lo (Von CD 32 evita).", "rolls": []},
            {"nome": "Magia Acelerada", "tipo_acao": "livre", "custo_pm": 4, "descricao": "1x/rodada: muda execução de magia para livre.", "rolls": []},
            {"nome": "Restabelecer a Igualdade", "tipo_acao": "reação", "descricao": "1x/rodada: ao sofrer ataque ou magia, pode fazer o atacante sofrer a mesma coisa.", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Cone de 15m: 16d12 luz e cego (Ref CD 40 reduz e evita).", "rolls": ["16d12"]},
            {"nome": "Magias (arcano 15º)", "tipo_acao": "passiva", "descricao": "CD 40. Círculo da Justiça, Curar Ferimentos, Desespero Esmagador, Dissipar Magia, Missão Divina, Selo de Mana, Velocidade.", "rolls": []}
        ],
        "atributos": {"forca": 13, "destreza": 1, "constituicao": 10, "inteligencia": 6, "sabedoria": 6, "carisma": 6},
        "pericias": [{"nome": "Enganação", "bonus": 22}, {"nome": "Intimidação", "bonus": 22}, {"nome": "Intuição", "bonus": 22}, {"nome": "Misticismo", "bonus": 22}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 71}
    },
    {
        "nome": "Dragão Venerável dos Recifes",
        "nd": "15", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 19, "percepcao": 20, "sentidos": ["percepção às cegas", "visão no escuro"],
        "defesa": 48, "fortitude": 28, "reflexos": 20, "vontade": 17,
        "defesas_especiais": {"reducao_dano": ["15"], "imunidades": ["eletricidade"], "resistencias": ["magia +4"], "vulnerabilidades": ["ácido"], "cura_acelerada": None},
        "pontos_de_vida": 790, "pontos_de_mana": 97, "deslocamento": "12m (8q), natação 24m (16q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "tipo": "corpo a corpo", "bonus_ataque": 44, "dano": "4d12+30", "tipo_dano": "perfuração", "margem_critico": 17, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "tipo": "corpo a corpo", "bonus_ataque": 44, "dano": "2d12+30", "tipo_dano": "corte", "margem_critico": 17, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"},
            {"nome": "Cauda", "tipo": "corpo a corpo", "bonus_ataque": 44, "dano": "2d12+30", "tipo_dano": "impacto", "margem_critico": 17, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 40 evita.", "rolls": []},
            {"nome": "Fluxo de Mana", "tipo_acao": "passiva", "descricao": "Pode manter dois efeitos sustentados com apenas uma ação livre.", "rolls": []},
            {"nome": "Magia Acelerada", "tipo_acao": "livre", "custo_pm": 4, "descricao": "1x/rodada: muda execução de magia para livre.", "rolls": []},
            {"nome": "Profunda Paixão", "tipo_acao": "passiva", "descricao": "Rola dois dados e usa o melhor em testes ligados a Carisma.", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Linha de 18m: 16d12 eletricidade e ofuscado (Ref CD 40 reduz e evita). Cada '12' rola um dado extra.", "rolls": ["16d12"]},
            {"nome": "Magias (arcano 15º)", "tipo_acao": "passiva", "descricao": "CD 40. Campo de Força, Controlar o Clima, Curar Ferimentos, Enfeitiçar, Globo de Invulnerabilidade, Suporte Ambiental, Velocidade.", "rolls": []}
        ],
        "atributos": {"forca": 12, "destreza": 4, "constituicao": 10, "inteligencia": 4, "sabedoria": 4, "carisma": 8},
        "pericias": [{"nome": "Atletismo", "bonus": 25}, {"nome": "Diplomacia", "bonus": 22}, {"nome": "Enganação", "bonus": 22}, {"nome": "Intimidação", "bonus": 22}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 71}
    },
    {
        "nome": "Dragão Feral",
        "nd": "12", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 13, "percepcao": 12, "sentidos": ["faro", "percepção às cegas", "visão no escuro"],
        "defesa": 38, "fortitude": 22, "reflexos": 10, "vontade": 14,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["frio"], "resistencias": ["magia +3"], "vulnerabilidades": ["fogo"], "cura_acelerada": None},
        "pontos_de_vida": 495, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "tipo": "corpo a corpo", "bonus_ataque": 30, "dano": "3d12+14", "tipo_dano": "perfuração", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "tipo": "corpo a corpo", "bonus_ataque": 30, "dano": "2d10+14", "tipo_dano": "corte", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Amadurecimento Primitivo", "tipo_acao": "passiva", "descricao": "Conta como adulto, mas não possui Magia Dracônica e Metamorfose Dracônica.", "rolls": []},
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 30 evita.", "rolls": []},
            {"nome": "Dilacerar", "tipo_acao": "passiva", "descricao": "Se acertar as duas garras na mesma criatura no mesmo turno, causa +3d10+14.", "rolls": ["3d10+14"]},
            {"nome": "Investida Imparável", "tipo_acao": "completa", "recarga": "movimento", "descricao": "Move até o dobro, passando por criaturas Grandes ou menores: 7d8+14 corte, empurradas e caídas (Ref CD 30 reduz e evita).", "rolls": ["7d8+14"]},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Cone de 12m: 12d12 frio e lento (Ref CD 30 reduz e evita).", "rolls": ["12d12"]},
            {"nome": "Varrer", "tipo_acao": "livre", "descricao": "1x/rodada: ao reduzir a 0 PV, ataque adicional em outra criatura.", "rolls": []}
        ],
        "atributos": {"forca": 13, "destreza": 3, "constituicao": 10, "inteligencia": -3, "sabedoria": 2, "carisma": -1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 72}
    },
    {
        "nome": "Dragão Bicéfalo",
        "nd": "12", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Enorme", "papel": "solo",
        "iniciativa": 13, "percepcao": 17, "sentidos": ["percepção às cegas", "não pode ser flanqueado", "visão no escuro"],
        "defesa": 44, "fortitude": 26, "reflexos": 12, "vontade": 20,
        "defesas_especiais": {"reducao_dano": ["10"], "imunidades": ["ácido", "eletricidade"], "resistencias": ["magia +3"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 650, "pontos_de_mana": None, "deslocamento": "12m (8q), voo 24m (16q)",
        "ataques": [
            {"nome": "Mordida", "tipo": "corpo a corpo", "bonus_ataque": 36, "dano": "4d10+26", "tipo_dano": "perfuração", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garra", "tipo": "corpo a corpo", "bonus_ataque": 36, "dano": "3d10+26", "tipo_dano": "corte", "margem_critico": 18, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 33 evita.", "rolls": []},
            {"nome": "Duas Mentes", "tipo_acao": "passiva", "descricao": "Ação padrão adicional por rodada. Rola dois dados e usa o melhor em Vontade.", "rolls": []},
            {"nome": "Sopro (Esfera)", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Esfera de 9m em alcance médio: 12d12 eletricidade e ofuscado por 1d4 rodadas (Ref CD 33 reduz e evita).", "rolls": ["12d12", "1d4"]},
            {"nome": "Sopro (Nuvem)", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Nuvem de ácido de 9m por 2 rodadas. Quem começa o turno na área sofre 12d6 ácido e fica vulnerável por 1d4 rodadas (Ref CD 33 reduz e evita).", "rolls": ["12d6", "1d4"]}
        ],
        "atributos": {"forca": 11, "destreza": 1, "constituicao": 8, "inteligencia": 3, "sabedoria": 5, "carisma": 4},
        "pericias": [{"nome": "Enganação", "bonus": 16}, {"nome": "Intimidação", "bonus": 16}, {"nome": "Misticismo", "bonus": 15}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 72}
    },
    {
        "nome": "Sckhar, Dragão-Rei do Fogo",
        "nd": "S+", "tipo": "Monstro", "subtipo": "dragão", "tamanho": "Colossal", "papel": "solo",
        "iniciativa": 23, "percepcao": 34, "sentidos": ["percepção às cegas (longo)", "visão no escuro"],
        "defesa": 71, "fortitude": 38, "reflexos": 25, "vontade": 33,
        "defesas_especiais": {"reducao_dano": ["20"], "imunidades": ["encantamento", "fogo"], "resistencias": ["magia +5"], "vulnerabilidades": ["frio"], "cura_acelerada": None},
        "pontos_de_vida": 4000, "pontos_de_mana": 287, "deslocamento": "12m (8q), voo 36m (24q)",
        "ataques": [
            {"nome": "Mordida", "tipo": "corpo a corpo", "bonus_ataque": 66, "dano": "10d20+60", "tipo_dano": "perfuração", "margem_critico": 16, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Garras", "tipo": "corpo a corpo", "bonus_ataque": 61, "dano": "10d20+60", "tipo_dano": "corte", "margem_critico": 16, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"}
        ],
        "habilidades": [
            {"nome": "Aqui Está, Aqui Pertence", "tipo_acao": "passiva", "descricao": "Criatura em alcance longo que use teletransporte faz Von CD 55 ou a habilidade falha.", "rolls": []},
            {"nome": "Aura Aterradora", "tipo_acao": "passiva", "descricao": "Vontade CD 55 evita. Quem falhar sofre 8d6 psíquico.", "rolls": ["8d6"]},
            {"nome": "Deus das Chamas", "tipo_acao": "passiva", "descricao": "Magias de fogo sob Magia Ampliada, dados de dano aumentam em 2 passos. Dano de fogo ignora RD e fere imunes a fogo (metade).", "rolls": []},
            {"nome": "Ego", "tipo_acao": "reação", "custo_pm": 5, "descricao": "1x/rodada: passa automaticamente em um teste de perícia (exceto ataque).", "rolls": []},
            {"nome": "Escamas Supremas", "tipo_acao": "passiva", "descricao": "Sofre metade do dano de fontes mundanas.", "rolls": []},
            {"nome": "Fluxo de Mana", "tipo_acao": "passiva", "descricao": "Pode manter dois efeitos sustentados com apenas uma ação livre.", "rolls": []},
            {"nome": "Magia Acelerada", "tipo_acao": "livre", "custo_pm": 4, "descricao": "1x/rodada: muda execução de magia para livre.", "rolls": []},
            {"nome": "Poder Incontestável", "tipo_acao": "passiva", "descricao": "A primeira magia lançada por rodada não pode ser alvo de contramágica.", "rolls": []},
            {"nome": "Sopro", "tipo_acao": "padrão", "recarga": "movimento", "descricao": "Cone de 30m: 30d12 fogo e em chamas (Ref CD 55 reduz e evita). Cada '12' no dano rola um dado extra.", "rolls": ["30d12"]},
            {"nome": "Varrer", "tipo_acao": "livre", "descricao": "1x/rodada: ao reduzir a 0 PV, ataque adicional contra outra criatura.", "rolls": []},
            {"nome": "Magias (arcano 20º)", "tipo_acao": "passiva", "descricao": "CD 55. Aprisionamento, Bola de Fogo, Campo de Força, Chuva de Meteoros, Coluna de Chamas, Controlar Fogo, Dissipar Magia, Globo de Invulnerabilidade, Imobilizar, Muralha Elemental, Segunda Chance, Velocidade.", "rolls": []}
        ],
        "atributos": {"forca": 20, "destreza": 2, "constituicao": 15, "inteligencia": 12, "sabedoria": 12, "carisma": 12},
        "pericias": [{"nome": "Diplomacia", "bonus": 33}, {"nome": "Enganação", "bonus": 33}, {"nome": "Intimidação", "bonus": 33}, {"nome": "Intuição", "bonus": 33}, {"nome": "Misticismo", "bonus": 33}, {"nome": "Nobreza", "bonus": 33}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 77}
    }
]

print(f"Iniciando importação de {len(ameacas_lote5)} monstros (Lote 5)...")
sucessos = 0
for ameaca in ameacas_lote5:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        sucessos += 1
        print(f"✅ {ameaca['nome']} importado.")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")

print(f"\nImportação concluída: {sucessos}/{len(ameacas_lote5)} monstros.")
