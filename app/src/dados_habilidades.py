# src/dados_habilidades.py

# =========================================================
# Efeitos Chave (para integração com o React/TypeScript):
# - pericia_escolha (int): Nível de treino extra em perícia à escolha.
# - poder_escolha (int): Quantos poderes gerais o jogador pode escolher.
# - pv_max_ini (int): Bônus fixo no PV máximo (nível 1).
# - pv_max_nivel (int): Bônus por nível no PV máximo (nível 2+).
# - pm_max_nivel (int): Bônus por nível no PM máximo.
# - deslocamento (int): Novo deslocamento base (em metros).
# - defesa_bonus (int): Bônus fixo na Defesa total.
# - penalidade_armadura (int): Penalidade na Defesa devido à raça.
# - resistencia_dano (dict): Ex: {"tipo": "veneno", "valor": 5, "teste": "Fortitude"}.
# - resistencia_rd (dict): Ex: {"frio": 10}.
# - bonus_pericia (dict): Ex: {"Percepção": 2}.
# - dano_arma_base (dict): Ex: {"tipo": "arremesso", "passos": 1}
# =========================================================

HABILIDADES_GERAIS = {


    # ------------------------------------------------------------------
    # --- PODERES E ORIGENS ---
    # ------------------------------------------------------------------
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
    },

    # ------------------------------------------------------------------
    # --- PODERES DE COMBATE ---
    # ------------------------------------------------------------------
    "Acuidade_Com_Arma": {
        "nome": "Acuidade com Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa Destreza em vez de Força em ataques e dano com armas leves ou de arremesso.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {"ataque_atributo_troca": {"origem": "for", "destino": "des", "tipo_arma": ["leve", "arremesso"]}}
    },
    "Arma_Secundaria_Grande": {
        "nome": "Arma Secundária Grande",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Pode empunhar duas armas de uma mão com Estilo de Duas Armas.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Duas Armas"],
        "efeitos": {}
    },
    "Arremesso_Potente": {
        "nome": "Arremesso Potente",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa Força em vez de Destreza em ataques com armas de arremesso. Permite usar Ataque Poderoso com elas.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1", "Estilo de Arremesso"],
        "efeitos": {"ataque_atributo_troca": {"origem": "des", "destino": "for", "tipo_arma": ["arremesso"]}}
    },
    "Arremesso_Multiplo": {
        "nome": "Arremesso Múltiplo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Gaste 1 PM para fazer um ataque extra com arma de arremesso (1/rodada).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1", "Estilo de Arremesso"],
        "efeitos": {}
    },
    "Ataque_Escudo": {
        "nome": "Ataque com Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Gaste 1 PM para fazer ataque extra com escudo ao agredir. Mantém bônus de defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma e Escudo"],
        "efeitos": {}
    },
    "Ataque_Pesado": {
        "nome": "Ataque Pesado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao atacar com arma de duas mãos, gaste 1 PM. Se acertar, faz manobra derrubar ou empurrar como ação livre.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Duas Mãos"],
        "efeitos": {}
    },
    "Ataque_Poderoso": {
        "nome": "Ataque Poderoso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Sofre -2 no ataque para receber +5 no dano.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1"],
        "efeitos": {}
    },
    "Ataque_Preciso": {
        "nome": "Ataque Preciso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 na margem de ameaça e +1 no multiplicador de crítico (uma mão, outra livre).",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Uma Arma"],
        "efeitos": {}
    },
    "Bloqueio_Escudo": {
        "nome": "Bloqueio com Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Reação: gaste 1 PM para ganhar RD igual ao bônus do escudo contra um dano.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma e Escudo"],
        "efeitos": {}
    },
    "Carga_Cavalaria": {
        "nome": "Carga de Cavalaria",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2d8 dano em investida montada. Pode continuar se movendo.",
        "fonte": "T20 JdA",
        "requisitos": ["Ginete"],
        "efeitos": {}
    },
    "Combate_Defensivo": {
        "nome": "Combate Defensivo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao agredir, sofra -2 no ataque para ganhar +5 na Defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {}
    },
    "Derrubar_Aprimorado": {
        "nome": "Derrubar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em derrubar. Gaste 1 PM para ataque extra ao derrubar.",
        "fonte": "T20 JdA",
        "requisitos": ["Combate Defensivo"],
        "efeitos": {"bonus_manobra": {"derrubar": 2}}
    },
    "Desarmar_Aprimorado": {
        "nome": "Desarmar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em desarmar. Gaste 1 PM para arremessar a arma longe.",
        "fonte": "T20 JdA",
        "requisitos": ["Combate Defensivo"],
        "efeitos": {"bonus_manobra": {"desarmar": 2}}
    },
    "Disparo_Preciso": {
        "nome": "Disparo Preciso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ignora penalidade de -5 contra oponentes em combate corpo a corpo.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Disparo ou Estilo de Arremesso"],
        "efeitos": {}
    },
    "Disparo_Rapido": {
        "nome": "Disparo Rápido",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação completa agredir: um ataque adicional com arma de disparo (-2 em todos os ataques).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1", "Estilo de Disparo"],
        "efeitos": {}
    },
    "Empunhadura_Poderosa": {
        "nome": "Empunhadura Poderosa",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Usa armas de tamanho maior com penalidade -2 (em vez de -5).",
        "fonte": "T20 JdA",
        "requisitos": ["For 3"],
        "efeitos": {}
    },
    "Encouraçado": {
        "nome": "Encouraçado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Se usar armadura pesada, recebe +2 na Defesa.",
        "fonte": "T20 JdA",
        "requisitos": ["Proficiência armadura pesada"],
        "efeitos": {"defesa_bonus_condicional": {"tipo": "armadura_pesada", "valor": 2}}
    },
    "Esquiva": {
        "nome": "Esquiva",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Você recebe +2 na Defesa e Reflexos.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {"defesa_bonus": 2, "bonus_pericia": {"Reflexos": 2}}
    },
    "Estilo_Arma_Escudo": {
        "nome": "Estilo de Arma e Escudo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Se usar escudo, bônus de defesa do escudo aumenta em +2.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta", "Proficiência com escudos"],
        "efeitos": {"bonus_escudo": 2}
    },
    "Estilo_Arma_Longa": {
        "nome": "Estilo de Arma Longa",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em ataques com armas alongadas. Pode atacar adjacentes.",
        "fonte": "T20 JdA",
        "requisitos": ["For 1", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Arremesso": {
        "nome": "Estilo de Arremesso",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Saca armas de arremesso como livre. +2 dano. Com Saque Rápido, +2 ataque.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Pontaria"],
        "efeitos": {"bonus_dano_tipo": {"arremesso": 2}}
    },
    "Estilo_Disparo": {
        "nome": "Estilo de Disparo",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Soma Destreza nas rolagens de dano com armas de disparo.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Pontaria"],
        "efeitos": {"dano_atributo_extra": "des"}
    },
    "Estilo_Duas_Armas": {
        "nome": "Estilo de Duas Armas",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao agredir com duas armas, faz dois ataques (-2 em ambos).",
        "fonte": "T20 JdA",
        "requisitos": ["Des 2", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Duas_Maos": {
        "nome": "Estilo de Duas Mãos",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+5 dano com arma de duas mãos (não leve).",
        "fonte": "T20 JdA",
        "requisitos": ["For 2", "Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Uma_Arma": {
        "nome": "Estilo de Uma Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 Defesa e Ataque se usar uma arma e nada na outra mão.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta"],
        "efeitos": {}
    },
    "Estilo_Desarmado": {
        "nome": "Estilo Desarmado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ataques desarmados causam 1d6 e podem ser letais.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Luta"],
        "efeitos": {"dano_desarmado": "1d6"}
    },
    "Fanatico": {
        "nome": "Fanático",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Deslocamento não reduz por armadura pesada.",
        "fonte": "T20 JdA",
        "requisitos": ["12º nível", "Encouraçado"],
        "efeitos": {"imunidade_penalidade_mov": ["armadura"]}
    },
    "Finta_Aprimorada": {
        "nome": "Finta Aprimorada",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em Enganação para fintar. Finta como ação de movimento.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Enganação"],
        "efeitos": {}
    },
    "Foco_Arma": {
        "nome": "Foco em Arma",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em ataque com uma arma escolhida.",
        "fonte": "T20 JdA",
        "requisitos": ["Proficiência com a arma"],
        "efeitos": {"arma_escolha_bonus_ataque": 2}
    },
    "Ginete": {
        "nome": "Ginete",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Passa auto em testes para não cair. Sem penalidade ataque/magia montado.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Cavalgar"],
        "efeitos": {}
    },
    "Inexpugnavel": {
        "nome": "Inexpugnável",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em testes de resistência se usar armadura pesada.",
        "fonte": "T20 JdA",
        "requisitos": ["Encouraçado", "6º nível"],
        "efeitos": {"resistencia_bonus_condicional": {"tipo": "armadura_pesada", "valor": 2}}
    },
    "Mira_Apurada": {
        "nome": "Mira Apurada",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 ataque e margem de ameaça com mirar.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Disparo Preciso"],
        "efeitos": {}
    },
    "Piqueiro": {
        "nome": "Piqueiro",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ataque de oportunidade com arma alongada quando inimigo entra no alcance.",
        "fonte": "T20 JdA",
        "requisitos": ["Estilo de Arma Longa"],
        "efeitos": {}
    },
    "Presenca_Aterradora": {
        "nome": "Presença Aterradora",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação padrão e 1 PM para assustar criaturas em alcance curto.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Intimidação"],
        "efeitos": {}
    },
    "Proficiencia": {
        "nome": "Proficiência",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Recebe uma proficiência (marciais, fogo, pesadas, escudos ou exóticas).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"proficiencia_escolha": 1}
    },
    "Quebrar_Aprimorado": {
        "nome": "Quebrar Aprimorado",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 em quebrar. Ataque extra ao destruir arma.",
        "fonte": "T20 JdA",
        "requisitos": ["Ataque Poderoso"],
        "efeitos": {"bonus_manobra": {"quebrar": 2}}
    },
    "Reflexos_Combate": {
        "nome": "Reflexos de Combate",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ação de movimento extra no primeiro turno.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 1"],
        "efeitos": {}
    },
    "Saque_Rapido": {
        "nome": "Saque Rápido",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+2 Iniciativa. Sacar como livre. Recarga diminui um passo.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Iniciativa"],
        "efeitos": {"bonus_pericia": {"Iniciativa": 2}}
    },
    "Trespassar": {
        "nome": "Trespassar",
        "tipo": "Poder Geral (Combate)",
        "descricao": "Ao reduzir inimigo a 0 PV, gaste 1 PM para ataque extra.",
        "fonte": "T20 JdA",
        "requisitos": ["Ataque Poderoso"],
        "efeitos": {}
    },
    "Vitalidade": {
        "nome": "Vitalidade",
        "tipo": "Poder Geral (Combate)",
        "descricao": "+1 PV por nível e +2 Fortitude.",
        "fonte": "T20 JdA",
        "requisitos": ["Con 1"],
        "efeitos": {"pv_max_nivel": 1, "bonus_pericia": {"Fortitude": 2}}
    },

    # ------------------------------------------------------------------
    # --- PODERES DE DESTINO ---
    # ------------------------------------------------------------------
    "Acrobatico": {
        "nome": "Acrobático",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Usa Destreza em Atletismo. Ignora terreno difícil. Pode investir em terreno difícil.",
        "fonte": "T20 JdA",
        "requisitos": ["Des 2"],
        "efeitos": {"atletismo_des": True, "imunidade_terreno_dificil": True}
    },
    "Ao_Sabor_Destino": {
        "nome": "Ao Sabor do Destino",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Bônus escalonados se não usar itens mágicos.",
        "fonte": "T20 JdA",
        "requisitos": ["6º nível"],
        "efeitos": {}
    },
    "Aparencia_Inofensiva": {
        "nome": "Aparência Inofensiva",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Primeira criatura a atacar deve passar em Vontade ou perde ação (1/cena).",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Atletico": {
        "nome": "Atlético",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Atletismo e +3m de deslocamento.",
        "fonte": "T20 JdA",
        "requisitos": ["For 2"],
        "efeitos": {"bonus_pericia": {"Atletismo": 2}, "deslocamento_bonus": 3}
    },
    "Atraente": {
        "nome": "Atraente",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em perícias de Carisma contra quem se atrai.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Comandar": {
        "nome": "Comandar",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Ação movimento e 1 PM: Aliados em alcance médio recebem +1 em perícias.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Costas_Largas": {
        "nome": "Costas Largas",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+5 espaços de carga e +1 item vestido.",
        "fonte": "T20 JdA",
        "requisitos": ["Con 1", "For 1"],
        "efeitos": {"carga_max_bonus": 5}
    },
    "Foco_Pericia": {
        "nome": "Foco em Perícia",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Escolha uma perícia. Pode rolar dois dados e usar o melhor (1 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado na perícia"],
        "efeitos": {"foco_pericia_escolha": 1}
    },
    "Inventario_Organizado": {
        "nome": "Inventário Organizado",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Soma INT na carga. Itens pequenos ocupam 1/4.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {"carga_soma_atributo": "int"}
    },
    "Investigador": {
        "nome": "Investigador",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Investigação e soma INT em Intuição.",
        "fonte": "T20 JdA",
        "requisitos": ["Int 1"],
        "efeitos": {"bonus_pericia": {"Investigação": 2}, "pericia_soma_atributo": {"Intuição": "int"}}
    },
    "Lobo_Solitario": {
        "nome": "Lobo Solitário",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+1 em perícias e Defesa se sem aliados perto. Cura em si mesmo sem penalidade.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Medicina": {
        "nome": "Medicina",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Ação completa para curar PV com teste de Cura.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Treinado em Cura"],
        "efeitos": {}
    },
    "Parceiro": {
        "nome": "Parceiro",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Recebe um parceiro iniciante.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Adestramento ou Diplomacia", "5º nível"],
        "efeitos": {"parceiro_adicional": 1}
    },
    "Sentidos_Agucados": {
        "nome": "Sentidos Aguçados",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em Percepção, não fica desprevenido vs invisível, rerola falha por camuflagem.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1", "Treinado em Percepção"],
        "efeitos": {"bonus_pericia": {"Percepção": 2}}
    },
    "Sortudo": {
        "nome": "Sortudo",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Gaste 3 PM para rerolar um teste.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Surto_Heroico": {
        "nome": "Surto Heroico",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Gaste 5 PM para ação padrão ou movimento extra (1/rodada).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Torcida": {
        "nome": "Torcida",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+2 em perícias e Defesa se tiver torcida.",
        "fonte": "T20 JdA",
        "requisitos": ["Car 1"],
        "efeitos": {}
    },
    "Treinamento_Pericia": {
        "nome": "Treinamento em Perícia",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Torna-se treinado em uma perícia.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"pericia_escolha": 1}
    },
    "Veneficio": {
        "nome": "Venefício",
        "tipo": "Poder Geral (Destino)",
        "descricao": "Uso seguro de venenos. CD +2.",
        "fonte": "T20 JdA",
        "requisitos": ["Treinado em Ofício (alquimista)"],
        "efeitos": {}
    },
    "Vontade_Ferro": {
        "nome": "Vontade de Ferro",
        "tipo": "Poder Geral (Destino)",
        "descricao": "+1 PM a cada dois níveis e +2 em Vontade.",
        "fonte": "T20 JdA",
        "requisitos": ["Sab 1"],
        "efeitos": {"pm_max_nivel_fracionado": 0.5, "bonus_pericia": {"Vontade": 2}}
    },

    # ------------------------------------------------------------------
    # --- PODERES DE MAGIA ---
    # ------------------------------------------------------------------
    "Celebrar_Ritual": {
        "nome": "Celebrar Ritual",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode lançar magias como rituais (dobro PM, tempo longo, custo $).",
        "fonte": "T20 JdA",
        "requisitos": ["8º nível", "Treinado em Misticismo ou Religião"],
        "efeitos": {}
    },
    "Escrever_Pergaminho": {
        "nome": "Escrever Pergaminho",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode fabricar pergaminhos.",
        "fonte": "T20 JdA",
        "requisitos": ["Magias", "Treinado em Ofício (escriba)"],
        "efeitos": {}
    },
    "Foco_Magia": {
        "nome": "Foco em Magia",
        "tipo": "Poder Geral (Magia)",
        "descricao": "-1 PM em uma magia escolhida.",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Acelerada": {
        "nome": "Magia Acelerada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Muda execução para livre (+4 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Magias 2º círculo"],
        "efeitos": {}
    },
    "Magia_Ampliada": {
        "nome": "Magia Ampliada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Aumenta alcance ou dobra área (+2 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Discreta": {
        "nome": "Magia Discreta",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Aprimoramento: Lança sem gesticular/falar (+2 PM).",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Magia_Ilimitada": {
        "nome": "Magia Ilimitada",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Soma atributo-chave ao limite de PM por magia.",
        "fonte": "T20 JdA",
        "requisitos": ["Lançar magias"],
        "efeitos": {}
    },
    "Preparar_Pocao": {
        "nome": "Preparar Poção",
        "tipo": "Poder Geral (Magia)",
        "descricao": "Pode fabricar poções.",
        "fonte": "T20 JdA",
        "requisitos": ["Magias", "Treinado em Ofício (alquimista)"],
        "efeitos": {}
    },

    # ------------------------------------------------------------------
    # --- PODERES CONCEDIDOS ---
    # ------------------------------------------------------------------
    "Coragem_Total": {
        "nome": "Coragem Total",
        "tipo": "Poder Concedido",
        "descricao": "Imune a medo.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Arsenal, Khalmyr, Lin-Wu ou Valkaria"],
        "efeitos": {"imunidade": ["medo"]}
    },
    "Escamas_Draconicas": {
        "nome": "Escamas Dracônicas",
        "tipo": "Poder Concedido",
        "descricao": "+2 Defesa e Fortitude.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Kallyadranoch"],
        "efeitos": {"defesa_bonus": 2, "bonus_pericia": {"Fortitude": 2}}
    },
    "Sangue_Ferro": {
        "nome": "Sangue de Ferro",
        "tipo": "Poder Concedido",
        "descricao": "3 PM para receber +2 dano e RD 5.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Arsenal"],
        "efeitos": {}
    },
    "Zumbificar": {
        "nome": "Zumbificar",
        "tipo": "Poder Concedido",
        "descricao": "3 PM para reanimar cadáver como parceiro.",
        "fonte": "T20 JdA",
        "requisitos": ["Devoto de Tenebra"],
        "efeitos": {}
    },

    # ------------------------------------------------------------------
    # --- PODERES DA TORMENTA ---
    # ------------------------------------------------------------------
    "Anatomia_Insana": {
        "nome": "Anatomia Insana",
        "tipo": "Poder da Tormenta",
        "descricao": "25% chance de ignorar crítico/furtivo. +25% por cada 2 outros poderes Tormenta.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Antenas": {
        "nome": "Antenas",
        "tipo": "Poder da Tormenta",
        "descricao": "+1 Iniciativa, Percepção, Vontade. Aumenta com outros poderes.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"bonus_pericia_tormenta": ["Iniciativa", "Percepção", "Vontade"]}
    },
    "Carapaca": {
        "nome": "Carapaça",
        "tipo": "Poder da Tormenta",
        "descricao": "+1 Defesa. Aumenta com outros poderes.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"defesa_bonus_tormenta": 1}
    },
    "Dentes_Afiados": {
        "nome": "Dentes Afiados",
        "tipo": "Poder da Tormenta",
        "descricao": "Arma natural mordida (1d4). Gaste 1 PM para ataque extra.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Empunhadura_Rubra": {
        "nome": "Empunhadura Rubra",
        "tipo": "Poder da Tormenta",
        "descricao": "Gaste 1 PM para +1 em Luta (aumenta com outros poderes).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Membros_Extras": {
        "nome": "Membros Extras",
        "tipo": "Poder da Tormenta",
        "descricao": "Duas patas insetoides (ataques extras). Pode empunhar armas leves.",
        "fonte": "T20 JdA",
        "requisitos": ["4 outros poderes Tormenta"],
        "efeitos": {}
    },
    "Olhos_Vermelhos": {
        "nome": "Olhos Vermelhos",
        "tipo": "Poder da Tormenta",
        "descricao": "Visão no escuro e +1 Intimidação (aumenta com outros poderes).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"visao_escuro": True, "bonus_pericia_tormenta": ["Intimidação"]}
    },
    "Pele_Corrompida": {
        "nome": "Pele Corrompida",
        "tipo": "Poder da Tormenta",
        "descricao": "RD 2 a ácido, eletricidade, fogo, frio, luz, trevas. Aumenta com outros poderes.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {"resistencia_elemental_tormenta": 2}
    },
    "Sangue_Acido": {
        "nome": "Sangue Ácido",
        "tipo": "Poder da Tormenta",
        "descricao": "Ao sofrer dano corpo a corpo, atacante sofre 1 dano ácido por poder Tormenta.",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    },
    "Visco_Rubro": {
        "nome": "Visco Rubro",
        "tipo": "Poder da Tormenta",
        "descricao": "1 PM para +1 dano corpo a corpo (aumenta com outros poderes).",
        "fonte": "T20 JdA",
        "requisitos": [],
        "efeitos": {}
    }
}
