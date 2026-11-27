from fastapi import APIRouter
from typing import Dict, Optional
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
from src.dados_equipamentos import DADOS_ARMAS, DADOS_ARMADURAS, DADOS_GERAIS
from src.dados_suplementos import (
    FONTE_LIVRO_BASICO,
    SUPLEMENTOS_CATALOGO,
    enriquecer_catalogo_com_fonte,
    inferir_fonte,
)

router = APIRouter(tags=["Dados"])


@router.get("/dados/suplementos", tags=["Dados Estáticos"])
def listar_suplementos():
    """Catálogo oficial de livros e suplementos suportados."""
    return SUPLEMENTOS_CATALOGO


def _filtrar_racas(incluir_suplementos: bool = False, fonte: Optional[str] = None) -> Dict:
    enriquecidas = enriquecer_catalogo_com_fonte(DADOS_RACAS, "raca")
    if fonte:
        return {k: v for k, v in enriquecidas.items() if v.get("fonte") == fonte}
    if incluir_suplementos:
        return enriquecidas
    return {k: v for k, v in enriquecidas.items() if v.get("fonte") == FONTE_LIVRO_BASICO}


@router.get("/racas")
def listar_nomes_racas(incluir_suplementos: bool = False, fonte: Optional[str] = None):
    return sorted(list(_filtrar_racas(incluir_suplementos=incluir_suplementos, fonte=fonte).keys()))

@router.get("/dados/racas", tags=["Dados Estáticos"])
def obter_detalhes_racas(incluir_suplementos: bool = False, fonte: Optional[str] = None):
    return _filtrar_racas(incluir_suplementos=incluir_suplementos, fonte=fonte)

@router.get("/classes")
def listar_nomes_classes():
    return sorted(list(DADOS_CLASSES.keys()))

@router.get("/dados/classes", tags=["Dados Estáticos"])
def obter_detalhes_classes():
    return enriquecer_catalogo_com_fonte(DADOS_CLASSES, "classe")

@router.get("/origens")
def listar_nomes_origens():
    return sorted(list(DADOS_ORIGENS.keys()))

@router.get("/dados/origens", tags=["Dados Estáticos"])
def listar_detalhes_origens():
    return enriquecer_catalogo_com_fonte(DADOS_ORIGENS, "origem")

@router.get("/pericias")
def listar_nomes_pericias():
    return sorted(list(DADOS_PERICIAS.keys()))

@router.get("/dados/habilidades", tags=["Dados Estáticos"])
def listar_detalhes_habilidades():
    return enriquecer_catalogo_com_fonte(HABILIDADES_GERAIS, "habilidade")

@router.get("/dados/habilidades-classe", tags=["Dados Estáticos"])
def listar_habilidades_classe():
    return enriquecer_catalogo_com_fonte(DADOS_HABILIDADES_CLASSE, "habilidade_classe")

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
    return enriquecer_catalogo_com_fonte(DADOS_DEUSES, "deus")

@router.get("/dados/poderes-concedidos", tags=["Dados Estáticos"])
def listar_poderes_concedidos():
    return enriquecer_catalogo_com_fonte(DADOS_PODERES_CONCEDIDOS, "poder_concedido")

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
            elif "Raça" in tipo:
                categoria = "Raça"
            elif "Grupo" in tipo:
                categoria = "Grupo"
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": categoria,
                "descricao": dados.get("descricao", ""),
                "requisitos": dados.get("requisitos", []),
                "is_general": True,
                "fonte": inferir_fonte("habilidade", chave, dados),
            })
            nomes_adicionados.add(dados["nome"])

    for nome, dados in DADOS_PODERES_CONCEDIDOS.items():
        if dados["nome"] not in nomes_adicionados:
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": "Poder Concedido",
                "descricao": dados.get("descricao", ""),
                "requisitos": [],
                "is_general": False,
                "fonte": inferir_fonte("poder_concedido", nome, dados),
            })
            nomes_adicionados.add(dados["nome"])

    for nome, dados in DADOS_PODERES_TORMENTA.items():
        if dados["nome"] not in nomes_adicionados:
            lista_poderes.append({
                "nome": dados["nome"],
                "categoria": "Tormenta",
                "descricao": dados.get("descricao", ""),
                "requisitos": dados.get("requisitos", []),
                "is_general": True,
                "fonte": inferir_fonte("poder_tormenta", nome, dados),
            })
            nomes_adicionados.add(dados["nome"])

    for raca_nome, raca_dados in DADOS_RACAS.items():
        if raca_nome == "Osteon":
            continue
        fonte_raca = inferir_fonte("raca", raca_nome, raca_dados)
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
                    "is_general": False,
                    "fonte": fonte_raca,
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


@router.get("/dados/escolhas", tags=["Dados Estáticos"])
def get_dados_escolhas():
    """Catálogo único de opções de escolha (fonte de verdade p/ frontend)."""
    from src.dados_escolhas import montar_catalogo_escolhas
    return montar_catalogo_escolhas()


@router.get("/dados/equipamentos", tags=["Dados Estáticos"])
async def get_equipamentos():
    """Catálogo de armas (T3-3), armaduras/escudos (T3-5), itens gerais e itens mágicos de suplementos."""
    from src.dados_equipamentos_herois import DADOS_ITENS_MAGICOS_HEROIS
    return {
        "armas": DADOS_ARMAS,
        "armaduras": DADOS_ARMADURAS,
        "gerais": DADOS_GERAIS,
        "itens_magicos_herois": DADOS_ITENS_MAGICOS_HEROIS,
    }


@router.get("/dados/regras-opcionais", tags=["Dados Estáticos"])
def get_regras_opcionais():
    """Catálogo oficial de Regras Opcionais (Heróis de Arton, Cap. 4)."""
    from src.dados_regras_opcionais_herois import obter_catalogo_regras_opcionais
    return obter_catalogo_regras_opcionais()


@router.get("/dados/duende/sonhos-malucos", tags=["Dados Estáticos"])
def rolar_duende_sonhos_malucos(seed: Optional[int] = None):
    """Gera um Duende aleatório oficial (1d3, 1d4, 2d6, 3d12 + 2 PM — Heróis de Arton, p. 9)."""
    from src.regras.duende import gerar_duende_aleatorio
    return gerar_duende_aleatorio(seed=seed)


@router.get("/dados/treinador", tags=["Dados Estáticos"])
def get_dados_treinador():
    """Catálogo oficial da classe Treinador: habilidades, mascotes, tipos e truques do Melhor Amigo."""
    from src.dados_treinador_herois import obter_catalogo_treinador
    return obter_catalogo_treinador()


@router.get("/dados/distincoes", tags=["Dados Estáticos"])
def get_dados_distincoes():
    """Catálogo oficial das 36 Distinções — Heróis de Arton (Cap. 2, p. 104–211)."""
    from src.dados_distincoes_herois import (
        DADOS_DISTINCOES_HEROIS,
        REGRAS_DISTINCOES_GERAIS,
    )
    return {
        "regras": REGRAS_DISTINCOES_GERAIS,
        "distincoes": DADOS_DISTINCOES_HEROIS,
    }
