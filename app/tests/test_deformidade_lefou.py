"""Deformidade (Lefou) e crédito de fonte nas raças canônicas."""
import src.dados_habilidades_raciais as mod_raciais
from src.dados_racas import DADOS_RACAS

DADOS = getattr(mod_raciais, "DADOS_HABILIDADES_RACIAIS", None) or \
    getattr(mod_raciais, "HABILIDADES_RACIAIS")


def test_lefou_possui_deformidade():
    assert "Deformidade_Lefou" in DADOS_RACAS["Lefou"]["habilidades"]


def test_deformidade_dois_bonus_e_troca_por_poder():
    efeitos = DADOS["Deformidade_Lefou"]["efeitos"]
    assert efeitos["pericia_bonus_escolha"] == 2
    assert efeitos["troca_poder_tormenta"] is True


def test_fonte_do_livro_nas_racas_canonicas():
    for raca in ["Humano", "Lefou", "Hynne", "Minotauro", "Dahllan"]:
        assert DADOS_RACAS[raca].get("fonte") == "T20 JdA", raca


def test_racas_de_teste_sem_fonte():
    assert "fonte" not in DADOS_RACAS["Duende"]
    assert "fonte" not in DADOS_RACAS["Sátiro"]
