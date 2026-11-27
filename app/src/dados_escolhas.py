# -*- coding: utf-8 -*-
"""Catálogo ÚNICO de opções de escolha do sistema (fonte de verdade).

O frontend NÃO duplica estas listas: tudo vem de GET /dados/escolhas.
Inclui escolhas do Livro Básico (T20 JdA) e dos suplementos (Ameaças, Atlas, etc.).
"""

ATRIBUTOS = [
    {"valor": "forca", "rotulo": "Força"},
    {"valor": "destreza", "rotulo": "Destreza"},
    {"valor": "constituicao", "rotulo": "Constituição"},
    {"valor": "inteligencia", "rotulo": "Inteligência"},
    {"valor": "sabedoria", "rotulo": "Sabedoria"},
    {"valor": "carisma", "rotulo": "Carisma"},
]

ESCOLAS_MAGIA = [
    "Abjuração", "Adivinhação", "Convocação", "Encantamento",
    "Evocação", "Ilusão", "Necromancia", "Transmutação",
]

FAMILIARES_ARCANOS = [
    "Borboleta", "Cobra", "Coruja", "Corvo", "Falcão",
    "Gato", "Lagarto", "Morcego", "Rato", "Sapo",
]

# Quadro "Animais Totêmicos" — Bárbaro (T20 JdA p.41)
ANIMAIS_TOTEMICOS_MAGIAS = {
    "Coruja": "Orientação",
    "Corvo": "Visão Mística",
    "Falcão": "Detectar Ameaças",
    "Grifo": "Primor Atlético",
    "Lobo": "Concentração de Combate",
    "Raposa": "Imagem Espelhada",
    "Tartaruga": "Armadura Arcana",
    "Urso": "Vitalidade Fantasma",
}

ANIMAIS_TOTEMICOS = [
    {"valor": animal, "rotulo": f"{animal} ({magia})"}
    for animal, magia in ANIMAIS_TOTEMICOS_MAGIAS.items()
]

TIPOS_DANO_ELEMENTAL = ["ácido", "eletricidade", "fogo", "frio", "trevas"]
TIPOS_DANO_KALLYANACH = ["ácido", "eletricidade", "fogo", "frio", "luz", "trevas"]

BENCAOS_KALLYADRANOCH = [
    {"valor": "Armamento Kallyanach", "rotulo": "Armamento Kallyanach (arma natural 1d6)"},
    {"valor": "Asas Dracônicas", "rotulo": "Asas Dracônicas (voo 9m por 1 PM/rod.)"},
    {"valor": "Escamas Elementais", "rotulo": "Escamas Elementais (+2 Defesa, RD 10)"},
    {"valor": "Prática Arcana", "rotulo": "Prática Arcana (magia arcana 1º círc. do elemento)"},
    {"valor": "Sentidos Dracônicos", "rotulo": "Sentidos Dracônicos (faro e visão no escuro)"},
    {"valor": "Sopro de Dragão", "rotulo": "Sopro de Dragão (cone 6m, 1d12 elemental)"},
]

TALENTOS_BANDO_KOBOLDS = [
    {"valor": "Amontoados", "rotulo": "Amontoados (conta como Grande p/ espaço e manobras)"},
    {"valor": "Armadilha Terrível", "rotulo": "Armadilha Terrível (engenhoca com magia 1º círc.)"},
    {"valor": "Diferentão", "rotulo": "Diferentão (poder de outra classe, nível -4)"},
    {"valor": "Ex-Familiar", "rotulo": "Ex-Familiar (+2 PM e benefícios de familiar)"},
    {"valor": "O Ousado", "rotulo": "O Ousado (1 PM destaca 1 kobold, 2d4 corte)"},
    {"valor": "Os do Fundo", "rotulo": "Os do Fundo (3º braço p/ arma leve; req: Organizadinhos)"},
    {"valor": "Organizadinhos", "rotulo": "Organizadinhos (Des para carga + 1 item vestido extra)"},
    {"valor": "Pestes Oportunistas", "rotulo": "Pestes Oportunistas (+1d6 dano em alvo já ferido)"},
    {"valor": "Somos Explosivos", "rotulo": "Somos Explosivos (arremessa kobold explosivo)"},
    {"valor": "Tática de Enxame", "rotulo": "Tática de Enxame (2 PM forma enxame; req: Amontoados)"},
]

MARAVILHAS_MECANICAS_MASHIN = [
    {"valor": "Adaptação Elemental", "rotulo": "Adaptação Elemental (2 PM: RD 10 elemental pela cena)"},
    {"valor": "Arma Acoplada", "rotulo": "Arma Acoplada (embutida, não desarmável, Saque Rápido)"},
    {"valor": "Arma Elemental", "rotulo": "Arma Elemental (2 PM: +1d6 elemental na arma)"},
    {"valor": "Auxílio de Mira", "rotulo": "Auxílio de Mira (1 PM: +2 margem de ameaça à distância)"},
    {"valor": "Caminho da Perfeição", "rotulo": "Caminho da Perfeição (+2 em uma perícia treinada)"},
    {"valor": "Canalizar Reparos", "rotulo": "Canalizar Reparos (ação completa: 5 PV por PM)"},
    {"valor": "Canhão Energético", "rotulo": "Canhão Energético (1 PM: +1 dado em arma de fogo acoplada)"},
    {"valor": "Dínamo de Mana", "rotulo": "Dínamo de Mana (movimento: -1 PM na habilidade escolhida)"},
    {"valor": "Pernas Aprimoradas", "rotulo": "Pernas Aprimoradas (2 PM: +6m desloc. e +5 Atletismo)"},
    {"valor": "Reservatório Alquímico", "rotulo": "Reservatório Alquímico (armazena 2 doses alquímicas)"},
]

PERICIAS_INT_CAR = [
    "Atuação", "Conhecimento", "Diplomacia", "Enganação", "Guerra",
    "Intimidação", "Investigação", "Jogatina", "Misticismo", "Nobreza", "Ofício",
]

PERICIAS_PAPEL_TRIBAL = ["Cura", "Intimidação", "Ofício", "Sobrevivência"]

TATUAGENS_MISTICAS_TAMALU = [
    {"valor": "defesa", "rotulo": "+1 na Defesa"},
    {"valor": "resistencia_magia", "rotulo": "Resistência a magia +2"},
    {"valor": "magia_1", "rotulo": "Lançar uma magia de 1º círculo (Sabedoria)"},
]

FORMATOS_DE_OUTRO_MUNDO = [
    {"valor": "habilidade", "rotulo": "Habilidade (mágica ou mundana)"},
    {"valor": "tecnologia", "rotulo": "Tecnologia (item Minúsculo 1 esp., +2 limite PM)"},
]

CAMINHOS_ARCANISTA_INFO = {
    "Bruxo": "Atributo-chave: Inteligência. Lança magias empunhando um foco (RD 10, PV = metade dos seus); sem foco, teste de Misticismo (CD 20 + PM).",
    "Feiticeiro": "Atributo-chave: Carisma. Poder inato por linhagem sobrenatural; aprende 1 magia nova a cada nível ímpar (3º, 5º, 7º...).",
    "Mago": "Atributo-chave: Inteligência. Memoriza metade das magias após 1h de estudo (1×/dia); +1 magia inicial e +1 a cada círculo novo.",
}

# Poderes e habilidades com escolha secundária -> chave salva em escolhas_aplicadas
# Suporta `catalogo` (lista estática deste arquivo) OU `tipo_dinamico` (resolvido pelo frontend/motor)
PODERES_COM_ESCOLHA = {
    # Livro Básico (T20 JdA)
    "Aumento de Atributo": [{"chave": "atributo", "rotulo": "Atributo", "catalogo": "ATRIBUTOS"}],
    "Especialista em Escola": [{"chave": "escola", "rotulo": "Escola de Magia", "catalogo": "ESCOLAS_MAGIA"}],
    "Mestre em Escola": [{"chave": "escola", "rotulo": "Escola de Magia", "catalogo": "ESCOLAS_MAGIA"}],
    "Familiar": [{"chave": "familiar", "rotulo": "Familiar Arcano", "catalogo": "FAMILIARES_ARCANOS"}],
    "Totem Espiritual": [{"chave": "totem", "rotulo": "Animal Totêmico", "catalogo": "ANIMAIS_TOTEMICOS"}],

    # Ameaças de Arton (Raças)
    "Herança Dracônica": [{"chave": "elemento", "rotulo": "Elemento (RD 5)", "catalogo": "TIPOS_DANO_KALLYANACH"}],
    "Bênção de Kallyadranoch": [
        {"chave": "bencao_1", "rotulo": "1ª Bênção de Kallyadranoch", "catalogo": "BENCAOS_KALLYADRANOCH"},
        {"chave": "bencao_2", "rotulo": "2ª Bênção de Kallyadranoch", "catalogo": "BENCAOS_KALLYADRANOCH"},
    ],
    "Talentos do Bando": [
        {"chave": "talento_1", "rotulo": "1º Talento do Bando", "catalogo": "TALENTOS_BANDO_KOBOLDS"},
        {"chave": "talento_2", "rotulo": "2º Talento do Bando", "catalogo": "TALENTOS_BANDO_KOBOLDS"},
    ],
    "Maravilha Mecânica": [
        {"chave": "maravilha_1", "rotulo": "Maravilha Mecânica", "catalogo": "MARAVILHAS_MECANICAS_MASHIN"},
    ],
    "Terror Vivo": [
        {"chave": "poder_tormenta", "rotulo": "Poder da Tormenta (sem perda de Carisma)", "tipo_dinamico": "poder_tormenta"},
    ],
    "Sapiência": [
        {"chave": "magia_1", "rotulo": "Magia de 1º Círculo (Adivinhação)", "tipo_dinamico": "magia_1_adivinhacao"},
    ],
    "Esperteza Vulpina": [
        {"chave": "pericia_bonus_1", "rotulo": "1ª Perícia (+2, Int/Car)", "catalogo": "PERICIAS_INT_CAR"},
        {"chave": "pericia_bonus_2", "rotulo": "2ª Perícia (+2, Int/Car)", "catalogo": "PERICIAS_INT_CAR"},
    ],
    "Papel Tribal": [
        {"chave": "pericia_1", "rotulo": "Perícia Treinada (Papel Tribal)", "catalogo": "PERICIAS_PAPEL_TRIBAL"},
    ],

    # Atlas de Arton (Origens Regionais com escolha)
    "Origem Regional: Duplo Feérico": [
        {"chave": "habilidade_nv1", "rotulo": "Habilidade de 1º Nível (outra classe)", "tipo_dinamico": "habilidade_classe_nv1_outra"},
        {"chave": "magia_1", "rotulo": "Magia de 1º Círculo (se escolheu Magias)", "tipo_dinamico": "magia_1_qualquer", "depende_de": {"chave": "habilidade_nv1", "contem": "Magias"}},
    ],
    "Origem Regional: Aspirante a Herói": [
        {"chave": "atributo", "rotulo": "Atributo (+1)", "catalogo": "ATRIBUTOS"},
    ],
    "Origem Regional: Futura Lenda": [
        {"chave": "poder_classe", "rotulo": "Poder de Classe (2º nível)", "tipo_dinamico": "poder_classe_atual"},
    ],
    "Origem Regional: Cosmopolita": [
        {"chave": "poder_geral", "rotulo": "Poder Geral (exceto Concedido/Tormenta)", "tipo_dinamico": "poder_geral_sem_concedido_tormenta"},
    ],
    "Origem Regional: Estandarte Vivo": [
        {"chave": "poder_combate_tormenta", "rotulo": "Poder de Combate ou da Tormenta", "tipo_dinamico": "poder_combate_ou_tormenta"},
    ],
    "Origem Regional: Estudante da Academia": [
        {"chave": "magia_1", "rotulo": "Magia Arcana de 1º Círculo (Int)", "tipo_dinamico": "magia_1_arcana"},
    ],
    "Origem Regional: De Outro Mundo": [
        {"chave": "magia_1", "rotulo": "Magia de 1º Círculo", "tipo_dinamico": "magia_1_qualquer"},
        {"chave": "atributo", "rotulo": "Atributo-Chave da Magia", "catalogo": "ATRIBUTOS"},
        {"chave": "formato", "rotulo": "Formato", "catalogo": "FORMATOS_DE_OUTRO_MUNDO"},
    ],
    "Origem Regional: Tamalu": [
        {"chave": "tatuagem", "rotulo": "Tatuagem Mística", "catalogo": "TATUAGENS_MISTICAS_TAMALU"},
        {"chave": "magia_1", "rotulo": "Magia de 1º Círculo (se escolheu Magia)", "tipo_dinamico": "magia_1_qualquer", "depende_de": {"chave": "tatuagem", "igual": "magia_1"}},
    ],

    # Heróis de Arton (Raça: Duende, p. 8–11)
    "Dons": [
        {"chave": "atributo_1", "rotulo": "1º Atributo (+1)", "catalogo": "ATRIBUTOS"},
        {"chave": "atributo_2", "rotulo": "2º Atributo (+1, diferente do 1º)", "catalogo": "ATRIBUTOS"},
    ],
    "Natureza Animal": [
        {"chave": "atributo", "rotulo": "Atributo da Natureza Animal (+1, pode acumular com Dons)", "catalogo": "ATRIBUTOS"},
    ],
    "Maldição": [
        {"chave": "resistencia", "rotulo": "Resistência da Maldição (CD Car)", "catalogo": "RESISTENCIAS_MALDICAO_DUENDE"},
        {"chave": "efeito_maldicao", "rotulo": "Efeito da Maldição", "catalogo": "MALDICOES_DUENDE"},
    ],
    "Metamorfose Animal": [
        {"chave": "forma_selvagem", "rotulo": "Forma Selvagem Básica", "catalogo": "FORMAS_SELVAGENS_BASICAS"},
    ],
    "Limitações de Duende": [
        {"chave": "sonhos_malucos", "rotulo": "Sonhos Malucos (criação aleatória: +2 PM)", "catalogo": "OPCOES_SONHOS_MALUCOS"},
    ],

    # Heróis de Arton (Classe: Treinador, p. 16–21)
    "Treino Especializado": [
        {"chave": "treino_especializado", "rotulo": "Treino Especializado (5º nível)", "catalogo": "TREINOS_ESPECIALIZADOS_TREINADOR"},
    ],
    "Mascote": [
        {"chave": "mascote", "rotulo": "Mascote do Treinador", "catalogo": "MASCOTES_TREINADOR"},
    ],

    # Heróis de Arton (Classes Variantes, p. 22–45)
    "Escola de Duelo": [
        {"chave": "escola_duelo", "rotulo": "Escola de Duelo (2º nível)", "catalogo": "ESCOLAS_DUELO"},
    ],
    "Sítio Sagrado": [
        {"chave": "terreno", "rotulo": "Terreno Associado ao Sítio Sagrado", "catalogo": "TERRENOS_SITIO_SAGRADO"},
    ],
    "Lorde": [
        {"chave": "caminho_lorde", "rotulo": "Caminho do Lorde (9º nível)", "catalogo": "CAMINHOS_LORDE_VASSALO"},
    ],

    # Heróis de Arton (Novas Origens Especiais, p. 46–53)
    "Origem Especial: Menestrel": [
        {"chave": "musica_bardo", "rotulo": "Poder de Música de Bardo", "catalogo": "MUSICAS_MENESTREL"},
    ],
    "Origem Especial: Espião": [
        {"chave": "pericia_carisma", "rotulo": "Perícia com Carisma (exceto Luta/Pontaria)", "catalogo": "PERICIAS_ESPIAO"},
    ],
}

MUSICAS_MENESTREL = [
    {"valor": "Balada Fascinante", "rotulo": "Música: Balada Fascinante"},
    {"valor": "Canção Assustadora", "rotulo": "Música: Canção Assustadora"},
    {"valor": "Melodia Curativa", "rotulo": "Música: Melodia Curativa"},
]

PERICIAS_ESPIAO = [
    "Acrobacia", "Adestramento", "Atletismo", "Atuação", "Cavalgar", "Conhecimento",
    "Cura", "Diplomacia", "Enganação", "Fortitude", "Furtividade", "Guerra",
    "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina",
    "Ladinagem", "Misticismo", "Nobreza", "Ofício", "Percepção", "Pilotagem",
    "Reflexos", "Religião", "Sobrevivência", "Vontade",
]

ESCOLAS_DUELO = [
    {"valor": "Escola Ambidestra", "rotulo": "Escola Ambidestra (+2 Def e Reflexos com 2 armas, 1 leve)"},
    {"valor": "Escola Clássica", "rotulo": "Escola Clássica (+2 dano com 1 arma e mão livre)"},
    {"valor": "Escola de Tiro", "rotulo": "Escola de Tiro (proficiência armas de fogo leves e de uma mão)"},
]

TERRENOS_SITIO_SAGRADO = [
    {"valor": "Aquático", "rotulo": "Aquático (RD Eletricidade 5 no 11º)"},
    {"valor": "Ártico", "rotulo": "Ártico (RD Frio 5 no 11º)"},
    {"valor": "Colina", "rotulo": "Colina (RD Impacto 5 no 11º)"},
    {"valor": "Deserto", "rotulo": "Deserto (RD Fogo 5 no 11º)"},
    {"valor": "Floresta", "rotulo": "Floresta (RD Corte 5 no 11º)"},
    {"valor": "Montanha", "rotulo": "Montanha (RD Perfuração 5 no 11º)"},
    {"valor": "Pântano", "rotulo": "Pântano (RD Ácido 5 no 11º)"},
    {"valor": "Planície", "rotulo": "Planície (RD Luz 5 no 11º)"},
    {"valor": "Subterrâneo", "rotulo": "Subterrâneo (RD Trevas 5 no 11º)"},
]

CAMINHOS_LORDE_VASSALO = [
    {"valor": "Caminho do Soldado", "rotulo": "Caminho do Soldado (Guerreiro; +1 PV/nv no 11º; RD 5 +2 Def no 13º)"},
    {"valor": "Caminho do Governante", "rotulo": "Caminho do Governante (Nobre; +1 Int no 11º; +Car em TR no 13º)"},
]

TREINOS_ESPECIALIZADOS_TREINADOR = [
    {"valor": "Conquistar pelos Números", "rotulo": "Conquistar pelos Números (2º Melhor Amigo; 3 PM ação padrão extra)"},
    {"valor": "Treino Intensivo", "rotulo": "Treino Intensivo (+4 PV/nível, RD 5/10/15, +1 truque no 5º e 11º)"},
]

MASCOTES_TREINADOR = [
    {"valor": "Águia Real", "rotulo": "Águia Real (+1d6 dano com arma 1×/rodada)"},
    {"valor": "Bicho Preguiça", "rotulo": "Bicho Preguiça (garra 1d6 x2 corte; 1 PM ataque extra)"},
    {"valor": "Camundongo Espiritual", "rotulo": "Camundongo Espiritual (+1 CD de habilidades mágicas)"},
    {"valor": "Fada-Borboleta", "rotulo": "Fada-Borboleta (-1 PM em habilidades mágicas)"},
    {"valor": "Gekko Malhado", "rotulo": "Gekko Malhado (+2 Defesa e +2 Reflexos)"},
    {"valor": "Mico-Leão Dourado", "rotulo": "Mico-Leão Dourado (punga com Ladinagem em alcance curto)"},
    {"valor": "Minivaca", "rotulo": "Minivaca (+1 ataque; +2 em investidas)"},
    {"valor": "Ossinhos", "rotulo": "Ossinhos (RD 2 contra corte, frio e perfuração)"},
]

RESISTENCIAS_MALDICAO_DUENDE = ["Fortitude", "Vontade"]

MALDICOES_DUENDE = [
    {"valor": "Apatia Profunda", "rotulo": "Apatia Profunda (alquebrada e frustrada)"},
    {"valor": "Coração de Geleia", "rotulo": "Coração de Geleia (abalada; 1ª ação hostil/cena repete TR ou perde ação)"},
    {"valor": "Envelhecimento Súbito", "rotulo": "Envelhecimento Súbito (fraca e lenta)"},
    {"valor": "Loucura do Verão", "rotulo": "Loucura do Verão (início de cada cena repete TR ou fica confusa)"},
    {"valor": "Mil Verrugas", "rotulo": "Mil Verrugas (-2 Car; criaturas em alcance curto testam Von ou pioram atitude)"},
    {"valor": "Ruína do Corpo", "rotulo": "Ruína do Corpo (fatigada e vulnerável)"},
]

FORMAS_SELVAGENS_BASICAS = ["Ágil", "Feroz", "Resistente", "Sorrateira", "Veloz"]

OPCOES_SONHOS_MALUCOS = [
    {"valor": "nao", "rotulo": "Não (criação escolhida)"},
    {"valor": "sim", "rotulo": "Sim — Sonhos Malucos (+2 PM)"},
]

# Escolhas fixas de classe (UI futura: Bardo/Druida escolhem 3 escolas)
ESCOLHAS_DE_CLASSE = {
    "Bardo": {"escolas_de_magia": 3},
    "Druida": {"escolas_de_magia": 3},
}


def _habilidades_classe_nv1() -> list[dict]:
    """Lista todas as habilidades de classe de 1º nível (para Duplo Feérico)."""
    from .dados_habilidades_classe import DADOS_HABILIDADES_CLASSE

    itens = []
    vistos = set()
    for chave, d in DADOS_HABILIDADES_CLASSE.items():
        if not isinstance(d, dict):
            continue
        if int(d.get("nivel") or 0) != 1:
            continue
        tipo = str(d.get("tipo") or "")
        if "Poder de" in tipo:
            continue
        classe = str(d.get("classe") or "")
        nome = str(d.get("nome") or chave)
        val = f"{classe}::{nome}"
        if val in vistos:
            continue
        vistos.add(val)
        itens.append({
            "valor": val,
            "rotulo": f"{nome} ({classe})",
            "classe": classe,
            "nome": nome,
            "descricao": d.get("descricao", ""),
            "fonte": d.get("fonte", "T20 JdA"),
            "chave_catalogo": chave,
        })
    return sorted(itens, key=lambda x: (x["classe"], x["nome"]))


def montar_catalogo_escolhas() -> dict:
    """Resolve os catálogos e devolve o payload pronto p/ frontend."""
    poderes = {}
    for poder, gatilhos in PODERES_COM_ESCOLHA.items():
        lista = []
        for g in gatilhos:
            entry = {"chave": g["chave"], "rotulo": g["rotulo"]}
            if "catalogo" in g:
                entry["opcoes"] = globals()[g["catalogo"]]
            if "tipo_dinamico" in g:
                entry["tipo_dinamico"] = g["tipo_dinamico"]
            if "depende_de" in g:
                entry["depende_de"] = g["depende_de"]
            lista.append(entry)
        poderes[poder] = lista

    return {
        "ATRIBUTOS": ATRIBUTOS,
        "ESCOLAS_MAGIA": ESCOLAS_MAGIA,
        "FAMILIARES_ARCANOS": FAMILIARES_ARCANOS,
        "ANIMAIS_TOTEMICOS": ANIMAIS_TOTEMICOS,
        "ANIMAIS_TOTEMICOS_MAGIAS": ANIMAIS_TOTEMICOS_MAGIAS,
        "TIPOS_DANO_ELEMENTAL": TIPOS_DANO_ELEMENTAL,
        "TIPOS_DANO_KALLYANACH": TIPOS_DANO_KALLYANACH,
        "BENCAOS_KALLYADRANOCH": BENCAOS_KALLYADRANOCH,
        "TALENTOS_BANDO_KOBOLDS": TALENTOS_BANDO_KOBOLDS,
        "MARAVILHAS_MECANICAS_MASHIN": MARAVILHAS_MECANICAS_MASHIN,
        "PERICIAS_INT_CAR": PERICIAS_INT_CAR,
        "PERICIAS_PAPEL_TRIBAL": PERICIAS_PAPEL_TRIBAL,
        "TATUAGENS_MISTICAS_TAMALU": TATUAGENS_MISTICAS_TAMALU,
        "FORMATOS_DE_OUTRO_MUNDO": FORMATOS_DE_OUTRO_MUNDO,
        "RESISTENCIAS_MALDICAO_DUENDE": RESISTENCIAS_MALDICAO_DUENDE,
        "MALDICOES_DUENDE": MALDICOES_DUENDE,
        "FORMAS_SELVAGENS_BASICAS": FORMAS_SELVAGENS_BASICAS,
        "OPCOES_SONHOS_MALUCOS": OPCOES_SONHOS_MALUCOS,
        "TREINOS_ESPECIALIZADOS_TREINADOR": TREINOS_ESPECIALIZADOS_TREINADOR,
        "MASCOTES_TREINADOR": MASCOTES_TREINADOR,
        "HABILIDADES_CLASSE_NV1": _habilidades_classe_nv1(),
        "CAMINHOS_ARCANISTA_INFO": CAMINHOS_ARCANISTA_INFO,
        "PODERES_COM_ESCOLHA": poderes,
        "ESCOLHAS_DE_CLASSE": ESCOLHAS_DE_CLASSE,
    }
