"""Inventor — testes de classe base, habilidades fixas e progressão de fabricação (T20 JdA p.67-71)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _inventor(nivel=1, con=1, inte=5):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Marlin", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Inventor", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, inteligencia=inte)
    f.atributos = f.atributos_base.model_copy()
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


@pytest.mark.parametrize("nivel,esperado", [
    (1, 13),   # 12 + 1
    (2, 17),   # 13 + 1*(3+1)
    (5, 29),   # 13 + 4*(3+1)
    (10, 49),  # 13 + 9*(3+1)
])
def test_inventor_pv_por_nivel(nivel, esperado):
    f = _inventor(nivel=nivel, con=1)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 4), (5, 20), (20, 80)])
def test_inventor_pm_por_nivel(nivel, esperado):
    f = _inventor(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_inventor_pericias_e_proficiencias():
    f = _inventor()
    atualizar_ficha(f)
    assert f.pericias["Vontade"].treino == 1
    dc = DADOS_CLASSES["Inventor"]
    assert dc["pericias_escolha"] == 4
    assert len(dc["pericias_lista"]) == 12
    assert "Ofício" in dc["pericias_lista"]
    assert dc["proficiencias"] == []


def test_inventor_habilidades_fixas_progressao():
    f1 = _inventor(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Engenhosidade") is not None
    assert _achar(f1, "Protótipo") is not None
    assert _achar(f1, "Fabricar Item Superior") is None

    f3 = _inventor(nivel=3)
    atualizar_ficha(f3)
    assert _achar(f3, "Fabricar Item Superior") is not None
    assert _achar(f3, "Comerciante") is not None

    f10 = _inventor(nivel=10)
    atualizar_ficha(f10)
    assert _achar(f10, "Encontrar Fraqueza") is not None
    assert _achar(f10, "Fabricar Item Mágico") is not None
    assert _achar(f10, "Olho do Dragão") is not None

    f20 = _inventor(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Obra-Prima") is not None


@pytest.mark.parametrize("nivel,melhorias,item_magico", [
    (1, 0, None),
    (2, 1, None),
    (5, 2, None),
    (8, 3, None),
    (9, 3, "Menor"),
    (11, 4, "Menor"),
    (13, 4, "Médio"),
    (17, 4, "Maior"),
])
def test_inventor_progressao_melhorias_e_item_magico(nivel, melhorias, item_magico):
    f = _inventor(nivel=nivel)
    atualizar_ficha(f)
    ic = f.combate.inventor_calc
    assert ic["melhorias_max"] == melhorias
    assert ic["item_magico"] == item_magico
