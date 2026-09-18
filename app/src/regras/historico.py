"""Histórico da ficha: diff legível entre duas versões da ficha.

O resumo de um level-up NÃO vem de uma tabela paralela de ganhos:
vem do diff antes/depois do atualizar_ficha(). Se um número mudou,
é porque o motor de regras mudou — a memória nunca mente.
"""
import logging

from ..models import Personagem

logger = logging.getLogger(__name__)


def resumir_mudancas(antes: Personagem, depois: Personagem) -> list:
    """Lista de strings legíveis descrevendo o que mudou entre versões."""
    resumo = []

    # Nível
    nv_a, nv_d = antes.cabecalho.nivel_total, depois.cabecalho.nivel_total
    if nv_d != nv_a:
        resumo.append(f"Nível {nv_a} → {nv_d}")

    # PV / PM máximos
    pv_a, pv_d = antes.status.pv.maximo, depois.status.pv.maximo
    if pv_d != pv_a:
        resumo.append(f"PV máximo {pv_a} → {pv_d} ({pv_d - pv_a:+d})")
    pm_a, pm_d = antes.status.pm.maximo, depois.status.pm.maximo
    if pm_d != pm_a:
        resumo.append(f"PM máximo {pm_a} → {pm_d} ({pm_d - pm_a:+d})")

    # Defesa
    df_a, df_d = antes.status.defesa.total, depois.status.defesa.total
    if df_d != df_a:
        resumo.append(f"Defesa {df_a} → {df_d} ({df_d - df_a:+d})")

    # Círculo máximo de magias
    c_a = antes.combate.circulo_maximo or 0
    c_d = depois.combate.circulo_maximo or 0
    if c_d != c_a:
        resumo.append(f"Círculo máximo de magias {c_a}º → {c_d}º")

    # Limite de magias conhecidas
    l_a, l_d = antes.combate.limite_magias, depois.combate.limite_magias
    if l_a != l_d:
        resumo.append(f"Limite de magias conhecidas {l_a} → {l_d}")

    # Habilidades novas / perdidas
    nomes_antes = {h.nome for h in antes.habilidades}
    nomes_depois = {h.nome for h in depois.habilidades}
    for h in depois.habilidades:
        if h.nome not in nomes_antes:
            resumo.append(f"Nova habilidade: {h.nome} ({h.tipo})")
    for h in antes.habilidades:
        if h.nome not in nomes_depois:
            resumo.append(f"Habilidade perdida: {h.nome}")

    # Magias novas
    mag_antes = {m.nome for m in antes.combate.magias}
    for m in depois.combate.magias:
        if m.nome not in mag_antes:
            resumo.append(f"Nova magia: {m.nome} ({m.circulo}º)")

    return resumo
