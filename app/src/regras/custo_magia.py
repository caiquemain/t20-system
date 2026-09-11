"""Lote R5 — Motor de custo de magia (T20 JdA, Capítulo 4).

Regras oficiais implementadas:
- Base = Tabela 4-1 por círculo (1/3/6/10/15 PM)
- Aprimoramentos somam PM (cumulativos "aumenta" até o limite de PM = nível)
- Truque: custo 0 e não combina com outros aprimoramentos
- Reduções multiplicativas (Alta Arcana ×0.5, arredonda p/ baixo)
- Reduções fixas por magia (reducao_custo_magia racial)
- Custo mínimo 1 PM (0 apenas para Truque)
- CD = 10 + metade do nível + atributo-chave (exposta p/ tooltip)
"""
import math
import logging
from typing import Optional

from ..models import Personagem, StatCalculado, FonteBonus

logger = logging.getLogger("RegrasT20")

CUSTO_POR_CIRCULO = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}


def _circulo_int(magia) -> int:
    try:
        return int(magia.circulo)
    except Exception:
        return 1


def calcular_cd_magia(ficha: Personagem, magia) -> int:
    """CD = 10 + metade do nível + modificador do atributo-chave."""
    from .utils import calcular_modificador
    attr = (magia.atributo_chave or "").lower()
    mapa = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
    val = getattr(ficha.atributos, mapa.get(attr, ''), 0) or 0
    return 10 + math.floor((ficha.cabecalho.nivel_total or 1) / 2) + calcular_modificador(val)


def calcular_custo_magia(ficha: Personagem, magia,
                         aprimoramentos_pm: int = 0,
                         eh_truque: bool = False) -> StatCalculado:
    circulo = _circulo_int(magia)
    base = CUSTO_POR_CIRCULO.get(circulo, 1)
    calc = StatCalculado(base=base, total=base)
    calc.fontes.append(FonteBonus(
        fonte=f"Custo do {circulo}º círculo (Tabela 4-1)", categoria="Base", valor=base))

    # Truque: custo zero, sem outros aprimoramentos
    if eh_truque:
        calc.adicionar_bonus("Truque (versão simples)", "Truque", -base)
        calc.total = 0
        return calc

    total = base
    if aprimoramentos_pm:
        total += aprimoramentos_pm
        calc.adicionar_bonus("Aprimoramentos", "Aprimoramento", aprimoramentos_pm)

    # Reduções multiplicativas (Alta Arcana ×0.5) — arredonda p/ baixo
    for hab in ficha.habilidades:
        efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
        mult = efeitos.get("reducao_custo_magia_global")
        if isinstance(mult, (int, float)) and 0 < mult < 1:
            antes = total
            total = math.floor(total * mult)
            calc.adicionar_bonus(f"{hab.nome} (×{mult})", "Multiplicativo", total - antes)

    # Reduções fixas por magia (racial: reducao_custo_magia {"nomes": [...], "valor": N})
    for hab in ficha.habilidades:
        rc = (hab.efeitos or {}).get("reducao_custo_magia")
        if isinstance(rc, dict) and magia.nome in (rc.get("nomes") or []):
            valor = int(rc.get("valor", 1))
            total -= valor
            calc.adicionar_bonus(f"{hab.nome} (−{valor} PM)", "Redução", -valor)

    # Mínimo 1 PM (regra confirmada); limite de gasto por magia = nível
    total = max(1, total)
    limite_pm = max(1, ficha.cabecalho.nivel_total or 1)
    if total > limite_pm:
        total = limite_pm
        calc.adicionar_bonus(f"Limite de PM por magia (nível {limite_pm})", "Limite", total - max(1, total))
    calc.total = total
    return calc
