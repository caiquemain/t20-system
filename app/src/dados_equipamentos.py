"""Catálogo de equipamentos do T20 JdA (Capítulo 3, Tabelas 3-3 e 3-5)."""

# --- TABELA 3-3: ARMAS ---
# categoria = proficiência | proposito | empunhadura | mecanica (arremesso/disparo)
DADOS_ARMAS = {
    # --- SIMPLES | CORPO A CORPO ---
    "Adaga": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Leve", "preco": 2, "dano": "1d4", "critico": "19", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": [], "arremessavel": True, "destreza_no_ataque": True},
    "Espada curta": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Leve", "preco": 10, "dano": "1d6", "critico": "19", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": []},
    "Foice": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Leve", "preco": 4, "dano": "1d6", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": []},
    "Clava": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 0, "dano": "1d6", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 1, "habilidades": []},
    "Lança": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 2, "dano": "1d6", "critico": "x2", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": [], "arremessavel": True},
    "Maça": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 12, "dano": "1d8", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 1, "habilidades": []},
    "Bordão": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 0, "dano": "1d6/1d6", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 2, "habilidades": ["dupla"]},
    "Pique": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 2, "dano": "1d8", "critico": "x2", "alcance": None, "tipo": "Perfuração", "espacos": 2, "habilidades": ["alongada"]},
    "Tacape": {"categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 0, "dano": "1d10", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 2, "habilidades": []},
    # --- SIMPLES | À DISTÂNCIA ---
    "Azagaia": {"categoria": "Simples", "proposito": "À Distância", "mecanica": "Arremesso", "empunhadura": "Uma Mão", "preco": 1, "dano": "1d6", "critico": "x2", "alcance": "Médio", "tipo": "Perfuração", "espacos": 1, "habilidades": []},
    "Besta leve": {"categoria": "Simples", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Uma Mão", "preco": 35, "dano": "1d8", "critico": "19", "alcance": "Médio", "tipo": "Perfuração", "espacos": 1, "habilidades": [], "recarga": "movimento"},
    "Funda": {"categoria": "Simples", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Uma Mão", "preco": 0, "dano": "1d4", "critico": "x2", "alcance": "Médio", "tipo": "Impacto", "espacos": 1, "habilidades": [], "for_no_dano": True, "recarga": "movimento"},
    "Arco curto": {"categoria": "Simples", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Duas Mãos", "preco": 30, "dano": "1d6", "critico": "x3", "alcance": "Médio", "tipo": "Perfuração", "espacos": 2, "habilidades": []},
    # --- MARCIAIS | CORPO A CORPO ---
    "Machadinha": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Leve", "preco": 6, "dano": "1d6", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": [], "arremessavel": True},
    "Cimitarra": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 15, "dano": "1d6", "critico": "18", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": ["ágil"]},
    "Espada longa": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 15, "dano": "1d8", "critico": "19", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": []},
    "Florete": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 20, "dano": "1d6", "critico": "18", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": ["ágil"]},
    "Machado de batalha": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 10, "dano": "1d8", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": []},
    "Mangual": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 8, "dano": "1d8", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 1, "habilidades": ["versátil"], "versatil": "+2 desarmar"},
    "Martelo de guerra": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 12, "dano": "1d8", "critico": "x3", "alcance": None, "tipo": "Impacto", "espacos": 1, "habilidades": []},
    "Picareta": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 8, "dano": "1d6", "critico": "x4", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": []},
    "Tridente": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 15, "dano": "1d8", "critico": "x2", "alcance": None, "tipo": "Perfuração", "espacos": 1, "habilidades": ["versátil"], "versatil": "+2 derrubar", "arremessavel": True},
    "Alabarda": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 10, "dano": "1d10", "critico": "x3", "alcance": None, "tipo": "Corte/Perfuração", "espacos": 2, "habilidades": ["alongada"]},
    "Alfange": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 75, "dano": "2d4", "critico": "18", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": []},
    "Gadanho": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 18, "dano": "2d4", "critico": "x4", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": []},
    "Lança montada": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 10, "dano": "1d8", "critico": "x3", "alcance": None, "tipo": "Perfuração", "espacos": 2, "habilidades": ["alongada"]},
    "Machado de guerra": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 20, "dano": "1d12", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": []},
    "Marreta": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 20, "dano": "3d4", "critico": "x2", "alcance": None, "tipo": "Impacto", "espacos": 2, "habilidades": []},
    "Montante": {"categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 50, "dano": "2d6", "critico": "19", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": []},
    "Arco longo": {"categoria": "Marcial", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Duas Mãos", "preco": 100, "dano": "1d8", "critico": "x3", "alcance": "Médio", "tipo": "Perfuração", "espacos": 2, "habilidades": [], "for_no_dano": True},
    "Besta pesada": {"categoria": "Marcial", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Duas Mãos", "preco": 50, "dano": "1d12", "critico": "19", "alcance": "Médio", "tipo": "Perfuração", "espacos": 2, "habilidades": [], "recarga": "padrão"},
    # --- EXÓTICAS ---
    "Chicote": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 2, "dano": "1d3", "critico": "x2", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": ["ágil", "versátil"], "versatil": "+2 derrubar/desarmar"},
    "Espada bastarda": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 35, "dano": "1d10/1d12", "critico": "19", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": ["adaptável"], "marcial_duas_maos": True},
    "Katana": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 100, "dano": "1d8/1d10", "critico": "19", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": ["adaptável", "ágil"], "marcial_duas_maos": True},
    "Machado anão": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão", "preco": 30, "dano": "1d10", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 1, "habilidades": [], "marcial_duas_maos": True},
    "Corrente de espinhos": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 25, "dano": "2d4/2d4", "critico": "19", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": ["ágil", "dupla", "versátil"], "versatil": "+2 derrubar/desarmar"},
    "Machado táurico": {"categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos", "preco": 50, "dano": "2d8", "critico": "x3", "alcance": None, "tipo": "Corte", "espacos": 2, "habilidades": ["desbalanceada"]},
    "Rede": {"categoria": "Exótica", "proposito": "À Distância", "mecanica": "Arremesso", "empunhadura": "Uma Mão", "preco": 20, "dano": None, "critico": "x2", "alcance": "Curto", "tipo": None, "espacos": 1, "habilidades": [], "efeito": "enredada"},
    # --- DE FOGO ---
    "Pistola": {"categoria": "Fogo", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Leve", "preco": 250, "dano": "2d6", "critico": "19/x3", "alcance": "Curto", "tipo": "Perfuração", "espacos": 1, "habilidades": [], "recarga": "padrão"},
    "Mosquete": {"categoria": "Fogo", "proposito": "À Distância", "mecanica": "Disparo", "empunhadura": "Duas Mãos", "preco": 500, "dano": "2d8", "critico": "19/x3", "alcance": "Médio", "tipo": "Perfuração", "espacos": 2, "habilidades": [], "recarga": "padrão"},
    # --- MUNIÇÕES ---
    "Virotes (20)": {"categoria": "Simples", "municao": True, "preco": 2, "dano": None, "critico": "x2", "alcance": None, "tipo": None, "espacos": 1, "habilidades": []},
    "Flechas (20)": {"categoria": "Simples", "municao": True, "preco": 1, "dano": None, "critico": "x2", "alcance": None, "tipo": None, "espacos": 1, "habilidades": []},
    "Pedras (20)": {"categoria": "Simples", "municao": True, "preco": 0.5, "dano": None, "critico": "x2", "alcance": None, "tipo": None, "espacos": 1, "habilidades": []},
    "Balas (20)": {"categoria": "Fogo", "municao": True, "preco": 20, "dano": None, "critico": "x2", "alcance": None, "tipo": None, "espacos": 1, "habilidades": []},
}

# --- TABELA 3-5: ARMADURAS & ESCUDOS ---
DADOS_ARMADURAS = {
    "Armadura acolchoada": {"tipo_armadura": "Leve", "preco": 5, "bonus_defesa": 1, "penalidade_armadura": 0, "espacos": 2, "extras": "+2 Fortitude"},
    "Armadura de couro": {"tipo_armadura": "Leve", "preco": 20, "bonus_defesa": 2, "penalidade_armadura": 0, "espacos": 2, "extras": ""},
    "Couro batido": {"tipo_armadura": "Leve", "preco": 35, "bonus_defesa": 3, "penalidade_armadura": -1, "espacos": 2, "extras": ""},
    "Gibão de peles": {"tipo_armadura": "Leve", "preco": 25, "bonus_defesa": 4, "penalidade_armadura": -3, "espacos": 2, "extras": ""},
    "Couraça": {"tipo_armadura": "Leve", "preco": 500, "bonus_defesa": 5, "penalidade_armadura": -4, "espacos": 2, "extras": ""},
    "Brunea": {"tipo_armadura": "Pesada", "preco": 50, "bonus_defesa": 5, "penalidade_armadura": -2, "espacos": 5, "extras": ""},
    "Cota de malha": {"tipo_armadura": "Pesada", "preco": 150, "bonus_defesa": 6, "penalidade_armadura": -2, "espacos": 5, "extras": ""},
    "Loriga segmentada": {"tipo_armadura": "Pesada", "preco": 250, "bonus_defesa": 7, "penalidade_armadura": -3, "espacos": 5, "extras": ""},
    "Meia armadura": {"tipo_armadura": "Pesada", "preco": 600, "bonus_defesa": 8, "penalidade_armadura": -4, "espacos": 5, "extras": ""},
    "Armadura completa": {"tipo_armadura": "Pesada", "preco": 3000, "bonus_defesa": 10, "penalidade_armadura": -5, "espacos": 5, "extras": ""},
    "Escudo leve": {"tipo_armadura": "Escudo", "preco": 5, "bonus_defesa": 1, "penalidade_armadura": -1, "espacos": 1, "extras": ""},
    "Escudo pesado": {"tipo_armadura": "Escudo", "preco": 15, "bonus_defesa": 2, "penalidade_armadura": -2, "espacos": 2, "extras": ""},
}


# --- TABELA 3-6: ITENS GERAIS ---
DADOS_GERAIS = {
    # Aventura
    "Mochila": {"subcategoria": "Aventura", "preco": 2, "espacos": 1, "notas": ""},
    "Corda (15m)": {"subcategoria": "Aventura", "preco": 5, "espacos": 1, "notas": ""},
    "Tocha": {"subcategoria": "Aventura", "preco": 1, "espacos": 1, "notas": "Luz 9m por 1h"},
    "Lanterna": {"subcategoria": "Aventura", "preco": 10, "espacos": 1, "notas": "Luz 9m; consome 1 óleo por 4h"},
    "Farol": {"subcategoria": "Aventura", "preco": 30, "espacos": 2, "notas": "Luz direcional 18m"},
    "Óleo (frasco)": {"subcategoria": "Aventura", "preco": 2, "espacos": 1, "notas": "Combustível p/ lanterna e farol"},
    "Pederneira": {"subcategoria": "Aventura", "preco": 1, "espacos": 1, "notas": "Acende fogo"},
    "Barraca (2 pessoas)": {"subcategoria": "Aventura", "preco": 10, "espacos": 2, "notas": ""},
    "Saco de dormir": {"subcategoria": "Aventura", "preco": 2, "espacos": 1, "notas": ""},
    "Cantil": {"subcategoria": "Aventura", "preco": 1, "espacos": 1, "notas": ""},
    "Ração de viagem (dia)": {"subcategoria": "Aventura", "preco": 1, "espacos": 1, "notas": ""},
    "Espelho de metal": {"subcategoria": "Aventura", "preco": 25, "espacos": 1, "notas": ""},
    "Apito": {"subcategoria": "Aventura", "preco": 5, "espacos": 1, "notas": ""},
    "Alforje": {"subcategoria": "Aventura", "preco": 5, "espacos": 1, "notas": ""},
    # Alquímicos
    "Ácido (frasco)": {"subcategoria": "Alquímico", "preco": 10, "espacos": 1, "notas": "Corrosivo (situacional)"},
    "Água benta (frasco)": {"subcategoria": "Alquímico", "preco": 25, "espacos": 1, "notas": "Contra mortos-vivos e trevas"},
    # Símbolos
    "Símbolo sagrado (prata)": {"subcategoria": "Símbolo", "preco": 25, "espacos": 1, "notas": "Foco p/ magias divinas"},
    "Símbolo sagrado (madeira)": {"subcategoria": "Símbolo", "preco": 5, "espacos": 1, "notas": "Foco p/ magias divinas"},
    # Ferramentas
    "Kit de ferramentas": {"subcategoria": "Ferramenta", "preco": 20, "espacos": 2, "notas": "Usado em Ofício"},
    "Kit de disfarces": {"subcategoria": "Ferramenta", "preco": 25, "espacos": 2, "notas": "Usado em Enganação (disfarce)"},
    "Kit de ladrão": {"subcategoria": "Ferramenta", "preco": 30, "espacos": 1, "notas": "Usado em Ladinagem (fechaduras)"},
    "Kit de medicamentos": {"subcategoria": "Ferramenta", "preco": 50, "espacos": 2, "notas": "Usado em Cura (medicina)"},
    "Instrumento musical (comum)": {"subcategoria": "Ferramenta", "preco": 15, "espacos": 2, "notas": "Usado em Atuação"},
    "Tinta (frasco)": {"subcategoria": "Ferramenta", "preco": 8, "espacos": 1, "notas": ""},
}