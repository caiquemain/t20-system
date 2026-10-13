"""Testes do Anão (T20 JdA p.20).

Bug #1 — Duro como Pedra:
    Livro: "+3 PV no 1º nível e +1 por nível seguinte."
    → Nível 1 = 3, Nível 2 = 4, Nível 5 = 7, Nível 10 = 12.

Bug #2 — Tradição de Heredrimm:
    Livro: "todos os machados, martelos, marretas e picaretas são armas
    simples. Você recebe +2 em ataques com essas armas."
    → O bônus precisa casar com os NOMES REAIS das armas no catálogo
      ('Machado de guerra', 'Machadinha', 'Marreta', 'Picareta', etc.),
      não com strings genéricas ('machado', 'martelo').
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo
from src.regras import atualizar_ficha
from src.regras.habilidades import garantir_habilidades_iniciais
from src.regras.combate import sincronizar_ataques


def _ficha_anao(nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Anão Teste", raca="Anão", nivel_total=nivel)
    f.classes = [ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)]
    return f


def _bonus_duro_como_pedra(f):
    """Extrai o valor total que 'Duro como Pedra' adicionou a PV máx."""
    if not f.status.pv_calc:
        return 0
    return sum(
        fnt.valor for fnt in f.status.pv_calc.fontes
        if "Duro como Pedra" in (fnt.fonte or "")
    )


# ===================================================================
# 1. Duro como Pedra — valor correto por nível
# ===================================================================

@pytest.mark.parametrize("nivel,esperado", [
    (1, 3),    # 3 + (1-1)*1 = 3
    (2, 4),    # 3 + (2-1)*1 = 4
    (5, 7),    # 3 + (5-1)*1 = 7
    (10, 12),  # 3 + (10-1)*1 = 12
    (20, 22),  # 3 + (20-1)*1 = 22
])
def test_anao_duro_como_pedra_bonus_pv_por_nivel(nivel, esperado):
    """Livro (p.20): +3 PV no 1º nível e +1 por nível seguinte."""
    f = _ficha_anao(nivel=nivel)
    atualizar_ficha(f)
    obtido = _bonus_duro_como_pedra(f)
    assert obtido == esperado, (
        f"Nível {nivel}: 'Duro como Pedra' deveria somar {esperado} PV, somou {obtido}. "
        f"Esperado = 3 + (nível - 1) * 1."
    )


def test_anao_nao_e_o_unico_bonus_de_pv():
    """Confirma que existe a fonte (a habilidade foi criada corretamente)."""
    f = _ficha_anao(nivel=1)
    atualizar_ficha(f)
    fontes = [fnt.fonte for fnt in (f.status.pv_calc.fontes if f.status.pv_calc else [])]
    assert any("Duro como Pedra" in (x or "") for x in fontes), (
        f"Nenhuma fonte 'Duro como Pedra' em PV calc. Fontes atuais: {fontes}"
    )


# ===================================================================
# 2. Tradição de Heredrimm — nomes reais de arma
# ===================================================================

def _nomes_reais_de_armas_anao():
    """Retorna todos os nomes do catálogo que casam com a regra do livro."""
    from src.dados_equipamentos import DADOS_ARMAS
    palavras = ["machado", "machadinha", "martelo", "marreta", "picareta"]
    return [
        nome for nome in DADOS_ARMAS
        if any(p in nome.lower() for p in palavras)
    ]


def test_anao_tradicao_heredrimm_cobre_todos_os_machados_do_catalogo():
    """O bônus de +2 deve existir com a chave EXATA de cada arma real."""
    f = _ficha_anao()
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    ba = f.combate.bonus_ataque_arma or {}

    nomes = _nomes_reais_de_armas_anao()
    assert nomes, "Catálogo não tem nenhum machado/martelo/marreta/picareta"

    faltando = []
    for nome in nomes:
        # Chave normalizada em lower — mesmo padrão de efeitos_de_armas_especificas
        chave = nome.lower()
        if ba.get(chave) != 2:
            faltando.append((nome, ba.get(chave)))

    assert not faltando, (
        f"Armas sem o +2 da Tradição de Heredrimm: {faltando}.\n"
        f"Chaves disponíveis em bonus_ataque_arma: {sorted(ba.keys())}"
    )


def test_anao_bonus_arma_nao_usa_chave_generica():
    """O bônus não pode ficar preso numa chave genérica como 'machado'."""
    f = _ficha_anao()
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    ba = f.combate.bonus_ataque_arma or {}
    # 'machado' sozinho não corresponde a nenhuma arma real do catálogo
    assert "machado" not in ba, (
        "Chave genérica 'machado' presente. A regra exige nomes exatos "
        "de armas (ex.: 'machado de guerra')."
    )
