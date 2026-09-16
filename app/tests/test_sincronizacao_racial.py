"""Limpeza automática de ataques raciais na troca de raça (bug Minotauro→Dahllan)."""
from src.models import Personagem, Ataque
from src.regras.combate import sincronizar_ataques


class _Hab:
    def __init__(self, nome, tipo="Racial", efeitos=None):
        self.nome = nome
        self.tipo = tipo
        self.fonte = tipo
        self.descricao = ""
        self.efeitos = efeitos or {}
        self.escolhas_aplicadas = {}


def _ataque_manual():
    return Ataque(
        nome="Soco", bonus_ataque="+0", dano="1d3", critico="x2",
        tipo="Impacto", alcance="Curto",
    )


def test_ataque_racial_criado_com_fonte():
    p = Personagem()
    p.cabecalho.raca = "Minotauro"
    p.habilidades = [_Hab("Chifres", efeitos={"arma_natural": "Chifres 1d6"})]
    sincronizar_ataques(p)
    assert any(a.nome == "Chifres" and a.fonte == "Racial" for a in p.combate.ataques)


def test_troca_de_raca_limpa_orfaos():
    p = Personagem()
    p.cabecalho.raca = "Minotauro"
    p.habilidades = [_Hab("Chifres", efeitos={"arma_natural": "Chifres 1d6"})]
    sincronizar_ataques(p)
    p.cabecalho.raca = "Dahllan"
    p.habilidades = [_Hab("Amiga das Plantas", efeitos={})]
    sincronizar_ataques(p)
    assert not [a for a in p.combate.ataques if a.nome == "Chifres"]


def test_ataque_manual_sobrevive_a_troca():
    p = Personagem()
    p.cabecalho.raca = "Minotauro"
    p.habilidades = [_Hab("Chifres", efeitos={"arma_natural": "Chifres 1d6"})]
    p.combate.ataques.append(_ataque_manual())
    sincronizar_ataques(p)
    p.cabecalho.raca = "Dahllan"
    p.habilidades = [_Hab("Amiga das Plantas", efeitos={})]
    sincronizar_ataques(p)
    assert any(a.nome == "Soco" and a.fonte is None for a in p.combate.ataques)


def test_resincronizar_nao_duplica_racial():
    p = Personagem()
    p.cabecalho.raca = "Minotauro"
    p.habilidades = [_Hab("Chifres", efeitos={"arma_natural": "Chifres 1d6"})]
    sincronizar_ataques(p)
    sincronizar_ataques(p)
    assert len([a for a in p.combate.ataques if a.nome == "Chifres"]) == 1
