"""Bardo — testes de classe base, habilidades fixas e progressão mágica (T20 JdA p.43-44).

Cobre:
    PV: 12 + Con inicial; +3 + Con por nível
    PM: 4 por nível + Carisma
    Perícias: Atuação e Reflexos + 6 escolhas entre 17 opções
    Proficiências: Armas Marciais
    Habilidades fixas: Inspiração (1º), Magias (Bardo) (1º), Eclético (2º), Artista Completo (20º)
    Círculos de magia: 1º (nv 1), 2º (nv 6), 3º (nv 10), 4º (nv 14)
    Magias conhecidas: 2 iniciais + 1 por nível par
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _bardo(nivel=1, con=1, car=4):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Menestrel", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bardo", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, carisma=car, destreza=2)
    f.atributos = f.atributos_base.model_copy()
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


# ===================================================================
# 1. PV / PM / Perícias / Proficiências
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 13),   # 12 + 1
    (2, 17),   # 13 + 1*(3+1)
    (5, 29),   # 13 + 4*(3+1)
    (10, 49),  # 13 + 9*(3+1)
])
def test_bardo_pv_por_nivel(nivel, esperado):
    f = _bardo(nivel=nivel, con=1)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,car,esperado", [
    (1, 4, 8),    # 4*1 + 4
    (5, 4, 24),   # 4*5 + 4
    (10, 5, 45),  # 4*10 + 5
])
def test_bardo_pm_soma_carisma(nivel, car, esperado):
    f = _bardo(nivel=nivel, car=car)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_bardo_pericias_fixas_e_lista_escolhas():
    f = _bardo()
    atualizar_ficha(f)
    assert f.pericias["Atuação"].treino == 1
    assert f.pericias["Reflexos"].treino == 1

    dc = DADOS_CLASSES["Bardo"]
    assert dc["pericias_escolha"] == 6
    assert len(dc["pericias_lista"]) == 17


def test_bardo_proficiencias():
    f = _bardo()
    atualizar_ficha(f)
    assert "Armas Marciais" in f.status.proficiencias


# ===================================================================
# 2. Habilidades fixas por nível
# ===================================================================

def test_bardo_habilidades_fixas_nivel_1():
    f = _bardo(nivel=1)
    atualizar_ficha(f)
    assert _achar(f, "Inspiração") is not None
    assert _achar(f, "Magias (Bardo)") is not None
    assert _achar(f, "Eclético") is None
    assert _achar(f, "Artista Completo") is None


def test_bardo_ecletico_nivel_2():
    f = _bardo(nivel=2)
    atualizar_ficha(f)
    ec = _achar(f, "Eclético")
    assert ec is not None
    assert ec.efeitos.get("acao_ativavel", {}).get("custo_pm") == 1


def test_bardo_artista_completo_nivel_20():
    f = _bardo(nivel=20)
    atualizar_ficha(f)
    ac = _achar(f, "Artista Completo")
    assert ac is not None
    assert ac.efeitos.get("artista_completo") is True
    assert ac.efeitos.get("inspiracao_acao_livre") is True
    assert ac.efeitos.get("reducao_custo_inspiracao_metade") is True


# ===================================================================
# 3. Círculos e limite de magias conhecidas
# ===================================================================

@pytest.mark.parametrize("nivel,circulo_esperado", [
    (1, 1),
    (5, 1),
    (6, 2),
    (9, 2),
    (10, 3),
    (13, 3),
    (14, 4),
    (20, 4),
])
def test_bardo_circulos_magia(nivel, circulo_esperado):
    f = _bardo(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.circulo_maximo == circulo_esperado


@pytest.mark.parametrize("nivel,limite_esperado", [
    (1, 2),   # 2 iniciais
    (2, 3),   # +1 (nv 2)
    (3, 3),   # ímpar não aprende
    (4, 4),   # +1 (nv 4)
    (10, 7),  # 2 + 5 pares
    (20, 12), # 2 + 10 pares
])
def test_bardo_limite_magias_conhecidas(nivel, limite_esperado):
    f = _bardo(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.limite_magias == limite_esperado
