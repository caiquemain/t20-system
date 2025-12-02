# --- TABELA DE CLASSES (T20 Jogo do Ano + Suplementos/Ghanor) ---
# pv_ini: PV no nível 1 (sem somar CON)
# pv_niv: PV por nível seguinte (sem somar CON)
# pm_ini: PM no nível 1
# pm_niv: PM por nível seguinte
# attr_chave: Atributo que soma no PM Total (Se a regra da classe permitir)

DADOS_CLASSES = {
    # --- CLASSES BÁSICAS (T20 JdA) ---
    "Arcanista": {
        "pv_ini": 8, "pv_niv": 2,
        "pm_ini": 6, "pm_niv": 6,
        "attr_chave": "int"
    },
    "Bárbaro": {
        "pv_ini": 24, "pv_niv": 6,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": ""
    },
    "Bardo": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Bucaneiro": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "des"
    },
    "Caçador": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "sab"
    },
    "Cavaleiro": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Clérigo": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 5, "pm_niv": 5,
        "attr_chave": "sab"
    },
    "Druida": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "sab"
    },
    "Guerreiro": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Inventor": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "int"
    },
    "Ladino": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "des"
    },
    "Lutador": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Nobre": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Paladino": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "car"
    },

    # --- CLASSES EXTRAS (Ghanor/Suplementos) ---
    "Frade": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 6, "pm_niv": 6,
        "attr_chave": "sab"
    },
    "Treinador": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Alquimista": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "int"
    },
    "Atleta": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Burguês": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Duelista": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "des"
    },
    "Ermitão": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "sab"
    },
    "Inovador": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Machado de Pedra": {
        "pv_ini": 24, "pv_niv": 6,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": ""
    },
    "Magimarcialista": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Necromante": {
        "pv_ini": 8, "pv_niv": 2,
        "pm_ini": 6, "pm_niv": 6,
        "attr_chave": "int"
    },
    "Santo": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "car"
    },
    "Seteiro": {
        "pv_ini": 16, "pv_niv": 4,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "sab"
    },
    "Vassalo": {
        "pv_ini": 20, "pv_niv": 5,
        "pm_ini": 3, "pm_niv": 3,
        "attr_chave": "for"
    },
    "Ventanista": {
        "pv_ini": 12, "pv_niv": 3,
        "pm_ini": 4, "pm_niv": 4,
        "attr_chave": "des"
    }
}
