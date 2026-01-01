# app/src/dados_poderes_origem.py

DADOS_PODERES_ORIGEM = {
    "Membro_Igreja_Acolito": {
        "nome": "Membro da Igreja",
        "tipo": "Origem (Acólito)",
        "descricao": "Você consegue hospedagem confortável e informação em qualquer templo de sua divindade, para você e seus aliados.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Amigo_Especial_AmigoAnimais": {
        "nome": "Amigo Especial",
        "tipo": "Origem (Amigo dos Animais)",
        "descricao": "Você recebe +5 em testes de Adestramento com animais. Além disso, possui um animal de estimação que o auxilia (+2 em uma perícia à sua escolha, exceto Luta ou Pontaria).",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia": {"Adestramento": 5}, "pericia_escolha_bonus": 1}
    },
    "Lembrancas_Graduais_Amnesico": {
        "nome": "Lembranças Graduais",
        "tipo": "Origem (Amnésico)",
        "descricao": "Durante suas aventuras, em momentos a critério do mestre, você pode fazer um teste de Sabedoria (CD 10) para reconhecer pessoas, criaturas ou lugares que tenha encontrado antes de perder a memória.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Sangue_Azul_Aristocrata": {
        "nome": "Sangue Azul",
        "tipo": "Origem (Aristocrata)",
        "descricao": "Você tem alguma influência política, suficiente para ser tratado com mais leniência pela guarda, conseguir uma audiência com o nobre local etc.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Frutos_Trabalho_Artesao": {
        "nome": "Frutos do Trabalho",
        "tipo": "Origem (Artesão)",
        "descricao": "No início de cada aventura, você recebe até 5 itens gerais que possa fabricar num valor total de até T$ 50. Valor aumenta no patamar veterano (T$ 100), heroico (T$ 300) e lenda (T$ 500).",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Dom_Artistico_Artista": {
        "nome": "Dom Artístico",
        "tipo": "Origem (Artista)",
        "descricao": "Você recebe +2 em testes de Atuação, e recebe o dobro de tibares em apresentações.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia": {"Atuação": 2}}
    },
    "Esse_Cheiro_AssistenteLab": {
        "nome": "Esse Cheiro...",
        "tipo": "Origem (Assistente de Laboratório)",
        "descricao": "Você recebe +2 em Fortitude e detecta automaticamente a presença (mas não a localização ou natureza) de itens alquímicos em alcance curto.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia": {"Fortitude": 2}}
    },
    "A_Prova_Tudo_Batedor": {
        "nome": "À Prova de Tudo",
        "tipo": "Origem (Batedor)",
        "descricao": "Você não sofre penalidade em deslocamento e Sobrevivência por clima ruim e por terreno difícil natural.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Confissao_Capanga": {
        "nome": "Confissão",
        "tipo": "Origem (Capanga)",
        "descricao": "Você pode usar Intimidação para interrogar sem custo e em uma hora (como Investigação).",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Alpinista_Social_Charlatao": {
        "nome": "Alpinista Social",
        "tipo": "Origem (Charlatão)",
        "descricao": "Você pode substituir testes de Diplomacia por testes de Enganação.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Truque_Magica_Circense": {
        "nome": "Truque de Mágica",
        "tipo": "Origem (Circense)",
        "descricao": "Você pode lançar Explosão de Chamas, Hipnotismo e Queda Suave, mas apenas com o aprimoramento Truque. Não é uma habilidade mágica.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Punguista_Criminoso": {
        "nome": "Punguista",
        "tipo": "Origem (Criminoso)",
        "descricao": "Você pode fazer testes de Ladinagem para sustento (como Ofício), mas em apenas um dia. Se passar, recebe o dobro do dinheiro, mas, se falhar, pode ter problemas com a lei.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Medico_Campo_Curandeiro": {
        "nome": "Médico de Campo",
        "tipo": "Origem (Curandeiro)",
        "descricao": "Você soma sua Sabedoria aos PV restaurados por suas habilidades e itens mundanos de cura.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Busca_Interior_Eremita": {
        "nome": "Busca Interior",
        "tipo": "Origem (Eremita)",
        "descricao": "Quando você e seus companheiros estão diante de um mistério, você pode gastar 1 PM para meditar sozinho durante algum tempo e receber uma dica do mestre.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Desejo_Liberdade_Escravo": {
        "nome": "Desejo de Liberdade",
        "tipo": "Origem (Escravo)",
        "descricao": "Ninguém voltará a torná-lo um escravo! Você recebe +5 em testes contra a manobra agarrar e efeitos de movimento.",
        "fonte": "T20 JdA",
        "efeitos": {"resistencia_manobra": {"agarrar": 5, "movimento": 5}}
    },
    "Palpite_Fund_Estudioso": {
        "nome": "Palpite Fundamentado",
        "tipo": "Origem (Estudioso)",
        "descricao": "Você pode gastar 2 PM para substituir um teste de qualquer perícia originalmente baseada em Inteligência ou Sabedoria por um teste de Conhecimento.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Agua_Feijao_Fazendeiro": {
        "nome": "Água no Feijão",
        "tipo": "Origem (Fazendeiro)",
        "descricao": "Você não sofre a penalidade de –5 e não gasta matéria prima adicional para fabricar pratos para cinco pessoas.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Cultura_Exotica_Forasteiro": {
        "nome": "Cultura Exótica",
        "tipo": "Origem (Forasteiro)",
        "descricao": "Você pode gastar 1 PM para fazer um teste de perícia somente treinada, mesmo sem ser treinado na perícia.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Pao_Circo_Gladiador": {
        "nome": "Pão e Circo",
        "tipo": "Origem (Gladiador)",
        "descricao": "Você pode escolher causar dano não letal sem sofrer a penalidade de –5.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Detetive_Guarda": {
        "nome": "Detetive",
        "tipo": "Origem (Guarda)",
        "descricao": "Você pode gastar 1 PM para substituir testes de Percepção e Intuição por testes de Investigação até o fim da cena.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Heranca_Herdeiro": {
        "nome": "Herança",
        "tipo": "Origem (Herdeiro)",
        "descricao": "Você herdou um item de preço de até T$ 1.000. Pode escolher este poder duas vezes, para um item de até T$ 2.000.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Coracao_Heroico_HeroiCampones": {
        "nome": "Coração Heroico",
        "tipo": "Origem (Herói Camponês)",
        "descricao": "Você recebe +3 pontos de mana. Quando atinge um novo patamar (no 5º, 11º e 17º níveis), recebe +3 PM.",
        "fonte": "T20 JdA",
        "efeitos": {"pm_max_ini": 3}
    },
    "Passagem_Navio_Marujo": {
        "nome": "Passagem de Navio",
        "tipo": "Origem (Marujo)",
        "descricao": "Você consegue transporte marítimo para você e seus aliados, sem custos, desde que todos paguem com trabalho.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Vendedor_Carcaças_Mateiro": {
        "nome": "Vendedor de Carcaças",
        "tipo": "Origem (Mateiro)",
        "descricao": "Você pode extrair recursos de criaturas em um minuto, em vez de uma hora, e recebe +5 no teste.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia_condicional": {"Sobrevivência": 5}}
    },
    "Rede_Contatos_MembroGuilda": {
        "nome": "Rede de Contatos",
        "tipo": "Origem (Membro de Guilda)",
        "descricao": "Graças à influência de sua guilda, você pode usar Diplomacia para interrogar sem custo e em uma hora (como Investigação).",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Negociacao_Mercador": {
        "nome": "Negociação",
        "tipo": "Origem (Mercador)",
        "descricao": "Você pode vender itens 10% mais caro (não cumulativo com barganha).",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Escavador_Minerador": {
        "nome": "Escavador",
        "tipo": "Origem (Minerador)",
        "descricao": "Você se torna proficiente em picaretas, causa +1 de dano com elas e não é afetado por terreno difícil em masmorras e subterrâneos.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Mochileiro_Nomade": {
        "nome": "Mochileiro",
        "tipo": "Origem (Nômade)",
        "descricao": "Seu limite de carga aumenta em 5 espaços.",
        "fonte": "T20 JdA",
        "efeitos": {"carga_max_bonus": 5}
    },
    "Quebra_Galho_Pivete": {
        "nome": "Quebra-galho",
        "tipo": "Origem (Pivete)",
        "descricao": "Em cidades ou metrópoles, você pode comprar qualquer item mundano não superior por metade do preço normal.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Estoico_Refugiado": {
        "nome": "Estoico",
        "tipo": "Origem (Refugiado)",
        "descricao": "Sua condição de descanso é uma categoria acima do padrão pela situação.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Antigo_Mestre_Seguidor": {
        "nome": "Antigo Mestre",
        "tipo": "Origem (Seguidor)",
        "descricao": "Uma vez por aventura, ele surge para ajudá-lo por uma cena. Ele é um parceiro mestre de um tipo à sua escolha.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Vida_Rustica_Selvagem": {
        "nome": "Vida Rústica",
        "tipo": "Origem (Selvagem)",
        "descricao": "Você é imune a efeitos prejudiciais de itens ingeríveis e sua recuperação de PV e PM nunca é inferior a seu próprio nível.",
        "fonte": "T20 JdA",
        "efeitos": {"imunidade_ingesta": True}
    },
    "Influencia_Militar_Soldado": {
        "nome": "Influência Militar",
        "tipo": "Origem (Soldado)",
        "descricao": "Onde houver acampamentos ou bases militares, você pode conseguir hospedagem e informações para você e seus aliados.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Gororoba_Taverneiro": {
        "nome": "Gororoba",
        "tipo": "Origem (Taverneiro)",
        "descricao": "Você não sofre a penalidade de –5 para fabricar um prato especial adicional.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },
    "Esforcado_Trabalhador": {
        "nome": "Esforçado",
        "tipo": "Origem (Trabalhador)",
        "descricao": "Você recebe um bônus de +2 em todos os testes de perícias estendidos (incluindo perigos complexos).",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia_estendida": 2}
    }
}
