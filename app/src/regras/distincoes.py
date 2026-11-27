# -*- coding: utf-8 -*-
"""Motor de regras de Distinções — Heróis de Arton (Cap. 2, p. 104–211)."""
from typing import Any, Dict, Optional

from ..dados_distincoes_herois import DADOS_DISTINCOES_HEROIS
from .inventario import catalogo_do_item
from ..models import Habilidade, Personagem


# Efeitos passivos reais de Poderes de Distinção (100% conforme texto oficial)
EFEITOS_PODERES_DISTINCAO: Dict[str, Dict[str, Any]] = {
    "Lar Infernal": {"imunidade": ["Efeitos de áreas de Tormenta"]},
    "Rainha Amazona": {"atributo_bonus": {"car": 1}},
    "Destemor Inflamado": {"imunidade": ["Medo"]},
    "Caminhar do Dragão": {"bonus_pericia": {"Atletismo": 5}, "custo_pm": 1},
    "Sentidos do Tigre": {"defesa_soma_atributo": {"atributo": "sab", "exige_liberdade_movimento": True}},
    "Sentença de Bolso": {"bonus_pericia": {"Intimidação": 2}},
    "Atrás das Linhas Inimigas": {"imunidade": ["Atordoamento", "Cansaço"]},
    "Coração Duro": {"imunidade": ["Medo"], "dano_armas_bonus": 2},
    "Rápido ou Morto": {"bonus_pericia": {"Iniciativa": 2}, "deslocamento_bonus": 3},
    "Perfume Intoxicante": {"bonus_pericia": {"Adestramento": 2, "Diplomacia": 2}},
    "Cavaleiro Rústico": {"defesa_soma_atributo": {"atributo": "sab"}},
    "Conjurador Encouraçado": {
        "proficiencia_add": ["Armaduras Pesadas"],
        "ignora_penalidade_armadura_magia": True,
    },
    "Arsenal Arcano": {"proficiencia_add": ["Armas Marciais"]},
    "Saúde Perfeita": {
        "atributo_bonus": {"con": 1},
        "imunidade": ["Veneno"],
        "pm_por_poder_distincao": 2,
    },
    "Rápido no Gatilho": {"iniciativa_por_poder_distincao": 2},
    "Um Minotauro de Bem": {
        "bonus_pericia": {
            "Adestramento": 1,
            "Atuação": 1,
            "Diplomacia": 1,
            "Enganação": 1,
            "Intimidação": 1,
            "Jogatina": 1,
        }
    },
    "Aquele Papinho": {
        "bonus_pericia": {"Diplomacia": 1, "Enganação": 1, "Intuição": 1}
    },
}


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
      - Injeta cada poder escolhido em `dist.poderes`, mesclando seus efeitos
        passivos reais (incluindo escaláveis por quantidade de poderes da distinção,
        como *Saúde Perfeita* e *Rápido no Gatilho*).
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
        poderes_validos = list(dict.fromkeys(p for p in dist.poderes if p in poderes_por_nome))
        qtd_poderes = len(poderes_validos)

        efeitos_marca = dict(marca_dados.get("efeitos") or {})
        if "pm_por_poder_distincao" in efeitos_marca and qtd_poderes > 0:
            efeitos_marca["pm_max_ini"] = (
                efeitos_marca.get("pm_max_ini", 0)
                + qtd_poderes * int(efeitos_marca["pm_por_poder_distincao"])
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

        for p_nome in poderes_validos:
            pd = poderes_por_nome[p_nome]
            ef_pod = dict(pd.get("efeitos") or {})
            extra = EFEITOS_PODERES_DISTINCAO.get(p_nome)
            if extra:
                ef_pod.update(extra)
                if "pm_por_poder_distincao" in extra and qtd_poderes > 0:
                    ef_pod["pm_max_ini"] = (
                        ef_pod.get("pm_max_ini", 0)
                        + qtd_poderes * int(extra["pm_por_poder_distincao"])
                    )
                if "iniciativa_por_poder_distincao" in extra and qtd_poderes > 0:
                    bp = dict(ef_pod.get("bonus_pericia") or {})
                    bp["Iniciativa"] = bp.get("Iniciativa", 0) + qtd_poderes * int(
                        extra["iniciativa_por_poder_distincao"]
                    )
                    ef_pod["bonus_pericia"] = bp
            ficha.habilidades.append(
                Habilidade(
                    nome=pd["nome"],
                    tipo="Poder de Distinção",
                    descricao=pd.get("descricao", ""),
                    efeitos=ef_pod,
                    fonte=fonte_hab,
                    escolhas_aplicadas=memoria.get(pd["nome"], {}) or {},
                )
            )
