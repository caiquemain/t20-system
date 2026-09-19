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

# ─────────────────────────────────────────────────────────────
# NORMALIZAÇÃO & CORREÇÕES (pós-extração de PDF)
# 1) remove espaços sobrando de chaves/valores string
# 2) corrige valores contra a Tabela 3-6 do JdA
# ─────────────────────────────────────────────────────────────
def _strip_dict(d):
    out = {}
    for k, v in d.items():
        nk = k.strip()
        nv = {kk.strip(): (vv.strip() if isinstance(vv, str) else vv) for kk, vv in v.items()}
        out[nk] = nv
    return out

DADOS_ARMAS = _strip_dict(DADOS_ARMAS)
DADOS_ARMADURAS = _strip_dict(DADOS_ARMADURAS)
DADOS_GERAIS = _strip_dict(DADOS_GERAIS)

_RENOMEIA = {
    "Corda (15m)": ("Corda (10m)", {"preco": 1}),
    "Espelho de metal": ("Espelho", {"preco": 10}),
    "Símbolo sagrado (madeira)": ("Símbolo sagrado", {}),
}
for velho, (novo, campos) in _RENOMEIA.items():
    if velho in DADOS_GERAIS:
        DADOS_GERAIS[novo] = DADOS_GERAIS.pop(velho)
        DADOS_GERAIS[novo].update(campos)

_CORRECOES_ARMAS = {
    "Rede": {"critico": None},
}
_CORRECOES_GERAIS = {
    "Mochila": {"espacos": 0, "notas": "Não ocupa espaço (regra p.141)"},
    "Água benta (frasco)": {"preco": 10, "espacos": 0.5},
    "Ácido (frasco)": {"espacos": 0.5},
    "Óleo (frasco)": {"preco": 0.1, "espacos": 0.5},
    "Tocha": {"preco": 0.1},
    "Saco de dormir": {"preco": 1},
    "Barraca (2 pessoas)": {"espacos": 1},
    "Ração de viagem (dia)": {"preco": 0.5, "espacos": 0.5},
    "Instrumento musical (comum)": {"preco": 35, "espacos": 1},
    "Kit de medicamentos": {"espacos": 1},
    "Alforje": {"subcategoria": "Animais", "preco": 30, "espacos": 0,
                "notas": "Montaria carrega até 10 espaços para você"},
    "Símbolo sagrado (prata)": {"notas": "Variante caseira — fora da tabela oficial JdA"},
}
for nome, campos in _CORRECOES_ARMAS.items():
    if nome in DADOS_ARMAS:
        DADOS_ARMAS[nome].update(campos)
for nome, campos in _CORRECOES_GERAIS.items():
    if nome in DADOS_GERAIS:
        DADOS_GERAIS[nome].update(campos)


# ─────────────────────────────────────────────────────────────
# ITENS AUSENTES DA TABELA 3-6 (completude do catálogo JdA)
# Valores conferidos no livro (preço T$ + espaços); notas = efeito mecânico curto.
# ─────────────────────────────────────────────────────────────
_ITENS_AUSENTES = {
    # --- Equipamento de Aventura ---
    "Algemas": {"subcategoria": "Aventura", "preco": 15, "espacos": 1, "notas": "Prender exige agarrar + teste; escapar CD 30 Acrobacia / 25 Força"},
    "Arpéu": {"subcategoria": "Aventura", "preco": 5, "espacos": 1, "notas": "+5 Atletismo p/ subir com corda; fixar CD 15 Pontaria"},
    "Bandoleira de poções": {"subcategoria": "Aventura", "preco": 20, "espacos": 1, "notas": "Vestido: sacar poções/alquímicos = ação livre"},
    "Lampião": {"subcategoria": "Aventura", "preco": 7, "espacos": 1, "notas": "Luz 15m; acender/carregar = ação padrão; dura 1 cena"},
    "Mochila de aventureiro": {"subcategoria": "Aventura", "preco": 50, "espacos": 0, "notas": "Vestido: +2 espaços de carga; não ocupa espaço"},
    "Organizador de pergaminhos": {"subcategoria": "Aventura", "preco": 25, "espacos": 1, "notas": "Vestido: sacar pergaminhos = ação livre"},
    "Pé de cabra": {"subcategoria": "Aventura", "preco": 2, "espacos": 1, "notas": "+5 Força p/ abrir; como arma usa stats de clava"},
    "Vara de madeira (3m)": {"subcategoria": "Aventura", "preco": 0.2, "espacos": 1, "notas": "Alcançar pontos distantes; frágil demais p/ arma"},
    # --- Ferramentas (nomes oficiais) ---
    "Alaúde élfico": {"subcategoria": "Ferramenta", "preco": 300, "espacos": 1, "notas": "Inspiração = ação de movimento; conta como instrumento musical"},
    "Coleção de livros": {"subcategoria": "Ferramenta", "preco": 75, "espacos": 1, "notas": "+1 em Conhecimento/Guerra/Misticismo/Nobreza/Religião (fixo na compra)"},
    "Equipamento de viagem": {"subcategoria": "Ferramenta", "preco": 10, "espacos": 1, "notas": "Sem ele: –5 Sobrevivência p/ acampar"},
    "Flauta mística": {"subcategoria": "Ferramenta", "preco": 150, "espacos": 1, "notas": "Bardo: +1 CD das magias; conta como instrumento musical"},
    "Luneta": {"subcategoria": "Ferramenta", "preco": 100, "espacos": 1, "notas": "+5 Percepção p/ observar em alcance longo ou além"},
    "Sela": {"subcategoria": "Ferramenta", "preco": 20, "espacos": 1, "notas": "Sem ela: –5 Cavalgar; no animal não ocupa espaço do personagem"},
    "Tambor das profundezas": {"subcategoria": "Ferramenta", "preco": 80, "espacos": 1, "notas": "Dobra alcance de Inspiração/Músicas de Bardo; conta como instrumento"},
    # --- Vestuário (todos precisam ser vestidos p/ funcionar) ---
    "Andrajos de aldeão": {"subcategoria": "Vestuário", "preco": 1, "espacos": 1, "notas": "+2 Investigação p/ interrogar; –2 perícias Carisma sociais"},
    "Bandana": {"subcategoria": "Vestuário", "preco": 5, "espacos": 1, "notas": "+1 Intimidação"},
    "Botas reforçadas": {"subcategoria": "Vestuário", "preco": 20, "espacos": 1, "notas": "+1,5m desloc. em terreno difícil (após a redução)"},
    "Camisa bufante": {"subcategoria": "Vestuário", "preco": 25, "espacos": 1, "notas": "+1 Atuação"},
    "Capa esvoaçante": {"subcategoria": "Vestuário", "preco": 25, "espacos": 1, "notas": "+1 Enganação"},
    "Capa pesada": {"subcategoria": "Vestuário", "preco": 15, "espacos": 1, "notas": "+1 Fortitude"},
    "Casaco longo": {"subcategoria": "Vestuário", "preco": 20, "espacos": 1, "notas": "+5 Fortitude vs frio; penalidade de armadura –2"},
    "Chapéu arcano": {"subcategoria": "Vestuário", "preco": 50, "espacos": 1, "notas": "+1 PM (apenas com Caminho do Arcanista)"},
    "Enfeite de elmo": {"subcategoria": "Vestuário", "preco": 15, "espacos": 1, "notas": "Resistência a medo +2"},
    "Farrapos de ermitão": {"subcategoria": "Vestuário", "preco": 1, "espacos": 1, "notas": "+2 Adestramento; –2 Diplomacia e Investigação p/ interrogar"},
    "Gorro de ervas": {"subcategoria": "Vestuário", "preco": 75, "espacos": 1, "notas": "+1 Vontade"},
    "Luva de pelica": {"subcategoria": "Vestuário", "preco": 5, "espacos": 1, "notas": "+1 Ladinagem"},
    "Manopla": {"subcategoria": "Vestuário", "preco": 10, "espacos": 1, "notas": "Dano desarmado vira letal; conta como arma p/ melhorias"},
    "Manto camuflado": {"subcategoria": "Vestuário", "preco": 12, "espacos": 1, "notas": "+2 Furtividade no terreno específico"},
    "Manto eclesiástico": {"subcategoria": "Vestuário", "preco": 20, "espacos": 1, "notas": "+1 Religião"},
    "Robe místico": {"subcategoria": "Vestuário", "preco": 50, "espacos": 1, "notas": "+1 Misticismo"},
    "Sapatos de camurça": {"subcategoria": "Vestuário", "preco": 8, "espacos": 1, "notas": "+1 Acrobacia"},
    "Tabardo": {"subcategoria": "Vestuário", "preco": 10, "espacos": 1, "notas": "+1 Diplomacia"},
    "Traje da corte": {"subcategoria": "Vestuário", "preco": 100, "espacos": 1, "notas": "Sem ele: –5 perícias Carisma em ambientes nobres"},
    "Traje de viajante": {"subcategoria": "Vestuário", "preco": 10, "espacos": 0, "notas": "Roupa padrão; sem bônus (não conta p/ limite de 4 vestidos)"},
    "Veste de seda": {"subcategoria": "Vestuário", "preco": 25, "espacos": 1, "notas": "+1 Reflexos"},
    # --- Esotéricos ---
    "Bolsa de pó": {"subcategoria": "Esotérico", "preco": 300, "espacos": 1, "notas": "+2 PM p/ aprimoramentos de Encantamento/Ilusão"},
    "Cajado arcano": {"subcategoria": "Esotérico", "preco": 1000, "espacos": 2, "notas": "+1 limite PM e +1 CD arcanas; 2 mãos; como arma = bordão"},
    "Cetro elemental": {"subcategoria": "Esotérico", "preco": 750, "espacos": 1, "notas": "+1 dado de dano do tipo da gema (ácido/eletricidade/fogo/frio)"},
    "Costela de lich": {"subcategoria": "Esotérico", "preco": 300, "espacos": 1, "notas": "+1d6 trevas nas magias; não recupera PV por cura mágica"},
    "Dedo de ente": {"subcategoria": "Esotérico", "preco": 200, "espacos": 1, "notas": "Ao gastar ≥1 PM: role 1d4, com 4 recupera 1 PM"},
    "Luva de ferro": {"subcategoria": "Esotérico", "preco": 150, "espacos": 1, "notas": "+1 em bônus de Defesa/resistência de magias pessoais"},
    "Medalhão de prata": {"subcategoria": "Esotérico", "preco": 750, "espacos": 1, "notas": "–1 PM em magias de alcance pessoal"},
    "Orbe cristalino": {"subcategoria": "Esotérico", "preco": 750, "espacos": 1, "notas": "+1 limite PM arcano"},
    "Tomo hermético": {"subcategoria": "Esotérico", "preco": 1500, "espacos": 1, "notas": "+2 CD de magias arcanas de 1 escola específica"},
    "Varinha arcana": {"subcategoria": "Esotérico", "preco": 100, "espacos": 1, "notas": "+1 CD de magias arcanas"},
    # --- Alquímicos: Preparados ---
    "Bálsamo restaurador": {"subcategoria": "Alquímico", "preco": 10, "espacos": 0.5, "notas": "Ação completa: cura 2d4 PV"},
    "Bomba": {"subcategoria": "Alquímico", "preco": 50, "espacos": 0.5, "notas": "6d6 impacto em 3m (Ref Des metade); acender mov. + arremessar padrão"},
    "Cosmético": {"subcategoria": "Alquímico", "preco": 30, "espacos": 0.5, "notas": "Ação completa: +2 perícias Carisma até fim da cena"},
    "Elixir do amor": {"subcategoria": "Alquímico", "preco": 100, "espacos": 0.5, "notas": "Enfeitiçado pela 1ª criatura vista (Vontade Car anula); 1d3 dias"},
    "Essência de mana": {"subcategoria": "Alquímico", "preco": 50, "espacos": 0.5, "notas": "Ação padrão: recupera 1d4 PM"},
    "Fogo alquímico": {"subcategoria": "Alquímico", "preco": 10, "espacos": 0.5, "notas": "1d6 fogo + em chamas (Ref Des metade evita as chamas)"},
    "Pó do desaparecimento": {"subcategoria": "Alquímico", "preco": 100, "espacos": 0.5, "notas": "Invisível por 2d6 rodadas (usuário não sabe quando termina)"},
    # --- Alquímicos: Catalisadores ---
    "Baga-de-fogo": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "+1d6 dano de fogo à magia"},
    "Dente-de-dragão": {"subcategoria": "Catalisador", "preco": 45, "espacos": 0.5, "notas": "+1 dado de dano do mesmo tipo"},
    "Essência abissal": {"subcategoria": "Catalisador", "preco": 150, "espacos": 0.5, "notas": "Aumenta categoria dos dados de dano de fogo (d4→d6→...→d12)"},
    "Líquen lilás": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "+1d6 dano de frio"},
    "Musgo púrpura": {"subcategoria": "Catalisador", "preco": 45, "espacos": 0.5, "notas": "+2 CD de magias de ilusão"},
    "Ossos de monstro": {"subcategoria": "Catalisador", "preco": 45, "espacos": 0.5, "notas": "+2 CD de magias de necromancia"},
    "Pó de cristal": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "–1 PM em magias de encantamento"},
    "Pó de giz": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "–1 PM em magias de convocação"},
    "Ramo verdejante": {"subcategoria": "Catalisador", "preco": 45, "espacos": 0.5, "notas": "+1 PV por dado de cura"},
    "Saco de sal": {"subcategoria": "Catalisador", "preco": 45, "espacos": 0.5, "notas": "+2 CD de magias de abjuração"},
    "Seixo de âmbar": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "–1 PM em magias de transmutação"},
    "Terra de cemitério": {"subcategoria": "Catalisador", "preco": 30, "espacos": 0.5, "notas": "+1d6 dano de trevas"},
    # --- Alquímicos: Venenos ---
    "Beladona": {"subcategoria": "Venenos", "preco": 1500, "espacos": 0.5, "notas": "Ingestão: lenta 3 rod.; CD fabricar/resistir +5"},
    "Bruma sonolenta": {"subcategoria": "Venenos", "preco": 150, "espacos": 0.5, "notas": "Inalação: inconsciente (enjorado 1 rod. se passar)"},
    "Cicuta": {"subcategoria": "Venenos", "preco": 60, "espacos": 0.5, "notas": "Ingestão: 1d12 PV/rod. por 3 rod."},
    "Essência de sombra": {"subcategoria": "Venenos", "preco": 100, "espacos": 0.5, "notas": "Contato: debilitada (fraca se passar)"},
    "Névoa tóxica": {"subcategoria": "Venenos", "preco": 30, "espacos": 0.5, "notas": "Inalação: 1d12 PV/rod. por 3 rod."},
    "Peçonha comum": {"subcategoria": "Venenos", "preco": 15, "espacos": 0.5, "notas": "Contato: perde 1d12 PV"},
    "Peçonha concentrada": {"subcategoria": "Venenos", "preco": 90, "espacos": 0.5, "notas": "Contato: 1d12 PV/rod. por 3 rod."},
    "Peçonha potente": {"subcategoria": "Venenos", "preco": 600, "espacos": 0.5, "notas": "Contato: 2d12 PV/rod. por 3 rod."},
    "Pó de lich": {"subcategoria": "Venenos", "preco": 3000, "espacos": 0.5, "notas": "Ingestão: 4d12 PV/rod. por 5 rod.; CD +5"},
    "Riso de Nimb": {"subcategoria": "Venenos", "preco": 150, "espacos": 0.5, "notas": "Inalação: confusa (lenta 1 rod. se passar)"},
    # --- Alimentação (pratos especiais: 1 bônus/dia) ---
    "Batata valkariana": {"subcategoria": "Alimentação", "preco": 2, "espacos": 0.5, "notas": "+1d6 em 1 teste até fim do dia"},
    "Gorad quente": {"subcategoria": "Alimentação", "preco": 18, "espacos": 0.5, "notas": "+2 PM temporários"},
    "Macarrão de Yuvalin": {"subcategoria": "Alimentação", "preco": 6, "espacos": 0.5, "notas": "+5 PV temporários"},
    "Prato do aventureiro": {"subcategoria": "Alimentação", "preco": 1, "espacos": 0.5, "notas": "+1 PV/nível na próxima noite de sono"},
    "Refeição comum": {"subcategoria": "Alimentação", "preco": 0.3, "espacos": 0.5, "notas": "Sem efeito mecânico"},
    "Sopa de peixe": {"subcategoria": "Alimentação", "preco": 1, "espacos": 0.5, "notas": "+1 PM/nível na próxima noite de sono"},
    # --- Animais (parceiros/montarias; não ocupam espaço do personagem) ---
    "Cão de caça": {"subcategoria": "Animal", "preco": 150, "espacos": 0, "notas": "Parceiro perseguidor (Adestramento) ou montaria p/ Pequenos/Minúsculos"},
    "Cavalo": {"subcategoria": "Animal", "preco": 75, "espacos": 0, "notas": "Montaria; sem treinamento: Cavalgar CD 20/rod. em combate"},
    "Cavalo de guerra": {"subcategoria": "Animal", "preco": 400, "espacos": 0, "notas": "Montaria treinada (dispensa teste em combate)"},
    "Estábulo (por dia)": {"subcategoria": "Animal", "preco": 0.1, "espacos": 0, "notas": "Inclui alimentação do animal"},
    "Pônei": {"subcategoria": "Animal", "preco": 5, "espacos": 0, "notas": "Montaria p/ raças Pequenas; sem treinamento: Cavalgar CD 20"},
    "Pônei de guerra": {"subcategoria": "Animal", "preco": 30, "espacos": 0, "notas": "Montaria treinada p/ raças Pequenas"},
    "Trobo": {"subcategoria": "Animal", "preco": 60, "espacos": 0, "notas": "Montaria/carga; ave dócil sem asas"},
    # --- Veículos (stats próprias; não ocupam espaço) ---
    "Balão goblin": {"subcategoria": "Veículo", "preco": 200, "espacos": 0, "notas": "Enorme, voo 12m, 100 PV, 8 criaturas Médias / 160 espaços"},
    "Carroça": {"subcategoria": "Veículo", "preco": 150, "espacos": 0, "notas": "Grande, 9m, 50 PV, 4 criaturas / 80 espaços"},
    "Carruagem": {"subcategoria": "Veículo", "preco": 500, "espacos": 0, "notas": "Como carroça + cobertura leve p/ passageiros"},
    "Canoa": {"subcategoria": "Veículo", "preco": 70, "espacos": 0, "notas": "Como carroça, deslocamento de natação"},
    "Veleiro": {"subcategoria": "Veículo", "preco": 10000, "espacos": 0, "notas": "Navio de viagem com 3 mastros"},
}

for _nome, _dados in _ITENS_AUSENTES.items():
    DADOS_GERAIS[_nome] = _dados

# Renomeia ferramentas caseiras p/ os nomes oficiais do livro
_RENOMEIA_FERRAMENTAS = {
    "Kit de ferramentas": "Instrumentos de <ofício>",
    "Kit de disfarces": "Estojo de disfarces",
    "Kit de ladrão": "Gazua",
    "Kit de medicamentos": "Maleta de medicamentos",
    "Instrumento musical (comum)": "Instrumento musical",
}
for _velho, _novo in _RENOMEIA_FERRAMENTAS.items():
    if _velho in DADOS_GERAIS:
        DADOS_GERAIS[_novo] = DADOS_GERAIS.pop(_velho)

# Valores oficiais pós-renomeio
DADOS_GERAIS["Instrumentos de <ofício>"].update({"preco": 30, "espacos": 1, "notas": "Sem eles: –5 na perícia de Ofício"})
DADOS_GERAIS["Estojo de disfarces"].update({"preco": 50, "espacos": 1, "notas": "Sem ele: –5 Enganação p/ disfarce"})
DADOS_GERAIS["Gazua"].update({"preco": 5, "espacos": 1, "notas": "Sem ela: –5 Ladinagem p/ abrir fechaduras"})
DADOS_GERAIS["Maleta de medicamentos"].update({"preco": 50, "espacos": 1, "notas": "Sem ela: –5 Cura"})
DADOS_GERAIS["Instrumento musical"].update({"preco": 35, "espacos": 1, "notas": "2 mãos p/ Músicas de Bardo; bardos podem usá-lo como esotérico"})

# Alforje: categoria oficial é Animais
if "Alforje" in DADOS_GERAIS:
    DADOS_GERAIS["Alforje"].update({"subcategoria": "Animal", "preco": 30, "espacos": 0,
                                    "notas": "Montaria carrega até 10 espaços para você"})

# --- Serviços (não ocupam espaço; preços por uso) ---
DADOS_SERVICOS = {
    "Estadia comum (noite)": {"preco": 0.5, "unidade": "noite", "notas": "Recupera 1 PV e 1 PM por nível"},
    "Estadia confortável (noite)": {"preco": 4, "unidade": "noite", "notas": "Recupera 2 PV e 2 PM por nível"},
    "Estadia luxuosa (noite)": {"preco": 20, "unidade": "noite", "notas": "Recupera 3 PV e 3 PM por nível"},
    "Condução terrestre (km)": {"preco": 0.5, "unidade": "km", "notas": ""},
    "Condução marítima (km)": {"preco": 0.1, "unidade": "km", "notas": ""},
    "Condução aérea (km)": {"preco": 10, "unidade": "km", "notas": "Balão goblin: 1/20 de queda a cada 100 km"},
    "Curandeiro": {"preco": 5, "unidade": "consulta", "notas": "Tratamento prolongado de doença/veneno"},
    "Magia 1º círculo": {"preco": 10, "unidade": "lançamento", "notas": ""},
    "Magia 2º círculo": {"preco": 90, "unidade": "lançamento", "notas": ""},
    "Magia 3º círculo": {"preco": 360, "unidade": "lançamento", "notas": ""},
    "Mensageiro (km)": {"preco": 0.5, "unidade": "km", "notas": ""},
}
