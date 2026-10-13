"""Testes de modificador de Furtividade por tamanho (T20 JdA p.106).

Tabela 1-4 (Categoria de Tamanho):
    Minúsculo +5, Pequeno +2, Médio 0, Grande -2, Enorme -5, Colossal -10.
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, TamanhoEnum
from src.regras import atualizar_ficha
from src.regras.habilidades import garantir_habilidades_iniciais
from src.regras.pericias import inicializar_pericias


def _ficha(tamanho: TamanhoEnum):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Furtivo", raca="Humano", nivel_total=1)
    f.classes = [ClasseInfo(nome="Ladino", nivel=1, primaria=True)]
    f.descricao.tamanho = tamanho
    return f


def _bonus_tamanho_furtividade(f):
    """Extrai da StatCalculado de Furtividade a fonte com sinal de tamanho."""
    info = f.pericias.get("Furtividade")
    if not info or not info.calculo:
        return None
    for fnt in info.calculo.fontes:
        if "Tamanho" in (fnt.fonte or ""):
            return fnt.valor
    return 0


@pytest.mark.parametrize("tamanho,esperado", [
    (TamanhoEnum.MINUSCULO, 5),
    (TamanhoEnum.PEQUENO, 2),
    (TamanhoEnum.MEDIO, 0),
    (TamanhoEnum.GRANDE, -2),
    (TamanhoEnum.ENORME, -5),
    (TamanhoEnum.COLOSSAL, -10),
])
def test_furtividade_por_tamanho(tamanho, esperado):
    f = _ficha(tamanho)
    garantir_habilidades_iniciais(f)
    inicializar_pericias(f)
    obtido = _bonus_tamanho_furtividade(f)
    assert obtido == esperado, (
        f"{tamanho.value}: Furtividade deveria ter {esperado:+d}, obteve {obtido}. "
        f"Livro p.106, Tabela de Categoria de Tamanho."
    )


# ---- Integração: cada raça cobre seu caso real ----

@pytest.mark.parametrize("raca,tamanho_esperado,mod_esperado", [
    ("Sílfide", TamanhoEnum.MINUSCULO, 5),
    ("Goblin", TamanhoEnum.PEQUENO, 2),
    ("Hynne", TamanhoEnum.PEQUENO, 2),
])
def test_racas_com_tamanho_nao_medio_recebem_modificador(raca, tamanho_esperado, mod_esperado):
    f = Personagem()
    f.cabecalho = Cabecalho(nome=raca, raca=raca, nivel_total=1)
    f.classes = [ClasseInfo(nome="Ladino", nivel=1, primaria=True)]
    atualizar_ficha(f)
    assert f.descricao.tamanho == tamanho_esperado, (
        f"{raca}: tamanho esperado {tamanho_esperado.value}, "
        f"obtido {f.descricao.tamanho.value}"
    )
    obtido = _bonus_tamanho_furtividade(f)
    assert obtido == mod_esperado, (
        f"{raca} ({tamanho_esperado.value}): esperado {mod_esperado:+d}, "
        f"obtido {obtido}"
    )
