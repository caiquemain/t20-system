"""Nobre — testes de classe base, Autoconfiança, Palavras Afiadas, Presença Aristocrática e Realeza (T20 JdA p.78-80)."""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Item
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _nobre(nivel=1, con=2, des=1, car=4, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Ayleth", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Nobre", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, destreza=des, carisma=car)
    f.atributos = f.atributos_base.model_copy()
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


@pytest.mark.parametrize("nivel,esperado", [
    (1, 18),   # 16 + 2
    (2, 24),   # 18 + 1*(4+2)
    (5, 42),   # 18 + 4*(4+2)
    (10, 72),  # 18 + 9*(4+2)
])
def test_nobre_pv_por_nivel(nivel, esperado):
    f = _nobre(nivel=nivel, con=2)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 4), (5, 20), (20, 80)])
def test_nobre_pm_por_nivel(nivel, esperado):
    f = _nobre(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_nobre_pericias_e_proficiencias():
    f = _nobre()
    atualizar_ficha(f)
    assert f.pericias["Vontade"].treino == 1
    assert "Armas Marciais" in f.status.proficiencias
    assert "Armaduras Pesadas" in f.status.proficiencias
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Nobre"]
    assert dc["pericias_fixas_selecao"] == ["Diplomacia", "Intimidação"]
    assert dc["pericias_escolha"] == 4
    assert len(dc["pericias_lista"]) == 18


def test_autoconfianca_usa_car_sem_armadura_pesada():
    # Sem armadura pesada: Car(4) substitui Des(1) -> Defesa = 10 + 4 = 14
    f_sem = _nobre(nivel=1, des=1, car=4)
    atualizar_ficha(f_sem)
    assert f_sem.status.defesa.total == 14

    # Com armadura pesada (Armadura completa +10): não soma Car -> 10 + 10 = 20
    f_pesada = _nobre(nivel=1, des=1, car=4, itens=["Armadura completa"])
    atualizar_ficha(f_pesada)
    assert f_pesada.status.defesa.total == 20


@pytest.mark.parametrize("nivel,formula_esp,custo_esp", [
    (2, "2d6", 1),
    (5, "2d6", 1),
    (6, "4d6", 2),
    (10, "6d6", 3),
    (14, "8d6", 4),
    (18, "10d6", 5),
    (20, "10d6", 5),
])
def test_palavras_afiadas_escala_tabela(nivel, formula_esp, custo_esp):
    f = _nobre(nivel=nivel, car=4)
    atualizar_ficha(f)
    pa = f.combate.nobre_calc["palavras_afiadas"]
    assert pa["formula"] == formula_esp
    assert pa["custo_max"] == custo_esp


def test_presenca_aristocratica_e_realeza_cd():
    f5 = _nobre(nivel=5, car=4)
    atualizar_ficha(f5)
    assert f5.combate.nobre_calc["presenca_aristocratica_cd"] == 16  # 10 + 2 + 4

    f20 = _nobre(nivel=20, car=5)
    atualizar_ficha(f20)
    assert f20.combate.nobre_calc["presenca_aristocratica_cd"] == 30  # 10 + 10 + 5 + 5 (Realeza)
    assert f20.combate.nobre_calc["realeza"] is True
