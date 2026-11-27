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


def test_passivos_armaduras_e_poderes_gerais_herois():
    from src.dados_habilidades import HABILIDADES_GERAIS
    from src.models import Habilidade

    def _mk(nivel: int = 7):
        return Personagem(
            cabecalho=Cabecalho(nome="Teste", raca="Humano"),
            classes=[ClasseInfo(nome="Guerreiro", nivel=nivel, primaria=True)],
            atributos_base=Atributos(forca=2, destreza=2, constituicao=2, inteligencia=2, sabedoria=2, carisma=2),
        )

    base = atualizar_ficha(_mk(7))

    # Herói dos Sete Instrumentos (+2 no nv 7 em perícias não treinadas)
    f = _mk(7)
    d_sete = HABILIDADES_GERAIS["HA_Heroi_Sete_Instrumentos"]
    f.habilidades.append(Habilidade(nome=d_sete["nome"], tipo=d_sete["tipo"], efeitos=dict(d_sete["efeitos"])))
    f = atualizar_ficha(f)
    assert f.pericias["Nobreza"].total == base.pericias["Nobreza"].total + 2

    # Defesa Armada (+2 Defesa e +2 Fortitude com arma 2 mãos corpo a corpo)
    f2 = _mk(7)
    d_da = HABILIDADES_GERAIS["HA_Defesa_Armada"]
    f2.habilidades.append(Habilidade(nome=d_da["nome"], tipo=d_da["tipo"], efeitos=dict(d_da["efeitos"])))
    f2.inventario.equipamentos.append(Item(nome="Montante", tipo="Arma", equipado=True))
    f2 = atualizar_ficha(f2)
    assert f2.status.defesa.total == base.status.defesa.total + 2
    assert f2.pericias["Fortitude"].total == base.pericias["Fortitude"].total + 2

    # Estilo Clássico (+2 Defesa com espada + escudo)
    f3 = _mk(7)
    d_ec = HABILIDADES_GERAIS["HA_Raca_Estilo_Classico"]
    f3.habilidades.append(Habilidade(nome=d_ec["nome"], tipo=d_ec["tipo"], efeitos=dict(d_ec["efeitos"])))
    f3.inventario.equipamentos.append(Item(nome="Espada longa", tipo="Arma", equipado=True))
    f3.inventario.equipamentos.append(Item(nome="Escudo leve", tipo="Escudo", equipado=True))
    f3 = atualizar_ficha(f3)
    # Escudo leve (+1) + Estilo Clássico (+2) = +3 sobre base
    assert f3.status.defesa.total == base.status.defesa.total + 3

    # Encastelado (RD 2 com armadura pesada)
    f4 = _mk(7)
    d_enc = HABILIDADES_GERAIS["HA_Encastelado"]
    f4.habilidades.append(Habilidade(nome=d_enc["nome"], tipo=d_enc["tipo"], efeitos=dict(d_enc["efeitos"])))
    f4.inventario.equipamentos.append(Item(nome="Armadura completa", tipo="Armadura", equipado=True))
    f4 = atualizar_ficha(f4)
    assert any("geral 2" in rd for rd in f4.status.rd)

    # Cota de moedas (+2 Diplomacia) e Armadura de engenhoqueiro goblin (-5 Furtividade)
    f5 = _mk(7)
    f5.inventario.equipamentos.append(Item(nome="Cota de moedas", tipo="Armadura", equipado=True))
    f5 = atualizar_ficha(f5)
    assert f5.pericias["Diplomacia"].total == base.pericias["Diplomacia"].total + 2


def test_passivos_poderes_distincao_e_encantos_herois():
    from src.models import DistincaoPersonagem
    from src.routers.dados import get_itens_magicos_herois

    base = atualizar_ficha(
        Personagem(
            cabecalho=Cabecalho(nome="Médico", raca="Humano"),
            classes=[ClasseInfo(nome="Inventor", nivel=7, primaria=True)],
            atributos_base=Atributos(forca=1, destreza=2, constituicao=2, inteligencia=3, sabedoria=2, carisma=2),
        )
    )
    f = Personagem(
        cabecalho=Cabecalho(nome="Médico", raca="Humano"),
        classes=[ClasseInfo(nome="Inventor", nivel=7, primaria=True)],
        atributos_base=Atributos(forca=1, destreza=2, constituicao=2, inteligencia=3, sabedoria=2, carisma=2),
        distincoes=[
            DistincaoPersonagem(
                nome="Médico de Salistick",
                admitido=True,
                poderes=["Medicina Avançada", "Saúde Perfeita"],
            ),
            DistincaoPersonagem(
                nome="Pistoleiro de Smokestone",
                admitido=True,
                poderes=["Rápido no Gatilho", "Balada do Pistoleiro"],
            ),
        ],
    )
    f = atualizar_ficha(f)
    # Saúde Perfeita: +1 Con, imune Veneno, +2 PM x 2 poderes = +4 PM
    assert f.atributos.constituicao == base.atributos.constituicao + 1
    assert "Veneno" in f.status.imunidades
    assert f.status.pm.maximo == base.status.pm.maximo + 4
    # Rápido no Gatilho: +2 Iniciativa x 2 poderes = +4 Iniciativa
    assert f.pericias["Iniciativa"].total == base.pericias["Iniciativa"].total + 4

    # Encantos e Itens Mágicos via endpoint
    im = get_itens_magicos_herois()
    assert len(im["encantos"]["armas"]) == 22
    assert len(im["encantos"]["armaduras_escudos"]) == 20
    assert len(im["encantos"]["esotericos"]) == 26
    assert len(im["encantos"]["acessorios"]) == 8
    assert len(im["itens_especificos"]) == 95

