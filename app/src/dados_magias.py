# ==============================================================================
# DADOS DE MAGIAS (Tormenta 20) - PARTE 1 (A - B)
# ==============================================================================

DADOS_MAGIAS= {
    "Abençoar Alimentos": {
        "nome": "Abençoar Alimentos",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Alimento para 1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Você purifica e abençoa uma porção de comida ou dose de bebida. Isso torna um alimento sujo, estragado ou envenenado próprio para consumo[cite: 5, 6]. O alimento oferece 5 PV temporários ou 1 PM temporário[cite: 7].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "O alimento é purificado, mas não fornece bônus.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta o número de alvos em +1.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Muda a duração para permanente, alvo para 1 frasco com água (cria água benta).", "efeitos": {}}
        ]
    },
    "Acalmar Animal": {
        "nome": "Acalmar Animal",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 animal",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "O animal fica prestativo em relação a você[cite: 16]. Você recebe +10 nos testes de Adestramento e Diplomacia contra o animal[cite: 17].",
        "efeitos": {
            "pericia_adestramento_bonus": 10,
            "pericia_diplomacia_bonus": 10
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda o alcance para médio.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Muda o alvo para 1 monstro ou espírito com Int -5 ou 4.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o número de alvos em +1.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda o alvo para 1 monstro ou espírito. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Adaga Mental": {
        "nome": "Adaga Mental",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Você manifesta e dispara uma adaga imaterial contra a mente do alvo, que sofre 2d6 pontos de dano psíquico e fica atordoado por uma rodada[cite: 26]. Se passar, sofre metade do dano e evita a condição[cite: 27].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Lança sem gesticular ou falar. Adaga invisível.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda a duração para um dia. Você sabe a direção e localização do alvo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o dano em +1d6.", "efeitos": {}}
        ]
    },
    "Alarme": {
        "nome": "Alarme",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Esfera com 9m de raio",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Cria uma barreira protetora invisível que detecta criaturas na área. Pode emitir aviso telepático ou sonoro[cite: 37, 39].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Muda o alcance para pessoal (emanação).", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Percebe efeitos de adivinhação e permite teste oposto de Misticismo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Muda duração para 1 dia ou até descarregada. Pode paralisar intruso (Vontade anula). +10 em Sobrevivência para rastrear.", "efeitos": {
                "pericia_sobrevivencia_rastrear": 10}}
        ]
    },
    "Aliado Animal": {
        "nome": "Aliado Animal",
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 animal prestativo",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Cria vínculo mental com animal. Ele funciona como parceiro veterano de um tipo a sua escolha[cite: 53, 55].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Muda alvo para animal Minúsculo e duração para 1 semana (mensageiro).", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Muda o parceiro para mestre. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+12 PM",
                "descricao": "Muda o alvo para 2 animais (ajuda de ambos). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Alterar Destino": {
        "nome": "Alterar Destino",
        "circulo": 5,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Reação",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Permite rolar novamente um teste de resistência com +10 ou forçar inimigo a rolar ataque novamente com -10[cite: 69].",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Alterar Memória": {
        "nome": "Alterar Memória",
        "circulo": 4,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Vontade anula",
        "descricao": "Altera ou apaga memórias do alvo da última hora[cite: 73].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda alcance para pessoal e alvo para cone de 4,5m.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Altera/apaga memórias das últimas 24 horas.", "efeitos": {}}
        ]
    },
    "Alterar Tamanho": {
        "nome": "Alterar Tamanho",
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 objeto",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Aumenta ou diminui o tamanho de um item mundano em até três categorias. Pode mudar consistência[cite: 78, 79].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta o número de alvos em +1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura. Aumenta categoria de tamanho, +2 Força.",
                "efeitos": {"atributo_forca": 2}},
            {"custo": "+3 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura. Diminui categoria de tamanho, +2 Destreza. Requer 3º círculo.",
                "efeitos": {"atributo_destreza": 2}},
            {"custo": "+7 PM", "descricao": "Muda alvo para criatura, duração permanente (Fortitude anula). Torna Minúsculo, For -5, Desl 3m. Requer 4º círculo.", "efeitos": {
                "atributo_forca_penalidade": -5}}
        ]
    },
    "Amarras Etéreas": {
        "nome": "Amarras Etéreas",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Reflexos anula",
        "descricao": "Três laços de energia deixam o alvo agarrado. Pode tentar se livrar (Atletismo). Laços têm Defesa 10, 10 PV, RD 5[cite: 95, 96, 98].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta número de laços em +1.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Laços destruídos com 1 ataque, mas causam 1d8+1 de dano de essência ao explodir. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Amedrontar": {
        "nome": "Amedrontar",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 animal ou humanoide",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Se falhar na resistência, fica apavorado por 1 rodada, depois abalado. Se passar, fica abalado por 1d4 rodadas[cite: 109].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Fica apavorado por 1d4+1 rodadas na falha.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda o alvo para 1 criatura.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta todos os alvos válidos no alcance.", "efeitos": {}}
        ]
    },
    "Âncora Dimensional": {
        "nome": "Âncora Dimensional",
        "circulo": 3,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura ou objeto",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Impede qualquer movimento planar, teletransporte ou incorpóreo[cite: 115, 116].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda para alcance médio, área esfera 3m, alvos escolhidos.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Cria fio de energia que prende alvo a ponto fixo (limite 3m).", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Cria corrente de energia (20 PV, RD 40).", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Muda para cubo de 9m, duração permanente (Bloqueio planar). Custo material T$ 2.000.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Prende todos os alvos ao centro da área (esfera 3m).", "efeitos": {}}
        ]
    },
    "Animar Objetos": {
        "nome": "Animar Objetos",
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Vários objetos (dep. tamanho)",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Concede vida a objetos, tornando-os parceiros sob seu controle[cite: 131]. Objetos são construtos.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Muda duração para permanente. Custo material T$ 1.000.", "efeitos": {}}
        ]
    },
    "Anular a Luz": {
        "nome": "Anular a Luz",
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Instantânea/Cena",
        "resistencia": "",
        "descricao": "Onda de escuridão dissipa magias de luz/nível menor. Aliados recebem +4 na Defesa. Inimigos ficam enjoados (1d4 rodadas)[cite: 153, 154, 155].",
        "efeitos": {
            "defesa_bonus_magia": 4
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o bônus na Defesa em +1.",
                "efeitos": {"defesa_bonus_magia": 1}},
            {"custo": "+4 PM", "descricao": "Dissipa magias até 4º círculo. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Dissipa magias até 5º círculo. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Aparência Perfeita": {
        "nome": "Aparência Perfeita",
        "circulo": 2,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Concede aparência idealizada. Se Carisma < 5, torna-se 5; senão recebe +2. Recebe +5 em Diplomacia e Enganação[cite: 164, 165].",
        "efeitos": {
            "pericia_diplomacia_bonus": 5,
            "pericia_enganacao_bonus": 5
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda o alcance para toque e o alvo para 1 humanoide.", "efeitos": {}}
        ]
    },
    "Aprisionamento": {
        "nome": "Aprisionamento",
        "circulo": 5,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Permanente",
        "resistencia": "Vontade anula",
        "descricao": "Cria uma prisão mágica (acorrentamento, contenção mínima, prisão dimensional, sepultamento ou sono eterno). Requer componente material T$ 1.000[cite: 172, 178].",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Área Escorregadia": {
        "nome": "Área Escorregadia",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Quadrado de 3m ou 1 objeto",
        "duracao": "Cena",
        "resistencia": "Reflexos (veja texto)",
        "descricao": "Recobre superfície com substância escorregadia. Criaturas devem passar na resistência para não cair. Testes de Acrobacia (CD 10) para andar[cite: 198, 199, 200].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta a área em +1 quadrado de 1,5m.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda a CD dos testes de Acrobacia para 15.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda a CD dos testes de Acrobacia para 20.", "efeitos": {}}
        ]
    },
    "Arma Espiritual": {
        "nome": "Arma Espiritual",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Invoca arma da divindade. Uma vez por rodada, reage a ataque corpo a corpo causando 2d6 de dano automático no atacante[cite: 207, 208].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "A arma protege: +1 na Defesa.",
                "efeitos": {"defesa_bonus_magia": 1}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus na Defesa em +1.",
                "efeitos": {"defesa_bonus_magia": 1}},
            {"custo": "+2 PM", "descricao": "Muda duração para sustentada. Ataca com ação livre no seu turno.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda tipo de dano para essência.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d6.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Invoca duas armas (dois contra-ataques/ataques). Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Arma Mágica": {
        "nome": "Arma Mágica",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 arma empunhada",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Arma fornece +1 em testes de ataque e rolagens de dano. Pode usar atributo de magia no ataque[cite: 223, 224].",
        "efeitos": {
            "ataque_bonus_magia": 1,
            "dano_bonus_magia": 1
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o bônus em +1.",
                "efeitos": {"ataque_bonus_magia": 1, "dano_bonus_magia": 1}},
            {"custo": "+2 PM",
                "descricao": "Arma causa +1d6 de dano elemental (ácido, eletricidade, fogo ou frio).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Muda bônus elemental para +2d6.", "efeitos": {}}
        ]
    },
    "Armadura Arcana": {
        "nome": "Armadura Arcana",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria uma película protetora invisível, fornecendo +5 na Defesa. Cumulativo com outras magias, mas não armaduras[cite: 230].",
        "efeitos": {
            "defesa_bonus_magia": 5
        },
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Muda execução para reação (+5 Defesa contra o ataque específico).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus na Defesa em +1.",
                "efeitos": {"defesa_bonus_magia": 1}},
            {"custo": "+2 PM", "descricao": "Muda a duração para um dia.", "efeitos": {}}
        ]
    },
    "Armamento da Natureza": {
        "nome": "Armamento da Natureza",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 arma",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Fortalece arma mundana primitiva, natural ou desarmado. Aumenta dano em um passo e considerada mágica[cite: 237, 238].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Fornece +1 nos testes de ataque.",
                "efeitos": {"ataque_bonus_magia": 1}},
            {"custo": "+2 PM",
                "descricao": "Muda execução para ação de movimento.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta bônus de ataque em +1.",
                "efeitos": {"ataque_bonus_magia": 1}},
            {"custo": "+5 PM", "descricao": "Aumenta o dano da arma em mais um passo.", "efeitos": {}}
        ]
    },
    "Assassino Fantasmagórico": {
        "nome": "Assassino Fantasmagórico",
        "circulo": 4,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "1 criatura",
        "duracao": "Cena (até descarregar)",
        "resistencia": "Vontade anula, Fortitude parcial",
        "descricao": "Cria ilusão do maior medo do alvo. Se falhar em Vontade, espectro persegue. Se tocar (Fortitude), causa 6d6 trevas ou colapso (-1 PV e sangrando)[cite: 247, 250, 255, 256].",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Augúrio": {
        "nome": "Augúrio",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Diz se uma ação no próximo hora trará resultados bons, ruins, ambos ou nada. Chance de falha em 1 no d6[cite: 260, 261].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Execução 1 min. Consulta divindade sobre evento de até 1 dia (frase/enigma). Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Execução 10 min, duração 1 min. Perguntas sim/não/não sei (1 por rodada). Requer 4º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Chance de falha diminui (d12, falha no 1).", "efeitos": {}},
            {"custo": "+12 PM",
                "descricao": "Chance de falha diminui (d20, falha no 1).", "efeitos": {}}
        ]
    },
    "Aura Divina": {
        "nome": "Aura Divina",
        "circulo": 5,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 9m de raio",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Aura brilhante. Aliados devotos imunes a encantamento, +10 Defesa/Resistência. Outros aliados +5 Defesa/Resistência. Inimigos sofrem condição[cite: 284, 285, 287].",
        "efeitos": {
            "defesa_bonus_magia": 5,
            "resistencia_bonus_magia": 5
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta bônus na Defesa e resistência em +1.",
                "efeitos": {"defesa_bonus_magia": 1, "resistencia_bonus_magia": 1}}
        ]
    },
    "Aviso": {
        "nome": "Aviso",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Movimento",
        "alcance": "Longo",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Envia aviso telepático. Escolha: Alerta (+5 Iniciativa/Percepção), Mensagem (25 palavras) ou Localização[cite: 292, 294].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta alcance fator x10.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Permite resposta na opção Mensagem.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Na opção Localização, dura pela cena.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}}
        ]
    },
    "Banimento": {
        "nome": "Banimento",
        "circulo": 3,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "1d3+1 rodadas",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Expulsa criatura não nativa ou rompe conexão de morto-vivo (0 PV). Se passar, fica enjoado. CD aumenta com itens opostos[cite: 306, 307].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+0 PM",
                "descricao": "Devolve automaticamente criatura conjurada (sem resistência).", "efeitos": {}}
        ]
    },
    "Barragem Elemental de Vectorius": {
        "nome": "Barragem Elemental de Vectorius",
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "4 esferas elementais (Raio 12m)",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "4 esferas (ácido, elétrica, fogo, frio) explodem causando 6d6 de dano cada e efeitos (vulnerável, atordoado, em chamas, lento)[cite: 315, 316, 319].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM",
                "descricao": "Aumenta dano de cada esfera em +2d6.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Muda dano para essência (mantém efeitos secundários).", "efeitos": {}}
        ]
    },
    "Bênção": {
        "nome": "Bênção",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Aliados",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Abençoa aliados com +1 em testes de ataque e rolagens de dano. Anula Perdição[cite: 326, 327].",
        "efeitos": {
            "ataque_bonus_magia": 1,
            "dano_bonus_magia": 1
        },
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Muda alvo para 1 cadáver (preserva por 1 semana).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta bônus em +1.",
                "efeitos": {"ataque_bonus_magia": 1, "dano_bonus_magia": 1}}
        ]
    },
    "Bola de Fogo": {
        "nome": "Bola de Fogo",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Explosão causa 6d6 pontos de dano de fogo em criaturas e objetos livres na área[cite: 333].",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o dano em +2d6.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Muda para Esfera Flamejante (duração cena, move 9m, 3d6 dano).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Muda duração para 1 dia (pedra flamejante/granada).", "efeitos": {}}
        ]
    },
    "Buraco Negro": {
        "nome": "Buraco Negro",
        "circulo": 5,
        "escola": "Convocação",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Longo",
        "alvo_area": "Buraco negro",
        "duracao": "3 rodadas",
        "resistencia": "Fortitude parcial",
        "descricao": "Cria vácuo que suga tudo. Criaturas devem fazer Fortitude ou são puxadas 30m e caem. Se terminar turno no centro, é sugada para sempre[cite: 345, 350, 355].",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Caminhos da Natureza": {
        "nome": "Caminhos da Natureza",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Criaturas escolhidas",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "As criaturas afetadas recebem deslocamento +3m e ignoram penalidades por terreno difícil em terrenos naturais.",
        "efeitos": {
            "deslocamento_bonus": 3
        },
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Muda alcance para pessoal. Recebe +5 em Sobrevivência para se orientar.",
                "efeitos": {"pericia_sobrevivencia_bonus": 5}},
            {"custo": "+1 PM", "descricao": "A CD para rastrear os alvos aumenta em +10.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus de deslocamento em +3m.",
                "efeitos": {"deslocamento_bonus": 3}}
        ]
    },
    "Campo Antimagia": {
        "nome": "Campo Antimagia",
        "circulo": 4,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você (esfera de 3m)",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Cria uma barreira invisível de 3m. Qualquer magia ou item mágico na área é suprimido. Criaturas convocadas desaparecem.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Muda o efeito para que você não seja afetado.", "efeitos": {}}
        ]
    },
    "Campo de Força": {
        "nome": "Campo de Força",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria película protetora. Você recebe 30 PV temporários.",
        "efeitos": {
            "pv_temporarios": 30
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda execução para reação e duração para instantânea. Recebe RD 30 contra o próximo dano.",
                "efeitos": {"rd_temporaria": 30}},
            {"custo": "+3 PM", "descricao": "Muda os PV temporários ou a RD para 50. Requer 3º círculo.",
                "efeitos": {"pv_temporarios": 50}},  # Substitui o valor base
            {"custo": "+7 PM", "descricao": "Muda os PV temporários ou a RD para 70. Requer 4º círculo.",
                "efeitos": {"pv_temporarios": 70}},
            {"custo": "+7 PM",
                "descricao": "Cria esfera imóvel (prisão de força) ao redor de alvo. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Como aprimoramento anterior, mas pode flutuar a esfera. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Camuflagem Ilusória": {
        "nome": "Camuflagem Ilusória",
        "circulo": 2,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "O alvo recebe camuflagem leve (20% de chance de falha em ataques contra ele).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Muda para sustentada. Aumenta para camuflagem total (50%).", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Muda alcance para curto e alvo para criaturas escolhidas. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Chuva de Meteoros": {
        "nome": "Chuva de Meteoros",
        "circulo": 5,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Longo",
        "alvo_area": "Quadrado com 18m de lado",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Meteoros caem causando 15d6 impacto + 15d6 fogo. Deixa criaturas caídas e agarradas. Terreno difícil e camuflagem leve.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d6 impacto e +2d6 fogo.", "efeitos": {}}
        ]
    },
    "Círculo da Justiça": {
        "nome": "Círculo da Justiça",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Esfera com 9m de raio",
        "duracao": "1 dia",
        "resistencia": "Vontade parcial",
        "descricao": "Criaturas na área sofrem -10 em Acrobacia, Enganação, Furtividade e Ladinagem e não podem mentir. Se passar, penalidade -5 e pode mentir.",
        "efeitos": {
            "pericia_acrobacia_penalidade": -10,
            "pericia_enganacao_penalidade": -10,
            "pericia_furtividade_penalidade": -10,
            "pericia_ladinagem_penalidade": -10
        },
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Revela criaturas invisíveis (Olho da Verdade).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Aumenta penalidade para -20 (falha) ou -10 (sucesso). Requer 4º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Muda duração para permanente (Custo T$ 5.000).", "efeitos": {}}
        ]
    },
    "Círculo da Restauração": {
        "nome": "Círculo da Restauração",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Esfera com 3m de raio",
        "duracao": "5 rodadas",
        "resistencia": "",
        "descricao": "Cria círculo de luz. Criatura viva que termine turno dentro recupera 3d8+3 PV e 1 PM. Mortos-vivos sofrem dano/perda de PM.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Aumenta regeneração de PV em 1d8+1.", "efeitos": {}}
        ]
    },
    "Cólera de Azgher": {
        "nome": "Cólera de Azgher",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Fulgor dourado causa 10d6 fogo (10d8 em mortos-vivos), cega (1d4 rodadas) e deixa em chamas.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Aumenta dano em +2d6 (+2d8 vs mortos-vivos).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta a área em +6m de raio.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Dissipa magias de necromancia na área. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Coluna de Chamas": {
        "nome": "Coluna de Chamas",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Cilindro com 3m raio e 30m altura",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Pilar de fogo sagrado causa 6d6 fogo + 6d6 luz.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta dano de fogo em +1d6.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta dano de luz em +1d6.", "efeitos": {}}
        ]
    },
    "Comando": {
        "nome": "Comando",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide",
        "duracao": "1 rodada",
        "resistencia": "Vontade anula",
        "descricao": "Dá uma ordem irresistível (Fuja, Largue, Pare, Senta, Venha).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda o alvo para 1 criatura.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Aumenta quantidade de alvos em +1.", "efeitos": {}}
        ]
    },
    "Compreensão": {
        "nome": "Compreensão",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura ou texto",
        "duracao": "Cena",
        "resistencia": "Vontade anula (veja texto)",
        "descricao": "Permite entender textos ou se comunicar com criaturas inteligentes. Pode sentir sentimentos de animais. Pode ler pensamentos (movimento).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda alcance para curto.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Muda alcance para curto e alvo para criaturas escolhidas (entende todas).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Pode vasculhar pensamentos para extrair informações. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda alcance para pessoal. Fala/escreve/entende qualquer idioma. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Comunhão com a Natureza": {
        "nome": "Comunhão com a Natureza",
        "circulo": 3,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Recebe 6d4 dados de auxílio para usar em testes de perícia em áreas naturais.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Descobre informações sobre a região (terreno, animais, etc). Instantânea.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta número de dados de auxílio em +2.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Muda tipo dos dados para d6.", "efeitos": {}},
            {"custo": "+8 PM", "descricao": "Muda tipo dos dados para d8.", "efeitos": {}}
        ]
    },
    "Conceder Milagre": {
        "nome": "Conceder Milagre",
        "circulo": 4,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Permanente até descarregada",
        "resistencia": "",
        "descricao": "Transfere uma magia sua de até 2º círculo para o alvo lançar sem custo de PM. Você sofre -3 PM temporários.",
        "efeitos": {
            "pm_temporarios_penalidade": -3
        },
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Muda círculo da magia para 3º e penalidade para -6 PM.",
                "efeitos": {"pm_temporarios_penalidade": -6}}
        ]
    },
    "Concentração de Combate": {
        "nome": "Concentração de Combate",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Livre",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "1 rodada",
        "resistencia": "",
        "descricao": "Ao fazer teste de ataque, rola dois dados e usa o melhor.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda execução para padrão e duração para cena. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Inimigos rolam 2 dados e usam o pior ao te atacar. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Muda execução para padrão, alcance curto, alvo criaturas, duração cena. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+14 PM", "descricao": "Duração 1 dia. Imune a surpreendido/desprevenido, +10 Defesa e Reflexos. Requer 5º círculo.",
                "efeitos": {"defesa_bonus_magia": 10, "resistencia_reflexos_bonus": 10}}
        ]
    },
    "Condição": {
        "nome": "Condição",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Até 5 criaturas",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Você sabe a posição e status (PV, condições, magias) dos alvos.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Muda duração para 1 dia.", "efeitos": {}}
        ]
    },
    "Conjurar Elemental": {
        "nome": "Conjurar Elemental",
        "circulo": 4,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Completa",
        "alcance": "Médio",
        "alvo_area": "Parceiro elemental",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Transforma elemento em elemental Grande (Parceiro Destruidor + 1 Mestre).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Elemental Enorme, recebe 2 tipos de parceiro.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Convoca um de cada tipo (4 elementais). Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Conjurar Monstro": {
        "nome": "Conjurar Monstro",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "1 criatura conjurada",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Conjura monstro Pequeno (Construto de energia). Gasta ação para dar ordens (Mover, Atacar, Lançar Magia).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Monstro ganha deslocamento escalada ou natação.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta deslocamento em +3m.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Muda tipo de dano (ácido, fogo, frio, elétrico).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Aumenta tamanho para Médio (Melhores stats).", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Aumenta tamanho para Grande. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Aumenta tamanho para Enorme. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+14 PM", "descricao": "Aumenta tamanho para Colossal. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Conjurar Mortos-Vivos": {
        "nome": "Conjurar Mortos-Vivos",
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "6 mortos-vivos (esqueletos)",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Cria 6 esqueletos capangas. Ação de movimento para andar, padrão para atacar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Aumenta número de mortos-vivos em +1.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Conjura Carniçais. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Conjura Sombras. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Consagrar": {
        "nome": "Consagrar",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Esfera com 9m de raio",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Enche área de energia positiva. Cura de luz maximizada. Mortos-vivos sofrem -2 testes e Defesa.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Mortos-vivos sofrem -2 testes e Defesa (Texto base já diz isso, pode ser cumulativo ou erro do resumo, PDF diz 'além do normal' para penalidade).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta penalidades para mortos-vivos em -1.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Execução 1h, permanente. Custo T$ 1.000. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Contato Extraplanar": {
        "nome": "Contato Extraplanar",
        "circulo": 3,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Recebe 6d6 dados de auxílio. Ao rolar '6', perde 1 PM (entidade suga mana).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta número de dados em +1.", "efeitos": {}},
            {"custo": "+8 PM", "descricao": "Dados viram d12. Rolar 12 perde 2 PM. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Controlar a Gravidade": {
        "nome": "Controlar a Gravidade",
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Cubo de 12m",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Altera gravidade: Aumentar (fatigado/caído), Inverter (cai p/ cima) ou Reduzir (flutua, +20 atletismo salto).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Controlar Água": {
        "nome": "Controlar Água",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Esfera com 30m de raio",
        "duracao": "Cena",
        "resistencia": "Veja texto",
        "descricao": "Controla água: Congelar, Derreter, Enchente, Evaporar (dano em elementais), Partir.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano do efeito Evaporar em +2d8.", "efeitos": {}}
        ]
    },
    "Controlar Fogo": {
        "nome": "Controlar Fogo",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Veja texto",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Controla chamas: Chamejar (+1d6 dano), Esquentar (1d6/rodada), Extinguir, Modelar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Muda para sustentada/Reflexos. Efeito Labaredas (ataque 4d6 fogo).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d6.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Muda alvo para criatura de fogo (dano ou morte).", "efeitos": {}}
        ]
    },
    "Controlar Madeira": {
        "nome": "Controlar Madeira",
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Objeto de madeira Grande ou menor",
        "duracao": "Cena",
        "resistencia": "Vontade anula (se objeto estiver em posse)",
        "descricao": "Fortalecer (aumenta passo dano, +2 defesa escudo), Modelar, Repelir, Retorcer (inutiliza).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Vira árvore Grande (disfarce).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Área 9m. Vegetação cria terreno difícil e causa dano.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Afeta alvo Enorme. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+12 PM",
                "descricao": "Afeta alvo Colossal. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Controlar o Clima": {
        "nome": "Controlar o Clima",
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Completa",
        "alcance": "2km",
        "alvo_area": "Esfera com 2km de raio",
        "duracao": "4d12 horas",
        "resistencia": "",
        "descricao": "Muda o clima da área (chuva, neve, ventos, névoas).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "(Druidas) Raio 3km, duração 1d4 dias.", "efeitos": {}}
        ]
    },
    "Controlar o Tempo": {
        "nome": "Controlar o Tempo",
        "circulo": 5,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Veja texto",
        "duracao": "Veja texto",
        "resistencia": "",
        "descricao": "Efeitos poderosos: Congelar o Tempo (3 rodadas só pra você), Saltar no Tempo (vai pro futuro), Voltar no Tempo (refaz rodada).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Controlar Plantas": {
        "nome": "Controlar Plantas",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Quadrado com 9m de lado",
        "duracao": "Cena",
        "resistencia": "Reflexos anula",
        "descricao": "Plantas enredam criaturas. Terreno difícil.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Anima planta (sem dano).", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Poda plantas (remove terreno difícil/camuflagem).", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Falha na resistência também deixa imóvel.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Fala com plantas (Diplomacia).", "efeitos": {}}
        ]
    },
    "Controlar Terra": {
        "nome": "Controlar Terra",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "9 cubos de 1,5m",
        "duracao": "Instantânea",
        "resistencia": "Veja texto",
        "descricao": "Manipula terra/pedra: Amolecer (desabamento ou lodo), Modelar, Solidificar (prende).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta área em +2 cubos.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Fusão com a terra (esconder-se).", "efeitos": {}}
        ]
    },
    "Convocação Instantânea": {
        "nome": "Convocação Instantânea",
        "circulo": 3,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Ilimitado",
        "alvo_area": "1 objeto preparado",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Invoca objeto preparado com runa para sua mão.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Pode enviar objeto de volta.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Esconde baú no Éter (Baú Secreto). Custo T$ 1.000 + T$ 100.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Muda para objeto de até 10 espaços.", "efeitos": {}}
        ]
    },
    "Crânio Voador de Vladislav": {
        "nome": "Crânio Voador de Vladislav",
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Crânio causa 4d8+4 trevas e deixa abalado (ou apavorado). Explosão afeta adjacentes (abalado).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d8+1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}}
        ]
    },
    "Criar Elementos": {
        "nome": "Criar Elementos",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Elemento escolhido",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Cria porção de elemento real (Água, Ar, Fogo, Terra). Pode causar dano pequeno ou utilidade.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta quantidade do elemento.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Arremessa elemento (ataque 2d4 impacto).", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Aumenta dano inicial do fogo em +1d6.", "efeitos": {}}
        ]
    },
    "Criar Ilusão": {
        "nome": "Criar Ilusão",
        "circulo": 1,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "4 cubos de 1,5m",
        "duracao": "Cena",
        "resistencia": "Vontade desacredita",
        "descricao": "Cria ilusão visual ou sonora simples.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Duração sustentada (move imagem).", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta efeito em +1 cubo.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Imagem + Som.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Sons complexos/volume alto.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Odores e temperatura.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Alcance longo, esfera 30m (Som de multidão). Dificulta conjuração. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Sensações táteis (barra passagem). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Sustentada, modifica ilusão livremente. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Cúpula de Repulsão": {
        "nome": "Cúpula de Repulsão",
        "circulo": 4,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "Vontade anula",
        "descricao": "Cúpula impede aproximação (3m) de tipo de criatura escolhido. Se falhar, perde ação.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta raio para 4,5m.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Também repele ataques à distância. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Curar Ferimentos": {
        "nome": "Curar Ferimentos",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Recupera 2d8+2 PV.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Causa 1d8 luz em morto-vivo.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta cura em +1d8+1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Remove fadiga.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda alcance para curto.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Alcance curto, criaturas escolhidas.", "efeitos": {}}
        ]
    },
    "Deflagração de Mana": {
        "nome": "Deflagração de Mana",
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 15m de raio",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Emana energia pura. Causa 150 pontos de dano de essência. Itens mágicos tornam-se mundanos por 1 dia.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta o dano em +10.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Afeta apenas criaturas a sua escolha.", "efeitos": {}}
        ]
    },
    "Desejo": {
        "nome": "Desejo",
        "circulo": 5,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Veja texto",
        "alvo_area": "Veja texto",
        "duracao": "Veja texto",
        "resistencia": "Veja texto",
        "descricao": "Altera a realidade. Dissipa magias, transporta grupo, desfaz acontecimento recente, cria item (sacrifício PM), duplica magia, aumenta atributo (sacrifício PM).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Desespero Esmagador": {
        "nome": "Desespero Esmagador",
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 6m",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Humanoides ficam fracos e frustrados pela cena (ou 1 rodada se passar).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Condições mudam para debilitado e esmorecido.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Afeta qualquer tipo de criatura.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Falha na resistência deixa pasmo por 1 rodada. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Desintegrar": {
        "nome": "Desintegrar",
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura ou objeto",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Raio causa 10d12 de dano de essência (2d12 se passar). Se reduzir a 0 PV, alvo vira pó.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Aumenta dano total em +2d12 e dano mínimo em +1d12.", "efeitos": {}}
        ]
    },
    "Despedaçar": {
        "nome": "Despedaçar",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura ou objeto Pequeno",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Som agudo causa 1d8+2 impacto e atordoa. Construtos/objetos sofrem dobro e ignoram RD.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d8+2.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda alvo para objeto Médio. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda alvo para objeto Grande. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Alcance pessoal, esfera 6m. Afeta tudo na área.", "efeitos": {}}
        ]
    },
    "Despertar Consciência": {
        "nome": "Despertar Consciência",
        "circulo": 3,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Toque",
        "alvo_area": "1 animal ou planta",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Desperta consciência. Alvo vira parceiro veterano (Int -1, fala).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM",
                "descricao": "Alvo escultura inanimada (construto).", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Duração permanente (Penalidade -3 PM).", "efeitos": {
                "pm_temporarios_penalidade": -3}}
        ]
    },
    "Detectar Ameaças": {
        "nome": "Detectar Ameaças",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 18m de raio",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Intuição sobre perigos. Teste de Percepção revela origem/direção de inimigos ou armadilhas.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Descobre raça/espécie e poder (aura) da criatura.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Não fica surpreendido, +5 resistência vs armadilhas. Requer 2º círculo.",
                "efeitos": {"resistencia_armadilhas_bonus": 5}}
        ]
    },
    "Dificultar Detecção": {
        "nome": "Dificultar Detecção",
        "circulo": 3,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura ou objeto",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Oculta alvo de detecção mágica (exige Vontade do conjurador inimigo).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Muda alvo para cubo de 9m.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Muda duração para 1 semana.", "efeitos": {}}
        ]
    },
    "Disfarce Ilusório": {
        "nome": "Disfarce Ilusório",
        "circulo": 1,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Vontade desacredita",
        "descricao": "Muda aparência. Recebe +10 em Enganação para disfarce.",
        "efeitos": {
            "pericia_enganacao_disfarce_bonus": 10
        },
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Pequena alteração inofensiva. Duração 1 semana.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Muda alvo para objeto (+10 falsificação).", "efeitos": {
                "pericia_enganacao_falsificacao_bonus": 10}},
            {"custo": "+2 PM", "descricao": "Inclui odores/sensações. Bônus sobe para +20.",
                "efeitos": {"pericia_enganacao_disfarce_bonus": 20}},
            {"custo": "+3 PM", "descricao": "Afeta criaturas escolhidas. Requer 2º círculo.", "efeitos": {}}
        ]
    },
    "Dispersar as Trevas": {
        "nome": "Dispersar as Trevas",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Instantânea/Cena",
        "resistencia": "",
        "descricao": "Dissipa magias de 3º círculo ou menor. Aliados: +4 Resistência, RD Trevas 10. Inimigos: cegos 1d4 rodadas. Anula 'Anular a Luz'.",
        "efeitos": {
            "resistencia_bonus_magia": 4,
            "rd_trevas": 10
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta bônus nas resistências em +1.",
                "efeitos": {"resistencia_bonus_magia": 1}},
            {"custo": "+4 PM", "descricao": "Alvo 1 criatura, imune a trevas.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Dissipa até 4º círculo. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Dissipa até 5º círculo. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Dissipar Magia": {
        "nome": "Dissipar Magia",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura/objeto ou esfera 3m",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Dissipa magias ativas (Teste Misticismo). Item mágico vira mundano temporariamente.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+12 PM",
                "descricao": "Disjunção (Esfera 9m). Dissipa tudo automático e itens viram mundanos pela cena. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Duplicata Ilusória": {
        "nome": "Duplicata Ilusória",
        "circulo": 4,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Cópia ilusória",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria cópia sua. Você pode ver/ouvir/falar e lançar magias através dela.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Cria uma cópia adicional.", "efeitos": {}}
        ]
    },
    "Enfeitiçar": {
        "nome": "Enfeitiçar",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "Alvo fica enfeitiçado (atitude melhora). Hostis recebem +5 na resistência.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Sugestão: Sugere ação e alvo obedece.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda alvo para espírito ou monstro. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta todos os alvos no alcance.", "efeitos": {}}
        ]
    },
    "Engenho de Mana": {
        "nome": "Engenho de Mana",
        "circulo": 5,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Disco de energia",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Disco faz contramágica automática. Se vencer, absorve PM.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Disco flutua adjacente a você.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Muda duração para 1 dia.", "efeitos": {}}
        ]
    },
    "Enxame de Pestes": {
        "nome": "Enxame de Pestes",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Médio",
        "alvo_area": "1 enxame Médio",
        "duracao": "Sustentada",
        "resistencia": "Fortitude reduz metade",
        "descricao": "Cria enxame (insetos/ratos) que causa 2d12 corte em quem estiver no espaço.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d12.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Criaturas maiores (gatos/kobolds). 3d12 dano. Reflexos reduz.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Aumenta número de enxames em +1. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Criaturas elementais. 5d12 dano energia. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Enxame Rubro de Ichabod": {
        "nome": "Enxame Rubro de Ichabod",
        "circulo": 3,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 enxame Grande (3m)",
        "duracao": "Sustentada",
        "resistencia": "Reflexos reduz metade",
        "descricao": "Enxame da Tormenta causa 4d12 ácido.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Falha na resistência deixa agarrado.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d12.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda dano para trevas.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Enxame Enorme (6m).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Ganha voo e ocupa cubo.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Multiplicação (cria novos enxames). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Erupção Glacial": {
        "nome": "Erupção Glacial",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Quadrado de 6m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Estacas de gelo causam 4d6 corte + 4d6 frio e deixam caído. Terreno difícil e cobertura.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta dano frio em +2d6 e corte em +2d6.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Tempestade de Granizo (Cilindro 6m, sustentada). 3d6 impacto + 3d6 frio. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Escudo da Fé": {
        "nome": "Escudo da Fé",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Reação",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "1 turno",
        "resistencia": "",
        "descricao": "Escudo místico fornece +2 na Defesa.",
        "efeitos": {
            "defesa_bonus_magia": 2
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda execução para padrão, alcance toque, duração cena.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Fornece camuflagem leve contra ataques à distância.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta bônus na Defesa em +1.",
                "efeitos": {"defesa_bonus_magia": 1}},
            {"custo": "+2 PM",
                "descricao": "Vínculo protetor (divide dano com conjurador). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Muda duração para 1 dia. Requer 2º círculo.", "efeitos": {}}
        ]
    },
    "Esculpir Sons": {
        "nome": "Esculpir Sons",
        "circulo": 2,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura ou objeto",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "Altera sons emitidos pelo alvo (omite ou transforma).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}}
        ]
    },
    "Escuridão": {
        "nome": "Escuridão",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 objeto",
        "duracao": "Cena",
        "resistencia": "Vontade anula (objeto em posse)",
        "descricao": "Objeto emana sombras (6m raio). Camuflagem leve. Anula Luz.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta área em +1,5m.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Muda para escuridão total (camuflagem total, bloqueia visão).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Alvo criatura (cega pela cena). Fortitude parcial (1 rodada). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Muda duração para 1 dia.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Alcance pessoal. Você recebe +10 Furtividade e camuflagem leve. Requer 2º círculo.",
                "efeitos": {"pericia_furtividade_bonus": 10}}
        ]
    },
    "Explosão Caleidoscópica": {
        "nome": "Explosão Caleidoscópica",
        "circulo": 4,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Luzes e sons desorientam. Efeito varia com nível/ND (inconsciente, atordoado, enjoado).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Explosão de Chamas": {
        "nome": "Explosão de Chamas",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 6m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Leque de chamas causa 2d6 dano de fogo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Pequena explosão inofensiva ou acende velas.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta dano em +1d6.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Falha na resistência deixa em chamas.", "efeitos": {}}
        ]
    },
    "Ferver Sangue": {
        "nome": "Ferver Sangue",
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Sustentada",
        "resistencia": "Fortitude parcial",
        "descricao": "Sangue ferve. 4d8 fogo + enjoado por rodada. Morte explode causando dano em área.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d8.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Alvo criaturas escolhidas. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Físico Divino": {
        "nome": "Físico Divino",
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Aumenta um atributo físico (For, Des, Con) em +2.",
        "efeitos": {
            "atributo_fisico_bonus": 2
        },
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Alcance curto, criaturas escolhidas.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta os três atributos físicos em +2. Requer 3º círculo.",
                "efeitos": {"atributo_forca_bonus": 2, "atributo_destreza_bonus": 2, "atributo_constituicao_bonus": 2}},
            {"custo": "+7 PM", "descricao": "Bônus aumenta para +4. Requer 4º círculo.",
                "efeitos": {"atributo_fisico_bonus": 4}},
            {"custo": "+12 PM", "descricao": "Aumenta os três atributos físicos em +4. Requer 5º círculo.",
                "efeitos": {"atributo_forca_bonus": 4, "atributo_destreza_bonus": 4, "atributo_constituicao_bonus": 4}}
        ]
    },
    "Flecha Ácida": {
        "nome": "Flecha Ácida",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura ou objeto",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Projétil causa 4d6 ácido. Falha causa +2d6 ácido por 2 rodadas. Dano dobrado em objetos.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Corrói armadura/escudo (-1 Defesa permanente).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta redução de defesa em +1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano inicial e contínuo em +1d6.", "efeitos": {}}
        ]
    },
    "Forma Etérea": {
        "nome": "Forma Etérea",
        "circulo": 4,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Vai para o plano etéreo. Invisível, incorpóreo, voo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM",
                "descricao": "Leva até 5 criaturas voluntárias (mãos dadas). Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Fúria do Panteão": {
        "nome": "Fúria do Panteão",
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Longo",
        "alvo_area": "Cubo de 90m",
        "duracao": "Sustentada",
        "resistencia": "Veja texto",
        "descricao": "Nuvem de tempestade. Efeitos variados por turno (Nevasca, Raios, Siroco, Trovões). Dano 10d6 ou 10d8.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Globo da Verdade de Gwen": {
        "nome": "Globo da Verdade de Gwen",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 globo",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Globo mostra cena vista até uma semana atrás por você ou criatura tocada.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Mostra cena de até um mês atrás.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Mostra cena de até um ano atrás.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Pode tocar cadáver (última cena vista).", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Cria 10 globos (mesma cena, alcance longo).", "efeitos": {}}
        ]
    },
    "Globo de Invulnerabilidade": {
        "nome": "Globo de Invulnerabilidade",
        "circulo": 3,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você (esfera de 3m)",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Detém magias de 2º círculo ou menor. Imóvel.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Afeta magias de até 3º círculo. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Afeta magias de até 4º círculo. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Guardião Divino": {
        "nome": "Guardião Divino",
        "circulo": 4,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Elemental de luz",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Invoca orbe de luz (100 pontos). Pode curar 1 PV/ponto ou remover condição (3 pontos).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Heroísmo": {
        "nome": "Heroísmo",
        "circulo": 3,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Alvo imune a medo, ganha 40 PV temporários e +4 ataque/dano contra maior ND.",
        "efeitos": {
            "pv_temporarios": 40,
            "ataque_bonus_magia": 4,
            "dano_bonus_magia": 4
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda o bônus para +6.",
                "efeitos": {"ataque_bonus_magia": 6, "dano_bonus_magia": 6}}
        ]
    },
    "Hipnotismo": {
        "nome": "Hipnotismo",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 animal ou humanoide",
        "duracao": "1d4 rodadas",
        "resistencia": "Vontade anula",
        "descricao": "Deixa o alvo fascinado. Combate dá +5 na resistência.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Duração 1 rodada, deixa pasmo.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Alvo não percebe que foi vítima.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Alvos escolhidos.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Duração sustentada.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta espíritos e monstros. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta construtos e mortos-vivos. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Ilusão Lacerante": {
        "nome": "Ilusão Lacerante",
        "circulo": 3,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Cubo de 9m",
        "duracao": "Sustentada",
        "resistencia": "Vontade anula",
        "descricao": "Cria ilusão de perigo. Falha em Vontade causa 3d6 dano psíquico/rodada.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Cubo de 90m. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Imagem Espelhada": {
        "nome": "Imagem Espelhada",
        "circulo": 1,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria 3 cópias. +6 Defesa. Erro remove cópia (-2 Defesa).",
        "efeitos": {
            "defesa_bonus_magia": 6
        },
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Aumenta cópias em +1 (+2 Defesa).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Destruir cópia ofusca atacante. Requer 2º círculo.", "efeitos": {}}
        ]
    },
    "Imobilizar": {
        "nome": "Imobilizar",
        "circulo": 3,
        "escola": "Encantamento",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide ou animal",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Deixa paralisado. Se passar, fica lento. Teste por rodada para se libertar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Afeta espírito.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Afeta 1 criatura (qualquer tipo). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Infligir Ferimentos": {
        "nome": "Infligir Ferimentos",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude reduz à metade",
        "descricao": "Causa 2d8+2 dano de trevas (cura mortos-vivos).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Falha deixa fraco.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d8+1.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Resistência nenhuma. Ataque corpo a corpo como parte.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Alcance curto, criaturas escolhidas.", "efeitos": {}}
        ]
    },
    "Intervenção Divina": {
        "nome": "Intervenção Divina",
        "circulo": 5,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Veja texto",
        "alvo_area": "Veja texto",
        "duracao": "Veja texto",
        "resistencia": "Veja texto",
        "descricao": "Pede ajuda direta à divindade. Cura total, dissipa magia, cria item (custo extra), ressuscita (1 rodada), protege cidade, etc.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Invisibilidade": {
        "nome": "Invisibilidade",
        "circulo": 2,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Livre",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "1 rodada",
        "resistencia": "",
        "descricao": "Fica invisível (+10 Furtividade, camuflagem total). Ação hostil dissipa.",
        "efeitos": {
            "pericia_furtividade_bonus": 10
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Ação padrão, toque, alvo criatura/objeto.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Duração cena. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Esfera de invisibilidade (3m raio). Sustentada. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Não dissipa com ação hostil. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Invulnerabilidade": {
        "nome": "Invulnerabilidade",
        "circulo": 5,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Barreira impenetrável. Escolha imunidade física (doenças, veneno, crítico, atordoado...) ou mental (medo, encantamento, ilusão...).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Alcance curto, alvo 1 criatura.", "efeitos": {}}
        ]
    },
    "Lágrimas de Wynna": {
        "nome": "Lágrimas de Wynna",
        "circulo": 5,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Alvo perde a habilidade de lançar magias arcanas pela cena (se falhar) ou 1 rodada (se passar).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda para esfera 6m e alvos escolhidos.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Execução 1 dia (ritual). Perda permanente de magia arcana. Sacrifício 1 PM.", "efeitos": {}}
        ]
    },
    "Lança Ígnea de Aleph": {
        "nome": "Lança Ígnea de Aleph",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Projétil de magma causa 4d6 fogo + 4d6 perfuração e deixa em chamas. Explosão atinge adjacentes (em chamas).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta dano inicial em +2d6 e dano em chamas em +1d6.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Duração cena. Cria 4 dardos flutuantes para disparar (ação livre, 1/rodada). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Legião": {
        "nome": "Legião",
        "circulo": 5,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Até 10 criaturas",
        "duracao": "Sustentada",
        "resistencia": "Vontade parcial",
        "descricao": "Domina a mente dos alvos, que obedecem cegamente. Teste por turno para se livrar (se passar, abalado 1 rodada).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}}
        ]
    },
    "Lendas e Histórias": {
        "nome": "Lendas e Histórias",
        "circulo": 3,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura, objeto ou local",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Descobre informações, estatísticas de jogo e magias ativas do alvo tocado.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Execução 1 dia, alcance ilimitado. Custo T$ 1.000.", "efeitos": {}}
        ]
    },
    "Leque Cromático": {
        "nome": "Leque Cromático",
        "circulo": 1,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 4,5m",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Luzes deixam atordoado (1 rodada) e ofuscado (cena). Vontade anula atordoamento.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Criaturas afetadas ficam vulneráveis pela cena.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta espíritos e monstros. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta construtos e mortos-vivos. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Libertação": {
        "nome": "Libertação",
        "circulo": 4,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Imune a restrição de movimento/paralisia. Pode usar habilidades de liberdade mesmo com armadura.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Caminha sobre líquidos.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Escolhe 20 em testes de Atletismo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Escolhe 20 em Acrobacia e usa sem treino.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta até 5 criaturas.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Dissipa Aprisionamento.", "efeitos": {}}
        ]
    },
    "Ligação Sombria": {
        "nome": "Ligação Sombria",
        "circulo": 4,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "1 criatura",
        "duracao": "1 dia",
        "resistencia": "Fortitude anula",
        "descricao": "Conecta seu corpo ao alvo. Se você sofre dano/condição, alvo sofre igual (se falhar em Fortitude). Termina se alvo cai a 0 PV.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM",
                "descricao": "Não termina a 0 PV (pode matar o alvo).", "efeitos": {}}
        ]
    },
    "Ligação Telepática": {
        "nome": "Ligação Telepática",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "2 criaturas voluntárias",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Elo mental permite comunicação a qualquer distância (mesmo plano).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta número de alvos em +1.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Permite ver/ouvir pelos sentidos do alvo. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Localização": {
        "nome": "Localização",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 90m de raio",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Indica direção/distância de criatura ou objeto específico ou tipo geral. Bloqueado por chumbo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Sabe norte e +5 Sobrevivência (orientação).", "efeitos": {
                "pericia_sobrevivencia_bonus": 5}},
            {"custo": "+5 PM", "descricao": "Aumenta área fator x10.", "efeitos": {}}
        ]
    },
    "Luz": {
        "nome": "Luz",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 objeto",
        "duracao": "Cena",
        "resistencia": "Vontade anula (se em posse)",
        "descricao": "Objeto ilumina raio de 6m. Anula Escuridão.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta raio em +3m.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Duração 1 dia.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Permanente (Custo T$ 50). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+0 PM",
                "descricao": "(Arcanos) Alvo criatura: ofuscada.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "(Arcanos) 4 globos flutuantes (Luzes Dançantes).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "(Divinos) Luz solar real (dano em vampiros, etc). Aliados estabilizam.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "(Divinos) Halo de luz: +10 Diplomacia, RD Trevas 10. Requer 2º círculo.", "efeitos": {
                "pericia_diplomacia_bonus": 10, "rd_trevas": 10}}
        ]
    },
    "Manto de Sombras": {
        "nome": "Manto de Sombras",
        "circulo": 3,
        "escola": "Ilusão",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Torna-se incorpóreo (só afetado por magia/armas mágicas). Vulnerável à luz (1 dano/rodada). Pode teletransportar entre sombras.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM",
                "descricao": "Alvo 1 criatura (toque). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Manto do Cruzado": {
        "nome": "Manto do Cruzado",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Escolha fixo ao aprender: Luz (Cura 2d8 em aliados, imune trevas, +2d8 dano luz) ou Trevas (Dano 4d8 em inimigos, cura metade).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Mão Poderosa de Talude": {
        "nome": "Mão Poderosa de Talude",
        "circulo": 4,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Mão gigante",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Mão protege (+5 Defesa) ou ataca (Agarrar/Empurrar +10, Esmagar 2d6+10).",
        "efeitos": {
            "defesa_bonus_magia": 5
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d6+5.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Bônus manobra +20. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Mapear": {
        "nome": "Mapear",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "Superfície plana",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria mapa da região (10km) ou andar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Alvo criatura, descobre caminho (Encontrar o Caminho).", "efeitos": {}}
        ]
    },
    "Marca da Obediência": {
        "nome": "Marca da Obediência",
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Universal",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "Grava marca e dá ordem. Criatura gasta turno obedecendo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Duração 1 dia. Teste a cada hora. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Falha na resistência causa 3d6 dano psíquico. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Marionete": {
        "nome": "Marionete",
        "circulo": 4,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Sustentada",
        "resistencia": "Fortitude anula",
        "descricao": "Controla ações físicas do alvo. Se falhar, você decide o que ele faz.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Mata-Dragão": {
        "nome": "Mata-Dragão",
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "2 rodadas",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 30m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Causa 20d12 dano de essência. Rolar 12 adiciona +1d12 (explosão).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta dano em +1d12.", "efeitos": {}}
        ]
    },
    "Mente Divina": {
        "nome": "Mente Divina",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Aumenta um atributo mental (Int, Sab, Car) em +2.",
        "efeitos": {
            "atributo_mental_bonus": 2
        },
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Alcance curto, alvos escolhidos.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta os três mentais em +2. Requer 3º círculo.", "efeitos": {
                "atributo_inteligencia_bonus": 2, "atributo_sabedoria_bonus": 2, "atributo_carisma_bonus": 2}},
            {"custo": "+7 PM", "descricao": "Bônus aumenta para +4. Requer 4º círculo.",
                "efeitos": {"atributo_mental_bonus": 4}},
            {"custo": "+12 PM", "descricao": "Aumenta os três mentais em +4. Requer 5º círculo.", "efeitos": {
                "atributo_inteligencia_bonus": 4, "atributo_sabedoria_bonus": 4, "atributo_carisma_bonus": 4}}
        ]
    },
    "Metamorfose": {
        "nome": "Metamorfose",
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Muda forma (humanoide ou animal). +20 Enganação (disfarce). Se animal, ganha bônus de Forma Selvagem (Druida) e perde magias.",
        "efeitos": {
            "pericia_enganacao_disfarce_bonus": 20
        },
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Ganha sentido (faro, visão penumbra/escuro).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Percepção às cegas. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Alvo 1 criatura (toque, Vontade anula).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Transformação em inofensivo (ovelha). Defesa 10, Desl 3m. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Forma Selvagem Aprimorada. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Forma Selvagem Superior. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+12 PM", "descricao": "Muda forma como ação livre por turno. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Miasma Mefítico": {
        "nome": "Miasma Mefítico",
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Nuvem de 6m de raio",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Causa 5d6 ácido e enjoado. Passar reduz metade/evita enjoo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Toque, alvo moribundo (0 PV). Se falhar, morre e dá +2 CD magias. Custo T$ 10.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d6.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Muda dano para trevas.", "efeitos": {}}
        ]
    },
    "Miragem": {
        "nome": "Miragem",
        "circulo": 3,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Cubo de 90m",
        "duracao": "1 dia",
        "resistencia": "Vontade desacredita",
        "descricao": "Muda aparência do terreno (estruturas, sons, cheiros). Pode criar armadilhas ilusórias.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM",
                "descricao": "Altera aparência de criaturas na área (Disfarce Ilusório).", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Permanente. Custo T$ 1.000. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Missão Divina": {
        "nome": "Missão Divina",
        "circulo": 3,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "1 semana",
        "resistencia": "Vontade anula",
        "descricao": "Obriga a cumprir tarefa. Se não se esforçar, acumula -2 em testes por dia.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Marca de punição (ativa com ação específica). Permanente. Penalidade -1 PM.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Duração 1 ano.", "efeitos": {}}
        ]
    },
    "Montaria Arcana": {
        "nome": "Montaria Arcana",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Criatura conjurada",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Cria cavalo de guerra veterano. Ignora terreno difícil. Usa Misticismo para Cavalgar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Aura de medo em animais (Vontade ou apavorado).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Permanente (-3 PM penalidade).", "efeitos": {
                "pm_temporarios_penalidade": -3}},
            {"custo": "+3 PM",
                "descricao": "Aumenta tamanho (Enorme/Colossal). Leva mais gente.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Parceiro Mestre. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Muralha de Ossos": {
        "nome": "Muralha de Ossos",
        "circulo": 4,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Muro de ossos (15x9m)",
        "duracao": "Cena",
        "resistencia": "Reflexos evita",
        "descricao": "Parede causa 4d8 corte ao surgir e agarra (Reflexos evita). Muro tem 40 PV, RD 10.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Aumenta tamanho (+15m comp, +3m alt).", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Esqueletos animados tentam agarrar quem escala/adjacente.", "efeitos": {}}
        ]
    },
    "Muralha Elemental": {
        "nome": "Muralha Elemental",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Muralha (30m) ou cúpula (3m)",
        "duracao": "Cena",
        "resistencia": "Veja texto",
        "descricao": "Fogo: 2d6 calor (perto), 8d6 atravessar. Gelo: 40 PV, RD 5. Romper causa 4d6 frio.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano atravessar em +2d6.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Dobra tamanho.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Essência (indestrutível, invisível). Bloqueia etéreos. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Névoa": {
        "nome": "Névoa",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Nuvem com 6m de raio e altura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Nuvem obscurece visão (camuflagem leve a 1,5m, total além de 3m). Vento dispersa.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Funciona sob a água (tinta).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Criaturas escolhidas enxergam através. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Nuvem fedorenta (Fortitude ou enjoado).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Nuvem ácida (2d4 ácido/rodada).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta dano ácido em +2d4.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Nuvem sólida. Deslocamento 3m, -2 ataque/dano.", "efeitos": {}}
        ]
    },
    "Oração": {
        "nome": "Oração",
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Todas as criaturas",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Aliados recebem +2 em testes e dano. Inimigos sofrem -2. Custo material T$ 20/PM.",
        "efeitos": {
            "ataque_bonus_magia": 2,
            "dano_bonus_magia": 2,
            "pericia_bonus_magia": 2
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta bônus aliados em +1.", "efeitos": {
                "ataque_bonus_magia": 1, "dano_bonus_magia": 1, "pericia_bonus_magia": 1}},
            {"custo": "+2 PM",
                "descricao": "Aumenta penalidade inimigos em -1.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Muda alcance para médio. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+12 PM",
                "descricao": "Muda duração para cena. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Orientação": {
        "nome": "Orientação",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "1 rodada",
        "resistencia": "",
        "descricao": "No próximo teste de perícia, rola dois dados e usa o melhor.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Duração cena. Rola 2 dados para um atributo específico. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Rola 2 dados para atributos físicos ou mentais. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta criaturas escolhidas. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Palavra Primordial": {
        "nome": "Palavra Primordial",
        "circulo": 5,
        "escola": "Encantamento",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura (nível menor que você)",
        "duracao": "Instantânea",
        "resistencia": "Vontade parcial",
        "descricao": "Pronuncia palavra do caos. Efeito à escolha: Atordoar (1d4+1 rodadas), Cegar, Matar (se falhar em Vontade e Fortitude).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Pele de Pedra": {
        "nome": "Pele de Pedra",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Ganha aspecto de rocha. Recebe RD 5.",
        "efeitos": {
            "rd_magia": 5
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Toque, alvo 1 criatura.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Duração 1 dia.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Pele de Aço: RD 10. Requer 4º círculo.",
                "efeitos": {"rd_magia": 10}},  # Substitui base
            {"custo": "+4 PM",
                "descricao": "Petrificar (transforma em estátua). Fortitude anula. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Petrificar permanente. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Perdição": {
        "nome": "Perdição",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Criaturas escolhidas",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": "Alvos sofrem -1 em ataques e dano. Anula Bênção.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta penalidade em -1.", "efeitos": {}}
        ]
    },
    "Poeira da Podridão": {
        "nome": "Poeira da Podridão",
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Nuvem com 6m de raio",
        "duracao": "Cena",
        "resistencia": "Fortitude (veja texto)",
        "descricao": "Nuvem causa 2d8+8 trevas por rodada. Falha impede cura por 1 rodada.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Possessão": {
        "nome": "Possessão",
        "circulo": 5,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "1 criatura",
        "duracao": "1 dia",
        "resistencia": "Vontade anula",
        "descricao": "Assume controle do corpo do alvo. Seu corpo fica inerte.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Ganha acesso a habilidades de raça/classe do alvo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Pode saltar entre corpos.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Permanente (destrói corpo original, imortalidade via trocas).", "efeitos": {}}
        ]
    },
    "Potência Divina": {
        "nome": "Potência Divina",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Aumenta tamanho, +4 Força, RD 10. Não pode lançar magias.",
        "efeitos": {
            "atributo_forca_bonus": 4,
            "rd_magia": 10
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta Força em +1.",
                "efeitos": {"atributo_forca_bonus": 1}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d8+4. Aumenta RD em +5.",
                "efeitos": {"rd_magia": 5, "dano_bonus_magia_extra": "1d8+4"}},
            {"custo": "+2 PM",
                "descricao": "Toque, alvo 1 criatura (mesma divindade).", "efeitos": {}}
        ]
    },
    "Premonição": {
        "nome": "Premonição",
        "circulo": 4,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Uma vez por rodada, pode rolar novamente um teste recém realizado (aceita o novo).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Reação, curto, 1 criatura. Obriga a rerrolar (Vontade nega se involuntário).", "efeitos": {}},
            {"custo": "+10 PM", "descricao": "Duração 1 dia.", "efeitos": {}}
        ]
    },
    "Primor Atlético": {
        "nome": "Primor Atlético",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Recebe deslocamento +9m e +10 em Atletismo.",
        "efeitos": {
            "deslocamento_bonus": 9,
            "pericia_atletismo_bonus": 10
        },
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "+20 Atletismo (salto). Total +30.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Escala paredes/tetos sem testes.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Salto de investida (Movimento, pessoal, instantânea).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Rola 2 dados em perícias físicas (For, Des, Con). Requer 2º círculo.", "efeitos": {}}
        ]
    },
    "Profanar": {
        "nome": "Profanar",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Esfera com 9m de raio",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Enche área de energia negativa. Dano de trevas maximizado. Anula Consagrar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Mortos-vivos recebem +2 Defesa e testes.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Aumenta bônus mortos-vivos em +1.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Execução 1h, permanente. Custo T$ 1.000. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Projetar Consciência": {
        "nome": "Projetar Consciência",
        "circulo": 5,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Ilimitado",
        "alvo_area": "Local ou criatura conhecidos",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Consciência sai do corpo. Forma fantasmagórica invisível, voo 18m, observa local.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+10 PM",
                "descricao": "Projeção pode lançar magias (sem custo material).", "efeitos": {}}
        ]
    },
    "Proteção contra Magia": {
        "nome": "Proteção contra Magia",
        "circulo": 3,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Recebe +5 em testes de resistência contra magias.",
        "efeitos": {
            "resistencia_magia_bonus": 5
        },
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Bônus aumenta para +10. Requer 4º círculo.",
                "efeitos": {"resistencia_magia_bonus": 10}},
            {"custo": "+4 PM", "descricao": "Imunidade a uma escola de magia. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Imunidade a duas escolas de magia. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Proteção Divina": {
        "nome": "Proteção Divina",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Barreira fornece +2 em testes de resistência.",
        "efeitos": {
            "resistencia_bonus_magia": 2
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta bônus em +1.",
                "efeitos": {"resistencia_bonus_magia": 1}},
            {"custo": "+2 PM",
                "descricao": "Reação, +5 no próximo teste (cumulativo).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta aliados em esfera 3m. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Imune a efeitos mentais e de medo. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Purificação": {
        "nome": "Purificação",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Remove uma condição prejudicial (ex: abalado, cego, enjoado, paralisado...).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Recupera PV perdidos por veneno.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Remove todas as condições listadas.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Solta item amaldiçoado.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Dissipa encantamento/necromancia/transmutação nocivos. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Queda Suave": {
        "nome": "Queda Suave",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Reação",
        "alcance": "Curto",
        "alvo_area": "1 criatura ou objeto Grande",
        "duracao": "Até chegar ao solo",
        "resistencia": "",
        "descricao": "Cai lentamente (18m/rodada), não sofre dano. Projéteis causam metade.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Levita objeto Minúsculo (Mão Mágica).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta até 10 alvos.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta limite de tamanho.", "efeitos": {}}
        ]
    },
    "Raio do Enfraquecimento": {
        "nome": "Raio do Enfraquecimento",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Fortitude parcial",
        "descricao": "Raio deixa fatigado (se falhar) ou vulnerável (se passar).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Toque, Fortitude anula, fatigado.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Exausto (falha) ou Fatigado (sucesso). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Alvo criaturas escolhidas. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Raio Polar": {
        "nome": "Raio Polar",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Raio causa 10d8 frio e deixa paralisado (gelo). Passar reduz metade e deixa lento.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Aumenta dano em +2d8.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Explosão (esfera 6m).", "efeitos": {}}
        ]
    },
    "Raio Solar": {
        "nome": "Raio Solar",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Linha de 30m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos parcial",
        "descricao": "Causa 4d8 luz (4d12 mortos-vivos) e ofusca.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Facho de luz (lanterna).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Aumenta dano/cura em +1d8 (+1d12).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Cura aliados vivos (4d8 PV).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Cega por 1d4 rodadas na falha.", "efeitos": {}}
        ]
    },
    "Reanimação Impura": {
        "nome": "Reanimação Impura",
        "circulo": 5,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Toque",
        "alvo_area": "1 criatura morta",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Reanima morto recente como morto-vivo temporário. Mantém habilidades.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Refúgio": {
        "nome": "Refúgio",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Domo de 6m raio",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Domo transparente dentro/opaco fora. Protege clima, camuflagem total.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Fumaça escura (bloqueia visão/audição de fora).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Cabana segura (Recuperação confortável). Paredes RD 5.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Espaço extradimensional (caverna). Requer 3º círculo.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Mansão extradimensional (Recuperação luxuosa). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Relâmpago": {
        "nome": "Relâmpago",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Linha de 30m",
        "duracao": "Instantânea",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Raio causa 6d6 eletricidade.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Vários relâmpagos (alvos escolhidos). Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Relâmpago Flamejante de Reynard": {
        "nome": "Relâmpago Flamejante de Reynard",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "2 rodadas",
        "alcance": "Médio",
        "alvo_area": "Bolas de fogo e relâmpagos",
        "duracao": "Sustentada",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Mãos carregam fogo e raio. Dispara Bola de Fogo (10d6) ou Relâmpago (10d6) com mov. Ou mistura (20d12) e encerra.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano rajadas +1d6 e mista +2d12.", "efeitos": {}}
        ]
    },
    "Réquiem": {
        "nome": "Réquiem",
        "circulo": 5,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Criaturas escolhidas",
        "duracao": "Sustentada",
        "resistencia": "Vontade anula",
        "descricao": "Cria ilusão temporal. Vítima acha que não agiu e repete ação anterior com -5 cumulativo.",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Resistência a Energia": {
        "nome": "Resistência a Energia",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Concede RD 10 contra um tipo de energia (ácido, fogo, frio, etc).",
        "efeitos": {
            "rd_energia_magia": 10
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta RD em +5.",
                "efeitos": {"rd_energia_magia": 5}},
            {"custo": "+2 PM",
                "descricao": "Duração 1 dia. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Alcance curto, criaturas escolhidas. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "RD contra todos os tipos. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Imunidade a um tipo. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Rogar Maldição": {
        "nome": "Rogar Maldição",
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Sustentada",
        "resistencia": "Fortitude anula",
        "descricao": "Amaldiçoa: Debilidade (esmorecido, sem magia), Doença, Fraqueza (debilitado/lento), Isolamento (sentidos).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Escolhe +1 efeito. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Permanente, resistência parcial (dura 1 rodada). Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Roubar a Alma": {
        "nome": "Roubar a Alma",
        "circulo": 5,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Permanente",
        "resistencia": "Vontade parcial",
        "descricao": "Aprisiona alma em objeto (T$ 1000/nível). Corpo inerte. Sacrifício 1 PM.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Objeto detém PM do alvo para você usar.", "efeitos": {}},
            {"custo": "+10 PM",
                "descricao": "Você possui o corpo vazio (Reação).", "efeitos": {}}
        ]
    },
    "Runa de Proteção": {
        "nome": "Runa de Proteção",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 2,
        "execucao": "1 hora",
        "alcance": "Toque",
        "alvo_area": "Área de 6m raio (armadilha)",
        "duracao": "Permanente até descarregada",
        "resistencia": "Reflexos reduz à metade",
        "descricao": "Escreve runa (T$ 200). Explode ao toque/aproximação: 6d6 dano.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Pessoal/Você. Armazena magia de 1º círculo para disparar como reação.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Armazena magia de 2º círculo. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Salto Dimensional": {
        "nome": "Salto Dimensional",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Você",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Transporta você para ponto visível ou imaginado. Não age até próxima rodada.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda alcance para médio.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Leva criatura voluntária (toque).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Execução reação. +5 Defesa/Reflexos contra ataque, depois salta.",
                "efeitos": {"defesa_bonus_magia": 5, "resistencia_reflexos_bonus": 5}},
            {"custo": "+3 PM", "descricao": "Muda alcance para longo.", "efeitos": {}}
        ]
    },
    "Santuário": {
        "nome": "Santuário",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "Inimigos devem passar em Vontade para atacar o alvo. Se alvo atacar, magia acaba.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Invisível para tipos de criatura Int baixa.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Protege contra efeitos de área (teste para incluir alvo na área).", "efeitos": {}}
        ]
    },
    "Segunda Chance": {
        "nome": "Segunda Chance",
        "circulo": 5,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Cura 200 PV e remove condições severas (cego, exausto, etc).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta cura em +20 PV.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Alcance curto, até 5 criaturas.", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Ressuscita criatura morta há 1 rodada.", "efeitos": {}}
        ]
    },
    "Selo de Mana": {
        "nome": "Selo de Mana",
        "circulo": 3,
        "escola": "Encantamento",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Se alvo gastar PM, deve passar em Vontade ou ação falha (PM gasto igual).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Alcance curto, criaturas escolhidas. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Semiplano": {
        "nome": "Semiplano",
        "circulo": 5,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Semiplano 30m lado",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Cria dimensão particular. Pode levar criaturas/objetos (custo PM).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Labirinto: Prende alvo (Investigação/Sobrevivência para sair).", "efeitos": {}},
            {"custo": "+5 PM",
                "descricao": "Permanente (Custo T$ 5.000).", "efeitos": {}}
        ]
    },
    "Servo Divino": {
        "nome": "Servo Divino",
        "circulo": 3,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Criatura conjurada",
        "duracao": "Cena/Tarefa",
        "resistencia": "",
        "descricao": "Espírito realiza tarefa de até 1h. Custo T$ 100.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+4 PM", "descricao": "Tarefa de 1 dia. Custo T$ 500.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Tarefa de 1 semana. Custo T$ 1.000.", "efeitos": {}}
        ]
    },
    "Servo Morto-Vivo": {
        "nome": "Servo Morto-Vivo",
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Toque",
        "alvo_area": "1 cadáver",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Cria Esqueleto ou Zumbi (Parceiro Iniciante). Pode sacrificar para evitar dano. Custo T$ 100.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Cria Carniçal (Veterano). Custo T$ 500.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Cria Sombra (Veterano). Custo T$ 500.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Cria Múmia (Mestre). Custo T$ 1.000. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Servos Invisíveis": {
        "nome": "Servos Invisíveis",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Criaturas conjuradas",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria 3 servos para tarefas simples. Pode gastar servo para +2 em perícia.",
        "efeitos": {
            "pericia_bonus_magia_uso_unico": 2
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta servos em +1.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Servos realizam tarefa complexa (passam automático com seu nível). Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Seta Infalível de Talude": {
        "nome": "Seta Infalível de Talude",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Criaturas escolhidas",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Lança 2 setas de energia. 1d4+1 essência cada. Acerto automático.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Lanças de energia (1d8+1 dano). Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda para 3 setas.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Muda para 5 setas. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Muda para 10 setas. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Silêncio": {
        "nome": "Silêncio",
        "circulo": 2,
        "escola": "Ilusão",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Área de silêncio total. Imune a som/trovão, impede conjuração verbal.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Alvo objeto (emanação 3m). Vontade se em posse.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Impede som de sair, mas permite som dentro.", "efeitos": {}}
        ]
    },
    "Soco de Arsenal": {
        "nome": "Soco de Arsenal",
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Causa 4d6+Força impacto e empurra 3m. Passar reduz metade e não empurra.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Pessoal/Cena. Aumenta alcance corpo a corpo em 3m.",
                "efeitos": {"alcance_corpo_a_corpo_bonus": 3}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +1d6.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Aumenta empurrão em +3m.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda dano para essência.", "efeitos": {}}
        ]
    },
    "Sombra Assassina": {
        "nome": "Sombra Assassina",
        "circulo": 5,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Sombra copia ações hostis do alvo contra ele mesmo. Passar dissipa após 1 rodada.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+10 PM",
                "descricao": "Afeta criaturas escolhidas na área.", "efeitos": {}}
        ]
    },
    "Sonho": {
        "nome": "Sonho",
        "circulo": 4,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "10 minutos",
        "alcance": "Ilimitado",
        "alvo_area": "1 criatura viva",
        "duracao": "Veja texto",
        "resistencia": "",
        "descricao": "Entra no sonho para conversar.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Pesadelo (1d10 trevas, fadiga, sem recuperação). Vontade anula.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta alvos em +1.", "efeitos": {}}
        ]
    },
    "Sono": {
        "nome": "Sono",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Deixa inconsciente (ou exausto se perigo). Se passar, fatigado.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Exausto por 1d4+1 rodadas na falha.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta 1 criatura.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta todos os alvos no alcance.", "efeitos": {}}
        ]
    },
    "Sopro da Salvação": {
        "nome": "Sopro da Salvação",
        "circulo": 3,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 9m",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Cura aliados em 2d8+4 e remove 1 condição.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta cura em +1d8+2.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Cura a partir de 0 PV (salva da morte).", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Remove todas as condições listadas.", "efeitos": {}}
        ]
    },
    "Sopro das Uivantes": {
        "nome": "Sopro das Uivantes",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 9m",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "4d6 frio, empurra 6m e derruba. Passar reduz metade.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta categoria de tamanho afetada. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Suporte Ambiental": {
        "nome": "Suporte Ambiental",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Imune a extremos de temperatura, respira na água, ignora fumaça.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM",
                "descricao": "Alcance curto, criaturas escolhidas.", "efeitos": {}}
        ]
    },
    "Sussurros Insanos": {
        "nome": "Sussurros Insanos",
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": "Alvo fica confuso.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta alvos em +1.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Afeta criatura.", "efeitos": {}},
            {"custo": "+12 PM",
                "descricao": "Criaturas escolhidas. Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Talho Invisível de Edauros": {
        "nome": "Talho Invisível de Edauros",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Cone de 9m",
        "duracao": "Instantânea",
        "resistencia": "Fortitude parcial",
        "descricao": "Lâmina de ar causa 10d8 corte e sangramento.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d8.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Sustentada. Dispara lâmina 6d8/rodada (Movimento).", "efeitos": {}}
        ]
    },
    "Teia": {
        "nome": "Teia",
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Cubo de 6m",
        "duracao": "Cena",
        "resistencia": "Reflexos anula",
        "descricao": "Enreda criaturas e cria terreno difícil. Inflamável.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Deixa imóvel também.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Teste a cada turno para não ser pego. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta área em +1 cubo 1,5m.", "efeitos": {}}
        ]
    },
    "Telecinesia": {
        "nome": "Telecinesia",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Veja texto",
        "duracao": "Sustentada ou Instantânea",
        "resistencia": "",
        "descricao": "Move criatura/objeto (sustentada) ou arremessa objetos (ataque).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM",
                "descricao": "Aumenta tamanho limite (Grande/Enorme/Colossal).", "efeitos": {}}
        ]
    },
    "Teletransporte": {
        "nome": "Teletransporte",
        "circulo": 3,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "5 criaturas voluntárias",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Leva a 1.000km. Teste de Misticismo para precisão.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta alvos em +5.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Santuário (local preparado): sem erro/distância.", "efeitos": {}},
            {"custo": "+9 PM",
                "descricao": "Círculo de teletransporte (Portal). Requer 5º círculo.", "efeitos": {}}
        ]
    },
    "Tempestade Divina": {
        "nome": "Tempestade Divina",
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Completa",
        "alcance": "Longo",
        "alvo_area": "Cilindro 15m raio/altura",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Vendaval (atrapalha ataque a distância). Pode ter chuva, neve ou granizo.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Raios (3d8 elétrico, ação padrão).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano raio em +1d8.", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Chuva forte (revela invisível, derruba voadores).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Granizo (2d6 dano/rodada).", "efeitos": {}},
            {"custo": "+3 PM",
                "descricao": "Neve (2d6 frio/rodada).", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta área para 90m.", "efeitos": {}}
        ]
    },
    "Tentáculos de Trevas": {
        "nome": "Tentáculos de Trevas",
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Esfera 6m raio",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Tentáculos agarram (Misticismo) e causam 4d6 trevas (esmaga). Terreno difícil.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta raio em +3m.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}}
        ]
    },
    "Terremoto": {
        "nome": "Terremoto",
        "circulo": 4,
        "escola": "Evocação",
        "tipo": "Divina",
        "custo_pm": 4,
        "execucao": "Padrão",
        "alcance": "Longo",
        "alvo_area": "Esfera 30m raio",
        "duracao": "1 rodada",
        "resistencia": "Veja texto",
        "descricao": "Tremor derruba e atordoa. Efeitos específicos por terreno (soterramento, fendas).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Toque Chocante": {
        "nome": "Toque Chocante",
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude reduz metade",
        "descricao": "2d8+2 eletricidade. Metal dá -5 na resistência.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta dano em +1d8+1.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Ataque corpo a corpo como parte (sem resistência).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Área pessoal (esfera 6m).", "efeitos": {}}
        ]
    },
    "Toque da Morte": {
        "nome": "Toque da Morte",
        "circulo": 5,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 5,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Veja texto",
        "descricao": "10d8+10 trevas. Se PV < metade, Fortitude ou reduz a -10 PV.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Alcance curto (raio).", "efeitos": {}},
            {"custo": "+10 PM",
                "descricao": "Inimigos em alcance curto (raios).", "efeitos": {}}
        ]
    },
    "Toque Vampírico": {
        "nome": "Toque Vampírico",
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Fortitude reduz metade",
        "descricao": "6d6 trevas. Cura metade do dano.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Ataque corpo a corpo como parte (sem resistência).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta dano em +2d6.", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Sustentada (repete toque 3d6 dano). Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Tranca Arcana": {
        "nome": "Tranca Arcana",
        "circulo": 1,
        "escola": "Abjuração",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "Objeto Grande ou menor",
        "duracao": "Permanente",
        "resistencia": "",
        "descricao": "Tranca mágica (+10 CD). Custo T$ 25.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque", "descricao": "Abre/fecha objeto destrancado.", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Abre trancas (mundanas ou mágicas).", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Aumenta CD em +5.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Afeta qualquer tamanho. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Tranquilidade": {
        "nome": "Tranquilidade",
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Divina",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 animal ou humanoide",
        "duracao": "Cena",
        "resistencia": "Vontade parcial",
        "descricao": "Torna indiferente (paz). Se passar, -2 ataque.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Afeta criatura.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Aumenta alvos em +1.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Criaturas escolhidas. Requer 3º círculo.", "efeitos": {}}
        ]
    },
    "Transformação de Guerra": {
        "nome": "Transformação de Guerra",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "+6 Defesa, ataque, dano. 30 PV temporários. Bloqueia magia.",
        "efeitos": {
            "defesa_bonus_magia": 6,
            "ataque_bonus_magia": 6,
            "dano_bonus_magia": 6,
            "pv_temporarios": 30
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta bônus em +1 e PV em +10.", "efeitos": {
                "defesa_bonus_magia": 1, "ataque_bonus_magia": 1, "dano_bonus_magia": 1, "pv_temporarios": 10}},
            {"custo": "+2 PM",
                "descricao": "Forma metálica (RD 10, imunidades). Custo T$ 100.", "efeitos": {"rd_magia": 10}}
        ]
    },
    "Transmutar Objetos": {
        "nome": "Transmutar Objetos",
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "Matéria-prima",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Cria objeto mundano (T$ 25).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "Truque",
                "descricao": "Limpa, colore ou conserta (1 PV).", "efeitos": {}},
            {"custo": "+1 PM",
                "descricao": "Cura construto (2d8 PV).", "efeitos": {}},
            {"custo": "+2 PM",
                "descricao": "Aumenta tamanho em uma categoria.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Aumenta preço x10.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Restaura objeto destruído. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+9 PM", "descricao": "Afeta item mágico.", "efeitos": {}}
        ]
    },
    "Velocidade": {
        "nome": "Velocidade",
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Sustentada",
        "resistencia": "",
        "descricao": "Ganha ação padrão ou movimento extra por turno (não magia).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+0 PM", "descricao": "Duração cena. Apenas ação de movimento extra.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Criaturas escolhidas. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+7 PM",
                "descricao": "Pessoal (Mente rápida). Pode lançar magia. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Vestimenta da Fé": {
        "nome": "Vestimenta da Fé",
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "Armadura, escudo ou roupa",
        "duracao": "1 dia",
        "resistencia": "",
        "descricao": "Concede +2 Defesa (Bônus encanto).",
        "efeitos": {
            "defesa_bonus_magia": 2
        },
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Concede bônus em Resistência também. Requer 3º círculo.",
                "efeitos": {"resistencia_bonus_magia": 2}},
            {"custo": "+4 PM", "descricao": "Aumenta bônus em +1.",
                "efeitos": {"defesa_bonus_magia": 1, "resistencia_bonus_magia": 1}},
            {"custo": "+7 PM", "descricao": "Concede RD 5. Requer 4º círculo.",
                "efeitos": {"rd_magia": 5}}
        ]
    },
    "Viagem Arbórea": {
        "nome": "Viagem Arbórea",
        "circulo": 3,
        "escola": "Convocação",
        "tipo": "Divina",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Entra em árvore e sai em outra (1km).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM",
                "descricao": "Leva 5 criaturas a 100km. Instantânea.", "efeitos": {}}
        ]
    },
    "Viagem Planar": {
        "nome": "Viagem Planar",
        "circulo": 4,
        "escola": "Convocação",
        "tipo": "Universal",
        "custo_pm": 4,
        "execucao": "Completa",
        "alcance": "Toque",
        "alvo_area": "Pessoal",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Viaja para outro plano. Custo T$ 1.000.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Leva 5 voluntários.", "efeitos": {}}
        ]
    },
    "Vidência": {
        "nome": "Vidência",
        "circulo": 3,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Ilimitado",
        "alvo_area": "1 criatura",
        "duracao": "Sustentada",
        "resistencia": "Vontade anula",
        "descricao": "Observa alvo a distância (superfície reflexiva).",
        "efeitos": {},
        "aprimoramentos": []
    },
    "Visão da Verdade": {
        "nome": "Visão da Verdade",
        "circulo": 4,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 4,
        "execucao": "Movimento",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Vê através de ilusão, escuridão e transmutação.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Toque, 1 criatura.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "+10 Percepção.",
                "efeitos": {"pericia_percepcao_bonus": 10}},
            {"custo": "+2 PM", "descricao": "+10 Intuição (detecta mentiras).", "efeitos": {
                "pericia_intuicao_bonus": 10}},
            {"custo": "+4 PM",
                "descricao": "Vê através de barreiras sólidas (30cm).", "efeitos": {}}
        ]
    },
    "Visão Mística": {
        "nome": "Visão Mística",
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Vê auras mágicas (detectar magia constante).",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Visão no escuro.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Duração 1 dia.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Ver o invisível.", "efeitos": {}}
        ]
    },
    "Vitalidade Fantasma": {
        "nome": "Vitalidade Fantasma",
        "circulo": 1,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Instantânea",
        "resistencia": "",
        "descricao": "Recebe 2d10 PV temporários (somem fim da cena).",
        "efeitos": {
            "pv_temporarios_rolagem": "2d10"
        },
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta em +1d10.",
                "efeitos": {"pv_temporarios_rolagem": "1d10"}},
            {"custo": "+5 PM",
                "descricao": "Drena vida de área (esfera 6m, Fortitude metade). Recebe PV = dano.", "efeitos": {}}
        ]
    },
    "Voo": {
        "nome": "Voo",
        "circulo": 3,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Ganha deslocamento de voo 12m.",
        "efeitos": {
            "deslocamento_voo": 12
        },
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Toque, 1 criatura.", "efeitos": {}},
            {"custo": "+4 PM",
                "descricao": "Duração 1 dia. Requer 4º círculo.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Alcance curto, 10 criaturas. Requer 4º círculo.", "efeitos": {}}
        ]
    },
    "Voz Divina": {
        "nome": "Voz Divina",
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Divina",
        "custo_pm": 2,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "",
        "descricao": "Fala com qualquer criatura.",
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM",
                "descricao": "Fala com cadáver (perguntas).", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Fala com plantas e rochas.", "efeitos": {}}
        ]
    }

}
