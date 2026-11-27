# -*- coding: utf-8 -*-
"""Testes do seed automático do Bestiário (285 ameaças)."""
import asyncio
from src.models import Ameaca
from src.routers.ameacas import carregar_seed_bestiario, garantir_seed_bestiario


class _FakeCollection:
    def __init__(self):
        self.docs = []

    async def count_documents(self, filtro):
        return len(self.docs)

    async def insert_many(self, docs):
        self.docs.extend(docs)


def test_seed_bestiario_valido_e_idempotente():
    docs = carregar_seed_bestiario()
    assert len(docs) == 285
    # Amostra de validação Pydantic
    for d in (docs[0], docs[len(docs) // 2], docs[-1]):
        am = Ameaca.model_validate(d)
        assert am.nome and am.nd

    fake_db = {"ameacas": _FakeCollection()}
    inseridos_1 = asyncio.run(garantir_seed_bestiario(fake_db))
    assert inseridos_1 == 285
    assert len(fake_db["ameacas"].docs) == 285

    # Segunda execução não duplica
    inseridos_2 = asyncio.run(garantir_seed_bestiario(fake_db))
    assert inseridos_2 == 0
    assert len(fake_db["ameacas"].docs) == 285
