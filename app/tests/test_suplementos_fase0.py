"""Testes da Fase 0 — Fundação Arquitetural para Suplementos."""
from src.dados_suplementos import (
    FONTE_AMEACAS,
    FONTE_ATLAS,
    FONTE_DEUSES,
    FONTE_HEROIS,
    FONTE_LIVRO_BASICO,
    LIVROS_OFICIAIS,
    SUPLEMENTOS_CATALOGO,
)
from src.models import (
    ClasseInfo,
    ComplicacaoPersonagem,
    DistincaoPersonagem,
    Personagem,
)
from src.routers.dados import (
    listar_poderes_categorizados,
    listar_suplementos,
    obter_detalhes_classes,
    obter_detalhes_deuses,
    obter_detalhes_racas,
)


def test_catalogo_suplementos_oficial():
    sup = listar_suplementos()
    ids = [s["id"] for s in sup]
    assert ids == LIVROS_OFICIAIS
    assert len(SUPLEMENTOS_CATALOGO) == 5
    assert FONTE_LIVRO_BASICO in ids
    assert FONTE_AMEACAS in ids
    assert FONTE_HEROIS in ids
    assert FONTE_DEUSES in ids
    assert FONTE_ATLAS in ids


def test_modelos_retrocompativeis_suplementos():
    p = Personagem()
    assert set(p.suplementos_ativos) == set(LIVROS_OFICIAIS)
    assert p.distincoes == []
    assert p.complicacoes == []

    p.classes.append(ClasseInfo(nome="Guerreiro", nivel=5, primaria=True, variante="Inovador"))
    p.distincoes.append(DistincaoPersonagem(nome="Gigante Furioso", admitido=True, poderes=["Fúria dos Gigantes"], fonte=FONTE_HEROIS))
    p.complicacoes.append(ComplicacaoPersonagem(nome="Cabeça Quente", poder_bonus="Reflexos de Combate", fonte=FONTE_HEROIS))
    assert p.classes[0].variante == "Inovador"
    assert p.distincoes[0].nome == "Gigante Furioso"
    assert p.complicacoes[0].poder_bonus == "Reflexos de Combate"


def test_enriquecimento_fonte_nos_catalogos():
    racas_todas = obter_detalhes_racas(incluir_suplementos=True)
    assert racas_todas["Humano"]["fonte"] == FONTE_LIVRO_BASICO
    assert racas_todas["Duende"]["fonte"] == FONTE_HEROIS
    assert racas_todas["Orc"]["fonte"] == FONTE_AMEACAS

    classes = obter_detalhes_classes()
    assert classes["Guerreiro"]["fonte"] == FONTE_LIVRO_BASICO
    assert classes["Frade"]["fonte"] == FONTE_HEROIS
    assert classes["Treinador"]["fonte"] == FONTE_HEROIS

    deuses = obter_detalhes_deuses()
    assert deuses["Khalmyr"]["fonte"] == FONTE_LIVRO_BASICO

    poderes = listar_poderes_categorizados()
    assert len(poderes) > 0
    assert all(isinstance(p.get("fonte"), str) and p["fonte"] for p in poderes)
