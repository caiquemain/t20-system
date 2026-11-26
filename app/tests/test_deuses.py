# -*- coding: utf-8 -*-
"""Testes dos 20 Deuses do Panteão (T20 JdA p.96-105) e mecânicas de devoção."""
from src.dados_deuses import DADOS_DEUSES, DUYSHIDAKK
from src.dados_pericias import DADOS_PERICIAS
from src.models import Personagem, ClasseInfo, Cabecalho, Atributos
from src.regras import atualizar_ficha


def test_catalogo_20_deuses_completo_e_valido():
    assert len(DADOS_DEUSES) == 20
    esperados = {
        "Aharadak", "Allihanna", "Arsenal", "Azgher", "Hyninn",
        "Kallyadranoch", "Khalmyr", "Lena", "Lin-Wu", "Marah",
        "Megalokk", "Nimb", "Oceano", "Sszzaas", "Tanna-Toh",
        "Tenebra", "Thwor", "Thyatis", "Valkaria", "Wynna",
    }
    assert set(DADOS_DEUSES.keys()) == esperados

    for nome, d in DADOS_DEUSES.items():
        assert d["nome"] == nome
        assert d["titulo"]
        assert d["crencas"]
        assert d["descricao"]
        assert d["simbolo"]
        assert d["energia"] in {"Positiva", "Negativa", "Qualquer"}
        assert len(d["poderes"]) == 4, f"{nome} deve ter 4 poderes concedidos"
        assert d["obrigacoes"], f"{nome} deve ter Obrigações & Restrições"
        assert len(d["devotos"]) > 0


def test_deuses_regras_especificas_livro_base():
    assert DADOS_DEUSES["Lena"]["arma"] is None
    assert DADOS_DEUSES["Marah"]["arma"] is None
    assert DADOS_DEUSES["Nimb"]["arma"] == "Qualquer"
    assert DADOS_DEUSES["Aharadak"]["devotos"] == ["Todos"]
    assert DADOS_DEUSES["Valkaria"]["devotos"] == ["Todos"]
    assert DADOS_DEUSES["Thwor"]["devotos"] == DUYSHIDAKK
    assert DADOS_DEUSES["Khalmyr"]["arma"] == "Espada longa"
    assert DADOS_DEUSES["Lin-Wu"]["arma"] == "Katana"
    assert DADOS_DEUSES["Oceano"]["arma"] == "Tridente"


def test_nimb_penalidade_menos_5_pericias_carisma():
    f_sem = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Bardo", raca="Humano", deus=""),
        classes=[ClasseInfo(nome="Bardo", nivel=1, primaria=True)],
        atributos_base=Atributos(carisma=3, forca=1),
    ))
    f_nimb = atualizar_ficha(Personagem(
        cabecalho=Cabecalho(nome="Bardo", raca="Humano", deus="Nimb"),
        classes=[ClasseInfo(nome="Bardo", nivel=1, primaria=True)],
        atributos_base=Atributos(carisma=3, forca=1),
    ))

    car_testadas = 0
    for p_nome, meta in DADOS_PERICIAS.items():
        if meta["atributo"] == "car":
            assert f_nimb.pericias[p_nome].total == f_sem.pericias[p_nome].total - 5
            car_testadas += 1
        elif p_nome == "Atletismo":
            assert f_nimb.pericias[p_nome].total == f_sem.pericias[p_nome].total
    assert car_testadas == 6
