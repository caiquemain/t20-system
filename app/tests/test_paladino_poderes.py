# -*- coding: utf-8 -*-
"""Testes dos 23 poderes de Paladino (T20 JdA p.82-83) e bônus progressivo de Virtudes."""
import pytest
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos, Habilidade
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_magias_conhecidas import PODERES_QUE_DAO_MAGIAS
from src.regras import atualizar_ficha


def _add_poder(ficha: Personagem, chave: str):
    d = DADOS_HABILIDADES_CLASSE[chave]
    ficha.habilidades.append(Habilidade(
        nome=d["nome"],
        tipo=d["tipo"],
        descricao=d["descricao"],
        fonte="Paladino",
        efeitos=dict(d.get("efeitos") or {}),
    ))


def _paladino_com_poderes(nivel: int, chaves_poderes, car: int = 4, condicoes=None) -> Personagem:
    ficha = Personagem(
        cabecalho=Cabecalho(nome="Gregor", raca="Humano"),
        classes=[ClasseInfo(nome="Paladino", nivel=nivel, primaria=True)],
        atributos_base=Atributos(forca=2, destreza=1, constituicao=2, inteligencia=0, sabedoria=2, carisma=car),
        condicoes_ativas=list(condicoes or []),
    )
    for ch in chaves_poderes:
        _add_poder(ficha, ch)
    return atualizar_ficha(ficha)


def test_catalogo_paladino_completo_30_entradas():
    pal_entries = [v for v in DADOS_HABILIDADES_CLASSE.values() if v.get("classe") == "Paladino"]
    fixas = [v for v in pal_entries if v.get("tipo") == "Habilidade de Classe"]
    poderes = [v for v in pal_entries if v.get("tipo") == "Poder de Paladino"]
    assert len(fixas) == 7
    assert len(poderes) == 23
    assert len(pal_entries) == 30


def test_arma_sagrada_e_fulgor_divino():
    f = _paladino_com_poderes(9, ["PALADINO_ARMA_SAGRADA", "PALADINO_FULGOR_DIVINO"], car=4)
    gd = f.combate.paladino_calc["golpe_divino"]
    assert gd["tipo_dado"] == "d12"
    assert gd["formula"] == "+3d12"
    assert gd["fulgor_divino"] is True


def test_poderes_de_aura():
    f = _paladino_com_poderes(
        18,
        [
            "PALADINO_AURA_PODEROSA",
            "PALADINO_AURA_CURA",
            "PALADINO_AURA_ARDENTE",
            "PALADINO_AURA_ANTIMAGIA",
            "PALADINO_AURA_INVENCIBILIDADE",
        ],
        car=4,
        condicoes=["aura_sagrada"],
    )
    aura = f.combate.paladino_calc["aura_sagrada"]
    assert aura["raio_m"] == 30
    assert aura["aura_cura_pv"] == 9
    assert aura["aura_ardente_dano"] == 9
    assert aura["aura_antimagia"] is True
    assert aura["aura_invencibilidade"] is True


@pytest.mark.parametrize("nivel,bonus_atq,formula_dano,custo_max", [
    (2, 1, "+1d8", 2),
    (5, 2, "+2d8", 3),
    (10, 3, "+3d8", 4),
    (15, 4, "+4d8", 5),
    (20, 5, "+5d8", 6),
])
def test_julgamento_vindicacao_escala(nivel, bonus_atq, formula_dano, custo_max):
    f = _paladino_com_poderes(nivel, ["PALADINO_JULGAMENTO_VINDICACAO"])
    v = f.combate.paladino_calc["vindicacao"]
    assert v["bonus_ataque_max"] == bonus_atq
    assert v["bonus_dano_max"] == formula_dano
    assert v["custo_max_pm"] == custo_max


def test_orar_no_catalogo_de_magias_conhecidas():
    assert PODERES_QUE_DAO_MAGIAS.get("Orar") == 1


@pytest.mark.parametrize("qtd,bonus_esperado", [
    (1, 1),
    (2, 3),
    (3, 6),
    (4, 10),
    (5, 15),
])
def test_virtudes_paladinescas_bonus_progressivo_pm(qtd, bonus_esperado):
    todas = [
        "PALADINO_VIRTUDE_CARIDADE",
        "PALADINO_VIRTUDE_CASTIDADE",
        "PALADINO_VIRTUDE_COMPAIXAO",
        "PALADINO_VIRTUDE_HUMILDADE",
        "PALADINO_VIRTUDE_TEMPERANCA",
    ]
    f_base = _paladino_com_poderes(6, [], car=3)
    f_virt = _paladino_com_poderes(6, todas[:qtd], car=3)
    assert f_virt.status.pm.maximo == f_base.status.pm.maximo + bonus_esperado
    assert f_virt.combate.paladino_calc["virtudes"]["quantidade"] == qtd
    assert f_virt.combate.paladino_calc["virtudes"]["pm_bonus"] == bonus_esperado


def test_virtude_castidade_imunidade_encantamento():
    f = _paladino_com_poderes(4, ["PALADINO_VIRTUDE_CASTIDADE"])
    assert "Encantamento" in f.status.imunidades


def test_virtude_compaixao_caridade_humildade():
    f = _paladino_com_poderes(
        6,
        ["PALADINO_VIRTUDE_COMPAIXAO", "PALADINO_VIRTUDE_CARIDADE", "PALADINO_VIRTUDE_HUMILDADE"],
        car=4,
    )
    cm = f.combate.paladino_calc["cura_pelas_maos"]
    assert cm["dado_por_pm"] == "2d6+1"
    assert cm["formula_max"] == "4d6+2"
    assert cm["alcance"] == "Curto"
    assert cm["reducao_pm_aliado"] == 1
    assert f.combate.paladino_calc["virtudes"]["humildade_pm_temp"] == 4
