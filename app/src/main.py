import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.routers import dados, personagens, admin

MONGO_URL = os.getenv("MONGO_URI", "mongodb://db:27017/tormenta20")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🔄 Conectando ao MongoDB em: {MONGO_URL} ...")
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        await client.server_info()
        app.state.mongo_client = client
        app.state.db = client.get_database("tormenta20")
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

app.include_router(dados.router)
app.include_router(personagens.router)
app.include_router(admin.router)