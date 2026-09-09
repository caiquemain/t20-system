from fastapi import APIRouter, Request
from src.dependencies import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.delete("/limpar-tudo")
async def limpar_banco(request: Request):
    db = get_db(request)
    await db["personagens"].delete_many({})
    return {"message": "Banco de dados limpo com sucesso!"}