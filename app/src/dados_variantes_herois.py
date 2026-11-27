# -*- coding: utf-8 -*-
"""Catálogo oficial das 14 Classes Variantes — Heróis de Arton (Cap. 1, p. 22–45).

Tabela 1-2:
  Arcanista -> Necromante        | Bárbaro   -> Machado de Pedra
  Bardo     -> Magimarcialista   | Bucaneiro -> Duelista
  Caçador   -> Seteiro           | Cavaleiro -> Vassalo
  Clérigo   -> Usurpador         | Druida    -> Ermitão
  Guerreiro -> Inovador          | Inventor  -> Alquimista
  Ladino    -> Ventanista        | Lutador   -> Atleta
  Nobre     -> Burguês           | Paladino  -> Santo
"""
from typing import Dict, Any
from .dados_suplementos import FONTE_HEROIS


MAPA_VARIANTE_PARA_BASE: Dict[str, str] = {
    "Alquimista": "Inventor",
    "Atleta": "Lutador",
    "Burguês": "Nobre",
    "Duelista": "Bucaneiro",
    "Ermitão": "Druida",
    "Inovador": "Guerreiro",
    "Machado de Pedra": "Bárbaro",
    "Magimarcialista": "Bardo",
    "Necromante": "Arcanista",
    "Santo": "Paladino",
    "Seteiro": "Caçador",
    "Usurpador": "Clérigo",
    "Vassalo": "Cavaleiro",
    "Ventanista": "Ladino",
}

TERRENOS_SITIO_SAGRADO_RD: Dict[str, str] = {
    "Aquático": "Eletricidade",
    "Ártico": "Frio",
    "Colina": "Impacto",
    "Deserto": "Fogo",
    "Floresta": "Corte",
    "Montanha": "Perfuração",
    "Pântano": "Ácido",
    "Planície": "Luz",
    "Subterrâneo": "Trevas",
}


# =====================================================================
# 1. CARACTERÍSTICAS DAS 14 CLASSES VARIANTES (p. 22–45)
# =====================================================================

DADOS_CLASSES_VARIANTES: Dict[str, Dict[str, Any]] = {
    "Alquimista": {
        "classe_base": "Inventor",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pericias_iniciais": ["Ofício (Alquimista)", "Vontade"],
        "pericias_escolha": 4,
        "pericias_lista": [
            "Conhecimento", "Cura", "Diplomacia", "Fortitude", "Iniciativa",
            "Investigação", "Luta", "Misticismo", "Ofício", "Percepção", "Pilotagem", "Pontaria",
        ],
        "proficiencias": [],
    },
    "Atleta": {
        "classe_base": "Lutador",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pericias_iniciais": ["Atletismo", "Luta"],
        "pericias_escolha": 4,
        "pericias_lista": [
            "Acrobacia", "Adestramento", "Cavalgar", "Cura", "Fortitude",
            "Iniciativa", "Intimidação", "Ofício", "Percepção", "Pilotagem", "Pontaria", "Reflexos",
        ],
        "proficiencias": [],
    },
    "Burguês": {
        "classe_base": "Nobre",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pericias_iniciais": ["Diplomacia", "Vontade"],
        "pericias_escolha": 6,
        "pericias_lista": [
            "Adestramento", "Atuação", "Cavalgar", "Conhecimento", "Diplomacia",
            "Enganação", "Fortitude", "Guerra", "Iniciativa", "Intimidação", "Intuição",
            "Investigação", "Jogatina", "Luta", "Nobreza", "Ofício", "Percepção", "Pontaria",
        ],
        "proficiencias": [],
    },
    "Duelista": {
        "classe_base": "Bucaneiro",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 3, "pm_nivel": 3,
        "pericias_iniciais": ["Reflexos"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Acrobacia", "Atletismo", "Atuação", "Diplomacia", "Fortitude",
            "Iniciativa", "Intimidação", "Luta", "Ofício", "Percepção", "Pilotagem", "Pontaria",
        ],
        "proficiencias": ["Armas marciais"],
    },
    "Ermitão": {
        "classe_base": "Druida",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "sab",
        "pericias_iniciais": ["Sobrevivência", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Cavalgar", "Conhecimento", "Cura",
            "Fortitude", "Iniciativa", "Intuição", "Luta", "Misticismo", "Ofício", "Percepção", "Religião",
        ],
        "proficiencias": [],
    },
    "Inovador": {
        "classe_base": "Guerreiro",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pericias_iniciais": ["Acrobacia"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Conhecimento", "Fortitude", "Guerra",
            "Iniciativa", "Intimidação", "Investigação", "Luta", "Ofício", "Pontaria", "Reflexos",
        ],
        "proficiencias": ["Armas marciais", "Armaduras pesadas", "Escudos"],
    },
    "Machado de Pedra": {
        "classe_base": "Bárbaro",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 24, "pv_nivel": 6,
        "pm_inicial": 3, "pm_nivel": 3,
        "pericias_iniciais": ["Fortitude", "Luta"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Cavalgar", "Iniciativa", "Intimidação",
            "Ofício", "Percepção", "Pontaria", "Sobrevivência", "Vontade",
        ],
        "proficiencias": ["Escudos"],
    },
    "Magimarcialista": {
        "classe_base": "Bardo",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Atuação", "Luta"],
        "pericias_escolha": 6,
        "pericias_lista": [
            "Acrobacia", "Atletismo", "Cavalgar", "Conhecimento", "Diplomacia",
            "Enganação", "Fortitude", "Guerra", "Iniciativa", "Jogatina", "Misticismo", "Reflexos",
        ],
        "proficiencias": ["Armas marciais"],
    },
    "Necromante": {
        "classe_base": "Arcanista",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 8, "pv_nivel": 2,
        "pm_inicial": 6, "pm_nivel": 6,
        "pm_atributo": "int",
        "pericias_iniciais": ["Misticismo", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Conhecimento", "Cura", "Diplomacia", "Enganação", "Fortitude",
            "Iniciativa", "Intimidação", "Intuição", "Investigação", "Nobreza", "Ofício", "Percepção",
        ],
        "proficiencias": [],
    },
    "Santo": {
        "classe_base": "Paladino",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Religião", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Conhecimento", "Cura", "Diplomacia",
            "Fortitude", "Guerra", "Iniciativa", "Intuição", "Luta", "Ofício", "Percepção",
        ],
        "proficiencias": ["Armas marciais", "Armaduras pesadas", "Escudos"],
    },
    "Seteiro": {
        "classe_base": "Caçador",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 4, "pm_nivel": 4,
        "pericias_iniciais": ["Pontaria", "Sobrevivência"],
        "pericias_escolha": 6,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Cavalgar", "Cura", "Fortitude",
            "Furtividade", "Iniciativa", "Investigação", "Luta", "Ofício", "Percepção", "Reflexos",
        ],
        "proficiencias": ["Armas marciais"],
    },
    "Usurpador": {
        "classe_base": "Clérigo",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 16, "pv_nivel": 4,
        "pm_inicial": 5, "pm_nivel": 5,
        "pm_atributo": "car",
        "pericias_iniciais": ["Enganação", "Vontade"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Atuação", "Conhecimento", "Cura", "Diplomacia", "Furtividade",
            "Iniciativa", "Intimidação", "Intuição", "Misticismo", "Nobreza",
            "Ofício", "Percepção", "Reflexos", "Religião",
        ],
        "proficiencias": [],
    },
    "Vassalo": {
        "classe_base": "Cavaleiro",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 20, "pv_nivel": 5,
        "pm_inicial": 3, "pm_nivel": 3,
        "pericias_iniciais": ["Fortitude", "Luta"],
        "pericias_escolha": 2,
        "pericias_lista": [
            "Adestramento", "Atletismo", "Cavalgar", "Diplomacia", "Guerra",
            "Iniciativa", "Intimidação", "Nobreza", "Percepção", "Vontade",
        ],
        "proficiencias": ["Armas marciais", "Escudos"],
    },
    "Ventanista": {
        "classe_base": "Ladino",
        "fonte": FONTE_HEROIS,
        "pv_inicial": 12, "pv_nivel": 3,
        "pm_inicial": 4, "pm_nivel": 4,
        "pm_atributo": "car",
        "pericias_iniciais": ["Ladinagem", "Reflexos"],
        "pericias_escolha": 8,
        "pericias_lista": [
            "Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Conhecimento",
            "Diplomacia", "Enganação", "Furtividade", "Iniciativa", "Intimidação",
            "Intuição", "Investigação", "Jogatina", "Nobreza", "Ofício", "Percepção", "Pilotagem",
        ],
        "proficiencias": [],
    },
}


# =====================================================================
# 2. HABILIDADES DE CLASSE DAS 14 VARIANTES (Tabelas 1-3 a 1-16)
# =====================================================================

def _h(classe: str, nome: str, nivel: int, descricao: str, efeitos: Dict[str, Any] = None, tipo: str = "Classe", custo_pm: int = 0, requisitos=None) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "nome": nome,
        "tipo": tipo,
        "classe": classe,
        "nivel": nivel,
        "fonte": FONTE_HEROIS,
        "descricao": descricao,
        "efeitos": efeitos or {},
    }
    if custo_pm:
        d["custo_pm"] = custo_pm
    if requisitos:
        d["requisitos"] = requisitos
    return d


DADOS_HABILIDADES_VARIANTES: Dict[str, Dict[str, Any]] = {
    # ── 1. ALQUIMISTA (Inventor, Tabela 1-3, p. 22–24) ──
    "ALQ_ENGENHOSIDADE": _h("Alquimista", "Engenhosidade", 1, "Como o inventor básico: gaste 2 PM para somar sua Inteligência em um teste de perícia (exceto ataques)."),
    "ALQ_LABORATORIO_PESSOAL": _h("Alquimista", "Laboratório Pessoal", 1, "Começa com instrumentos de alquimista aprimorados e 10 itens alquímicos com preço total de até T$ 300."),
    "ALQ_ALQUIMISTA_INICIADO": _h("Alquimista", "Alquimista Iniciado", 2, "Recebe o poder Alquimista Iniciado (T20 p. 68)."),
    "ALQ_MISTURA_BASICA": _h("Alquimista", "Mistura Básica", 3, "Pode usar catalisadores em itens alquímicos como se fossem magias."),
    "ALQ_APLICACAO_RAPIDA": _h("Alquimista", "Aplicação Rápida", 5, "Ação completa e 2 PM: usa dois preparados alquímicos ao mesmo tempo.", custo_pm=2),
    "ALQ_MAGIA_ENGARRAFADA": _h("Alquimista", "Magia Engarrafada", 7, "Pode usar Mistura Básica e Aplicação Rápida em poções."),
    "ALQ_ODORES_ALQUIMICOS": _h("Alquimista", "Odores Alquímicos", 8, "Ação completa: detecta itens alquímicos e poções em alcance médio, identificando tipo, uso e magia/PM."),
    "ALQ_FABRICAR_EMULSAO": _h("Alquimista", "Fabricar Emulsão", 9, "Fabrica emulsões temporárias de encantos (1 encanto nv9 T$ 250 CD 25; 2 encantos nv13 T$ 750 CD 30; 3 encantos nv17 T$ 1.500 CD 35)."),
    "ALQ_MESTRE_ALQUIMISTA": _h("Alquimista", "Mestre Alquimista", 10, "Recebe o poder Mestre Alquimista (T20 p. 69)."),
    "ALQ_BOMBARDEIO_EFICIENTE": _h("Alquimista", "Bombardeio Eficiente", 11, "Ao usar preparado alquímico ou poção de dano, gaste 1 PM para ignorar 10 pontos de RD.", custo_pm=1),
    "ALQ_PEDRA_FILOSOFAL": _h("Alquimista", "Pedra Filosofal", 20, "Cura Acelerada 10 e rola 2 dados em Fortitude (usa o melhor). Pode sacrificar a pedra para salvar a si ou aliado (efeito Segunda Chance + reconstrução; refaz em 1 semana e T$ 18.000).", {"cura_acelerada": 10}),

    # ── 2. ATLETA (Lutador, Tabela 1-4, p. 24–25) ──
    "ATL_BRIGA": _h("Atleta", "Briga", 1, "Como o lutador básico (1d6 → 1d8 nv5 → 1d10 nv9 → 2d6 nv13 → 2d8 nv17 → 2d10 nv20)."),
    "ATL_FACANHA_ATLETICA": _h("Atleta", "Façanha Atlética", 1, "Em um teste de perícia, gaste PM (até sua Força) para receber +2 no teste por PM gasto."),
    "ATL_ARREMESSO_ATLETICO": _h("Atleta", "Arremesso Atlético", 2, "Alcance de armas de arremesso sobe em 1 passo e usa o dano de Briga. A partir do 10º nível, conta como ataque desarmado para habilidades de lutador."),
    "ATL_PODERIO_MUSCULAR": _h("Atleta", "Poderio Muscular", 2, "Aprende e pode lançar Primor Atlético apenas em si mesmo (magia simulada).", {"magias_conhecidas": ["Primor Atlético"], "magia_simulada": True}),
    "ATL_CASCA_GROSSA": _h("Atleta", "Casca Grossa", 3, "Sem armadura pesada, soma Con na Defesa (+1 no 7º, 12º, 15º e 19º níveis).", {"defesa_soma_atributo": {"atributo": "con", "sem_armadura_pesada": True}, "casca_grossa_escala": {"inicio": 7, "cada": 4, "bonus": 1}}),
    "ATL_MAIS_ALTO_MAIS_RAPIDO": _h("Atleta", "Mais Alto e Mais Rápido", 5, "Deslocamento +3m; deslocamento de escalada e natação igual à metade do deslocamento normal (+nível de atleta em rodadas prendendo respiração).", {"deslocamento_bonus": 3}),
    "ATL_DISCIPLINA_ATLETICA": _h("Atleta", "Disciplina Atlética", 9, "Ao falhar em um teste de resistência, gaste 2 PM para rolar novamente usando Atletismo.", custo_pm=2),
    "ATL_CORPO_IDEAL": _h("Atleta", "Corpo Ideal", 20, "Imune a cansaço, metabolismo e veneno, RD 10 e dano desarmado/arremesso sobe para 2d10.", {"imunidade": ["Cansaço", "Metabolismo", "Veneno"], "resistencia_rd": {"geral": 10}}),

    # ── 3. BURGUÊS (Nobre, Tabela 1-5, p. 25–27) ──
    "BUR_MEIOS_PRODUCAO": _h("Burguês", "Meios de Produção", 1, "Início de cada aventura recebe T$ 100 em dinheiro/itens mundanos/poções (T$ 300 veterano, T$ 600 campeão, T$ 1.000 lenda)."),
    "BUR_ORGULHO": _h("Burguês", "Orgulho", 1, "Como o nobre básico: gaste PM (até Carisma) para +2 por PM em teste de perícia."),
    "BUR_PODER_MONETARIO": _h("Burguês", "Poder Monetário", 1, "Ao usar habilidade com custo em PM, pode consumir TO (até Carisma) para pagar 1 PM por TO (limite diário = nível; 2× nível a partir do 5º)."),
    "BUR_DESMORALIZAR": _h("Burguês", "Desmoralizar", 2, "Aprende e lança Perdição como magia simulada (círculos como clérigo; apenas criaturas inteligentes; mental).", {"magias_conhecidas": ["Perdição"], "atributo_magia_fixo": "car", "magia_simulada": True}),
    "BUR_NEGOCIANTE_NATO": _h("Burguês", "Negociante Nato", 3, "Gaste 1 dia na comunidade + Diplomacia CD 20: vende itens por 60% (+10% a cada 10 acima da CD, máx. 100%)."),
    "BUR_SUBORNO": _h("Burguês", "Suborno", 4, "Aprende e lança Enfeitiçar (Car, magia simulada); +2 na CD se pagar ao menos 1 TO pelo custo.", {"magias_conhecidas": ["Enfeitiçar"], "atributo_magia_fixo": "car", "magia_simulada": True}),
    "BUR_OSTENTACAO": _h("Burguês", "Ostentação", 5, "Pode vestir +1 item vestido adicional. +1 CD de habilidades de burguês por item banhado a ouro, cravejado de gemas ou de mitral (máx. +3).", {"itens_vestidos_bonus": 1}),
    "BUR_NOVO_RICO": _h("Burguês", "Novo Rico", 9, "+1 PM por nível de poder de cada item mágico vestido (após 1 dia de uso)."),
    "BUR_MAGNATA": _h("Burguês", "Magnata", 20, "Desmoralizar também reduz CD dos alvos; consumir TO para pagar PM concede 10 PV temporários cumulativos pela cena."),

    # ── 4. DUELISTA (Bucaneiro, Tabela 1-6, p. 27–29) ──
    "DUE_DUELO": _h("Duelista", "Duelo", 1, "Gaste 2 PM: +2 ataque e dano contra 1 oponente em alcance curto pela cena (+1 PM por +1 a cada 5 níveis).", custo_pm=2),
    "DUE_INSOLENCIA": _h("Duelista", "Insolência", 1, "Sem armadura pesada, soma Carisma na Defesa (limitado pelo nível).", {"defesa_soma_atributo": {"atributo": "car", "limite_por_nivel": True, "sem_armadura_pesada": True}}),
    "DUE_ESCOLA_DUELO": _h("Duelista", "Escola de Duelo", 2, "Escolha permanente: Escola Ambidestra (+2 Def e Reflexos com 2 armas sendo 1 leve), Escola Clássica (+2 dano com 1 arma e mão livre) ou Escola de Tiro (proficiência armas de fogo leves/1 mão)."),
    "DUE_ESQUIVA_SAGAZ": _h("Duelista", "Esquiva Sagaz", 3, "+1 na Defesa e Reflexos (+1 a cada 4 níveis; exige liberdade de movimento).", {"defesa_bonus": 1, "bonus_pericia": {"Reflexos": 1}, "exige_liberdade_movimento": True, "escala_nivel": {"inicio": 3, "cada": 4, "bonus": 1, "classe": "Duelista"}}),
    "DUE_TRUQUES_CAPA": _h("Duelista", "Truques de Capa", 4, "Usando capa esvoaçante, gaste 2 PM para Capa Inoportuna, Distração Oportuna (+5 Ref/Von), Efeito Dramático (+5 Car), Impulso (+9m desl, +5 Acr/Atl), Paraquedas (-6d6 queda) ou Rasgar a Capa (metade dano).", custo_pm=2),
    "DUE_TECNICA_AVANCADA": _h("Duelista", "Técnica Avançada", 10, "Aprimora sua Escola de Duelo (Ambidestra: contra-ataque 1 PM; Clássica: dano +5 e ataque extra em crítico; Tiro: +1 passo dano e +1 alcance)."),
    "DUE_DUELISTA_LENDARIO": _h("Duelista", "Duelista Lendário", 20, "Usando sua escola, gaste 1 PM para rerrolar seu ataque ou forçar oponente a rerrolar ataque contra você.", custo_pm=1),

    # ── 5. ERMITÃO (Druida, Tabela 1-7, p. 29–30) ──
    "ERM_DEVOTO_FIEL": _h("Ermitão", "Devoto Fiel", 1, "Como o druida básico (Allihanna, Megalokk ou Oceano; 2 poderes concedidos)."),
    "ERM_EMPATIA_SELVAGEM": _h("Ermitão", "Empatia Selvagem", 1, "Como o druida básico, mas também se comunica com plantas não inteligentes e espíritos."),
    "ERM_MAGIAS": _h("Ermitão", "Magias", 1, "Como o druida básico (1º círculo nv1, 2º nv6, 3º nv10, 4º nv14; atributo-chave Sabedoria)."),
    "ERM_SITIO_SAGRADO": _h("Ermitão", "Sítio Sagrado", 3, "Área erma de 5 km (conta como base básica com custo reduzido à metade). Escolha um terreno associado (soma Sab em Furtividade, Percepção, Misticismo, Religião e Sobrevivência; +1 terreno ou +2 bônus no 7º e a cada 4 níveis)."),
    "ERM_VINCULO_TERRA": _h("Ermitão", "Vínculo com a Terra", 5, "Em terreno associado ao sítio sagrado, magias custam -1 PM (-2 PM dentro do próprio sítio)."),
    "ERM_TEMPERADO_CLIMA": _h("Ermitão", "Temperado pelo Clima", 11, "Recebe RD 5 contra o tipo de dano correspondente a cada terreno associado ao seu sítio sagrado."),
    "ERM_EIXO_PEDRAS": _h("Ermitão", "Eixo de Pedras", 20, "1×/aventura armazena magias somando nível + Sab PM; em terreno associado, descarrega 1/rodada como ação livre sem custo."),

    # ── 6. INOVADOR (Guerreiro, Tabela 1-8, p. 30–31) ──
    "INO_DO_BOM_MELHOR": _h("Inovador", "Do Bom e do Melhor", 1, "Começa com arma, armadura ou escudo superior de até T$ 500; porém é não proficiente com equipamentos que não sejam superiores ou mágicos."),
    "INO_SEQUENCIA_ESPECIAL": _h("Inovador", "Sequência Especial", 1, "Gaste 2 PM: +1 cumulativo em ataque e dano (máx. +2; +2 máx. a cada 4 níveis por +1 PM) a cada ataque com arma ainda não usada na sequência.", custo_pm=2),
    "INO_BOMBARDEIO_SEQUENCIAL": _h("Inovador", "Bombardeio Sequencial", 2, "Pode usar Sequência Especial com itens alquímicos ou poções (aplica o bônus na CD)."),
    "INO_ACROBACIA_DEFENSIVA": _h("Inovador", "Acrobacia Defensiva", 3, "Quando sofre dano, gaste 2 PM para fazer teste de Acrobacia e subtrair o resultado do dano.", custo_pm=2),
    "INO_DOMINIO_EXCENTRICO": _h("Inovador", "Domínio Excêntrico", 4, "Após 1 semana carregando arma exótica ou de fogo superior/mágica, recebe proficiência nela."),
    "INO_TECNICA_REVOLUCIONARIA": _h("Inovador", "Técnica Revolucionária", 7, "Gaste 2 PM para conceder adaptável, ágil, alongada, dupla ou versátil às armas empunhadas pelo combate.", custo_pm=2),
    "INO_ESTILO_UNICO": _h("Inovador", "Estilo Único", 20, "Escolha 2 poderes de guerreiro ou combate que possua: ignora todos os requisitos e restrições de armas para esses poderes."),

    # ── 7. MACHADO DE PEDRA (Bárbaro, Tabela 1-9, p. 32–33) ──
    "MDP_FURIA": _h("Machado de Pedra", "Fúria", 1, "Como o bárbaro básico (+2/+3/+4/+5 ataque e dano por 2 PM).", custo_pm=2),
    "MDP_GRUNHIDOS": _h("Machado de Pedra", "Grunhidos", 1, "Conhece apenas o idioma rústico de sua tribo + 1 palavra em valkar por nível de machado de pedra."),
    "MDP_MACHADO_PEDRA": _h("Machado de Pedra", "Machado de Pedra", 1, "Sem proficiência em armas simples; sabe usar adaga, azagaia, clava, funda, lança, machadinha e tacape (+1 arma simples/marcial no 9º). +1 ataque e dano com essas armas, armas naturais ou desarmado."),
    "MDP_TANGA_PELES": _h("Machado de Pedra", "Tanga de Peles", 1, "Sem armaduras leves; sem armadura soma Con na Defesa e ganha +1 Defesa no 3º e a cada 4 níveis (+1 nv3, +2 nv7, +3 nv11, +4 nv15, +5 nv19).", {"defesa_soma_atributo": {"atributo": "con", "sem_armadura": True}}),
    "MDP_TANGA_PELES_ESCALA": _h("Machado de Pedra", "Tanga de Peles (Defesa)", 3, "Bônus escalável de Defesa sem armadura (+1 no 3º e a cada 4 níveis).", {"defesa_bonus": 1, "escala_nivel": {"inicio": 3, "cada": 4, "bonus": 1, "classe": "Machado de Pedra"}}),
    "MDP_FURIA_PRIMITIVA": _h("Machado de Pedra", "Fúria Primitiva", 2, "Sem armadura e com arma de Machado de Pedra, Fúria custa -1 PM; 1×/cena ao entrar em fúria ganha nível + Con PV temporários."),
    "MDP_INSTINTO_SELVAGEM": _h("Machado de Pedra", "Instinto Selvagem", 3, "Como o bárbaro básico (+1 dano e Percepção no 3º, +2 no 9º, +3 no 15º).", {"bonus_pericia": {"Percepção": 1}, "escala_nivel": {"inicio": 3, "cada": 6, "bonus": 1, "classe": "Machado de Pedra"}}),
    "MDP_RESILIENCIA_PRIMAL": _h("Machado de Pedra", "Resiliência Primal", 5, "Recebe RD 3 no 5º nível (+3 a cada 3 níveis, máx. RD 15 no 17º).", {"rd_fixa": 3, "rd_max": 15, "escala_nivel": {"cada": 3, "bonus": 3}}),
    "MDP_FURIA_RUSTICA": _h("Machado de Pedra", "Fúria Rústica", 20, "Ao entrar em fúria, gaste 5 PM para ganhar Cura Acelerada 10 (cumulativa) e 1 ataque desarmado extra ao agredir.", custo_pm=5),

    # ── 8. MAGIMARCIALISTA (Bardo, Tabela 1-10, p. 33–34) ──
    "MAG_CADENCIA": _h("Magimarcialista", "Cadência Magimarcial", 1, "Lançar magia de bardo gera 1 carga arcana; agredir gera 1 carga marcial (máx. de cada = Carisma; dura até o fim da cena)."),
    "MAG_MAGIAS": _h("Magimarcialista", "Magias", 1, "Como o bardo básico (1º círculo nv1, 2º nv6, 3º nv10, 4º nv14; atributo-chave Carisma)."),
    "MAG_MAGIFICACAO": _h("Magimarcialista", "Magificação", 1, "Com ao menos 1 carga arcana e 1 marcial, recebe +2 ataque e dano (+1 a cada 5 níveis) e conta como sob Inspiração."),
    "MAG_BRAVADO": _h("Magimarcialista", "Bravado Magimarcial", 2, "Gaste 1 carga marcial ao lançar magia (-1 PM) ou 1 carga arcana ao atacar (+1d6 dano)."),
    "MAG_DANCA_DEFENSIVA": _h("Magimarcialista", "Dança Defensiva", 3, "Gaste 1 carga marcial (+5 em TR) ou 1 carga arcana (RD 10 contra dano recebido)."),
    "MAG_ARTE_SUBLIME": _h("Magimarcialista", "Arte Sublime", 7, "Pode gastar 1 carga adicional em Bravado Magimarcial ou Dança Defensiva para dobrar o efeito."),
    "MAG_CRESCENDO_VITORIOSO": _h("Magimarcialista", "Crescendo Vitorioso", 20, "Inicia cada combate com 1 carga arcana e 1 marcial; soma cargas marciais na CD de bardo e cargas arcanas em ataque e dano."),

    # ── 9. NECROMANTE (Arcanista, Tabela 1-11, p. 34–37) ──
    "NEC_CAMINHO": _h("Necromante", "Caminho do Necromante", 1, "Aprende magias de necromancia divinas como arcanas; não aprende encantamento; ≥50% das magias devem ser necromancia. Ativa conexão com a morte gastando PV = círculo máximo desejado pela cena. Atributo-chave: Inteligência."),
    "NEC_FALAR_MORTOS": _h("Necromante", "Falar com Mortos", 1, "Usa Misticismo com mortos-vivos para mudar atitude/persuasão. Nv 3+: 1 PM e ação padrão para falar com cadáver (Voz Divina)."),
    "NEC_MAGIAS": _h("Necromante", "Magias", 1, "Como o arcanista básico (1º círculo nv1, 2º nv5, 3º nv9, 4º nv13, 5º nv17; atributo-chave Inteligência)."),
    "NEC_ANIMAR_CADAVER": _h("Necromante", "Animar Cadáver", 2, "Ação completa e 3 PM: anima cadáver como parceiro iniciante (6 PM veterano nv7, 9 PM mestre nv11; não conta no limite, máx. 1; sacrifica para reduzir dano à metade).", custo_pm=3),
    "NEC_NECROLOGIA": _h("Necromante", "Necrologia", 3, "Recebe +2 em Cura, Fortitude e CD de magias de necromancia (+1 a cada 5 níveis: +3 nv8, +4 nv13, +5 nv18).", {"bonus_pericia": {"Cura": 2, "Fortitude": 2}, "escala_nivel": {"inicio": 3, "cada": 5, "bonus": 1, "classe": "Necromante"}}),
    "NEC_DISTORCAO_NECROTICA": _h("Necromante", "Distorção Necrótica", 4, "Escolha 1 magia conhecida de 1º círculo: sua escola muda para necromancia."),
    "NEC_NECROPOTENCIA": _h("Necromante", "Necropotência", 5, "Ao dobrar o gasto de PV da conexão com a morte, reduzir inimigos vivos a 0 PV com necromancia concede 2 PM temporários (máx. nível/cena)."),
    "NEC_DOMINIO_MORTE": _h("Necromante", "Domínio Sobre a Morte", 20, "Custo em PM de magias de necromancia reduzido à metade; ao matar vivo com necromancia, 2 PM para erguer como Servo Morto-Vivo sem componente."),
    "NEC_RITUAL_LICH": _h(
        "Necromante",
        "Ritual do Lich",
        0,
        "Você aprendeu o Ritual do Lich (p. 36): Filactério (T$ 20.000), Poção do Sono Eterno (CD 35) e transformação em Lich (+1 Int/Sab/Car, -1 Con, Morto-Vivo, +5 Defesa, RD 10/mágico, Aura de Medo, Toque Gélido 6d6+6 frio).",
        efeitos={"ritual_lich": True},
        tipo="Poder de Arcanista",
        requisitos=["Celebrar Ritual", "Escrever Pergaminho", "Preparar Poção", "17º nível de necromante"],
    ),

    # ── 10. SANTO (Paladino, Tabela 1-12, p. 37–38) ──
    "SAN_ABENCOADO": _h("Santo", "Abençoado", 1, "Como o paladino básico (soma Carisma nos PM; não pode ser santo do bem sem divindade)."),
    "SAN_CODIGO_HEROI": _h("Santo", "Código do Herói", 1, "Como o paladino básico."),
    "SAN_LADAINHA_COMBATE": _h("Santo", "Ladainha de Combate", 1, "Ação padrão e 2 PM (sustentada): aura 9m dá +1 ataque, dano e Defesa (+1 a cada 4 níveis por +2 PM; conta como Aura Sagrada). Nv 5: +1d8 luz vs malignos. Nv 9: armas recebem encanto veloz.", custo_pm=2),
    "SAN_SANTO_CURANDEIRO": _h("Santo", "Santo Curandeiro", 2, "Ação de movimento + PM (até Car): aliado mais ferido em alcance médio recupera 2d8 PV/PM por luz (nv 6+: remove 1 condição)."),
    "SAN_VASO_ESPIRITO": _h("Santo", "Vaso do Espírito", 3, "Ao fazer teste de resistência, gaste 1 PM para somar seu Carisma.", custo_pm=1),
    "SAN_MARTIR": _h("Santo", "Mártir", 6, "Gaste 1 PM para dar seu Carisma no TR de aliado em alcance médio (nv 12+: 1×/cena pode sofrer o efeito no lugar dele).", custo_pm=1),
    "SAN_PIRA_SANTA": _h("Santo", "Pira Santa", 8, "Sob Ladainha, ação de movimento + PM (até Car): inimigo de maior ND em alcance médio sofre 2d8 luz/PM e fica ofuscado (Fort CD Car reduz à metade)."),
    "SAN_VINGADOR_SANTIFICADO": _h("Santo", "Vingador Santificado", 20, "Na Ladainha, gaste +5 PM para dobrar bônus numéricos e conceder imunidade a críticos + RD 5 + Carisma na aura.", custo_pm=5),

    # ── 11. SETEIRO (Caçador, Tabela 1-13, p. 38–40) ──
    "SET_CAMINHO_ATIRADOR": _h("Seteiro", "Caminho do Atirador", 1, "Suas habilidades de seteiro relacionadas a ataques e armas só funcionam com arcos e bestas."),
    "SET_MARCA_PRESA": _h("Seteiro", "Marca da Presa", 1, "Como o caçador básico (+1d4 nv1, +1d8 nv5, +1d12 nv9, +2d8 nv13, +2d10 nv17).", custo_pm=1),
    "SET_TIRO_SUPRESSAO": _h("Seteiro", "Tiro de Supressão", 1, "Causar dano com arco/besta em alvo de Marca da Presa impõe -1 cumulativo em rolagens de dano (até os PM gastos em Marca da Presa)."),
    "SET_EVASAO": _h("Seteiro", "Evasão", 3, "Como ladino/caçador: 0 dano ao passar em Reflexos (sem armadura pesada ou imóvel)."),
    "SET_DISPARO_CONSTRITOR": _h("Seteiro", "Disparo Constritor", 5, "Ao mirar, pague 2 PM para executar desarmar, empurrar ou quebrar com ataque à distância no turno.", custo_pm=2),
    "SET_RAJADA_FLECHAS": _h("Seteiro", "Rajada de Flechas", 10, "Ação completa e 2 PM: ataca todos os inimigos em raio 3m de um ponto (1 munição; +2 dano cumulativo por acerto).", custo_pm=2),
    "SET_EVASAO_APRIMORADA": _h("Seteiro", "Evasão Aprimorada", 13, "0 dano ao passar em Reflexos e metade se falhar (sem armadura pesada ou imóvel)."),
    "SET_SENTINELA": _h("Seteiro", "Sentinela", 15, "1×/rodada, quando alvo de Marca da Presa acerta aliado, gaste 1 PM para atacá-lo.", custo_pm=1),
    "SET_MESTRE_DISPARO": _h("Seteiro", "Mestre do Disparo", 20, "Marca da Presa como ação livre e 1 ataque extra/rodada com arco/besta contra alvo marcado."),

    # ── 12. USURPADOR (Clérigo, Tabela 1-14, p. 40–41) ──
    "USU_INIMIGO_DEUSES": _h("Usurpador", "Inimigo dos Deuses", 1, "Não pode ter nenhuma devoção."),
    "USU_MAGIAS": _h("Usurpador", "Magias", 1, "Lança magias divinas (1º círculo nv1, 2º nv5, 3º nv9, 4º nv13, 5º nv17; atributo-chave Carisma; soma Car nos PM)."),
    "USU_USURPAR": _h("Usurpador", "Usurpar", 1, "Pode lançar qualquer magia divina de círculo acessível passando em Enganação CD 15 + PM (sem escolher 10; sofre PA; -5 perto de símbolo sagrado)."),
    "USU_CANALIZACAO_FALSA": _h("Usurpador", "Canalização Falsa", 2, "Pode canalizar tanto energia positiva quanto negativa."),
    "USU_DISCRICAO_DIVINA": _h("Usurpador", "Discrição Divina", 3, "Recebe +1 em Furtividade e testes de resistência (+2 no 9º, +3 no 15º).", {"bonus_pericia": {"Furtividade": 1, "Fortitude": 1, "Reflexos": 1, "Vontade": 1}, "escala_nivel": {"inicio": 3, "cada": 6, "bonus": 1, "classe": "Usurpador"}}),
    "USU_PODER_CAPTURADO": _h("Usurpador", "Poder Capturado", 4, "1 hora + Enganação CD 20 (+5/uso extra no dia): rouba 1 poder concedido de um deus maior por nível até o fim do dia sem O&R (falha perde 3 PM)."),
    "USU_ROUBO_DIVINO": _h("Usurpador", "Roubo Divino", 20, "Ao usar Usurpar, -1 PM e +1 CD a cada 10 pontos no teste de Enganação."),

    # ── 13. VASSALO (Cavaleiro, Tabela 1-15, p. 41–43) ──
    "VAS_BALUARTE": _h("Vassalo", "Baluarte", 1, "Como o cavaleiro básico (+2/+4/+6/+8/+10 Defesa e TR).", custo_pm=1),
    "VAS_CODIGO_HONRA": _h("Vassalo", "Código de Honra", 1, "Como o cavaleiro básico."),
    "VAS_JOVEM_PAJEM": _h("Vassalo", "Jovem Pajem", 1, "Torna-se treinado em Adestramento ou Ofício (armeiro) (+2 se já for treinado)."),
    "VAS_SUSERANO": _h("Vassalo", "Suserano", 1, "Serve a um nobre: +5 Diplomacia e Intimidação com vassalos inferiores e alojamento/alimentação nas terras dele."),
    "VAS_VALETE": _h("Vassalo", "Valete", 2, "Torna-se treinado em Diplomacia ou Nobreza e recebe 1 poder de cavaleiro."),
    "VAS_ESCUDEIRO_APRENDIZ": _h("Vassalo", "Escudeiro Aprendiz", 3, "Torna-se treinado em Cavalgar e recebe proficiência com armaduras pesadas (+2 Defesa com pesada se já tinha).", {"pericia_treino": ["Cavalgar"], "proficiencia_add": ["Armaduras pesadas"]}),
    "VAS_GUARDA_CASTELO": _h("Vassalo", "Guarda do Castelo", 4, "Torna-se treinado em Intuição e recebe 1 poder de cavaleiro.", {"pericia_treino": ["Intuição"]}),
    "VAS_VIGILANTE_ESTRADAS": _h("Vassalo", "Vigilante de Estradas", 5, "Recebe Montaria e torna-se treinado em Percepção.", {"pericia_treino": ["Percepção"]}),
    "VAS_CAVALEIRO_REINO": _h("Vassalo", "Cavaleiro do Reino", 6, "Título de sir/dame, item superior com 2 melhorias e 1 poder de cavaleiro."),
    "VAS_SARGENTO_REINO": _h("Vassalo", "Sargento do Reino", 7, "Recebe 1 poder de cavaleiro ou de guerreiro (nível igual ao seu)."),
    "VAS_CAPITAO_REINO": _h("Vassalo", "Capitão do Reino", 8, "Recebe o poder Escudeiro e Golpe Divino (como paladino de mesmo nível, magia simulada)."),
    "VAS_LORDE": _h("Vassalo", "Lorde", 9, "Recebe Autoridade Feudal e escolhe Caminho do Soldado (poder de guerreiro) ou Caminho do Governante (poder de nobre)."),
    "VAS_BARAO": _h("Vassalo", "Barão", 10, "Recebe Título e um domínio de nível 1 (ou 1 construção gratuita)."),
    "VAS_VISCONDE": _h("Vassalo", "Visconde", 11, "Caminho do Soldado: +1 PV por nível de vassalo. Caminho do Governante: +1 em Inteligência."),
    "VAS_CONDE": _h("Vassalo", "Conde", 12, "Orçamento de T$ 30.000 em itens mágicos por aventura + 1 poder de cavaleiro ou geral."),
    "VAS_MARQUES": _h("Vassalo", "Marquês", 13, "Caminho do Soldado: RD 5 e +2 na Defesa. Caminho do Governante: soma Carisma nos testes de resistência."),
    "VAS_DUQUE": _h("Vassalo", "Duque", 14, "Autoridade Feudal sobe 1 passo + 1 poder de cavaleiro."),
    "VAS_ARQUIDUQUE": _h("Vassalo", "Arquiduque", 15, "1×/rodada, quando criatura inteligente causar dano, gaste 5 PM para reduzir o dano a 0.", custo_pm=5),
    "VAS_CONSELHEIRO_REAL": _h("Vassalo", "Conselheiro Real", 16, "Recebe 1 poder de cavaleiro e aprende 1 magia divina de até 4º círculo (Car)."),
    "VAS_REI_MERCENARIO": _h("Vassalo", "Rei Mercenário", 17, "Recebe 3 pontos de atributo para distribuir em For/Des/Con (Soldado) ou Int/Sab/Car (Governante)."),
    "VAS_REI": _h("Vassalo", "Rei", 18, "Recebe +1 em Carisma e 1 poder de cavaleiro.", {"atributo_bonus": {"car": 1}}),
    "VAS_ALTO_REI": _h("Vassalo", "Alto Rei", 19, "Orçamento de itens mágicos sobe para T$ 100.000 e limite de parceiros aumenta em +2."),
    "VAS_IMPERADOR": _h("Vassalo", "Imperador", 20, "Recebe +1 em dois atributos diferentes e aprende 1 magia divina de até 5º círculo (Car)."),

    # ── 14. VENTANISTA (Ladino, Tabela 1-16, p. 44–45) ──
    "VEN_CHARME": _h("Ventanista", "Charme", 1, "Soma Carisma no total de PM. Em testes de perícia (exceto ataques), gaste PM (até Carisma) para +2 por PM."),
    "VEN_TRUQUES_OFICIO": _h("Ventanista", "Truques do Ofício", 1, "Lança magias arcanas simuladas de encantamento e ilusão (1º nv1, 2º nv6, 3º nv10, 4º nv14; começa com 2 e +1 por nível par; veste armadura leve sem teste; atributo-chave Inteligência)."),
    "VEN_EVASAO": _h("Ventanista", "Evasão", 2, "Como o ladino básico."),
    "VEN_DISFARCE_ELABORADO": _h("Ventanista", "Disfarce Elaborado", 3, "Ao se disfarçar, assume -3 PM para usar 1 poder relacionado ao disfarce (exceto Tormenta); +1 poder por -3 PM no 9º e 15º níveis."),
    "VEN_ESQUIVA_SOBRENATURAL": _h("Ventanista", "Esquiva Sobrenatural", 4, "Como o ladino básico: nunca fica surpreendido."),
    "VEN_VIRAR_CASACA": _h("Ventanista", "Virar a Casaca", 7, "Disfarçado, gaste 1 PM para remover o disfarce e esconder-se usando Enganação no lugar de Furtividade mesmo sem camuflagem.", custo_pm=1),
    "VEN_OLHOS_COSTAS": _h("Ventanista", "Olhos nas Costas", 8, "Como o ladino básico: não pode ser flanqueado."),
    "VEN_EVASAO_APRIMORADA": _h("Ventanista", "Evasão Aprimorada", 10, "Como o ladino básico."),
    "VEN_PROVOCACAO_OUSADA": _h("Ventanista", "Provocação Ousada", 11, "1º turno da cena, ação completa: inimigos ganham +2 Percepção/Sobrevivência/Vontade contra você, mas você recupera 2 PM no início de seus turnos (máx. nível/cena)."),
    "VEN_GRANDE_GOLPE": _h("Ventanista", "O Grande Golpe", 20, "Início da aventura escolhe magias (até Int) associadas a tipo de cena; lança sem gastar PM (limite 20 PM, Int, magia simulada)."),
}


def validar_multiclasse_variante(nomes_classes) -> Dict[str, Any]:
    """Valida a regra oficial (p. 22): não é possível fazer multiclasse entre uma
    classe básica e uma de suas variantes (ambas são a mesma classe).
    """
    vistos: Dict[str, str] = {}
    for nome in (nomes_classes or []):
        n = (nome or "").strip()
        if not n:
            continue
        base = MAPA_VARIANTE_PARA_BASE.get(n, n)
        if base in vistos and vistos[base] != n:
            return {
                "valido": False,
                "motivo": f"Não é permitido multiclasse entre {vistos[base]} e {n} (ambas pertencem à classe {base}).",
            }
        vistos[base] = n
    return {"valido": True, "motivo": ""}
