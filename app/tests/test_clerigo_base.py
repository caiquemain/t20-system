"""Clérigo — testes de classe base, habilidades fixas e progressão mágica (T20 JdA p.56-58).

Cobre:
    PV: 16 + Con inicial; +4 + Con por nível
    PM: 5 por nível + Sabedoria
    Perícias: Religião, Vontade + 2 escolhas (11 opções)
    Proficiências: Armaduras Pesadas e Escudos
    Habilidades fixas: Devoto Fiel (1º), Magias (Clérigo) (1º), Mão da Divindade (20º)
    Círculos: 1º (1º), 2º (5º), 3º (9º), 4º (13º), 5º (17º)
    Magias conhecidas: 3 iniciais + 1 por nível
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _clerigo(nivel=1, con=2, sab=4):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Vanessa", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Clérigo", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, sabedoria=sab)
    f.atributos = f.atributos_base.model_copy()
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


@pytest.mark.parametrize("nivel,esperado", [
    (1, 18),   # 16 + 2
    (2, 24),   # 18 + 1*(4+2)
    (5, 42),   # 18 + 4*(4+2)
    (10, 72),  # 18 + 9*(4+2)
])
def test_clerigo_pv_por_nivel(nivel, esperado):
    f = _clerigo(nivel=nivel, con=2)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,sab,esperado", [
    (1, 4, 9),     # 5*1 + 4
    (5, 4, 29),    # 5*5 + 4
    (20, 6, 106),  # 5*20 + 6
])
def test_clerigo_pm_soma_sabedoria(nivel, sab, esperado):
    f = _clerigo(nivel=nivel, sab=sab)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_clerigo_pericias_e_proficiencias():
    f = _clerigo()
    atualizar_ficha(f)
    assert f.pericias["Religião"].treino == 1
    assert f.pericias["Vontade"].treino == 1
    assert "Armaduras Pesadas" in f.status.proficiencias
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Clérigo"]
    assert dc["pericias_escolha"] == 2
    assert len(dc["pericias_lista"]) == 11


def test_clerigo_habilidades_fixas_progressao():
    f1 = _clerigo(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Devoto Fiel") is not None
    assert _achar(f1, "Magias (Clérigo)") is not None
    assert _achar(f1, "Mão da Divindade") is None

    f20 = _clerigo(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Mão da Divindade") is not None


@pytest.mark.parametrize("nivel,circulo_esp", [
    (1, 1), (4, 1), (5, 2), (8, 2), (9, 3), (12, 3), (13, 4), (16, 4), (17, 5), (20, 5),
])
def test_clerigo_circulos_magia(nivel, circulo_esp):
    f = _clerigo(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.circulo_maximo == circulo_esp


@pytest.mark.parametrize("nivel,limite_esp", [
    (1, 3), (2, 4), (5, 7), (10, 12), (20, 22),
])
def test_clerigo_limite_magias_conhecidas(nivel, limite_esp):
    f = _clerigo(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.limite_magias == limite_esp
