import os
from contextlib import asynccontextmanager
from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Body, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

# Importando Modelos, Regras e DADOS
from src.models import Personagem
from src.regras import atualizar_ficha
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES

# --- CONFIGURAÇÃO ---
MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017/tormenta20")

# --- CICLO DE VIDA ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_database()
    app.mongodb = db
    print(f"✅ Conectado ao MongoDB em: {MONGO_URL}")
    yield
    client.close()
    print("🛑 Desconectado do MongoDB")

app = FastAPI(
    title="Tormenta 20 System API",
    description="API inteligente para fichas de T20",
    version="1.3.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTAS AUXILIARES ---


@app.get("/racas", tags=["Dados"])
def listar_opcoes_racas():
    return sorted(list(DADOS_RACAS.keys()))


@app.get("/classes", tags=["Dados"])
def listar_opcoes_classes():
    return sorted(list(DADOS_CLASSES.keys()))

# --- ROTAS DE PERSONAGEM (CRUD) ---


@app.get("/", tags=["Health"])
async def root():
    return {"status": "online", "system": "T20 RPG"}


@app.post("/personagens/", response_model=Personagem, status_code=status.HTTP_201_CREATED, tags=["Personagens"])
async def criar_personagem(personagem: Personagem):
    personagem_calculado = atualizar_ficha(personagem)
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True, mode='json')
    novo_personagem = await app.mongodb["personagens"].insert_one(personagem_dict)
    criado = await app.mongodb["personagens"].find_one({"_id": novo_personagem.inserted_id})
    return criado


@app.get("/personagens/", response_model=List[Personagem], tags=["Personagens"])
async def listar_personagens():
    personagens = await app.mongodb["personagens"].find().to_list(100)
    return personagens


@app.get("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def obter_personagem(personagem_id: UUID):
    personagem = await app.mongodb["personagens"].find_one({"_id": str(personagem_id)})
    if personagem is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")
    return personagem


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

# --- NOVAS ROTAS DE DELETAR ---


@app.delete("/personagens/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Personagens"])
async def deletar_personagem(personagem_id: UUID):
    delete_result = await app.mongodb["personagens"].delete_one({"_id": str(personagem_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado para deleção")

    return None


@app.delete("/personagens/", tags=["Admin"])
async def deletar_todos_personagens():
    """PERIGO: Apaga todas as fichas do banco."""
    result = await app.mongodb["personagens"].delete_many({})
    return {"mensagem": f"{result.deleted_count} fichas foram apagadas."}
