# --- TABELA DE ITENS (T20 Jogo do Ano) ---
# espaco: Peso em espaços (0, 1, 2...)
# tipo: arma, armadura, escudo, geral
# bonus_defesa: Apenas para armaduras/escudos
# penalidade: Penalidade de armadura

DADOS_ITENS = {
    # --- ARMAS SIMPLES ---
    "Adaga": {"espaco": 1, "tipo": "arma", "dano": "1d4", "crit": "19"},
    "Espada Curta": {"espaco": 1, "tipo": "arma", "dano": "1d6", "crit": "19"},
    "Lança": {"espaco": 1, "tipo": "arma", "dano": "1d6", "crit": "20"},
    "Azagaia": {"espaco": 1, "tipo": "arma", "dano": "1d6", "crit": "20"},

    # --- ARMAS MARCIAIS ---
    "Espada Longa": {"espaco": 1, "tipo": "arma", "dano": "1d8", "crit": "19"},
    "Machado de Batalha": {"espaco": 1, "tipo": "arma", "dano": "1d8", "crit": "x3"},
    "Montante": {"espaco": 2, "tipo": "arma", "dano": "2d6", "crit": "19"},
    "Arco Longo": {"espaco": 1, "tipo": "arma", "dano": "1d8", "crit": "x3"},

    # --- ARMADURAS LEVES ---
    "Armadura de Couro": {"espaco": 2, "tipo": "armadura", "bonus_defesa": 2, "penalidade": 0},
    "Couro Batido": {"espaco": 2, "tipo": "armadura", "bonus_defesa": 3, "penalidade": 1},
    "Gibão de Peles": {"espaco": 5, "tipo": "armadura", "bonus_defesa": 4, "penalidade": 3},

    # --- ARMADURAS PESADAS ---
    "Brunea": {"espaco": 5, "tipo": "armadura", "bonus_defesa": 5, "penalidade": 2},
    "Cota de Malha": {"espaco": 10, "tipo": "armadura", "bonus_defesa": 6, "penalidade": 2},
    "Armadura Completa": {"espaco": 10, "tipo": "armadura", "bonus_defesa": 10, "penalidade": 5},

    # --- ESCUDOS ---
    "Escudo Leve": {"espaco": 1, "tipo": "escudo", "bonus_defesa": 1, "penalidade": 1},
    "Escudo Pesado": {"espaco": 2, "tipo": "escudo", "bonus_defesa": 2, "penalidade": 2},

    # --- GERAL ---
    "Mochila de Aventureiro": {"espaco": 0, "tipo": "geral"},
    "Kit de Aventureiro": {"espaco": 2, "tipo": "geral"},
    "Poção de Cura": {"espaco": 0.5, "tipo": "consumivel"},
    "Símbolo Sagrado": {"espaco": 0, "tipo": "geral"}
}
