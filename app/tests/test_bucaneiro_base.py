"""Bucaneiro — testes de classe base, Insolência e Esquiva Sagaz (T20 JdA p.46-48).

Cobre:
    PV: 16 + Con inicial; +4 + Con por nível
    PM: 3 por nível
    Perícias: Reflexos, Luta ou Pontaria + 4 escolhas (14 opções)
    Proficiências: Armas Marciais
    Habilidades fixas: Audácia (1º), Insolência (1º), Evasão (2º),
        Esquiva Sagaz (3º), Panache (5º), Evasão Aprimorada (10º), Sorte de Nimb (20º)
    Insolência: +Car na Defesa limitado pelo nível; bloqueada por armadura pesada ou imóvel
    Esquiva Sagaz: +1 Defesa/Reflexos no 3º; +2 (7º), +3 (11º), +4 (15º), +5 (19º); bloqueada sem liberdade
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Item
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _bucaneiro(nivel=1, con=2, des=3, car=4, condicoes=None, itens=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Nargom", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bucaneiro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, destreza=des, carisma=car)
    f.atributos = f.atributos_base.model_copy()
    if condicoes:
        f.condicoes_ativas = list(condicoes)
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


# ===================================================================
# 1. PV / PM / Perícias / Proficiências
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 18),   # 16 + 2
    (2, 24),   # 18 + 1*(4+2)
    (5, 42),   # 18 + 4*(4+2)
    (10, 72),  # 18 + 9*(4+2)
])
def test_bucaneiro_pv_por_nivel(nivel, esperado):
    f = _bucaneiro(nivel=nivel, con=2)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 3), (5, 15), (20, 60)])
def test_bucaneiro_pm_por_nivel(nivel, esperado):
    f = _bucaneiro(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_bucaneiro_pericias_e_proficiencias():
    f = _bucaneiro()
    atualizar_ficha(f)
    assert f.pericias["Reflexos"].treino == 1
    assert "Armas Marciais" in f.status.proficiencias

    dc = DADOS_CLASSES["Bucaneiro"]
    assert dc["pericias_escolha"] == 4
    assert dc["pericias_fixas_selecao"] == ["Luta", "Pontaria"]
    assert len(dc["pericias_lista"]) == 14


# ===================================================================
# 2. Habilidades fixas por nível
# ===================================================================

def test_bucaneiro_habilidades_fixas_progressao():
    f1 = _bucaneiro(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Audácia") is not None
    assert _achar(f1, "Insolência") is not None
    assert _achar(f1, "Evasão") is None

    f2 = _bucaneiro(nivel=2)
    atualizar_ficha(f2)
    assert _achar(f2, "Evasão") is not None
    assert _achar(f2, "Esquiva Sagaz") is None

    f5 = _bucaneiro(nivel=5)
    atualizar_ficha(f5)
    assert _achar(f5, "Esquiva Sagaz") is not None
    assert _achar(f5, "Panache") is not None
    assert _achar(f5, "Evasão Aprimorada") is None

    f10 = _bucaneiro(nivel=10)
    atualizar_ficha(f10)
    assert _achar(f10, "Evasão Aprimorada") is not None
    assert _achar(f10, "Sorte de Nimb") is None

    f20 = _bucaneiro(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Sorte de Nimb") is not None


# ===================================================================
# 3. Insolência (Car na Defesa limitado pelo nível + liberdade de mov.)
# ===================================================================

def test_insolencia_limitada_pelo_nivel():
    # Nível 1 com Des 3 e Car 4: Defesa = 10 + 3 (Des) + 1 (Insolência limitada ao nv 1) = 14
    f1 = _bucaneiro(nivel=1, des=3, car=4)
    atualizar_ficha(f1)
    assert f1.status.defesa.total == 14

    # Nível 2 com Des 3 e Car 4: Defesa = 10 + 3 + 2 = 15
    f2 = _bucaneiro(nivel=2, des=3, car=4)
    atualizar_ficha(f2)
    assert f2.status.defesa.total == 15

    # Nível 6 com Des 3 e Car 4: Defesa = 10 + 3 (Des) + 4 (Insolência) + 1 (Esquiva Sagaz) = 18
    f6 = _bucaneiro(nivel=6, des=3, car=4)
    atualizar_ficha(f6)
    assert f6.status.defesa.total == 18


def test_insolencia_e_esquiva_sagaz_bloqueadas_por_imovel_ou_armadura_pesada():
    # Condição "imovel": perde Insolência (+4) e Esquiva Sagaz (+2 no nv 7), mantém Des (+3) -> 13
    f_imovel = _bucaneiro(nivel=7, des=3, car=4, condicoes=["imovel"])
    atualizar_ficha(f_imovel)
    assert f_imovel.status.defesa.total == 13
    assert all("Esquiva Sagaz" not in s for s in f_imovel.pericias["Reflexos"].fontes_bonus)

    # Armadura completa (pesada, +10 Defesa): perde Des, Insolência e Esquiva Sagaz -> 10 + 10 = 20
    f_pesada = _bucaneiro(nivel=7, des=3, car=4, itens=["Armadura completa"])
    atualizar_ficha(f_pesada)
    assert f_pesada.status.defesa.total == 20
    assert all("Esquiva Sagaz" not in s for s in f_pesada.pericias["Reflexos"].fontes_bonus)


# ===================================================================
# 4. Esquiva Sagaz (escala a cada 4 níveis em Defesa e Reflexos)
# ===================================================================

@pytest.mark.parametrize("nivel,bonus_esp", [
    (3, 1),
    (6, 1),
    (7, 2),
    (10, 2),
    (11, 3),
    (15, 4),
    (19, 5),
    (20, 5),
])
def test_esquiva_sagaz_escala_defesa_e_reflexos(nivel, bonus_esp):
    f = _bucaneiro(nivel=nivel, des=2, car=0)
    atualizar_ficha(f)
    # Defesa = 10 + Des(2) + Esquiva Sagaz(bonus_esp)
    assert f.status.defesa.total == 10 + 2 + bonus_esp
    # Reflexos = floor(nivel/2) + Des(2) + treino(2/4/6) + Esquiva Sagaz(bonus_esp)
    treino = 2 if nivel < 7 else (4 if nivel < 15 else 6)
    assert f.pericias["Reflexos"].total == (nivel // 2) + 2 + treino + bonus_esp
