"""Auditoria Lote A: bonus de raca em pericia e Defesa (T20 JdA Cap. 1).

Cobre bonus declarados no catalogo mas sem teste previo:
    Elfo      - Sentidos Elicos: +2 Misticismo, +2 Percepcao
    Goblin    - Rato das Ruas: +2 Fortitude
    Hynne     - Pequeno e Rechonchudo: +2 Enganacao
    Aao      - Conhecimento das Rochas: +2 Percepcao/Sobrevivencia
                 (condicional subterraneo, ja testado em test_racas)
    Aggelus   - Luz Sagrada: +2 Diplomacia, +2 Intuicao
    Sulfure   - Sombras Profanas: +2 Enganacao, +2 Furtividade
    Minotauro - Couro Rigido: +1 Defesa
    Trog      - Reptiliano: +1 Defesa
"""
import pytest
from src.models import Personagem, Cabecalho, ClasseInfo
from src.regras import atualizar_ficha


def _ficha(raca, classe="Guerreiro", nivel=1):
    f = Personagem()
    f.cabecalho = Cabecalho(nome=f"Teste {raca}", raca=raca, nivel_total=nivel)
    f.classes = [ClasseInfo(nome=classe, nivel=nivel, primaria=True)]
    return f


def _fontes_bonus(f, pericia):
    """Devolve a lista de strings de fontes_bonus de uma pericia."""
    info = f.pericias.get(pericia)
    return list(info.fontes_bonus) if info else []


def _tem_fonte(f, pericia, trecho):
    return any(trecho in linha for linha in _fontes_bonus(f, pericia))


# ===================================================================
# 1. Elfo - Sentidos Elicos: +2 Misticismo e +2 Percepcao
# ===================================================================

def test_elfo_sentidos_elicos_misticismo():
    f = _ficha("Elfo")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Misticismo", "Sentidos Élficos"), (
        f"Fontes de Misticismo: {_fontes_bonus(f, 'Misticismo')}"
    )


def test_elfo_sentidos_elicos_percepcao():
    f = _ficha("Elfo")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Percepção", "Sentidos Élficos"), (
        f"Fontes de Percepção: {_fontes_bonus(f, 'Percepção')}"
    )


# ===================================================================
# 2. Goblin - Rato das Ruas: +2 Fortitude
# ===================================================================

def test_goblin_rato_das_ruas_fortitude():
    f = _ficha("Goblin")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Fortitude", "Rato das Ruas"), (
        f"Fontes de Fortitude: {_fontes_bonus(f, 'Fortitude')}"
    )


# ===================================================================
# 3. Hynne - Pequeno e Rechonchudo: +2 Enganacao
# ===================================================================

def test_hynne_pequeno_rechonchudo_enganacao():
    f = _ficha("Hynne")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Enganação", "Pequeno e Rechonchudo"), (
        f"Fontes de Enganação: {_fontes_bonus(f, 'Enganação')}"
    )


# ===================================================================
# 4. Aggelus - Luz Sagrada: +2 Diplomacia e +2 Intuicao
# ===================================================================

def test_aggelus_luz_sagrada_diplomacia():
    f = _ficha("Suraggel (Aggelus)")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Diplomacia", "Luz Sagrada"), (
        f"Fontes de Diplomacia: {_fontes_bonus(f, 'Diplomacia')}"
    )


def test_aggelus_luz_sagrada_intuicao():
    f = _ficha("Suraggel (Aggelus)")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Intuição", "Luz Sagrada"), (
        f"Fontes de Intuição: {_fontes_bonus(f, 'Intuição')}"
    )


# ===================================================================
# 5. Sulfure - Sombras Profanas: +2 Enganacao e +2 Furtividade
# ===================================================================

def test_sulfure_sombras_profanas_enganacao():
    f = _ficha("Suraggel (Sulfure)")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Enganação", "Sombras Profanas"), (
        f"Fontes de Enganação: {_fontes_bonus(f, 'Enganação')}"
    )


def test_sulfure_sombras_profanas_furtividade():
    f = _ficha("Suraggel (Sulfure)")
    atualizar_ficha(f)
    assert _tem_fonte(f, "Furtividade", "Sombras Profanas"), (
        f"Fontes de Furtividade: {_fontes_bonus(f, 'Furtividade')}"
    )


# ===================================================================
# 6. Minotauro - Couro Rigido: +1 Defesa
# ===================================================================

def test_minotauro_couro_rigido_defesa():
    f = _ficha("Minotauro")
    atualizar_ficha(f)
    fontes = [fnt for fnt in f.status.defesa_calc.fontes
              if "Couro Rígido" in (fnt.fonte or "")]
    assert fontes, (
        f"Couro Rígido nao somou na Defesa. "
        f"Fontes: {[(fnt.fonte, fnt.valor) for fnt in f.status.defesa_calc.fontes]}"
    )
    assert fontes[0].valor == 1


# ===================================================================
# 7. Trog - Reptiliano: +1 Defesa
# ===================================================================

def test_trog_reptiliano_defesa():
    f = _ficha("Trog")
    atualizar_ficha(f)
    fontes = [fnt for fnt in f.status.defesa_calc.fontes
              if "Reptiliano" in (fnt.fonte or "")]
    assert fontes, (
        f"Reptiliano nao somou na Defesa. "
        f"Fontes: {[(fnt.fonte, fnt.valor) for fnt in f.status.defesa_calc.fontes]}"
    )
    assert fontes[0].valor == 1


# ===================================================================
# 8. Nao-duplicacao: nao deve somar duas vezes
# ===================================================================

@pytest.mark.parametrize("raca,pericia,fonte", [
    ("Elfo", "Misticismo", "Sentidos Élficos"),
    ("Elfo", "Percepção", "Sentidos Élficos"),
    ("Goblin", "Fortitude", "Rato das Ruas"),
    ("Hynne", "Enganação", "Pequeno e Rechonchudo"),
])
def test_bonus_racial_nao_duplica_em_reprocessamentos(raca, pericia, fonte):
    """Rodar atualizar_ficha varias vezes nao pode duplicar o bonus."""
    f = _ficha(raca)
    for _ in range(3):
        atualizar_ficha(f)
    ocorrencias = [linha for linha in _fontes_bonus(f, pericia) if fonte in linha]
    assert len(ocorrencias) == 1, (
        f"{raca}/{pericia}/{fonte}: esperava 1 ocorrencia, achei {len(ocorrencias)}. "
        f"Fontes completas: {_fontes_bonus(f, pericia)}"
    )
