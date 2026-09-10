# -*- coding: utf-8 -*-
"""Regras de MAGIAS CONHECIDAS por classe/subclasse (T20 Jogo do Ano)."""

# Classe base: magias iniciais no 1º nível e aprendizadas por nível seguinte
REGRAS_MAGIAS_CONHECIDAS = {
    "Arcanista": {"inicial": 3, "por_nivel": 1},
    # Bardo, Clérigo, Druida: adicionar quando o texto do livro for confirmado
}

# Modificadores por subclasse (Caminho do Arcanista)
REGRAS_MAGIAS_POR_SUBCLASSE = {
    "Mago": {"inicial_extra": 1, "extra_por_circulo_novo": 1},
    "Feiticeiro": {"aprende_apenas_niveis_impares": True},
    "Bruxo": {},
}

# Poderes que aumentam o limite de magias conhecidas
PODERES_QUE_DAO_MAGIAS = {
    "Conhecimento Mágico": 2,
}


# ── Outras classes conjuradoras (T20 livro base) ──
# Bardo: 2 magias iniciais; +1 a cada nível PAR (2º, 4º...)
REGRAS_MAGIAS_CONHECIDAS["Bardo"] = {"inicial": 2, "por_nivel": 0, "aprende_apenas_niveis_pares": True}
# Druida: idem ao Bardo
REGRAS_MAGIAS_CONHECIDAS["Druida"] = {"inicial": 2, "por_nivel": 0, "aprende_apenas_niveis_pares": True}
# Clérigo: 3 iniciais; +1 por nível (igual Arcanista)
REGRAS_MAGIAS_CONHECIDAS["Clérigo"] = {"inicial": 3, "por_nivel": 1}
