from fastapi import APIRouter, HTTPException, Request, status
from pymongo import ReturnDocument
from bson import ObjectId
from typing import List
from src.models import Personagem
from src.regras import atualizar_ficha
from src.dependencies import get_db

router = APIRouter(prefix="/personagens", tags=["Personagens"])

@router.post("/", response_model=Personagem, status_code=status.HTTP_201_CREATED)
async def criar_personagem(personagem: Personagem, request: Request):
    db = get_db(request)
    personagem_calculado = atualizar_ficha(personagem)
    personagem_dict = personagem_calculado.model_dump(by_alias=True, mode='json', exclude={"id"})
    novo_personagem = await db["personagens"].insert_one(personagem_dict)
    criado = await db["personagens"].find_one({"_id": novo_personagem.inserted_id})
    return criado

@router.get("/", response_model=List[Personagem])
async def listar_personagens(request: Request):
    db = get_db(request)
    return await db["personagens"].find().to_list(100)

@router.get("/{personagem_id}", response_model=Personagem)
async def obter_personagem(personagem_id: str, request: Request):
    db = get_db(request)
    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id
    personagem = await db["personagens"].find_one({"_id": query_id})
    if personagem is None:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    personagem_obj = Personagem.model_validate(personagem)
    return atualizar_ficha(personagem_obj)

@router.put("/{personagem_id}", response_model=Personagem)
async def atualizar_personagem(personagem_id: str, personagem: Personagem, request: Request):
    db = get_db(request)
    personagem_calculado = atualizar_ficha(personagem)
    personagem_dict = personagem_calculado.model_dump(by_alias=True, mode='json', exclude={"id"})
    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id
    
    result = await db["personagens"].find_one_and_update(
        {"_id": query_id}, 
        {"$set": personagem_dict}, 
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return result

@router.delete("/{personagem_id}", status_code=204)
async def deletar_personagem(personagem_id: str, request: Request):
    db = get_db(request)
    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id
    resultado = await db["personagens"].delete_one({"_id": query_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return None