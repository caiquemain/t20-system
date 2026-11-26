"""Caçador — testes de classe base, Marca da Presa, Rastreador e Explorador (T20 JdA p.49-51).

Cobre:
    PV: 16 + Con inicial; +4 + Con por nível
    PM: 4 por nível
    Perícias: Sobrevivência, Luta ou Pontaria + 6 escolhas (13 opções)
    Proficiências: Armas Marciais e Escudos
    Habilidades fixas: Marca da Presa (1º), Rastreador (1º), Explorador (3º),
        Caminho do Explorador (5º), Mestre Caçador (20º)
    Marca da Presa: 1d4 (1º), 1d8 (5º), 1d12 (9º), 2d8 (13º), 2d10 (17º); Livre no 20º
    Explorador: +Sab (mín +1) na Defesa e em Acrobacia, Atletismo, Furtividade, Percepção e Sobrevivência
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.dados_classes import DADOS_CLASSES
from src.regras import atualizar_ficha


def _cacador(nivel=1, con=2, des=3, sab=3, condicoes=None):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Enver", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Caçador", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, destreza=des, sabedoria=sab)
    f.atributos = f.atributos_base.model_copy()
    if condicoes:
        f.condicoes_ativas = list(condicoes)
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
def test_cacador_pv_por_nivel(nivel, esperado):
    f = _cacador(nivel=nivel, con=2)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado


@pytest.mark.parametrize("nivel,esperado", [(1, 4), (5, 20), (20, 80)])
def test_cacador_pm_por_nivel(nivel, esperado):
    f = _cacador(nivel=nivel)
    atualizar_ficha(f)
    assert f.status.pm.maximo == esperado


def test_cacador_pericias_e_proficiencias():
    f = _cacador(nivel=1, sab=3)
    atualizar_ficha(f)
    assert f.pericias["Sobrevivência"].treino == 1
    # Rastreador dá +2 em Sobrevivência: 0 (metade nv1) + 3 (Sab) + 2 (treino) + 2 (Rastreador) = 7
    assert f.pericias["Sobrevivência"].total == 7
    assert "Armas Marciais" in f.status.proficiencias
    assert "Escudos" in f.status.proficiencias

    dc = DADOS_CLASSES["Caçador"]
    assert dc["pericias_escolha"] == 6
    assert dc["pericias_fixas_selecao"] == ["Luta", "Pontaria"]
    assert len(dc["pericias_lista"]) == 13


# ===================================================================
# 2. Habilidades fixas por nível
# ===================================================================

def test_cacador_habilidades_fixas_progressao():
    f1 = _cacador(nivel=1)
    atualizar_ficha(f1)
    assert _achar(f1, "Marca da Presa") is not None
    assert _achar(f1, "Rastreador") is not None
    assert _achar(f1, "Explorador") is None

    f3 = _cacador(nivel=3)
    atualizar_ficha(f3)
    assert _achar(f3, "Explorador") is not None
    assert _achar(f3, "Caminho do Explorador") is None

    f5 = _cacador(nivel=5)
    atualizar_ficha(f5)
    assert _achar(f5, "Caminho do Explorador") is not None
    assert _achar(f5, "Mestre Caçador") is None

    f20 = _cacador(nivel=20)
    atualizar_ficha(f20)
    assert _achar(f20, "Mestre Caçador") is not None


# ===================================================================
# 3. Marca da Presa (Tabela 1-9)
# ===================================================================

@pytest.mark.parametrize("nivel,dado_esp,custo_esp", [
    (1, "1d4", 1),
    (4, "1d4", 1),
    (5, "1d8", 2),
    (8, "1d8", 2),
    (9, "1d12", 3),
    (12, "1d12", 3),
    (13, "2d8", 4),
    (16, "2d8", 4),
    (17, "2d10", 5),
    (20, "2d10", 5),
])
def test_marca_da_presa_escala_tabela(nivel, dado_esp, custo_esp):
    f = _cacador(nivel=nivel)
    atualizar_ficha(f)
    mp = f.combate.marca_presa_calc
    assert mp is not None
    assert mp["dado"] == dado_esp
    assert mp["custo_max"] == custo_esp
    assert mp["acao"] == ("Livre" if nivel >= 20 else "Movimento")
    assert mp["alcance"] == "Curto"
    assert mp["mestre_cacador"] is (nivel >= 20)


# ===================================================================
# 4. Explorador (terreno escolhido: +Sab mín +1 em Defesa e 5 perícias)
# ===================================================================

def test_explorador_aplica_bonus_em_terreno():
    f_fora = _cacador(nivel=3, des=2, sab=3, condicoes=[])
    atualizar_ficha(f_fora)

    f_dentro = _cacador(nivel=3, des=2, sab=3, condicoes=["terreno_explorador"])
    atualizar_ficha(f_dentro)

    assert f_dentro.status.defesa.total == f_fora.status.defesa.total + 3
    for p in ("Acrobacia", "Atletismo", "Furtividade", "Percepção", "Sobrevivência"):
        assert f_dentro.pericias[p].total == f_fora.pericias[p].total + 3

    # Sabedoria 0 ainda garante mínimo +1
    f_sab0_fora = _cacador(nivel=3, des=2, sab=0, condicoes=[])
    atualizar_ficha(f_sab0_fora)
    f_sab0_dentro = _cacador(nivel=3, des=2, sab=0, condicoes=["terreno_explorador"])
    atualizar_ficha(f_sab0_dentro)
    assert f_sab0_dentro.status.defesa.total == f_sab0_fora.status.defesa.total + 1
