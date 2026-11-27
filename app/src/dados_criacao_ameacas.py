# -*- coding: utf-8 -*-
"""Manual de Criação de Ameaças — Ameaças de Arton (Cap. 2, p. 378–390).

Tabelas oficiais 2-3 A (Solos), 2-3 B (Lacaios) e 2-3 C (Especiais),
além de gerador de ficha balanceada por Papel × ND.
"""
from typing import Any, Dict, List, Optional
from .models import (
    Ameaca,
    AtaqueAmeaca,
    Atributos,
    HabilidadeAmeaca,
    PapelAmeacaEnum,
    TamanhoEnum,
)

NDS_ORDENADOS: List[str] = [
    "1/4", "1/2",
    "1", "2", "3", "4",
    "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16",
    "17", "18", "19", "20",
    "S", "S+",
]

TIPOS_AMEACA: List[str] = [
    "Animal",
    "Construto",
    "Espírito",
    "Humanoide",
    "Monstro",
    "Morto-vivo",
]

TAMANHOS_AMEACA: List[str] = [
    "Minúsculo",
    "Pequeno",
    "Médio",
    "Grande",
    "Enorme",
    "Colossal",
]

TESOUROS_AMEACA: List[str] = [
    "Nenhum",
    "Metade",
    "Padrão",
    "Dobro",
]

DESLOCAMENTO_POR_TAMANHO: Dict[str, str] = {
    "Minúsculo": "6m (4q)",
    "Pequeno": "6m (4q)",
    "Médio": "9m (6q)",
    "Grande": "12m (8q)",
    "Enorme": "15m (10q)",
    "Colossal": "18m (12q)",
}


def _row(patamar: str, atq: int, dano: int, defesa: int, rf: int, rm: int, rfr: int, pv: int, cd: int) -> Dict[str, Any]:
    return {
        "patamar": patamar,
        "ataque": atq,
        "dano_medio": dano,
        "defesa": defesa,
        "res_forte": rf,
        "res_media": rm,
        "res_fraca": rfr,
        "pv": pv,
        "cd": cd,
    }


# Tabela 2-3 A: Parâmetros de Criaturas Solos (Ameaças de Arton, p. 383)
TABELA_SOLO: Dict[str, Dict[str, Any]] = {
    "1/4": _row("Iniciante", 6, 8, 11, 3, 0, -2, 7, 12),
    "1/2": _row("Iniciante", 7, 10, 14, 6, 3, -1, 15, 13),
    "1":   _row("Iniciante", 9, 15, 16, 11, 5, 0, 35, 14),
    "2":   _row("Iniciante", 12, 18, 19, 13, 7, 2, 70, 16),
    "3":   _row("Iniciante", 14, 21, 21, 15, 9, 3, 105, 17),
    "4":   _row("Iniciante", 16, 24, 23, 16, 10, 4, 140, 18),
    "5":   _row("Veterano", 17, 40, 24, 17, 11, 5, 200, 20),
    "6":   _row("Veterano", 20, 56, 27, 18, 12, 6, 240, 22),
    "7":   _row("Veterano", 24, 62, 31, 20, 14, 7, 280, 24),
    "8":   _row("Veterano", 26, 68, 33, 21, 15, 8, 320, 26),
    "9":   _row("Veterano", 27, 74, 34, 21, 15, 9, 360, 28),
    "10":  _row("Veterano", 29, 80, 36, 22, 16, 10, 400, 30),
    "11":  _row("Campeão", 34, 130, 41, 24, 18, 11, 550, 31),
    "12":  _row("Campeão", 36, 144, 43, 26, 20, 12, 600, 33),
    "13":  _row("Campeão", 37, 158, 44, 26, 20, 13, 650, 35),
    "14":  _row("Campeão", 39, 172, 46, 28, 22, 14, 700, 38),
    "15":  _row("Campeão", 43, 186, 50, 28, 22, 15, 750, 40),
    "16":  _row("Campeão", 46, 200, 53, 30, 24, 16, 800, 42),
    "17":  _row("Lenda", 47, 270, 54, 30, 24, 17, 1020, 44),
    "18":  _row("Lenda", 49, 288, 56, 32, 26, 18, 1080, 47),
    "19":  _row("Lenda", 52, 306, 59, 32, 26, 19, 1140, 47),
    "20":  _row("Lenda", 54, 324, 61, 34, 28, 20, 1200, 49),
    "S":   _row("L+", 58, 360, 65, 36, 30, 22, 2500, 51),
    "S+":  _row("L+", 65, 500, 70, 38, 33, 25, 4000, 55),
}

# Tabela 2-3 B: Parâmetros de Criaturas Lacaios (Ameaças de Arton, p. 384)
TABELA_LACAIO: Dict[str, Dict[str, Any]] = {
    "1/4": _row("Iniciante", 7, 9, 10, 2, 0, -1, 4, 12),
    "1/2": _row("Iniciante", 9, 11, 13, 5, 3, 0, 6, 13),
    "1":   _row("Iniciante", 11, 17, 15, 10, 5, 1, 9, 14),
    "2":   _row("Iniciante", 14, 21, 18, 12, 7, 3, 14, 16),
    "3":   _row("Iniciante", 16, 24, 20, 14, 9, 4, 21, 17),
    "4":   _row("Iniciante", 17, 32, 22, 15, 10, 5, 28, 18),
    "5":   _row("Veterano", 20, 56, 23, 16, 11, 6, 40, 20),
    "6":   _row("Veterano", 24, 62, 26, 17, 12, 7, 48, 22),
    "7":   _row("Veterano", 26, 68, 30, 19, 14, 8, 56, 24),
    "8":   _row("Veterano", 27, 74, 32, 20, 15, 9, 64, 26),
    "9":   _row("Veterano", 29, 80, 33, 20, 15, 10, 72, 28),
    "10":  _row("Veterano", 34, 105, 35, 21, 16, 11, 80, 30),
    "11":  _row("Campeão", 36, 144, 40, 23, 18, 12, 110, 31),
    "12":  _row("Campeão", 37, 158, 42, 25, 20, 13, 120, 33),
    "13":  _row("Campeão", 39, 172, 43, 25, 20, 14, 130, 35),
    "14":  _row("Campeão", 43, 186, 45, 27, 22, 15, 140, 38),
    "15":  _row("Campeão", 46, 200, 49, 27, 22, 16, 150, 40),
    "16":  _row("Campeão", 47, 235, 52, 29, 24, 17, 160, 42),
    "17":  _row("Lenda", 49, 288, 53, 29, 24, 18, 204, 44),
    "18":  _row("Lenda", 52, 306, 55, 31, 26, 19, 216, 47),
    "19":  _row("Lenda", 54, 324, 58, 31, 26, 20, 228, 47),
    "20":  _row("Lenda", 56, 344, 60, 33, 28, 21, 240, 49),
    "S":   _row("L+", 60, 385, 64, 35, 30, 23, 500, 51),
    "S+":  _row("L+", 67, 540, 69, 37, 33, 26, 800, 55),
}

# Tabela 2-3 C: Parâmetros de Criaturas Especiais (Ameaças de Arton, p. 385)
TABELA_ESPECIAL: Dict[str, Dict[str, Any]] = {
    "1/4": _row("Iniciante", 4, 8, 11, 3, 0, -2, 5, 14),
    "1/2": _row("Iniciante", 5, 10, 12, 6, 3, -1, 11, 15),
    "1":   _row("Iniciante", 7, 15, 14, 11, 5, 0, 25, 16),
    "2":   _row("Iniciante", 10, 18, 17, 13, 7, 2, 49, 18),
    "3":   _row("Iniciante", 12, 21, 19, 15, 9, 3, 74, 19),
    "4":   _row("Iniciante", 14, 24, 21, 16, 10, 4, 98, 20),
    "5":   _row("Veterano", 15, 40, 22, 17, 11, 5, 140, 22),
    "6":   _row("Veterano", 18, 56, 25, 18, 12, 6, 168, 24),
    "7":   _row("Veterano", 22, 62, 29, 20, 14, 7, 196, 26),
    "8":   _row("Veterano", 24, 68, 31, 21, 15, 8, 224, 28),
    "9":   _row("Veterano", 25, 74, 32, 21, 15, 9, 252, 30),
    "10":  _row("Veterano", 27, 80, 34, 22, 16, 10, 280, 32),
    "11":  _row("Campeão", 32, 130, 39, 24, 18, 11, 385, 33),
    "12":  _row("Campeão", 34, 144, 41, 26, 20, 12, 420, 35),
    "13":  _row("Campeão", 35, 158, 42, 26, 20, 13, 455, 37),
    "14":  _row("Campeão", 37, 172, 44, 28, 22, 14, 490, 40),
    "15":  _row("Campeão", 41, 186, 48, 28, 22, 15, 525, 42),
    "16":  _row("Campeão", 44, 200, 51, 30, 24, 16, 560, 44),
    "17":  _row("Lenda", 45, 270, 52, 30, 24, 17, 714, 46),
    "18":  _row("Lenda", 47, 288, 54, 32, 26, 18, 756, 49),
    "19":  _row("Lenda", 50, 306, 57, 32, 26, 19, 798, 49),
    "20":  _row("Lenda", 52, 324, 59, 34, 28, 20, 840, 51),
    "S":   _row("L+", 55, 360, 63, 36, 30, 22, 1750, 55),
    "S+":  _row("L+", 60, 500, 67, 38, 33, 25, 2800, 60),
}

TABELAS_POR_PAPEL: Dict[str, Dict[str, Dict[str, Any]]] = {
    "solo": TABELA_SOLO,
    "lacaio": TABELA_LACAIO,
    "especial": TABELA_ESPECIAL,
}


def nd_para_numero(nd: str) -> int:
    if nd in ("1/4", "1/2"):
        return 0
    if nd == "S":
        return 22
    if nd == "S+":
        return 25
    try:
        return int(nd)
    except ValueError:
        return 1


def sugerir_formula_dano(dano_medio: int) -> str:
    """Converte dano médio da Tabela 2-3 em uma fórmula prática de dados (ex: 2d8+9)."""
    if dano_medio <= 10:
        bonus = max(1, dano_medio - 4)
        return f"1d6+{bonus}"
    if dano_medio <= 25:
        bonus = max(2, dano_medio - 9)
        return f"2d8+{bonus}"
    if dano_medio <= 80:
        dados = max(2, min(8, dano_medio // 10))
        bonus = max(4, round(dano_medio - dados * 5.5))
        return f"{dados}d10+{bonus}"
    dados = max(4, min(12, dano_medio // 25))
    bonus = max(10, round(dano_medio - dados * 6.5))
    return f"{dados}d12+{bonus}"


def obter_tabelas_construtor() -> Dict[str, Any]:
    return {
        "fonte": "Ameaças de Arton (Manual de Criação de Ameaças, p. 378–390)",
        "nds": NDS_ORDENADOS,
        "tipos": TIPOS_AMEACA,
        "tamanhos": TAMANHOS_AMEACA,
        "tesouros": TESOUROS_AMEACA,
        "deslocamento_por_tamanho": DESLOCAMENTO_POR_TAMANHO,
        "tabelas": TABELAS_POR_PAPEL,
    }


def gerar_ameaca_manual(
    nome: str,
    nd: str = "1",
    papel: str = "solo",
    tipo: str = "Monstro",
    tamanho: str = "Médio",
    res_forte: str = "fortitude",
    res_media: str = "reflexos",
    res_fraca: str = "vontade",
    deslocamento: Optional[str] = None,
    pontos_de_mana: Optional[int] = None,
    sentidos: Optional[List[str]] = None,
    ataques: Optional[List[Dict[str, Any]]] = None,
    habilidades: Optional[List[Dict[str, Any]]] = None,
    atributos: Optional[Dict[str, int]] = None,
    equipamento: Optional[str] = None,
    tesouro: str = "Padrão",
    ajustes: Optional[Dict[str, int]] = None,
) -> Ameaca:
    """Gera uma ficha de Ameaça balanceada seguindo a Tabela 2-3 oficial."""
    papel_norm = papel.lower() if papel.lower() in TABELAS_POR_PAPEL else "solo"
    nd_norm = nd if nd in TABELAS_POR_PAPEL[papel_norm] else "1"
    params = TABELAS_POR_PAPEL[papel_norm][nd_norm]
    aj = ajustes or {}

    defesa = max(10, params["defesa"] + int(aj.get("defesa", 0)))
    pv = max(1, params["pv"] + int(aj.get("pv", 0)))
    ataque_bonus = params["ataque"] + int(aj.get("ataque", 0))
    cd = params["cd"] + int(aj.get("cd", 0))

    res_map = {
        res_forte.lower(): params["res_forte"],
        res_media.lower(): params["res_media"],
        res_fraca.lower(): params["res_fraca"],
    }
    fort = res_map.get("fortitude", params["res_media"])
    refl = res_map.get("reflexos", params["res_media"])
    vont = res_map.get("vontade", params["res_fraca"])

    nd_num = nd_para_numero(nd_norm)
    metade_nd = nd_num // 2
    bonus_treino = 2 if nd_num <= 6 else (4 if nd_num <= 14 else 6)

    atrib_obj = Atributos(**(atributos or {}))
    iniciativa = metade_nd + bonus_treino + atrib_obj.destreza
    percepcao = metade_nd + bonus_treino + atrib_obj.sabedoria

    if ataques:
        ataques_list = []
        for a in ataques:
            mod_raw = a.get("modalidade") or a.get("tipo") or "corpo a corpo"
            mod_norm = "à distância" if "dist" in str(mod_raw).lower() else "corpo a corpo"
            ataques_list.append(
                AtaqueAmeaca(
                    nome=a.get("nome", "Ataque"),
                    modalidade=mod_norm,
                    bonus_ataque=int(a.get("bonus_ataque", a.get("bonus", ataque_bonus))),
                    dano=str(a.get("dano", sugerir_formula_dano(params["dano_medio"]))),
                )
            )
    else:
        ataques_list = [
            AtaqueAmeaca(
                nome="Ataque Principal",
                modalidade="corpo a corpo",
                bonus_ataque=ataque_bonus,
                dano=sugerir_formula_dano(params["dano_medio"]),
            )
        ]

    habs_list = [HabilidadeAmeaca(**h) for h in (habilidades or [])]

    pm_final = pontos_de_mana
    if pm_final is None and papel_norm == "especial":
        pm_final = max(6, nd_num * 3)

    return Ameaca(
        nome=nome.strip() or "Nova Ameaça",
        nd=nd_norm,
        tipo=tipo,
        tamanho=TamanhoEnum(tamanho) if tamanho in TAMANHOS_AMEACA else TamanhoEnum.MEDIO,
        papel=PapelAmeacaEnum(papel_norm),
        iniciativa=iniciativa,
        percepcao=percepcao,
        sentidos=sentidos or [],
        defesa=defesa,
        fortitude=fort,
        reflexos=refl,
        vontade=vont,
        pontos_de_vida=pv,
        pontos_de_mana=pm_final,
        deslocamento=deslocamento or DESLOCAMENTO_POR_TAMANHO.get(tamanho, "9m (6q)"),
        ataques=ataques_list,
        habilidades=habs_list,
        cd_magias=cd,
        atributos=atrib_obj,
        equipamento=equipamento,
        tesouro=tesouro,
        tags=["Custom", f"Patamar: {params['patamar']}"],
        fonte={"livro": "Manual de Criação de Ameaças (Ameaças de Arton)", "custom": True},
    )
