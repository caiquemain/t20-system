# --- TABELA DE PERÍCIAS (T20 Jogo do Ano) ---
# Estrutura: "Nome": {"atributo": "...", "treino_apenas": bool, "penalidade_armadura": bool}

DADOS_PERICIAS = {
    "Acrobacia":    {"atributo": "des", "treino_apenas": False, "penalidade_armadura": True},
    "Adestramento": {"atributo": "car", "treino_apenas": True,  "penalidade_armadura": False},
    "Atletismo":    {"atributo": "for", "treino_apenas": False, "penalidade_armadura": False},
    "Atuação":      {"atributo": "car", "treino_apenas": True,  "penalidade_armadura": False},
    "Cavalgar":     {"atributo": "des", "treino_apenas": False, "penalidade_armadura": False},
    "Conhecimento": {"atributo": "int", "treino_apenas": True,  "penalidade_armadura": False},
    "Cura":         {"atributo": "sab", "treino_apenas": False, "penalidade_armadura": False},
    "Diplomacia":   {"atributo": "car", "treino_apenas": False, "penalidade_armadura": False},
    "Enganação":    {"atributo": "car", "treino_apenas": False, "penalidade_armadura": False},
    "Fortitude":    {"atributo": "con", "treino_apenas": False, "penalidade_armadura": False},
    "Furtividade":  {"atributo": "des", "treino_apenas": False, "penalidade_armadura": True},
    "Guerra":       {"atributo": "int", "treino_apenas": True,  "penalidade_armadura": False},
    "Iniciativa":   {"atributo": "des", "treino_apenas": False, "penalidade_armadura": False},
    "Intimidação":  {"atributo": "car", "treino_apenas": False, "penalidade_armadura": False},
    "Intuição":     {"atributo": "sab", "treino_apenas": False, "penalidade_armadura": False},
    "Investigação": {"atributo": "int", "treino_apenas": False, "penalidade_armadura": False},
    "Jogatina":     {"atributo": "car", "treino_apenas": True,  "penalidade_armadura": False},
    "Ladinagem":    {"atributo": "des", "treino_apenas": True,  "penalidade_armadura": True},
    "Luta":         {"atributo": "for", "treino_apenas": False, "penalidade_armadura": False},
    "Misticismo":   {"atributo": "int", "treino_apenas": True,  "penalidade_armadura": False},
    "Nobreza":      {"atributo": "int", "treino_apenas": True,  "penalidade_armadura": False},
    # Genérico para a lista base
    "Ofício":       {"atributo": "int", "treino_apenas": True,  "penalidade_armadura": False},
    "Percepção":    {"atributo": "sab", "treino_apenas": False, "penalidade_armadura": False},
    "Pilotagem":    {"atributo": "des", "treino_apenas": True,  "penalidade_armadura": False},
    "Pontaria":     {"atributo": "des", "treino_apenas": False, "penalidade_armadura": False},
    "Reflexos":     {"atributo": "des", "treino_apenas": False, "penalidade_armadura": False},
    "Religião":     {"atributo": "sab", "treino_apenas": True,  "penalidade_armadura": False},
    "Sobrevivência": {"atributo": "sab", "treino_apenas": False, "penalidade_armadura": False},
    "Vontade":      {"atributo": "sab", "treino_apenas": False, "penalidade_armadura": False}
}

# Lista de Tipos de Ofícios para o Frontend
TIPOS_OFICIO = [
    "Alquimia", "Armeiro", "Artesão", "Alfaiate", "Cozinheiro", "Escrita", "Fazendeiro", "Engenhoqueiro"
]
