"""Catálogo oficial de livros/suplementos de Tormenta20 e helpers de rastreamento de fonte."""
from typing import Dict, Any

FONTE_LIVRO_BASICO = "T20 JdA"
FONTE_AMEACAS = "Ameaças de Arton"
FONTE_HEROIS = "Heróis de Arton"
FONTE_DEUSES = "Deuses de Arton"
FONTE_ATLAS = "Atlas de Arton"

LIVROS_OFICIAIS = [
    FONTE_LIVRO_BASICO,
    FONTE_AMEACAS,
    FONTE_HEROIS,
    FONTE_DEUSES,
    FONTE_ATLAS,
]

SUPLEMENTOS_CATALOGO = [
    {
        "id": FONTE_LIVRO_BASICO,
        "nome": "Tormenta20 — Jogo do Ano",
        "sigla": "JdA",
        "cor": "#b71c1c",
        "basico": True,
        "descricao": "Livro Básico (edição Jogo do Ano).",
    },
    {
        "id": FONTE_AMEACAS,
        "nome": "Ameaças de Arton",
        "sigla": "Ameaças",
        "cor": "#6a1b9a",
        "basico": False,
        "descricao": "Raças jogáveis de ameaças, equipamentos, materiais especiais, poderes e parceiros.",
    },
    {
        "id": FONTE_HEROIS,
        "nome": "Heróis de Arton",
        "sigla": "Heróis",
        "cor": "#1565c0",
        "basico": False,
        "descricao": "Novas classes (Frade, Treinador), variantes, distinções, complicações, poderes e itens.",
    },
    {
        "id": FONTE_DEUSES,
        "nome": "Deuses de Arton",
        "sigla": "Deuses",
        "cor": "#c77800",
        "basico": False,
        "descricao": "Expansão dos 20 Deuses Maiores, Deuses Menores, poderes concedidos e magias divinas.",
    },
    {
        "id": FONTE_ATLAS,
        "nome": "Atlas de Arton",
        "sigla": "Atlas",
        "cor": "#2e7d32",
        "basico": False,
        "descricao": "Origens regionais e equipamentos de Arton.",
    },
]

# Mapeamento de fallback para entradas de suplementos já existentes nos catálogos
_RACAS_HEROIS = {"Duende", "Eiradaan", "Galokk", "Meio-Elfo", "Sátiro"}
_CLASSES_HEROIS = {"Frade", "Treinador"}


def inferir_fonte(tipo: str, nome: str, dados: Dict[str, Any]) -> str:
    """Retorna a fonte oficial de uma entidade, respeitando o campo explícito se já existir."""
    explicita = dados.get("fonte")
    if isinstance(explicita, str) and explicita.strip():
        return explicita.strip()

    if tipo == "raca":
        if nome in _RACAS_HEROIS:
            return FONTE_HEROIS
        return FONTE_AMEACAS

    if tipo == "classe":
        if nome in _CLASSES_HEROIS:
            return FONTE_HEROIS
        return FONTE_LIVRO_BASICO

    return FONTE_LIVRO_BASICO


def enriquecer_catalogo_com_fonte(catalogo: Dict[str, Dict[str, Any]], tipo: str) -> Dict[str, Dict[str, Any]]:
    """Retorna cópia rasa do catálogo garantindo o campo 'fonte' em cada item."""
    resultado: Dict[str, Dict[str, Any]] = {}
    for nome, dados in catalogo.items():
        if isinstance(dados, dict):
            item = dict(dados)
            item["fonte"] = inferir_fonte(tipo, nome, dados)
            resultado[nome] = item
        else:
            resultado[nome] = dados
    return resultado
