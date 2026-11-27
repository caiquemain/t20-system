import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.routers import dados, personagens, ameacas, admin, pdf, historico

MONGO_URL = os.getenv("MONGO_URI", "mongodb://db:27017/tormenta20")
STORAGE_MODE = os.getenv("STORAGE_MODE", "mongo").strip().lower()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = None
    app.state.db = None
    client = None

    if STORAGE_MODE == "stateless" or not MONGO_URL:
        print("⚡ API iniciada em modo STATELESS (sem MongoDB — fichas no localStorage do navegador).")
    else:
        print(f"🔄 Conectando ao MongoDB em: {MONGO_URL} ...")
        last_error = None
        for tentativa in range(1, 6):
            try:
                client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
                await client.server_info()
                app.state.mongo_client = client
                app.state.db = client.get_database("tormenta20")
                print("✅ Conectado com sucesso!")
                try:
                    await ameacas.garantir_seed_bestiario(app.state.db)
                except Exception as seed_err:
                    print(f"⚠️ Aviso ao popular bestiário: {seed_err}")
                last_error = None
                break
            except Exception as e:
                last_error = e
                print(f"⚠️ Tentativa {tentativa}/5 falhou ao conectar no Banco: {e}")
                if client:
                    client.close()
                    client = None
                if tentativa < 5:
                    await asyncio.sleep(2)

        if last_error is not None:
            print(f"❌ Erro ao conectar no Banco após 5 tentativas: {last_error}")

    try:
        yield
    finally:
        if client:
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

app.include_router(dados.router)
app.include_router(personagens.router)
app.include_router(ameacas.router)
app.include_router(admin.router)
app.include_router(pdf.router)
app.include_router(historico.router)
