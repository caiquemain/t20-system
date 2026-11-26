"""Druida — testes de classe base, habilidades fixas, progressão mágica e Força da Natureza (T20 JdA p.60-63)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Magia
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha
from src.regras.custo_magia import calcular_cd_magia, calcular_custo_magia


def _druida(nivel=1, con=2, sab=4, condicoes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Oihana", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Druida", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, sabedoria=sab)
    f.atributos = f.atributos_base.model_copy()
    if condicoes:
        f.condicoes_ativas = list(condicoes)
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


@pytest.mark.parametrize("nivel,esperado", [
    (1, 18),   # 16 + 2
    (2, 24),   # 18 + 1*(4+2)
    (5, 42),   # 18 + 4*(4+2)
    (10, 72),  # 18 + 9*(4+2)
])
def test_druida_pv_por_nivel(nivel, esperado):
    f = _druida(nivel=nivel, con=2)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,sab,esperado", [
    (1, 4, 8),    # 4*1 + 4
    (5, 4, 24),   # 4*5 + 4
    (20, 6, 86),  # 4*20 + 6
])
def test_druida_pm_soma_sabedoria(nivel, sab, esperado):
    f = _druida(nivel=nivel, sab=sab)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_druida_pericias_e_proficiencias():
    f = _druida()
    atualizar_ficha(f)
    assert f.pericias["Sobrevivência"].treino == 1
    assert f.pericias["Vontade"].treino == 1
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Druida"]
    assert dc["pericias_escolha"] == 4
    assert len(dc["pericias_lista"]) == 13


def test_druida_habilidades_fixas_progressao():
    f1 = _druida(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Devoto Fiel (Druida)") is not None
    assert _achar(f1, "Empatia Selvagem") is not None
    assert _achar(f1, "Magias (Druida)") is not None
    assert _achar(f1, "Caminho dos Ermos") is None

    f2 = _druida(nivel=2)
    atualizar_ficha(f2)
    assert _achar(f2, "Caminho dos Ermos") is not None
    assert _achar(f2, "Força da Natureza") is None

    f20 = _druida(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Força da Natureza") is not None


@pytest.mark.parametrize("nivel,circulo_esp", [
    (1, 1), (5, 1), (6, 2), (9, 2), (10, 3), (13, 3), (14, 4), (20, 4),
])
def test_druida_circulos_magia(nivel, circulo_esp):
    f = _druida(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.circulo_maximo == circulo_esp


@pytest.mark.parametrize("nivel,limite_esp", [
    (1, 2), (2, 3), (3, 3), (4, 4), (10, 7), (20, 12),
])
def test_druida_limite_magias_conhecidas(nivel, limite_esp):
    f = _druida(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.limite_magias == limite_esp


def test_forca_da_natureza_reduz_custo_e_aumenta_cd():
    magia_3 = Magia(nome="Controlar Plantas", circulo=3, tipo="Divina", atributo_chave="sab")

    # Fora de terreno natural: -2 PM (6 -> 4) e +2 CD (10 + 10 + 5 + 2 = 27)
    f_fora = _druida(nivel=20, sab=5, condicoes=[])
    atualizar_ficha(f_fora)
    assert calcular_custo_magia(f_fora, magia_3).total == 4
    assert calcular_cd_magia(f_fora, magia_3) == 27

    # Em terreno natural: -4 PM (6 -> 2) e +4 CD (10 + 10 + 5 + 4 = 29)
    f_nat = _druida(nivel=20, sab=5, condicoes=["terreno_natural"])
    atualizar_ficha(f_nat)
    assert calcular_custo_magia(f_nat, magia_3).total == 2
    assert calcular_cd_magia(f_nat, magia_3) == 29
