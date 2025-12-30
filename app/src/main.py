import os
from contextlib import asynccontextmanager
from typing import List, Any, cast, Optional
from bson import ObjectId  # Importante para IDs do Mongo
from typing import Dict

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
from src.dados_deuses import DADOS_DEUSES
from src.dados_poderes_concedidos import DADOS_PODERES_CONCEDIDOS
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from src.models import Magia
# --- CONFIGURAÇÃO ---
# Prioriza o nome do host 'db' (Docker), fallback para localhost
MONGO_URL = os.getenv("MONGO_URI", "mongodb://db:27017/tormenta20")

# --- CICLO DE VIDA ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🔄 Conectando ao MongoDB em: {MONGO_URL} ...")
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        # Testa a conexão
        await client.server_info()
        app.state.mongo_client = client
        app.state.db = client.get_database(
            "tormenta20")  # Força o nome do banco
        print(f"✅ Conectado com sucesso!")
        yield
        client.close()
        print("🛑 Desconectado do MongoDB")
    except Exception as e:
        print(f"❌ Erro ao conectar no Banco: {e}")
        yield

app = FastAPI(title="Tormenta 20 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db(request: Request):
    return request.app.state.db

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


@app.get("/dados/magias", response_model=Dict[str, Magia]) 
def get_magias():
    return DADOS_MAGIAS

@app.get("/dados/itens", tags=["Dados Estáticos"])
def listar_itens():
    return DADOS_ITENS

# --- NOVAS ROTAS (DEUSES E PODERES) ---


@app.get("/deuses", tags=["Dados"])
def listar_nomes_deuses():
    return sorted(list(DADOS_DEUSES.keys()))


@app.get("/dados/deuses", tags=["Dados Estáticos"])
def obter_detalhes_deuses():
    return DADOS_DEUSES


@app.get("/dados/poderes-concedidos", tags=["Dados Estáticos"])
def listar_poderes_concedidos():
    return DADOS_PODERES_CONCEDIDOS


@app.get("/poderes", tags=["Dados"])
def listar_poderes_categorizados():
    """
    Retorna uma lista unificada de Poderes Gerais e Poderes Concedidos
    para ser usada nos seletores do Frontend.
    """
    lista_poderes = []

    # 1. Processar Habilidades Gerais
    for chave, dados in HABILIDADES_GERAIS.items():
        tipo = dados.get("tipo", "")
        # Filtra apenas o que é considerado "Poder" de compra ou Origem
        if "Poder" in tipo or "Origem" in tipo:
            categoria = "Geral"
            if "Combate" in tipo:
                categoria = "Combate"
            elif "Destino" in tipo:
                categoria = "Destino"
            elif "Magia" in tipo:
                categoria = "Magia"
            elif "Tormenta" in tipo:
                categoria = "Tormenta"
            elif "Origem" in tipo:
                categoria = "Origem"

            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": categoria,
                "descricao": dados.get("descricao", ""),
                "requisitos": dados.get("requisitos", [])
            })

    # 2. Processar Poderes Concedidos
    for nome, dados in DADOS_PODERES_CONCEDIDOS.items():
        lista_poderes.append({
            "nome": dados["nome"],
            "categoria": "Poder Concedido",
            "descricao": dados.get("descricao", ""),
            "requisitos": []
        })

    return sorted(lista_poderes, key=lambda x: x["nome"])

# --- ROTAS DE PERSONAGEM (CRUD) ---


@app.post("/personagens/", response_model=Personagem, status_code=status.HTTP_201_CREATED, tags=["Personagens"])
async def criar_personagem(personagem: Personagem, request: Request):
    db = get_db(request)

    # 1. Recalcula Regras (PV, PM, Habilidades Iniciais)
    personagem_calculado = atualizar_ficha(personagem)

    # 2. Prepara JSON (EXCLUI O ID para o Mongo gerar um novo)
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True,
        mode='json',
        exclude={"id"}  # Importante!
    )

    # 3. Insere
    novo_personagem = await db["personagens"].insert_one(personagem_dict)

    # 4. Retorna o objeto criado
    criado = await db["personagens"].find_one({"_id": novo_personagem.inserted_id})
    return criado


@app.get("/personagens/", response_model=List[Personagem], tags=["Personagens"])
async def listar_personagens(request: Request):
    db = get_db(request)
    # Retorna lista (limitada a 100 para segurança)
    return await db["personagens"].find().to_list(100)


@app.get("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def obter_personagem(personagem_id: str, request: Request):
    db = get_db(request)

    # Tenta converter string para ObjectId
    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id  # Tenta buscar como string se falhar (legado)

    personagem = await db["personagens"].find_one({"_id": query_id})

    if personagem is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")

    # Converte e Atualiza (Garante que regras novas se apliquem a fichas salvas)
    personagem_obj = Personagem.model_validate(personagem)
    return atualizar_ficha(personagem_obj)


@app.put("/personagens/{personagem_id}", response_model=Personagem, tags=["Personagens"])
async def atualizar_personagem(personagem_id: str, personagem: Personagem, request: Request):
    db = get_db(request)

    # Recalcula regras antes de salvar
    personagem_calculado = atualizar_ficha(personagem)

    # Prepara dados, excluindo ID para não sobrescrever a chave primária
    personagem_dict = personagem_calculado.model_dump(
        by_alias=True,
        mode='json',
        exclude={"id"}
    )

    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id

    # Find One and Update retorna o documento ATUALIZADO
    result = await db["personagens"].find_one_and_update(
        {"_id": query_id},
        {"$set": personagem_dict},
        return_document=ReturnDocument.AFTER
    )

    if result is None:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")

    return result


@app.delete("/personagens/{personagem_id}", status_code=204, tags=["Personagens"])
async def deletar_personagem(personagem_id: str, request: Request):
    db = get_db(request)

    try:
        query_id = ObjectId(personagem_id)
    except:
        query_id = personagem_id

    resultado = await db["personagens"].delete_one({"_id": query_id})

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Personagem não encontrado")

    return None


@app.delete("/admin/limpar-tudo", tags=["Admin"])
async def limpar_banco(request: Request):
    """Apaga TODOS os personagens. Use com cuidado!"""
    db = get_db(request)
    await db["personagens"].delete_many({})
    return {"message": "Banco de dados limpo com sucesso!"}
