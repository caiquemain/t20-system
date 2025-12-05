from src.models import TamanhoEnum

# --- TABELA DE RAÇAS (T20 Jogo do Ano + Ameaças/Atlas) ---
# Separamos os dados aqui para facilitar a adição de Habilidades e Poderes depois.
# Estrutura:
# 'attrs': Modificadores FIXOS.
# 'escolhas': Quantos atributos o jogador escolhe somar +1.
# 'tamanho': Enum para regras de furtividade/manobras.
# 'habilidades': Lista de strings com as CHAVES das habilidades definidas em DADOS_HABILIDADES.

DADOS_RACAS = {
    # --- BÁSICAS DO LIVRO BÁSICO (Habilidades Adicionadas) ---
    "Humano": {
        "attrs": {},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Versatil_Humano"]
    },
    "Anão": {
        "attrs": {"con": 2, "sab": 1, "des": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Conhecimento_Rochas_Anao", "Devagar_Sempre_Anao", "Duro_Pedra_Anao", "Tradicao_Heredrimm_Anao"]
    },
    "Dahllan": {
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Amiga_Plantas_Dahllan", "Armadura_Allihanna_Dahllan", "Empatia_Selvagem_Dahllan"]
    },
    "Elfo": {
        "attrs": {"int": 2, "des": 1, "con": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Graca_Glorienn_Elfo", "Sangue_Magico_Elfo", "Sentidos_Elficos_Elfo"]
    },
    "Goblin": {
        "attrs": {"des": 2, "int": 1, "car": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "habilidades": ["Engenhoso_Goblin", "Espelunqueiro_Goblin", "Peste_Esguia_Goblin", "Rato_Ruas_Goblin"]
    },
    "Lefou": {
        "attrs": {"car": -1},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Cria_Tormenta_Lefou", "Deformidade_Lefou"]
    },
    "Minotauro": {
        "attrs": {"for": 2, "con": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Couro_Rigido_Minotauro", "Faro_Minotauro", "Medo_Altura_Minotauro"]
    },
    "Qareen": {
        "attrs": {"car": 2, "int": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Desejos_Qareen", "Resistencia_Elemental_Qareen", "Tatuagem_Mist_Qareen"]
    },
    "Golem": {
        "attrs": {"for": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Chassi_Golem", "Criatura_Artificial_Golem", "Fonte_Elemental_Golem", "Proposito_Criacao_Golem"]
    },
    "Hynne": {
        "attrs": {"des": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "habilidades": ["Arremessador_Hynne", "Pequeno_Rechonchudo_Hynne", "Sorte_Salvadora_Hynne"]
    },
    "Kliren": {
        "attrs": {"int": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Hibrido_Kliren", "Engenhosidade_Kliren", "Ossos_Frageis_Kliren", "Vanguardista_Kliren"]
    },
    "Medusa": {
        "attrs": {"des": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Natureza_Venenosa_Medusa", "Olhar_Atordoante_Medusa"]
    },
    "Osteon": {
        "attrs": {"con": -1},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Armadura_Ossea_Osteon", "Memoria_Postuma_Osteon", "Natureza_Esqueletica_Osteon", "Preco_Nao_Vida_Osteon"]
    },
    "Sereia/Tritão": {
        "attrs": {},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Cancao_Mares_Sereia", "Mestre_Tridente_Sereia", "Transf_Anfibia_Sereia"]
    },
    "Sílfide": {
        "attrs": {"car": 2, "des": 1, "for": -2},
        "tamanho": TamanhoEnum.MINUSCULO,
        "habilidades": ["Asas_Borboleta_Silfide", "Esp_Natureza_Silfide", "Magia_Fadas_Silfide"]
    },
    "Suraggel (Aggelus)": {
        "attrs": {"sab": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Heranca_Divina_Suraggel", "Luz_Sagrada_Aggelus"]
    },
    "Suraggel (Sulfure)": {
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Heranca_Divina_Suraggel", "Sombras_Prof_Sulfure"]
    },
    "Trog": {
        "attrs": {"con": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "habilidades": ["Mau_Cheiro_Trog", "Mordida_Trog", "Reptiliano_Trog", "Sangue_Frio_Trog"]
    },

    # --- ATLAS E AMEAÇAS DE ARTON (Mantidas como Placeholder) ---
    "Eiradaan": {
        "attrs": {"sab": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Galokk": {
        "attrs": {"for": 1, "con": 1, "car": -1},
        "escolhas": 1,
        "tamanho": TamanhoEnum.GRANDE
    },
    "Meio-Elfo": {
        "attrs": {"int": 1},
        "escolhas": 2,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Sátiro": {
        "attrs": {"car": 2, "des": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Meio-Orc": {
        "attrs": {"for": 2},
        "escolhas": 1,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Orc": {
        "attrs": {"for": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Tabrachi": {
        "attrs": {"con": 2, "for": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Bugbear": {
        "attrs": {"for": 2, "des": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Hobgoblin": {
        "attrs": {"con": 2, "des": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Centauro": {
        "attrs": {"sab": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.GRANDE
    },
    "Gnoll": {
        "attrs": {"con": 2, "sab": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Kallyanach": {
        "attrs": {},
        "escolhas": 2,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Kaijin": {
        "attrs": {"for": 2, "con": 1, "car": -2},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Kappa": {
        "attrs": {"des": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Nezumi": {
        "attrs": {"con": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Tengu": {
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Minauro": {
        "attrs": {"for": 1},
        "escolhas": 2,
        "tamanho": TamanhoEnum.MEDIO
    },
    # --- MOREAUS E OUTROS ---
    "Ceratops": {
        "attrs": {"con": 2, "for": 1, "des": -1, "int": -1},
        "tamanho": TamanhoEnum.GRANDE
    },
    "Pteros": {
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Velocis": {
        "attrs": {"des": 2, "sab": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Voracis": {
        "attrs": {"des": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Yidishan": {
        "attrs": {"car": -2},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Elfo-do-Mar": {
        "attrs": {"des": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Nagah (Macho)": {
        "attrs": {"for": 1, "des": 1, "con": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Nagah (Fêmea)": {
        "attrs": {"int": 1, "sab": 1, "car": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Finntroll": {
        "attrs": {"int": 2, "con": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO
    }
}
