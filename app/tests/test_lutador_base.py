"""Lutador — testes de classe base, Briga, Casca Grossa, Golpe Cruel/Violento e Dono da Rua (T20 JdA p.75-77)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Item
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _lutador(nivel=1, forca=4, des=2, con=3, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Maquius", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Lutador", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(forca=forca, destreza=des, constituicao=con)
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
def test_lutador_pv_por_nivel(nivel, esperado):
    f = _lutador(nivel=nivel, con=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 3), (5, 15), (20, 60)])
def test_lutador_pm_por_nivel(nivel, esperado):
    f = _lutador(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_lutador_pericias_e_proficiencias():
    f = _lutador()
    atualizar_ficha(f)
    assert f.pericias["Fortitude"].treino == 1
    assert f.pericias["Luta"].treino == 1
    dc = DADOS_CLASSES["Lutador"]
    assert dc["pericias_escolha"] == 4
    assert len(dc["pericias_lista"]) == 11
    assert dc["proficiencias"] == []


@pytest.mark.parametrize("nivel,dado_esp,margem_esp,mult_esp", [
    (1, "1d6", 20, 2),
    (5, "1d8", 19, 2),
    (9, "1d10", 19, 3),
    (13, "2d6", 19, 3),
    (17, "2d8", 19, 3),
    (20, "2d10", 19, 3),
])
def test_briga_escala_tabela(nivel, dado_esp, margem_esp, mult_esp):
    f = _lutador(nivel=nivel)
    atualizar_ficha(f)
    bc = f.combate.briga_calc
    assert bc is not None
    assert bc["dado"] == dado_esp
    assert bc["margem_ameaca"] == margem_esp
    assert bc["multiplicador"] == mult_esp
    assert bc["dono_da_rua"] is (nivel >= 20)


@pytest.mark.parametrize("nivel,defesa_esp", [
    (3, 15),   # 10 + Des(2) + Con(3)
    (6, 15),   # 10 + 2 + 3
    (7, 16),   # 10 + 2 + 3 + 1
    (11, 17),  # 10 + 2 + 3 + 2
    (15, 18),  # 10 + 2 + 3 + 3
    (19, 19),  # 10 + 2 + 3 + 4
])
def test_casca_grossa_escala_defesa(nivel, defesa_esp):
    f = _lutador(nivel=nivel, des=2, con=3)
    atualizar_ficha(f)
    assert f.status.defesa.total == defesa_esp


def test_casca_grossa_bloqueada_por_armadura_pesada():
    f_pesada = _lutador(nivel=11, des=2, con=3, itens=["Armadura completa"])
    atualizar_ficha(f_pesada)
    # 10 + 10 (Armadura completa), sem Des e sem Casca Grossa
    assert f_pesada.status.defesa.total == 20
