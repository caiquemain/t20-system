import os
from contextlib import asynccontextmanager
from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Body, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

# Importando Modelos e Regras
from src.models import Personagem
from src.regras import atualizar_ficha

# --- CONFIGURAÇÃO ---
MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017/tormenta20")

# --- CICLO DE VIDA ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conexão ao iniciar
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_database()
    app.mongodb = db
    print(f"✅ Conectado ao MongoDB em: {MONGO_URL}")

    yield

    # Desconexão ao desligar
    client.close()
    print("🛑 Desconectado do MongoDB")

app = FastAPI(
    title="Tormenta 20 System API",
    description="API inteligente para fichas de T20",
    version="1.1.0",
    lifespan=lifespan
)

# --- ROTAS ---


@app.get("/", tags=["Health"])
async def root():
    return {"status": "online", "system": "T20 RPG"}

# 1. CRIAR FICHA (Agora com Regras!)


@app.post("/personagens/", response_model=Personagem, status_code=status.HTTP_201_CREATED, tags=["Personagens"])
async def criar_personagem(personagem: Personagem):
    # 1. Aplica as regras de negócio (Cálculos automáticos)
    # O objeto 'personagem' é modificado in-place e retornado
    personagem_calculado = atualizar_ficha(personagem)

    # 2. Converte para JSON compatível com Mongo
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True, mode='json')

    # 3. Salva no Banco
    novo_personagem = await app.mongodb["personagens"].insert_one(personagem_dict)

    # 4. Retorna o documento salvo
    criado = await app.mongodb["personagens"].find_one({"_id": novo_personagem.inserted_id})
    return criado

# 2. LISTAR TODOS


@app.get("/personagens/", response_model=List[Personagem], tags=["Personagens"])
async def listar_personagens():
    personagens = await app.mongodb["personagens"].find().to_list(100)
    return personagens

# 3. BUSCAR UM


@app.get("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def obter_personagem(personagem_id: UUID):
    personagem = await app.mongodb["personagens"].find_one({"_id": str(personagem_id)})
    if personagem is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")
    return personagem

# 4. ATUALIZAR STATUS RÁPIDO


@app.patch("/personagens/{personagem_id}/status", response_model=Personagem, tags=["Jogabilidade"])
async def atualizar_pv_pm(
    personagem_id: UUID,
    pv_atual: int = Body(None, embed=True),
    pm_atual: int = Body(None, embed=True)
):
    updates = {}
    if pv_atual is not None:
        updates["status.pv.atual"] = pv_atual
    if pm_atual is not None:
        updates["status.pm.atual"] = pm_atual

    if not updates:
        raise HTTPException(status_code=400, detail="Nada para atualizar")

    personagem_atualizado = await app.mongodb["personagens"].find_one_and_update(
        {"_id": str(personagem_id)},
        {"$set": updates},
        return_document=ReturnDocument.AFTER
    )

    if personagem_atualizado is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")

    return personagem_atualizado
