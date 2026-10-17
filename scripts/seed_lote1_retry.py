import requests

API_URL = "http://localhost:8000/ameacas/"

ameacas_faltantes = [
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
    }
]

print(f"Iniciando reimportação de {len(ameacas_faltantes)} monstros...")
for ameaca in ameacas_faltantes:
    r = requests.post(API_URL, json=ameaca)
    if r.status_code == 201:
        print(f"✅ {ameaca['nome']} importado com sucesso.")
    else:
        print(f"❌ Erro ao importar {ameaca['nome']}: {r.text}")
