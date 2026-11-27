# -*- coding: utf-8 -*-
"""Regras adicionais de Ameaças de Arton (p. 374–375).

- Criaturas e Ataques (Luta/Pontaria, Armas Naturais Tabela 2-1, Removendo Equipamentos)
- CD de Habilidades por categoria (Atléticas, Fisiológicas, Controle, Magias)
- Ameaças e Morte (variante simplificada para lacaios, solos e especiais)
- Condições de Itens (Avariado, Destruído e reparo)
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Tuple

# Tabela 2-1: Armas Naturais (Ameaças de Arton, p. 374)
TABELA_ARMAS_NATURAIS: Dict[str, str] = {
    "Cascos": "Impacto",
    "Cauda": "Impacto",
    "Chifres": "Perfuração",
    "Ferrão": "Perfuração",
    "Garra": "Corte",
    "Marrada": "Impacto",
    "Mordida": "Perfuração",
    "Pancada": "Impacto",
    "Pinça": "Corte",
    "Presas": "Perfuração",
    "Tentáculo": "Impacto",
    "Tromba": "Impacto",
}

# Escada de passos de dano (Tabela 3-2, T20 JdA p. 143)
_PASSOS_DANO = [
    "1", "1d2", "1d3", "1d4", "1d6", "1d8", "1d10", "1d12",
    "3d6", "4d6", "4d8", "4d10", "4d12",
]

_DELTA_PASSO_TAMANHO: Dict[str, int] = {
    "Minúsculo": -1,
    "Pequeno": 0,
    "Médio": 0,
    "Grande": 1,
    "Enorme": 1,
    "Colossal": 2,
}


def ajustar_passo_dano(dado_base: str, passos: int) -> str:
    """Move um dado de dano na escada da Tabela 3-2 (T20 p. 143)."""
    if dado_base not in _PASSOS_DANO:
        return dado_base
    idx = _PASSOS_DANO.index(dado_base)
    novo_idx = max(0, min(len(_PASSOS_DANO) - 1, idx + passos))
    return _PASSOS_DANO[novo_idx]


def dano_arma_natural_por_tamanho(tamanho: str = "Médio") -> str:
    """Dano padrão de arma natural por tamanho (p. 374): 1d6 base (Peq/Méd), -1 Min, +1 Gra/Eno, +2 Col."""
    delta = _DELTA_PASSO_TAMANHO.get(tamanho, 0)
    return ajustar_passo_dano("1d6", delta)


def dano_desarmado_ameaca(tamanho: str = "Médio", bonus_dano_principal: int = 0) -> str:
    """Dano desarmado rápido quando uma ameaça perde sua arma (p. 374): 1d3 base + bônus principal."""
    delta = _DELTA_PASSO_TAMANHO.get(tamanho, 0)
    dado = ajustar_passo_dano("1d3", delta)
    if bonus_dano_principal > 0:
        return f"{dado}+{bonus_dano_principal}"
    if bonus_dano_principal < 0:
        return f"{dado}{bonus_dano_principal}"
    return dado


def calcular_ataque_ameaca_sem_pericia(nd: float, mod_atributo: int) -> int:
    """Modificador de ataque de ameaça não treinada na perícia (p. 374): metade do ND (chão) + atributo."""
    metade_nd = math.floor(max(0.0, float(nd)) / 2)
    return metade_nd + int(mod_atributo)


def determinar_atributo_chave_cd_ameaca(
    categoria: str,
    atributos: Dict[str, int],
) -> Tuple[str, int]:
    """Determina (atributo_chave, valor) para CD de habilidade de ameaça (p. 375).

    Categorias aceitas:
      - 'atletica': maior entre Força e Destreza
      - 'fisiologica': Constituição
      - 'controle': Carisma
      - 'magia_arcana': maior entre Inteligência e Carisma
      - 'fisica': maior entre Força, Destreza e Constituição
      - 'magica' / 'mental': maior entre Inteligência, Sabedoria e Carisma
      - qualquer outra: maior de todos os atributos
    """
    attrs = {
        "forca": int(atributos.get("forca", atributos.get("for", 0)) or 0),
        "destreza": int(atributos.get("destreza", atributos.get("des", 0)) or 0),
        "constituicao": int(atributos.get("constituicao", atributos.get("con", 0)) or 0),
        "inteligencia": int(atributos.get("inteligencia", atributos.get("int", 0)) or 0),
        "sabedoria": int(atributos.get("sabedoria", atributos.get("sab", 0)) or 0),
        "carisma": int(atributos.get("carisma", atributos.get("car", 0)) or 0),
    }
    cat = (categoria or "").strip().lower()
    if cat in ("atletica", "atlética", "atleticas", "atléticas"):
        candidatos = ["forca", "destreza"]
    elif cat in ("fisiologica", "fisiológica", "fisiologicas", "fisiológicas"):
        candidatos = ["constituicao"]
    elif cat in ("controle", "psiquica", "psíquica"):
        candidatos = ["carisma"]
    elif cat in ("magia_arcana", "arcana"):
        candidatos = ["inteligencia", "carisma"]
    elif cat in ("fisica", "física"):
        candidatos = ["forca", "destreza", "constituicao"]
    elif cat in ("magica", "mágica", "mental"):
        candidatos = ["inteligencia", "sabedoria", "carisma"]
    else:
        candidatos = list(attrs.keys())

    melhor = max(candidatos, key=lambda k: attrs[k])
    return melhor, attrs[melhor]


def avaliar_morte_ameaca(papel: str, pv_atual: int, dano_nao_letal: bool = False) -> str:
    """Regra variante Ameaças e Morte (p. 375).

    Retorna: 'ativo' | 'inconsciente' | 'morto' | '50%_vivo'
    """
    if pv_atual > 0:
        return "ativo"
    if dano_nao_letal:
        return "inconsciente"
    papel_norm = (papel or "").strip().lower()
    if papel_norm == "lacaio":
        return "morto"
    return "50%_vivo"


def aplicar_condicao_item(condicao_atual: Optional[str], nova_condicao: str) -> str:
    """Aplica condição de item (Ameaças de Arton, p. 375).

    - Avariado + Avariado -> Destruído
    - Destruído permanece Destruído
    """
    atual = (condicao_atual or "").strip()
    nova = (nova_condicao or "").strip()
    if atual == "Destruído" or nova == "Destruído":
        return "Destruído"
    if atual == "Avariado" and nova == "Avariado":
        return "Destruído"
    return nova or atual


def reparar_item() -> None:
    """Remove condições Avariado/Destruído após reparo ou Transmutar Objetos (p. 375)."""
    return None
