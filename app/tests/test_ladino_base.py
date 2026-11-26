"""Ladino — testes de classe base, Ataque Furtivo e habilidades fixas (T20 JdA p.72-74)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _ladino(nivel=1, con=1, des=4, inte=3):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Leon", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Ladino", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, destreza=des, inteligencia=inte)
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
def test_ladino_pv_por_nivel(nivel, esperado):
    f = _ladino(nivel=nivel, con=1)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 4), (5, 20), (20, 80)])
def test_ladino_pm_por_nivel(nivel, esperado):
    f = _ladino(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_ladino_pericias_e_proficiencias():
    f = _ladino()
    atualizar_ficha(f)
    assert f.pericias["Ladinagem"].treino == 1
    assert f.pericias["Reflexos"].treino == 1
    dc = DADOS_CLASSES["Ladino"]
    assert dc["pericias_escolha"] == 8
    assert len(dc["pericias_lista"]) == 18
    assert dc["proficiencias"] == []


def test_ladino_habilidades_fixas_progressao():
    f1 = _ladino(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Ataque Furtivo") is not None
    assert _achar(f1, "Especialista") is not None
    assert _achar(f1, "Evasão") is None

    f4 = _ladino(nivel=4)
    atualizar_ficha(f4)
    assert _achar(f4, "Evasão") is not None
    assert _achar(f4, "Esquiva Sobrenatural") is not None
    assert "surpreendido" in f4.status.imunidades

    f8 = _ladino(nivel=8)
    atualizar_ficha(f8)
    assert _achar(f8, "Olhos nas Costas") is not None
    assert "flanqueado" in f8.status.imunidades

    f10 = _ladino(nivel=10)
    atualizar_ficha(f10)
    assert _achar(f10, "Evasão Aprimorada") is not None

    f20 = _ladino(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "A Pessoa Certa para o Trabalho") is not None


@pytest.mark.parametrize("nivel,dados_esp,formula_esp", [
    (1, 1, "1d6"),
    (2, 1, "1d6"),
    (3, 2, "2d6"),
    (5, 3, "3d6"),
    (7, 4, "4d6"),
    (9, 5, "5d6"),
    (11, 6, "6d6"),
    (13, 7, "7d6"),
    (15, 8, "8d6"),
    (17, 9, "9d6"),
    (19, 10, "10d6"),
    (20, 10, "10d6"),
])
def test_ataque_furtivo_escala_tabela(nivel, dados_esp, formula_esp):
    f = _ladino(nivel=nivel, inte=3)
    atualizar_ficha(f)
    af = f.combate.ataque_furtivo_calc
    assert af is not None
    assert af["dados"] == dados_esp
    assert af["formula"] == formula_esp
    assert af["especialista_slots"] == 3
