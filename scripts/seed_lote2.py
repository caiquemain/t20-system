import requests

API_URL = "http://localhost:8000/ameacas/"

ameacas_lote2 = [
    {
        "nome": "Meio-Orc Bandoleiro",
        "nd": "1/2", "tipo": "Humanoide", "subtipo": "meio-orc", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 5, "percepcao": 1, "sentidos": ["visão no escuro"],
        "defesa": 15, "fortitude": 10, "reflexos": 5, "vontade": 1,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 15, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Espada curta", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d6+13", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "Ataque Furtivo +2d6."},
            {"nome": "Adaga", "modalidade": "à distância", "bonus_ataque": 9, "dano": "1d4+7", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Pontaria", "descricao": "Ataque Furtivo +2d6."}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +2d6 em alvos desprevenidos ou flanqueados.", "rolls": ["2d6"]}
        ],
        "atributos": {"forca": 3, "destreza": 1, "constituicao": 2, "inteligencia": 0, "sabedoria": -1, "carisma": -1},
        "pericias": [{"nome": "Intimidação", "bonus": 7}, {"nome": "Sobrevivência", "bonus": 6}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 31}
    },
    {
        "nome": "Orc Combatente",
        "nd": "1/1", "tipo": "Humanoide", "subtipo": "orc", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 4, "percepcao": 1, "sentidos": ["visão no escuro", "sensibilidade a luz"],
        "defesa": 14, "fortitude": 5, "reflexos": 3, "vontade": 0,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 8, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Maça", "modalidade": "corpo a corpo", "bonus_ataque": 9, "dano": "1d8+7", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [],
        "atributos": {"forca": 4, "destreza": 1, "constituicao": 2, "inteligencia": -1, "sabedoria": -1, "carisma": -1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 33}
    },
    {
        "nome": "Orc Chefe",
        "nd": "3", "tipo": "Humanoide", "subtipo": "orc", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 5, "percepcao": 3, "sentidos": ["visão no escuro", "sensibilidade a luz"],
        "defesa": 19, "fortitude": 13, "reflexos": 7, "vontade": 2,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 66, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Machado de batalha", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d8+12", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 3, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Urro Selvagem", "tipo_acao": "movimento", "descricao": "Recebe +2 em testes de ataque e rolagens de dano corpo a corpo até o fim da cena, mas não pode fazer ações que exijam calma e concentração.", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 2, "constituicao": 4, "inteligencia": 0, "sabedoria": 0, "carisma": 0},
        "pericias": [{"nome": "Intimidação", "bonus": 4}, {"nome": "Sobrevivência", "bonus": 5}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 33}
    },
    {
        "nome": "Orc Rei",
        "nd": "7", "tipo": "Humanoide", "subtipo": "orc", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 7, "percepcao": 4, "sentidos": ["visão no escuro", "sensibilidade a luz"],
        "defesa": 25, "fortitude": 15, "reflexos": 11, "vontade": 7,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["atordoado", "cansaço"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 210, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Lança", "modalidade": "corpo a corpo", "bonus_ataque": 18, "dano": "2d8+12", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 3, "pericia": "Luta", "descricao": "dois ataques"}
        ],
        "habilidades": [
            {"nome": "Aura de Fúria", "tipo_acao": "passiva", "descricao": "Outros orcs sob comando do orc rei em um raio de 30m recebem +2 na Defesa, em testes de perícia e em rolagens de dano.", "rolls": []},
            {"nome": "Estocada Atroz", "tipo_acao": "passiva", "descricao": "Uma criatura atingida por um ataque de lança do rei fica sangrando (Fort CD 20 evita).", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 1, "constituicao": 4, "inteligencia": 0, "sabedoria": 0, "carisma": 1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 33}
    },
    {
        "nome": "Sapo Atroz",
        "nd": "2", "tipo": "Monstro", "subtipo": None, "tamanho": "Grande", "papel": "solo",
        "iniciativa": 6, "percepcao": 3, "sentidos": ["visão na penumbra"],
        "defesa": 16, "fortitude": 15, "reflexos": 7, "vontade": 0,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 95, "pontos_de_mana": None, "deslocamento": "12m (8q), natação 9m (6q)",
        "ataques": [
            {"nome": "Língua", "modalidade": "corpo a corpo", "bonus_ataque": 12, "dano": "1d6+6", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "mais veneno, alcance 3m"}
        ],
        "habilidades": [
            {"nome": "Agarrar Aprimorado", "tipo_acao": "livre", "descricao": "Língua (teste +16).", "rolls": []},
            {"nome": "Boca de Sapo", "tipo_acao": "livre", "descricao": "No início do turno, causa 2d6+8 de impacto mais veneno na criatura agarrada.", "rolls": ["2d6+8"]},
            {"nome": "Salto Esmagador", "tipo_acao": "padrão", "descricao": "Pula sobre oponente em alcance curto. Alvo cai e sofre 2d6+12 impacto (Ref CD 17 reduz e evita).", "rolls": ["2d6+12"]},
            {"nome": "Veneno", "tipo_acao": "passiva", "descricao": "Perde 1d12 PV e fica paralisado por 1 rodada, Fort CD 18 evita paralisia e reduz perda para 1d6.", "rolls": ["1d12"]}
        ],
        "atributos": {"forca": 6, "destreza": 1, "constituicao": 3, "inteligencia": -4, "sabedoria": 1, "carisma": -2},
        "pericias": [{"nome": "Atletismo", "bonus": 10}, {"nome": "Furtividade", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 36}
    },
    {
        "nome": "Tabrachi Soldado",
        "nd": "1/2", "tipo": "Humanoide", "subtipo": "tabrachi", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 5, "percepcao": 2, "sentidos": ["visão na penumbra"],
        "defesa": 16, "fortitude": 5, "reflexos": 10, "vontade": 1,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 12, "pontos_de_mana": None, "deslocamento": "9m (6q), natação 9m (6q)",
        "ataques": [
            {"nome": "Lança", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Língua", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d4+5", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "alcance 3m"}
        ],
        "habilidades": [
            {"nome": "Linguarudo", "tipo_acao": "passiva", "descricao": "Recebe +2 em testes para desarmar ou derrubar com a língua.", "rolls": []}
        ],
        "atributos": {"forca": 2, "destreza": 2, "constituicao": 3, "inteligencia": -1, "sabedoria": -1, "carisma": -2},
        "pericias": [{"nome": "Atletismo", "bonus": 8}, {"nome": "Furtividade", "bonus": 4}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 37}
    },
    {
        "nome": "Trog Combatente",
        "nd": "1/2", "tipo": "Monstro", "subtipo": "trog", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 3, "percepcao": 0, "sentidos": ["visão no escuro"],
        "defesa": 16, "fortitude": 10, "reflexos": 5, "vontade": 1,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 11, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Lança", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d6+5", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Mau Cheiro", "tipo_acao": "padrão", "descricao": "Fortitude CD 15 evita.", "rolls": []}
        ],
        "atributos": {"forca": 3, "destreza": 1, "constituicao": 3, "inteligencia": -2, "sabedoria": 0, "carisma": -1},
        "pericias": [{"nome": "Furtividade", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 38}
    },
    {
        "nome": "Trog Rei dos Túneis",
        "nd": "4", "tipo": "Monstro", "subtipo": "trog", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 5, "percepcao": 4, "sentidos": ["visão no escuro"],
        "defesa": 25, "fortitude": 17, "reflexos": 11, "vontade": 4,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 226, "pontos_de_mana": None, "deslocamento": "9m (6q), escavação 6m (4q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 17, "dano": "1d8+6", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "duas garras"},
            {"nome": "Mordida", "modalidade": "corpo a corpo", "bonus_ataque": 17, "dano": "1d8+6", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Dilacerar", "tipo_acao": "passiva", "descricao": "Se acertar os dois ataques de garra na mesma criatura, causa +2d8+6.", "rolls": ["2d8+6"]},
            {"nome": "Gosto por Tripas", "tipo_acao": "passiva", "descricao": "Recebe +2 em rolagens de dano contra criaturas que já tenha causado dano na cena.", "rolls": []},
            {"nome": "Mau Cheiro", "tipo_acao": "padrão", "descricao": "Fortitude CD 20 evita.", "rolls": []},
            {"nome": "Terror dos Túneis", "tipo_acao": "passiva", "descricao": "Criatura que comece o turno em alcance curto fica apavorada por 1 rodada e então abalada (Von CD 20 muda para abalada).", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 1, "constituicao": 5, "inteligencia": -2, "sabedoria": 0, "carisma": -1},
        "pericias": [{"nome": "Furtividade", "bonus": 7}, {"nome": "Intimidação", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 38}
    },
    {
        "nome": "Ogro",
        "nd": "3", "tipo": "Humanoide", "subtipo": "gigante", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 3, "percepcao": 1, "sentidos": ["visão na penumbra"],
        "defesa": 23, "fortitude": 16, "reflexos": 10, "vontade": 0,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 130, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Tacape", "modalidade": "corpo a corpo", "bonus_ataque": 16, "dano": "1d12+18", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Burro Demais...", "tipo_acao": "passiva", "descricao": "Sofre -5 em testes de Intuição e Vontade.", "rolls": []},
            {"nome": "...Para Morrer!", "tipo_acao": "passiva", "descricao": "Todo o dano de corte, impacto e perfuração que o ogro sofre é reduzido à metade.", "rolls": []}
        ],
        "atributos": {"forca": 7, "destreza": 0, "constituicao": 4, "inteligencia": -3, "sabedoria": -2, "carisma": -2},
        "pericias": [{"nome": "Atletismo", "bonus": 12}, {"nome": "Intuição", "bonus": -5}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 41}
    },
    {
        "nome": "Ogro Capanga",
        "nd": "7", "tipo": "Humanoide", "subtipo": "gigante", "tamanho": "Grande", "papel": "solo",
        "iniciativa": 9, "percepcao": 4, "sentidos": ["visão na penumbra"],
        "defesa": 36, "fortitude": 23, "reflexos": 18, "vontade": 8,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["enfeitiçado"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 111, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Marreta", "modalidade": "corpo a corpo", "bonus_ataque": 36, "dano": "3d6+49", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques"}
        ],
        "habilidades": [
            {"nome": "Cruel Demais...", "tipo_acao": "passiva", "descricao": "Cada ataque de marreta atinge todas as criaturas ao seu redor. Um único teste contra a Defesa de cada criatura.", "rolls": []},
            {"nome": "...Para Sentir!", "tipo_acao": "passiva", "descricao": "Sofre -5 em Intuição e Vontade. Efeitos negativos duram no máximo 2 rodadas e penalidades são reduzidas à metade.", "rolls": []}
        ],
        "atributos": {"forca": 11, "destreza": 0, "constituicao": 6, "inteligencia": -3, "sabedoria": -1, "carisma": -2},
        "pericias": [{"nome": "Atletismo", "bonus": 20}, {"nome": "Intuição", "bonus": 4}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 41}
    }
]

print(f"Iniciando importação de {len(ameacas_lote2)} monstros (Lote 2)...")
sucessos = 0
for ameaca in ameacas_lote2:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        sucessos += 1
        print(f"✅ {ameaca['nome']} importado.")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")

print(f"\nImportação concluída: {sucessos}/{len(ameacas_lote2)} monstros.")
