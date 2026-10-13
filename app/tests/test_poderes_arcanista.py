"""Poderes de Arcanista - testes legacy (T20 p.37-38).

Reescrito apos fix da formula de CD (p.173):
    CD = 10 + metade do nivel + atributo-chave + bonus de poder

Historico: os testes originais esperavam CD = 10 + bonus (formula
incorreta), que foi corrigida no commit em que passamos a somar
nivel/2 e atributo-chave em poderes_arcanista.py.
"""
from unittest.mock import patch
from src.models import (
    Personagem, Cabecalho, ClasseInfo, Atributos, Habilidade, Status,
)
from src.regras.poderes_arcanista import aplicar_poderes_arcanista


def _ficha_arcanista(base: Personagem, nivel=1, subclasse="Mago"):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Arc", raca="Humano", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Arcanista", nivel=nivel,
                            primaria=True, subclasse=subclasse)]
    f.atributos_base = base.atributos_base.model_copy()
    f.atributos = base.atributos.model_copy()
    return f


def _hab(nome, escolhas=None):
    return Habilidade(
        nome=nome, tipo="Poder de Arcanista",
        escolhas_aplicadas=escolhas or {},
    )


def _cd_esperada(nivel: int, mod_int: int, bonus_poder: int = 0) -> int:
    """Formula oficial: 10 + floor(nivel/2) + mod_atributo + bonus."""
    import math
    return 10 + math.floor(nivel / 2) + mod_int + bonus_poder


# ===================================================================
# Fortalecimento Arcano
# ===================================================================

def test_fortalecimento_arcano_cd_bonus_padrao(personagem_base):
    """Nivel 5, Int 3, sem 4o circulo -> +1 CD."""
    f = _ficha_arcanista(personagem_base, nivel=5)
    f.atributos.inteligencia = 3
    f.combate.circulo_maximo = 2
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == _cd_esperada(5, 3, bonus_poder=1), (
        f"Esperado {_cd_esperada(5, 3, 1)}, obtido {f.combate.cd_magias}"
    )


def test_fortalecimento_arcano_cd_com_4_circulo(personagem_base):
    """Nivel 13, Int 3, 4o circulo disponivel -> +2 CD."""
    f = _ficha_arcanista(personagem_base, nivel=13)
    f.atributos.inteligencia = 3
    f.combate.circulo_maximo = 4
    f.habilidades = [_hab("Fortalecimento Arcano")]
    aplicar_poderes_arcanista(f)
    assert f.combate.cd_magias == _cd_esperada(13, 3, bonus_poder=2), (
        f"Esperado {_cd_esperada(13, 3, 2)}, obtido {f.combate.cd_magias}"
    )


# ===================================================================
# Poder Magico
# ===================================================================

def test_poder_magico_soma_pm_por_nivel(personagem_base):
    f = _ficha_arcanista(personagem_base, nivel=5)
    f.status.pm.maximo = 30
    f.habilidades = [_hab("Poder Mágico")]
    aplicar_poderes_arcanista(f)
    assert any(
        fr.fonte == "Poder Mágico" and fr.valor == 5
        for fr in (f.status.pm_calc.fontes if f.status.pm_calc else [])
    ), f"Poder Magico +5 PM nao apareceu. Fontes: {[x.fonte for x in (f.status.pm_calc.fontes if f.status.pm_calc else [])]}"


# ===================================================================
# Acumulacao de poderes
# ===================================================================

def test_multiplos_poderes_acumulam(personagem_base):
    """Poder Magico + Familiar (Sapo) + Fortalecimento aplicam juntos."""
    f = _ficha_arcanista(personagem_base, nivel=5)
    f.atributos.inteligencia = 3
    f.combate.circulo_maximo = 2
    f.habilidades = [
        _hab("Poder Mágico"),
        _hab("Fortalecimento Arcano"),
        _hab("Familiar", {"familiar": "Sapo"}),
    ]
    aplicar_poderes_arcanista(f)

    # PM: Poder Magico soma +5 (nivel da classe)
    assert any(
        "Poder Mágico" in (fr.fonte or "") and fr.valor == 5
        for fr in (f.status.pm_calc.fontes if f.status.pm_calc else [])
    ), "Poder Magico nao somou +5 PM"

    # CD: 10 + 2 (nivel 5) + 3 (Int) + 1 (Fortalecimento) = 16
    assert f.combate.cd_magias == _cd_esperada(5, 3, bonus_poder=1), (
        f"CD esperada {_cd_esperada(5, 3, 1)}, obtida {f.combate.cd_magias}"
    )
