from src.models import TamanhoEnum

# --- DADOS DE RAÇAS (T20 Jogo do Ano) ---
DADOS_RACAS = {
    # --- RAÇAS BÁSICAS ---
    "Humano": {
        "fonte": "T20 JdA",
        "attrs": {},  # +1 em três atributos diferentes (escolha)
        "escolhas": 3,
        "bonus_por_escolha": 1,  # T20 JdA: Humano = +1 em três atributos diferentes
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Versatil_Humano"]
    },
    "Anão": {
        "fonte": "T20 JdA",
        "attrs": {"con": 2, "sab": 1, "des": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 6,
        "habilidades": ["Conhecimento_Rochas_Anao", "Devagar_Sempre_Anao", "Duro_Pedra_Anao", "Tradicao_Heredrimm_Anao"]
    },
    "Dahllan": {
        "fonte": "T20 JdA",
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Amiga_Plantas_Dahllan", "Armadura_Allihanna_Dahllan", "Empatia_Selvagem_Dahllan"]
    },
    "Elfo": {
        "fonte": "T20 JdA",
        "attrs": {"int": 2, "des": 1, "con": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "habilidades": ["Graca_Glorienn_Elfo", "Sangue_Magico_Elfo", "Sentidos_Elficos_Elfo"]
    },
    "Goblin": {
        "fonte": "T20 JdA",
        "attrs": {"des": 2, "int": 1, "car": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "deslocamento": 9,
        "habilidades": ["Engenhoso_Goblin", "Espelunqueiro_Goblin", "Peste_Esguia_Goblin", "Rato_Ruas_Goblin"]
    },
    "Lefou": {
        "fonte": "T20 JdA",
        # +1 em três atributos diferentes (exceto Carisma)
        "attrs": {"car": -1},
        "escolhas": 3,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Cria_Tormenta_Lefou", "Deformidade_Lefou"]
    },
    "Minotauro": {
        "fonte": "T20 JdA",
        "attrs": {"for": 2, "con": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Chifres_Minotauro", "Couro_Rigido_Minotauro", "Faro_Minotauro", "Medo_Altura_Minotauro"]
    },
    "Qareen": {
        "fonte": "T20 JdA",
        "attrs": {"car": 2, "int": 1, "sab": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Desejos_Qareen", "Resistencia_Elemental_Qareen", "Tatuagem_Mist_Qareen"]
    },
    "Golem": {
        "fonte": "T20 JdA",
        "attrs": {"for": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 6,
        "habilidades": ["Chassi_Golem", "Criatura_Artificial_Golem", "Fonte_Elemental_Golem", "Proposito_Criacao_Golem"]
    },
    "Hynne": {
        "fonte": "T20 JdA",
        "attrs": {"des": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "deslocamento": 6,
        "habilidades": ["Arremessador_Hynne", "Pequeno_Rechonchudo_Hynne", "Sorte_Salvadora_Hynne"]
    },
    "Kliren": {
        "fonte": "T20 JdA",
        "attrs": {"int": 2, "car": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Hibrido_Kliren", "Engenhosidade_Kliren", "Ossos_Frageis_Kliren", "Vanguardista_Kliren"]
    },
    "Medusa": {
        "fonte": "T20 JdA",
        "attrs": {"des": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Cria_Megalokk_Medusa", "Natureza_Venenosa_Medusa", "Olhar_Atordoante_Medusa"]
    },
    "Osteon": {
        "fonte": "T20 JdA",
        "attrs": {"con": -1},  # +1 em três atributos (exceto Con)
        "escolhas": 3,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Armadura_Ossea_Osteon", "Memoria_Postuma_Osteon", "Natureza_Esqueletica_Osteon", "Preco_Nao_Vida_Osteon"]
    },
    "Sereia/Tritão": {
        "fonte": "T20 JdA",
        "attrs": {},  # +1 em três atributos diferentes
        "escolhas": 3,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,  # +12m natação (regra especial)
        "habilidades": ["Cancao_Mares_Sereia", "Mestre_Tridente_Sereia", "Transf_Anfibia_Sereia"]
    },
    "Sílfide": {
        "fonte": "T20 JdA",
        "attrs": {"car": 2, "des": 1, "for": -2},
        "tamanho": TamanhoEnum.MINUSCULO,
        "deslocamento": 9,  # Voo
        "habilidades": ["Asas_Borboleta_Silfide", "Esp_Natureza_Silfide", "Magia_Fadas_Silfide"]
    },
    "Suraggel (Aggelus)": {
        "fonte": "T20 JdA",
        "attrs": {"sab": 2, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Heranca_Divina_Suraggel", "Luz_Sagrada_Aggelus"]
    },
    "Suraggel (Sulfure)": {
        "fonte": "T20 JdA",
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Heranca_Divina_Suraggel", "Sombras_Prof_Sulfure"]
    },
    "Trog": {
        "fonte": "T20 JdA",
        "attrs": {"con": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Mau_Cheiro_Trog", "Mordida_Trog", "Reptiliano_Trog", "Sangue_Frio_Trog"]
    },

    # -- Heróis de Arton) ---
    "Duende": {
        "attrs": {},
        "escolhas": 0,
        "tamanho": TamanhoEnum.PEQUENO, 
        "deslocamento": 9,
        "habilidades": [
            "Natureza_Duende",
            "Tamanho_Duende",       
            "Dons_Duende",          
            "Presentes_Duende",     
            "Limitacoes_Duende"     
        ]
    },
    "Eiradaan": {
        "attrs": {"sab": 2, "car": 1, "for": -1},
        "escolhas": 0,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": [
            "Essencia_Feerica_Eiradaan",
            "Magia_Instintiva_Eiradaan",
            "Sentidos_Misticos_Eiradaan",
            "Cancao_Melancolia_Eiradaan"
        ]
    },
    "Galokk": {
        "attrs": {"for": 1, "con": 1, "car": -1},
        "escolhas": 1,
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 9,
        "habilidades": ["Forca_Titas_Galokk", "Meio_Gigante_Galokk", "Infancia_Pequenos_Galokk"]
    },
    "Meio-Elfo": {
        "attrs": {"int": 1},
        "escolhas": 2,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": [
            "Ambicao_Herdada_MeioElfo",
            "Entre_Dois_Mundos_MeioElfo",
            "Sangue_Elfico_MeioElfo"
        ]
    },
    "Sátiro": {
        "attrs": {"car": 2, "des": 1, "sab": -1},
        "escolhas": 0,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12, 
        "habilidades": [
            "Festeiro_Feerico_Satiro",
            "Instrumentista_Magico_Satiro",
            "Marrada_Satiro",
            "Pernas_Caprinas_Satiro"
        ]
    },
    # ── AMEAÇAS DE ARTON (40 raças/heranças/variantes jogáveis oficiais) ──
    "Bugbear": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 2, "des": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Megalokk", "Tenebra"],
        "habilidades": ["Empunhadura_Poderosa_Bugbear", "Saborear_Pavor_Bugbear", "Sentidos_Predador_Bugbear"],
    },
    "Centauro": {
        "fonte": "Ameaças de Arton",
        "attrs": {"sab": 2, "for": 1, "int": -1},
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 12,
        "devotos": ["Allihanna", "Hippion", "Megalokk"],
        "habilidades": ["Avantajado_Centauro", "Cascos_Centauro", "Ginete_Natural_Centauro", "Medo_Altura_Ameacas"],
    },
    "Ceratops": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "for": 1, "des": -1, "int": -1},
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Arsenal", "Azgher", "Lena", "Megalokk"],
        "habilidades": ["Chifres_Ceratops", "Paquidermico_Ceratops", "Papel_Tribal_Ceratops", "Medo_Altura_Ameacas"],
    },
    "Elfo-do-Mar": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Arsenal", "Hyninn", "Megalokk", "Oceano"],
        "habilidades": ["Arsenal_Oceano_ElfoMar", "Cria_Aguas_ElfoMar", "Dependencia_Agua_ElfoMar"],
    },
    "Finntroll": {
        "fonte": "Ameaças de Arton",
        "attrs": {"int": 2, "con": 1, "for": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Corpo_Vegetal_Finntroll", "Presenca_Arcana_Finntroll", "Regeneracao_Vegetal_Finntroll", "Intolerancia_Luz_Finntroll"],
    },
    "Gnoll": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "sab": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Hyninn"],
        "habilidades": ["Faro_Ameacas", "Mordida_1d6_Perf_Ameacas", "Oportunista_Gnoll", "Rendicao_Gnoll"],
    },
    "Harpia": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "car": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "devotos": ["Hyninn", "Megalokk", "Tenebra"],
        "habilidades": ["Asas_Abutre_Harpia", "Cria_Masmorra_Harpia", "Grito_Aterrorizante_Harpia", "Pes_Rapinantes_Ameacas"],
    },
    "Hobgoblin": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "des": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Megalokk", "Tenebra"],
        "habilidades": ["Arte_Guerra_Hobgoblin", "Metalurgia_Hobgoblin", "Taticas_Guerrilha_Hobgoblin"],
    },
    "Kallyanach": {
        "fonte": "Ameaças de Arton",
        "attrs": {},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Kallyadranoch", "Megalokk", "Wynna"],
        "habilidades": ["Heranca_Draconica_Kallyanach", "Bencao_Kallyadranoch_Kallyanach"],
    },
    "Kaijin": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 2, "con": 1, "car": -2},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Lin-Wu"],
        "habilidades": ["Couraca_Rubra_Kaijin", "Cria_Tormenta_Kaijin", "Disforme_Kaijin", "Terror_Vivo_Kaijin"],
    },
    "Kappa": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "con": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Hyninn", "Lena", "Lin-Wu", "Oceano"],
        "habilidades": ["Alma_Agua_Kappa", "Carapaca_Kappa", "Cura_Aguas_Kappa", "Tigela_Dagua_Kappa"],
    },
    "Kobolds": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "for": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Kallyadranoch", "Khalmyr", "Lena", "Megalokk", "Tenebra"],
        "habilidades": ["Ajuntamento_Escamoso_Kobolds", "Praga_Monstruosa_Kobolds", "Sensibilidade_Luz_Ameacas", "Talentos_Bando_Kobolds"],
    },
    "Mashin": {
        "fonte": "Ameaças de Arton",
        "attrs": {},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Chassi_Mashin", "Maravilha_Mecanica_Mashin"],
    },
    "Meio-Orc": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 2},
        "escolhas": 1,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Adaptavel_MeioOrc", "Criatura_Profundezas_MeioOrc", "Sangue_Orc_MeioOrc"],
    },
    "Minauro": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Faro_Ameacas", "Mente_Aberta_Minauro", "Plurivalente_Minauro"],
    },
    "Moreau (Búfalo)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Chifres_1d6_Moreau_Bufalo", "Faro_Ameacas", "Marrada_Impressionante_Moreau_Bufalo"],
    },
    "Moreau (Coelho)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Patas_Ligeiras_Moreau_Coelho", "Pe_Coelho_Moreau_Coelho", "Senso_Preservacao_Moreau_Coelho"],
    },
    "Moreau (Coruja)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"sab": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Espreitador_Moreau_Coruja", "Garras_1d6_Corte_Ameacas", "Sapiencia_Moreau_Coruja"],
    },
    "Moreau (Crocodilo)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Mordida_Poderosa_Moreau_Crocodilo", "Predador_Aquatico_Moreau_Crocodilo", "Surto_Reptiliano_Moreau_Crocodilo"],
    },
    "Moreau (Gato)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"car": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Muitas_Vidas_Gato_Moreau_Gato", "Garras_1d6_Corte_Ameacas", "Sentidos_Felinos_Moreau_Gato"],
    },
    "Moreau (Hiena)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"sab": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Destemor_Moreau_Hiena", "Faro_Ameacas", "Mordida_1d6_Perf_Ameacas"],
    },
    "Moreau (Leão)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Mordida_1d8_Perf_Ameacas", "Rugido_Imponente_Moreau_Leao", "Sentidos_Realeza_Moreau_Leao"],
    },
    "Moreau (Lobo)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"car": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Faro_Ameacas", "Mordida_1d6_Perf_Ameacas", "Taticas_Matilha_Moreau_Lobo"],
    },
    "Moreau (Morcego)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Asas_Moreau_Morcego", "Criatura_Noite_Moreau_Morcego", "Ecolocalizacao_Moreau_Morcego"],
    },
    "Moreau (Raposa)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"int": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Agarra_Me_Se_Puderes_Moreau_Raposa", "Esperteza_Vulpina_Moreau_Raposa", "Faro_Ameacas"],
    },
    "Moreau (Serpente)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"int": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Arboricola_Moreau_Serpente", "Constritor_Moreau_Serpente", "Instintos_Traicoeiros_Moreau_Serpente"],
    },
    "Moreau (Urso)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 1},
        "escolhas": 2,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 9,
        "devotos": ["Todos"],
        "habilidades": ["Heranca_Moreau_Base", "Abraco_Urso_Moreau_Urso", "Faro_Ameacas", "Mordida_1d8_Perf_Ameacas"],
    },
    "Nagah (Macho)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 1, "des": 1, "con": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Hyninn", "Kallyadranoch", "Megalokk", "Sszzaas", "Tenebra", "Wynna"],
        "habilidades": ["Cauda_Nagah", "Inocencia_Dissimulada_Nagah", "Presentes_Sszzaas_Nagah", "Fraquezas_Ofidicas_Nagah"],
    },
    "Nagah (Fêmea)": {
        "fonte": "Ameaças de Arton",
        "attrs": {"int": 1, "sab": 1, "car": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Hyninn", "Kallyadranoch", "Megalokk", "Sszzaas", "Tenebra", "Wynna"],
        "habilidades": ["Cauda_Nagah", "Inocencia_Dissimulada_Nagah", "Presentes_Sszzaas_Nagah", "Fraquezas_Ofidicas_Nagah"],
    },
    "Nezumi": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.PEQUENO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Megalokk", "Tenebra"],
        "habilidades": ["Empunhadura_Poderosa_Bugbear", "Pequeno_Mas_Nao_Metade_Nezumi", "Roedor_Nezumi", "Sentidos_Murideos_Nezumi"],
    },
    "Ogro": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 3, "con": 2, "int": -1, "car": -1},
        "tamanho": TamanhoEnum.GRANDE,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Arsenal", "Megalokk", "Tenebra"],
        "habilidades": ["Quanto_Maior_Tamanho_Ogro", "Maior_Porrada_Ogro", "Camada_Ingenuidade_Ogro"],
    },
    "Orc": {
        "fonte": "Ameaças de Arton",
        "attrs": {"for": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Arsenal", "Megalokk", "Nimb", "Tenebra"],
        "habilidades": ["Feroz_Orc", "Habitante_Cavernas_Orc", "Vigor_Brutal_Orc"],
    },
    "Pteros": {
        "fonte": "Ameaças de Arton",
        "attrs": {"sab": 2, "des": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Lena", "Marah", "Wynna"],
        "habilidades": ["Ligacao_Natural_Pteros", "Maos_Rudimentares_Pteros", "Pes_Rapinantes_Ameacas", "Senhor_Ceus_Pteros", "Sentidos_Rapinantes_Pteros"],
    },
    "Soterrado": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": -1},
        "escolhas": 3,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "habilidades": ["Natureza_Esqueletica_Osteon", "Preco_Nao_Vida_Osteon", "Abraco_Gelido_Soterrado", "Esquife_Gelo_Soterrado"],
    },
    "Tabrachi": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "for": 1, "car": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Megalokk", "Nimb", "Sszzaas", "Tenebra"],
        "habilidades": ["Batraquio_Tabrachi", "Linguarudo_Tabrachi", "Saltador_Tabrachi"],
    },
    "Tengu": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "int": 1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Khalmyr", "Lin-Wu", "Tanna-Toh", "Valkaria", "Wynna"],
        "habilidades": ["Asas_Desorientadoras_Tengu", "Caminhante_Ceu_Tengu", "Espirito_Corvino_Tengu"],
    },
    "Trog Anão": {
        "fonte": "Ameaças de Arton",
        "attrs": {"con": 2, "for": 1, "des": -1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 6,
        "habilidades": ["Mau_Cheiro_Trog", "Mordida_Trog", "Quase_Anao_TrogAnao", "Sangue_Frio_Trog"],
    },
    "Velocis": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "sab": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 12,
        "devotos": ["Allihanna", "Lena", "Marah"],
        "habilidades": ["Atraves_Espinheiros_Velocis", "Sentidos_Selvagens_Ameacas", "Velocista_Planicie_Velocis"],
    },
    "Voracis": {
        "fonte": "Ameaças de Arton",
        "attrs": {"des": 2, "con": 1, "int": -1},
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Allihanna", "Arsenal", "Megalokk"],
        "habilidades": ["Garras_1d6_Corte_Ameacas", "Rainha_Selva_Voracis", "Sentidos_Selvagens_Ameacas"],
    },
    "Yidishan": {
        "fonte": "Ameaças de Arton",
        "attrs": {"car": -2},
        "escolhas": 3,
        "bonus_por_escolha": 1,
        "tamanho": TamanhoEnum.MEDIO,
        "deslocamento": 9,
        "devotos": ["Arsenal", "Megalokk", "Nimb"],
        "habilidades": ["Hibrido_Mecanico_Yidishan", "Natureza_Organica_Yidishan", "Pecas_Metalicas_Yidishan"],
    },
}
