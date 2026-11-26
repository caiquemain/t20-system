"""Cavaleiro — testes de classe base, Baluarte, Duelo e Caminho do Cavaleiro (T20 JdA p.52-55).

Cobre:
    PV: 20 + Con inicial; +5 + Con por nível
    PM: 3 por nível
    Perícias: Fortitude, Luta + 2 escolhas (10 opções)
    Proficiências: Armas Marciais, Armaduras Pesadas, Escudos
    Habilidades fixas: Código de Honra (1º), Baluarte (1º), Duelo (2º),
        Caminho do Cavaleiro (5º), Resoluto (11º), Bravura Final (20º)
    Baluarte: +2 (1º), +4 (5º), +6 (9º), +8 (13º), +10 (17º); aliados adj (7º), curto (15º)
    Duelo: +2 (2º), +3 (7º), +4 (12º), +5 (17º)
    Bastião + Especialização em Armadura: RD 5 e RD 10 acumulativas de armadura pesada
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Item, Habilidade
from src.dados_classes import DADOS_CLASSES
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.regras import atualizar_ficha


def _cavaleiro(nivel=1, con=3, forca=3, car=2, subclasse="", itens=None, poderes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Orion", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Cavaleiro", nivel=nivel, primaria=True, subclasse=subclasse)]
    f.atributos_base = Atributos(constituicao=con, forca=forca, carisma=car)
    f.atributos = f.atributos_base.model_copy()
    for nome_item in (itens or []):
        f.inventario.equipamentos.append(Item(nome=nome_item, equipado=True))
    for chave in (poderes or []):
        d = DADOS_HABILIDADES_CLASSE[chave]
        f.habilidades.append(Habilidade(
            nome=d["nome"],
            tipo=d["tipo"],
            descricao=d["descricao"],
            efeitos=dict(d.get("efeitos", {})),
            fonte="Poder de Cavaleiro",
        ))
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if (h.nome or "") == nome), None)


# ===================================================================
# 1. PV / PM / Perícias / Proficiências
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 23),   # 20 + 3
    (2, 31),   # 23 + 1*(5+3)
    (5, 55),   # 23 + 4*(5+3)
    (10, 95),  # 23 + 9*(5+3)
])
def test_cavaleiro_pv_por_nivel(nivel, esperado):
    f = _cavaleiro(nivel=nivel, con=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 3), (5, 15), (20, 60)])
def test_cavaleiro_pm_por_nivel(nivel, esperado):
    f = _cavaleiro(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_cavaleiro_pericias_e_proficiencias():
    f = _cavaleiro()
    atualizar_ficha(f)
    assert f.pericias["Fortitude"].treino == 1
    assert f.pericias["Luta"].treino == 1
    assert "Armas Marciais" in f.status.proficiencias
    assert "Armaduras Pesadas" in f.status.proficiencias
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Cavaleiro"]
    assert dc["pericias_escolha"] == 2
    assert len(dc["pericias_lista"]) == 10


# ===================================================================
# 2. Habilidades fixas por nível
# ===================================================================

def test_cavaleiro_habilidades_fixas_progressao():
    f1 = _cavaleiro(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Código de Honra") is not None
    assert _achar(f1, "Baluarte") is not None
    assert _achar(f1, "Duelo") is None

    f5 = _cavaleiro(nivel=5)
    atualizar_ficha(f5)
    assert _achar(f5, "Duelo") is not None
    assert _achar(f5, "Caminho do Cavaleiro") is not None
    assert _achar(f5, "Resoluto") is None

    f11 = _cavaleiro(nivel=11)
    atualizar_ficha(f11)
    assert _achar(f11, "Resoluto") is not None
    assert _achar(f11, "Bravura Final") is None

    f20 = _cavaleiro(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Bravura Final") is not None


# ===================================================================
# 3. Baluarte e Duelo (Tabela 1-10)
# ===================================================================

@pytest.mark.parametrize("nivel,bal_bonus,bal_custo,adj,curto", [
    (1, 2, 1, False, False),
    (5, 4, 2, False, False),
    (7, 4, 2, True, False),
    (9, 6, 3, True, False),
    (13, 8, 4, True, False),
    (15, 8, 4, True, True),
    (17, 10, 5, True, True),
])
def test_baluarte_escala_tabela(nivel, bal_bonus, bal_custo, adj, curto):
    f = _cavaleiro(nivel=nivel)
    atualizar_ficha(f)
    bal = f.combate.cavaleiro_calc["baluarte"]
    assert bal["bonus"] == bal_bonus
    assert bal["custo"] == bal_custo
    assert bal["aliados_adjacentes"] is adj
    assert bal["aliados_alcance_curto"] is curto


@pytest.mark.parametrize("nivel,duelo_esperado", [
    (1, None),
    (2, {"bonus": 2, "custo": 2}),
    (6, {"bonus": 2, "custo": 2}),
    (7, {"bonus": 3, "custo": 3}),
    (12, {"bonus": 4, "custo": 4}),
    (17, {"bonus": 5, "custo": 5}),
    (20, {"bonus": 5, "custo": 5}),
])
def test_duelo_escala_tabela(nivel, duelo_esperado):
    f = _cavaleiro(nivel=nivel)
    atualizar_ficha(f)
    assert f.combate.cavaleiro_calc["duelo"] == duelo_esperado


# ===================================================================
# 4. Bastião + Especialização em Armadura (RD 5 / RD 10 acumulativa)
# ===================================================================

def test_bastiao_e_especializacao_em_armadura_acumulam_rd():
    # Sem armadura pesada: sem RD
    f_sem = _cavaleiro(nivel=12, subclasse="Bastião", poderes=["CAVALEIRO_ESPECIALIZACAO_ARMADURA"])
    atualizar_ficha(f_sem)
    assert "geral 5" not in f_sem.status.rd
    assert "geral 10" not in f_sem.status.rd

    # Bastião com Armadura completa: RD 5
    f_bast = _cavaleiro(nivel=5, subclasse="Bastião", itens=["Armadura completa"])
    atualizar_ficha(f_bast)
    assert "geral 5" in f_bast.status.rd

    # Bastião + Especialização em Armadura com Armadura completa: RD 10
    f_ambos = _cavaleiro(
        nivel=12, subclasse="Bastião",
        itens=["Armadura completa"],
        poderes=["CAVALEIRO_ESPECIALIZACAO_ARMADURA"],
    )
    atualizar_ficha(f_ambos)
    assert "geral 10" in f_ambos.status.rd
