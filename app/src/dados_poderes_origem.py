# -*- coding: utf-8 -*-
# app/src/dados_poderes_origem.py
# Poderes exclusivos das 35 Origens do Livro Básico (T20 JdA p.85-95)

DADOS_PODERES_ORIGEM = {
    "Membro_Igreja_Acolito": {
        "nome": "Membro da Igreja",
        "tipo": "Origem (Acólito)",
        "descricao": "Você consegue hospedagem confortável e informação em qualquer templo de sua divindade, para você e seus aliados.",
        "fonte": "T20 JdA",
        "efeitos": {"beneficio_social": "hospedagem_informacao_templo"},
    },
    "Amigo_Especial_AmigoAnimais": {
        "nome": "Amigo Especial",
        "tipo": "Origem (Amigo dos Animais)",
        "descricao": "Você recebe +5 em testes de Adestramento com animais. Além disso, possui um animal de estimação que o auxilia e o acompanha em suas aventuras (parceiro que fornece +2 em uma perícia a sua escolha, exceto Luta ou Pontaria, sem contar no limite de parceiros).",
        "fonte": "T20 JdA",
        "efeitos": {
            "bonus_pericia": {"Adestramento": 5},
            "pericia_escolha_bonus": {"valor": 2, "excluir": ["Luta", "Pontaria"]},
            "parceiro_nao_conta_limite": True,
        },
    },
    "Lembrancas_Graduais_Amnesico": {
        "nome": "Lembranças Graduais",
        "tipo": "Origem (Amnésico)",
        "descricao": "Durante suas aventuras, em determinados momentos a critério do mestre, você pode fazer um teste de Sabedoria (CD 10) para reconhecer pessoas, criaturas ou lugares que tenha encontrado antes de perder a memória.",
        "fonte": "T20 JdA",
        "efeitos": {"teste_lembranca_sab_cd": 10},
    },
    "Sangue_Azul_Aristocrata": {
        "nome": "Sangue Azul",
        "tipo": "Origem (Aristocrata)",
        "descricao": "Você tem alguma influência política, suficiente para ser tratado com mais leniência pela guarda, conseguir uma audiência com o nobre local etc.",
        "fonte": "T20 JdA",
        "efeitos": {"beneficio_social": "influencia_politica"},
    },
    "Frutos_Trabalho_Artesao": {
        "nome": "Frutos do Trabalho",
        "tipo": "Origem (Artesão)",
        "descricao": "No início de cada aventura, você recebe até 5 itens gerais que possa fabricar num valor total de até T$ 50. Esse valor aumenta para T$ 100 no patamar veterano, T$ 300 no campeão e T$ 500 no lenda.",
        "fonte": "T20 JdA",
        "efeitos": {
            "itens_inicio_aventura": {
                "max_itens": 5,
                "valor_por_patamar": {
                    "iniciante": 50,
                    "veterano": 100,
                    "campeao": 300,
                    "lenda": 500,
                },
            }
        },
    },
    "Dom_Artistico_Artista": {
        "nome": "Dom Artístico",
        "tipo": "Origem (Artista)",
        "descricao": "Você recebe +2 em testes de Atuação, e recebe o dobro de tibares em apresentações.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia": {"Atuação": 2}, "dobro_tibares_apresentacao": True},
    },
    "Esse_Cheiro_AssistenteLab": {
        "nome": "Esse Cheiro...",
        "tipo": "Origem (Assistente de Laboratório)",
        "descricao": "Você recebe +2 em Fortitude e detecta automaticamente a presença (mas não a localização ou natureza) de itens alquímicos em alcance curto.",
        "fonte": "T20 JdA",
        "efeitos": {
            "bonus_pericia": {"Fortitude": 2},
            "detecta_alquimicos_alcance": "Curto",
        },
    },
    "A_Prova_Tudo_Batedor": {
        "nome": "À Prova de Tudo",
        "tipo": "Origem (Batedor)",
        "descricao": "Você não sofre penalidade em deslocamento e Sobrevivência por clima ruim e por terreno difícil natural.",
        "fonte": "T20 JdA",
        "efeitos": {
            "ignora_terreno_dificil": ["natural"],
            "ignora_penalidade_clima_ruim": True,
        },
    },
    "Confissao_Capanga": {
        "nome": "Confissão",
        "tipo": "Origem (Capanga)",
        "descricao": "Você pode usar Intimidação para interrogar sem custo e em um minuto (veja Investigação).",
        "fonte": "T20 JdA",
        "efeitos": {"interrogar_com_pericia": "Intimidação", "interrogar_tempo": "1 minuto", "interrogar_sem_custo": True},
    },
    "Alpinista_Social_Charlatao": {
        "nome": "Alpinista Social",
        "tipo": "Origem (Charlatão)",
        "descricao": "Você pode substituir testes de Diplomacia por testes de Enganação.",
        "fonte": "T20 JdA",
        "efeitos": {"substitui_pericia": {"Diplomacia": "Enganação"}},
    },
    "Truque_Magica_Circense": {
        "nome": "Truque de Mágica",
        "tipo": "Origem (Circense)",
        "descricao": "Você pode lançar Explosão de Chamas, Hipnotismo e Queda Suave, mas apenas com o aprimoramento Truque. Esta não é uma habilidade mágica — os efeitos provêm de prestidigitação.",
        "fonte": "T20 JdA",
        "efeitos": {
            "magias_truque": ["Explosão de Chamas", "Hipnotismo", "Queda Suave"],
            "magico": False,
        },
    },
    "Punguista_Criminoso": {
        "nome": "Punguista",
        "tipo": "Origem (Criminoso)",
        "descricao": "Você pode fazer testes de Ladinagem para sustento (como a perícia Ofício), mas em apenas um dia. Se passar, recebe o dobro do dinheiro, mas, se falhar, pode ter problemas com a lei (a critério do mestre).",
        "fonte": "T20 JdA",
        "efeitos": {"sustento_ladinagem_1_dia": True, "sustento_multiplicador": 2},
    },
    "Medico_Campo_Curandeiro": {
        "nome": "Médico de Campo",
        "tipo": "Origem (Curandeiro)",
        "descricao": "Você soma sua Sabedoria aos PV restaurados por suas habilidades e itens mundanos de cura.",
        "fonte": "T20 JdA",
        "efeitos": {"cura_mundana_soma_atributo": "sab"},
    },
    "Busca_Interior_Eremita": {
        "nome": "Busca Interior",
        "tipo": "Origem (Eremita)",
        "descricao": "Quando você e seus companheiros estão diante de um mistério, incapazes de prosseguir, você pode gastar 1 PM para meditar sozinho durante algum tempo e receber uma dica do mestre.",
        "fonte": "T20 JdA",
        "efeitos": {"custo_pm": 1, "dica_mestre": True},
    },
    "Desejo_Liberdade_Escravo": {
        "nome": "Desejo de Liberdade",
        "tipo": "Origem (Escravo)",
        "descricao": "Ninguém voltará a torná-lo um escravo! Você recebe +5 em testes contra a manobra agarrar e efeitos de movimento.",
        "fonte": "T20 JdA",
        "efeitos": {"resistencia_manobra": {"agarrar": 5, "movimento": 5}},
    },
    "Palpite_Fund_Estudioso": {
        "nome": "Palpite Fundamentado",
        "tipo": "Origem (Estudioso)",
        "descricao": "Quando vai fazer um teste de perícia originalmente baseada em Inteligência ou Sabedoria, você pode gastar 2 PM para substituí-la por Conhecimento.",
        "fonte": "T20 JdA",
        "efeitos": {"custo_pm": 2, "substitui_pericias_attr_por": {"atributos": ["int", "sab"], "pericia": "Conhecimento"}},
    },
    "Agua_Feijao_Fazendeiro": {
        "nome": "Água no Feijão",
        "tipo": "Origem (Fazendeiro)",
        "descricao": "Você não sofre a penalidade de –5 e não gasta matéria-prima adicional para fabricar pratos para cinco pessoas.",
        "fonte": "T20 JdA",
        "efeitos": {"cozinhar_5_pessoas_sem_penalidade": True},
    },
    "Cultura_Exotica_Forasteiro": {
        "nome": "Cultura Exótica",
        "tipo": "Origem (Forasteiro)",
        "descricao": "Quando vai fazer um teste de perícia que requer treinamento, você pode gastar 1 PM para ignorar esse requerimento para esse teste.",
        "fonte": "T20 JdA",
        "efeitos": {"custo_pm": 1, "ignora_requisito_treino": True},
    },
    "Pao_Circo_Gladiador": {
        "nome": "Pão e Circo",
        "tipo": "Origem (Gladiador)",
        "descricao": "Por seu treino em combates de exibição, você sabe 'bater sem machucar'. Pode escolher causar dano não letal sem sofrer a penalidade de –5.",
        "fonte": "T20 JdA",
        "efeitos": {"sem_penalidade_nao_letal": True},
    },
    "Detetive_Guarda": {
        "nome": "Detetive",
        "tipo": "Origem (Guarda)",
        "descricao": "Você pode gastar 1 PM para substituir testes de Percepção e Intuição por testes de Investigação até o fim da cena.",
        "fonte": "T20 JdA",
        "efeitos": {"custo_pm": 1, "substitui_pericia_cena": {"Percepção": "Investigação", "Intuição": "Investigação"}},
    },
    "Heranca_Herdeiro": {
        "nome": "Herança",
        "tipo": "Origem (Herdeiro)",
        "descricao": "Você herdou um item de preço de até T$ 1.000. Você pode escolher este poder duas vezes, para um item de até T$ 2.000.",
        "fonte": "T20 JdA",
        "efeitos": {"heranca_item_valor": 1000, "heranca_item_valor_duplo": 2000, "multiplo_max": 2},
    },
    "Coracao_Heroico_HeroiCampones": {
        "nome": "Coração Heroico",
        "tipo": "Origem (Herói Camponês)",
        "descricao": "Você recebe +3 pontos de mana. Quando atinge um novo patamar (no 5º, 11º e 17º níveis), recebe +3 PM.",
        "fonte": "T20 JdA",
        "efeitos": {"pm_por_patamar": 3},
    },
    "Passagem_Navio_Marujo": {
        "nome": "Passagem de Navio",
        "tipo": "Origem (Marujo)",
        "descricao": "Você consegue transporte marítimo para você e seus aliados, sem custos, desde que todos paguem com trabalho (passar em pelo menos um teste de perícia adequado durante a viagem).",
        "fonte": "T20 JdA",
        "efeitos": {"beneficio_social": "transporte_maritimo_trabalho"},
    },
    "Vendedor_Carcaças_Mateiro": {
        "nome": "Vendedor de Carcaças",
        "tipo": "Origem (Mateiro)",
        "descricao": "Você pode extrair recursos de criaturas em um minuto, em vez de uma hora, e recebe +5 no teste.",
        "fonte": "T20 JdA",
        "efeitos": {
            "bonus_pericia_situacional": {
                "Sobrevivência": {"valor": 5, "condicao": "extrair recursos de criaturas"},
            },
            "extracao_criaturas_tempo": "1 minuto",
        },
    },
    "Rede_Contatos_MembroGuilda": {
        "nome": "Rede de Contatos",
        "tipo": "Origem (Membro de Guilda)",
        "descricao": "Graças à influência de sua guilda, você pode usar Diplomacia para interrogar sem custo e em um minuto (veja Investigação).",
        "fonte": "T20 JdA",
        "efeitos": {"interrogar_com_pericia": "Diplomacia", "interrogar_tempo": "1 minuto", "interrogar_sem_custo": True},
    },
    "Negociacao_Mercador": {
        "nome": "Negociação",
        "tipo": "Origem (Mercador)",
        "descricao": "Você pode vender itens 10% mais caro (não cumulativo com barganha).",
        "fonte": "T20 JdA",
        "efeitos": {"venda_itens_bonus_pct": 10},
    },
    "Escavador_Minerador": {
        "nome": "Escavador",
        "tipo": "Origem (Minerador)",
        "descricao": "Você se torna proficiente em picaretas, causa +1 de dano com elas e não é afetado por terreno difícil em masmorras e subterrâneos.",
        "fonte": "T20 JdA",
        "efeitos": {
            "proficiencia_add": ["Picareta"],
            "bonus_dano_arma": {"picareta": 1},
            "ignora_terreno_dificil": ["masmorras", "subterrâneos"],
        },
    },
    "Mochileiro_Nomade": {
        "nome": "Mochileiro",
        "tipo": "Origem (Nômade)",
        "descricao": "Seu limite de carga aumenta em 5 espaços.",
        "fonte": "T20 JdA",
        "efeitos": {"carga_max_bonus": 5},
    },
    "Quebra_Galho_Pivete": {
        "nome": "Quebra-Galho",
        "tipo": "Origem (Pivete)",
        "descricao": "Em cidades ou metrópoles, você pode comprar qualquer item mundano não superior por metade do preço normal. Esses itens não podem ser matérias-primas e não podem ser revendidos.",
        "fonte": "T20 JdA",
        "efeitos": {"compra_mundano_desconto_pct": 50},
    },
    "Estoico_Refugiado": {
        "nome": "Estoico",
        "tipo": "Origem (Refugiado)",
        "descricao": "Sua condição de descanso é uma categoria acima do padrão pela situação (normal em condições ruins, confortável em condições normais e luxuosa em condições confortáveis ou melhores).",
        "fonte": "T20 JdA",
        "efeitos": {"descanso_categoria_bonus": 1},
    },
    "Antigo_Mestre_Seguidor": {
        "nome": "Antigo Mestre",
        "tipo": "Origem (Seguidor)",
        "descricao": "Uma vez por aventura, o herói que você costumava servir surge para ajudá-lo por uma cena. Ele é um parceiro mestre de um tipo a sua escolha (definido ao obter este poder) que não conta em seu limite de aliados.",
        "fonte": "T20 JdA",
        "efeitos": {"parceiro_mestre_1x_aventura": True, "parceiro_nao_conta_limite": True},
    },
    "Vida_Rustica_Selvagem": {
        "nome": "Vida Rústica",
        "tipo": "Origem (Selvagem)",
        "descricao": "Você é imune a efeitos prejudiciais de itens ingeríveis e também consegue descansar nos lugares mais desconfortáveis (mesmo dormindo ao relento, sua recuperação de PV e PM nunca é inferior a seu próprio nível).",
        "fonte": "T20 JdA",
        "efeitos": {
            "imunidade": ["Itens ingeríveis prejudiciais"],
            "imunidade_ingesta": True,
            "recuperacao_minima_nivel": True,
        },
    },
    "Influencia_Militar_Soldado": {
        "nome": "Influência Militar",
        "tipo": "Origem (Soldado)",
        "descricao": "Onde houver acampamentos ou bases militares, você pode conseguir hospedagem e informações para você e seus aliados.",
        "fonte": "T20 JdA",
        "efeitos": {"beneficio_social": "hospedagem_informacao_militar"},
    },
    "Gororoba_Taverneiro": {
        "nome": "Gororoba",
        "tipo": "Origem (Taverneiro)",
        "descricao": "Você não sofre a penalidade de –5 para fabricar um prato especial adicional.",
        "fonte": "T20 JdA",
        "efeitos": {"prato_especial_adicional_sem_penalidade": True},
    },
    "Esforcado_Trabalhador": {
        "nome": "Esforçado",
        "tipo": "Origem (Trabalhador)",
        "descricao": "Você recebe um bônus de +2 em todos os testes de perícias estendidos (incluindo perigos complexos).",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia_estendida": 2},
    },
}

from .dados_origens_atlas import DADOS_PODERES_ORIGEM_ATLAS
from .dados_origens_herois import DADOS_PODERES_ORIGEM_HEROIS

DADOS_PODERES_ORIGEM.update(DADOS_PODERES_ORIGEM_ATLAS)
DADOS_PODERES_ORIGEM.update(DADOS_PODERES_ORIGEM_HEROIS)
