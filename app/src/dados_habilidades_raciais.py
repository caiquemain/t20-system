# src/dados_habilidades_raciais.py
# Habilidades de Raça - Tormenta 20 (Jogo do Ano)
# Estrutura atualizada com 'modificadores' matemáticos para Buffs

DADOS_HABILIDADES_RACIAIS = {
    # --- HUMANO ---
    "Versatil_Humano": {
        "nome": "Versátil",
        "tipo": "Racial",
        "descricao": "Você se torna treinado em duas perícias à sua escolha (não precisam ser da sua classe). Você pode trocar uma dessas perícias por um poder geral à sua escolha.",
        "fonte": "T20 JdA",
        "efeitos": {
            "pericia_escolha": 1,
            "pericia_ou_poder_escolha": 1
        }
    },

    # --- ANÃO ---
    "Conhecimento_Rochas_Anao": {
        "nome": "Conhecimento das Rochas",
        "tipo": "Racial",
        "descricao": "Você recebe visão no escuro e +2 em testes de Percepção e Sobrevivência realizados no subterrâneo.",
        "fonte": "T20 JdA",
        "efeitos": {"visao_escuro": True, "bonus_pericia_condicional": {"Percepção": 2, "Sobrevivência": 2}}
    },
    "Devagar_Sempre_Anao": {
        "nome": "Devagar e Sempre",
        "tipo": "Racial",
        "descricao": "Seu deslocamento é 6m (em vez de 9m). Porém, seu deslocamento não é reduzido por uso de armadura ou excesso de carga.",
        "fonte": "T20 JdA",
        "efeitos": {"deslocamento": 6, "imunidade_penalidade_mov": ["armadura", "carga"]}
    },
    "Duro_Pedra_Anao": {
        "nome": "Duro como Pedra",
        "tipo": "Racial",
        "descricao": "Você recebe +3 pontos de vida no 1º nível e +1 por nível seguinte.",
        "fonte": "T20 JdA",
        "efeitos": {"pv_max_ini": 3, "pv_max_nivel": 1}
    },
    "Tradicao_Heredrimm_Anao": {
        "nome": "Tradição de Heredrimm",
        "tipo": "Racial",
        "descricao": "Você é perito nas armas tradicionais anãs. Para você, todos os machados, martelos, marretas e picaretas são armas simples. Você recebe +2 em ataques com essas armas.",
        "fonte": "T20 JdA",
        "efeitos": {"proficiencia_simples": ["machado", "martelo", "marreta", "picareta"], "bonus_ataque_arma": {"machado": 2, "martelo": 2, "marreta": 2, "picareta": 2}}
    },

    # --- DAHLLAN ---
    "Amiga_Plantas_Dahllan": {
        "nome": "Amiga das Plantas",
        "tipo": "Racial",
        "descricao": "Você pode lançar a magia Controlar Plantas (atributo-chave Sabedoria). Caso aprenda novamente essa magia, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {
            "magia_adicional": {"nome": "Controlar Plantas", "atributo": "Sab"},
            "reducao_custo_magia": {"nomes": ["Controlar Plantas"], "valor": 1}
        }
    },
    "Armadura_Allihanna_Dahllan": {
        "nome": "Armadura de Allihanna",
        "tipo": "Racial",
        "descricao": "Você pode gastar uma ação de movimento e 1 PM para transformar sua pele em casca de árvore, recebendo +2 na Defesa até o fim da cena.",
        "fonte": "T20 JdA",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Movimento",
                "alcance": "Pessoal",
                "duracao": "Cena",
                "efeito": "Defesa +2",
                "modificadores": [
                    {
                        "atributo": "defesa",
                        "valor": 2,
                        "tipo_bonus": "melhoria"
                    }
                ]
            }
        }
    },
    "Empatia_Selvagem_Dahllan": {
        "nome": "Empatia Selvagem",
        "tipo": "Racial",
        "descricao": "Você pode se comunicar com animais por meio de linguagem corporal e vocalizações. Você pode usar Adestramento para mudar atitude e persuasão com animais. Caso receba esta habilidade novamente, recebe +2 em Adestramento.",
        "fonte": "T20 JdA",
        "efeitos": {"pericia_adestramento_persuasao": True}
    },

    # --- ELFO ---
    "Graca_Glorienn_Elfo": {
        "nome": "Graça de Glanna",
        "tipo": "Racial",
        "descricao": "Seu deslocamento é 12m (em vez de 9m).",
        "fonte": "T20 JdA",
        "efeitos": {"deslocamento": 12}
    },
    "Sangue_Magico_Elfo": {
        "nome": "Sangue Mágico",
        "tipo": "Racial",
        "descricao": "Você recebe +1 ponto de mana por nível.",
        "fonte": "T20 JdA",
        "efeitos": {"pm_max_nivel": 1}
    },
    "Sentidos_Elficos_Elfo": {
        "nome": "Sentidos Élficos",
        "tipo": "Racial",
        "descricao": "Você recebe visão na penumbra e +2 em Misticismo e Percepção.",
        "fonte": "T20 JdA",
        "efeitos": {"visao_penumbra": True, "bonus_pericia": {"Misticismo": 2, "Percepção": 2}}
    },

    # --- GOBLIN ---
    "Engenhoso_Goblin": {
        "nome": "Engenhoso",
        "tipo": "Racial",
        "descricao": "Você não sofre penalidades em testes de perícia por não usar ferramentas. Se usar a ferramenta necessária, recebe +2 no teste de perícia.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_ferramenta": 2}
    },
    "Espelunqueiro_Goblin": {
        "nome": "Espelunqueiro",
        "tipo": "Racial",
        "descricao": "Você recebe visão no escuro e deslocamento de escalada igual ao seu deslocamento terrestre.",
        "fonte": "T20 JdA",
        "efeitos": {"visao_escuro": True, "deslocamento_escalada_igual": True}
    },
    "Peste_Esguia_Goblin": {
        "nome": "Peste Esguia",
        "tipo": "Racial",
        "descricao": "Seu tamanho é Pequeno (veja a página 106), mas seu deslocamento se mantém 9m.",
        "fonte": "T20 JdA",
        "efeitos": {"tamanho": "Pequeno", "deslocamento": 9}
    },
    "Rato_Ruas_Goblin": {
        "nome": "Rato das Ruas",
        "tipo": "Racial",
        "descricao": "Você recebe +2 em Fortitude e sua recuperação de PV e PM nunca é inferior ao seu nível.",
        "fonte": "T20 JdA",
        "efeitos": {"bonus_pericia": {"Fortitude": 2}, "recuperacao_minima": True}
    },

    # --- LEFOU ---
    "Cria_Tormenta_Lefou": {
        "nome": "Cria da Tormenta",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo monstro e recebe +5 em testes de resistência contra efeitos causados por lefeu e pela Tormenta.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Monstro", "resistencia_tormenta": 5}
    },
    "Deformidade_Lefou": {
        "nome": "Deformidade",
        "tipo": "Racial",
        "descricao": "Você recebe +2 em duas perícias a sua escolha. Cada um desses bônus conta como um poder da Tormenta (exceto para perda de Carisma). Você pode trocar um desses bônus por um poder da Tormenta a sua escolha (ele também não conta para perda de Carisma).",
        "fonte": "T20 JdA",
        "efeitos": {
            "pericia_bonus_escolha": 2,
            "troca_poder_tormenta": True
        }
    },

    # --- MINOTAURO ---
    "Chifres_Minotauro": {
        "nome": "Chifres",
        "tipo": "Racial",
        "descricao": "Você possui uma arma natural de chifres (dano 1d6, crítico x2, perfuração). Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, pode gastar 1 PM para fazer um ataque corpo a corpo extra com os chifres.",
        "fonte": "T20 JdA",
        "efeitos": {"arma_natural": "Chifres 1d6", "ataque_extra_pm": 1}
    },
    "Couro_Rigido_Minotauro": {
        "nome": "Couro Rígido",
        "tipo": "Racial",
        "descricao": "Sua pele é dura como a de um touro. Você recebe +1 na Defesa.",
        "fonte": "T20 JdA",
        "efeitos": {"defesa_bonus": 1}
    },
    "Faro_Minotauro": {
        "nome": "Faro",
        "tipo": "Racial",
        "descricao": "Você tem olfato apurado. Contra inimigos em alcance curto que não possa perceber, você não fica desprevenido e camuflagem total lhe causa apenas 20% de chance de falha.",
        "fonte": "T20 JdA",
        "efeitos": {
            "visao_faro_desprevenido": True,
            "info_extra": {"alcance": "Curto", "detalhe": "Ignora camuflagem/desprevenido"}
        }
    },
    "Medo_Altura_Minotauro": {
        "nome": "Medo de Altura",
        "tipo": "Racial",
        "descricao": "Se estiver adjacente a uma queda de 3m ou mais de altura (como um buraco ou penhasco), você fica abalado.",
        "fonte": "T20 JdA",
        "efeitos": {"condicao_situacional": "Abalado (Altura > 3m)"}
    },

    # --- QAREEN ---
    "Desejos_Qareen": {
        "nome": "Desejos",
        "tipo": "Racial",
        "descricao": "Se lançar uma magia que alguém tenha pedido desde seu último turno, o custo da magia diminui em –1 PM. Fazer um desejo ao qareen é uma ação livre.",
        "fonte": "T20 JdA",
        "efeitos": {"reducao_pm_condicional": 1}
    },
    "Resistencia_Elemental_Qareen": {
        "nome": "Resistência Elemental",
        "tipo": "Racial",
        "descricao": "Você recebe redução 10 a um tipo de dano. Escolha uma: frio (qareen da água), eletricidade (do ar), fogo (do fogo), ácido (da terra), luz (da luz) ou trevas (qareen das trevas).",
        "fonte": "T20 JdA",
        "efeitos": {"resistencia_rd_escolha": 10}
    },
    "Tatuagem_Mist_Qareen": {
        "nome": "Tatuagem Mística",
        "tipo": "Racial",
        "descricao": "Você pode lançar uma magia de 1º círculo a sua escolha. Caso aprenda novamente essa magia, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {
            "magia_adicional_escolha": {"circulo": 1, "atributo": "Car"},
            "reducao_custo_se_conhecida": 1,
            "tag_adicional": "Racial: Qareen"
        }
    },

    # --- GOLEM ---
    "Chassi_Golem": {
        "nome": "Chassi",
        "tipo": "Racial",
        "descricao": "Seu corpo artificial é resistente, mas rígido. Seu deslocamento é 6m, mas não é reduzido por uso de armadura ou excesso de carga. Você recebe +2 na Defesa, mas possui penalidade de armadura –2. Você leva um dia para vestir ou remover uma armadura.",
        "fonte": "T20 JdA",
        "efeitos": {"deslocamento": 6, "imunidade_penalidade_mov": ["armadura", "carga"], "defesa_bonus": 2, "penalidade_armadura": -2}
    },
    "Criatura_Artificial_Golem": {
        "nome": "Criatura Artificial",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo construto. Recebe visão no escuro e imunidade a efeitos de cansaço, metabólicos e de veneno. Além disso, não precisa respirar, alimentar-se ou dormir, mas não se beneficia de cura mundana e de itens da categoria alimentação. Você precisa ficar inerte por oito horas por dia para recarregar sua fonte de energia. A perícia Cura não funciona em você, mas Ofício (artesão) pode ser usada no lugar dela.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Construto", "visao_escuro": True, "imunidade": ["cansaço", "metabólico", "veneno"]}
    },
    "Fonte_Elemental_Golem": {
        "nome": "Fonte Elemental",
        "tipo": "Racial",
        "descricao": "Você possui um espírito elemental preso em seu corpo. Escolha entre água (frio), ar (eletricidade), fogo (fogo) e terra (ácido). Você é imune a dano desse tipo. Se fosse sofrer dano mágico desse tipo, em vez disso cura PV em quantidade igual à metade do dano.",
        "fonte": "T20 JdA",
        "efeitos": {"imunidade_dano_escolha": True}
    },
    "Proposito_Criacao_Golem": {
        "nome": "Propósito de Criação",
        "tipo": "Racial",
        "descricao": "Você foi construído “pronto” para um propósito específico e não teve uma infância. Você não tem direito a escolher uma origem, mas recebe um poder geral a sua escolha.",
        "fonte": "T20 JdA",
        "efeitos": {
            "poder_escolha": 1,
            "sem_origem": True
        }
    },

    # --- HYNNE ---
    "Arremessador_Hynne": {
        "nome": "Arremessador",
        "tipo": "Racial",
        "descricao": "Quando faz um ataque à distância com uma funda ou uma arma de arremesso, seu dano aumenta em um passo.",
        "fonte": "T20 JdA",
        "efeitos": {"dano_arma_base": {"tipo": "arremesso_funda", "passos": 1}}
    },
    "Pequeno_Rechonchudo_Hynne": {
        "nome": "Pequeno e Rechonchudo",
        "tipo": "Racial",
        "descricao": "Seu tamanho é Pequeno (veja a página 106) e seu deslocamento é 6m. Você recebe +2 em Enganação e pode usar Destreza como atributo-chave de Atletismo (em vez de Força).",
        "fonte": "T20 JdA",
        "efeitos": {"deslocamento": 6, "bonus_pericia": {"Enganação": 2}, "atletismo_des": True}
    },
    "Sorte_Salvadora_Hynne": {
        "nome": "Sorte Salvadora",
        "tipo": "Racial",
        "descricao": "Quando faz um teste de resistência, você pode gastar 1 PM para rolar este teste novamente.",
        "fonte": "T20 JdA",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Reação",
                "efeito": "Rerolar teste de resistência",
                "duracao": "Instantâneo"
            }
        }
    },

    # --- KLIREN ---
    "Hibrido_Kliren": {
        "nome": "Híbrido",
        "tipo": "Racial",
        "descricao": "Sua natureza multifacetada fez com que você aprendesse conhecimentos variados. Você se torna treinado em uma perícia a sua escolha (não precisa ser da sua classe).",
        "fonte": "T20 JdA",
        "efeitos": {"pericia_escolha": 1}
    },
    "Engenhosidade_Kliren": {
        "nome": "Engenhosidade",
        "tipo": "Racial",
        "descricao": "Quando faz um teste de perícia, você pode gastar 2 PM para somar sua Inteligência no teste. Você não pode usar esta habilidade em testes de ataque. Caso receba esta habilidade novamente, seu custo é reduzido em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 2,
                "acao": "Livre",
                "gatilho": "Teste de Perícia",
                "efeito": "Soma Inteligência no teste atual.",
                "duracao": "Instantâneo",
                "nome_acumulo": "Engenhosidade",
                "reducao_se_acumular": 1,
                # Nota: Modificadores de perícia 'ao vivo' ainda não são somados automaticamente pelo regras.py
                # mas deixamos estruturado para futuro
                "modificadores": [
                    {
                        "atributo": "teste_pericia",
                        "valor_dinamico": "inteligencia",
                        "tipo_bonus": "engenhosidade"
                    }
                ]
            }
        }
    },
    "Ossos_Frageis_Kliren": {
        "nome": "Ossos Frágeis",
        "tipo": "Racial",
        "descricao": "Você sofre 1 ponto de dano adicional por dado de dano de impacto. Por exemplo, se for atingido por uma clava (dano 1d6), sofre 1d6+1 pontos de dano.",
        "fonte": "T20 JdA",
        "efeitos": {"vulnerabilidade_dado": {"tipo": "impacto", "valor": 1}}
    },
    "Vanguardista_Kliren": {
        "nome": "Vanguardista",
        "tipo": "Racial",
        "descricao": "Você recebe proficiência em armas de fogo e +2 em Ofício (um qualquer, a sua escolha).",
        "fonte": "T20 JdA",
        "efeitos": {"proficiencia_adicional": ["armas de fogo"], "bonus_pericia_escolha": {"Ofício": 2}}
    },

    # --- MEDUSA ---
    "Cria_Megalokk_Medusa": {
        "nome": "Cria de Megalokk",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo monstro e recebe visão no escuro.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Monstro", "visao_escuro": True}
    },
    "Natureza_Venenosa_Medusa": {
        "nome": "Natureza Venenosa",
        "tipo": "Racial",
        "descricao": "Você recebe resistência a veneno +5 e pode gastar uma ação de movimento e 1 PM para envenenar uma arma que esteja usando. A arma causa perda de 1d12 pontos de vida.",
        "fonte": "T20 JdA",
        "efeitos": {
            "resistencia_veneno": 5,
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Movimento",
                "alcance": "Pessoal (Arma)",
                "efeito": "Arma causa perda de 1d12 PV ao acertar.",
                "duracao": "Cena",
                "modificadores": [
                    {
                        "atributo": "dano_arma_extra",
                        "valor_dado": "1d12",
                        "tipo": "veneno"
                    }
                ]
            }
        }
    },
    "Olhar_Atordoante_Medusa": {
        "nome": "Olhar Atordoante",
        "tipo": "Racial",
        "descricao": "Você pode gastar uma ação de movimento e 1 PM para forçar uma criatura em alcance curto a fazer um teste de Fortitude (CD Car). Se a criatura falhar, fica atordoada por uma rodada (apenas uma vez por cena).",
        "fonte": "T20 JdA",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Movimento",
                "alcance": "Curto",
                "resistencia": "Fortitude (CD Car)",
                "efeito": "Deixa o alvo Atordoado por 1 rodada.",
                "limite": "1 vez por cena"
            }
        }
    },

    # --- OSTEON ---
    "Armadura_Ossea_Osteon": {
        "nome": "Armadura Óssea",
        "tipo": "Racial",
        "descricao": "Você recebe redução de corte, frio e perfuração 5.",
        "fonte": "T20 JdA",
        "efeitos": {"resistencia_rd": {"corte": 5, "frio": 5, "perfuração": 5}}
    },
    "Memoria_Postuma_Osteon": {
        "nome": "Memória Póstuma",
        "tipo": "Racial",
        "descricao": "Você se torna treinado em uma perícia (não precisa ser da sua classe) ou recebe um poder geral a sua escolha. Como alternativa, você pode ser um osteon de outra raça humanoide que não humano. Neste caso, você ganha uma habilidade dessa raça a sua escolha.",
        "fonte": "T20 JdA",
        "efeitos": {"pericia_escolha": 1, "poder_escolha": 1, "habilidade_raca_escolha": True}
    },
    "Natureza_Esqueletica_Osteon": {
        "nome": "Natureza Esquelética",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo morto-vivo. Recebe visão no escuro e imunidade a efeitos de cansaço, metabólicos, de trevas e de veneno. Além disso, não precisa respirar, alimentar-se ou dormir. Por fim, efeitos mágicos de cura de luz causam dano a você e você não se beneficia de itens da categoria alimentação, mas dano de trevas recupera seus PV.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Morto-Vivo", "visao_escuro": True, "imunidade": ["cansaço", "metabólico", "trevas", "veneno"]}
    },
    "Preco_Nao_Vida_Osteon": {
        "nome": "Preço da Não Vida",
        "tipo": "Racial",
        "descricao": "Você precisa passar oito horas sob a luz de estrelas ou no subterrâneo. Se fizer isso, recupera PV e PM por descanso em condições normais. Caso contrário, sofre os efeitos de fome.",
        "fonte": "T20 JdA",
        "efeitos": {}
    },

    # --- SEREIA/TRITÃO ---
    "Cancao_Mares_Sereia": {
        "nome": "Canção dos Mares",
        "tipo": "Racial",
        "descricao": "Você pode lançar duas das magias a seguir: Amedrontar, Comando, Despedaçar, Enfeitiçar, Hipnotismo ou Sono (atributo-chave Carisma). Caso aprenda novamente uma dessas magias, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {"magia_adicional_escolha": {"quantidade": 2, "lista": ["Amedrontar", "Comando", "Despedaçar", "Enfeitiçar", "Hipnotismo", "Sono"], "atributo": "Car"}}
    },
    "Mestre_Tridente_Sereia": {
        "nome": "Mestre do Tridente",
        "tipo": "Racial",
        "descricao": "Para você, o tridente é uma arma simples. Além disso, você recebe +2 em rolagens de dano com azagaias, lanças e tridentes.",
        "fonte": "T20 JdA",
        "efeitos": {"proficiencia_simples": ["tridente"], "bonus_dano_arma": {"azagaia": 2, "lança": 2, "tridente": 2}}
    },
    "Transf_Anfibia_Sereia": {
        "nome": "Transformação Anfíbia",
        "tipo": "Racial",
        "descricao": "Você pode respirar debaixo d’água e possui uma cauda que fornece deslocamento de natação 12m. Quando fora d’água, sua cauda desaparece e dá lugar a pernas (deslocamento 9m).",
        "fonte": "T20 JdA",
        "efeitos": {
            # Passivos
            "respirar_agua": True,
            "deslocamento": 9,
            "deslocamento_natacao": 12,

            # Ativável
            "habilidade_ativavel": {
                "custo": 0,
                "acao": "Livre",
                "efeito": "Alterna entre Pernas (9m) e Cauda (12m Natação).",
                "info_extra": "Altera seu tipo de deslocamento principal."
            }
        }
    },
    # --- SÍLFIDE ---
    "Asas_Borboleta_Silfide": {
        "nome": "Asas de Borboleta",
        "tipo": "Racial",
        "descricao": "Seu tamanho é Minúsculo. Você pode pairar a 1,5m do chão com deslocamento 9m. Isso permite que você ignore terreno difícil e o torna imune a dano por queda. Você pode gastar 1 PM por rodada para voar com deslocamento de 12m.",
        "fonte": "T20 JdA",
        "efeitos": {
            # --- PARTE PASSIVA ---
            "tamanho": "Minúsculo",
            "deslocamento": 9,
            "deslocamento_voo_base": 1.5,
            "imune_queda": True,
            "ignora_terreno_dificil": True,

            # --- PARTE ATIVÁVEL (BUFF) ---
            # Voo aumenta o deslocamento para 12m. Se o base é 9m, o buff é +3m.
            "habilidade_ativavel": {
                "custo": 1,
                "acao": "Livre",
                "duracao": "1 Rodada (Sustentada)",
                "efeito": "Voo com deslocamento 12m.",
                "modificadores": [
                    {
                        "atributo": "deslocamento",
                        "valor": 3,
                        "tipo_bonus": "voo"
                    }
                ]
            }
        }
    },
    "Esp_Natureza_Silfide": {
        "nome": "Espírito da Natureza",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo espírito, recebe visão na penumbra e pode falar com animais livremente.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Espírito", "visao_penumbra": True, "fala_animais": True}
    },
    "Magia_Fadas_Silfide": {
        "nome": "Magia das Fadas",
        "tipo": "Racial",
        "descricao": "Você pode lançar duas das magias a seguir (atributo-chave Carisma): Criar Ilusão, Enfeitiçar, Luz (como uma magia arcana) e Sono. Caso aprenda novamente uma dessas magias, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {"magia_adicional_escolha": {"quantidade": 2, "lista": ["Criar Ilusão", "Enfeitiçar", "Luz", "Sono"], "atributo": "Car"}}
    },

    # --- SURAGGEL ---
    "Heranca_Divina_Suraggel": {
        "nome": "Herança Divina",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo espírito e recebe visão no escuro.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Espírito", "visao_escuro": True}
    },
    "Luz_Sagrada_Aggelus": {
        "nome": "Luz Sagrada",
        "tipo": "Racial",
        "descricao": "Você recebe +2 em Diplomacia e Intuição. Além disso, pode lançar Luz (como uma magia divina; atributo-chave Carisma). Caso aprenda novamente essa magia, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {
            "bonus_pericia": {"Diplomacia": 2, "Intuição": 2},
            "magia_adicional": {"nome": "Luz", "atributo": "Car"},
            "reducao_custo_magia": {"nomes": ["Luz"], "valor": 1}
        }
    },
    "Sombras_Prof_Sulfure": {
        "nome": "Sombras Profanas",
        "tipo": "Racial",
        "descricao": "Você recebe +2 em Enganação e Furtividade. Além disso, pode lançar Escuridão (como uma magia divina; atributo-chave Inteligência). Caso aprenda novamente essa magia, seu custo diminui em –1 PM.",
        "fonte": "T20 JdA",
        "efeitos": {
            "bonus_pericia": {"Enganação": 2, "Furtividade": 2},
            "magia_adicional": {"nome": "Escuridão", "atributo": "Int"},
            "reducao_custo_magia": {"nomes": ["Escuridão"], "valor": 1}
        }
    },

    # --- TROG ---
    "Mau_Cheiro_Trog": {
        "nome": "Mau Cheiro",
        "tipo": "Racial",
        "descricao": "Você pode gastar uma ação padrão e 2 PM para expelir um gás fétido. Todas as criaturas (exceto trogs) em alcance curto devem passar em um teste de Fortitude contra veneno (CD Con) ou ficarão enjoadas durante 1d6 rodadas. Uma criatura que passe no teste de resistência fica imune a esta habilidade por um dia.",
        "fonte": "T20 JdA",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 2,
                "acao": "Padrão",
                "alcance": "Curto",
                "resistencia": "Fortitude (CD Con)",
                "efeito": "Deixa criaturas em alcance curto Enjoadas (1d6 rodadas).",
                "imunidade_pos_teste": True
            }
        }
    },
    "Mordida_Trog": {
        "nome": "Mordida",
        "tipo": "Racial",
        "descricao": "Você possui uma arma natural de mordida (dano 1d6, crítico x2, perfuração). Uma vez por rodada, quando usa a ação agredir para atacar com outra arma, pode gastar 1 PM para fazer um ataque corpo a corpo extra com a mordida.",
        "fonte": "T20 JdA",
        "efeitos": {"arma_natural": "Mordida 1d6", "ataque_extra_pm": 1}
    },
    "Reptiliano_Trog": {
        "nome": "Reptiliano",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo monstro e recebe visão no escuro, +1 na Defesa e, se estiver sem armadura ou roupas pesadas, +5 em Furtividade.",
        "fonte": "T20 JdA",
        "efeitos": {"tipo_criatura": "Monstro", "visao_escuro": True, "defesa_bonus": 1, "bonus_pericia_condicional": {"Furtividade": 5}}
    },
    "Sangue_Frio_Trog": {
        "nome": "Sangue Frio",
        "tipo": "Racial",
        "descricao": "Você sofre 1 ponto de dano adicional por dado de dano de frio.",
        "fonte": "T20 JdA",
        "efeitos": {"vulnerabilidade_dado": {"tipo": "frio", "valor": 1}}
    },

    # --- MEIO-ELFO (Versão Herós de Arton) ---
    "Ambicao_Herdada_MeioElfo": {
        "nome": "Ambição Herdada",
        "tipo": "Racial",
        "descricao": "Você recebe um poder geral ou poder único de origem a sua escolha.",
        "fonte": "Heróis de Arton",
        "efeitos": {
            # Abre o seletor de Poderes Gerais (o frontend já trata isso)
            "poder_geral_ou_origem": 1
        }
    },
    "Entre_Dois_Mundos_MeioElfo": {
        "nome": "Entre Dois Mundos",
        "tipo": "Racial",
        "descricao": "Você recebe +1 em perícias baseadas em Carisma.",
        "fonte": "Heróis de Arton",
        "efeitos": {
            # Nova mecânica: Aplica em qualquer perícia cujo atributo chave seja 'car'
            "bonus_pericia_atributo": {"car": 1}
        }
    },
    "Sangue_Elfico_MeioElfo": {
        "nome": "Sangue Élfico",
        "tipo": "Racial",
        "descricao": "Você recebe visão na penumbra e +1 ponto de mana a cada nível ímpar (incluindo o 1º). Além disso, é considerado um elfo para efeitos relacionados a raça.",
        "fonte": "Heróis de Arton",
        "efeitos": {
            "visao_penumbra": True,
            # Nova chave mecânica que vamos ensinar o regras.py a ler
            "pm_por_nivel_impar": 1,
            "tags_raciais": ["Elfo", "Humano"]
        }
    },
    # --- GALOKK ---
    "Forca_Titas_Galokk": {
        "nome": "Força dos Titãs",
        "tipo": "Racial",
        "descricao": "Quando acerta um ataque corpo a corpo ou de arremesso, você pode gastar 1 PM. Se fizer isso, sempre que rolar o resultado máximo em um dado de dano da arma, role um dado extra, até um limite de dados extras igual à sua Força.",
        "fonte": "Heróis de Arton",
        "efeitos": {
            "dano_explosao": {
                "custo_pm": 1,
                "limite_atributo": "for",
                "tipo_ataque": ["corpo_a_corpo", "arremesso"],
                "gatilho": "maximo_dado"
            }
        }
    },
    "Meio_Gigante_Galokk": {
        "nome": "Meio-Gigante",
        "tipo": "Racial",
        "descricao": "Você é uma criatura do tipo humanoide (gigante). Seu tamanho é Grande e você pode usar Força como atributo-chave de Intimidação.",
        "fonte": "Heróis de Arton",
        "efeitos": {
            "tamanho": "Grande",
            "pericia_atributo_opcao": {"Intimidação": "for"},
            "tags_raciais": ["Humanoide", "Gigante"]
        }
    },
    "Infancia_Pequenos_Galokk": {
        "nome": "Infância entre os Pequenos",
        "tipo": "Racial",
        "descricao": "Você se torna treinado em uma perícia a sua escolha.",
        "fonte": "Heróis de Arton",
        "efeitos": {"pericia_escolha": 1}
    }
}
