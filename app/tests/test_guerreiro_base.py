"""Guerreiro — testes de classe base, Ataque Especial, Durão, Ataque Extra e Campeão (T20 JdA p.64-66)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Item
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _guerreiro(nivel=1, con=3, forca=4, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Val", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, forca=forca)
    f.atributos = f.atributos_base.model_copy()
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


@pytest.mark.parametrize("nivel,esperado", [
    (1, 23),   # 20 + 3
    (2, 31),   # 23 + 1*(5+3)
    (5, 55),   # 23 + 4*(5+3)
    (10, 95),  # 23 + 9*(5+3)
])
def test_guerreiro_pv_por_nivel(nivel, esperado):
    f = _guerreiro(nivel=nivel, con=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 3), (5, 15), (20, 60)])
def test_guerreiro_pm_por_nivel(nivel, esperado):
    f = _guerreiro(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_guerreiro_pericias_e_proficiencias():
    f = _guerreiro()
    atualizar_ficha(f)
    assert f.pericias["Fortitude"].treino == 1
    assert "Armas Marciais" in f.status.proficiencias
    assert "Armaduras Pesadas" in f.status.proficiencias
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Guerreiro"]
    assert dc["pericias_escolha"] == 2
    assert dc["pericias_fixas_selecao"] == ["Luta", "Pontaria"]
    assert len(dc["pericias_lista"]) == 11
    assert "Vontade" not in dc["pericias_lista"]


def test_guerreiro_habilidades_fixas_progressao():
    f1 = _guerreiro(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Ataque Especial") is not None
    assert _achar(f1, "Durão") is None

    f3 = _guerreiro(nivel=3)
    atualizar_ficha(f3)
    assert _achar(f3, "Durão") is not None
    assert _achar(f3, "Ataque Extra") is None

    f6 = _guerreiro(nivel=6)
    atualizar_ficha(f6)
    assert _achar(f6, "Ataque Extra") is not None
    assert _achar(f6, "Campeão") is None

    f20 = _guerreiro(nivel=20, itens=["Espada longa"])
    atualizar_ficha(f20)
    assert _achar(f20, "Campeão") is not None
    assert "Campeão (+1 passo de dano)" in f20.combate.ataques[0].especial


@pytest.mark.parametrize("nivel,bonus_esp,custo_esp", [
    (1, 4, 1),
    (4, 4, 1),
    (5, 8, 2),
    (8, 8, 2),
    (9, 12, 3),
    (12, 12, 3),
    (13, 16, 4),
    (16, 16, 4),
    (17, 20, 5),
    (20, 20, 5),
])
def test_ataque_especial_escala_tabela(nivel, bonus_esp, custo_esp):
    f = _guerreiro(nivel=nivel)
    atualizar_ficha(f)
    ae = f.combate.ataque_especial_calc
    assert ae is not None
    assert ae["bonus"] == bonus_esp
    assert ae["custo"] == custo_esp
    assert ae["campeao_recupera_metade"] is (nivel >= 20)
