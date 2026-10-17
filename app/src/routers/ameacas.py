from fastapi import APIRouter, HTTPException, Query, Request, status
from pymongo import ReturnDocument
from bson import ObjectId
from typing import List, Optional
from src.models import Ameaca
from src.dependencies import get_db

router = APIRouter(prefix="/ameacas", tags=["Ameaças"])


def _parse_id(ameaca_id: str):
    """Tenta converter para ObjectId; se falhar, usa string (fixtures de teste)."""
    try:
        return ObjectId(ameaca_id)
    except Exception:
        return ameaca_id


@router.post("/", response_model=Ameaca, status_code=status.HTTP_201_CREATED)
async def criar_ameaca(ameaca: Ameaca, request: Request):
    db = get_db(request)
    ameaca_dict = ameaca.model_dump(by_alias=True, mode="json", exclude={"id"})
    nova = await db["ameacas"].insert_one(ameaca_dict)
    criada = await db["ameacas"].find_one({"_id": nova.inserted_id})
    return criada


@router.get("/", response_model=List[Ameaca])
async def listar_ameacas(
    request: Request,
    nd: Optional[str] = Query(None, description="Filtra por ND exato (ex: '3', '1/2', 'S+')"),
    tipo: Optional[str] = Query(None, description="Filtra por tipo (ex: 'Monstro', 'Morto-vivo')"),
    papel: Optional[str] = Query(None, description="solo | lacaio | especial"),
    limite: int = Query(100, ge=1, le=500),
):
    db = get_db(request)
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
