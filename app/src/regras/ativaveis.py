# -*- coding: utf-8 -*-
"""Motor executável de Habilidades Ativáveis (T20 JdA + Suplementos).

Normaliza qualquer habilidade ativável (Classe, Geral, Raça, Grupo, Tormenta,
Distinção ou Concedido) em uma especificação estruturada e executável pelo
backend — utilizável tanto pela ficha web quanto por clientes externos ou
futuros ports/mods de jogos de RPG.
"""
import re
from typing import Any, Dict, List, Optional

from ..models import Buff, Habilidade, Personagem


def _inferir_acao(efeitos: Dict[str, Any], desc: str) -> str:
    if isinstance(efeitos.get("postura_combate"), dict):
        return efeitos["postura_combate"].get("acao", "movimento")
    if isinstance(efeitos.get("missa"), dict):
        return efeitos["missa"].get("tempo", "1 hora")
    if isinstance(efeitos.get("habilidade_ativavel"), dict):
        ac = efeitos["habilidade_ativavel"].get("acao")
        if ac:
            return str(ac).lower()
    low = desc.lower()
    if "reação" in low or "reacao" in low:
        return "reação"
    if "ação completa" in low or "acao completa" in low:
        return "completa"
    if "ação padrão" in low or "acao padrao" in low or "padrão" in low:
        return "padrão"
    if "ação de movimento" in low or "acao de movimento" in low or re.search(r"\bmovimento\b", low):
        return "movimento"
    if "ação livre" in low or "acao livre" in low or re.search(r"\blivre\b", low):
        return "livre"
    return "livre"


def _inferir_frequencia(desc: str) -> str:
    low = desc.lower()
    if re.search(r"1[×x/]rodada|uma vez por rodada", low):
        return "1/rodada"
    if re.search(r"1[×x/]cena|uma vez por cena", low):
        return "1/cena"
    if re.search(r"1[×x/]combate|uma vez por combate", low):
        return "1/combate"
    if re.search(r"1[×x/]dia|uma vez por dia", low):
        return "1/dia"
    return "ilimitada"


def _inferir_duracao(efeitos: Dict[str, Any], desc: str) -> str:
    if isinstance(efeitos.get("postura_combate"), dict):
        return efeitos["postura_combate"].get("duracao", "cena")
    if isinstance(efeitos.get("missa"), dict):
        return efeitos["missa"].get("duracao", "1 dia")
    low = desc.lower()
    if "sustentada" in low:
        return "sustentada"
    if "até o fim da cena" in low or "pela cena" in low:
        return "cena"
    if "até o fim do dia" in low or "por 1 dia" in low or "dura 1 dia" in low:
        return "1 dia"
    if "até o próximo turno" in low or "até seu próximo turno" in low or "por 1 rodada" in low:
        return "1 rodada"
    if "até o fim do turno" in low or "neste turno" in low:
        return "1 turno"
    return "instantânea"


def _inferir_custo_pm(efeitos: Dict[str, Any], desc: str) -> int:
    if "custo_pm" in efeitos and isinstance(efeitos["custo_pm"], (int, float)):
        return int(efeitos["custo_pm"])
    if isinstance(efeitos.get("postura_combate"), dict):
        return int(efeitos["postura_combate"].get("custo_pm", 2))
    if isinstance(efeitos.get("habilidade_ativavel"), dict):
        c = efeitos["habilidade_ativavel"].get("custo_pm")
        if isinstance(c, (int, float)):
            return int(c)
    m = re.search(r"(?:gastar|gaste|custo:\s*\+?)\s*(?:[^.]{0,45}?)?\b(\d+)\s*PM\b", desc, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m2 = re.search(r"\b(\d+)\s*PM\s*:", desc, re.IGNORECASE)
    if m2:
        return int(m2.group(1))
    return 0


def _inferir_efeitos_ativos(efeitos: Dict[str, Any], desc: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    low = desc.lower()
    m_def = re.search(r"\+(\d+)\s+(?:na|em)\s+defesa", low)
    if m_def:
        out["defesa_bonus"] = int(m_def.group(1))
    m_atk = re.search(r"\+(\d+)\s+(?:em|nos)\s+(?:testes de )?ataques?", low)
    if m_atk:
        out["ataque_bonus"] = int(m_atk.group(1))
    m_dano = re.search(r"\+(\d+d\d+|\d+)\s+(?:pontos de )?dano", low)
    if m_dano:
        out["dano_extra"] = m_dano.group(1)
    m_rd = re.search(r"\brd\s+(\d+)", low)
    if m_rd:
        out["rd"] = int(m_rd.group(1))
    if efeitos.get("postura_combate"):
        out["postura_combate"] = True
    if efeitos.get("missa"):
        out["missa"] = True
    return out


def extrair_especificacao_ativavel(hab: Habilidade) -> Dict[str, Any]:
    """Extrai a especificação estruturada de execução de uma habilidade."""
    ef = dict(hab.efeitos or {})
    desc = hab.descricao or ""
    custo_pm = _inferir_custo_pm(ef, desc)
    freq = _inferir_frequencia(desc)
    duracao = _inferir_duracao(ef, desc)
    low = desc.lower()

    tem_gatilho_ativo = (
        custo_pm > 0
        or bool(ef.get("habilidade_ativavel"))
        or bool(ef.get("postura_combate"))
        or bool(ef.get("missa"))
        or freq != "ilimitada"
        or any(
            kw in low
            for kw in (
                "pode gastar",
                "gaste ",
                "ação padrão",
                "ação de movimento",
                "ação completa",
                "ação livre",
                "reação",
            )
        )
    )

    acao = _inferir_acao(ef, desc) if tem_gatilho_ativo else "passiva"
    return {
        "nome": hab.nome,
        "tipo": hab.tipo,
        "fonte": hab.fonte or "",
        "ativavel": tem_gatilho_ativo,
        "custo_pm": custo_pm,
        "acao": acao,
        "frequencia": freq,
        "duracao": duracao,
        "efeitos_ativos": _inferir_efeitos_ativos(ef, desc) if tem_gatilho_ativo else {},
        "descricao": desc,
    }


def listar_habilidades_ativaveis(ficha: Personagem) -> List[Dict[str, Any]]:
    """Lista todas as habilidades ativáveis do personagem com status de disponibilidade."""
    nivel = max(1, ficha.cabecalho.nivel_total or 1)
    pm_atual = ficha.status.pm.atual
    resultado: List[Dict[str, Any]] = []

    for hab in ficha.habilidades:
        spec = extrair_especificacao_ativavel(hab)
        if not spec["ativavel"]:
            continue
        custo = spec["custo_pm"]
        motivo: Optional[str] = None
        if custo > nivel:
            motivo = f"Custo ({custo} PM) excede o limite por nível ({nivel} PM)"
        elif pm_atual < custo:
            motivo = f"PM insuficiente ({pm_atual}/{custo} PM)"
        spec["pode_ativar"] = motivo is None
        spec["motivo_bloqueio"] = motivo
        resultado.append(spec)
    return resultado


def ativar_habilidade(
    ficha: Personagem,
    nome_habilidade: str,
    pm_extra: int = 0,
) -> Dict[str, Any]:
    """Executa uma habilidade ativável no motor de regras.

    Valida posse, limite de PM (nível) e PM disponível, desconta PM e registra
    um Buff ativo quando a habilidade possui duração (cena, rodada, turno, dia).
    """
    alvo_low = nome_habilidade.strip().lower()
    hab = next((h for h in ficha.habilidades if (h.nome or "").strip().lower() == alvo_low), None)
    if hab is None:
        return {"sucesso": False, "erro": f"Habilidade '{nome_habilidade}' não encontrada na ficha."}

    spec = extrair_especificacao_ativavel(hab)
    if not spec["ativavel"]:
        return {"sucesso": False, "erro": f"Habilidade '{hab.nome}' é passiva e não requer ativação."}

    custo_total = spec["custo_pm"] + max(0, int(pm_extra or 0))
    nivel = max(1, ficha.cabecalho.nivel_total or 1)
    if custo_total > nivel:
        return {
            "sucesso": False,
            "erro": f"Custo total ({custo_total} PM) excede o limite por uso ({nivel} PM).",
        }
    if ficha.status.pm.atual < custo_total:
        return {
            "sucesso": False,
            "erro": f"PM insuficiente: necessário {custo_total} PM, disponível {ficha.status.pm.atual} PM.",
        }

    ficha.status.pm.atual -= custo_total

    buff_aplicado: Optional[Dict[str, Any]] = None
    if spec["duracao"] != "instantânea":
        # Remove buff anterior da mesma habilidade para não duplicar
        ficha.status.buffs = [b for b in ficha.status.buffs if b.origem != hab.nome]
        ef_at = spec["efeitos_ativos"]
        attr_buff = "defesa" if "defesa_bonus" in ef_at else (
            "ataque" if "ataque_bonus" in ef_at else (
                "rd" if "rd" in ef_at else "efeito"
            )
        )
        val_buff = int(
            ef_at.get("defesa_bonus")
            or ef_at.get("ataque_bonus")
            or ef_at.get("rd")
            or 0
        )
        novo_buff = Buff(
            origem=hab.nome,
            atributo=attr_buff,
            valor=val_buff,
            duracao=spec["duracao"],
        )
        ficha.status.buffs.append(novo_buff)
        buff_aplicado = novo_buff.model_dump(mode="json")

    return {
        "sucesso": True,
        "habilidade": hab.nome,
        "custo_pm": custo_total,
        "pm_restante": ficha.status.pm.atual,
        "acao": spec["acao"],
        "frequencia": spec["frequencia"],
        "duracao": spec["duracao"],
        "efeitos_ativos": spec["efeitos_ativos"],
        "buff_aplicado": buff_aplicado,
        "descricao": spec["descricao"],
    }
