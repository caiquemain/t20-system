# -*- coding: utf-8 -*-
"""Progressão oficial de círculos de magia por classe (T20 Jogo do Ano).

Formato: {nivel_minimo: circulo_ganho}
Ex.: Arcanista ganha o 2º círculo no nível 5 -> {5: 2}
Classes que não conjuram não aparecem aqui (círculo máximo = 0).
"""

PROGRESSAO_CIRCULOS_POR_CLASSE = {
    # Tabela 1-5 / 1-11: 1º no 1, 2º no 5, 3º no 9, 4º no 13, 5º no 17
    "Arcanista": {1: 1, 5: 2, 9: 3, 13: 4, 17: 5},
    "Clérigo":   {1: 1, 5: 2, 9: 3, 13: 4, 17: 5},
    # Tabela 1-7 / 1-12: 1º no 1, 2º no 6, 3º no 10, 4º no 14 (para no 4º)
    "Bardo":     {1: 1, 6: 2, 10: 3, 14: 4},
    "Druida":    {1: 1, 6: 2, 10: 3, 14: 4},
}


# Subclasses (Caminhos) que herdam a progressão da classe base.
# Ex.: "Caminho do Arcanista" -> Bruxo / Mago / Feiticeiro
MAPA_SUBCLASSE_PARA_CLASSE = {
    "Bruxo": "Arcanista",
    "Mago": "Arcanista",
    "Feiticeiro": "Arcanista",
}
