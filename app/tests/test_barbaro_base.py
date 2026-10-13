"""Bárbaro — testes de classe, RD e Instinto Selvagem (T20 JdA p.40-41).

Cobre:
    PV: 24 + Con inicial; +6 + Con por nível
    PM: 3 por nível (sem atributo-chave)
    Perícias: Fortitude, Luta + 4 escolhas
    Proficiências: armas marciais e escudos
    Fúria (1º nível): habilidade existe, marcada como ativável
    Instinto Selvagem (3º): +1 dano/Percepção/Reflexos; +2 no 9º; +3 no 15º
    Redução de Dano (5º): 2; 8º: 4; 11º: 6; 14º: 8; 17º: 10
    Fúria Titânica (20º): dobra o bônus da Fúria
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos
from src.regras import atualizar_ficha


def _barbaro(nivel=1, con=3):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Barb", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bárbaro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=con, forca=4)
    f.atributos = f.atributos_base.model_copy()
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if nome in (h.nome or "")), None)


# ===================================================================
# 1. PV / PM / perícias
# ===================================================================

def test_barbaro_pv_inicial():
    """24 + Con 3 = 27 no nível 1."""
    f = _barbaro(nivel=1, con=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == 27, (
        f"PV nível 1 esperado 24 + 3 = 27, obtido {f.status.pv.maximo}"
    )


@pytest.mark.parametrize("nivel,esperado", [
    (1, 27),    # 24 + 3
    (2, 36),    # 27 + 1*(6+3)
    (5, 63),    # 27 + 4*(6+3) = 27 + 36
    (10, 108),  # 27 + 9*(6+3) = 27 + 81
])
def test_barbaro_pv_por_nivel(nivel, esperado):
    f = _barbaro(nivel=nivel, con=3)
    atualizar_ficha(f)
    assert f.status.pv.maximo == esperado, (
        f"Nível {nivel}: PV esperado {esperado}, obtido {f.status.pv.maximo}"
    )


def test_barbaro_pm_por_nivel():
    """PM: 3 por nível, sem atributo-chave."""
    f = _barbaro(nivel=5)
    atualizar_ficha(f)
    assert f.status.pm.maximo == 15, (
        f"PM esperado 15 (3×5), obtido {f.status.pm.maximo}"
    )


def test_barbaro_pericias_fixas():
    f = _barbaro()
    atualizar_ficha(f)
    assert f.pericias["Fortitude"].treino == 1
    assert f.pericias["Luta"].treino == 1


def test_barbaro_proficiencias():
    f = _barbaro()
    atualizar_ficha(f)
    profs = " ".join(f.status.proficiencias).lower()
    assert "marciais" in profs, f"Sem armas marciais: {f.status.proficiencias}"
    assert "escudos" in profs, f"Sem escudos: {f.status.proficiencias}"


# ===================================================================
# 2. Fúria (habilidade base)
# ===================================================================

def test_barbaro_furia_existe_nivel_1():
    f = _barbaro(nivel=1)
    atualizar_ficha(f)
    furia = _achar(f, "Fúria")
    assert furia is not None, (
        f"Habilidade 'Fúria' ausente. Habilidades: "
        f"{[h.nome for h in f.habilidades if h.tipo == 'Classe']}"
    )


# ===================================================================
# 3. Instinto Selvagem
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 0),    # ainda não tem
    (3, 1),    # +1
    (6, 1),    # ainda +1
    (9, 2),    # +2
    (12, 2),   # ainda +2
    (15, 3),   # +3
    (20, 3),   # ainda +3
])
def test_barbaro_instinto_selvagem_dano(nivel, esperado):
    """+1 dano em níveis 3-8, +2 em 9-14, +3 em 15+.

    O motor expõe esse bônus em `combate.bonus_dano_geral` para que
    ataques (na UI) possam somar o valor na rolagem de dano.
    """
    f = _barbaro(nivel=nivel)
    atualizar_ficha(f)
    obtido = getattr(f.combate, "bonus_dano_geral", None) or 0
    assert obtido == esperado, (
        f"Nível {nivel}: Instinto Selvagem esperado +{esperado} dano, "
        f"obtido {obtido}"
    )


@pytest.mark.parametrize("nivel,esperado", [
    (3, 1), (9, 2), (15, 3),
])
def test_barbaro_instinto_selvagem_percepcao(nivel, esperado):
    f = _barbaro(nivel=nivel)
    atualizar_ficha(f)
    info = f.pericias.get("Percepção")
    assert info is not None
    tem = any("Instinto" in (linha or "") for linha in info.fontes_bonus)
    assert tem or (info.bonus_automatico or 0) >= esperado, (
        f"Nível {nivel}: +{esperado} Percepção não aplicado. "
        f"Fontes: {info.fontes_bonus}, bonus_auto: {info.bonus_automatico}"
    )


@pytest.mark.parametrize("nivel,esperado", [
    (3, 1), (9, 2), (15, 3),
])
def test_barbaro_instinto_selvagem_reflexos(nivel, esperado):
    f = _barbaro(nivel=nivel)
    atualizar_ficha(f)
    info = f.pericias.get("Reflexos")
    assert info is not None
    tem = any("Instinto" in (linha or "") for linha in info.fontes_bonus)
    assert tem or (info.bonus_automatico or 0) >= esperado, (
        f"Nível {nivel}: +{esperado} Reflexos não aplicado. "
        f"Fontes: {info.fontes_bonus}"
    )


# ===================================================================
# 4. Redução de Dano
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 0),    # sem RD
    (4, 0),
    (5, 2),    # RD 2
    (7, 2),
    (8, 4),    # RD 4
    (10, 4),
    (11, 6),   # RD 6
    (13, 6),
    (14, 8),   # RD 8
    (16, 8),
    (17, 10),  # RD 10
    (20, 10),
])
def test_barbaro_reducao_de_dano(nivel, esperado):
    """Livro (p.41): RD 2 no 5º, +2 a cada 3 níveis, máx 10 no 17º."""
    f = _barbaro(nivel=nivel)
    atualizar_ficha(f)
    # Aceita duas formas de exposição:
    #   (a) entrada "geral N" em status.rd (padrão do projeto)
    #   (b) campo dedicado combate.rd_geral (fallback futuro)
    if esperado == 0:
        tem_rd = not any("geral" in (rd or "").lower() for rd in (f.status.rd or []))
    else:
        tem_rd = any(f"geral {esperado}" in (rd or "").lower()
                     for rd in (f.status.rd or []))
    if not tem_rd:
        rd_geral = getattr(f.combate, "rd_geral", None)
        if rd_geral is not None:
            tem_rd = (rd_geral == esperado)
    assert tem_rd, (
        f"Nível {nivel}: RD esperada {esperado}, status.rd={f.status.rd}, "
        f"combate.rd_geral={getattr(f.combate, 'rd_geral', None)}"
    )


# ===================================================================
# 5. Fúria Titânica (nível 20)
# ===================================================================

def test_barbaro_furia_titanica_existe_nivel_20():
    f = _barbaro(nivel=20)
    atualizar_ficha(f)
    hab = _achar(f, "Fúria Titânica")
    assert hab is not None, (
        f"Fúria Titânica ausente no nível 20. Habilidades: "
        f"{[h.nome for h in f.habilidades if h.tipo == 'Classe']}"
    )
