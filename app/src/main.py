import os
from contextlib import asynccontextmanager
from typing import List, Any, cast
from uuid import UUID

from fastapi import FastAPI, HTTPException, Body, status, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

# --- IMPORTAÇÕES DE DADOS ---
from src.models import Personagem
from src.regras import atualizar_ficha
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_itens import DADOS_ITENS
from src.dados_origens import DADOS_ORIGENS
from src.dados_pericias import DADOS_PERICIAS
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_magias import DADOS_MAGIAS

# --- CONFIGURAÇÃO ---
MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017/tormenta20")

# --- CICLO DE VIDA ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_with_db = cast(Any, app)
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_database()
    app_with_db.mongodb = db
    print(f"✅ Conectado ao MongoDB em: {MONGO_URL}")
    yield
    client.close()
    print("🛑 Desconectado do MongoDB")

app = FastAPI(title="Tormenta 20 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_client(app: FastAPI):
    return cast(Any, app).mongodb

# --- ROTAS DE DADOS ESTÁTICOS ---


@app.get("/racas", tags=["Dados"])
def listar_nomes_racas():
    return sorted(list(DADOS_RACAS.keys()))


@app.get("/dados/racas", tags=["Dados Estáticos"])
def obter_detalhes_racas():
    return DADOS_RACAS


@app.get("/classes", tags=["Dados"])
def listar_nomes_classes():
    return sorted(list(DADOS_CLASSES.keys()))


@app.get("/dados/classes", tags=["Dados Estáticos"])
def obter_detalhes_classes():
    return DADOS_CLASSES


@app.get("/origens", tags=["Dados"])
def listar_nomes_origens():
    return sorted(list(DADOS_ORIGENS.keys()))


@app.get("/dados/origens", tags=["Dados Estáticos"])
def listar_detalhes_origens():
    return DADOS_ORIGENS


@app.get("/pericias", tags=["Dados"])
def listar_nomes_pericias():
    return sorted(list(DADOS_PERICIAS.keys()))


@app.get("/dados/habilidades", tags=["Dados Estáticos"])
def listar_detalhes_habilidades():
    return HABILIDADES_GERAIS


@app.get("/dados/habilidades-classe", tags=["Dados Estáticos"])
def listar_habilidades_classe():
    return DADOS_HABILIDADES_CLASSE


@app.get("/dados/magias", tags=["Dados Estáticos"])
def listar_magias():
    return DADOS_MAGIAS


@app.get("/dados/itens", tags=["Dados Estáticos"])
def listar_itens():
    return DADOS_ITENS

# --- ROTAS DE PERSONAGEM ---


@app.post("/personagens/", response_model=Personagem, status_code=status.HTTP_201_CREATED, tags=["Personagens"])
async def criar_personagem(personagem: Personagem, request: Request):
    db_client = get_db_client(request.app)
    personagem_calculado = atualizar_ficha(personagem)
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True, mode='json')
    novo_personagem = await db_client["personagens"].insert_one(personagem_dict)
    criado = await db_client["personagens"].find_one({"_id": novo_personagem.inserted_id})
    return criado


@app.get("/personagens/", response_model=List[Personagem], tags=["Personagens"])
async def listar_personagens(request: Request):
    db_client = get_db_client(request.app)
    return await db_client["personagens"].find().to_list(100)


@app.get("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def obter_personagem(personagem_id: UUID, request: Request):
    db_client = get_db_client(request.app)
    personagem = await db_client["personagens"].find_one({"_id": str(personagem_id)})
    if personagem is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")
    personagem_obj = Personagem.model_validate(personagem)
    return atualizar_ficha(personagem_obj)


@app.put("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def atualizar_personagem(personagem_id: UUID, personagem: Personagem, request: Request):
    db_client = get_db_client(request.app)
    personagem_calculado = atualizar_ficha(personagem)
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True, mode='json', exclude_unset=True)
    result = await db_client["personagens"].find_one_and_update(
        {"_id": str(personagem_id)},
        {"$set": personagem_dict},
        return_document=ReturnDocument.AFTER
    )
    if result is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")
    return result


@app.delete("/personagens/{personagem_id}", status_code=204, tags=["Personagens"])
async def deletar_personagem(personagem_id: UUID, request: Request):
    db_client = get_db_client(request.app)
    await db_client["personagens"].delete_one({"_id": str(personagem_id)})
    return None

# --- ROTA CORRIGIDA: INCLUI REQUISITOS ---


@app.get("/poderes", tags=["Dados"])
def listar_poderes_categorizados():
    lista_poderes = []
    for chave, dados in HABILIDADES_GERAIS.items():
        tipo = dados.get("tipo", "")
        if "Poder" in tipo or "Origem" in tipo:
            categoria = "Geral"
            if "Combate" in tipo:
                categoria = "Combate"
            elif "Destino" in tipo:
                categoria = "Destino"
            elif "Magia" in tipo:
                categoria = "Magia"
            elif "Concedido" in tipo:
                categoria = "Concedido"
            elif "Tormenta" in tipo:
                categoria = "Tormenta"
            elif "Origem" in tipo:
                categoria = "Origem"

            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": categoria,
                "descricao": dados.get("descricao", ""),
                # <--- LINHA CRUCIAL ADICIONADA
                "requisitos": dados.get("requisitos", [])
            })
    return sorted(lista_poderes, key=lambda x: x["nome"])
