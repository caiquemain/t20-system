from src.models import TamanhoEnum

# --- TABELA DE RAÇAS (T20 Jogo do Ano + Ameaças/Atlas) ---
# Separamos os dados aqui para facilitar a adição de Habilidades e Poderes depois.
# Estrutura:
# 'attrs': Modificadores FIXOS.
# 'escolhas': Quantos atributos o jogador escolhe somar +1.
# 'tamanho': Enum para regras de furtividade/manobras.
# 'habilidades': (Futuro) Lista de dicionários com nome e descrição das skills.

DADOS_RACAS = {
    # --- BÁSICAS DO LIVRO BÁSICO ---
    "Humano": {
        "attrs": {},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Anão": {
        "attrs": {"con": 2, "sab": 1, "des": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Dahllan": {
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Elfo": {
        "attrs": {"int": 2, "des": 1, "con": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Goblin": {
        "attrs": {"des": 2, "int": 1, "car": -1},
        "tamanho": TamanhoEnum.PEQUENO
    },
    "Lefou": {
        "attrs": {"car": -1},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Minotauro": {
        "attrs": {"for": 2, "con": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Qareen": {
        "attrs": {"car": 2, "int": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Golem": {
        "attrs": {"for": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Hynne": {
        "attrs": {"des": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.PEQUENO
    },
    "Kliren": {
        "attrs": {"int": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Medusa": {
        "attrs": {"des": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Osteon": {
        "attrs": {"con": -1},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Sereia/Tritão": {
        "attrs": {},
        "escolhas": 3,
        "tamanho": TamanhoEnum.MEDIO
    },
    "Sílfide": {
        "attrs": {"car": 2, "des": 1, "for": -2},
        "tamanho": TamanhoEnum.MINUSCULO
    },
    "Suraggel (Aggelus)": {
        "attrs": {"sab": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Suraggel (Sulfure)": {
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO
    },
    "Trog": {
        "attrs": {"con": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO
    },

    # --- ATLAS E AMEAÇAS DE ARTON ---
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
