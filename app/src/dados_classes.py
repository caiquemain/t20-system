DADOS_CLASSES = {
    # ------------------- CLASSES BÁSICAS -------------------
    "Arcanista": {
        "pv_inicial": 8, "pv_nivel": 2,
        "pm_inicial": 6, "pm_nivel": 6,
        "pm_atributo": "int",
        "pericias_iniciais": ["Misticismo", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": ["Conhecimento", "Diplomacia", "Enganação", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Nobreza", "Ofício", "Percepção"],
        "proficiencias": []
    },
    "Bárbaro": {
        "pv_inicial": 24, "pv_nivel": 6,
        "pm_inicial": 3, "pm_nivel": 3,
        # Nota: Bárbaro no JdA usa Força para muita coisa, mas PM padrão é Int/Sab ou fixo. Mantendo sua escolha.
        "pm_atributo": "for",
        "pericias_iniciais": ["Fortitude", "Luta"],
        "pericias_escolha": 4,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Sobrevivência", "Vontade"],
        "proficiencias": ["Armas Marciais", "Escudos"]
    },
    "Bardo": {
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Atuação", "Reflexos"],
        "pericias_escolha": 6,
        "pericias_lista": ["Acrobacia", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intuição", "Investigação", "Jogatina", "Ladinagem", "Luta", "Misticismo", "Nobreza", "Percepção", "Pontaria", "Vontade"],
        "proficiencias": ["Armas Marciais"]
    },
    "Bucaneiro": {
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 3, "pm_nivel": 3,
        "pm_atributo": "des",
        "pericias_iniciais": ["Reflexos"],
        "pericias_fixas_selecao": ["Luta", "Pontaria"],
        "pericias_escolha": 5,
        "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Enganação", "Fortitude", "Furtividade", "Iniciativa", "Intimidação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": ["Armas Marciais"]
    },
    "Caçador": {
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "sab",
        "pericias_iniciais": ["Sobrevivência"],
        "pericias_fixas_selecao": ["Luta", "Pontaria"],
        "pericias_escolha": 7,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Fortitude", "Furtividade", "Iniciativa", "Investigação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos"],
        "proficiencias": ["Armas Marciais", "Escudos"]
    },
    "Cavaleiro": {
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pm_atributo": "for",
        "pericias_iniciais": ["Fortitude", "Luta"],
        "pericias_escolha": 2,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Nobreza", "Percepção", "Vontade"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Clérigo": {
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 5, "pm_nivel": 5,
        "pm_atributo": "sab",
        "pericias_iniciais": ["Religião", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Nobreza", "Ofício", "Percepção"],
        "proficiencias": ["Armaduras Pesadas", "Escudos"]
    },
    "Druida": {
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "sab",
        "pericias_iniciais": ["Sobrevivência", "Vontade"],
        "pericias_escolha": 4,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Conhecimento", "Cura", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Ofício", "Percepção", "Religião"],
        "proficiencias": ["Escudos"]
    },
    "Guerreiro": {
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pm_atributo": "for",
        "pericias_iniciais": ["Fortitude"],
        "pericias_fixas_selecao": ["Luta", "Pontaria"],
        "pericias_escolha": 3,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Guerra", "Iniciativa", "Intimidação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Vontade"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Inventor": {
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "int",
        "pericias_iniciais": ["Ofício", "Vontade"],
        "pericias_escolha": 4,
        "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Investigação", "Luta", "Misticismo", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": []
    },
    "Ladino": {
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "des",
        "pericias_iniciais": ["Ladinagem", "Reflexos"],
        "pericias_escolha": 8,
        "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"],
        "proficiencias": []
    },
    "Lutador": {
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pm_atributo": "for",
        "pericias_iniciais": ["Fortitude", "Luta"],
        "pericias_escolha": 4,
        "pericias_lista": ["Acrobacia", "Adestramento", "Atletismo", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Reflexos"],
        "proficiencias": []
    },
    "Nobre": {
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Vontade"],
        "pericias_escolha": 5,
        "pericias_lista": ["Adestramento", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Nobreza", "Ofício", "Percepção", "Pontaria"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },
    "Paladino": {
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pm_atributo": "car",
        "pericias_iniciais": ["Luta", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intuição", "Nobreza", "Percepção", "Religião"],
        "proficiencias": ["Armas Marciais", "Armaduras Pesadas", "Escudos"]
    },

    # ------------------- CLASSES EXTRAS MANTIDAS -------------------
    "Frade": {
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 6, "pm_nivel": 6,
        "pm_atributo": "sab",
        "pericias_iniciais": ["Religião", "Vontade"],
        "pericias_escolha": 4,
        "pericias_lista": ["Adestramento", "Atuação", "Conhecimento", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Misticismo", "Ofício", "Percepção", "Nobreza"],
        "proficiencias": []
    },
    "Treinador": {
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Adestramento", "Vontade"],
        "pericias_escolha": 4,
        "pericias_lista": ["Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Religião", "Sobrevivência"],
        "proficiencias": []
    },
}

# ------------------- ADIÇÃO DE CLASSES VARIANTES -------------------
# Mantendo a lógica de herança, mas sobrescrevendo as chaves corretas se necessário
DADOS_CLASSES["Necromante"] = {
    **DADOS_CLASSES["Arcanista"],
    "pericias_iniciais": ["Misticismo", "Vontade"],
    "pericias_lista": ["Conhecimento", "Diplomacia", "Enganação", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Nobreza", "Ofício", "Percepção"]
}
DADOS_CLASSES["Machado de Pedra"] = {
    **DADOS_CLASSES["Bárbaro"],
    "pericias_iniciais": ["Fortitude", "Luta"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Sobrevivência", "Vontade"]
}
DADOS_CLASSES["Magimarcialista"] = {
    **DADOS_CLASSES["Bardo"],
    "pericias_iniciais": ["Atuação", "Reflexos"],
    "pericias_lista": ["Acrobacia", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intuição", "Investigação", "Jogatina", "Ladinagem", "Luta", "Misticismo", "Nobreza", "Percepção", "Pontaria", "Vontade"]
}
DADOS_CLASSES["Duelista"] = {
    **DADOS_CLASSES["Bucaneiro"],
    "pericias_iniciais": ["Reflexos"],
    "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Enganação", "Fortitude", "Furtividade", "Iniciativa", "Intimidação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Seteiro"] = {
    **DADOS_CLASSES["Caçador"],
    "pericias_iniciais": ["Sobrevivência"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Fortitude", "Furtividade", "Iniciativa", "Investigação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos"]
}
DADOS_CLASSES["Vassalo"] = {
    **DADOS_CLASSES["Cavaleiro"],
    "pericias_iniciais": ["Fortitude", "Luta"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Diplomacia", "Guerra", "Iniciativa", "Intimidação", "Nobreza", "Percepção", "Vontade"]
}
DADOS_CLASSES["Usurpador"] = {
    **DADOS_CLASSES["Clérigo"],
    "pericias_iniciais": ["Religião", "Vontade"],
    "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Nobreza", "Ofício", "Percepção"]
}
DADOS_CLASSES["Ermitão"] = {
    **DADOS_CLASSES["Druida"],
    "pericias_iniciais": ["Sobrevivência", "Vontade"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Conhecimento", "Cura", "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Ofício", "Percepção", "Religião"]
}
DADOS_CLASSES["Inovador"] = {
    **DADOS_CLASSES["Guerreiro"],
    "pericias_iniciais": ["Fortitude"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Guerra", "Iniciativa", "Intimidação", "Luta", "Ofício", "Percepção", "Pontaria", "Reflexos", "Vontade"]
}
DADOS_CLASSES["Alquimista"] = {
    **DADOS_CLASSES["Inventor"],
    "pericias_iniciais": ["Ofício", "Vontade"],
    "pericias_lista": ["Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa", "Investigação", "Luta", "Misticismo", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Ventanista"] = {
    **DADOS_CLASSES["Ladino"],
    "pericias_iniciais": ["Ladinagem", "Reflexos"],
    "pericias_lista": ["Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria"]
}
DADOS_CLASSES["Atleta"] = {
    **DADOS_CLASSES["Lutador"],
    "pericias_iniciais": ["Fortitude", "Luta"],
    "pericias_lista": ["Acrobacia", "Adestramento", "Atletismo", "Enganação", "Furtividade", "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pontaria", "Reflexos"]
}
DADOS_CLASSES["Burguês"] = {
    **DADOS_CLASSES["Nobre"],
    "pericias_iniciais": ["Vontade"],
    "pericias_lista": ["Adestramento", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia", "Enganação", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Luta", "Nobreza", "Ofício", "Percepção", "Pontaria"]
}
DADOS_CLASSES["Santo"] = {
    **DADOS_CLASSES["Paladino"],
    "pericias_iniciais": ["Luta", "Vontade"],
    "pericias_lista": ["Adestramento", "Atletismo", "Cavalgar", "Cura", "Diplomacia", "Fortitude", "Guerra", "Iniciativa", "Intuição", "Nobreza", "Percepção", "Religião"]
}
