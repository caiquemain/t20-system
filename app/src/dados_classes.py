# --- TABELA DE CLASSES (T20 Jogo do Ano + Variantes) ---
# pv_ini: PV Inicial (sem CON)
# pv_niv: PV por Nível (sem CON)
# pm_ini: PM Inicial
# pm_niv: PM por Nível
# attr_chave: Atributo do PM
# pericias_fixas: Lista de perícias que a classe ganha automaticamente (obrigatórias).
# qtd_escolhas: Quantas perícias adicionais o jogador escolhe da lista.
# pericias_lista: Opções disponíveis para escolha.
# proficiencias: Lista de proficiências (Armas Marciais, Armaduras Pesadas, Escudos).

DADOS_CLASSES = {
    # ------------------- CLASSES BÁSICAS -------------------
    "Arcanista": {
        "pv_ini": 8, "pv_niv": 2, "pm_ini": 6, "pm_niv": 6, "attr_chave": "int",
        "pericias_fixas": ["Misticismo", "Vontade"],
        "qtd_escolhas": 2,
        "pericias_lista": ["Conhecimento", "Diplomacia", "Enganação", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Nobreza", "Ofício", "Percepção"],
        "proficiencias": []
    },
    "Bárbaro": {
        "pv_ini": 24, "pv_niv": 6, "pm_ini": 3, "pm_niv": 3, "attr_chave": "for",
        "pericias_fixas": ["Fortitude", "Luta"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Sobrevivência", "Vontade"],
        "proficiencias": ["Armas Marciais", "Escudos"]
    },
    "Bardo": {
        "pv_ini": 12, "pv_niv": 3, "pm_ini": 4, "pm_niv": 4, "attr_chave": "car",
        "pericias_fixas": ["Atuação", "Reflexos"],
        "qtd_escolhas": 6,
        "pericias_lista": ["Acrobacia", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intuição", "Investigação", "Jogatina", "Ladinagem", "Luta", "Misticismo", "Nobreza", "Percepção", "Pontaria", "Vontade"],
        "proficiencias": ["Armas Marciais"]
    },
    "Bucaneiro": {
        "pv_ini": 16, "pv_niv": 4, "pm_ini": 3, "pm_niv": 3, "attr_chave": "des",
        "pericias_fixas": ["Reflexos"],
        "qtd_escolhas": 5,
        "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Enganação", "Fortitude", "Furtividade", "Iniciativa", "Intimidação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": ["Armas Marciais"]
    },
    "Caçador": {
        "pv_ini": 16, "pv_niv": 4, "pm_ini": 4, "pm_niv": 4, "attr_chave": "sab",
        "pericias_fixas": ["Sobrevivência"],
        "qtd_escolhas": 7,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Fortitude", "Furtividade", "Iniciativa", "Investigação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos"],
        "proficiencias": ["Armas Marciais", "Escudos"]
    },
    "Cavaleiro": {
        "pv_ini": 20, "pv_niv": 5, "pm_ini": 3, "pm_niv": 3, "attr_chave": "for",
        "pericias_fixas": ["Fortitude", "Luta"],
        "qtd_escolhas": 2,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Nobreza", "Percepção", "Vontade"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Clérigo": {
        "pv_ini": 16, "pv_niv": 4, "pm_ini": 5, "pm_niv": 5, "attr_chave": "sab",
        "pericias_fixas": ["Religião", "Vontade"],
        "qtd_escolhas": 2,
        "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Nobreza", "Ofício", "Percepção"],
        "proficiencias": ["Armaduras Pesadas", "Escudos"]
    },
    "Druida": {
        "pv_ini": 16, "pv_niv": 4, "pm_ini": 4, "pm_niv": 4, "attr_chave": "sab",
        "pericias_fixas": ["Sobrevivência", "Vontade"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Conhecimento", "Cura", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Ofício", "Percepção", "Religião"],
        "proficiencias": ["Escudos"]
    },
    "Guerreiro": {
        "pv_ini": 20, "pv_niv": 5, "pm_ini": 3, "pm_niv": 3, "attr_chave": "for",
        "pericias_fixas": ["Fortitude"],
        "qtd_escolhas": 3,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Guerra", "Iniciativa", "Intimidação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Vontade"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Inventor": {
        "pv_ini": 12, "pv_niv": 3, "pm_ini": 4, "pm_niv": 4, "attr_chave": "int",
        "pericias_fixas": ["Ofício", "Vontade"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Investigação", "Luta", "Misticismo", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": []
    },
    "Ladino": {
        "pv_ini": 12, "pv_niv": 3, "pm_ini": 4, "pm_niv": 4, "attr_chave": "des",
        "pericias_fixas": ["Ladinagem", "Reflexos"],
        "qtd_escolhas": 8,
        "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": []
    },
    "Lutador": {
        "pv_ini": 20, "pv_niv": 5, "pm_ini": 3, "pm_niv": 3, "attr_chave": "for",
        "pericias_fixas": ["Fortitude", "Luta"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Acrobacia", "Adestramento", "Atletismo", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Reflexos"],
        "proficiencias": []
    },
    "Nobre": {
        "pv_ini": 16, "pv_niv": 4, "pm_ini": 4, "pm_niv": 4, "attr_chave": "car",
        "pericias_fixas": ["Vontade"],
        "qtd_escolhas": 5,
        "pericias_lista": ["Adestramento", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Nobreza", "Ofício", "Percepção", "Pontaria"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Paladino": {
        "pv_ini": 20, "pv_niv": 5, "pm_ini": 3, "pm_niv": 3, "attr_chave": "car",
        "pericias_fixas": ["Luta", "Vontade"],
        "qtd_escolhas": 2,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intuição", "Nobreza", "Percepção", "Religião"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },

    # ------------------- CLASSES EXTRAS MANTIDAS -------------------
    "Frade": {
        "pv_ini": 12, "pv_niv": 3, "pm_ini": 6, "pm_niv": 6, "attr_chave": "sab",
        "pericias_fixas": ["Religião", "Vontade"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Adestramento", "Atuação", "Conhecimento", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Misticismo", "Ofício", "Percepção", "Nobreza"],
        "proficiencias": []
    },
    "Treinador": {
        "pv_ini": 12, "pv_niv": 3, "pm_ini": 4, "pm_niv": 4, "attr_chave": "car",
        "pericias_fixas": ["Adestramento", "Vontade"],
        "qtd_escolhas": 4,
        "pericias_lista": ["Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Religião", "Sobrevivência"],
        "proficiencias": []
    },
}

# ------------------- ADIÇÃO DE CLASSES VARIANTES -------------------
# Esta seção deve vir DEPOIS que DADOS_CLASSES foi definido.
DADOS_CLASSES["Necromante"] = {
    **DADOS_CLASSES["Arcanista"],
    "pericias_fixas": ["Misticismo", "Vontade"],
    "pericias_lista": ["Conhecimento", "Diplomacia", "Enganação", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Nobreza", "Ofício", "Percepção"]
}
DADOS_CLASSES["Machado de Pedra"] = {
    **DADOS_CLASSES["Bárbaro"],
    "pericias_fixas": ["Fortitude", "Luta"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Sobrevivência", "Vontade"]
}
DADOS_CLASSES["Magimarcialista"] = {
    **DADOS_CLASSES["Bardo"],
    "pericias_fixas": ["Atuação", "Reflexos"],
    "pericias_lista": ["Acrobacia", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intuição", "Investigação", "Jogatina", "Ladinagem", "Luta", "Misticismo", "Nobreza", "Percepção", "Pontaria", "Vontade"]
}
DADOS_CLASSES["Duelista"] = {
    **DADOS_CLASSES["Bucaneiro"],
    "pericias_fixas": ["Reflexos"],
    "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Enganação", "Fortitude", "Furtividade", "Iniciativa", "Intimidação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Seteiro"] = {
    **DADOS_CLASSES["Caçador"],
    "pericias_fixas": ["Sobrevivência"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Fortitude", "Furtividade", "Iniciativa", "Investigação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos"]
}
DADOS_CLASSES["Vassalo"] = {
    **DADOS_CLASSES["Cavaleiro"],
    "pericias_fixas": ["Fortitude", "Luta"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Nobreza", "Percepção", "Vontade"]
}
DADOS_CLASSES["Usurpador"] = {
    **DADOS_CLASSES["Clérigo"],
    "pericias_fixas": ["Religião", "Vontade"],
    "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Nobreza", "Ofício", "Percepção"]
}
DADOS_CLASSES["Ermitão"] = {
    **DADOS_CLASSES["Druida"],
    "pericias_fixas": ["Sobrevivência", "Vontade"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Conhecimento", "Cura", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Ofício", "Percepção", "Religião"]
}
DADOS_CLASSES["Inovador"] = {
    **DADOS_CLASSES["Guerreiro"],
    "pericias_fixas": ["Fortitude"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Guerra", "Iniciativa", "Intimidação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Vontade"]
}
DADOS_CLASSES["Alquimista"] = {
    **DADOS_CLASSES["Inventor"],
    "pericias_fixas": ["Ofício", "Vontade"],
    "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Investigação", "Luta", "Misticismo", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Ventanista"] = {
    **DADOS_CLASSES["Ladino"],
    "pericias_fixas": ["Ladinagem", "Reflexos"],
    "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Atleta"] = {
    **DADOS_CLASSES["Lutador"],
    "pericias_fixas": ["Fortitude", "Luta"],
    "pericias_lista": ["Acrobacia", "Adestramento", "Atletismo", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Reflexos"]
}
DADOS_CLASSES["Burguês"] = {
    **DADOS_CLASSES["Nobre"],
    "pericias_fixas": ["Vontade"],
    "pericias_lista": ["Adestramento", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Nobreza", "Ofício", "Percepção", "Pontaria"]
}
DADOS_CLASSES["Santo"] = {
    **DADOS_CLASSES["Paladino"],
    "pericias_fixas": ["Luta", "Vontade"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intuição", "Nobreza", "Percepção", "Religião"]
}
