# -*- coding: utf-8 -*-
"""Novas Magias e Aprimoramentos do suplemento Ameaças de Arton (p. 404–405)."""

_F = "Ameaças de Arton"

DADOS_MAGIAS_AMEACAS = {
    "Açoite Flamejante": {
        "nome": "Açoite Flamejante",
        "fonte": _F,
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Efeito: açoite de chamas criado em sua mão",
        "duracao": "Sustentada",
        "resistencia": "Reflexos parcial",
        "descricao": (
            "Um açoite de fogo surge em uma de suas mãos (fica ocupada pela duração). "
            "Você pode usar uma ação padrão para causar 2d6 pontos de dano de fogo em uma criatura em alcance curto "
            "e deixá-la em chamas e enredada enquanto estiver em chamas dessa forma. "
            "Passar na resistência reduz o dano à metade e evita as chamas."
        ),
        "rolagem": {"formula": "2d6", "tipo": "dano", "tipo_dano": "fogo"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda a execução para movimento.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda o dano para 4d6. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda o dano para 6d6. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Dardo Gélido": {
        "nome": "Dardo Gélido",
        "fonte": _F,
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": (
            "Você dispara um dardo de gelo contra o alvo, que sofre 2d6 pontos de dano de frio "
            "e fica lento por 1 rodada. Passar no teste de resistência reduz o dano à metade e evita a condição."
        ),
        "rolagem": {"formula": "2d6", "tipo": "dano", "tipo_dano": "frio"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta o dano em +1d6.", "efeitos": {}},
            {
                "custo": "+1 PM",
                "descricao": "Aumenta o número de alvos em +1 (limitado pelo círculo máximo de magia que você pode lançar).",
                "efeitos": {},
            },
        ],
    },
    "Invocar Fagulha Elemental": {
        "nome": "Invocar Fagulha Elemental",
        "fonte": _F,
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Efeito: familiar elemental",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": (
            "Transforma uma porção de um elemento inerte (ar, água, fogo ou terra) em um elemental Pequeno "
            "que funciona como um familiar comum ou elemental. Auxilia apenas você e não conta em seu limite de parceiros."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Além do normal, o elemental fornece redução 10 contra o dano correspondente a seu tipo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Em vez do normal, o elemental recebe a habilidade de dois familiares, um comum e um elemental.", "efeitos": {}},
        ],
    },
    "Jato Corrosivo": {
        "nome": "Jato Corrosivo",
        "fonte": _F,
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Linha de 9m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": (
            "Você dispara um jato que causa 2d6 pontos de dano de ácido às criaturas na área. "
            "Contra construtos e objetos soltos, a magia causa +1 ponto de dano por dado."
        ),
        "rolagem": {"formula": "2d6", "tipo": "dano", "tipo_dano": "ácido"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta o dano em +1d6.", "efeitos": {}},
            {
                "custo": "+1 PM",
                "descricao": "Muda a resistência para Reflexos parcial (se falhar, fica vulnerável; se passar, reduz à metade).",
                "efeitos": {},
            },
        ],
    },
    "Katana Celestial": {
        "nome": "Katana Celestial",
        "fonte": _F,
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 15,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Linha de 60m ou duas linhas de 30m (em V)",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": (
            "Um golpe vindo dos céus risca o campo de batalha. Criaturas na área sofrem 12d8 pontos de dano de luz "
            "(ou 12d12 se forem mortos-vivos) e ficam cegas e surdas até o fim da cena "
            "(Reflexos reduz à metade e evita as condições)."
        ),
        "rolagem": {"formula": "12d8", "tipo": "dano", "tipo_dano": "luz"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta o dano em +2d8 (ou +2d12 contra mortos-vivos).", "efeitos": {}},
            {"custo": "+6 PM", "descricao": "Muda a área para uma linha de 120m ou quatro linhas de 30m em direções opostas, formando um X.", "efeitos": {}},
        ],
    },
    "Momento de Tormenta": {
        "nome": "Momento de Tormenta",
        "fonte": _F,
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Cubo de 30m",
        "duracao": "Sustentada",
        "resistencia": "Veja texto",
        "descricao": (
            "Uma nuvem rubra surge acima do conjurador. 1x/turno (ação de movimento) manifesta: "
            "Chuva ácida (6d4 ácido), Neblina venenosa (perde 2d12 PV veneno, Fort evita), "
            "Raios escarlates (até 6 inimigos 6d8 eletricidade, Ref metade) ou Pesadelos reais "
            "(4d6 psíquico e perde 1d4 PM, Von metade e evita perda de PM). "
            "Requer ter observado uma área de Tormenta ao menos uma vez."
        ),
        "rolagem": {"formula": "6d4", "tipo": "dano", "tipo_dano": "ácido"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta o dano em +1 dado do mesmo tipo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Além do normal, criaturas na área ficam alquebradas enquanto permanecerem na área.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "(Apenas Devotos de Aharadak) Muda a área para círculo de 1km de raio.", "efeitos": {}},
        ],
    },
    "Transformação em Dragão": {
        "nome": "Transformação em Dragão",
        "fonte": _F,
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 10,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "Reflexos reduz à metade (sopro)",
        "descricao": (
            "Concede +2 em Força, Constituição, Inteligência e Carisma (sem PV/PM/perícias adicionais), "
            "+5 na Defesa e RD 30 contra o elemento do dragão do componente material (couro/escama T$ 1.000). "
            "1x/rodada (ação padrão) exala sopro em cone de 9m causando 8d6+8 pontos de dano do elemento (Ref metade)."
        ),
        "rolagem": {"formula": "8d6+8", "tipo": "dano", "tipo_dano": "elemental"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o dano do sopro em +1d6+1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus na Defesa em +1.", "efeitos": {}},
            {"custo": "+6 PM", "descricao": "Além do normal, asas de couro brotam de suas costas (deslocamento de voo 18m).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Recebe mordida (1d6, x2, corte; 1 PM ataque extra; ou +2 passos se já tiver mordida).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "O bônus em atributos se torna +4.", "efeitos": {}},
        ],
    },
}

# Aprimoramentos opcionais de Conjurar Mortos-Vivos (Ameaças de Arton, p. 405)
APRIMORAMENTOS_CONJURAR_MORTOS_VIVOS_AMEACAS = [
    {
        "custo": "+2 PM",
        "fonte": _F,
        "opcional": True,
        "descricao": "(Apenas Arcanos, opcional Ameaças) Conjura soterrados (dano de frio; Fort ou enredado 1 rod.). Requer 3º círculo.",
        "efeitos": {},
    },
    {
        "custo": "+3 PM",
        "fonte": _F,
        "opcional": True,
        "descricao": "(Opcional Ameaças) Conjura fúrias de Tauron (Pequeno, voo 12m, incorpóreo, Des 5, Def 18, 1d6 trevas + 1d6 fogo; desprevenido e em chamas, Fort evita). Requer 3º círculo.",
        "efeitos": {},
    },
    {
        "custo": "+3 PM",
        "fonte": _F,
        "opcional": True,
        "descricao": "(Apenas Devotos de Arsenal, opcional Ameaças) Conjura guerreiros perpétuos (For 5, Des 4, Def 33, incorpóreo, 3d6 impacto x2). Requer 3º círculo.",
        "efeitos": {},
    },
    {
        "custo": "+3 PM",
        "fonte": _F,
        "opcional": True,
        "descricao": "(Apenas Devotos de Sszzaas, opcional Ameaças) Conjura zumbis peçonha (For 3, Des 1, Def 25, 1d8+1 trevas + 2d6 veneno; atordoado 1 rod. e fraco, Fort reduz). Requer 3º círculo.",
        "efeitos": {},
    },
]
