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
