"""Arcanista - Lote 5: poderes com efeitos declarativos (VTT-ready).

Estes poderes ainda nao tem comportamento motor (contramagica, foco
vital, fluxo de mana, etc.). O objetivo aqui e garantir que a
ESTRUTURA de dados esta pronta para quando o motor evoluir ou para
quando exportarmos para um VTT/mod (BG3, Foundry, etc).

Nao testa semantica de jogo — testa forma dos dados.
"""
import pytest
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE


PODERES_DECLARATIVOS = [
    "ARCANISTA_CONTRAMAGICA_APRIMORADA",
    "ARCANISTA_ENVOLTO_MISTERIO",
    "ARCANISTA_ESCRIBA_ARCANO",
    "ARCANISTA_FLUXO_MANA",
    "ARCANISTA_FOCO_VITAL",
    "ARCANISTA_HERANCA_APRIMORADA",
    "ARCANISTA_HERANCA_SUPERIOR",
    "ARCANISTA_MAGIA_PUNGENTE",
    "ARCANISTA_RAIO_ARCANO",
    "ARCANISTA_RAIO_ELEMENTAL",
    "ARCANISTA_RAIO_PODEROSO",
    "ARCANISTA_TINTA_MAGO",
]


@pytest.mark.parametrize("chave", PODERES_DECLARATIVOS)
def test_poder_declarativo_tem_efeitos_nao_vazios(chave):
    hab = DADOS_HABILIDADES_CLASSE.get(chave)
    assert hab is not None, f"Chave '{chave}' ausente no catalogo"
    efeitos = hab.get("efeitos") or {}
    assert efeitos, (
        f"{chave}: efeitos vazios. Mesmo declarativo precisa de ao menos "
        f"uma chave para VTT/mod ler."
    )


@pytest.mark.parametrize("chave", PODERES_DECLARATIVOS)
def test_poder_declarativo_tem_nota_ou_chave_reconhecivel(chave):
    """Cada poder precisa ter ao menos uma chave ativa OU uma 'nota'."""
    hab = DADOS_HABILIDADES_CLASSE.get(chave)
    efeitos = hab.get("efeitos") or {}
    tem_nota = isinstance(efeitos.get("nota"), str) and efeitos["nota"].strip()
    tem_chave_ativa = any(
        k in efeitos for k in (
            "contramagica_como_reacao", "sustentados_simultaneos",
            "sobrevive_a_dano_letal", "aprender_magias_por_copia",
            "fabricar_pergaminho", "bonus_pericia_condicional",
            "heranca_nivel", "cd_ativavel", "ataque_magico",
            "raio_elemental", "raio_poderoso",
        )
    )
    assert tem_nota or tem_chave_ativa, (
        f"{chave}: sem 'nota' e sem chave ativa. Efeitos: {efeitos}"
    )


@pytest.mark.parametrize("chave", PODERES_DECLARATIVOS)
def test_poder_declarativo_valores_sao_tipados(chave):
    """Sanidade: nenhum valor pode ser None solto."""
    hab = DADOS_HABILIDADES_CLASSE.get(chave)
    efeitos = hab.get("efeitos") or {}
    for k, v in efeitos.items():
        assert v is not None, f"{chave}.efeitos['{k}'] = None"


def test_nenhum_poder_de_arcanista_tem_efeitos_vazios():
    """Guard geral: todo poder de Arcanista tem efeitos nao-vazios."""
    problemas = []
    for chave, hab in DADOS_HABILIDADES_CLASSE.items():
        if hab.get("classe") != "Arcanista":
            continue
        efeitos = hab.get("efeitos")
        if efeitos is None:
            problemas.append((chave, "efeitos=None"))
        elif isinstance(efeitos, dict) and not efeitos:
            problemas.append((chave, "efeitos={}"))
    assert not problemas, (
        f"Poderes de Arcanista sem efeitos: {problemas}. "
        f"Preencher com estrutura declarativa (ver docs/efeitos-schema.md)."
    )
