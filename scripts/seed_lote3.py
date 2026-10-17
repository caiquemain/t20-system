import requests

API_URL = "http://localhost:8000/ameacas/"

ameacas_lote3 = [
    {
        "nome": "Bandido Comum",
        "nd": "1/4", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 4, "percepcao": 1, "sentidos": [],
        "defesa": 13, "fortitude": 1, "reflexos": 3, "vontade": -1,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 6, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Clava", "modalidade": "corpo a corpo", "bonus_ataque": 7, "dano": "1d6+3", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [],
        "atributos": {"forca": 1, "destreza": 2, "constituicao": 1, "inteligencia": 0, "sabedoria": -1, "carisma": 0},
        "pericias": [{"nome": "Furtividade", "bonus": 5}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 42}
    },
    {
        "nome": "Bandido Ligeiro",
        "nd": "1/2", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 4, "percepcao": 1, "sentidos": [],
        "defesa": 15, "fortitude": 3, "reflexos": 5, "vontade": 0,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 9, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Clava", "modalidade": "corpo a corpo", "bonus_ataque": 9, "dano": "1d6+5", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Funda", "modalidade": "à distância", "bonus_ataque": 9, "dano": "1d6+1", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Pontaria", "descricao": None}
        ],
        "habilidades": [],
        "atributos": {"forca": 1, "destreza": 2, "constituicao": 1, "inteligencia": 0, "sabedoria": -1, "carisma": 0},
        "pericias": [{"nome": "Furtividade", "bonus": 6}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 42}
    },
    {
        "nome": "Bandido Selvagem",
        "nd": "1/2", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 4, "percepcao": 3, "sentidos": [],
        "defesa": 16, "fortitude": 8, "reflexos": 6, "vontade": 2,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 12, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Lança", "modalidade": "corpo a corpo", "bonus_ataque": 11, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques"},
            {"nome": "Azagaia", "modalidade": "à distância", "bonus_ataque": 11, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Pontaria", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Arremesso de Emboscada", "tipo_acao": "livre", "descricao": "Uma vez no primeiro turno, saca uma azagaia e faz ataque à distância.", "rolls": []}
        ],
        "atributos": {"forca": 2, "destreza": 1, "constituicao": 1, "inteligencia": 0, "sabedoria": 0, "carisma": -1},
        "pericias": [{"nome": "Furtividade", "bonus": 7}, {"nome": "Sobrevivência", "bonus": 2}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 43}
    },
    {
        "nome": "Capanga",
        "nd": "1/4", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 3, "percepcao": 2, "sentidos": [],
        "defesa": 13, "fortitude": 5, "reflexos": 3, "vontade": 0,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 7, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Tacape", "modalidade": "corpo a corpo", "bonus_ataque": 10, "dano": "1d10+5", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Ímpeto Agressor", "tipo_acao": "passiva", "descricao": "Recebe +1d10 na rolagem de dano do primeiro ataque na cena.", "rolls": ["1d10"]}
        ],
        "atributos": {"forca": 3, "destreza": 1, "constituicao": 1, "inteligencia": -1, "sabedoria": 0, "carisma": -1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 43}
    },
    {
        "nome": "Jagunço",
        "nd": "1", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "lacaio",
        "iniciativa": 7, "percepcao": 3, "sentidos": [],
        "defesa": 18, "fortitude": 8, "reflexos": 9, "vontade": 5,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["medo"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 21, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Espada longa", "modalidade": "corpo a corpo", "bonus_ataque": 14, "dano": "1d8+6", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques"},
            {"nome": "Pistola", "modalidade": "à distância", "bonus_ataque": 14, "dano": "2d6+6", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 3, "pericia": "Pontaria", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Saque Rápido", "tipo_acao": "passiva", "descricao": "Saca ou guarda itens como ação livre e recarrega pistola como ação de movimento.", "rolls": []}
        ],
        "atributos": {"forca": 2, "destreza": 3, "constituicao": 2, "inteligencia": -1, "sabedoria": 0, "carisma": -1},
        "pericias": [{"nome": "Intimidação", "bonus": 6}, {"nome": "Sobrevivência", "bonus": 5}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 43}
    },
    {
        "nome": "Capanga Minotauro",
        "nd": "3", "tipo": "Humanoide", "subtipo": "minotauro", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 3, "percepcao": 2, "sentidos": ["faro"],
        "defesa": 22, "fortitude": 15, "reflexos": 5, "vontade": 10,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 35, "pontos_de_mana": None, "deslocamento": "6m (4q)",
        "ataques": [
            {"nome": "Machado de batalha", "modalidade": "corpo a corpo", "bonus_ataque": 17, "dano": "2d6+15", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 3, "pericia": "Luta", "descricao": None},
            {"nome": "Chifres", "modalidade": "corpo a corpo", "bonus_ataque": 17, "dano": "1d6+15", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Azagaia", "modalidade": "à distância", "bonus_ataque": 17, "dano": "1d6+10", "tipo_dano": "perfuração", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Pontaria", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Medo de Altura", "tipo_acao": "passiva", "descricao": "Se adjacente a queda de 3m+, fica abalado.", "rolls": []}
        ],
        "atributos": {"forca": 5, "destreza": 0, "constituicao": 3, "inteligencia": -1, "sabedoria": 0, "carisma": -1},
        "pericias": [],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 44}
    },
    {
        "nome": "Chefe Bandido",
        "nd": "2", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 4, "percepcao": 2, "sentidos": [],
        "defesa": 16, "fortitude": 5, "reflexos": 8, "vontade": 3,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 30, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Espada curta", "modalidade": "corpo a corpo", "bonus_ataque": 9, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Adaga", "modalidade": "à distância", "bonus_ataque": 7, "dano": "1d4+3", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Pontaria", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +2d6 em alvos desprevenidos ou flanqueados.", "rolls": ["2d6"]}
        ],
        "atributos": {"forca": 3, "destreza": 2, "constituicao": 2, "inteligencia": 0, "sabedoria": 0, "carisma": 1},
        "pericias": [{"nome": "Furtividade", "bonus": 7}, {"nome": "Intimidação", "bonus": 6}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 45}
    },
    {
        "nome": "Chefe de Gangue",
        "nd": "3", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 6, "percepcao": 6, "sentidos": [],
        "defesa": 19, "fortitude": 11, "reflexos": 7, "vontade": 4,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": ["medo +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 63, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Espada longa", "modalidade": "corpo a corpo", "bonus_ataque": 12, "dano": "1d8+5", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Espada curta", "modalidade": "corpo a corpo", "bonus_ataque": 12, "dano": "1d6+5", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +2d6 em alvos desprevenidos ou flanqueados.", "rolls": ["2d6"]},
            {"nome": "Ordens", "tipo_acao": "movimento", "descricao": "Grita ordens. Aliados em alcance médio recebem +2 em testes de perícia até o fim da cena.", "rolls": []}
        ],
        "atributos": {"forca": 3, "destreza": 2, "constituicao": 2, "inteligencia": 1, "sabedoria": 0, "carisma": 1},
        "pericias": [{"nome": "Furtividade", "bonus": 7}, {"nome": "Intimidação", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 45}
    },
    {
        "nome": "Chefe de Quadrilha",
        "nd": "5", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "solo",
        "iniciativa": 8, "percepcao": 5, "sentidos": [],
        "defesa": 22, "fortitude": 14, "reflexos": 11, "vontade": 5,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": ["medo +5"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 120, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Espada longa", "modalidade": "corpo a corpo", "bonus_ataque": 16, "dano": "1d8+6", "tipo_dano": "corte", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None},
            {"nome": "Espada curta", "modalidade": "corpo a corpo", "bonus_ataque": 16, "dano": "1d6+6", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": None}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +3d6 em alvos desprevenidos ou flanqueados.", "rolls": ["3d6"]},
            {"nome": "Ordens", "tipo_acao": "movimento", "descricao": "Grita ordens. Aliados em alcance médio recebem +2 em testes de perícia até o fim da cena.", "rolls": []},
            {"nome": "Tropas Dispensáveis", "tipo_acao": "reação", "descricao": "Uma vez por rodada, quando afetado por ataque/efeito, faz um aliado adjacente sofrer os efeitos em seu lugar.", "rolls": []}
        ],
        "atributos": {"forca": 3, "destreza": 3, "constituicao": 2, "inteligencia": 1, "sabedoria": 0, "carisma": 1},
        "pericias": [{"nome": "Furtividade", "bonus": 8}, {"nome": "Intimidação", "bonus": 8}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 45}
    },
    {
        "nome": "Gatuno",
        "nd": "1", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 7, "percepcao": 2, "sentidos": [],
        "defesa": 14, "fortitude": 0, "reflexos": 11, "vontade": 5,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 25, "pontos_de_mana": None, "deslocamento": "9m (6q), escalada 6m (4q)",
        "ataques": [
            {"nome": "Porrete", "modalidade": "corpo a corpo", "bonus_ataque": 9, "dano": "1d6+5", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "não letal"}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +2d6 em alvos desprevenidos ou flanqueados.", "rolls": ["2d6"]},
            {"nome": "Pancada na Cabeça", "tipo_acao": "passiva", "descricao": "Criatura atingida por ataque furtivo fica inconsciente e caída, ou exausta se em combate (Fort CD 16 reduz para fatigada).", "rolls": []},
            {"nome": "Sombra", "tipo_acao": "passiva", "descricao": "Não sofre penalidade em Furtividade por mover e reduz penalidade de ações chamativas para -10.", "rolls": []}
        ],
        "atributos": {"forca": 0, "destreza": 4, "constituicao": 1, "inteligencia": 1, "sabedoria": 0, "carisma": 0},
        "pericias": [{"nome": "Acrobacia", "bonus": 7}, {"nome": "Furtividade", "bonus": 10}, {"nome": "Ladinagem", "bonus": 7}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 49}
    },
    {
        "nome": "Gatuno Mestre",
        "nd": "3", "tipo": "Humanoide", "subtipo": "humano", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 8, "percepcao": 3, "sentidos": [],
        "defesa": 19, "fortitude": 3, "reflexos": 15, "vontade": 9,
        "defesas_especiais": {"reducao_dano": [], "imunidades": [], "resistencias": ["movimento +3", "evasão"], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 68, "pontos_de_mana": None, "deslocamento": "9m (6q), escalada 6m (4q)",
        "ataques": [
            {"nome": "Porrete", "modalidade": "corpo a corpo", "bonus_ataque": 14, "dano": "1d6+7", "tipo_dano": "impacto", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "não letal"}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +3d6 em alvos desprevenidos ou flanqueados.", "rolls": ["3d6"]},
            {"nome": "Bomba de Fumaça", "tipo_acao": "padrão", "descricao": "Bomba em ponto em alcance curto. Fumaça em raio de 6m até o fim da cena (camuflagem leve a 1,5m e total a partir de 3m).", "rolls": []},
            {"nome": "Pancada na Cabeça", "tipo_acao": "passiva", "descricao": "Criatura atingida por ataque furtivo fica inconsciente e caída, ou exausta se em combate (Fort CD 19 reduz para fatigada).", "rolls": []},
            {"nome": "Sombra", "tipo_acao": "passiva", "descricao": "Não sofre penalidade em Furtividade por mover e reduz penalidade de ações chamativas para -10.", "rolls": []}
        ],
        "atributos": {"forca": 0, "destreza": 4, "constituicao": 1, "inteligencia": 1, "sabedoria": 0, "carisma": 0},
        "pericias": [{"nome": "Acrobacia", "bonus": 9}, {"nome": "Furtividade", "bonus": 12}, {"nome": "Ladinagem", "bonus": 10}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 49}
    },
    {
        "nome": "Sacerdote de Hyninn",
        "nd": "2", "tipo": "Humanoide", "subtipo": "goblin", "tamanho": "Pequeno", "papel": "especial",
        "iniciativa": 6, "percepcao": 6, "sentidos": ["visão no escuro"],
        "defesa": 17, "fortitude": 5, "reflexos": 7, "vontade": 12,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["efeitos mentais"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": None},
        "pontos_de_vida": 49, "pontos_de_mana": 28, "deslocamento": "9m (6q), escalada 9m (6q)",
        "ataques": [
            {"nome": "Adaga", "modalidade": "corpo a corpo", "bonus_ataque": 10, "dano": "1d4+5", "tipo_dano": "perfuração", "margem_critico": 19, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques"}
        ],
        "habilidades": [
            {"nome": "Bênção do Gatuno", "tipo_acao": "livre", "descricao": "Uma vez por cena, lança uma magia como ação livre pagando o custo normal.", "rolls": []},
            {"nome": "Forma de Macaco", "tipo_acao": "completa", "custo_pm": 2, "descricao": "Transforma-se em macaco. Adquire tamanho Minúsculo (+5 Furtividade, -5 manobras). Dura até atacar/lançar magia/sofrer dano.", "rolls": []},
            {"nome": "Malandragem Divina", "tipo_acao": "livre", "custo_pm": 1, "descricao": "Quando faz teste de perícia, usa Enganação no lugar da perícia original.", "rolls": []},
            {"nome": "Magias (clérigo 2º)", "tipo_acao": "passiva", "descricao": "CD 18. Arma Espiritual, Curar Ferimentos, Despedaçar.", "rolls": []}
        ],
        "atributos": {"forca": -1, "destreza": 3, "constituicao": 1, "inteligencia": 0, "sabedoria": 3, "carisma": 2},
        "pericias": [{"nome": "Enganação", "bonus": 7}, {"nome": "Ladinagem", "bonus": 10}, {"nome": "Religião", "bonus": 6}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 46}
    },
    {
        "nome": "Duplo",
        "nd": "5", "tipo": "Humanoide", "subtipo": "duplo", "tamanho": "Médio", "papel": "especial",
        "iniciativa": 9, "percepcao": 6, "sentidos": [],
        "defesa": 21, "fortitude": 5, "reflexos": 15, "vontade": 10,
        "defesas_especiais": {"reducao_dano": [], "imunidades": ["adivinhação", "efeitos mentais"], "resistencias": [], "vulnerabilidades": [], "cura_acelerada": "5"},
        "pontos_de_vida": 143, "pontos_de_mana": None, "deslocamento": "9m (6q)",
        "ataques": [
            {"nome": "Garra", "modalidade": "corpo a corpo", "bonus_ataque": 14, "dano": "1d6+7", "tipo_dano": "corte", "margem_critico": 20, "multiplicador_critico": 2, "pericia": "Luta", "descricao": "dois ataques"}
        ],
        "habilidades": [
            {"nome": "Ataque Furtivo", "tipo_acao": "passiva", "descricao": "Causa +3d6 em alvos desprevenidos ou flanqueados.", "rolls": ["3d6"]},
            {"nome": "Detectar Pensamentos", "tipo_acao": "passiva", "descricao": "Detecta pensamentos superficiais em alcance curto. Não pode ser surpreendido e recebe +2 Defesa/perícias contra essas criaturas.", "rolls": []},
            {"nome": "Mudar Forma", "tipo_acao": "padrão", "descricao": "Assume forma de qualquer humanoide Pequeno a Grande (como Metamorfose). Pode manter indefinidamente, mas reverte à forma natural se morrer.", "rolls": []}
        ],
        "atributos": {"forca": 2, "destreza": 5, "constituicao": 2, "inteligencia": 2, "sabedoria": 2, "carisma": 4},
        "pericias": [{"nome": "Enganação", "bonus": 14}, {"nome": "Furtividade", "bonus": 11}, {"nome": "Intuição", "bonus": 10}],
        "fonte": {"livro": "Ameaças de Arton", "pagina": 50}
    }
]

print(f"Iniciando importação de {len(ameacas_lote3)} monstros (Lote 3)...")
sucessos = 0
for ameaca in ameacas_lote3:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        sucessos += 1
        print(f"✅ {ameaca['nome']} importado.")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")

print(f"\nImportação concluída: {sucessos}/{len(ameacas_lote3)} monstros.")
