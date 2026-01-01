from src.models import TamanhoEnum

# --- DADOS DE RAÇAS (T20 Jogo do Ano) ---
DADOS_RACAS = {
    # --- RAÇAS BÁSICAS ---
    "Humano": {
        "attrs": {},  # +2 em três atributos diferentes (escolha)
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Versatil_Humano"]
    },
    "Anão": {
        "attrs": {"con": 2, "sab": 1, "des": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 6,
        "habilidades": ["Conhecimento_Rochas_Anao", "Devagar_Sempre_Anao", "Duro_Pedra_Anao", "Tradicao_Heredrimm_Anao"]
    },
    "Dahllan": {
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Amiga_Plantas_Dahllan", "Armadura_Allihanna_Dahllan", "Empatia_Selvagem_Dahllan"]
    },
    "Elfo": {
        "attrs": {"int": 2, "des": 1, "con": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "habilidades": ["Graca_Glorienn_Elfo", "Sangue_Magico_Elfo", "Sentidos_Elficos_Elfo"]
    },
    "Goblin": {
        "attrs": {"des": 2, "int": 1, "car": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "deslocamento": 9,
        "habilidades": ["Engenhoso_Goblin", "Espelunqueiro_Goblin", "Peste_Esguia_Goblin", "Rato_Ruas_Goblin"]
    },
    "Lefou": {
        # +1 em três atributos diferentes (exceto Carisma)
        "attrs": {"car": -1},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Cria_Tormenta_Lefou", "Deformidade_Lefou"]
    },
    "Minotauro": {
        "attrs": {"for": 2, "con": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Chifres_Minotauro", "Couro_Rigido_Minotauro", "Faro_Minotauro", "Medo_Altura_Minotauro"]
    },
    "Qareen": {
        "attrs": {"car": 2, "int": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Desejos_Qareen", "Resistencia_Elemental_Qareen", "Tatuagem_Mist_Qareen"]
    },
    "Golem": {
        "attrs": {"for": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 6,
        "habilidades": ["Chassi_Golem", "Criatura_Artificial_Golem", "Fonte_Elemental_Golem", "Proposito_Criacao_Golem"]
    },
    "Hynne": {
        "attrs": {"des": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "deslocamento": 6,
        "habilidades": ["Arremessador_Hynne", "Pequeno_Rechonchudo_Hynne", "Sorte_Salvadora_Hynne"]
    },
    "Kliren": {
        "attrs": {"int": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Hibrido_Kliren", "Engenhosidade_Kliren", "Ossos_Frageis_Kliren", "Vanguardista_Kliren"]
    },
    "Medusa": {
        "attrs": {"des": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Cria_Megalokk_Medusa", "Natureza_Venenosa_Medusa", "Olhar_Atordoante_Medusa"]
    },
    "Osteon": {
        "attrs": {"con": -1},  # +1 em três atributos (exceto Con)
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Armadura_Ossea_Osteon", "Memoria_Postuma_Osteon", "Natureza_Esqueletica_Osteon", "Preco_Nao_Vida_Osteon"]
    },
    "Sereia/Tritão": {
        "attrs": {},  # +1 em três atributos diferentes
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,  # +12m natação (regra especial)
        "habilidades": ["Cancao_Mares_Sereia", "Mestre_Tridente_Sereia", "Transf_Anfibia_Sereia"]
    },
    "Sílfide": {
        "attrs": {"car": 2, "des": 1, "for": -2},
        "tamanho": TamanhoEnum.MINUSCULO,
        "deslocamento": 9,  # Voo
        "habilidades": ["Asas_Borboleta_Silfide", "Esp_Natureza_Silfide", "Magia_Fadas_Silfide"]
    },
    "Suraggel (Aggelus)": {
        "attrs": {"sab": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Heranca_Divina_Suraggel", "Luz_Sagrada_Aggelus"]
    },
    "Suraggel (Sulfure)": {
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Heranca_Divina_Suraggel", "Sombras_Prof_Sulfure"]
    },
    "Trog": {
        "attrs": {"con": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Mau_Cheiro_Trog", "Mordida_Trog", "Reptiliano_Trog", "Sangue_Frio_Trog"]
    },

    # -- Heróis de Arton) ---
    "Eiradaan": {
        "attrs": {"sab": 2, "car": 1, "for": -1},
        "escolhas": 0,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": [
            "Essencia_Feerica_Eiradaan",
            "Magia_Instintiva_Eiradaan",
            "Sentidos_Misticos_Eiradaan",
            "Cancao_Melancolia_Eiradaan"
        ]
    },
    "Galokk": {
        "attrs": {"for": 1, "con": 1, "car": -1},
        "escolhas": 1,
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 9,
        "habilidades": ["Forca_Titas_Galokk", "Meio_Gigante_Galokk", "Infancia_Pequenos_Galokk"]
    },
    "Meio-Elfo": {
        "attrs": {"int": 1},
        "escolhas": 2,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": [
            "Ambicao_Herdada_MeioElfo",
            "Entre_Dois_Mundos_MeioElfo",
            "Sangue_Elfico_MeioElfo"
        ]
    },
    "Sátiro": {"attrs": {"car": 2, "des": 1, "sab": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Meio-Orc": {"attrs": {"for": 2}, "escolhas": 1, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Orc": {"attrs": {"for": 2, "con": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Tabrachi": {"attrs": {"con": 2, "for": 1, "car": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Bugbear": {"attrs": {"for": 2, "des": 1, "car": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Hobgoblin": {"attrs": {"con": 2, "des": 1, "car": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    # Geralmente +rápido
    "Centauro": {"attrs": {"sab": 2, "for": 1, "int": -1}, "tamanho": TamanhoEnum.GRANDE, "deslocamento": 12},
    "Gnoll": {"attrs": {"con": 2, "sab": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Kallyanach": {"attrs": {}, "escolhas": 2, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Kaijin": {"attrs": {"for": 2, "con": 1, "car": -2}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Kappa": {"attrs": {"des": 2, "con": 1, "car": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Nezumi": {"attrs": {"con": 2, "des": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Tengu": {"attrs": {"des": 2, "int": 1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Minauro": {"attrs": {"for": 1}, "escolhas": 2, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Ceratops": {"attrs": {"con": 2, "for": 1, "des": -1, "int": -1}, "tamanho": TamanhoEnum.GRANDE, "deslocamento": 9},
    "Pteros": {"attrs": {"sab": 2, "des": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Velocis": {"attrs": {"des": 2, "sab": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 12},
    "Voracis": {"attrs": {"des": 2, "con": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Yidishan": {"attrs": {"car": -2}, "escolhas": 3, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Elfo-do-Mar": {"attrs": {"des": 2, "con": 1, "int": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Nagah (Macho)": {"attrs": {"for": 1, "des": 1, "con": 1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Nagah (Fêmea)": {"attrs": {"int": 1, "sab": 1, "car": 1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9},
    "Finntroll": {"attrs": {"int": 2, "con": 1, "for": -1}, "tamanho": TamanhoEnum.MEDIO, "deslocamento": 9}
}
