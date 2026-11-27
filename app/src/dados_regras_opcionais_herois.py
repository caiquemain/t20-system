"""Catálogo oficial de Regras Opcionais — Heróis de Arton (Capítulo 4, p. 280–328).

Todas as regras deste módulo são estritamente opt-in por ficha (ativadas via
`ficha.regras_opcionais_ativas`, `ficha.complicacoes` ou `ficha.papel_grupo`).
Nenhuma regra opcional altera personagens comuns se não for habilitada.
"""
from typing import Dict, Any, List
from .dados_suplementos import FONTE_HEROIS


# =====================================================================
# 1. LISTA DE REGRAS OPCIONAIS & ESTILOS DE JOGO (p. 328)
# =====================================================================

LISTA_REGRAS_OPCIONAIS: Dict[str, Dict[str, Any]] = {
    # Regras Mais Soltas (p. 280-281)
    "racas_abertas": {
        "id": "racas_abertas",
        "nome": "Raças Abertas",
        "categoria": "Criação",
        "pagina": 281,
        "automatizada": True,
        "descricao": "Aplica os modificadores de atributo raciais livremente (máximo +1 por atributo).",
        "fonte": FONTE_HEROIS,
    },
    "devocoes_abertas": {
        "id": "devocoes_abertas",
        "nome": "Devoções Abertas",
        "categoria": "Criação",
        "pagina": 281,
        "automatizada": True,
        "descricao": "Permite ser devoto de qualquer divindade, independente de raça ou classe.",
        "fonte": FONTE_HEROIS,
    },
    # Complicações (p. 282-287)
    "complicacoes": {
        "id": "complicacoes",
        "nome": "Complicações",
        "categoria": "Criação",
        "pagina": 282,
        "automatizada": True,
        "descricao": "Permite escolher até 1 complicação na criação em troca de +1 poder geral bônus.",
        "fonte": FONTE_HEROIS,
    },
    "superacao": {
        "id": "superacao",
        "nome": "Superação",
        "categoria": "Criação",
        "pagina": 287,
        "automatizada": False,
        "descricao": "A partir do patamar Campeão (nível 11+), permite superar uma complicação pagando T$ 100 por nível e treinamento.",
        "fonte": FONTE_HEROIS,
    },
    # Idades Variadas (p. 288-291)
    "idades_variadas": {
        "id": "idades_variadas",
        "nome": "Idades Variadas",
        "categoria": "Criação",
        "pagina": 288,
        "automatizada": True,
        "descricao": "Substitui a tabela básica de envelhecimento por 7 faixas etárias (Criança a Ancião) com complicações de idade.",
        "fonte": FONTE_HEROIS,
    },
    # Objetivos Heroicos & Papéis no Grupo (p. 292-295)
    "objetivos_heroicos": {
        "id": "objetivos_heroicos",
        "nome": "Objetivos Heroicos",
        "categoria": "Campanha",
        "pagina": 292,
        "automatizada": True,
        "descricao": "Define um objetivo pessoal heroico com benefício ativo, penalidade e recompensa permanente ao concluir.",
        "fonte": FONTE_HEROIS,
    },
    "papeis_no_grupo": {
        "id": "papeis_no_grupo",
        "nome": "Papéis no Grupo",
        "categoria": "Campanha",
        "pagina": 294,
        "automatizada": True,
        "descricao": "Concede um pequeno benefício mecânico (+1 PM ou +1 em uma perícia) ligado à função do jogador na mesa.",
        "fonte": FONTE_HEROIS,
    },
    # Combate Avançado (p. 296-304)
    "acoes_rapidas": {
        "id": "acoes_rapidas",
        "nome": "Ações Rápidas",
        "categoria": "Combate",
        "pagina": 296,
        "automatizada": False,
        "descricao": "Permite converter ações de movimento/padrão em ações rápidas em situações específicas.",
        "fonte": FONTE_HEROIS,
    },
    "armas_leves_e_ageis": {
        "id": "armas_leves_e_ageis",
        "nome": "Armas Leves e Ágeis",
        "categoria": "Combate",
        "pagina": 296,
        "automatizada": False,
        "descricao": "Ajusta a interação entre armas leves/ágeis e Destreza em combate.",
        "fonte": FONTE_HEROIS,
    },
    "ataques_de_oportunidade": {
        "id": "ataques_de_oportunidade",
        "nome": "Ataques de Oportunidade",
        "categoria": "Combate",
        "pagina": 296,
        "automatizada": False,
        "descricao": "Permite reações de ataque quando inimigos deixam áreas ameaçadas ou realizam ações distraídas.",
        "fonte": FONTE_HEROIS,
    },
    "ataques_mirados": {
        "id": "ataques_mirados",
        "nome": "Ataques Mirados",
        "categoria": "Combate",
        "pagina": 297,
        "automatizada": False,
        "descricao": "Permite mirar partes específicas do alvo (-5 membros, -10 cabeça) para impor efeitos adicionais.",
        "fonte": FONTE_HEROIS,
    },
    "cobertura_leve_e_efeitos": {
        "id": "cobertura_leve_e_efeitos",
        "nome": "Cobertura Leve e Efeitos",
        "categoria": "Combate",
        "pagina": 297,
        "automatizada": False,
        "descricao": "Cobertura leve também concede +5 em testes de Reflexos contra efeitos de área.",
        "fonte": FONTE_HEROIS,
    },
    "defesa_epica": {
        "id": "defesa_epica",
        "nome": "Defesa Épica",
        "categoria": "Combate",
        "pagina": 297,
        "automatizada": True,
        "descricao": "Personagens recebem +1 na Defesa por nível par (metade do nível, arredondado para baixo).",
        "fonte": FONTE_HEROIS,
    },
    "desafiando_a_morte": {
        "id": "desafiando_a_morte",
        "nome": "Desafiando a Morte",
        "categoria": "Combate",
        "pagina": 298,
        "automatizada": False,
        "descricao": "Permite continuar agindo mesmo com PV negativos sob risco de agravar ferimentos.",
        "fonte": FONTE_HEROIS,
    },
    "efeitos_criticos": {
        "id": "efeitos_criticos",
        "nome": "Efeitos Críticos",
        "categoria": "Combate",
        "pagina": 298,
        "automatizada": False,
        "descricao": "Acertos críticos também geram efeitos extras conforme localização e tipo de dano (Tabelas 4-3 e 4-4).",
        "fonte": FONTE_HEROIS,
    },
    "escalando_criaturas": {
        "id": "escalando_criaturas",
        "nome": "Escalando Criaturas",
        "categoria": "Combate",
        "pagina": 299,
        "automatizada": False,
        "descricao": "Regras para escalar criaturas duas ou mais categorias de tamanho maiores.",
        "fonte": FONTE_HEROIS,
    },
    "falhas_criticas": {
        "id": "falhas_criticas",
        "nome": "Falhas Críticas",
        "categoria": "Combate",
        "pagina": 300,
        "automatizada": False,
        "descricao": "Resultados naturais 1 em ataques podem gerar consequências adicionais (Tabela 4-6, d100).",
        "fonte": FONTE_HEROIS,
    },
    "morte_alternativa": {
        "id": "morte_alternativa",
        "nome": "Morte Alternativa",
        "categoria": "Combate",
        "pagina": 302,
        "automatizada": True,
        "descricao": "Substitui morte imediata por Testes de Morte (Tabela 4-5), Lesões (-2 em perícias) e Ferimentos Permanentes.",
        "fonte": FONTE_HEROIS,
    },
    "lancinante_revisado": {
        "id": "lancinante_revisado",
        "nome": "Lancinante Revisado",
        "categoria": "Combate",
        "pagina": 303,
        "automatizada": True,
        "descricao": "Encanto Lancinante causa +1 dado extra de dano da arma por multiplicador em vez de multiplicar bônus fixos.",
        "fonte": FONTE_HEROIS,
    },
    "mais_armas_ageis": {
        "id": "mais_armas_ageis",
        "nome": "Mais Armas Ágeis",
        "categoria": "Combate",
        "pagina": 303,
        "automatizada": True,
        "descricao": "Azagaia (corpo a corpo), bordão e lança também contam como armas ágeis.",
        "fonte": FONTE_HEROIS,
    },
    "movimento_intercalado": {
        "id": "movimento_intercalado",
        "nome": "Movimento Intercalado",
        "categoria": "Combate",
        "pagina": 303,
        "automatizada": False,
        "descricao": "Permite dividir o deslocamento antes e depois de uma ação padrão.",
        "fonte": FONTE_HEROIS,
    },
    "posicionamento": {
        "id": "posicionamento",
        "nome": "Posicionamento",
        "categoria": "Combate",
        "pagina": 304,
        "automatizada": False,
        "descricao": "Regras táticas adicionais de flanqueamento, terreno elevado e linha de visão.",
        "fonte": FONTE_HEROIS,
    },
    "rd_combinada": {
        "id": "rd_combinada",
        "nome": "RD Combinada",
        "categoria": "Combate",
        "pagina": 304,
        "automatizada": True,
        "descricao": "Redução de dano de armadura e escudo se acumulam.",
        "fonte": FONTE_HEROIS,
    },
    "saque_rapido_limitado": {
        "id": "saque_rapido_limitado",
        "nome": "Saque Rápido Limitado",
        "categoria": "Combate",
        "pagina": 304,
        "automatizada": False,
        "descricao": "Limita o número de itens que podem ser sacados ou guardados como ação livre por rodada.",
        "fonte": FONTE_HEROIS,
    },
    # Culinária Avançada, Exploração e Domínios (p. 305-327)
    "culinaria_avancada": {
        "id": "culinaria_avancada",
        "nome": "Culinária Avançada",
        "categoria": "Exploração",
        "pagina": 305,
        "automatizada": False,
        "descricao": "Sistema de ingredientes, pratos especiais, tempero especial e poderes culinários.",
        "fonte": FONTE_HEROIS,
    },
    "exploracao_masmorras": {
        "id": "exploracao_masmorras",
        "nome": "Exploração de Masmorras",
        "categoria": "Exploração",
        "pagina": 310,
        "automatizada": False,
        "descricao": "Controle de encontros aleatórios por barulho (d8/d6/d4/d3), luz/escuridão e cenas em 6 segmentos.",
        "fonte": FONTE_HEROIS,
    },
    "dominios": {
        "id": "dominios",
        "nome": "Domínios",
        "categoria": "Campanha",
        "pagina": 314,
        "automatizada": True,
        "descricao": "Gestão de terras, cortes, conselheiros, construções, unidades militares, impostos e domínios místicos.",
        "fonte": FONTE_HEROIS,
    },
}

ESTILOS_DE_JOGO: Dict[str, Dict[str, Any]] = {
    "Tática": {
        "nome": "Tática",
        "descricao": "Foco em combate estratégico, posicionamento e gestão de recursos.",
        "regras_sugeridas": [
            "ataques_de_oportunidade",
            "ataques_mirados",
            "cobertura_leve_e_efeitos",
            "movimento_intercalado",
            "posicionamento",
            "saque_rapido_limitado",
        ],
        "fonte": FONTE_HEROIS,
    },
    "Épica": {
        "nome": "Épica",
        "descricao": "Personagens mais heroicos, resistentes e grandiosos em campanhas de alta fantasia.",
        "regras_sugeridas": [
            "complicacoes",
            "defesa_epica",
            "desafiando_a_morte",
            "objetivos_heroicos",
            "papeis_no_grupo",
            "rd_combinada",
            "dominios",
        ],
        "fonte": FONTE_HEROIS,
    },
    "Velha Guarda": {
        "nome": "Velha Guarda",
        "descricao": "Campanhas mais letais e focadas em exploração de masmorras clássica.",
        "regras_sugeridas": [
            "efeitos_criticos",
            "falhas_criticas",
            "morte_alternativa",
            "exploracao_masmorras",
            "culinaria_avancada",
        ],
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 2. REGRAS MAIS SOLTAS — MÉTODOS DE GERAÇÃO DE ATRIBUTOS (p. 280–281)
# =====================================================================

METODOS_GERACAO_ATRIBUTOS: Dict[str, Dict[str, Any]] = {
    "Clássica": {
        "nome": "Clássica",
        "formula": "3d6",
        "descricao": "Role 3d6 seis vezes e converta cada total para o modificador correspondente na tabela padrão.",
        "fonte": FONTE_HEROIS,
    },
    "Épica": {
        "nome": "Épica",
        "formula": "3d6+6 (descarta menor)",
        "descricao": "Role 3d6+6 descartando o menor dado de cada conjunto para atributos acima da média.",
        "fonte": FONTE_HEROIS,
    },
    "Valkaria": {
        "nome": "Valkaria",
        "formula": "Base 8 + 7d6 inteiros (máx. +4)",
        "descricao": "Comece com base 8 em todos os atributos e distribua os resultados inteiros de 7d6 (máximo +4 por atributo).",
        "fonte": FONTE_HEROIS,
    },
    "Khalmyr": {
        "nome": "Khalmyr",
        "valores_fixos": [3, 3, 2, 1, 0, -1],
        "descricao": "Distribua o conjunto fixo de modificadores: +3, +3, +2, +1, 0 e -1.",
        "fonte": FONTE_HEROIS,
    },
    "Nimb": {
        "nome": "Nimb",
        "formula": "7d20 (descarta menor)",
        "descricao": "Role 7d20 e descarte o menor (1–3 → -3; 18–19 → +4; 20 → +5).",
        "fonte": FONTE_HEROIS,
    },
    "Pontos Variados": {
        "nome": "Pontos Variados",
        "opcoes_pontos": [5, 10, 15],
        "descricao": "Compra de pontos padrão ajustada para 5 pontos (campanhas mundanas) ou 15 pontos (campanhas épicas).",
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 3. COMPLICAÇÕES (Tabela 4-1, p. 282–287)
# =====================================================================

DADOS_COMPLICACOES_GERAIS: Dict[str, Dict[str, Any]] = {
    "Amaldiçoado": {
        "nome": "Amaldiçoado",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você carrega uma maldição que traz infortúnios recorrentes em momentos críticos.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Apetitoso": {
        "nome": "Apetitoso",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Monstros e predadores sentem um cheiro irresistível em você e tendem a escolhê-lo como alvo prioritário.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Assombrado": {
        "nome": "Assombrado",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Espíritos inquietos perturbam sua mente e podem atrapalhar suas ações.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Cabeça Quente": {
        "nome": "Cabeça Quente",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você perde a calma facilmente sob provocação ou dano, reagindo de forma intempestiva.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Caolho": {
        "nome": "Caolho",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você perdeu a visão de um olho. Sofre -2 em Iniciativa, Percepção, Pontaria e Reflexos.",
        "efeitos": {
            "bonus_pericia": {
                "Iniciativa": -2,
                "Percepção": -2,
                "Pontaria": -2,
                "Reflexos": -2,
            }
        },
        "fonte": FONTE_HEROIS,
    },
    "Chato": {
        "nome": "Chato",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Sua companhia é difícil de suportar. Sofre -5 em Diplomacia.",
        "efeitos": {"bonus_pericia": {"Diplomacia": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Combalido": {
        "nome": "Combalido",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Sua saúde é frágil. Sofre -5 em Fortitude e -1 PV por nível.",
        "efeitos": {"bonus_pericia": {"Fortitude": -5}, "pv_max_nivel": -1},
        "fonte": FONTE_HEROIS,
    },
    "Covarde": {
        "nome": "Covarde",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você entra em pânico facilmente. Sofre -5 em testes de resistência contra efeitos de medo.",
        "efeitos": {"penalidade_tr_medo": -5},
        "fonte": FONTE_HEROIS,
    },
    "Cria de Nimb": {
        "nome": "Cria de Nimb",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Seu comportamento caótico e errático impõe -5 em perícias baseadas em Carisma.",
        "efeitos": {"bonus_pericia_atributo": {"car": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Criado na Cidade": {
        "nome": "Criado na Cidade",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você não está acostumado aos ermos. Sofre -5 em Sobrevivência.",
        "efeitos": {"bonus_pericia": {"Sobrevivência": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Crise de Fé": {
        "nome": "Crise de Fé",
        "tipo": "Geral",
        "comportamental": True,
        "descricao": "Sua fé vacila (†). Sofre -2 em Vontade e precisa respeitar restrições comportamentais ligadas à sua dúvida espiritual.",
        "efeitos": {"bonus_pericia": {"Vontade": -2}},
        "fonte": FONTE_HEROIS,
    },
    "Desprotegido": {
        "nome": "Desprotegido",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você se expõe ao perigo. Sofre -2 na Defesa e em testes de resistência (Fortitude, Reflexos e Vontade).",
        "efeitos": {
            "defesa_bonus": -2,
            "bonus_pericia": {"Fortitude": -2, "Reflexos": -2, "Vontade": -2},
        },
        "fonte": FONTE_HEROIS,
    },
    "Distraído": {
        "nome": "Distraído",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você vive com a cabeça nas nuvens. Sofre -5 em Iniciativa e Percepção.",
        "efeitos": {"bonus_pericia": {"Iniciativa": -5, "Percepção": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Emotivo": {
        "nome": "Emotivo",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Suas emoções à flor da pele tornam você mais vulnerável a efeitos mentais e sociais.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Expurgo de Wynna": {
        "nome": "Expurgo de Wynna",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "A magia rejeita você. Sofre -5 em testes de resistência contra magias.",
        "efeitos": {"resistencia_magia_bonus": -5},
        "fonte": FONTE_HEROIS,
    },
    "Fracote": {
        "nome": "Fracote",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Sua compleição é permanentemente debilitada: você está permanentemente sob a condição fraco.",
        "efeitos": {"condicao_permanente": "fraco"},
        "fonte": FONTE_HEROIS,
    },
    "Hedonista": {
        "nome": "Hedonista",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você busca conforto e prazer acima de tudo, sofrendo penalidades quando privado de luxos ou descanso confortável.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Ímpio": {
        "nome": "Ímpio",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você atrai a desaprovação divina. Sofre -5 em testes de resistência contra efeitos divinos.",
        "efeitos": {"penalidade_tr_divinas": -5},
        "fonte": FONTE_HEROIS,
    },
    "Impulsivo": {
        "nome": "Impulsivo",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você age antes de pensar. Sofre -5 em Furtividade e Investigação.",
        "efeitos": {"bonus_pericia": {"Furtividade": -5, "Investigação": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Inculto": {
        "nome": "Inculto",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você teve pouca educação formal. Recebe 2 perícias treinadas a menos na criação.",
        "efeitos": {"pericias_treinadas_bonus": -2},
        "fonte": FONTE_HEROIS,
    },
    "Indolente": {
        "nome": "Indolente",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você é preguiçoso e lento para reagir. Sofre -5 em Reflexos e -3m em seu deslocamento.",
        "efeitos": {"bonus_pericia": {"Reflexos": -5}, "deslocamento_bonus": -3},
        "fonte": FONTE_HEROIS,
    },
    "Ingênuo": {
        "nome": "Ingênuo",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você confia demais nos outros. Sofre -5 em Enganação, Intuição, Investigação e Ladinagem.",
        "efeitos": {
            "bonus_pericia": {
                "Enganação": -5,
                "Intuição": -5,
                "Investigação": -5,
                "Ladinagem": -5,
            }
        },
        "fonte": FONTE_HEROIS,
    },
    "Maneta": {
        "nome": "Maneta",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você perdeu uma mão ou braço, não podendo empunhar armas de duas mãos ou dois objetos simultaneamente.",
        "efeitos": {"maos_disponiveis": 1},
        "fonte": FONTE_HEROIS,
    },
    "Marcado pelo Passado": {
        "nome": "Marcado pelo Passado",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Traumas antigos drenam sua energia e afastam as pessoas. Sofre -5 em Diplomacia e -1 PM por nível.",
        "efeitos": {"bonus_pericia": {"Diplomacia": -5}, "pm_max_nivel": -1},
        "fonte": FONTE_HEROIS,
    },
    "Matugo": {
        "nome": "Matugo",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você cresceu isolado e desconhece costumes urbanos, tecnologia e etiqueta.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Míope": {
        "nome": "Míope",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você tem dificuldade para enxergar à distância. Sofre -5 em Percepção e Pontaria.",
        "efeitos": {"bonus_pericia": {"Percepção": -5, "Pontaria": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Mouco": {
        "nome": "Mouco",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Sua audição é bastante prejudicada. Sofre -2 em Iniciativa, Intuição, Percepção e Reflexos.",
        "efeitos": {
            "bonus_pericia": {
                "Iniciativa": -2,
                "Intuição": -2,
                "Percepção": -2,
                "Reflexos": -2,
            }
        },
        "fonte": FONTE_HEROIS,
    },
    "Paladar Infantil": {
        "nome": "Paladar Infantil",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você recusa comidas elaboradas ou estranhas, restringindo benefícios de alimentação especial.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Paranoico": {
        "nome": "Paranoico",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você desconfia de tudo e de todos, dificultando descanso e cooperação.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Temeroso": {
        "nome": "Temeroso",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você evita confronto direto. Sofre -5 em Luta.",
        "efeitos": {"bonus_pericia": {"Luta": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Tolo": {
        "nome": "Tolo",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Você é facilmente enganado ou dominado. Sofre -5 em Intuição e Vontade.",
        "efeitos": {"bonus_pericia": {"Intuição": -5, "Vontade": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Vagaroso": {
        "nome": "Vagaroso",
        "tipo": "Geral",
        "comportamental": False,
        "descricao": "Seus movimentos são permanentemente arrastados: você está permanentemente sob a condição lento.",
        "efeitos": {"condicao_permanente": "lento"},
        "fonte": FONTE_HEROIS,
    },
}

DADOS_COMPLICACOES_CLASSE: Dict[str, Dict[str, Any]] = {
    # Arcanista (4)
    "Arcanista de Rotina": {
        "nome": "Arcanista de Rotina",
        "tipo": "Classe",
        "classe": "Arcanista",
        "comportamental": False,
        "descricao": "Você depende de rotinas rígidas para conjurar suas magias arcanas.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Foco Exigente": {
        "nome": "Foco Exigente",
        "tipo": "Classe",
        "classe": "Arcanista",
        "subclasse": "Bruxo",
        "comportamental": False,
        "descricao": "Seu foco arcano de bruxo exige cuidados especiais e impõe restrições severas caso seja perdido ou avariado.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Linhagem Prepotente": {
        "nome": "Linhagem Prepotente",
        "tipo": "Classe",
        "classe": "Arcanista",
        "subclasse": "Feiticeiro",
        "comportamental": False,
        "descricao": "Seu sangue mágico se manifesta de modo arrogante ou difícil de conter.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Mente Cansada": {
        "nome": "Mente Cansada",
        "tipo": "Classe",
        "classe": "Arcanista",
        "subclasse": "Mago",
        "comportamental": False,
        "descricao": "O estudo constante sobrecarrega sua memória, limitando sua preparação de magias.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Bárbaro (2)
    "De Peito Aberto": {
        "nome": "De Peito Aberto",
        "tipo": "Classe",
        "classe": "Bárbaro",
        "comportamental": True,
        "descricao": "Você despreza armaduras e se recusa a vesti-las em combate (†).",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Totem Gigante": {
        "nome": "Totem Gigante",
        "tipo": "Classe",
        "classe": "Bárbaro",
        "comportamental": True,
        "descricao": "Você carrega um totem colossal (10 espaços) que impõe -5 de penalidade de armadura (†).",
        "efeitos": {"penalidade_armadura": -5, "carga_extra": 10},
        "fonte": FONTE_HEROIS,
    },
    # Bardo (2)
    "Estrelismo": {
        "nome": "Estrelismo",
        "tipo": "Classe",
        "classe": "Bardo",
        "comportamental": False,
        "descricao": "Seu ego artístico atrapalha relações sinceras. Sofre -5 em Diplomacia e Intuição.",
        "efeitos": {"bonus_pericia": {"Diplomacia": -5, "Intuição": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Falastrão": {
        "nome": "Falastrão",
        "tipo": "Classe",
        "classe": "Bardo",
        "comportamental": False,
        "descricao": "Você não consegue ficar quieto nem manter a compostura. Sofre -5 em Furtividade e Nobreza.",
        "efeitos": {"bonus_pericia": {"Furtividade": -5, "Nobreza": -5}},
        "fonte": FONTE_HEROIS,
    },
    # Bucaneiro (2)
    "Coragem Líquida": {
        "nome": "Coragem Líquida",
        "tipo": "Classe",
        "classe": "Bucaneiro",
        "comportamental": False,
        "descricao": "Você precisa de bebida para manter sua audácia e bravatas em dia.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Esbanjador": {
        "nome": "Esbanjador",
        "tipo": "Classe",
        "classe": "Bucaneiro",
        "comportamental": False,
        "descricao": "Você gasta suas riquezas sem pensar no amanhã assim que chega a uma cidade.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Caçador (1)
    "Limitado a (Criatura)": {
        "nome": "Limitado a (Criatura)",
        "tipo": "Classe",
        "classe": "Caçador",
        "comportamental": False,
        "descricao": "Seu treinamento de caça é especializado demais em um único tipo de criatura.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Cavaleiro (1)
    "Superprotetor": {
        "nome": "Superprotetor",
        "tipo": "Classe",
        "classe": "Cavaleiro",
        "comportamental": False,
        "descricao": "Você se coloca em risco excessivo para proteger aliados e inocentes.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Clérigo (2)
    "Divindade Exigente": {
        "nome": "Divindade Exigente",
        "tipo": "Classe",
        "classe": "Clérigo",
        "comportamental": False,
        "descricao": "Sua divindade cobra obrigações e restrições ainda mais rigorosas de você.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Preparação Litúrgica": {
        "nome": "Preparação Litúrgica",
        "tipo": "Classe",
        "classe": "Clérigo",
        "comportamental": False,
        "descricao": "Você precisa realizar longos rituais litúrgicos para preparar suas magias divinas.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Druida (1)
    "Tosco": {
        "nome": "Tosco",
        "tipo": "Classe",
        "classe": "Druida",
        "comportamental": True,
        "descricao": "Você rejeita confortos e modos civilizados (†).",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Guerreiro (1)
    "Precavido": {
        "nome": "Precavido",
        "tipo": "Classe",
        "classe": "Guerreiro",
        "comportamental": False,
        "descricao": "Sua cautela excessiva o torna mais hesitante. Sofre -2 em testes de ataque e testes de resistência.",
        "efeitos": {
            "bonus_pericia": {
                "Luta": -2,
                "Pontaria": -2,
                "Fortitude": -2,
                "Reflexos": -2,
                "Vontade": -2,
            }
        },
        "fonte": FONTE_HEROIS,
    },
    # Inventor (1)
    "Trabalhador Ocupado": {
        "nome": "Trabalhador Ocupado",
        "tipo": "Classe",
        "classe": "Inventor",
        "comportamental": False,
        "descricao": "Seus projetos consomem tempo extra e dificultam fabricações apressadas.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Ladino (1)
    "Honra de Ladrão": {
        "nome": "Honra de Ladrão",
        "tipo": "Classe",
        "classe": "Ladino",
        "comportamental": True,
        "descricao": "Você segue um código estrito de conduta entre ladinos e jamais trai certos princípios (†).",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Lutador (1)
    "Firula": {
        "nome": "Firula",
        "tipo": "Classe",
        "classe": "Lutador",
        "comportamental": True,
        "descricao": "Você faz questão de exibir estilo e acrobacias chamativas durante a luta (†).",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Nobre (2)
    "Filantropo": {
        "nome": "Filantropo",
        "tipo": "Classe",
        "classe": "Nobre",
        "comportamental": False,
        "descricao": "Você doa grande parte dos seus recursos e tesouros para causas e necessitados.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Mimado": {
        "nome": "Mimado",
        "tipo": "Classe",
        "classe": "Nobre",
        "comportamental": False,
        "descricao": "Você não tolera privações nem trabalhos braçais indignos da sua posição.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    # Paladino (1)
    "Certinho": {
        "nome": "Certinho",
        "tipo": "Classe",
        "classe": "Paladino",
        "comportamental": False,
        "descricao": "Você leva as regras e a moralidade ao pé da letra, mesmo quando isso complica a missão.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
}

DADOS_COMPLICACOES_IDADE: Dict[str, Dict[str, Any]] = {
    "Abatido": {
        "nome": "Abatido",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "O peso dos anos reduziu sua vitalidade. Você sofre -2 PV por nível.",
        "efeitos": {"pv_max_nivel": -2},
        "fonte": FONTE_HEROIS,
    },
    "Catarata": {
        "nome": "Catarata",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Sua visão está enevoada pela idade. Sofre -5 em Percepção e Pontaria.",
        "efeitos": {"bonus_pericia": {"Percepção": -5, "Pontaria": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Dedos Trêmulos": {
        "nome": "Dedos Trêmulos",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Suas mãos não têm mais a firmeza de outrora. Sofre -2 em Luta e Pontaria.",
        "efeitos": {"bonus_pericia": {"Luta": -2, "Pontaria": -2}},
        "fonte": FONTE_HEROIS,
    },
    "Definhamento": {
        "nome": "Definhamento",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Seu vigor físico enfraqueceu. Sofre -5 em Fortitude e em testes de manobras de combate.",
        "efeitos": {"bonus_pericia": {"Fortitude": -5}, "penalidade_manobras": -5},
        "fonte": FONTE_HEROIS,
    },
    "Desatento": {
        "nome": "Desatento",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Sua atenção oscila com frequência, facilitando ser surpreendido.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    '"Devagar, Jovem!"': {
        "nome": '"Devagar, Jovem!"',
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Suas pernas já não acompanham o ritmo dos mais jovens. Seu deslocamento diminui em -3m.",
        "efeitos": {"deslocamento_bonus": -3},
        "fonte": FONTE_HEROIS,
    },
    "Gota": {
        "nome": "Gota",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Crises dolorosas nas articulações limitam esforços físicos prolongados.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Juntas Duras": {
        "nome": "Juntas Duras",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Sua agilidade foi afetada pela rigidez articular. Sofre -5 em Acrobacia e Reflexos.",
        "efeitos": {"bonus_pericia": {"Acrobacia": -5, "Reflexos": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Melancólico": {
        "nome": "Melancólico",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "A nostalgia drena sua energia espiritual. Você sofre -1 PM por nível.",
        "efeitos": {"pm_max_nivel": -1},
        "fonte": FONTE_HEROIS,
    },
    "Memórias Tristes": {
        "nome": "Memórias Tristes",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Lembranças dolorosas de perdas passadas ressurgem em momentos tensos.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    '"No Meu Tempo..."': {
        "nome": '"No Meu Tempo..."',
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Você se apega demais ao passado. Sofre -5 em Intuição e Vontade.",
        "efeitos": {"bonus_pericia": {"Intuição": -5, "Vontade": -5}},
        "fonte": FONTE_HEROIS,
    },
    "Pulmão Ruim": {
        "nome": "Pulmão Ruim",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Você perde o fôlego com facilidade sob esforço físico intenso.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Rabugento": {
        "nome": "Rabugento",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Seu mau humor afasta os outros. Sofre -5 em perícias baseadas em Carisma (exceto Intimidação).",
        "efeitos": {
            "bonus_pericia": {
                "Atuação": -5,
                "Diplomacia": -5,
                "Enganação": -5,
                "Jogatina": -5,
            }
        },
        "fonte": FONTE_HEROIS,
    },
    "Recurvado": {
        "nome": "Recurvado",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Sua postura encurvada reduz sua capacidade de carga e resistência física.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Sono Ruim": {
        "nome": "Sono Ruim",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Você tem dificuldade para dormir bem, prejudicando a recuperação em descansos.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Teimoso": {
        "nome": "Teimoso",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Você se recusa a mudar de ideia ou aceitar ajuda facilmente.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Tosse": {
        "nome": "Tosse",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Crises de tosse podem denunciar sua posição ou atrapalhar sua concentração.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
    "Turrão": {
        "nome": "Turrão",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Você não aplica metade do seu nível em testes de perícias nas quais não seja treinado.",
        "efeitos": {"sem_metade_nivel_nao_treinadas": True},
        "fonte": FONTE_HEROIS,
    },
    "Velha Ferida": {
        "nome": "Velha Ferida",
        "tipo": "Idade",
        "comportamental": False,
        "descricao": "Uma lesão antiga volta a doer em combates difíceis ou mudanças de tempo.",
        "efeitos": {},
        "fonte": FONTE_HEROIS,
    },
}

DADOS_COMPLICACOES: Dict[str, Dict[str, Any]] = {
    **DADOS_COMPLICACOES_GERAIS,
    **DADOS_COMPLICACOES_CLASSE,
    **DADOS_COMPLICACOES_IDADE,
}


# =====================================================================
# 4. IDADES VARIADAS (Tabela 4-2, p. 288–291)
# =====================================================================

DADOS_IDADES_VARIADAS: Dict[str, Dict[str, Any]] = {
    "Criança": {
        "nome": "Criança",
        "faixa_humana": "9–12 anos",
        "idade_min": 9,
        "idade_max": 12,
        "mod_atributos": {"forca": -2, "constituicao": -1, "sabedoria": -1},
        "niveis_extras": 0,
        "complicacoes_idade": 0,
        "tamanho_delta": -1,
        "sem_origem": True,
        "bloqueia_aumento_fisico": False,
        "habilidades_especiais": [
            {
                "nome": "Protegido dos Deuses",
                "descricao": "Você recebe +2 na Defesa e +5 em testes de resistência (Fortitude, Reflexos e Vontade).",
                "efeitos": {
                    "defesa_bonus": 2,
                    "bonus_pericia": {"Fortitude": 5, "Reflexos": 5, "Vontade": 5},
                },
            }
        ],
        "fonte": FONTE_HEROIS,
    },
    "Adolescente": {
        "nome": "Adolescente",
        "faixa_humana": "13–17 anos",
        "idade_min": 13,
        "idade_max": 17,
        "mod_atributos": {"sabedoria": -1},
        "niveis_extras": 0,
        "complicacoes_idade": 0,
        "tamanho_delta": 0,
        "origem_em_construcao": True,
        "bloqueia_aumento_fisico": False,
        "habilidades_especiais": [
            {
                "nome": "Ímpeto Juvenil",
                "descricao": "Você recebe +3 PM.",
                "efeitos": {"pm_max_ini": 3},
            }
        ],
        "fonte": FONTE_HEROIS,
    },
    "Jovem": {
        "nome": "Jovem",
        "faixa_humana": "18–24 anos",
        "idade_min": 18,
        "idade_max": 24,
        "mod_atributos": {},
        "niveis_extras": 0,
        "complicacoes_idade": 0,
        "tamanho_delta": 0,
        "bloqueia_aumento_fisico": False,
        "habilidades_especiais": [],
        "fonte": FONTE_HEROIS,
    },
    "Adulto": {
        "nome": "Adulto",
        "faixa_humana": "25–39 anos",
        "idade_min": 25,
        "idade_max": 39,
        "mod_atributos": {},
        "niveis_extras": 0,
        "poder_geral_opcional": 1,
        "complicacoes_idade": 1,
        "tamanho_delta": 0,
        "bloqueia_aumento_fisico": False,
        "habilidades_especiais": [],
        "fonte": FONTE_HEROIS,
    },
    "Maduro": {
        "nome": "Maduro",
        "faixa_humana": "40–59 anos",
        "idade_min": 40,
        "idade_max": 59,
        "mod_atributos": {},
        "niveis_extras": 1,
        "complicacoes_idade": 2,
        "tamanho_delta": 0,
        "bloqueia_aumento_fisico": False,
        "habilidades_especiais": [],
        "fonte": FONTE_HEROIS,
    },
    "Velho": {
        "nome": "Velho",
        "faixa_humana": "60–79 anos",
        "idade_min": 60,
        "idade_max": 79,
        "mod_atributos": {"forca": -1, "destreza": -1, "constituicao": -1},
        "niveis_extras": 2,
        "complicacoes_idade": 3,
        "tamanho_delta": 0,
        "bloqueia_aumento_fisico": True,
        "habilidades_especiais": [],
        "fonte": FONTE_HEROIS,
    },
    "Ancião": {
        "nome": "Ancião",
        "faixa_humana": "80+ anos",
        "idade_min": 80,
        "idade_max": None,
        "mod_atributos": {"forca": -2, "destreza": -2, "constituicao": -2},
        "niveis_extras": 3,
        "complicacoes_idade": 4,
        "tamanho_delta": 0,
        "bloqueia_aumento_fisico": True,
        "habilidades_especiais": [],
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 5. OBJETIVOS HEROICOS (p. 292–293)
# =====================================================================

DADOS_OBJETIVOS_HEROICOS: Dict[str, Dict[str, Any]] = {
    "Desafio": {
        "nome": "Desafio",
        "descricao": "Superar um rival formidável, monstro lendário ou provação extrema.",
        "fonte": FONTE_HEROIS,
    },
    "Descoberta": {
        "nome": "Descoberta",
        "descricao": "Desvendar um segredo perdido, explorar terras desconhecidas ou revelar uma verdade oculta.",
        "fonte": FONTE_HEROIS,
    },
    "Liderança": {
        "nome": "Liderança",
        "descricao": "Conquistar autoridade, unir um povo ou fundar uma ordem/domínio.",
        "fonte": FONTE_HEROIS,
    },
    "Obra": {
        "nome": "Obra",
        "descricao": "Criar uma obra-prima, artefato, tratado ou monumento que perdure pelos séculos.",
        "fonte": FONTE_HEROIS,
    },
    "Riqueza": {
        "nome": "Riqueza",
        "descricao": "Acumular fortuna lendária ou recuperar um tesouro perdido.",
        "fonte": FONTE_HEROIS,
    },
    "Salvação": {
        "nome": "Salvação",
        "descricao": "Resgatar alguém importante, curar uma maldição ou impedir uma catástrofe.",
        "fonte": FONTE_HEROIS,
    },
    "Vingança": {
        "nome": "Vingança",
        "descricao": "Fazer justiça ou punir o responsável por uma tragédia do seu passado.",
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 6. PAPÉIS NO GRUPO (p. 294–295)
# =====================================================================

DADOS_PAPEIS_GRUPO: Dict[str, Dict[str, Any]] = {
    "Advogado": {
        "nome": "Advogado",
        "beneficio": "+1 PM",
        "descricao": "Responsável por conhecer e consultar as regras na mesa. Concede +1 PM.",
        "efeitos": {"pm_max_ini": 1},
        "fonte": FONTE_HEROIS,
    },
    "Arquivista": {
        "nome": "Arquivista",
        "beneficio": "+1 em Diplomacia",
        "descricao": "Registra o resumo das sessões e o diário da campanha. Concede +1 em Diplomacia.",
        "efeitos": {"bonus_pericia": {"Diplomacia": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Bibliotecário": {
        "nome": "Bibliotecário",
        "beneficio": "+1 em Conhecimento",
        "descricao": "Cataloga NPCs, locais, lore e pistas da campanha. Concede +1 em Conhecimento.",
        "efeitos": {"bonus_pericia": {"Conhecimento": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Cartógrafo": {
        "nome": "Cartógrafo",
        "beneficio": "+1 em Sobrevivência",
        "descricao": "Desenha e mantém mapas de masmorras e viagens. Concede +1 em Sobrevivência.",
        "efeitos": {"bonus_pericia": {"Sobrevivência": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Enfermeiro": {
        "nome": "Enfermeiro",
        "beneficio": "+1 em Cura",
        "descricao": "Acompanha PV, PM e condições do grupo durante o combate. Concede +1 em Cura.",
        "efeitos": {"bonus_pericia": {"Cura": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Estrategista": {
        "nome": "Estrategista",
        "beneficio": "+1 em Guerra",
        "descricao": "Coordena táticas, posicionamento e planos do grupo. Concede +1 em Guerra.",
        "efeitos": {"bonus_pericia": {"Guerra": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Teratólogo": {
        "nome": "Teratólogo",
        "beneficio": "+1 em Misticismo",
        "descricao": "Anota habilidades, resistências e fraquezas das criaturas enfrentadas. Concede +1 em Misticismo.",
        "efeitos": {"bonus_pericia": {"Misticismo": 1}},
        "fonte": FONTE_HEROIS,
    },
    "Tesoureiro": {
        "nome": "Tesoureiro",
        "beneficio": "+1 em Nobreza ou Ofício",
        "descricao": "Controla tesouros, despesas e partilha do grupo. Concede +1 em Nobreza ou Ofício.",
        "efeitos": {"bonus_pericia": {"Nobreza": 1}},
        "pericias_opcoes": ["Nobreza", "Ofício"],
        "fonte": FONTE_HEROIS,
    },
    "Xerife": {
        "nome": "Xerife",
        "beneficio": "+1 em Iniciativa",
        "descricao": "Controla a ordem de iniciativa, turnos e ritmo da mesa. Concede +1 em Iniciativa.",
        "efeitos": {"bonus_pericia": {"Iniciativa": 1}},
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 7. PODERES GERAIS DE CULINÁRIA AVANÇADA (p. 309)
# =====================================================================

PODERES_CULINARIA_HEROIS: Dict[str, Dict[str, Any]] = {
    "As_da_Cozinha": {
        "nome": "Ás da Cozinha",
        "tipo": "Poder de Destino",
        "requisitos": ["Treinado em Ofício (cozinheiro)", "5º nível de personagem"],
        "descricao": "Você é um mestre da gastronomia aventureira, capaz de preparar pratos especiais com maestria e tempero superior.",
        "efeitos": {"as_da_cozinha": True},
        "fonte": FONTE_HEROIS,
    },
    "Bom_de_Garfo": {
        "nome": "Bom de Garfo",
        "tipo": "Poder de Destino",
        "requisitos": ["Con 1"],
        "descricao": "Você recebe +3 pontos de vida por patamar e pode se beneficiar de até dois pratos especiais por dia.",
        "efeitos": {"pv_por_patamar": 3, "pratos_por_dia": 2},
        "fonte": FONTE_HEROIS,
    },
}


# =====================================================================
# 8. CONSTANTES DE COMBATE AVANÇADO, EXPLORAÇÃO E DOMÍNIOS
# =====================================================================

ARMAS_AGEIS_EXTRA_HEROIS = {"Azagaia", "Bordão", "Lança"}

EXPLORACAO_MASMORRAS_BARULHO: Dict[str, str] = {
    "silencioso": "1d8",
    "normal": "1d6",
    "barulhento": "1d4",
    "muito_barulhento": "1d3",
}

DOMINIOS_CORTES: List[str] = ["Inexistente", "Pobre", "Comum", "Rica"]
DOMINIOS_POPULARIDADES: List[str] = ["Odiado", "Impopular", "Tolerado", "Popular", "Adorado"]
DOMINIOS_CONSELHEIROS: List[str] = [
    "Almirante",
    "Arquimago",
    "Chanceler",
    "Espião-Mestre",
    "General",
    "Marechal",
    "Sumo-Sacerdote",
    "Tesoureiro",
    "Xerife",
]


def obter_catalogo_regras_opcionais() -> Dict[str, Any]:
    """Retorna o catálogo estruturado completo de Regras Opcionais (Heróis de Arton Cap. 4)."""
    return {
        "fonte": FONTE_HEROIS,
        "regras": LISTA_REGRAS_OPCIONAIS,
        "estilos_de_jogo": ESTILOS_DE_JOGO,
        "metodos_geracao_atributos": METODOS_GERACAO_ATRIBUTOS,
        "complicacoes_gerais": DADOS_COMPLICACOES_GERAIS,
        "complicacoes_classe": DADOS_COMPLICACOES_CLASSE,
        "complicacoes_idade": DADOS_COMPLICACOES_IDADE,
        "idades_variadas": DADOS_IDADES_VARIADAS,
        "objetivos_heroicos": DADOS_OBJETIVOS_HEROICOS,
        "papeis_grupo": DADOS_PAPEIS_GRUPO,
        "poderes_culinaria": PODERES_CULINARIA_HEROIS,
        "armas_ageis_extra": sorted(ARMAS_AGEIS_EXTRA_HEROIS),
        "exploracao_masmorras": {
            "segmentos_por_cena": 6,
            "dados_barulho": EXPLORACAO_MASMORRAS_BARULHO,
        },
        "dominios": {
            "cortes": DOMINIOS_CORTES,
            "popularidades": DOMINIOS_POPULARIDADES,
            "conselheiros": DOMINIOS_CONSELHEIROS,
            "formula_pm_mistico": "nivel ** 2",
        },
    }
