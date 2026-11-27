# -*- coding: utf-8 -*-
"""Motor de regras de Distinções — Heróis de Arton (Cap. 2, p. 104–211)."""
from typing import Any, Dict, Optional

from ..dados_distincoes_herois import DADOS_DISTINCOES_HEROIS
from .inventario import catalogo_do_item
from ..models import Habilidade, Personagem


def _usa_armadura_pesada(ficha: Personagem) -> bool:
    for item in ficha.inventario.equipamentos:
        if not item.equipado:
            continue
        if (catalogo_do_item(item.nome) or {}).get("tipo_armadura") == "Pesada":
            return True
    return False


def sincronizar_distincoes(
    ficha: Personagem,
    memoria_escolhas: Optional[Dict[str, Any]] = None,
) -> None:
    """Sincroniza Marcas da Distinção e Poderes de Distinção na lista de habilidades.

    - Remove habilidades anteriores cuja fonte comece com "Distinção: " (evitando
      resíduos ao remover uma distinção ou um poder).
    - Para cada distinção em `ficha.distincoes` com `admitido=True`:
      - Preenche `dist.marca` e `dist.fonte` a partir do catálogo oficial.
      - Injeta a Marca da Distinção (aplicando efeitos dinâmicos como +1 PM por
        poder da distinção em *Cavaleiro Feérico* e +2 Defesa sem armadura pesada
        em *Amazona*).
      - Injeta cada poder escolhido em `dist.poderes`.
    """
    memoria = memoria_escolhas or {}

    ficha.habilidades = [
        h for h in ficha.habilidades
        if not (h.fonte or "").startswith("Distinção: ")
    ]

    if not ficha.distincoes:
        return

    usa_pesada = _usa_armadura_pesada(ficha)

    for dist in ficha.distincoes:
        if not dist.admitido:
            continue
        dados = DADOS_DISTINCOES_HEROIS.get(dist.nome)
        if not dados:
            continue

        marca_dados = dados["marca"]
        dist.marca = marca_dados["nome"]
        if not dist.fonte:
            dist.fonte = dados["fonte"]

        fonte_hab = f"Distinção: {dist.nome}"
        poderes_por_nome = {p["nome"]: p for p in dados["poderes"]}
        poderes_validos = [p for p in dist.poderes if p in poderes_por_nome]

        efeitos_marca = dict(marca_dados.get("efeitos") or {})
        if "pm_por_poder_distincao" in efeitos_marca:
            qtd = len(poderes_validos)
            if qtd > 0:
                efeitos_marca["pm_max_ini"] = (
                    efeitos_marca.get("pm_max_ini", 0)
                    + qtd * int(efeitos_marca["pm_por_poder_distincao"])
                )
        if "defesa_bonus_sem_armadura_pesada" in efeitos_marca and not usa_pesada:
            efeitos_marca["defesa_bonus"] = (
                efeitos_marca.get("defesa_bonus", 0)
                + int(efeitos_marca["defesa_bonus_sem_armadura_pesada"])
            )

        ficha.habilidades.append(
            Habilidade(
                nome=marca_dados["nome"],
                tipo="Marca da Distinção",
                descricao=marca_dados.get("descricao", ""),
                efeitos=efeitos_marca,
                fonte=fonte_hab,
                escolhas_aplicadas=memoria.get(marca_dados["nome"], {}) or {},
            )
        )

        vistos = set()
        for p_nome in poderes_validos:
            if p_nome in vistos:
                continue
            vistos.add(p_nome)
            pd = poderes_por_nome[p_nome]
            ficha.habilidades.append(
                Habilidade(
                    nome=pd["nome"],
                    tipo="Poder de Distinção",
                    descricao=pd.get("descricao", ""),
                    efeitos=dict(pd.get("efeitos") or {}),
                    fonte=fonte_hab,
                    escolhas_aplicadas=memoria.get(pd["nome"], {}) or {},
                )
            )
