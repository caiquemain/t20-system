from fastapi import APIRouter
from typing import Dict
from src.models import Magia
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
from src.dados_poderes_tormenta import DADOS_PODERES_TORMENTA

router = APIRouter(tags=["Dados"])

@router.get("/racas")
def listar_nomes_racas():
    return sorted(list(DADOS_RACAS.keys()))

@router.get("/dados/racas", tags=["Dados Estáticos"])
def obter_detalhes_racas():
    return DADOS_RACAS

@router.get("/classes")
def listar_nomes_classes():
    return sorted(list(DADOS_CLASSES.keys()))

@router.get("/dados/classes", tags=["Dados Estáticos"])
def obter_detalhes_classes():
    return DADOS_CLASSES

@router.get("/origens")
def listar_nomes_origens():
    return sorted(list(DADOS_ORIGENS.keys()))

@router.get("/dados/origens", tags=["Dados Estáticos"])
def listar_detalhes_origens():
    return DADOS_ORIGENS

@router.get("/pericias")
def listar_nomes_pericias():
    return sorted(list(DADOS_PERICIAS.keys()))

@router.get("/dados/habilidades", tags=["Dados Estáticos"])
def listar_detalhes_habilidades():
    return HABILIDADES_GERAIS

@router.get("/dados/habilidades-classe", tags=["Dados Estáticos"])
def listar_habilidades_classe():
    return DADOS_HABILIDADES_CLASSE

@router.get("/dados/magias", response_model=Dict[str, Magia], tags=["Dados Estáticos"])
def get_magias():
    return DADOS_MAGIAS

@router.get("/dados/itens", tags=["Dados Estáticos"])
def listar_itens():
    return DADOS_ITENS

@router.get("/deuses")
def listar_nomes_deuses():
    return sorted(list(DADOS_DEUSES.keys()))

@router.get("/dados/deuses", tags=["Dados Estáticos"])
def obter_detalhes_deuses():
    return DADOS_DEUSES

@router.get("/dados/poderes-concedidos", tags=["Dados Estáticos"])
def listar_poderes_concedidos():
    return DADOS_PODERES_CONCEDIDOS

@router.get("/poderes")
def listar_poderes_categorizados():
    lista_poderes = []
    nomes_adicionados = set()

    for chave, dados in HABILIDADES_GERAIS.items():
        tipo = dados.get("tipo", "")
        if "Poder" in tipo:
            categoria = "Geral"
            if "Combate" in tipo:
                categoria = "Combate"
            elif "Destino" in tipo:
                categoria = "Destino"
            elif "Magia" in tipo:
                categoria = "Magia"
            elif "Tormenta" in tipo:
                categoria = "Tormenta"
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": categoria,
                "descricao": dados.get("descricao", ""),
                "requisitos": dados.get("requisitos", []),
                "is_general": True
            })
            nomes_adicionados.add(dados["nome"])

    for nome, dados in DADOS_PODERES_CONCEDIDOS.items():
        if dados["nome"] not in nomes_adicionados:
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": "Poder Concedido",
                "descricao": dados.get("descricao", ""),
                "requisitos": [],
                "is_general": False
            })
            nomes_adicionados.add(dados["nome"])

    for nome, dados in DADOS_PODERES_TORMENTA.items():
        if dados["nome"] not in nomes_adicionados:
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": "Tormenta",
                "descricao": dados.get("descricao", ""),
                "requisitos": dados.get("requisitos", []),
                "is_general": True
            })
            nomes_adicionados.add(dados["nome"])

    for raca_nome, raca_dados in DADOS_RACAS.items():
        if raca_nome == "Osteon":
            continue
        habilidades_keys = raca_dados.get("habilidades", [])
        for hab_key in habilidades_keys:
            dados = DADOS_HABILIDADES_RACIAIS.get(hab_key) or HABILIDADES_GERAIS.get(hab_key)
            if dados:
                nome_hab = dados["nome"]
                lista_poderes.append({
                    "nome": nome_hab,
                    "categoria": f"Raça: {raca_nome}",
                    "descricao": dados.get("descricao", ""),
                    "requisitos": [],
                    "is_general": False
                })
    return sorted(lista_poderes, key=lambda x: x["nome"])

@router.get("/dados/habilidades-raciais", tags=["Dados Estáticos"])
def get_dados_habilidades_raciais():
    resposta = {}
    for chave, dados in DADOS_HABILIDADES_RACIAIS.items():
        item = dados.copy()
        item["id"] = chave
        resposta[chave] = item
    return resposta

@router.get("/dados/progressao-circulos", tags=["Dados Estáticos"])
def get_progressao_circulos():
    """Tabela oficial de círculos de magia por classe/nível (T20)."""
    from src.dados_progressao_magias import PROGRESSAO_CIRCULOS_POR_CLASSE
    return PROGRESSAO_CIRCULOS_POR_CLASSE
