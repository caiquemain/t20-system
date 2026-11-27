# -*- coding: utf-8 -*-
"""Testes de Deuses de Arton — Equipamentos Religiosos, Melhorias, Itens Litúrgicos,
Magias Divinas, 23 Distinções e Regras de Devoção (Cap. 1 e 2)."""
from src.dados_deuses import DADOS_DEUSES
from src.dados_distincoes_deuses import DADOS_DISTINCOES_DEUSES
from src.dados_equipamentos import DADOS_GERAIS, DADOS_MELHORIAS
from src.dados_equipamentos_deuses import (
    DADOS_GERAIS_DEUSES,
    DADOS_ITENS_LITURGICOS_DEUSES,
    DADOS_MELHORIAS_DEUSES,
)
from src.dados_magias import DADOS_MAGIAS
from src.dados_magias_deuses import DADOS_MAGIAS_DEUSES
from src.dados_suplementos import FONTE_DEUSES
from src.models import Atributos, Cabecalho, ClasseInfo, DistincaoPersonagem, Personagem
from src.regras import atualizar_ficha


def test_equipamentos_melhorias_e_liturgicos_deuses():
    assert len(DADOS_GERAIS_DEUSES) == 70
    assert len(DADOS_MELHORIAS_DEUSES) == 5
    assert len(DADOS_ITENS_LITURGICOS_DEUSES) == 35

    for nome, d in DADOS_GERAIS_DEUSES.items():
        assert d["fonte"] == FONTE_DEUSES
        assert d["descricao"]
        assert nome in DADOS_GERAIS

    for nome, d in DADOS_MELHORIAS_DEUSES.items():
        assert d["fonte"] == FONTE_DEUSES
        assert nome in DADOS_MELHORIAS

    for nome, d in DADOS_ITENS_LITURGICOS_DEUSES.items():
        assert d["fonte"] == FONTE_DEUSES
        assert d["deus"] in DADOS_DEUSES
        assert d["preco"] > 0, f"{nome} deve ter preço > 0"
        assert d["descricao"]


def test_magias_divinas_deuses():
    assert len(DADOS_MAGIAS_DEUSES) == 29
    for nome, m in DADOS_MAGIAS_DEUSES.items():
        assert nome in DADOS_MAGIAS
        assert m["fonte"] == FONTE_DEUSES
        assert m["tipo"] in {"Divina", "Universal"}
        assert m["circulo"] in {1, 2, 3, 4, 5}
        assert m["descricao"]
    assert "Arma de Jade" in DADOS_MAGIAS
    assert "Bofetada de Nimb" in DADOS_MAGIAS
    assert "Couraça de Allihanna" in DADOS_MAGIAS
    assert "Voz da Razão" in DADOS_MAGIAS


def test_23_distincoes_deuses_no_motor():
    assert len(DADOS_DISTINCOES_DEUSES) == 23
    total_poderes = sum(len(d["poderes"]) for d in DADOS_DISTINCOES_DEUSES.values())
    assert total_poderes == 112

    for nome, d in DADOS_DISTINCOES_DEUSES.items():
        assert d["fonte"] == FONTE_DEUSES
        assert d["marca"]["nome"]
        assert len(d["poderes"]) >= 2

    # Testa sincronização real no motor de ficha com uma Distinção de Deuses de Arton
    ficha = Personagem(
        cabecalho=Cabecalho(nome="Sombra", raca="Humano", deus="Tenebra"),
        classes=[ClasseInfo(nome="Ladino", nivel=7, primaria=True)],
        atributos_base=Atributos(destreza=4, inteligencia=2, sabedoria=2),
        distincoes=[
            DistincaoPersonagem(
                nome="Sombra de Tenebra",
                admitido=True,
                poderes=["Caminhar nas Trevas", "Clone Sombrio"],
            )
        ],
    )
    ficha = atualizar_ficha(ficha)
    nomes_hab = {h.nome for h in ficha.habilidades}
    assert "Ameaça das Sombras" in nomes_hab
    assert "Caminhar nas Trevas" in nomes_hab
    assert "Clone Sombrio" in nomes_hab


def test_ser_devoto_druida_tenebra_e_devocao_ampla():
    assert "Druida" in DADOS_DEUSES["Tenebra"]["devotos"]

    # Frade do Panteão nível 5 (Veterano = 2 patamares) -> +4 PM de Devoção Ampla
    base = atualizar_ficha(
        Personagem(
            cabecalho=Cabecalho(nome="Frade Wynna", raca="Humano", deus="Wynna"),
            classes=[ClasseInfo(nome="Frade", nivel=5, primaria=True)],
            atributos_base=Atributos(sabedoria=4),
        )
    )
    panteao = atualizar_ficha(
        Personagem(
            cabecalho=Cabecalho(nome="Frade Panteão", raca="Humano", deus="Panteão"),
            classes=[ClasseInfo(nome="Frade", nivel=5, primaria=True)],
            atributos_base=Atributos(sabedoria=4),
        )
    )
    assert panteao.status.pm.maximo == base.status.pm.maximo + 4

    # Druida de Arton nível 11 (Campeão = 3 patamares) -> +6 PM de Devoção Ampla
    druida_allihanna = atualizar_ficha(
        Personagem(
            cabecalho=Cabecalho(nome="D1", raca="Humano", deus="Allihanna"),
            classes=[ClasseInfo(nome="Druida", nivel=11, primaria=True)],
            atributos_base=Atributos(sabedoria=4),
        )
    )
    druida_arton = atualizar_ficha(
        Personagem(
            cabecalho=Cabecalho(nome="D2", raca="Humano", deus="Arton"),
            classes=[ClasseInfo(nome="Druida", nivel=11, primaria=True)],
            atributos_base=Atributos(sabedoria=4),
        )
    )
    assert druida_arton.status.pm.maximo == druida_allihanna.status.pm.maximo + 6
