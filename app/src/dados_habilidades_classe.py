# src/dados_habilidades_classe.py

# ==============================================================================
# BANCO DE DADOS DE HABILIDADES E PODERES DE CLASSE (T20 JdA)
# Estrutura unificada para facilitar classes variantes.
#
# Chave: CLASSE_NOME_HABILIDADE (Upper Snake Case)
# nome: Nome oficial (Display)
# tipo: "Habilidade de Classe" (Fixa) ou "Poder de [Classe]" (Escolha)
# classe: Nome da classe principal associada (para filtros)
# nivel: Nível em que a habilidade fixa é ganha (0 se for poder de escolha)
# descricao: Texto de regras
# requisitos: Lista de strings (ex: ["For 1", "Treinado em Luta"])
# efeitos: Dicionário de automação
# ==============================================================================

DADOS_HABILIDADES_CLASSE = {

    # ==========================================================================
    # ARCANISTA
    # ==========================================================================
    "ARCANISTA_CAMINHO": {
        "nome": "Caminho do Arcanista",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 1,
        "descricao": "Escolha um caminho: Bruxo (foco, Int), Feiticeiro (linhagem, Car) ou Mago (grimório, Int). Define seu atributo-chave e mecânica de magia.",
        "efeitos": {"escolha_subclasse": ["Bruxo", "Feiticeiro", "Mago"]}
    },
    "ARCANISTA_MAGIAS": {
        "nome": "Magias (Arcanista)",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 1,
        "descricao": "Você pode lançar magias arcanas. Começa com 3 magias de 1º círculo (mais se for Mago).",
        "efeitos": {"habilita_magia": {"tipo": "Arcana", "circulo_max": 1}}
    },
    "ARCANISTA_ALTA_ARCANA": {
        "nome": "Alta Arcana",
        "tipo": "Habilidade de Classe",
        "classe": "Arcanista",
        "nivel": 20,
        "descricao": "O custo em PM de suas magias arcanas é reduzido à metade.",
        "efeitos": {"reducao_custo_magia_global": 0.5}
    },
    # --- PODERES DE ARCANISTA ---
    "ARCANISTA_ARCANO_BATALHA": {
        "nome": "Arcano de Batalha",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você soma seu atributo-chave nas rolagens de dano de suas magias.",
        "efeitos": {"dano_magia_soma_atributo": True}
    },
    "ARCANISTA_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você recebe +1 em um atributo. Pode escolher várias vezes (1x por patamar por atributo).",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "ARCANISTA_CALDEIRAO_BRUXO": {
        "nome": "Caldeirão do Bruxo",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Bruxo", "Treinado em Ofício (alquimista)"],
        "descricao": "Pode criar poções como se tivesse Preparar Poção. Se tiver ambos, cria até 5º círculo.",
        "efeitos": {"fabricar_pocao": True}
    },
    "ARCANISTA_CONHECIMENTO_MAGICO": {
        "nome": "Conhecimento Mágico",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você aprende duas magias de qualquer círculo que possa lançar.",
        "efeitos": {"magias_adicionais": 2}
    },
    "ARCANISTA_CONTRAMAGICA_APRIMORADA": {
        "nome": "Contramágica Aprimorada",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Magia: Dissipar Magia"],
        "descricao": "1x/rodada: Pode fazer contramágica como reação.",
        "efeitos": {
        "contramagica_como_reacao": True,
        "gatilho": "inimigo_lanca_magia",
        "custo_acao": "reacao",
        "nota": "Acao de combate nao modelada pelo motor. Reservado p/ VTT."
    }
    },
    "ARCANISTA_ENVOLTO_MISTERIO": {
        "nome": "Envolto em Mistério",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "+5 em Enganação e Intimidação contra pessoas não treinadas em Conhecimento ou Misticismo.",
        "efeitos": {
            "bonus_pericia_condicional": {"Enganação": 5, "Intimidação": 5},
            "condicao_bonus_pericia": "vs alvos nao treinados em Conhecimento ou Misticismo",
            "nota": "Bonus condicional por alvo; motor exibe como situacional."
        }
    },
    "ARCANISTA_ESCRIBA_ARCANO": {
        "nome": "Escriba Arcano",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Mago", "Treinado em Ofício (escriba)"],
        "descricao": "Pode aprender magias copiando pergaminhos/grimórios (T$ 250/PM).",
        "efeitos": {
        "aprender_magias_por_copia": {
            "custo_tempo_dias_por_pm": 1,
            "custo_material_por_pm": 250,
            "requer": ["Mago", "Oficio (escriba)"]
        },
        "nota": "Mecanica de downtime; motor nao consome. Reservado p/ VTT."
    }
    },
    "ARCANISTA_ESPECIALISTA_ESCOLA": {
        "nome": "Especialista em Escola",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Bruxo ou Mago"],
        "descricao": "Escolha uma escola. CD para resistir a magias dessa escola aumenta em +2.",
        "efeitos": {"cd_magia_escola_bonus": 2}
    },
    "ARCANISTA_FAMILIAR": {
        "nome": "Familiar",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Você possui um animal mágico que concede bônus.",
        "efeitos": {"familiar_escolha": True}
    },
    "ARCANISTA_FLUXO_MANA": {
        "nome": "Fluxo de Mana",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Nível 10"],
        "descricao": "Pode manter dois efeitos sustentados com uma ação livre (pagando ambos).",
        "efeitos": {
        "sustentados_simultaneos": 2,
        "custo_acao_manutencao": "livre",
        "nota": "Motor nao rastreia sustentados; reservado p/ VTT."
    }
    },
    "ARCANISTA_FOCO_VITAL": {
        "nome": "Foco Vital",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Bruxo"],
        "descricao": "Se sofrer dano letal segurando foco, fica com 1 PV e foco absorve o resto (pode quebrar).",
        "efeitos": {
        "sobrevive_a_dano_letal": {
            "preserva_pv_minimo": 1,
            "absorve_dano_no_foco": True,
            "foco_pode_ser_destruido": True
        },
        "nota": "Reacao a dano; motor nao tem pipeline. Reservado p/ VTT."
    }
    },
    "ARCANISTA_FORTALECIMENTO_ARCANO": {
        "nome": "Fortalecimento Arcano",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Nível 5"],
        "descricao": "A CD de suas magias aumenta em +1. Se lançar 4º círculo, aumenta em +2.",
        "efeitos": {"cd_magia_bonus": 1}
    },
    "ARCANISTA_HERANCA_APRIMORADA": {
        "nome": "Herança Aprimorada",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Feiticeiro", "Nível 6"],
        "descricao": "Recebe a herança aprimorada de sua linhagem.",
        "efeitos": {
        "heranca_nivel": "aprimorada",
        "nota": "Aplicada em poderes_arcanista.py por nome da Linhagem."
    }
    },
    "ARCANISTA_HERANCA_SUPERIOR": {
        "nome": "Herança Superior",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Herança Aprimorada", "Nível 11"],
        "descricao": "Recebe a herança superior de sua linhagem.",
        "efeitos": {
        "heranca_nivel": "superior",
        "nota": "Aplicada em poderes_arcanista.py por nome da Linhagem."
    }
    },
    "ARCANISTA_MAGIA_PUNGENTE": {
        "nome": "Magia Pungente",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Ao lançar magia, pague +1 PM para aumentar a CD em +2.",
        "efeitos": {
        "cd_ativavel": 2,
        "custo_ativavel": 1,
        "duracao": "proxima_magia",
        "nota": "Buff temporario; motor le status.buffs com origem 'Magia Pungente'."
    }
    },
    "ARCANISTA_MESTRE_ESCOLA": {
        "nome": "Mestre em Escola",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Especialista em Escola", "Nível 8"],
        "descricao": "Custo de magias da escola escolhida diminui em -1 PM.",
        "efeitos": {"reducao_custo_escola": 1}
    },
    "ARCANISTA_PODER_MAGICO": {
        "nome": "Poder Mágico",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Recebe +1 PM por nível de arcanista.",
        "efeitos": {"pm_max_nivel": 1}
    },
    "ARCANISTA_RAIO_ARCANO": {
        "nome": "Raio Arcano",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "descricao": "Padrão: 1d8 essência (curto). +1d8 por círculo máximo. Reflexos metade.",
        "efeitos": {
        "ataque_magico": {
            "dano_base": "1d8",
            "dano_por_circulo_acima_1": "1d8",
            "alcance": "curto",
            "resistencia": "Reflexos",
            "tipo_dano": "essencia"
        },
        "nota": "Recriado em sincronizar_ataques_magicos; efeito serve de catalogo."
    }
    },
    "ARCANISTA_RAIO_ELEMENTAL": {
        "nome": "Raio Elemental",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Raio Arcano"],
        "descricao": "+1 PM: Raio causa dano elemental (ácido/fogo/frio/eletricidade/trevas) e inflige condição na falha.",
        "efeitos": {
        "raio_elemental": True,
        "custo_ativavel": 1,
        "tipos": ["acido", "eletricidade", "fogo", "frio", "trevas"],
        "nota": "Aplicado em sincronizar_ataques_magicos por nome."
    }
    },
    "ARCANISTA_RAIO_PODEROSO": {
        "nome": "Raio Poderoso",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Raio Arcano"],
        "descricao": "Dado do Raio aumenta para d12 e alcance para médio.",
        "efeitos": {
        "raio_poderoso": True,
        "dado": "1d12",
        "alcance": "medio",
        "nota": "Aplicado em sincronizar_ataques_magicos por nome."
    }
    },
    "ARCANISTA_TINTA_MAGO": {
        "nome": "Tinta do Mago",
        "tipo": "Poder de Arcanista",
        "classe": "Arcanista",
        "requisitos": ["Caminho: Mago", "Treinado em Ofício (escriba)"],
        "descricao": "Pode criar pergaminhos (como Escrever Pergaminho). Se tiver ambos, custo é metade.",
        "efeitos": {
            "fabricar_pergaminho": True,
            "reducao_custo_com_escrever_pergaminho": 0.5,
            "nota": "Downtime; motor nao consome. Reservado p/ VTT."
        }
    },

    # ==========================================================================
    # BÁRBARO
    # ==========================================================================
    # Habilidades de Classe (Fixas)
    "BARBARO_FURIA": {
        "nome": "Fúria",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 1,
        "descricao": "Gaste 2 PM: +2 ataque e dano corpo a corpo. Não pode concentrar. +1/+1 a cada 5 níveis. Termina se não atacar/ser atacado.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "ataque_bonus": 2, "dano_bonus": 2, "restricao": "sem_concentracao", "escala_nivel": {"cada": 5, "bonus": 1}}
        }
    },
    "BARBARO_INSTINTO_SELVAGEM": {
        "nome": "Instinto Selvagem",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 3,
        "descricao": "Recebe +1 em Percepção, Reflexos e rolagens de dano. Aumenta a cada 6 níveis.",
        "efeitos": {
            "bonus_pericia": {"Percepção": 1, "Reflexos": 1},
            "dano_bonus": 1,
            "escala_nivel": {"cada": 6, "bonus": 1}
        }
    },
    "BARBARO_REDUCAO_DANO": {
        "nome": "Redução de Dano",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 5,
        "descricao": "Recebe RD 2. Aumenta em +2 a cada 3 níveis.",
        "efeitos": {
            "rd_fixa": 2,
            "escala_nivel": {"cada": 3, "bonus": 2},
            "rd_max": 10
        }
    },
    "BARBARO_FURIA_TITANICA": {
        "nome": "Fúria Titânica",
        "tipo": "Habilidade de Classe",
        "classe": "Bárbaro",
        "nivel": 20,
        "descricao": "O bônus de ataque e dano da Fúria é dobrado.",
        "efeitos": {
            "furia_titanica": {"dobra_bonus_furia": True, "nivel": 20},
            "nota": "No 20º nível, o bônus de Fúria é dobrado (T20 p.41).",
        }
    },

    # Poderes de Bárbaro
    "BARBARO_ALMA_BRONZE": {
        "nome": "Alma de Bronze",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Ao entrar em Fúria, ganha PV temporários iguais a Nível + Força.",
        "efeitos": {
            "pv_temp_em_furia": {"nivel": True, "atributo": "forca"},
            "nota": "Ao entrar em Fúria, ganha PV temporários = nível + Força (T20 p.41).",
        }
    },
    "BARBARO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Recebe +1 em um atributo. Pode ser escolhido várias vezes (1x por patamar por atributo).",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "BARBARO_BRADO_ASSUSTADOR": {
        "nome": "Brado Assustador",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Treinado em Intimidação"],
        "descricao": "1 PM (Movimento): Berro feroz deixa inimigos em alcance curto vulneráveis (fim da cena).",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "acao": "movimento", "alcance": "curto",
                "alvos": "inimigos", "efeito": "vulneravel",
                "duracao": "cena", "tipo_efeito": "medo",
                "pre_requisito": "treinado em Intimidação",
            },
        }
    },
    "BARBARO_CRITICO_BRUTAL": {
        "nome": "Crítico Brutal",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Nível 6"],
        "descricao": "Multiplicador de crítico com armas corpo a corpo/arremesso aumenta em +1.",
        "efeitos": {"multiplicador_critico_bonus": 1}
    },
    "BARBARO_DESTRUIDOR": {
        "nome": "Destruidor",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["For 1"],
        "descricao": "Ao causar dano com arma de duas mãos corpo a corpo, rerola 1 ou 2 no dano.",
        "efeitos": {
            "rerola_dado_dano": {
                "valores": [1, 2], "arma": "duas_maos_corpo_a_corpo",
            },
            "pre_requisito": "For 1",
            "nota": "Rola novamente qualquer 1 ou 2 nas rolagens de dano (T20 p.41).",
        }
    },
    "BARBARO_ESPIRITO_INQUEBRAVEL": {
        "nome": "Espírito Inquebrável",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Alma de Bronze"],
        "descricao": "Em fúria, não fica inconsciente com 0 PV (morre apenas com negativo = metade PV máx).",
        "efeitos": {
            "em_furia": {
                "nao_inconsciente_em_0pv": True,
                "morte_em_negativo": "metade_pv_max",
            },
            "pre_requisito": "Alma de Bronze",
        }
    },
    "BARBARO_ESQUIVA_SOBRENATURAL": {
        "nome": "Esquiva Sobrenatural",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Você nunca fica surpreendido.",
        "efeitos": {"imunidade": ["surpreendido"]}
    },
    "BARBARO_FORCA_INDOMAVEL": {
        "nome": "Força Indomável",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "1 PM: Soma nível em teste de Força ou Atletismo (pode usar após rolar).",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "acao": "livre", "efeito": "soma_nivel_teste",
                "pericias": ["Força", "Atletismo"],
                "gatilho": "apos_rolar_dado_antes_do_mestre_responder",
            },
        }
    },
    "BARBARO_FRENESI": {
        "nome": "Frenesi",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Em Fúria, ao agredir, gaste 2 PM para fazer um ataque extra.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2, "acao": "reacao",
                "gatilho": "acao_agredir_em_furia",
                "efeito": "ataque_adicional",
                "limite": "uma_vez_por_rodada",
            },
        }
    },
    "BARBARO_FURIA_SAVANA": {
        "nome": "Fúria da Savana",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Deslocamento +3m. Fúria aplica bônus também a armas de arremesso.",
        "efeitos": {"deslocamento_bonus": 3, "furia_arremesso": True}
    },
    "BARBARO_FURIA_RAIVOSA": {
        "nome": "Fúria Raivosa",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "1 PM: Mantém a fúria ativa na rodada mesmo se não atacar/ser atacado.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "acao": "livre",
                "gatilho": "furia_terminaria_por_inatividade",
                "efeito": "estender_furia_1_rodada",
            },
        }
    },
    "BARBARO_GOLPE_PODEROSO": {
        "nome": "Golpe Poderoso",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Ao acertar ataque, 1 PM: Causa um dado extra de dano do mesmo tipo.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "acao": "livre",
                "gatilho": "acerto_corpo_a_corpo_ou_arremesso",
                "efeito": "dado_extra_dano",
                "dado_extra": 1,
            },
        }
    },
    "BARBARO_IMPETO": {
        "nome": "Ímpeto",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "1 PM: Aumenta deslocamento em +6m por uma rodada.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "acao": "livre",
                "efeito": "deslocamento_bonus_temporario",
                "valor": 6, "duracao": "rodada",
            },
        }
    },
    "BARBARO_INVESTIDA_IMPRUDENTE": {
        "nome": "Investida Imprudente",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Na investida, pode aceitar -5 Defesa para ganhar +1d12 dano.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 0, "acao": "livre",
                "gatilho": "investida",
                "efeito": "trocar_defesa_por_dano",
                "penalidade_defesa": -5, "dano_extra": "1d12",
            },
        }
    },
    "BARBARO_PELE_ACO": {
        "nome": "Pele de Aço",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Pele de Ferro", "Nível 8"],
        "descricao": "O bônus de Pele de Ferro aumenta para +8.",
        "efeitos": {"defesa_bonus": 8}
    },
    "BARBARO_PELE_FERRO": {
        "nome": "Pele de Ferro",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Recebe +4 na Defesa (se não usar armadura pesada).",
        "efeitos": {"defesa_bonus": 4}
    },
    "BARBARO_SANGUE_INIMIGOS": {
        "nome": "Sangue dos Inimigos",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Em fúria, ao criticar ou zerar PV inimigo: ganha +1 ataque/dano cumulativo (máx nível) pela cena.",
        "efeitos": {
            "em_furia": {
                "bonus_cumulativo": {
                    "valor": 1, "limite": "nivel", "duracao": "cena",
                    "gatilhos": ["acerto_critico", "reduzir_a_0_pv"],
                },
            },
        }
    },
    "BARBARO_SUPERSTICAO": {
        "nome": "Superstição",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Recebe resistência a magia +5.",
        "efeitos": {"resistencia_magia_bonus": 5}
    },
    "BARBARO_TOTEM_ESPIRITUAL": {
        "nome": "Totem Espiritual",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "requisitos": ["Sab 1", "Nível 4"],
        "descricao": "Soma Sabedoria aos PM. Aprende uma magia definida pelo animal (lança com Sab, mesmo em fúria).",
        "efeitos": {"pm_soma_atributo": "sab", "escolha_totem": True}
    },
    "BARBARO_VIGOR_PRIMAL": {
        "nome": "Vigor Primal",
        "tipo": "Poder de Bárbaro",
        "classe": "Bárbaro",
        "descricao": "Movimento: Gaste PM (limite Constituição). Recupera 1d12 PV por PM gasto.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": "variavel", "acao": "movimento",
                "efeito": "cura", "por_pm": "1d12",
                "limite_pm": "constituicao",
            },
        }
    },

    # ==========================================================================
    # BARDO (T20 JdA, p. 43-44)
    # ==========================================================================
    "BARDO_INSPIRACAO": {
        "nome": "Inspiração",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 1,
        "descricao": "Ação padrão, 2 PM: você e aliados em alcance curto ganham +1 em testes de perícia até o fim da cena. A cada 4 níveis (5º, 9º, 13º, 17º), pode gastar +2 PM para aumentar o bônus em +1.",
        "efeitos": {
            "acao_ativavel": {
                "acao": "padrão",
                "custo_pm": 2,
                "alcance": "curto",
                "duracao": "cena",
                "bonus_pericias_aliados": 1,
                "escala_nivel": {"cada": 4, "bonus": 1, "custo_pm_extra": 2},
            }
        }
    },
    "BARDO_MAGIAS": {
        "nome": "Magias (Bardo)",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 1,
        "descricao": "Escolha três escolas de magia (escolha permanente). Lança magias arcanas de 1º círculo (2º no 6º nível, 3º no 10º, 4º no 14º) dessas escolas. Começa com 2 magias e aprende +1 a cada nível par. Pode lançar de armadura leve sem teste de Misticismo. Atributo-chave: Carisma (soma Carisma no total de PM).",
        "efeitos": {
            "habilita_magia": {
                "tipo": "Arcana",
                "atributo": "car",
                "escolas_restritas": 3,
                "armadura_leve_sem_teste": True,
            }
        }
    },
    "BARDO_ECLETICO": {
        "nome": "Eclético",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 2,
        "descricao": "Ao fazer um teste de perícia, pode gastar 1 PM para receber os benefícios de ser treinado nesta perícia neste teste.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "efeito": "beneficios_treinado_pericia",
            }
        }
    },
    "BARDO_ARTISTA_COMPLETO": {
        "nome": "Artista Completo",
        "tipo": "Habilidade de Classe",
        "classe": "Bardo",
        "nivel": 20,
        "descricao": "Pode usar Inspiração como ação livre. Enquanto sob efeito de sua Inspiração, qualquer habilidade de bardo (incluindo magias) tem seu custo em PM reduzido pela metade (após aprimoramentos e outras reduções).",
        "efeitos": {
            "artista_completo": True,
            "inspiracao_acao_livre": True,
            "reducao_custo_inspiracao_metade": True,
        }
    },
    # --- PODERES DE BARDO (20 poderes oficiais, T20 JdA p. 43-44) ---
    "BARDO_ARTE_MAGICA": {
        "nome": "Arte Mágica",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Enquanto sob efeito de sua habilidade Inspiração, a CD de todas as suas habilidades de bardo aumenta em +2.",
        "efeitos": {"cd_bardo_inspiracao": 2}
    },
    "BARDO_AUMENTAR_REPERTORIO": {
        "nome": "Aumentar Repertório",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Aprende duas magias de qualquer círculo que possa lançar, pertencentes às escolas que conhece, arcanas ou divinas. Pode escolher este poder quantas vezes quiser.",
        "efeitos": {"magias_adicionais": 2, "multipla_escolha": True}
    },
    "BARDO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "BARDO_DANCA_LAMINAS": {
        "nome": "Dança das Lâminas",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Esgrima Mágica", "Nível 10"],
        "descricao": "Quando lança uma magia com execução de uma ação padrão, pode gastar 1 PM para fazer um ataque corpo a corpo como uma ação livre.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "acao": "livre",
                "gatilho": "lancar_magia_acao_padrao",
                "efeito": "ataque_corpo_a_corpo_extra",
            }
        }
    },
    "BARDO_ESGRIMA_MAGICA": {
        "nome": "Esgrima Mágica",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Enquanto sob efeito de sua Inspiração, substitui testes de Luta por Atuação para ataques com armas corpo a corpo leves ou de uma mão.",
        "efeitos": {
            "ataque_pericia_troca": {
                "origem": "Luta",
                "destino": "Atuação",
                "condicao": "inspiracao",
                "empunhadura": ["Leve", "Uma Mão"],
            }
        }
    },
    "BARDO_ESTRELATO": {
        "nome": "Estrelato",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Nível 6"],
        "descricao": "Quando usa Atuação para impressionar uma plateia, o bônus recebido em perícias baseadas em Carisma aumenta para +5.",
        "efeitos": {"estrelato_bonus_carisma": 5}
    },
    "BARDO_FASCINAR_EM_MASSA": {
        "nome": "Fascinar em Massa",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Música: Balada Fascinante"],
        "descricao": "Quando usa Música: Balada Fascinante, pode gastar +2 PM para afetar todas as criaturas escolhidas no alcance da habilidade (um único teste de Atuação oposto pela Vontade de cada criatura).",
        "efeitos": {
            "aprimoramento_musica": {
                "musica": "Música: Balada Fascinante",
                "custo_pm_extra": 2,
                "efeito": "afeta_todas_criaturas_escolhidas_alcance",
            }
        }
    },
    "BARDO_GOLPE_ELEMENTAL": {
        "nome": "Golpe Elemental",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Golpe Mágico"],
        "descricao": "Enquanto sob efeito de sua Inspiração, sempre que acertar um ataque corpo a corpo, pode gastar 1 PM para causar +1d6 de dano extra (ácido, eletricidade, fogo ou frio). A cada 4 níveis, pode gastar +1 PM para +1d6.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "gatilho": "acertar_ataque_corpo_a_corpo_inspiracao",
                "dano_extra": "1d6",
                "tipos": ["ácido", "eletricidade", "fogo", "frio"],
                "escala_nivel": {"cada": 4, "dado_extra": "1d6", "custo_pm_extra": 1},
            }
        }
    },
    "BARDO_GOLPE_MAGICO": {
        "nome": "Golpe Mágico",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Esgrima Mágica"],
        "descricao": "Enquanto sob efeito de sua Inspiração, sempre que acertar um ataque corpo a corpo em um inimigo, recebe 2 PM temporários cumulativos (máximo por cena igual ao seu nível).",
        "efeitos": {
            "golpe_magico_pm_temp": 2,
            "limite_cena": "nivel",
            "condicao": "inspiracao",
        }
    },
    "BARDO_INSPIRACAO_MARCIAL": {
        "nome": "Inspiração Marcial",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Quando usa Inspiração, você e seus aliados aplicam o bônus recebido também em rolagens de dano.",
        "efeitos": {"inspiracao_aplica_dano": True}
    },
    "BARDO_LENDAS_HISTORIAS": {
        "nome": "Lendas e Histórias",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Int 1"],
        "descricao": "Pode gastar 1 PM para rolar novamente um teste recém realizado de Conhecimento, Misticismo, Nobreza ou Religião para informação, identificar criaturas ou identificar itens mágicos.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "efeito": "rerrolar_pericia",
                "pericias": ["Conhecimento", "Misticismo", "Nobreza", "Religião"],
            }
        }
    },
    "BARDO_MANIPULAR": {
        "nome": "Manipular",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Música: Balada Fascinante"],
        "descricao": "Pode gastar 1 PM para fazer uma criatura fascinada por você ficar enfeitiçada até o fim da cena (Vontade CD Car anula; se passar, fica imune por 1 dia). Usar esta habilidade não conta como ameaça à criatura fascinada.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "condicao_alvo": "fascinada",
                "efeito": "enfeiticar",
                "resistencia": "Vontade",
                "atributo_cd": "car",
            }
        }
    },
    "BARDO_MANIPULAR_EM_MASSA": {
        "nome": "Manipular em Massa",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Fascinar em Massa", "Manipular", "Nível 10"],
        "descricao": "Quando usa Manipular, pode gastar +2 PM para afetar todas as criaturas escolhidas em alcance curto.",
        "efeitos": {
            "aprimoramento_habilidade": {
                "habilidade": "Manipular",
                "custo_pm_extra": 2,
                "alcance": "curto",
                "efeito": "afeta_todas_criaturas_escolhidas",
            }
        }
    },
    "BARDO_MUSICA_BALADA_FASCINANTE": {
        "nome": "Música: Balada Fascinante",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Música de Bardo (requer treino em Atuação e instrumento musical; ação padrão, 1 PM, alcance curto): teste de Atuação oposto à Vontade de uma criatura. Se vencer, o alvo fica fascinado enquanto você se concentrar (ação padrão por rodada). Criatura hostil ou em combate recebe +5 no teste e novo teste a cada rodada de concentração. Se passar, fica imune por 1 dia.",
        "efeitos": {
            "musica_bardo": {
                "acao": "padrão",
                "custo_pm": 1,
                "alcance": "curto",
                "requer_instrumento": True,
                "requer_pericia": "Atuação",
                "efeito": "fascinado",
                "resistencia": "Vontade",
            }
        }
    },
    "BARDO_MUSICA_CANCAO_ASSUSTADORA": {
        "nome": "Música: Canção Assustadora",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Música de Bardo (requer treino em Atuação e instrumento musical; ação padrão, 1 PM, alcance curto): teste de Atuação oposto à Vontade de cada criatura escolhida no alcance. Alvos que falhem ficam abalados até o fim da cena. Alvos que passem ficam imunes por 1 dia.",
        "efeitos": {
            "musica_bardo": {
                "acao": "padrão",
                "custo_pm": 1,
                "alcance": "curto",
                "requer_instrumento": True,
                "requer_pericia": "Atuação",
                "efeito": "abalado",
                "resistencia": "Vontade",
            }
        }
    },
    "BARDO_MUSICA_MELODIA_CURATIVA": {
        "nome": "Música: Melodia Curativa",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Música de Bardo (requer treino em Atuação e instrumento musical; ação padrão, 1 PM, alcance curto): criaturas escolhidas no alcance recuperam 1d6 PV. Pode gastar +1 PM para aumentar a cura em +1d6 PV (sem limite além do limite de PM por nível).",
        "efeitos": {
            "musica_bardo": {
                "acao": "padrão",
                "custo_pm": 1,
                "alcance": "curto",
                "requer_instrumento": True,
                "requer_pericia": "Atuação",
                "cura": "1d6",
                "custo_pm_extra_por_dado": 1,
            }
        }
    },
    "BARDO_MELODIA_RESTAURADORA": {
        "nome": "Melodia Restauradora",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Música: Melodia Curativa"],
        "descricao": "Quando usa Música: Melodia Curativa, pode gastar +2 PM para remover uma condição (abalado, alquebrado, apavorado, atordoado, cego, confuso, enfeitiçado, esmorecido, exausto, fatigado, frustrado, pasmo ou surdo) das criaturas afetadas.",
        "efeitos": {
            "aprimoramento_musica": {
                "musica": "Música: Melodia Curativa",
                "custo_pm_extra": 2,
                "efeito": "remove_condicao",
                "condicoes": [
                    "abalado", "alquebrado", "apavorado", "atordoado", "cego",
                    "confuso", "enfeitiçado", "esmorecido", "exausto", "fatigado",
                    "frustrado", "pasmo", "surdo",
                ],
            }
        }
    },
    "BARDO_MESTRE_SUSSURROS": {
        "nome": "Mestre dos Sussurros",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Car 1", "Treinado em Enganação", "Treinado em Investigação"],
        "descricao": "Rola dois dados e usa o melhor resultado em testes de Investigação para interrogar e Enganação para intriga. Em ambientes sociais (tavernas, festas, cortes), pode fazer esses testes sem custo monetário e em 1 minuto.",
        "efeitos": {
            "vantagem_pericia_situacional": {
                "Investigação": "interrogar",
                "Enganação": "intriga",
            }
        }
    },
    "BARDO_PARODIA": {
        "nome": "Paródia",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "descricao": "Uma vez por rodada, quando vê outra criatura lançando uma magia em alcance médio, pode pagar 1 PM e fazer um teste de Atuação (CD 15 + custo em PM da magia). Se passar, até o final do seu próximo turno pode lançar essa magia.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "frequencia": "1x_por_rodada",
                "alcance": "médio",
                "pericia": "Atuação",
                "cd_formula": "15 + custo_pm",
            }
        }
    },
    "BARDO_PRESTIDIGITACAO": {
        "nome": "Prestidigitação",
        "tipo": "Poder de Bardo",
        "classe": "Bardo",
        "requisitos": ["Nível 6"],
        "descricao": "Quando faz uma ação padrão, pode fazer um teste de Atuação (CD 15 + custo em PM da magia) para lançar uma magia com execução de ação completa ou menor como ação livre (se falhar, a magia não funciona mas gasta os PM). Outros personagens só percebem com Misticismo CD 20.",
        "efeitos": {
            "acao_ativavel": {
                "gatilho": "acao_padrao",
                "acao": "livre",
                "pericia": "Atuação",
                "cd_formula": "15 + custo_pm",
                "cd_perceber_misticismo": 20,
            }
        }
    },

    # ==========================================================================
    # BUCANEIRO (T20 JdA, p. 46-48)
    # ==========================================================================
    "BUCANEIRO_AUDACIA": {
        "nome": "Audácia",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 1,
        "descricao": "Quando faz um teste de perícia, pode gastar 2 PM para somar seu Carisma no teste. Não pode ser usada em testes de ataque.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2,
                "efeito": "soma_carisma_pericia",
                "exceto_ataque": True,
            }
        }
    },
    "BUCANEIRO_INSOLENCIA": {
        "nome": "Insolência",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 1,
        "descricao": "Soma seu Carisma na Defesa, limitado pelo seu nível. Exige liberdade de movimentos (não funciona de armadura pesada ou imóvel).",
        "efeitos": {
            "defesa_soma_atributo": {
                "atributo": "car",
                "limite_por_nivel": True,
                "exige_liberdade_movimento": True,
            }
        }
    },
    "BUCANEIRO_EVASAO": {
        "nome": "Evasão",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 2,
        "descricao": "Quando sofre um efeito que permite teste de Reflexos para reduzir dano à metade, não sofre dano algum se passar. Exige liberdade de movimentos.",
        "efeitos": {"evasao": True, "exige_liberdade_movimento": True}
    },
    "BUCANEIRO_ESQUIVA_SAGAZ": {
        "nome": "Esquiva Sagaz",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 3,
        "descricao": "Recebe +1 na Defesa e em Reflexos. Esse bônus aumenta em +1 a cada quatro níveis (7º, 11º, 15º, 19º). Exige liberdade de movimentos.",
        "efeitos": {
            "defesa_bonus": 1,
            "bonus_pericia": {"Reflexos": 1},
            "escala_nivel": {"inicio": 3, "cada": 4, "bonus": 1, "classe": "Bucaneiro"},
            "exige_liberdade_movimento": True,
        }
    },
    "BUCANEIRO_PANACHE": {
        "nome": "Panache",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 5,
        "descricao": "Sempre que faz um acerto crítico em combate ou reduz um inimigo a 0 PV, recupera 1 PM.",
        "efeitos": {"panache_recupera_pm": 1}
    },
    "BUCANEIRO_EVASAO_APRIMORADA": {
        "nome": "Evasão Aprimorada",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 10,
        "descricao": "Quando sofre efeito com Reflexos para metade, não sofre dano se passar e sofre apenas metade se falhar. Exige liberdade de movimentos.",
        "efeitos": {"evasao_aprimorada": True, "exige_liberdade_movimento": True}
    },
    "BUCANEIRO_SORTE_DE_NIMB": {
        "nome": "Sorte de Nimb",
        "tipo": "Habilidade de Classe",
        "classe": "Bucaneiro",
        "nivel": 20,
        "descricao": "Quando faz um teste, pode gastar 5 PM para rolá-lo novamente. Qualquer resultado 11 ou mais na segunda rolagem é considerado um 20 natural.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 5,
                "efeito": "rerrolar_teste_11_vira_20",
            },
            "sorte_de_nimb": True,
        }
    },
    # --- PODERES DE BUCANEIRO (19 poderes oficiais, T20 JdA p. 46-48) ---
    "BUCANEIRO_ABUSAR_DOS_FRACOS": {
        "nome": "Abusar dos Fracos",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Flagelo dos Mares"],
        "descricao": "Quando ataca uma criatura sob efeito de uma condição de medo, seu dano aumenta em um passo.",
        "efeitos": {"abusar_dos_fracos_passo_dano": 1}
    },
    "BUCANEIRO_AMIGOS_NO_PORTO": {
        "nome": "Amigos no Porto",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Car 1", "Nível 6"],
        "descricao": "Ao chegar em comunidade portuária, teste de Carisma (CD 10) para encontrar um amigo que presta um favor ou atua como parceiro veterano de um tipo a sua escolha por um dia.",
        "efeitos": {
            "acao_ativavel": {
                "pericia_ou_atributo": "Carisma",
                "cd": 10,
                "efeito": "parceiro_veterano_ou_favor_1_dia",
            }
        }
    },
    "BUCANEIRO_APARAR": {
        "nome": "Aparar",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Esgrimista"],
        "descricao": "Uma vez por rodada, quando atingido por um ataque, pode gastar 1 PM para fazer teste de ataque com bônus igual ao seu nível (além do normal) com arma corpo a corpo leve ou ágil; se maior que o do oponente, evita o ataque.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "frequencia": "1x_por_rodada",
                "bonus_ataque": "nivel",
                "tipo_arma": ["leve", "ágil"],
                "efeito": "evitar_ataque",
            }
        }
    },
    "BUCANEIRO_APOSTADOR": {
        "nome": "Apostador",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Treinado em Jogatina"],
        "descricao": "Pode gastar um dia para participar de jogos de azar. Escolha um valor e faça teste de Jogatina: T$ 100 (CD 15), T$ 200 (CD 20), T$ 400 (CD 25), T$ 800 (CD 30), T$ 1.600 (CD 35) e assim por diante.",
        "efeitos": {
            "acao_ativavel": {
                "tempo": "1 dia",
                "pericia": "Jogatina",
                "efeito": "apostar_dinheiro",
            }
        }
    },
    "BUCANEIRO_ATAQUE_ACROBATICO": {
        "nome": "Ataque Acrobático",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Quando se aproxima de um inimigo com um salto ou pirueta (Atletismo ou Acrobacia para se mover) e o ataca no mesmo turno, recebe +2 nesse teste de ataque e na rolagem de dano.",
        "efeitos": {
            "ataque_acrobatico": {"ataque": 2, "dano": 2}
        }
    },
    "BUCANEIRO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "BUCANEIRO_AVENTUREIRO_AVIDO": {
        "nome": "Aventureiro Ávido",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Uma vez por rodada, pode gastar 5 PM para realizar uma ação padrão ou de movimento adicional. Se possuir Surto Heroico, em vez disso seu custo diminui em -2 PM.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 5,
                "frequencia": "1x_por_rodada",
                "efeito": "acao_padrao_ou_movimento_extra",
                "reducao_surto_heroico_pm": 2,
            }
        }
    },
    "BUCANEIRO_BRAVATA_AUDAZ": {
        "nome": "Bravata Audaz",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Bravata: jura fazer uma façanha específica (ND >= nível). Se cumprir, seus PM aumentam em +2 por nível de bucaneiro até o fim da aventura.",
        "efeitos": {
            "bravata": "audaz",
            "pm_por_nivel_se_cumprida": 2,
        }
    },
    "BUCANEIRO_BRAVATA_IMPRUDENTE": {
        "nome": "Bravata Imprudente",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Bravata: na 1ª rodada de combate, jura derrotar seus inimigos com uma restrição válida. Se vencer, recebe +2 nos testes de ataque e na margem de ameaça até o fim da aventura.",
        "efeitos": {
            "bravata": "imprudente",
            "ataque_se_cumprida": 2,
            "margem_ameaca_se_cumprida": 2,
        }
    },
    "BUCANEIRO_EN_GARDE": {
        "nome": "En Garde",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Esgrimista"],
        "descricao": "Ação de movimento, 1 PM: até o fim da cena, usando arma corpo a corpo leve ou ágil, recebe +2 na margem de ameaça com essas armas e +2 na Defesa.",
        "efeitos": {
            "acao_ativavel": {
                "acao": "movimento",
                "custo_pm": 1,
                "duracao": "cena",
                "defesa_bonus": 2,
                "margem_ameaca_bonus": 2,
                "tipo_arma": ["leve", "ágil"],
            }
        }
    },
    "BUCANEIRO_ESGRIMISTA": {
        "nome": "Esgrimista",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Int 1"],
        "descricao": "Quando usa uma arma corpo a corpo leve ou ágil, soma sua Inteligência nas rolagens de dano (limitado pelo seu nível).",
        "efeitos": {
            "dano_soma_atributo_extra": {
                "atributo": "int",
                "tipo_arma": ["leve", "ágil"],
                "limite_por_nivel": True,
            }
        }
    },
    "BUCANEIRO_FLAGELO_DOS_MARES": {
        "nome": "Flagelo dos Mares",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Treinado em Intimidação"],
        "descricao": "Aprende e pode lançar Amedrontar (atributo-chave Carisma). Não é uma habilidade mágica.",
        "efeitos": {
            "magia_adicional": {"nome": "Amedrontar", "atributo": "car", "nao_magica": True}
        }
    },
    "BUCANEIRO_FOLIAO": {
        "nome": "Folião",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Car 1"],
        "descricao": "Durante festas, tavernas e bailes, recebe +2 em testes de perícias de Carisma e a atitude de todas as pessoas em relação a você melhora em uma categoria.",
        "efeitos": {"foliao_bonus_carisma": 2}
    },
    "BUCANEIRO_GRUDAR_O_CANO": {
        "nome": "Grudar o Cano",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Treinado em Luta", "Pistoleiro"],
        "descricao": "Quando faz um ataque à distância com arma de fogo contra oponente adjacente, não sofre a penalidade de -5 no teste de ataque e aumenta seu dano em um passo.",
        "efeitos": {"grudar_o_cano": True}
    },
    "BUCANEIRO_PERNAS_DO_MAR": {
        "nome": "Pernas do Mar",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Recebe +2 em Acrobacia e Atletismo. Quando está se equilibrando ou escalando, não fica desprevenido e seu deslocamento não é reduzido à metade.",
        "efeitos": {
            "bonus_pericia": {"Acrobacia": 2, "Atletismo": 2},
            "pernas_do_mar": True,
        }
    },
    "BUCANEIRO_PISTOLEIRO": {
        "nome": "Pistoleiro",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "descricao": "Recebe proficiência com armas de fogo e +2 nas rolagens de dano com essas armas.",
        "efeitos": {
            "proficiencia_adicional": ["Armas de Fogo"],
            "dano_bonus_condicional": {"tipo": "arma_fogo", "valor": 2},
        }
    },
    "BUCANEIRO_PRESENCA_PARALISANTE": {
        "nome": "Presença Paralisante",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Car 1", "Nível 4"],
        "descricao": "Soma seu Carisma em Iniciativa e, se for o primeiro na iniciativa, ganha uma ação padrão extra na primeira rodada.",
        "efeitos": {
            "pericia_soma_atributo": {"Iniciativa": "car"},
            "presenca_paralisante": True,
        }
    },
    "BUCANEIRO_RIPOSTAR": {
        "nome": "Ripostar",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Aparar", "Nível 12"],
        "descricao": "Quando usa Aparar e evita o ataque, pode gastar 1 PM para fazer um ataque corpo a corpo imediato contra o inimigo que o atacou (se em alcance).",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "gatilho": "evitar_ataque_com_aparar",
                "efeito": "ataque_corpo_a_corpo_imediato",
            }
        }
    },
    "BUCANEIRO_TOUCHE": {
        "nome": "Touché",
        "tipo": "Poder de Bucaneiro",
        "classe": "Bucaneiro",
        "requisitos": ["Esgrimista", "Nível 10"],
        "descricao": "Quando se aproxima de um inimigo e o ataca com arma corpo a corpo leve ou ágil no mesmo turno, pode gastar 2 PM para aumentar seu dano em um passo e receber +5 na margem de ameaça neste ataque.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2,
                "tipo_arma": ["leve", "ágil"],
                "passo_dano": 1,
                "margem_ameaca_bonus": 5,
            }
        }
    },

    # ==========================================================================
    # CAÇADOR (T20 JdA, p. 49-51)
    # ==========================================================================
    "CACADOR_MARCA_PRESA": {
        "nome": "Marca da Presa",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 1,
        "descricao": "Ação de movimento, 1 PM: analisa uma criatura em alcance curto; até o fim da cena recebe +1d4 nas rolagens de dano contra ela. A cada 4 níveis, pode gastar +1 PM para aumentar o bônus (+1d8 no 5º, +1d12 no 9º, +2d8 no 13º, +2d10 no 17º).",
        "efeitos": {
            "acao_ativavel": {
                "acao": "movimento",
                "custo_pm": 1,
                "alcance": "curto",
                "duracao": "cena",
                "progressao_dados": ["1d4", "1d8", "1d12", "2d8", "2d10"],
                "escala_nivel": 4,
            },
            "dano_bonus_dado": "1d4",
        }
    },
    "CACADOR_RASTREADOR": {
        "nome": "Rastreador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 1,
        "descricao": "Recebe +2 em Sobrevivência e pode se mover com deslocamento normal enquanto rastreia sem sofrer penalidade no teste.",
        "efeitos": {"bonus_pericia": {"Sobrevivência": 2}, "rastreador_sem_penalidade": True}
    },
    "CACADOR_EXPLORADOR": {
        "nome": "Explorador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 3,
        "descricao": "Escolha um tipo de terreno (aquático, ártico, colina, deserto, floresta, montanha, pântano, planície, subterrâneo ou urbano; a partir do 11º nível, também área de Tormenta). Nesse terreno, soma Sabedoria (mínimo +1) na Defesa e em Acrobacia, Atletismo, Furtividade, Percepção e Sobrevivência. A cada 4 níveis (7º, 11º, 15º, 19º), escolhe outro terreno ou aumenta o bônus em um já escolhido em +2.",
        "efeitos": {
            "terreno_predileto_escolha": 1,
            "explorador_terreno": True,
            "pericias_terreno": ["Acrobacia", "Atletismo", "Furtividade", "Percepção", "Sobrevivência"],
        }
    },
    "CACADOR_CAMINHO_EXPLORADOR": {
        "nome": "Caminho do Explorador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 5,
        "descricao": "Em terrenos nos quais possua Explorador, atravessa terrenos difíceis sem reduzir seu deslocamento e a CD para rastreá-lo aumenta em +10.",
        "efeitos": {"caminho_do_explorador": True, "cd_rastrear_bonus": 10}
    },
    "CACADOR_MESTRE_CACADOR": {
        "nome": "Mestre Caçador",
        "tipo": "Habilidade de Classe",
        "classe": "Caçador",
        "nivel": 20,
        "descricao": "Usa Marca da Presa como ação livre. Ao usá-la, pode pagar 5 PM para aumentar sua margem de ameaça contra a criatura em +2. Se reduzir uma criatura marcada a 0 PV, recupera 5 PM.",
        "efeitos": {
            "mestre_cacador": True,
            "marca_presa_acao_livre": True,
            "recupera_pm_abate_marcada": 5,
        }
    },
    # --- PODERES DE CAÇADOR (23 poderes oficiais, T20 JdA p. 50-51) ---
    "CACADOR_AMBIDESTRIA": {
        "nome": "Ambidestria",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Des 2"],
        "descricao": "Empunhando duas armas (ao menos uma leve) na ação agredir, pode fazer dois ataques (um com cada arma) sofrendo -2 em todos os testes de ataque até seu próximo turno.",
        "efeitos": {"ambidestria": True, "penalidade_ataque": -2}
    },
    "CACADOR_ARMADILHA_ARATACA": {
        "nome": "Armadilha: Arataca",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Armadilha (ação completa, 3 PM, área 3m adjacente, Investigação CD Sab): a vítima sofre 2d6 pontos de dano de perfuração e fica agarrada (escapar: ação padrão, Força ou Acrobacia CD Sab).",
        "efeitos": {
            "armadilha": {
                "acao": "completa", "custo_pm": 3, "area": "3m",
                "dano": "2d6", "tipo_dano": "perfuração",
                "condicao": "agarrada", "cd_atributo": "sab",
            }
        }
    },
    "CACADOR_ARMADILHA_ESPINHOS": {
        "nome": "Armadilha: Espinhos",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Armadilha (ação completa, 3 PM, área 3m adjacente, Investigação CD Sab): a vítima sofre 6d6 pontos de dano de perfuração (Reflexos CD Sab reduz à metade).",
        "efeitos": {
            "armadilha": {
                "acao": "completa", "custo_pm": 3, "area": "3m",
                "dano": "6d6", "tipo_dano": "perfuração",
                "resistencia": "Reflexos", "cd_atributo": "sab",
            }
        }
    },
    "CACADOR_ARMADILHA_LACO": {
        "nome": "Armadilha: Laço",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Armadilha (ação completa, 3 PM, área 3m adjacente, Investigação CD Sab): a vítima faz Reflexos CD Sab; se passar, fica caída; se falhar, fica agarrada (soltar: ação padrão, Força ou Acrobacia CD Sab).",
        "efeitos": {
            "armadilha": {
                "acao": "completa", "custo_pm": 3, "area": "3m",
                "resistencia": "Reflexos", "cd_atributo": "sab",
                "efeito_sucesso": "caída", "efeito_falha": "agarrada",
            }
        }
    },
    "CACADOR_ARMADILHA_REDE": {
        "nome": "Armadilha: Rede",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Armadilha (ação completa, 3 PM, área 3m adjacente, Investigação CD Sab): todas as criaturas na área ficam enredadas e não podem sair (libertar: ação padrão, Força ou Acrobacia CD 25). Área vira terreno difícil; escolhe quantas criaturas ativam.",
        "efeitos": {
            "armadilha": {
                "acao": "completa", "custo_pm": 3, "area": "3m",
                "condicao": "enredada", "cd_escapar": 25, "terreno_dificil": True,
            }
        }
    },
    "CACADOR_ARMADILHEIRO": {
        "nome": "Armadilheiro",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Um poder de armadilha", "Nível 5"],
        "descricao": "Soma sua Sabedoria no dano e na CD de suas armadilhas (cumulativo).",
        "efeitos": {"armadilheiro_soma_sab": True}
    },
    "CACADOR_ARQUEIRO": {
        "nome": "Arqueiro",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Sab 1"],
        "descricao": "Usando arma de ataque à distância, soma sua Sabedoria nas rolagens de dano (limitado pelo seu nível).",
        "efeitos": {"dano_distancia_soma_atributo": {"atributo": "sab", "limite_por_nivel": True}}
    },
    "CACADOR_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "CACADOR_BOTE": {
        "nome": "Bote",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Ambidestria", "Nível 6"],
        "descricao": "Empunhando duas armas durante uma investida, pode pagar 1 PM para fazer um ataque adicional com sua arma secundária.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1, "gatilho": "investida_duas_armas",
                "efeito": "ataque_adicional_arma_secundaria",
            }
        }
    },
    "CACADOR_CAMUFLAGEM": {
        "nome": "Camuflagem",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Nível 6"],
        "descricao": "Pode gastar 2 PM para se esconder mesmo sem camuflagem ou cobertura disponível.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "efeito": "esconder_sem_cobertura"}
        }
    },
    "CACADOR_CHUVA_LAMINAS": {
        "nome": "Chuva de Lâminas",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Des 4", "Ambidestria", "Nível 12"],
        "descricao": "Uma vez por rodada, quando usa Ambidestria, pode pagar 2 PM para fazer um ataque adicional com sua arma primária.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2, "frequencia": "1x_por_rodada",
                "gatilho": "ambidestria", "efeito": "ataque_adicional_arma_primaria",
            }
        }
    },
    "CACADOR_COMPANHEIRO_ANIMAL": {
        "nome": "Companheiro Animal",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Car 1", "Treinado em Adestramento"],
        "descricao": "Recebe um companheiro animal (parceiro).",
        "efeitos": {"parceiro_adicional": 1}
    },
    "CACADOR_ELO_NATUREZA": {
        "nome": "Elo com a Natureza",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Sab 1", "Nível 3"],
        "descricao": "Soma sua Sabedoria no total de PM e aprende e pode lançar Caminhos da Natureza (atributo-chave Sabedoria).",
        "efeitos": {
            "pm_soma_atributo": "sab",
            "magia_adicional": {"nome": "Caminhos da Natureza", "atributo": "sab"},
        }
    },
    "CACADOR_EMBOSCAR": {
        "nome": "Emboscar",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "Na primeira rodada de um combate, pode gastar 2 PM para realizar uma ação padrão adicional em seu turno.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2, "gatilho": "primeira_rodada_combate",
                "efeito": "acao_padrao_adicional",
            }
        }
    },
    "CACADOR_EMPATIA_SELVAGEM": {
        "nome": "Empatia Selvagem",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Comunica-se com animais por linguagem corporal e vocalizações; usa Adestramento com animais para mudar atitude e persuasão.",
        "efeitos": {
            "pericia_adestramento_persuasao": True,
            "bonus_pericia_se_duplicada": {"Adestramento": 2},
        }
    },
    "CACADOR_ESCARAMUCA": {
        "nome": "Escaramuça",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Des 2", "Nível 6"],
        "descricao": "Quando se move 6m ou mais, recebe +2 na Defesa e Reflexos e +1d8 nas rolagens de dano corpo a corpo e à distância em alcance curto até o início do próximo turno (não funciona de armadura pesada).",
        "efeitos": {
            "escaramuca": {"defesa": 2, "reflexos": 2, "dano": "1d8", "sem_armadura_pesada": True}
        }
    },
    "CACADOR_ESCARAMUCA_SUPERIOR": {
        "nome": "Escaramuça Superior",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "requisitos": ["Escaramuça", "Nível 12"],
        "descricao": "Aumenta os bônus de Escaramuça para +5 na Defesa e Reflexos e +1d12 em rolagens de dano.",
        "efeitos": {
            "escaramuca_superior": {"defesa": 5, "reflexos": 5, "dano": "1d12", "sem_armadura_pesada": True}
        }
    },
    "CACADOR_ESPREITAR": {
        "nome": "Espreitar",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Quando usa Marca da Presa, recebe +1 em testes de perícia contra a criatura marcada (+1 por PM adicional gasto; dobra com Inimigo).",
        "efeitos": {"espreitar_marca_presa": True}
    },
    "CACADOR_ERVAS_CURATIVAS": {
        "nome": "Ervas Curativas",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Ação completa + PM (limitado por Sabedoria): aplica ervas em si ou aliado adjacente; para cada PM gasto, cura 2d6 PV ou remove uma condição envenenado.",
        "efeitos": {
            "acao_ativavel": {
                "acao": "completa", "custo_pm": "variavel",
                "limite_pm": "sabedoria", "cura_por_pm": "2d6",
                "remove_condicao": "envenenado",
            }
        }
    },
    "CACADOR_IMPETO": {
        "nome": "Ímpeto",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Pode gastar 1 PM para aumentar seu deslocamento em +6m por uma rodada.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 1, "deslocamento_bonus": 6, "duracao": "1 rodada"}
        }
    },
    "CACADOR_INIMIGO": {
        "nome": "Inimigo de (Criatura)",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Escolha um tipo de criatura (animal, construto, espírito, monstro ou morto-vivo) ou duas raças humanoides. Ao usar Marca da Presa contra ela, dobra os dados de bônus no dano. Pode escolher outras vezes para inimigos diferentes.",
        "efeitos": {"inimigo_predileto_escolha": 1, "multipla_escolha": True}
    },
    "CACADOR_OLHO_FALCAO": {
        "nome": "Olho do Falcão",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Pode usar a habilidade Marca da Presa em criaturas em alcance longo.",
        "efeitos": {"marca_presa_alcance": "Longo"}
    },
    "CACADOR_PONTO_FRACO": {
        "nome": "Ponto Fraco",
        "tipo": "Poder de Caçador",
        "classe": "Caçador",
        "descricao": "Quando usa Marca da Presa, seus ataques contra a criatura marcada recebem +2 na margem de ameaça (dobra com Inimigo).",
        "efeitos": {"ponto_fraco_margem": 2}
    },

    # ==========================================================================
    # CAVALEIRO (T20 JdA, p. 52-55)
    # ==========================================================================
    "CAVALEIRO_CODIGO_HONRA": {
        "nome": "Código de Honra",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 1,
        "descricao": "Não pode atacar oponente pelas costas (flanquear), caído, desprevenido ou incapaz de lutar. Se violar, perde todos os PM e só pode recuperá-los a partir do próximo dia.",
        "efeitos": {"codigo_de_honra": True}
    },
    "CAVALEIRO_BALUARTE": {
        "nome": "Baluarte",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 1,
        "descricao": "Ao sofrer ataque ou fazer teste de resistência, 1 PM para +2 Defesa e resistências até início do próximo turno (+2/+1 PM a cada 4 níveis: +4 no 5º, +6 no 9º, +8 no 13º, +10 no 17º). 7º nível: +2 PM estende a aliados adjacentes; 15º nível: +5 PM estende a alcance curto.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "bonus_defesa_resistencia": 2,
                "escala_nivel": {"cada": 4, "bonus": 2, "custo_pm_extra": 1},
            }
        }
    },
    "CAVALEIRO_DUELO": {
        "nome": "Duelo",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 2,
        "descricao": "2 PM: escolhe um oponente em alcance curto e recebe +2 em ataques e dano contra ele até fim da cena (termina se atacar outro). A cada 5 níveis (7º, 12º, 17º), +1 PM para +1 bônus.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 2,
                "alcance": "curto",
                "duracao": "cena",
                "bonus_ataque_dano": 2,
                "escala_nivel": {"inicio": 2, "cada": 5, "bonus": 1, "custo_pm_extra": 1},
            }
        }
    },
    "CAVALEIRO_CAMINHO": {
        "nome": "Caminho do Cavaleiro",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 5,
        "descricao": "Escolha entre Bastião (RD 5 de armadura pesada, cumulativa com Especialização em Armadura) ou Montaria (cavalo de guerra com +5 Adestramento e Cavalgar, parceiro veterano; mestre no 11º).",
        "efeitos": {"escolha_caminho_cavaleiro": ["Bastião", "Montaria"]}
    },
    "CAVALEIRO_RESOLUTO": {
        "nome": "Resoluto",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 11,
        "descricao": "1 PM para refazer um teste de resistência contra uma condição que o esteja afetando com +5 de bônus (se passar, cancela o efeito; 1x por efeito).",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 1, "bonus_rerrolagem": 5, "efeito": "refazer_resistencia_condicao"},
            "resoluto": True,
        }
    },
    "CAVALEIRO_BRAVURA_FINAL": {
        "nome": "Bravura Final",
        "tipo": "Habilidade de Classe",
        "classe": "Cavaleiro",
        "nivel": 20,
        "descricao": "Se reduzido a 0 ou menos PV, pode gastar 3 PM (sustentada) para continuar consciente e de pé.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 3, "duracao": "sustentada", "efeito": "continuar_de_pe_0_pv"},
            "bravura_final": True,
        }
    },
    # --- PODERES DE CAVALEIRO (20 poderes oficiais, T20 JdA p. 53-55) ---
    "CAVALEIRO_ARMADURA_HONRA": {
        "nome": "Armadura da Honra",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "No início de cada cena, recebe PV temporários iguais a seu nível + seu Carisma (duram até o final da cena).",
        "efeitos": {"armadura_honra_pv_temp": True}
    },
    "CAVALEIRO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "CAVALEIRO_AUTORIDADE_FEUDAL": {
        "nome": "Autoridade Feudal",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Nível 6"],
        "descricao": "1 hora e 2 PM: conclama o povo (sem título ou posição religiosa) como parceiro iniciante de um tipo a sua escolha até o fim da aventura.",
        "efeitos": {
            "acao_ativavel": {"tempo": "1 hora", "custo_pm": 2, "efeito": "parceiro_iniciante_aventura"}
        }
    },
    "CAVALEIRO_DESPREZAR_COVARDES": {
        "nome": "Desprezar os Covardes",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Recebe redução de dano 5 se estiver caído, desprevenido ou flanqueado.",
        "efeitos": {"rd_condicional_covardes": 5}
    },
    "CAVALEIRO_ESCUDEIRO": {
        "nome": "Escudeiro",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Parceiro especial que não conta no limite: suas armas fornecem +1 dano e sua armadura concede +1 Defesa. 1 PM: ação de movimento extra (levantar, sacar item ou trazer montaria).",
        "efeitos": {"dano_bonus": 1, "defesa_bonus_armadura": 1, "escudeiro": True}
    },
    "CAVALEIRO_ESPECIALIZACAO_ARMADURA": {
        "nome": "Especialização em Armadura",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Nível 12"],
        "descricao": "Se estiver usando armadura pesada, recebe redução de dano 5 (cumulativa com a RD de Bastião).",
        "efeitos": {"rd_armadura_pesada": 5}
    },
    "CAVALEIRO_ESTANDARTE": {
        "nome": "Estandarte",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Título", "Nível 14"],
        "descricao": "No início de cada cena, você e todos os aliados que possam ver seu estandarte recebem PM temporários iguais ao seu Carisma (mínimo 1).",
        "efeitos": {"estandarte_pm_temp": True}
    },
    "CAVALEIRO_ETIQUETA": {
        "nome": "Etiqueta",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Recebe +2 em Diplomacia e Nobreza; ao fazer teste dessas perícias, pode gastar 1 PM para rolá-lo novamente.",
        "efeitos": {
            "bonus_pericia": {"Diplomacia": 2, "Nobreza": 2},
            "acao_ativavel": {"custo_pm": 1, "efeito": "rerrolar_diplomacia_nobreza"},
        }
    },
    "CAVALEIRO_INVESTIDA_DESTRUIDORA": {
        "nome": "Investida Destruidora",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Ao fazer a ação investida, pode gastar 2 PM (antes de rolar o ataque) para causar +2d8 pontos de dano.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "gatilho": "investida", "dano_extra": "2d8"}
        }
    },
    "CAVALEIRO_MONTARIA_CORAJOSA": {
        "nome": "Montaria Corajosa",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Montaria"],
        "descricao": "Sua montaria concede +1d6 em rolagens de dano corpo a corpo (cumulativo com qualquer bônus de parceiro).",
        "efeitos": {"montaria_corajosa_dano": "1d6"}
    },
    "CAVALEIRO_PAJEM": {
        "nome": "Pajem",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Recebe +2 em Diplomacia e sua condição de descanso sobe uma categoria. Executa pequenas tarefas e não conta no limite de parceiros.",
        "efeitos": {"bonus_pericia": {"Diplomacia": 2}, "descanso_categoria_acima": 1}
    },
    "CAVALEIRO_POSTURA_ARIETE": {
        "nome": "Postura de Combate: Aríete Implacável",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena): +2 ataque em investidas (+1 por +2 PM extra) e +2d8 dano contra construtos ou objetos. Precisa se deslocar todos os turnos para manter.",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "bonus_investida": 2, "dano_construto_objeto": "2d8",
            }
        }
    },
    "CAVALEIRO_POSTURA_CASTIGO": {
        "nome": "Postura de Combate: Castigo de Ferro",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena): sempre que um aliado adjacente sofrer ataque corpo a corpo, pode gastar 1 PM para fazer um ataque na criatura que o atacou.",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "custo_contra_ataque": 1,
            }
        }
    },
    "CAVALEIRO_POSTURA_FOCO": {
        "nome": "Postura de Combate: Foco de Batalha",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena): sempre que um inimigo atacá-lo, recebe 1 PM temporário cumulativo (máximo por cena igual ao nível).",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "pm_temp_por_ataque": 1, "limite_cena": "nivel",
            }
        }
    },
    "CAVALEIRO_POSTURA_MURALHA": {
        "nome": "Postura de Combate: Muralha Intransponível",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena, requer escudo): +1 Defesa e Reflexos (+1 por +2 PM extra), Evasão em Reflexos para metade, mas deslocamento reduzido para 3m.",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "requer_escudo": True, "bonus_defesa_reflexos": 1, "deslocamento": 3,
            }
        }
    },
    "CAVALEIRO_POSTURA_PROVOCACAO": {
        "nome": "Postura de Combate: Provocação Petulante",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena): inimigos que iniciarem turnos em alcance curto fazem Vontade (CD Car); se falharem, ações hostis devem ter você como alvo. Mental.",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "resistencia": "Vontade", "atributo_cd": "car", "mental": True,
            }
        }
    },
    "CAVALEIRO_POSTURA_TORRE": {
        "nome": "Postura de Combate: Torre Inabalável",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Postura (movimento, 2 PM, cena): imune a ser tirado do lugar (mundano/mágico), não pode se deslocar, soma Constituição na Defesa e pode substituir Reflexos e Vontade por Fortitude.",
        "efeitos": {
            "postura_combate": {
                "acao": "movimento", "custo_pm": 2, "duracao": "cena",
                "deslocamento": 0, "defesa_soma_con": True, "substitui_resistencias_fortitude": True,
            }
        }
    },
    "CAVALEIRO_SOLIDEZ": {
        "nome": "Solidez",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Se estiver usando um escudo, soma o bônus na Defesa recebido pelo escudo em testes de resistência.",
        "efeitos": {"solidez_escudo_resistencias": True}
    },
    "CAVALEIRO_TITULO": {
        "nome": "Título",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "requisitos": ["Autoridade Feudal", "Nível 10"],
        "descricao": "Adquire título de nobreza: início de cada aventura recebe 20 TO por nível de cavaleiro ou ajuda de um parceiro veterano da corte.",
        "efeitos": {"titulo_nobreza_to_por_nivel": 20}
    },
    "CAVALEIRO_TORRE_ARMADA": {
        "nome": "Torre Armada",
        "tipo": "Poder de Cavaleiro",
        "classe": "Cavaleiro",
        "descricao": "Quando um inimigo erra um ataque contra você, pode gastar 1 PM para receber +5 em rolagens de dano contra esse inimigo até o fim do seu próximo turno.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 1, "gatilho": "inimigo_erra_ataque", "dano_bonus": 5}
        }
    },

    # ==========================================================================
    # CLÉRIGO (T20 JdA, p. 56-58)
    # ==========================================================================
    "CLERIGO_DEVOTO": {
        "nome": "Devoto Fiel",
        "tipo": "Habilidade de Classe",
        "classe": "Clérigo",
        "nivel": 1,
        "descricao": "Torna-se devoto de um deus maior e recebe dois poderes concedidos (em vez de um). Alternativamente, pode cultuar o Panteão (sem poder concedido; proibição de armas cortantes/perfurantes; arma preferida maça; escolhe energia positiva ou negativa).",
        "efeitos": {"escolha_divindade": True, "poderes_concedidos_bonus": 1, "permite_panteao": True}
    },
    "CLERIGO_MAGIAS": {
        "nome": "Magias (Clérigo)",
        "tipo": "Habilidade de Classe",
        "classe": "Clérigo",
        "nivel": 1,
        "descricao": "Lança magias divinas de 1º círculo (+1 círculo a cada 4 níveis: 2º no 5º, 3º no 9º, 4º no 13º, 5º no 17º). Começa com 3 magias de 1º círculo e aprende +1 por nível. Atributo-chave: Sabedoria (soma Sabedoria no total de PM).",
        "efeitos": {"habilita_magia": {"tipo": "Divina", "atributo": "sab", "circulo_max": 1}}
    },
    "CLERIGO_MAO_DIVINDADE": {
        "nome": "Mão da Divindade",
        "tipo": "Habilidade de Classe",
        "classe": "Clérigo",
        "nivel": 20,
        "descricao": "Ação completa, 15 PM: lança três magias divinas quaisquer (mesmo desconhecidas) como ação livre sem gastar PM (paga aprimoramentos e outros custos). Após usar, fica atordoado por 1d4 rodadas (mesmo se imune).",
        "efeitos": {
            "acao_ativavel": {"acao": "completa", "custo_pm": 15, "magias_livres": 3, "atordoado_rodadas": "1d4"},
            "mao_da_divindade": True,
        }
    },
    # --- PODERES DE CLÉRIGO (18 poderes oficiais, T20 JdA p. 57-58) ---
    "CLERIGO_ABENCOAR_ARMA": {
        "nome": "Abençoar Arma",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Proficiente na arma preferida de sua divindade. Empunhando-a, ação de movimento e 3 PM: até fim da cena, arma mágica que ilumina como tocha, dano +1 passo e usa Sabedoria em ataque e dano (não cumulativo com efeitos que somam Sab).",
        "efeitos": {
            "proficiencia_arma_divindade": True,
            "acao_ativavel": {"acao": "movimento", "custo_pm": 3, "duracao": "cena", "passo_dano": 1, "atributo_ataque_dano": "sab"},
        }
    },
    "CLERIGO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "CLERIGO_AUTORIDADE_ECLESIASTICA": {
        "nome": "Autoridade Eclesiástica",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "requisitos": ["Nível 5", "Devoto de um deus maior"],
        "descricao": "Recebe +5 em Diplomacia ou Intimidação ao lidar com devotos de sua divindade e paga metade do preço de itens alquímicos, poções e serviços em templos de sua divindade.",
        "efeitos": {"autoridade_eclesiastica": {"bonus_devotos": 5, "desconto_templo": 0.5}}
    },
    "CLERIGO_CANALIZAR": {
        "nome": "Canalizar Energia Positiva/Negativa",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ação padrão + PM, alcance curto: libera onda de luz (cura 1d6/PM em vivos, 1d6/PM dano luz em mortos-vivos, Vontade CD Sab metade) ou trevas (inverso).",
        "efeitos": {
            "acao_ativavel": {
                "acao": "padrão", "custo_pm": "variavel", "alcance": "curto",
                "por_pm": "1d6", "resistencia": "Vontade", "atributo_cd": "sab",
            }
        }
    },
    "CLERIGO_CANALIZAR_AMPLO": {
        "nome": "Canalizar Amplo",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "requisitos": ["Canalizar Energia Positiva/Negativa"],
        "descricao": "Ao usar Canalizar Energia, pode gastar +2 PM para aumentar o alcance para médio.",
        "efeitos": {"canalizar_alcance_medio": True, "custo_pm_extra": 2}
    },
    "CLERIGO_COMUNHAO_VITAL": {
        "nome": "Comunhão Vital",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ao lançar magia que cure uma criatura, pode pagar +2 PM para outra criatura em alcance curto (ou você mesmo) recuperar metade dos PV da cura original.",
        "efeitos": {"comunhao_vital": {"custo_pm_extra": 2, "alcance": "curto"}}
    },
    "CLERIGO_CONHECIMENTO_MAGICO": {
        "nome": "Conhecimento Mágico",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Aprende duas magias de qualquer círculo que possa lançar. Pode escolher este poder quantas vezes quiser.",
        "efeitos": {"magias_adicionais": 2, "multipla_escolha": True}
    },
    "CLERIGO_EXPULSAR_COMANDAR": {
        "nome": "Expulsar/Comandar Mortos-Vivos",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "requisitos": ["Canalizar Energia Positiva/Negativa"],
        "descricao": "Ação padrão, 3 PM, alcance curto: expulsa (apavorados 1d6 rodadas) ou comanda (não inteligentes Int -4 ou menor por 1 dia até soma ND = nível + 3; inteligentes fascinados 1 rodada) mortos-vivos. Vontade CD Sab anula.",
        "efeitos": {
            "acao_ativavel": {
                "acao": "padrão", "custo_pm": 3, "alcance": "curto",
                "resistencia": "Vontade", "atributo_cd": "sab",
            }
        }
    },
    "CLERIGO_LITURGIA_MAGICA": {
        "nome": "Liturgia Mágica",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ação de movimento: aumenta em +2 a CD para resistir à sua próxima habilidade de clérigo (usada até o final do próximo turno).",
        "efeitos": {"cd_clerigo_liturgia": 2}
    },
    "CLERIGO_MAGIA_SAGRADA_PROFANA": {
        "nome": "Magia Sagrada/Profana",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ao lançar magia divina de dano, pode gastar +1 PM para mudar o tipo de dano para luz (positiva) ou trevas (negativa).",
        "efeitos": {"magia_sagrada_profana": {"custo_pm_extra": 1}}
    },
    "CLERIGO_MESTRE_CELEBRANTE": {
        "nome": "Mestre Celebrante",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "requisitos": ["Qualquer poder de Missa", "Nível 12"],
        "descricao": "O número de pessoas afetadas por uma Missa aumenta em dez vezes e os benefícios que elas recebem dobram.",
        "efeitos": {"mestre_celebrante": True, "missa_pessoas_mult": 10, "missa_beneficio_mult": 2}
    },
    "CLERIGO_MISSA_BENCAO_VIDA": {
        "nome": "Missa: Bênção da Vida",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa (1 hora, T$ 25, 1 + Sab pessoas, 1 dia): participantes recebem PV temporários iguais ao seu nível + sua Sabedoria.",
        "efeitos": {"missa": {"tempo": "1 hora", "custo_to": 25, "duracao": "1 dia", "tipo": "bencao_da_vida"}}
    },
    "CLERIGO_MISSA_CHAMADO_ARMAS": {
        "nome": "Missa: Chamado às Armas",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa (1 hora, T$ 25, 1 + Sab pessoas, 1 dia): participantes recebem +1 em testes de ataque e rolagens de dano.",
        "efeitos": {"missa": {"tempo": "1 hora", "custo_to": 25, "duracao": "1 dia", "tipo": "chamado_as_armas", "bonus_ataque_dano": 1}}
    },
    "CLERIGO_MISSA_ELEVACAO_ESPIRITO": {
        "nome": "Missa: Elevação do Espírito",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa (1 hora, T$ 25, 1 + Sab pessoas, 1 dia): participantes recebem PM temporários iguais à sua Sabedoria.",
        "efeitos": {"missa": {"tempo": "1 hora", "custo_to": 25, "duracao": "1 dia", "tipo": "elevacao_do_espirito"}}
    },
    "CLERIGO_MISSA_ESCUDO": {
        "nome": "Missa: Escudo Divino",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa (1 hora, T$ 25, 1 + Sab pessoas, 1 dia): participantes recebem +1 na Defesa e em testes de resistência.",
        "efeitos": {"missa": {"tempo": "1 hora", "custo_to": 25, "duracao": "1 dia", "tipo": "escudo_divino", "bonus_defesa_resistencia": 1}}
    },
    "CLERIGO_MISSA_SUPERAR_LIMITACOES": {
        "nome": "Missa: Superar as Limitações",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Missa (1 hora, T$ 25, 1 + Sab pessoas, 1 dia): cada participante recebe +1d6 num único teste à escolha (pode usar mesmo após rolar o dado).",
        "efeitos": {"missa": {"tempo": "1 hora", "custo_to": 25, "duracao": "1 dia", "tipo": "superar_as_limitacoes", "bonus_dado": "1d6"}}
    },
    "CLERIGO_PRECE_COMBATE": {
        "nome": "Prece de Combate",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ao lançar magia divina (ação padrão) em si mesmo, pode gastar +2 PM para lançá-la como ação de movimento.",
        "efeitos": {"prece_de_combate": {"custo_pm_extra": 2}}
    },
    "CLERIGO_SIMBOLO_ENERGIZADO": {
        "nome": "Símbolo Sagrado Energizado",
        "tipo": "Poder de Clérigo",
        "classe": "Clérigo",
        "descricao": "Ação de movimento, 1 PM: energiza seu símbolo sagrado até o fim da cena (ilumina como tocha); enquanto empunhá-lo, reduz o custo em PM de suas magias divinas em -1 PM.",
        "efeitos": {
            "acao_ativavel": {"acao": "movimento", "custo_pm": 1, "duracao": "cena"},
            "reducao_pm_magias_divinas_energizado": 1,
        }
    },

    # ==========================================================================
    # DRUIDA (T20 JdA, p. 60-63)
    # ==========================================================================
    "DRUIDA_DEVOTO": {
        "nome": "Devoto Fiel (Druida)",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Torna-se devoto de Allihanna, Megalokk ou Oceano e recebe dois poderes concedidos (em vez de um).",
        "efeitos": {"escolha_divindade": {"restrito": ["Allihanna", "Megalokk", "Oceano"]}, "poderes_concedidos_bonus": 1}
    },
    "DRUIDA_EMPATIA": {
        "nome": "Empatia Selvagem",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Comunica-se com animais por linguagem corporal e vocalizações; usa Adestramento com animais para mudar atitude e persuasão.",
        "efeitos": {
            "pericia_adestramento_persuasao": True,
            "bonus_pericia_se_duplicada": {"Adestramento": 2},
        }
    },
    "DRUIDA_MAGIAS": {
        "nome": "Magias (Druida)",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 1,
        "descricao": "Escolha três escolas de magia (escolha permanente). Lança magias divinas de 1º círculo (2º no 6º nível, 3º no 10º, 4º no 14º) dessas escolas. Começa com 2 magias e aprende +1 a cada nível par. Atributo-chave: Sabedoria (soma Sabedoria no total de PM).",
        "efeitos": {"habilita_magia": {"tipo": "Divina", "atributo": "sab", "escolas_restritas": 3}}
    },
    "DRUIDA_CAMINHO_ERMOS": {
        "nome": "Caminho dos Ermos",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 2,
        "descricao": "Em terrenos naturais, atravessa terrenos difíceis sem reduzir deslocamento e a CD para rastreá-lo aumenta em +10.",
        "efeitos": {"imunidade_terreno_dificil_natural": True, "cd_rastrear_natural_bonus": 10}
    },
    "DRUIDA_FORCA_NATUREZA": {
        "nome": "Força da Natureza",
        "tipo": "Habilidade de Classe",
        "classe": "Druida",
        "nivel": 20,
        "descricao": "Diminui o custo de todas as suas magias em -2 PM e aumenta a CD delas em +2. Os bônus dobram (-4 PM e +4 na CD) em terrenos naturais.",
        "efeitos": {
            "forca_da_natureza": True,
            "reducao_pm_magias": 2,
            "cd_magias_bonus": 2,
            "dobra_em_terreno_natural": True,
        }
    },
    # --- PODERES DE DRUIDA (22 poderes oficiais, T20 JdA p. 61-63) ---
    "DRUIDA_ASPECTO_INVERNO": {
        "nome": "Aspecto do Inverno",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende uma magia de convocação ou evocação (arcana ou divina). Recebe RD frio 5 e suas magias de dano de frio causam +1 de dano por dado.",
        "efeitos": {
            "magia_adicional_escolas": ["Convocação", "Evocação"],
            "resistencia_rd": {"frio": 5},
            "bonus_dano_dado_frio": 1,
        }
    },
    "DRUIDA_ASPECTO_OUTONO": {
        "nome": "Aspecto do Outono",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende uma magia de necromancia (arcana ou divina). Pode gastar 1 PM para impor -2 nos testes de resistência de todos os inimigos em alcance curto até o início do próximo turno.",
        "efeitos": {
            "magia_adicional_escola": "Necromancia",
            "acao_ativavel": {"custo_pm": 1, "alcance": "curto", "penalidade_resistencias": -2},
        }
    },
    "DRUIDA_ASPECTO_PRIMAVERA": {
        "nome": "Aspecto da Primavera",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende uma magia de encantamento ou ilusão (arcana ou divina). Escolha um número de magias igual ao seu Carisma (mínimo 1); o custo delas é reduzido em -1 PM.",
        "efeitos": {
            "magia_adicional_escolas": ["Encantamento", "Ilusão"],
            "reducao_pm_magias_escolhidas": {"qtd_atributo": "car", "minimo": 1, "valor": 1},
        }
    },
    "DRUIDA_ASPECTO_VERAO": {
        "nome": "Aspecto do Verão",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende uma magia de transmutação (arcana ou divina). Pode gastar 1 PM para cobrir uma arma com chamas até o fim da cena (+1d6 fogo; ao acertar em combate ganha 1 PM temporário, máx por cena = nível).",
        "efeitos": {
            "magia_adicional_escola": "Transmutação",
            "acao_ativavel": {"custo_pm": 1, "duracao": "cena", "dano_fogo": "1d6", "pm_temp_acerto": 1},
        }
    },
    "DRUIDA_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "DRUIDA_COMPANHEIRO_ANIMAL": {
        "nome": "Companheiro Animal",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Car 1", "Treinado em Adestramento"],
        "descricao": "Recebe um companheiro animal (parceiro iniciante; veterano no 7º nível, mestre no 15º). Pode escolher quantas vezes quiser para companheiros diferentes (sujeito ao limite de parceiros).",
        "efeitos": {"parceiro_adicional": 1, "multipla_escolha": True}
    },
    "DRUIDA_COMPANHEIRO_APRIMORADO": {
        "nome": "Companheiro Animal Aprimorado",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Companheiro Animal", "Nível 6"],
        "descricao": "Um de seus companheiros animais recebe um segundo tipo, ganhando os bônus de seu nível.",
        "efeitos": {"companheiro_segundo_tipo": True}
    },
    "DRUIDA_COMPANHEIRO_LENDARIO": {
        "nome": "Companheiro Animal Lendário",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Companheiro Animal", "Nível 18"],
        "descricao": "Um de seus companheiros animais dobra os bônus concedidos de seu tipo original.",
        "efeitos": {"companheiro_dobra_bonus": True}
    },
    "DRUIDA_COMPANHEIRO_MAGICO": {
        "nome": "Companheiro Animal Mágico",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Companheiro Animal", "Nível 8"],
        "descricao": "Um de seus companheiros animais recebe um segundo tipo diferente entre adepto, destruidor, magivocador ou médico.",
        "efeitos": {"companheiro_tipo_magico": ["adepto", "destruidor", "magivocador", "médico"]}
    },
    "DRUIDA_CORACAO_SELVA": {
        "nome": "Coração da Selva",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "A CD para resistir a seus efeitos de veneno aumenta em +2 e estes efeitos causam +1 de perda de vida por dado.",
        "efeitos": {"veneno_cd_bonus": 2, "veneno_dano_por_dado": 1}
    },
    "DRUIDA_ESPIRITO_EQUINOCIOS": {
        "nome": "Espírito dos Equinócios",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Aspecto da Primavera", "Aspecto do Outono", "Nível 10"],
        "descricao": "4 PM: até o final da cena, pode rolar novamente qualquer resultado 1 nos dados.",
        "efeitos": {"acao_ativavel": {"custo_pm": 4, "duracao": "cena", "efeito": "rerrolar_1"}}
    },
    "DRUIDA_ESPIRITO_SOLSTICIOS": {
        "nome": "Espírito dos Solstícios",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Aspecto do Inverno", "Aspecto do Verão", "Nível 10"],
        "descricao": "Ao lançar magia, pode gastar +4 PM para maximizar os efeitos numéricos variáveis dela.",
        "efeitos": {"acao_ativavel": {"custo_pm_extra": 4, "efeito": "maximizar_magia"}}
    },
    "DRUIDA_FORCA_PENHASCOS": {
        "nome": "Força dos Penhascos",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Nível 4"],
        "descricao": "Recebe +2 em Fortitude. Em contato com solo ou pedra, ao sofrer dano pode gastar até Sab PM para reduzir esse dano em 10 por PM.",
        "efeitos": {
            "bonus_pericia": {"Fortitude": 2},
            "acao_ativavel": {"custo_pm": "variavel", "limite_pm": "sabedoria", "rd_por_pm": 10},
        }
    },
    "DRUIDA_FORMA_PRIMAL": {
        "nome": "Forma Primal",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Nível 18"],
        "descricao": "Ao usar Forma Selvagem, pode se transformar em uma fera primal recebendo os benefícios de dois tipos de animais (bônus iguais não acumulam).",
        "efeitos": {"forma_primal": True}
    },
    "DRUIDA_FORMA_SELVAGEM": {
        "nome": "Forma Selvagem",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Ação completa, 3 PM: transforma-se em criatura selvagem (Ágil, Feroz, Resistente, Sorrateira ou Veloz). Não pode falar, empunhar itens ou lançar magias; mantém itens vestidos; +10 em Enganação para se passar por animal comum.",
        "efeitos": {
            "forma_selvagem": True,
            "acao_ativavel": {"acao": "completa", "custo_pm": 3},
            "formas": ["Ágil", "Feroz", "Resistente", "Sorrateira", "Veloz"],
        }
    },
    "DRUIDA_FORMA_SELVAGEM_APRIMORADA": {
        "nome": "Forma Selvagem Aprimorada",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Forma Selvagem", "Nível 6"],
        "descricao": "Ao usar Forma Selvagem, pode gastar 6 PM ao todo para assumir uma forma aprimorada.",
        "efeitos": {"forma_selvagem_aprimorada": True, "custo_pm_total": 6}
    },
    "DRUIDA_FORMA_SELVAGEM_SUPERIOR": {
        "nome": "Forma Selvagem Superior",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Forma Selvagem Aprimorada", "Nível 12"],
        "descricao": "Ao usar Forma Selvagem, pode gastar 10 PM ao todo para assumir uma forma superior.",
        "efeitos": {"forma_selvagem_superior": True, "custo_pm_total": 10}
    },
    "DRUIDA_LIBERDADE_PRADARIA": {
        "nome": "Liberdade da Pradaria",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Recebe +2 em Reflexos. Ao ar livre, pode gastar 1 PM ao lançar magia para aumentar o alcance em um passo (toque -> curto -> médio -> longo).",
        "efeitos": {
            "bonus_pericia": {"Reflexos": 2},
            "acao_ativavel": {"custo_pm": 1, "condicao": "ar_livre", "efeito": "aumentar_alcance_magia_1_passo"},
        }
    },
    "DRUIDA_MAGIA_NATURAL": {
        "nome": "Magia Natural",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "requisitos": ["Forma Selvagem"],
        "descricao": "Em forma selvagem, pode lançar magias e empunhar catalisadores e esotéricos.",
        "efeitos": {"magia_em_forma_selvagem": True}
    },
    "DRUIDA_PRESAS_AFIADAS": {
        "nome": "Presas Afiadas",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "A margem de ameaça de suas armas naturais aumenta em +2.",
        "efeitos": {"armas_naturais_margem_ameaca": 2}
    },
    "DRUIDA_SEGREDOS_NATUREZA": {
        "nome": "Segredos da Natureza",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Aprende duas magias de qualquer círculo que possa lançar, das escolas conhecidas (arcanas ou divinas). Pode escolher este poder quantas vezes quiser.",
        "efeitos": {"magias_adicionais": 2, "multipla_escolha": True}
    },
    "DRUIDA_TRANQUILIDADE_LAGOS": {
        "nome": "Tranquilidade dos Lagos",
        "tipo": "Poder de Druida",
        "classe": "Druida",
        "descricao": "Recebe +2 em Vontade. Portando recipiente com água, 1x/rodada pode pagar 1 PM para refazer um teste de resistência.",
        "efeitos": {
            "bonus_pericia": {"Vontade": 2},
            "acao_ativavel": {"custo_pm": 1, "frequencia": "1x_por_rodada", "efeito": "refazer_resistencia"},
        }
    },

    # ==========================================================================
    # GUERREIRO (T20 JdA, p. 64-66)
    # ==========================================================================
    "GUERREIRO_ATAQUE_ESPECIAL": {
        "nome": "Ataque Especial",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 1,
        "descricao": "Ao fazer um ataque, gasta 1 PM para receber +4 no teste de ataque ou na rolagem de dano (+4/+1 PM a cada 4 níveis: +8 no 5º, +12 no 9º, +16 no 13º, +20 no 17º). Pode dividir os bônus igualmente.",
        "efeitos": {
            "acao_ativavel": {
                "custo_pm": 1,
                "bonus_ataque_ou_dano": 4,
                "escala_nivel": {"cada": 4, "bonus": 4, "custo_pm_extra": 1},
            }
        }
    },
    "GUERREIRO_DURAO": {
        "nome": "Durão",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 3,
        "descricao": "Sempre que sofre dano, pode gastar 3 PM para reduzir esse dano à metade.",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 3, "efeito": "reduzir_dano_metade"},
            "durao": True,
        }
    },
    "GUERREIRO_ATAQUE_EXTRA": {
        "nome": "Ataque Extra",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 6,
        "descricao": "Quando usa a ação agredir, pode gastar 2 PM para realizar um ataque adicional (uma vez por rodada).",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "frequencia": "1x_por_rodada", "efeito": "ataque_adicional"},
            "ataque_extra": True,
        }
    },
    "GUERREIRO_CAMPEAO": {
        "nome": "Campeão",
        "tipo": "Habilidade de Classe",
        "classe": "Guerreiro",
        "nivel": 20,
        "descricao": "O dano de todos os seus ataques aumenta em um passo. Além disso, sempre que acerta um Ataque Especial ou Golpe Pessoal, recupera metade dos PM gastos nele.",
        "efeitos": {"campeao": True, "passo_dano_global": 1, "recupera_metade_pm_especial": True}
    },
    # --- PODERES DE GUERREIRO (19 poderes oficiais, T20 JdA p. 65-66) ---
    "GUERREIRO_AMBIDESTRIA": {
        "nome": "Ambidestria",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Des 2"],
        "descricao": "Empunhando duas armas (ao menos uma leve) na ação agredir, pode fazer dois ataques (um com cada arma), sofrendo -2 em todos os testes de ataque até seu próximo turno.",
        "efeitos": {"ambidestria": True, "penalidade_ataque": -2}
    },
    "GUERREIRO_ARQUEIRO": {
        "nome": "Arqueiro",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Sab 1"],
        "descricao": "Usando arma de ataque à distância, soma sua Sabedoria em rolagens de dano (limitado pelo seu nível).",
        "efeitos": {"dano_distancia_soma_atributo": {"atributo": "sab", "limite_por_nivel": True}}
    },
    "GUERREIRO_ATAQUE_REFLEXO": {
        "nome": "Ataque Reflexo",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Des 1"],
        "descricao": "Se um alvo em alcance corpo a corpo ficar desprevenido ou sair voluntariamente do alcance, pode gastar 1 PM para fazer um ataque corpo a corpo contra ele (1x por alvo por rodada).",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 1, "frequencia": "1x_por_alvo_rodada", "efeito": "ataque_oportunidade"}
        }
    },
    "GUERREIRO_AUMENTO_ATRIBUTO": {
        "nome": "Aumento de Atributo",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Recebe +1 em um atributo. Pode escolher este poder várias vezes, mas apenas uma vez por patamar para um mesmo atributo.",
        "efeitos": {"atributo_bonus_escolha": 1}
    },
    "GUERREIRO_BATER_CORRER": {
        "nome": "Bater e Correr",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Quando faz investida, pode continuar se movendo após o ataque até o limite de deslocamento. 2 PM: investida sobre terreno difícil e sem penalidade de Defesa.",
        "efeitos": {"bater_e_correr": True, "acao_ativavel": {"custo_pm": 2, "efeito": "investida_sem_penalidade"}}
    },
    "GUERREIRO_DESTRUIDOR": {
        "nome": "Destruidor",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["For 1"],
        "descricao": "Quando causa dano com arma corpo a corpo de duas mãos, pode rolar novamente qualquer resultado 1 ou 2 na rolagem de dano da arma.",
        "efeitos": {"destruidor_rerrolar_1_2": True}
    },
    "GUERREIRO_ESGRIMISTA": {
        "nome": "Esgrimista",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Int 1"],
        "descricao": "Quando usa arma corpo a corpo leve ou ágil, soma sua Inteligência em rolagens de dano (limitado pelo seu nível).",
        "efeitos": {
            "dano_soma_atributo_extra": {"atributo": "int", "tipo_arma": ["leve", "ágil"], "limite_por_nivel": True}
        }
    },
    "GUERREIRO_ESPECIALIZACAO_ARMA": {
        "nome": "Especialização em Arma",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Escolha uma arma. Recebe +2 em rolagens de dano com essa arma. Pode escolher outras vezes para armas diferentes.",
        "efeitos": {"especializacao_arma_dano": 2, "multipla_escolha": True}
    },
    "GUERREIRO_ESPECIALIZACAO_ARMADURA": {
        "nome": "Especialização em Armadura",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Nível 12"],
        "descricao": "Recebe redução de dano 5 se estiver usando uma armadura pesada.",
        "efeitos": {"rd_armadura_pesada": 5}
    },
    "GUERREIRO_GOLPE_RASPAO": {
        "nome": "Golpe de Raspão",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Uma vez por rodada, quando erra um ataque, pode gastar 2 PM para causar metade do dano que causaria (ignorando efeitos de acerto).",
        "efeitos": {
            "acao_ativavel": {"custo_pm": 2, "frequencia": "1x_por_rodada", "efeito": "metade_dano_ao_errar"},
            "golpe_de_raspao": True,
        }
    },
    "GUERREIRO_GOLPE_DEMOLIDOR": {
        "nome": "Golpe Demolidor",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Quando usa manobra quebrar ou ataca objeto, pode gastar 2 PM para ignorar a redução de dano dele.",
        "efeitos": {"acao_ativavel": {"custo_pm": 2, "efeito": "ignorar_rd_objeto"}}
    },
    "GUERREIRO_GOLPE_PESSOAL": {
        "nome": "Golpe Pessoal",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Nível 5"],
        "descricao": "Constrói uma técnica única com arma específica combinando efeitos (mínimo 1 PM): Amplo (+3), Atordoante (+2), Brutal (+1), Conjurador (Custo+1), Destruidor (+2), Distante (+1), Elemental (+2), Impactante (+1), Letal (+2), Penetrante (+1), Preciso (+1), Qualquer Arma (+1), Ricocheteante (+1), Teleguiado (+1), Lento (-2), Perto da Morte (-2), Sacrifício (-2). Pode escolher várias vezes.",
        "efeitos": {
            "golpe_pessoal_slot": 1,
            "multipla_escolha": True,
            "efeitos_disponiveis": {
                "Amplo": 3, "Atordoante": 2, "Brutal": 1, "Conjurador": "custo+1",
                "Destruidor": 2, "Distante": 1, "Elemental": 2, "Impactante": 1,
                "Letal": 2, "Penetrante": 1, "Preciso": 1, "Qualquer Arma": 1,
                "Ricocheteante": 1, "Teleguiado": 1, "Lento": -2,
                "Perto da Morte": -2, "Sacrifício": -2,
            },
        }
    },
    "GUERREIRO_IMPETO": {
        "nome": "Ímpeto",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Pode gastar 1 PM para aumentar seu deslocamento em +6m por uma rodada.",
        "efeitos": {"acao_ativavel": {"custo_pm": 1, "deslocamento_bonus": 6, "duracao": "1 rodada"}}
    },
    "GUERREIRO_MESTRE_ARMA": {
        "nome": "Mestre em Arma",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Especialização em Arma", "Nível 12"],
        "descricao": "Escolha uma arma com Especialização em Arma: dano aumenta em um passo e pode gastar 2 PM para rolar novamente um teste de ataque com ela.",
        "efeitos": {"mestre_arma_passo_dano": 1, "custo_rerrolar_ataque": 2}
    },
    "GUERREIRO_PLANEJAMENTO_MARCIAL": {
        "nome": "Planejamento Marcial",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Treinado em Guerra", "Nível 10"],
        "descricao": "1x/dia, 1 hora e 3 PM: escolhe um poder de guerreiro ou de combate cujos pré-requisitos cumpra e recebe seus benefícios até o próximo dia.",
        "efeitos": {"acao_ativavel": {"tempo": "1 hora", "custo_pm": 3, "frequencia": "1x_por_dia"}}
    },
    "GUERREIRO_ROMPER_RESISTENCIAS": {
        "nome": "Romper Resistências",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Quando faz um Ataque Especial, pode gastar 1 PM adicional para ignorar 10 pontos de redução de dano.",
        "efeitos": {"romper_resistencias_rd": 10, "custo_pm_extra": 1}
    },
    "GUERREIRO_SOLIDEZ": {
        "nome": "Solidez",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Se estiver usando um escudo, aplica o bônus na Defesa recebido pelo escudo em testes de resistência.",
        "efeitos": {"solidez_escudo_resistencias": True}
    },
    "GUERREIRO_TORNADO_DOR": {
        "nome": "Tornado de Dor",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "requisitos": ["Nível 6"],
        "descricao": "Ação padrão, 2 PM: ataque corpo a corpo contra cada inimigo em alcance natural; rolagem de dano com bônus cumulativo de +2 para cada acerto.",
        "efeitos": {"acao_ativavel": {"acao": "padrão", "custo_pm": 2, "bonus_dano_por_acerto": 2}}
    },
    "GUERREIRO_VALENTAO": {
        "nome": "Valentão",
        "tipo": "Poder de Guerreiro",
        "classe": "Guerreiro",
        "descricao": "Recebe +2 em testes de ataque e rolagens de dano contra oponentes caídos, desprevenidos, flanqueados ou indefesos.",
        "efeitos": {"valentao_bonus": 2}
    },

    # ==========================================================================
    # INVENTOR
    # ==========================================================================
    "INVENTOR_ENGENHOSIDADE": {
        "nome": "Engenhosidade",
        "tipo": "Habilidade de Classe",
        "classe": "Inventor",
        "nivel": 1,
        "descricao": "2 PM: Soma Inteligência em teste de perícia (exceto ataque). ",
        "efeitos": {
            "habilidade_ativavel": {
                "custo": 2,
                "acao": "Livre",
                "gatilho": "Teste de Perícia",
                "efeito": "Soma Inteligência no teste atual.",
                "duracao": "Instantâneo",
                "nome_acumulo": "Engenhosidade",
                "reducao_se_acumular": 1,
                "modificadores": [
                    {"atributo": "teste_pericia", "valor_dinamico": "inteligencia", "tipo_bonus": "engenhosidade"}
                ]
            }
        }
    },
    "INVENTOR_PROTOTIPO": {
        "nome": "Protótipo",
        "tipo": "Habilidade de Classe",
        "classe": "Inventor",
        "nivel": 1,
        "descricao": "Começa com item superior ou alquímicos (T$ 500). ",
        "efeitos": {}
    },
    # --- PODERES DE INVENTOR ---
    "INVENTOR_AGITE_ANTES": {
        "nome": "Agite Antes de Usar",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Ofício (alquimista)"],
        "descricao": "Gaste PM para aumentar dano de alquímicos (+1d/PM). ",
        "efeitos": {}
    },
    "INVENTOR_ALQUIMISTA_INICIADO": {
        "nome": "Alquimista Iniciado",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Int 1", "Sab 1", "Treinado em Ofício (alquimista)"],
        "descricao": "Recebe livro de fórmulas, faz poções (1º e 2º círculo). ",
        "efeitos": {"fabricar_pocao": True}
    },
    "INVENTOR_ARMEIRO": {
        "nome": "Armeiro",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Luta", "Treinado em Ofício (armeiro)"],
        "descricao": "Proficiência armas marciais corpo a corpo. Usa Int no ataque/dano. ",
        "efeitos": {"proficiencia_adicional": ["marciais"], "ataque_atributo_troca": "int"}
    },
    "INVENTOR_BALISTICA": {
        "nome": "Balística",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Treinado em Pontaria", "Treinado em Ofício (armeiro)"],
        "descricao": "Proficiência armas marciais distância/fogo. Usa Int no ataque. ",
        "efeitos": {"proficiencia_adicional": ["marciais distância", "fogo"], "ataque_atributo_troca": "int"}
    },
    "INVENTOR_ENGENHOQUEIRO": {
        "nome": "Engenhoqueiro",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "requisitos": ["Int 3", "Treinado em Ofício (engenhoqueiro)"],
        "descricao": "Pode fabricar engenhocas que simulam magias. ",
        "efeitos": {"fabricar_engenhoca": True}
    },
    "INVENTOR_MAESTRIA_PERICIA": {
        "nome": "Maestria em Perícia",
        "tipo": "Poder de Inventor",
        "classe": "Inventor",
        "descricao": "Escolha perícias igual Int. Pode gastar 1 PM para escolher 10 nelas. ",
        "efeitos": {"maestria_escolhas": "int"}
    },

    # ==========================================================================
    # LADINO
    # ==========================================================================
    "LADINO_ATAQUE_FURTIVO": {
        "nome": "Ataque Furtivo",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 1,
        "descricao": "+1d6 dano em desprevenidos/flanqueados (1/rodada). Aumenta a cada 2 níveis. ",
        "efeitos": {"dano_furtivo_base": "1d6"}
    },
    "LADINO_ESPECIALISTA": {
        "nome": "Especialista",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 1,
        "descricao": "1 PM: Dobra bônus de treino em perícias escolhidas (Qtd = Int). ",
        "efeitos": {"especialista_slots": "int"}
    },
    "LADINO_EVASAO": {
        "nome": "Evasão",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 2,
        "descricao": "Não sofre dano se passar em Reflexos contra área. ",
        "efeitos": {"evasao": True}
    },
    "LADINO_ESQUIVA_SOBRENATURAL": {
        "nome": "Esquiva Sobrenatural",
        "tipo": "Habilidade de Classe",
        "classe": "Ladino",
        "nivel": 4,
        "descricao": "Nunca fica surpreendido. ",
        "efeitos": {"imunidade": ["surpreendido"]}
    },
    # --- PODERES DE LADINO ---
    "LADINO_ASSASSINAR": {
        "nome": "Assassinar",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Nível 5"],
        "descricao": "3 PM: Analisa alvo. Dobra dados de ataque furtivo. ",
        "efeitos": {}
    },
    "LADINO_EMBOSCAR": {
        "nome": "Emboscar",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "2 PM: Ação padrão extra na primeira rodada. ",
        "efeitos": {}
    },
    "LADINO_MENTE_CRIMINOSA": {
        "nome": "Mente Criminosa",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Int 1"],
        "descricao": "Soma Inteligência em Ladinagem e Furtividade. ",
        "efeitos": {"pericia_soma_atributo": {"Ladinagem": "int", "Furtividade": "int"}}
    },
    "LADINO_ROLAMENTO_DEFENSIVO": {
        "nome": "Rolamento Defensivo",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Reflexos"],
        "descricao": "Reação (2 PM): Reduz dano à metade. Fica caído. ",
        "efeitos": {}
    },
    "LADINO_SOMBRA": {
        "nome": "Sombra",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Treinado em Furtividade"],
        "descricao": "+2 Furtividade. Sem penalidade por mover. ",
        "efeitos": {"bonus_pericia": {"Furtividade": 2}}
    },
    "LADINO_TRUQUE_MAGICO": {
        "nome": "Truque Mágico",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Int 1"],
        "descricao": "Aprende uma magia arcana de 1º círculo (Int). ",
        "efeitos": {"magia_adicional_arcana": 1}
    },
    "LADINO_VELOCIDADE_LADINA": {
        "nome": "Velocidade Ladina",
        "tipo": "Poder de Ladino",
        "classe": "Ladino",
        "requisitos": ["Des 2", "Treinado em Iniciativa"],
        "descricao": "2 PM: Ação de movimento extra. ",
        "efeitos": {}
    },

    # ==========================================================================
    # LUTADOR
    # ==========================================================================
    "LUTADOR_BRIGA": {
        "nome": "Briga",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 1,
        "descricao": "Dano desarmado 1d6. Aumenta com nível. ",
        "efeitos": {"dano_desarmado_base": "1d6"}
    },
    "LUTADOR_GOLPE_RELAMPAGO": {
        "nome": "Golpe Relâmpago",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 1,
        "descricao": "1 PM: Ataque desarmado extra ao agredir. ",
        "efeitos": {}
    },
    "LUTADOR_CASCA_GROSSA": {
        "nome": "Casca Grossa",
        "tipo": "Habilidade de Classe",
        "classe": "Lutador",
        "nivel": 3,
        "descricao": "Soma Constituição na Defesa (se sem armadura pesada). ",
        "efeitos": {"defesa_soma_atributo": "con"}
    },
    # --- PODERES DE LUTADOR ---
    "LUTADOR_ATE_ACERTAR": {
        "nome": "Até Acertar",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "Se errar, recebe +2 cumulativo no próximo ataque. ",
        "efeitos": {}
    },
    "LUTADOR_BRACOS_CALEJADOS": {
        "nome": "Braços Calejados",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "Soma Força na Defesa (se sem armadura). ",
        "efeitos": {"defesa_soma_atributo": "for"}
    },
    "LUTADOR_GOLPE_BAIXO": {
        "nome": "Golpe Baixo",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "2 PM: Acerto exige Fortitude ou atordoa alvo. ",
        "efeitos": {}
    },
    "LUTADOR_LINGUA_BECOS": {
        "nome": "Língua dos Becos",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "requisitos": ["For 1", "Treinado em Intimidação"],
        "descricao": "1 PM: Usa Força em vez de Carisma em perícia social. ",
        "efeitos": {}
    },
    "LUTADOR_TROCACAO": {
        "nome": "Trocação",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "requisitos": ["Nível 6"],
        "descricao": "Ao acertar, paga PM (1, 2, 3...) para atacar de novo. ",
        "efeitos": {}
    },
    "LUTADOR_VOADORA": {
        "nome": "Voadora",
        "tipo": "Poder de Lutador",
        "classe": "Lutador",
        "descricao": "2 PM: Investida causa +1d6 dano a cada 3m deslocado. ",
        "efeitos": {}
    },

    # ==========================================================================
    # NOBRE
    # ==========================================================================
    "NOBRE_AUTOCONFIANCA": {
        "nome": "Autoconfiança",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Usa Carisma na Defesa em vez de Destreza. ",
        "efeitos": {"defesa_atributo_troca": "car"}
    },
    "NOBRE_ESPOLIO": {
        "nome": "Espólio",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Recebe item de até T$ 2.000. ",
        "efeitos": {"item_inicial_extra_valor": 2000}
    },
    "NOBRE_ORGULHO": {
        "nome": "Orgulho",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 1,
        "descricao": "Gaste PM para ganhar +2 em perícia por PM. ",
        "efeitos": {}
    },
    "NOBRE_RIQUEZA": {
        "nome": "Riqueza",
        "tipo": "Habilidade de Classe",
        "classe": "Nobre",
        "nivel": 3,
        "descricao": "Recebe dinheiro (Teste Carisma x Nível) uma vez por aventura. ",
        "efeitos": {}
    },
    # --- PODERES DE NOBRE ---
    "NOBRE_ARMADURA_BRILHANTE": {
        "nome": "Armadura Brilhante",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Nível 8"],
        "descricao": "Soma Carisma na Defesa com armadura pesada (substitui Des). ",
        "efeitos": {}
    },
    "NOBRE_GRITO_TIRANICO": {
        "nome": "Grito Tirânico",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Nível 8"],
        "descricao": "Palavras Afiadas vira ação completa, d8 dano e atinge área. ",
        "efeitos": {}
    },
    "NOBRE_INSPIRAR_CONFIANCA": {
        "nome": "Inspirar Confiança",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "descricao": "2 PM: Aliado rerola teste recém realizado. ",
        "efeitos": {}
    },
    "NOBRE_INSPIRAR_GLORIA": {
        "nome": "Inspirar Glória",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "requisitos": ["Inspirar Confiança", "Nível 8"],
        "descricao": "5 PM: Aliado ganha ação padrão extra. ",
        "efeitos": {}
    },
    "NOBRE_LINGUA_PRATA": {
        "nome": "Língua de Prata",
        "tipo": "Poder de Nobre",
        "classe": "Nobre",
        "descricao": "2 PM: Soma metade do nível em perícia de Carisma. ",
        "efeitos": {}
    },

    # ==========================================================================
    # PALADINO
    # ==========================================================================
    "PALADINO_ABENCOADO": {
        "nome": "Abençoado",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "Soma Carisma aos PM. Devoto ganha 2 poderes concedidos. ",
        "efeitos": {"pm_soma_atributo": "car", "poderes_concedidos_bonus": 1}
    },
    "PALADINO_CODIGO_HEROI": {
        "nome": "Código do Herói",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "Deve manter palavra, proteger inocentes, não mentir/roubar. Violação perde PM. ",
        "efeitos": {}
    },
    "PALADINO_GOLPE_DIVINO": {
        "nome": "Golpe Divino",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 1,
        "descricao": "2 PM: Soma Car no ataque e +1d8 dano. Aumenta com nível. ",
        "efeitos": {}
    },
    "PALADINO_CURA_MAOS": {
        "nome": "Cura pelas Mãos",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 2,
        "descricao": "Movimento (1 PM): Cura 1d8+1 PV (toque). Aumenta com nível. ",
        "efeitos": {}
    },
    "PALADINO_AURA_SAGRADA": {
        "nome": "Aura Sagrada",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 3,
        "descricao": "1 PM (Sustentada): +Carisma em testes de resistência para aliados em 9m. ",
        "efeitos": {}
    },
    "PALADINO_BENCAO_JUSTICA": {
        "nome": "Bênção da Justiça",
        "tipo": "Habilidade de Classe",
        "classe": "Paladino",
        "nivel": 5,
        "descricao": "Escolha: Égide Sagrada (Bônus Defesa) ou Montaria Sagrada. ",
        "efeitos": {"escolha_bencao": ["Égide Sagrada", "Montaria Sagrada"]}
    },
    # --- PODERES DE PALADINO ---
    "PALADINO_ARMA_SAGRADA": {
        "nome": "Arma Sagrada",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "Golpe Divino com arma da divindade usa d12. ",
        "efeitos": {}
    },
    "PALADINO_AURA_CURA": {
        "nome": "Aura de Cura",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "requisitos": ["Nível 6"],
        "descricao": "Aura cura 5 + Carisma no início do turno. ",
        "efeitos": {}
    },
    "PALADINO_AURA_PODEROSA": {
        "nome": "Aura Poderosa",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "requisitos": ["Nível 6"],
        "descricao": "Raio da aura aumenta para 30m. ",
        "efeitos": {}
    },
    "PALADINO_JULGAMENTO_VINDICACAO": {
        "nome": "Julgamento: Vindicação",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "2 PM: Marca inimigo. +1 ataque / +1d8 dano contra ele. ",
        "efeitos": {}
    },
    "PALADINO_VIRTUDE_TEMPERANCA": {
        "nome": "Virtude: Temperança",
        "tipo": "Poder de Paladino",
        "classe": "Paladino",
        "descricao": "Itens consumíveis (poções/comida) rendem o dobro. +PM passivo. ",
        "efeitos": {"pm_bonus_virtude": True}
    }
}
