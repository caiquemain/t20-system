"""Regras do Capítulo 8 — Recompensas & Itens Mágicos (T20 Jogo do Ano, p.326–348).

- Cálculo de XP por desafio (ND × 1.000 / nº personagens, desafios irrelevantes e XP parcial)
- Fabricação de itens mágicos de uso único (poções e pergaminhos) e permanentes (melhorias + encantos)
- Estatísticas de destruição e testes de resistência de itens mágicos
"""
from typing import Optional

from ..dados_equipamentos import PRECO_MELHORIAS
from ..dados_recompensas import PRECO_ENCANTOS, CATEGORIAS_ITEM_MAGICO


def calcular_xp_desafio(
    nd: float,
    num_personagens: int,
    nivel_grupo: Optional[int] = None,
    resultado: str = "vitoria",
) -> int:
    """Calcula a XP recebida por cada personagem ao enfrentar um desafio (T20 JdA p.326–327).

    Fórmula: ND × 1.000 / nº personagens.
    - Desafio irrelevante: ND <= nível_grupo - 5 rende 0 XP.
    - XP Parcial: vitória = 100%, empate = 50%, derrota = 25%.
    """
    if num_personagens <= 0:
        raise ValueError("num_personagens deve ser >= 1")
    if nd <= 0:
        return 0
    if nivel_grupo is not None and nd <= (nivel_grupo - 5):
        return 0

    fatores = {
        "vitoria": 1.0,
        "vitória": 1.0,
        "empate": 0.5,
        "derrota": 0.25,
    }
    res_norm = (resultado or "vitoria").strip().lower()
    if res_norm not in fatores:
        raise ValueError(f"Resultado inválido para XP: {resultado!r}")

    xp_total = nd * 1000.0 * fatores[res_norm]
    return int(xp_total // num_personagens)


def calcular_fabricacao_consumivel(custo_pm: int) -> dict:
    """Preço, custo de fabricação e CD para poção ou pergaminho (T20 JdA p.333).

    Preço = T$ 30 × (custo em PM)² (mínimo 1 PM).
    CD de Ofício = 20 + custo em PM.
    """
    pm = max(1, int(custo_pm or 1))
    preco = 30 * (pm ** 2)
    return {
        "custo_pm": pm,
        "preco": preco,
        "custo_fabricacao": round(preco / 3, 2),
        "cd": 20 + pm,
    }


def calcular_fabricacao_item_permanente(
    preco_base: float,
    num_melhorias: int = 0,
    num_encantos: int = 0,
    cd_base: int = 20,
) -> dict:
    """Calcula preço, custo de fabricação (1/3), CD de Ofício e sacrifício de PM
    para itens superiores e/ou encantados (T20 JdA p.164 e p.334).

    Exemplo do livro (p.334):
    - Espada longa (T$ 15) + 1 encanto: preço T$ 18.015, custo T$ 6.005, CD 30, 1 PM.
    - Espada longa (T$ 15) + 4 melhorias + 3 encantos: preço T$ 90.015, custo T$ 30.005, CD 60, 3 PM.
    """
    m = max(0, min(4, int(num_melhorias or 0)))
    e = max(0, min(3, int(num_encantos or 0)))

    inc_mel = PRECO_MELHORIAS.get(m, {"aumento_preco": 0, "aumento_cd": 0})
    inc_enc = PRECO_ENCANTOS.get(e, {"aumento_preco": 0, "aumento_cd": 0, "sacrificio_pm": 0})

    preco_total = preco_base + inc_mel["aumento_preco"] + inc_enc["aumento_preco"]
    cd_total = cd_base + inc_mel["aumento_cd"] + inc_enc["aumento_cd"]
    return {
        "preco": preco_total,
        "custo_fabricacao": round(preco_total / 3, 2),
        "cd": cd_total,
        "sacrificio_pm": inc_enc.get("sacrificio_pm", 0),
    }


def calcular_estatisticas_item_magico(categoria: str, pv_base: int = 0, rd_base: int = 0) -> dict:
    """Retorna PV, RD e bônus de resistência de um item mágico permanente (T20 JdA p.334–335)."""
    cat_norm = (categoria or "").strip().capitalize()
    if cat_norm == "Medio":
        cat_norm = "Médio"
    if cat_norm not in CATEGORIAS_ITEM_MAGICO:
        raise ValueError(f"Categoria de item mágico inválida: {categoria!r}")
    info = CATEGORIAS_ITEM_MAGICO[cat_norm]
    return {
        "categoria": cat_norm,
        "pv": pv_base + info["pv_rd_bonus"],
        "rd": rd_base + info["pv_rd_bonus"],
        "resistencia": info["resistencia_item"],
        "cd_oficio": info["cd_oficio"],
        "sacrificio_pm": info["sacrificio_pm"],
    }
