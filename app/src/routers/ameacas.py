import json
import uuid
from pathlib import Path
from fastapi import APIRouter, Body, HTTPException, Query, Request, status
from pymongo import ReturnDocument
from bson import ObjectId
from typing import Any, Dict, List, Optional
from src.models import Ameaca
from src.dependencies import get_db
from src.dados_criacao_ameacas import gerar_ameaca_manual, obter_tabelas_construtor

router = APIRouter(prefix="/ameacas", tags=["Ameaças"])

_SEED_PATH = Path(__file__).resolve().parent.parent / "data" / "bestiario_seed.json"


def carregar_seed_bestiario() -> List[dict]:
    if not _SEED_PATH.exists():
        return []
    return json.loads(_SEED_PATH.read_text(encoding="utf-8"))


async def garantir_seed_bestiario(db) -> int:
    """Popula automaticamente a collection `ameacas` quando estiver vazia."""
    col = db["ameacas"]
    if await col.count_documents({}) > 0:
        return 0
    docs = carregar_seed_bestiario()
    if not docs:
        return 0
    await col.insert_many(docs)
    print(f"🐉 Bestiário populado automaticamente com {len(docs)} ameaças!")
    return len(docs)


def _parse_id(ameaca_id: str):
    """Tenta converter para ObjectId; se falhar, usa string (fixtures de teste)."""
    try:
        return ObjectId(ameaca_id)
    except Exception:
        return ameaca_id


@router.get("/construtor/tabelas")
async def get_tabelas_construtor():
    """Tabelas oficiais do Manual de Criação de Ameaças (Ameaças de Arton, p. 378–390)."""
    return obter_tabelas_construtor()


@router.post("/construtor/gerar", response_model=Ameaca)
async def gerar_ameaca_construtor(payload: Dict[str, Any] = Body(...)):
    """Gera uma ficha de Ameaça balanceada seguindo as Tabelas 2-3 A/B/C oficiais."""
    return gerar_ameaca_manual(
        nome=payload.get("nome", "Nova Ameaça"),
        nd=str(payload.get("nd", "1")),
        papel=payload.get("papel", "solo"),
        tipo=payload.get("tipo", "Monstro"),
        tamanho=payload.get("tamanho", "Médio"),
        res_forte=payload.get("res_forte", "fortitude"),
        res_media=payload.get("res_media", "reflexos"),
        res_fraca=payload.get("res_fraca", "vontade"),
        deslocamento=payload.get("deslocamento"),
        pontos_de_mana=payload.get("pontos_de_mana"),
        sentidos=payload.get("sentidos"),
        ataques=payload.get("ataques"),
        habilidades=payload.get("habilidades"),
        atributos=payload.get("atributos"),
        equipamento=payload.get("equipamento"),
        tesouro=payload.get("tesouro", "Padrão"),
        ajustes=payload.get("ajustes"),
    )


@router.post("/", response_model=Ameaca, status_code=status.HTTP_201_CREATED)
async def criar_ameaca(ameaca: Ameaca, request: Request):
    db = get_db(request)
    ameaca_dict = ameaca.model_dump(by_alias=True, mode="json", exclude={"id"})
    if db is None:
        ameaca_dict["_id"] = f"custom-{uuid.uuid4().hex[:10]}"
        return Ameaca.model_validate(ameaca_dict)
    nova = await db["ameacas"].insert_one(ameaca_dict)
    criada = await db["ameacas"].find_one({"_id": nova.inserted_id})
    return criada


@router.get("/", response_model=List[Ameaca])
async def listar_ameacas(
    request: Request,
    nd: Optional[str] = Query(None, description="Filtra por ND exato (ex: '3', '1/2', 'S+')"),
    tipo: Optional[str] = Query(None, description="Filtra por tipo (ex: 'Monstro', 'Morto-vivo')"),
    papel: Optional[str] = Query(None, description="solo | lacaio | especial"),
    limite: int = Query(500, ge=1, le=1000),
):
    db = get_db(request)
    if db is None:
        docs = carregar_seed_bestiario()
        out = []
        for idx, d in enumerate(docs):
            if nd is not None and str(d.get("nd")) != str(nd):
                continue
            if tipo is not None and d.get("tipo") != tipo:
                continue
            if papel is not None and d.get("papel") != papel:
                continue
            item = dict(d)
            item["_id"] = f"seed-{idx}"
            out.append(item)
            if len(out) >= limite:
                break
        return out

    filtro: dict = {}
    if nd is not None:
        filtro["nd"] = nd
    if tipo is not None:
        filtro["tipo"] = tipo
    if papel is not None:
        filtro["papel"] = papel
    return await db["ameacas"].find(filtro).to_list(limite)


@router.get("/{ameaca_id}", response_model=Ameaca)
async def obter_ameaca(ameaca_id: str, request: Request):
    db = get_db(request)
    if db is None:
        docs = carregar_seed_bestiario()
        if ameaca_id.startswith("seed-"):
            try:
                idx = int(ameaca_id.split("-", 1)[1])
                if 0 <= idx < len(docs):
                    item = dict(docs[idx])
                    item["_id"] = ameaca_id
                    return Ameaca.model_validate(item)
            except ValueError:
                pass
        raise HTTPException(status_code=404, detail="Ameaça não encontrada")
    ameaca = await db["ameacas"].find_one({"_id": _parse_id(ameaca_id)})
    if ameaca is None:
        raise HTTPException(status_code=404, detail="Ameaça não encontrada")
    return Ameaca.model_validate(ameaca)


@router.put("/{ameaca_id}", response_model=Ameaca)
async def atualizar_ameaca(ameaca_id: str, ameaca: Ameaca, request: Request):
    db = get_db(request)
    ameaca_dict = ameaca.model_dump(by_alias=True, mode="json", exclude={"id"})
    result = await db["ameacas"].find_one_and_update(
        {"_id": _parse_id(ameaca_id)},
        {"$set": ameaca_dict},
        return_document=ReturnDocument.AFTER,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Ameaça não encontrada")
    return result


@router.delete("/{ameaca_id}", status_code=204)
async def deletar_ameaca(ameaca_id: str, request: Request):
    db = get_db(request)
    resultado = await db["ameacas"].delete_one({"_id": _parse_id(ameaca_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ameaça não encontrada")
    return None
