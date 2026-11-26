# -*- coding: utf-8 -*-
"""Testes da Tabela 2-1: Perícias (T20 JdA p.114-123) e cálculo de bônus de treinamento."""
import pytest
from src.dados_pericias import DADOS_PERICIAS
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos
from src.regras import atualizar_ficha


def test_tabela_2_1_todas_29_pericias_oficiais():
    assert len(DADOS_PERICIAS) == 29

    somente_treinadas = {k for k, v in DADOS_PERICIAS.items() if v["treino_apenas"]}
    assert somente_treinadas == {
        "Adestramento", "Atuação", "Conhecimento", "Guerra", "Jogatina",
        "Ladinagem", "Misticismo", "Nobreza", "Ofício", "Pilotagem", "Religião",
    }

    penalidade_armadura = {k for k, v in DADOS_PERICIAS.items() if v["penalidade_armadura"]}
    assert penalidade_armadura == {"Acrobacia", "Furtividade", "Ladinagem"}


@pytest.mark.parametrize("nivel,metade,treino", [
    (1, 0, 2),
    (6, 3, 2),
    (7, 3, 4),
    (14, 7, 4),
    (15, 7, 6),
    (20, 10, 6),
])
def test_formula_valor_pericia_por_nivel(nivel, metade, treino):
    f = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Teste", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
        atributos_base=Atributos(forca=4, destreza=0, constituicao=0, inteligencia=0, sabedoria=0, carisma=0),
    ))
    # Guerreiro tem Fortitude como perícia fixa (Con 0) -> metade + 0 + treino
    assert f.pericias["Fortitude"].total == metade + treino
    # Atletismo não treinada (For 4) -> metade + 4
    assert f.pericias["Atletismo"].total == metade + 4
