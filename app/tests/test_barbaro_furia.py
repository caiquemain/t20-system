"""Bárbaro — Fúria (T20 JdA p.41).

Regras (livro):
    Fúria (1º): 2 PM → +2 ataque/dano corpo a corpo.
    A cada 5 níveis, +1 PM para aumentar bônus em +1:
        Nv 1-5  = +2 (2 PM)
        Nv 6-10 = +3 (3 PM)
        Nv 11-15 = +4 (4 PM)
        Nv 16-20 = +5 (5 PM)
    Fúria Titânica (20º): dobra o bônus (ex.: +10 com 5 PM).

Custo declarado em 'acao_ativavel' (padrão do catálogo do Bárbaro).
NOTA: o motor precisa expor o bônus calculado para a UI somar no ataque.
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade
from src.regras import atualizar_ficha


def _barbaro(nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Barb", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Bárbaro", nivel=nivel, primaria=True)]
    f.atributos_base = Atributos(constituicao=3, forca=4)
    f.atributos = f.atributos_base.model_copy()
    return f


def _achar(f, nome):
    return next((h for h in f.habilidades if nome in (h.nome or "")), None)


def _ativavel_de(hab):
    """Extrai o dict de ativação, aceitando os dois padrões do projeto."""
    efeitos = hab.efeitos or {}
    return efeitos.get("acao_ativavel") or efeitos.get("habilidade_ativavel")


# ===================================================================
# 1. Catálogo — estrutura de Fúria
# ===================================================================

def test_furia_catalogo_estrutura():
    """Fúria deve ter custo_pm, ataque_bonus, dano_bonus e escala_nivel."""
    f = _barbaro(nivel=1)
    atualizar_ficha(f)
    furia = _achar(f, "Fúria")
    assert furia is not None, "Fúria ausente"
    ativavel = _ativavel_de(furia)
    assert ativavel is not None, (
        f"Fúria sem campo de ativação. Efeitos: {furia.efeitos}"
    )
    for chave in ("custo_pm", "ataque_bonus", "dano_bonus"):
        assert chave in ativavel, (
            f"Fúria.{chave} ausente em {ativavel}"
        )
    assert ativavel["custo_pm"] == 2
    assert ativavel["ataque_bonus"] == 2
    assert ativavel["dano_bonus"] == 2


def test_furia_tem_escala_de_nivel():
    """Escala: +1 bônus a cada 5 níveis."""
    f = _barbaro(nivel=1)
    atualizar_ficha(f)
    furia = _achar(f, "Fúria")
    ativavel = _ativavel_de(furia)
    escala = ativavel.get("escala_nivel")
    assert isinstance(escala, dict), f"Fúria sem escala_nivel: {ativavel}"
    assert escala.get("cada") == 5
    assert escala.get("bonus") == 1


# ===================================================================
# 2. Motor — expõe o bônus de Fúria calculado
# ===================================================================

@pytest.mark.parametrize("nivel,esperado_bonus,esperado_custo", [
    (1, 2, 2),
    (5, 2, 2),
    (6, 3, 3),
    (10, 3, 3),
    (11, 4, 4),
    (15, 4, 4),
    (16, 5, 5),
    (19, 5, 5),   # ultimo nivel sem Furia Titanica
])
def test_furia_bonus_e_custo_escalam(nivel, esperado_bonus, esperado_custo):
    """Motor deve expor o bônus/custo ativo de Fúria por nível.

    Nv 1 = +2 ataque/dano, custo 2 PM.
    A cada 5 níveis: +1 no bônus e +1 no custo.
    Nv 20 e coberto por test_furia_titanica_dobra_bonus_nivel_20.
    """
    f = _barbaro(nivel=nivel)
    atualizar_ficha(f)
    ativavel_calc = getattr(f.combate, "furia_calc", None)
    assert ativavel_calc is not None, (
        f"Nível {nivel}: combate.furia_calc ausente. "
        f"Motor precisa expor o cálculo de Fúria para a UI."
    )
    # Aceita dict {"bonus": X, "custo": Y} ou objeto com atributos
    if isinstance(ativavel_calc, dict):
        assert ativavel_calc.get("bonus") == esperado_bonus, (
            f"Nível {nivel}: bônus esperado {esperado_bonus}, "
            f"obtido {ativavel_calc.get('bonus')}"
        )
        assert ativavel_calc.get("custo") == esperado_custo, (
            f"Nível {nivel}: custo esperado {esperado_custo}, "
            f"obtido {ativavel_calc.get('custo')}"
        )
    else:
        assert getattr(ativavel_calc, "bonus", None) == esperado_bonus
        assert getattr(ativavel_calc, "custo", None) == esperado_custo


# ===================================================================
# 3. Fúria Titânica — dobra o bônus
# ===================================================================

def test_furia_titanica_dobra_bonus_nivel_20():
    """Fúria Titânica dobra o bônus. Nv 20 = +5 base → +10."""
    f = _barbaro(nivel=20)
    atualizar_ficha(f)
    ativavel_calc = getattr(f.combate, "furia_calc", None)
    assert ativavel_calc is not None, "combate.furia_calc ausente no nível 20"
    if isinstance(ativavel_calc, dict):
        assert ativavel_calc.get("bonus") == 10, (
            f"Fúria Titânica deveria dobrar +5 → +10. "
            f"Obtido: {ativavel_calc.get('bonus')}"
        )
    else:
        assert getattr(ativavel_calc, "bonus", None) == 10


def test_furia_sem_titanica_nao_dobra():
    """Nível 19 não tem Fúria Titânica. Bônus = +5 (sem dobra)."""
    f = _barbaro(nivel=19)
    atualizar_ficha(f)
    ativavel_calc = getattr(f.combate, "furia_calc", None)
    assert ativavel_calc is not None
    if isinstance(ativavel_calc, dict):
        assert ativavel_calc.get("bonus") == 5, (
            f"Nível 19: bônus deveria ser +5 (sem Fúria Titânica). "
            f"Obtido: {ativavel_calc.get('bonus')}"
        )
    else:
        assert getattr(ativavel_calc, "bonus", None) == 5
