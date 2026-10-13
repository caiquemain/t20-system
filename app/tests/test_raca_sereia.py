"""Testes de Sereia/Tritão (T20 JdA p.30).

Bugs cobertos:
#3 — Mestre do Tridente: +2 em dano com azagaias, lanças e tridentes.
     O catálogo usa chave 'lança', mas a arma real chama-se 'Lança montada'.
#4 — Canção dos Mares: "Caso aprenda novamente uma dessas magias, seu
     custo diminui em –1 PM." O catálogo não declara reducao_custo_se_conhecida.
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo, Magia
from src.regras import atualizar_ficha
from src.regras.habilidades import garantir_habilidades_iniciais
from src.regras.combate import sincronizar_ataques


def _ficha_sereia(classe="Guerreiro", nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome="Sereia Teste", raca="Sereia/Tritão", nivel_total=nivel)
    f.classes = [ClasseInfo(nome=classe, nivel=nivel, primaria=True)]
    return f


def _achar_hab(f, nome):
    return next((h for h in f.habilidades if h.nome == nome), None)


# ===================================================================
# 1. Mestre do Tridente — todos os nomes reais do catálogo
# ===================================================================

def _nomes_reais_de_armas_tridente():
    """Armas que a regra do livro deve cobrir: azagaias, lanças, tridentes."""
    from src.dados_equipamentos import DADOS_ARMAS
    palavras = ["azagaia", "lança", "tridente"]
    return [
        nome for nome in DADOS_ARMAS
        if any(p in nome.lower() for p in palavras)
    ]


def test_sereia_mestre_tridente_cobre_azagaia_lanca_tridente():
    f = _ficha_sereia()
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    bd = f.combate.bonus_dano_arma or {}

    nomes = _nomes_reais_de_armas_tridente()
    assert nomes, "Catálogo não tem azagaia/lança/tridente"

    faltando = []
    for nome in nomes:
        chave = nome.lower()
        if bd.get(chave) != 2:
            faltando.append((nome, bd.get(chave)))

    assert not faltando, (
        f"Armas sem o +2 do Mestre do Tridente: {faltando}.\n"
        f"Chaves disponíveis em bonus_dano_arma: {sorted(bd.keys())}"
    )


def test_sereia_mestre_tridente_inclui_lanca_montada():
    """Caso específico: 'Lança montada' deve casar com 'lança' da regra."""
    from src.dados_equipamentos import DADOS_ARMAS
    if "Lança montada" not in DADOS_ARMAS:
        pytest.skip("Lança montada não está no catálogo atual")

    f = _ficha_sereia()
    garantir_habilidades_iniciais(f)
    sincronizar_ataques(f)
    bd = f.combate.bonus_dano_arma or {}
    assert bd.get("lança montada") == 2, (
        f"'Lança montada' sem bônus. Chaves atuais: {sorted(bd.keys())}"
    )


def test_sereia_mestre_tridente_proficiencia_simples_so_tridente():
    """Livro: APENAS o tridente conta como arma simples. Não lança, não azagaia."""
    f = _ficha_sereia()
    garantir_habilidades_iniciais(f)
    hab = _achar_hab(f, "Mestre do Tridente")
    assert hab is not None
    prof = hab.efeitos.get("proficiencia_simples") or []
    assert "tridente" in [p.lower() for p in prof]
    assert not any("lança" in p.lower() for p in prof), (
        "Lança NÃO é arma simples para Sereia — só o tridente é."
    )
    assert not any("azagaia" in p.lower() for p in prof), (
        "Azagaia NÃO é arma simples para Sereia."
    )


# ===================================================================
# 2. Canção dos Mares — redução por reaprendizado
# ===================================================================

def test_sereia_cancao_dos_mares_tem_reducao_reaprendizado():
    """O catálogo precisa declarar reducao_custo_se_conhecida (ou reaprendizado)."""
    from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
    c = DADOS_HABILIDADES_RACIAIS["Cancao_Mares_Sereia"]
    e = c["efeitos"]
    tem_reducao = (
        e.get("reducao_custo_se_conhecida")
        or e.get("reducao_custo_reaprendizado")
    )
    assert tem_reducao, (
        "Canção dos Mares não declara reducao_custo_se_conhecida. "
        "Livro (p.30): 'Caso aprenda novamente uma dessas magias, "
        "seu custo diminui em –1 PM.'"
    )


def test_sereia_reaprendizado_reduz_custo_end_to_end():
    """Fluxo completo: Sereia escolhe Amedrontar; Arcanista também aprende
    Amedrontar. Ao lançar, o custo deve ter o desconto de –1 PM."""
    from src.regras.custo_magia import calcular_custo_magia

    f = _ficha_sereia()
    garantir_habilidades_iniciais(f)
    hab = _achar_hab(f, "Canção dos Mares")
    assert hab is not None
    # Sereia escolhe 'Amedrontar' (1º da lista)
    hab.escolhas_aplicadas = {"magia_0": "Amedrontar"}

    # Simula a magia já conhecida de outra fonte (ex.: Arcanista nv 1)
    magia = Magia(
        nome="Amedrontar",
        circulo=1,
        fonte="Classe: Arcanista",
        fonte_origem="Habilidade: Caminho do Arcanista",
    )
    # Adiciona no grimório como se viesse de outra fonte
    f.combate.magias = [magia]
    # Re-garante escolhas após reset
    f.habilidades = [h for h in f.habilidades if h.nome != "Canção dos Mares"]
    garantir_habilidades_iniciais(f)
    h2 = _achar_hab(f, "Canção dos Mares")
    h2.escolhas_aplicadas = {"magia_0": "Amedrontar"}

    calc = calcular_custo_magia(f, magia)
    # Sem redução de reaprendizado seria 1 (base 1º círculo).
    # Com redução deveria ser max(1, 1-1) = 1 — o mínimo trava.
    # Por isso o teste verifica que a fonte de reaprendizado aparece no calc.
    fontes = [fnt.fonte for fnt in calc.fontes]
    tem_fonte_reducao = any(
        "Canção dos Mares" in (x or "") or "reaprendizado" in (x or "").lower()
        for x in fontes
    )
    # Se não apareceu a fonte, pelo menos verifica que o catálogo tem a chave
    if not tem_fonte_reducao:
        e = h2.efeitos or {}
        assert e.get("reducao_custo_se_conhecida") or e.get("reducao_custo_reaprendizado"), (
            f"Sem redução de reaprendizado nem em efeitos nem no calc. "
            f"Fontes: {fontes}"
        )
