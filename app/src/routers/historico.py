"""Histórico da ficha (o "git" da ficha): level-up com memória,
linha do tempo consultável e restauração via snapshots.

Regras de ouro:
- Append-only: nunca deletar ou reescrever eventos.
- Restaurar = criar evento novo apontando para o snapshot antigo.
"""
import logging
from datetime import datetime
from typing import Any, Dict

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..dependencies import get_db
from ..models import Personagem
from ..regras import atualizar_ficha
from ..regras.historico import resumir_mudancas

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/personagens", tags=["Histórico"])


class LevelUpRequest(BaseModel):
    escolhas: Dict[str, Any] = Field(default_factory=dict)  # MVP: vazio


def _oid(valor: str) -> ObjectId:
    try:
        return ObjectId(valor)
    except Exception:
        raise HTTPException(status_code=404, detail="ID inválido")


async def _buscar_personagem(db, personagem_id: str) -> Personagem:
    doc = await db.personagens.find_one({"_id": _oid(personagem_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return Personagem(**doc)


def _recalcular(ficha: Personagem) -> Personagem:
    resultado = atualizar_ficha(ficha)
    return resultado if isinstance(resultado, Personagem) else ficha


def _dump(ficha: Personagem) -> dict:
    return ficha.model_dump(by_alias=True, exclude={"id"}, mode="json")


async def _gravar_evento(db, evento: dict) -> str:
    resultado = await db.historico.insert_one(evento)
    return str(resultado.inserted_id)


@router.post("/{personagem_id}/level-up")
async def level_up(personagem_id: str, payload: LevelUpRequest = LevelUpRequest(), db=Depends(get_db)):
    """Sobe 1 nível, recalcula a ficha e grava evento com snapshot."""
    antes = await _buscar_personagem(db, personagem_id)

    if not antes.classes:
        raise HTTPException(status_code=400, detail="Ficha sem classe: impossível subir de nível")
    nivel_atual = antes.classes[0].nivel
    if nivel_atual >= 20:
        raise HTTPException(status_code=400, detail="Nível 20 é o máximo do T20")

    # 1. Sobe o nível
    depois = antes.model_copy(deep=True)
    depois.classes[0].nivel = nivel_atual + 1
    depois.cabecalho.nivel_total = max(depois.cabecalho.nivel_total, nivel_atual + 1)

    # 2. Motor recalcula TUDO (fonte única de verdade)
    depois = _recalcular(depois)

    # 3. Resumo vem do diff (nunca mente)
    resumo = resumir_mudancas(antes, depois)

    # 4. Persiste a ficha
    doc = _dump(depois)
    await db.personagens.update_one({"_id": _oid(personagem_id)}, {"$set": doc})

    # 5. Evento com snapshot (time machine)
    evento_id = await _gravar_evento(db, {
        "personagem_id": personagem_id,
        "tipo": "level_up",
        "nivel": depois.cabecalho.nivel_total,
        "resumo": resumo,
        "escolhas": payload.escolhas,
        "snapshot": doc,
        "criado_em": datetime.utcnow(),
    })

    logger.info(f"[HISTORICO] level-up {personagem_id}: nv {depois.cabecalho.nivel_total} | {resumo}")
    return {"evento_id": evento_id, "nivel": depois.cabecalho.nivel_total, "resumo": resumo}


@router.get("/{personagem_id}/historico")
async def listar_historico(personagem_id: str, db=Depends(get_db)):
    """Linha do tempo leve (sem snapshots)."""
    _oid(personagem_id)
    eventos = []
    cursor = db.historico.find({"personagem_id": personagem_id}, {"snapshot": 0}).sort("criado_em", 1)
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        eventos.append(doc)
    return eventos


@router.get("/{personagem_id}/historico/{evento_id}")
async def ver_evento(personagem_id: str, evento_id: str, db=Depends(get_db)):
    """Evento completo, incluindo snapshot."""
    doc = await db.historico.find_one({"_id": _oid(evento_id), "personagem_id": personagem_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/{personagem_id}/historico/{evento_id}/restaurar")
async def restaurar_evento(personagem_id: str, evento_id: str, db=Depends(get_db)):
    """Restaura a ficha ao snapshot do evento (sem apagar histórico)."""
    evento = await db.historico.find_one({"_id": _oid(evento_id), "personagem_id": personagem_id})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    snapshot = evento.get("snapshot")
    if not snapshot:
        raise HTTPException(status_code=400, detail="Evento não possui snapshot")

    ficha = _recalcular(Personagem(**snapshot))
    doc = _dump(ficha)
    await db.personagens.update_one({"_id": _oid(personagem_id)}, {"$set": doc})

    novo_id = await _gravar_evento(db, {
        "personagem_id": personagem_id,
        "tipo": "restauracao",
        "nivel": ficha.cabecalho.nivel_total,
        "resumo": [f"Ficha restaurada ao estado do evento {evento_id} (nível {evento.get('nivel')})"],
        "escolhas": {"evento_origem": evento_id},
        "snapshot": doc,
        "criado_em": datetime.utcnow(),
    })
    return {"evento_id": novo_id, "restaurado_de": evento_id}
