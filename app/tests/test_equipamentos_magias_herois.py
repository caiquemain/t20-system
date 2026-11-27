# -*- coding: utf-8 -*-
"""Testes de Equipamentos, Melhorias, Magias e Itens Mágicos — Heróis de Arton (Cap. 3)."""
from src.dados_equipamentos import (
    DADOS_ARMADURAS,
    DADOS_ARMAS,
    DADOS_GERAIS,
    DADOS_MELHORIAS,
)
from src.dados_equipamentos_herois import (
    DADOS_ARMADURAS_HEROIS,
    DADOS_ARMAS_HEROIS,
    DADOS_GERAIS_HEROIS,
    DADOS_ITENS_MAGICOS_HEROIS,
    DADOS_MELHORIAS_HEROIS,
)
from src.dados_magias import DADOS_MAGIAS
from src.dados_magias_herois import DADOS_MAGIAS_HEROIS
from src.dados_suplementos import FONTE_HEROIS
from src.models import Atributos, Cabecalho, ClasseInfo, Item, Personagem
from src.regras import atualizar_ficha


def test_catalogos_equipamentos_e_magias_herois_completos():
    assert len(DADOS_ARMAS_HEROIS) == 37
    assert len(DADOS_ARMADURAS_HEROIS) == 14
    assert len(DADOS_GERAIS_HEROIS) == 136
    assert len(DADOS_MELHORIAS_HEROIS) == 12
    assert len(DADOS_ITENS_MAGICOS_HEROIS) == 95
    assert len(DADOS_MAGIAS_HEROIS) == 22

    for k in DADOS_ARMAS_HEROIS:
        assert k in DADOS_ARMAS
        assert DADOS_ARMAS[k]["fonte"] == FONTE_HEROIS
    for k in DADOS_ARMADURAS_HEROIS:
        assert k in DADOS_ARMADURAS
        assert DADOS_ARMADURAS[k]["fonte"] == FONTE_HEROIS
    for k in DADOS_MELHORIAS_HEROIS:
        assert k in DADOS_MELHORIAS
        assert DADOS_MELHORIAS[k]["fonte"] == FONTE_HEROIS
    for k, m in DADOS_MAGIAS_HEROIS.items():
        assert k in DADOS_MAGIAS
        assert m["fonte"] == FONTE_HEROIS
        assert m["circulo"] in (1, 2, 3)


def test_armaduras_e_armas_herois_funcionam_no_motor():
    f = Personagem(
        cabecalho=Cabecalho(nome="Hussardo", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=5, primaria=True)],
        atributos_base=Atributos(forca=3, destreza=2, constituicao=2, inteligencia=1, sabedoria=1, carisma=1),
    )
    f.inventario.equipamentos.append(
        Item(nome="Armadura de pedra", tipo="Armadura", equipado=True)
    )
    f.inventario.equipamentos.append(
        Item(nome="Espada de execução", tipo="Arma", equipado=True)
    )
    f = atualizar_ficha(f)

    # Armadura de pedra: Pesada (+12 Defesa, sem somar Des) => 10 + 12 = 22
    assert f.status.defesa.total == 22
    nomes_ataques = {a.nome for a in f.combate.ataques}
    assert "Espada de execução" in nomes_ataques
