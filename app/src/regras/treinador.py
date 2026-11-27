# -*- coding: utf-8 -*-
"""Motor de regras da classe Treinador e ficha automática do Melhor Amigo (Heróis de Arton, p. 16–21)."""
from typing import Any, Dict, List, Optional
from ..models import Personagem
from ..dados_treinador_herois import (
    DADOS_MASCOTES_TREINADOR,
    DADOS_TIPOS_MELHOR_AMIGO,
    DADOS_TRUQUES_MELHOR_AMIGO,
)
from .utils import calcular_modificador

_PASSOS_DANO = ["1d4", "1d6", "1d8", "1d10", "1d12", "3d6", "4d6", "4d8", "4d10", "4d12"]


def _subir_passo_dano(dado: str, passos: int) -> str:
    if dado not in _PASSOS_DANO or passos <= 0:
        return dado
    idx = min(len(_PASSOS_DANO) - 1, _PASSOS_DANO.index(dado) + passos)
    return _PASSOS_DANO[idx]


def _nivel_treinador(ficha: Personagem) -> int:
    return sum(
        int(c.nivel or 0)
        for c in (ficha.classes or [])
        if (c.nome or "").strip().lower() == "treinador"
    )


def _tem_hab(ficha: Personagem, nome: str) -> bool:
    alvo = nome.strip().lower()
    return any((h.nome or "").strip().lower() == alvo for h in (ficha.habilidades or []))


def _contar_hab(ficha: Personagem, nome: str) -> int:
    alvo = nome.strip().lower()
    return sum(1 for h in (ficha.habilidades or []) if (h.nome or "").strip().lower() == alvo)


def _obter_treino_especializado(ficha: Personagem) -> Optional[str]:
    for h in (ficha.habilidades or []):
        if (h.nome or "").strip() == "Treino Especializado":
            esc = (h.escolhas_aplicadas or {}).get("treino_especializado") or ""
            if esc:
                return str(esc).strip()
    if _tem_hab(ficha, "Conquistar pelos Números"):
        return "Conquistar pelos Números"
    if _tem_hab(ficha, "Treino Intensivo"):
        return "Treino Intensivo"
    return None


def _obter_mascotes_ativos(ficha: Personagem) -> List[str]:
    mascotes: List[str] = []
    for h in (ficha.habilidades or []):
        if (h.nome or "").strip() == "Mascote":
            m = (h.escolhas_aplicadas or {}).get("mascote")
            if isinstance(m, str) and m.strip() and m.strip() not in mascotes:
                mascotes.append(m.strip())
        elif (h.nome or "").strip() in DADOS_MASCOTES_TREINADOR:
            nome_m = (h.nome or "").strip()
            if nome_m not in mascotes:
                mascotes.append(nome_m)
    return mascotes


def calcular_melhor_amigo(
    ficha: Personagem,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Calcula a ficha derivada completa de um Melhor Amigo (Heróis de Arton, p. 20–21)."""
    cfg = dict(config or {})
    nv_tr = _nivel_treinador(ficha)
    nv_total = max(1, int(ficha.cabecalho.nivel_total or nv_tr or 1))
    usa_ecletico = _tem_hab(ficha, "Treinador Eclético")
    nv_ef = nv_total if usa_ecletico else max(1, nv_tr)

    patamares_acima_ini = (1 if nv_ef >= 5 else 0) + (1 if nv_ef >= 11 else 0) + (1 if nv_ef >= 17 else 0)
    mod_car_tr = calcular_modificador(ficha.atributos.carisma)
    treino_esp = _obter_treino_especializado(ficha)
    eh_intensivo = treino_esp == "Treino Intensivo" and nv_tr >= 5
    mascotes = _obter_mascotes_ativos(ficha)

    nome = cfg.get("nome") or "Melhor Amigo"
    tipo_nome = cfg.get("tipo") or "Animal"
    dados_tipo = DADOS_TIPOS_MELHOR_AMIGO.get(tipo_nome, DADOS_TIPOS_MELHOR_AMIGO["Animal"])
    tamanho = cfg.get("tamanho") or "Médio"
    truques: List[str] = list(cfg.get("truques") or [])
    truques_set = set(truques)

    # 1. Atributos base (For 1, Des 1, Con 1, Int -4, Sab 1, Car 0) + Tipo + Truques
    atributos = {
        "forca": 1,
        "destreza": 1,
        "constituicao": 1,
        "inteligencia": -2 if "Anatomia Humanoide" in truques_set else -4,
        "sabedoria": 1,
        "carisma": 0,
    }
    for k, v in (dados_tipo.get("mod_atributos") or {}).items():
        atributos[k] = atributos.get(k, 0) + int(v)

    if "Amigão" in truques_set:
        atributos["forca"] += 1
        tamanho = "Enorme"

    # Condicionamento Especial (+2 em um atributo, +1 em outro, exceto Int)
    for cond in (cfg.get("condicionamentos") or []):
        a2 = str(cond.get("atributo_2") or "").lower()
        a1 = str(cond.get("atributo_1") or "").lower()
        if a2 in atributos and a2 != "inteligencia":
            atributos[a2] += 2
        if a1 in atributos and a1 != "inteligencia" and a1 != a2:
            atributos[a1] += 1

    # 2. Pontos de Vida: 16 + Con + (nv_ef - 1) * (4 + Con) [+ 4 * nv_ef se Treino Intensivo]
    con_amigo = atributos["constituicao"]
    pv_max = 16 + con_amigo + max(0, nv_ef - 1) * (4 + con_amigo)
    if eh_intensivo:
        pv_max += 4 * nv_ef

    # 3. Defesa: 10 + Des + Car_treinador + (nv_ef se Treinamento Defensivo else nv_ef // 2)
    bonus_nv_def = nv_ef if "Treinamento Defensivo" in truques_set else (nv_ef // 2)
    defesa = 10 + atributos["destreza"] + mod_car_tr + bonus_nv_def
    if "Veloz" in truques_set:
        defesa += 2
    if "Gekko Malhado" in mascotes:
        defesa += 2

    # 4. Deslocamento: 12m (+3m Veloz)
    deslocamento = int(cfg.get("deslocamento_montaria") or 12)
    if "Veloz" in truques_set:
        deslocamento += 3
    deslocamento_voo = 15 if "Alado" in truques_set else (12 if "Asas" in truques_set else 0)

    # 5. Redução de Dano
    rd: List[str] = []
    rd_geral = 0
    if eh_intensivo:
        rd_geral += 15 if nv_tr >= 17 else (10 if nv_tr >= 11 else 5)
    if "Redução de Dano" in truques_set:
        rd_geral += 5
    if rd_geral > 0:
        rd.append(f"geral {rd_geral}")
    if "Ossinhos" in mascotes:
        rd.extend(["Corte 2", "Frio 2", "Perfuração 2"])

    # 6. Grau de Parceiro
    grau_parceiro = "Mestre" if "Amigo Mestre" in truques_set else (
        "Veterano" if "Amigo Veterano" in truques_set else "Iniciante"
    )

    # 7. Arma Natural & Ataques
    passos_extra = (1 if "Amigão" in truques_set else 0) + (1 if "Amigo Feroz" in truques_set else 0)
    dano_natural = _subir_passo_dano("1d8", passos_extra)
    margem_ameaca = 20 - int(dados_tipo.get("margem_ameaca_bonus", 0)) - (2 if "Amigo Feroz" in truques_set else 0)
    bonus_ataque = (2 if "Amigo Feroz" in truques_set else 0) + (1 if "Minivaca" in mascotes else 0)
    bonus_dano = 0
    if "Treinamento Marcial" in truques_set:
        tm_bonus = 2 + patamares_acima_ini
        bonus_ataque += tm_bonus
        bonus_dano += tm_bonus

    qtd_armas_naturais = (0 if "Anatomia Humanoide" in truques_set else 1)
    qtd_armas_naturais += int(dados_tipo.get("armas_naturais_extras", 0))
    if "Arma Natural Adicional" in truques_set:
        qtd_armas_naturais += 1

    # 8. Perícias treinadas
    pericias_treinadas = list(cfg.get("pericias_treinadas") or [])
    for p in dados_tipo.get("pericias_treinadas", []):
        if p not in pericias_treinadas:
            pericias_treinadas.append(p)
    if "Veloz" in truques_set and "Atletismo" not in pericias_treinadas:
        pericias_treinadas.append("Atletismo")

    return {
        "nome": nome,
        "tipo": tipo_nome,
        "tamanho": tamanho,
        "nivel_efetivo": nv_ef,
        "grau_parceiro": grau_parceiro,
        "atributos": atributos,
        "pv_maximo": pv_max,
        "defesa": defesa,
        "deslocamento": deslocamento,
        "deslocamento_voo": deslocamento_voo,
        "rd": rd,
        "sentidos": list(dados_tipo.get("sentidos", [])),
        "imunidades": list(dados_tipo.get("imunidades", [])),
        "pericias_treinadas": pericias_treinadas,
        "truques": truques,
        "ataque_natural": {
            "quantidade": qtd_armas_naturais,
            "dano": dano_natural,
            "tipo_dano": cfg.get("tipo_dano") or "Corte",
            "margem_ameaca": margem_ameaca,
            "critico": "x2",
            "bonus_ataque": bonus_ataque,
            "bonus_dano": bonus_dano,
        },
    }


def calcular_treinador(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula estatísticas derivadas da classe Treinador (Tabela 1-1, p. 16–21)."""
    nv_tr = _nivel_treinador(ficha)
    if nv_tr <= 0:
        return None

    nv_total = max(nv_tr, int(ficha.cabecalho.nivel_total or nv_tr))
    mod_car = calcular_modificador(ficha.atributos.carisma)
    treino_esp = _obter_treino_especializado(ficha) if nv_tr >= 5 else None
    mascotes = _obter_mascotes_ativos(ficha)

    # Truques: 2 no nv 1 + 1 a cada 3 níveis (4, 7, 10, 13, 16, 19)
    truques_base = 2 + ((nv_tr - 1) // 3)
    truques_intensivo = 0
    if treino_esp == "Treino Intensivo":
        truques_intensivo = 2 if nv_tr >= 11 else 1
    truques_poder = _contar_hab(ficha, "Ensinar Truque")

    # Domar Criatura (nv 2+): 2d8 (+2d8 nos nv 6, 10, 14, 18 -> 10d8)
    domar = None
    if nv_tr >= 2:
        qtd_dados = 2 + 2 * ((nv_tr - 2) // 4)
        dado = "d10" if _tem_hab(ficha, "Domador Cativante") else "d8"
        bonus_car_domar = mod_car if _tem_hab(ficha, "Domador Cativante") else 0
        domar = {
            "formula": f"{qtd_dados}{dado}" + (f"+{bonus_car_domar}" if bonus_car_domar > 0 else ""),
            "qtd_dados": qtd_dados,
            "dado": dado,
            "bonus_carisma": bonus_car_domar,
            "domador_lendario": _tem_hab(ficha, "Domador Lendário"),
            "formula_lendaria": f"{qtd_dados}d12" + (f"+{bonus_car_domar}" if bonus_car_domar > 0 else "") if _tem_hab(ficha, "Domador Lendário") else None,
            "controla_cena": nv_tr >= 5,
            "nd_max_cena": nv_tr if nv_tr >= 5 else 0,
            "controla_dia": nv_tr >= 8,
            "nd_max_dia": max(0, nv_tr - 3) if nv_tr >= 8 else 0,
        }

    # Coração Grande: +1 limite de parceiros (+2 no 11º)
    limite_parceiros_bonus = 0
    if _tem_hab(ficha, "Coração Grande"):
        limite_parceiros_bonus = 2 if nv_tr >= 11 else 1

    # Calcula fichas dos melhores amigos configurados (ou 1 padrão se lista vazia)
    configs_amigos = getattr(ficha, "melhores_amigos", None) or [{}]
    amigos_calculados = [calcular_melhor_amigo(ficha, cfg) for cfg in configs_amigos]

    return {
        "nivel_treinador": nv_tr,
        "nivel_efetivo_amigo": nv_total if _tem_hab(ficha, "Treinador Eclético") else nv_tr,
        "alcance_habilidades": "Médio" if _tem_hab(ficha, "Comandos Distantes") else "Curto",
        "max_melhores_amigos": 2 if treino_esp == "Conquistar pelos Números" else 1,
        "treino_especializado": treino_esp,
        "truques_disponiveis": truques_base + truques_intensivo + truques_poder,
        "direcionar_bonus": mod_car,
        "direcionamento_marcial": _tem_hab(ficha, "Direcionamento Marcial"),
        "domar_criatura": domar,
        "sincronia_combate": nv_tr >= 6,
        "sincronia_perfeita": nv_tr >= 20,
        "limite_parceiros_bonus": limite_parceiros_bonus,
        "mascotes": mascotes,
        "melhores_amigos": amigos_calculados,
    }
