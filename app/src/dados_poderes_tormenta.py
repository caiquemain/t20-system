# app/src/dados_poderes_tormenta.py

DADOS_PODERES_TORMENTA = {
    "Anatomia_Insana": {
        "nome": "Anatomia Insana",
        "tipo": "Poder da Tormenta",
        "descricao": "25% chance de ignorar crítico/furtivo. +25% por cada 2 outros poderes Tormenta. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    },
    "Antenas": {
        "nome": "Antenas",
        "tipo": "Poder da Tormenta",
        "descricao": "+1 Iniciativa, Percepção, Vontade. Aumenta com outros poderes. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "bonus_pericia_tormenta": ["Iniciativa", "Percepção", "Vontade"],
            "atributo_bonus": {"car": -1}
        }
    },
    "Carapaca": {
        "nome": "Carapaça",
        "tipo": "Poder da Tormenta",
        "descricao": "+1 Defesa. Aumenta com outros poderes. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "defesa_bonus_tormenta": 1,
            "atributo_bonus": {"car": -1}
        }
    },
    "Dentes_Afiados": {
        "nome": "Dentes Afiados",
        "tipo": "Poder da Tormenta",
        "descricao": "Arma natural mordida (1d4). Gaste 1 PM para ataque extra. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    },
    "Empunhadura_Rubra": {
        "nome": "Empunhadura Rubra",
        "tipo": "Poder da Tormenta",
        "descricao": "Gaste 1 PM para +1 em Luta (aumenta com outros poderes). (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    },
    "Membros_Extras": {
        "nome": "Membros Extras",
        "tipo": "Poder da Tormenta",
        "descricao": "Duas patas insetoides (ataques extras). Pode empunhar armas leves. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": ["4 outros poderes Tormenta"],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    },
    "Olhos_Vermelhos": {
        "nome": "Olhos Vermelhos",
        "tipo": "Poder da Tormenta",
        "descricao": "Visão no escuro e +1 Intimidação (aumenta com outros poderes). (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "visao_escuro": True,
            "bonus_pericia_tormenta": ["Intimidação"],
            "atributo_bonus": {"car": -1}
        }
    },
    "Pele_Corrompida": {
        "nome": "Pele Corrompida",
        "tipo": "Poder da Tormenta",
        "descricao": "RD 2 a ácido, eletricidade, fogo, frio, luz, trevas. Aumenta +2 para cada outro poder da Tormenta. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "rd_escalavel_tormenta": {
                "elementos": ["Ácido", "Eletricidade", "Fogo", "Frio", "Luz", "Trevas"],
                "base": 2,
                "por_poder": 2
            },
            "atributo_bonus": {"car": -1}
        }
    },
    "Sangue_Acido": {
        "nome": "Sangue Ácido",
        "tipo": "Poder da Tormenta",
        "descricao": "Ao sofrer dano corpo a corpo, atacante sofre 1 dano ácido por poder Tormenta. (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    },
    "Visco_Rubro": {
        "nome": "Visco Rubro",
        "tipo": "Poder da Tormenta",
        "descricao": "1 PM para +1 dano corpo a corpo (aumenta com outros poderes). (Perde 1 Carisma)",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {
            "atributo_bonus": {"car": -1}
        }
    }
}
