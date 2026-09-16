"""Motor de inventário (T20 JdA, Capítulo 3): carga e ataques de equipamento."""
from typing import Dict, List, Optional

from ..models import Personagem, Ataque
from ..dados_equipamentos import DADOS_ARMAS, DADOS_ARMADURAS


def catalogo_do_item(nome: str) -> Optional[Dict]:
    """Retorna os dados do catálogo (arma ou armadura/escudo) pelo nome."""
    if nome in DADOS_ARMAS:
        return {"_categoria": "Arma", **DADOS_ARMAS[nome]}
    if nome in DADOS_ARMADURAS:
        d = DADOS_ARMADURAS[nome]
        return {"_categoria": d.get("tipo_armadura", "Armadura"), **d}
    return None


def mod_atributo(ficha: Personagem, chave: str) -> int:
    """Lê o modificador de um atributo de forma defensiva (for/des/con...)."""
    attrs = getattr(ficha, "atributos", None)
    if attrs is None:
        return 0
    obj = getattr(attrs, chave, None)
    if obj is None:
        obj = getattr(attrs, chave + "_", None)
    if obj is None and isinstance(attrs, dict):
        obj = attrs.get(chave) or attrs.get(chave + "_")
    if obj is None:
        return 0
    if isinstance(obj, (int, float)):
        return int(obj)
    for campo in ("mod", "modificador", "total", "valor"):
        v = obj.get(campo) if isinstance(obj, dict) else getattr(obj, campo, None)
        if isinstance(v, (int, float)):
            return int(v)
    return 0


def espacos_item(item) -> float:
    """Espaços de um item (catálogo sobrepõe item.espaco), vezes quantidade."""
    cat = catalogo_do_item(item.nome)
    esp = cat.get("espacos", item.espaco) if cat else item.espaco
    return float(esp) * max(1, item.qtd)


def sincronizar_carga(ficha: Personagem) -> None:
    """Limite = 10 + 2 por FOR (ou -1 por FOR negativo). Sobrecarga > limite."""
    inv = ficha.inventario
    for_ = mod_atributo(ficha, "for")
    inv.carga_maxima = max(0, 10 + 2 * for_) if for_ >= 0 else max(0, 10 + for_)
    inv.carga_total = int(sum(espacos_item(i) for i in inv.equipamentos))
    inv.sobrecargado = inv.carga_total > inv.carga_maxima


def ataques_de_equipamento(ficha: Personagem) -> List[Ataque]:
    """Armas empunhadas viram ataques (fonte=Equipamento)."""
    ataques: List[Ataque] = []
    profs = " ".join(getattr(ficha, "proficiencias", []) or []).lower()
    for item in ficha.inventario.equipamentos:
        cat = catalogo_do_item(item.nome)
        if not cat or cat.get("_categoria") != "Arma" or not item.equipado:
            continue
        if cat.get("municao"):
            continue
        categoria_arma = cat.get("categoria", "Simples")
        proficiente = (
            categoria_arma.lower() in profs
            or ("marcial" in profs and cat.get("marcial_duas_maos"))
        )
        teste = "Luta" if cat.get("proposito") == "Corpo a Corpo" else "Pontaria"
        especial = []
        if cat.get("habilidades"):
            especial.append(", ".join(cat["habilidades"]))
        if cat.get("versatil"):
            especial.append(cat["versatil"])
        if "desbalanceada" in cat.get("habilidades", []):
            especial.append("-2 ataque (desbalanceada)")
        if not proficiente:
            especial.append("-5 ataque (não proficiente)")
        ataques.append(Ataque(
            nome=item.nome,
            bonus_ataque="+0",
            dano=cat.get("dano") or "-",
            critico=cat.get("critico", "x2"),
            tipo=cat.get("tipo") or "-",
            alcance=cat.get("alcance") or "Curto",
            teste=teste,
            especial="; ".join(especial),
            fonte="Equipamento",
        ))
    return ataques


def sincronizar_ataques_equipamento(ficha: Personagem) -> None:
    """Remove ataques de equipamento antigos e re-injeta os atuais."""
    ficha.combate.ataques = [
        a for a in ficha.combate.ataques if a.fonte != "Equipamento"
    ] + ataques_de_equipamento(ficha)
