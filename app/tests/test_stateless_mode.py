# -*- coding: utf-8 -*-
"""Testes do modo stateless (Vercel + Render sem banco de dados / localStorage)."""
import asyncio
from types import SimpleNamespace

from src.models import Atributos, Cabecalho, ClasseInfo, DistincaoPersonagem, Personagem
from src.routers.ameacas import listar_ameacas, obter_ameaca
from src.routers.pdf import exportar_odt_stateless
from src.routers.personagens import (
    ativar_habilidade_stateless,
    calcular_personagem_stateless,
)


def _req_sem_db():
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(db=None)))


def test_calcular_e_ativar_stateless_sem_banco():
    f = Personagem(
        cabecalho=Cabecalho(nome="Herói Local", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=7, primaria=True)],
        atributos_base=Atributos(forca=3, destreza=2, constituicao=2, inteligencia=1, sabedoria=1, carisma=1),
        distincoes=[DistincaoPersonagem(nome="Campeão de Dojo", admitido=True, poderes=["Golpe Concentrado"])],
    )
    calc = asyncio.run(calcular_personagem_stateless(f))
    assert calc.status.pv.maximo > 0
    assert calc.status.pm.maximo > 0

    res = asyncio.run(
        ativar_habilidade_stateless(
            {"personagem": calc.model_dump(mode="json"), "nome": "Golpe Concentrado"}
        )
    )
    assert res["resultado"]["sucesso"] is True
    assert res["resultado"]["custo_pm"] == 2
    assert res["personagem"].status.pm.atual == calc.status.pm.maximo - 2


def test_bestiario_e_exportacao_odt_funcionam_sem_mongodb():
    lista = asyncio.run(listar_ameacas(_req_sem_db(), nd=None, tipo=None, papel=None, limite=500))
    assert len(lista) == 285
    assert lista[0]["_id"] == "seed-0"

    am = asyncio.run(obter_ameaca("seed-0", _req_sem_db()))
    assert am.nome == lista[0]["nome"]

    f = Personagem(
        cabecalho=Cabecalho(nome="Export Local", raca="Humano"),
        classes=[ClasseInfo(nome="Guerreiro", nivel=1, primaria=True)],
    )
    resp = asyncio.run(exportar_odt_stateless(f))
    assert resp.status_code == 200
    assert len(resp.body) > 1000
