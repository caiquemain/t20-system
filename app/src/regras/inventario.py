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


# Abreviações T20 -> nomes de campo no modelo Personagem
_ALIASES = {
    "for": "forca", "des": "destreza", "con": "constituicao",
    "int": "inteligencia", "sab": "sabedoria", "car": "carisma",
}


def mod_atributo(ficha: Personagem, chave: str) -> int:
    """Lê o modificador de um atributo de forma defensiva (for/des/con...)."""
    attrs = getattr(ficha, "atributos", None)
    if attrs is None:
        return 0
    nomes = [chave, _ALIASES.get(chave, ""), chave + "_"]
    for nome in nomes:
        if not nome:
            continue
        obj = getattr(attrs, nome, None)
        if obj is None and isinstance(attrs, dict):
            obj = attrs.get(nome)
        if obj is None:
            continue
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


def _proficiente_categoria(categoria: str, profs: str) -> bool:
    """Checa proficiência por categoria tolerando o plural do livro.

    'Armas Marciais' NÃO contém a substring 'marcial' (marcial -> marciais),
    então testamos singular, plural -s (exótica -> exóticas) e plural
    -ais (marcial -> marciais).
    """
    c = categoria.lower()
    return (
        c in profs
        or c + "s" in profs
        or (c[:-1] + "is" in profs if c.endswith("al") else False)  # marcial -> marciais
    )


def efeitos_de_armas_especificas(ficha: Personagem) -> dict:
    """Efeitos de habilidades que modificam armas específicas por nome.

    Consome (efeitos + escolhas_aplicadas, padrão do projeto):
    - bonus_dano_arma: {arma: +X} -> dano da arma empunhada
      (Mestre do Tridente: +2 com azagaia, lança e tridente)
    - proficiencia_simples: [arma] -> arma conta como Simples p/ proficiência
      ("para você, o tridente é uma arma simples")
    Retorna {arma_lower: {bonus_dano, fonte_dano, simples, fonte_simples}}.
    """
    out: dict = {}
    for hab in ficha.habilidades:
        efeitos = dict(hab.efeitos or {})
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        for arma, val in (efeitos.get("bonus_dano_arma") or {}).items():
            e = out.setdefault(str(arma).lower(), {})
            if int(val) > e.get("bonus_dano", 0):
                e["bonus_dano"] = int(val)
                e["fonte_dano"] = hab.nome
        for arma in (efeitos.get("proficiencia_simples") or []):
            e = out.setdefault(str(arma).lower(), {})
            e["simples"] = True
            e["fonte_simples"] = hab.nome
    return out


def ataques_de_equipamento(ficha: Personagem) -> List[Ataque]:
    """Armas empunhadas viram ataques (fonte=Equipamento)."""
    ataques: List[Ataque] = []
    profs = " ".join(
        list(getattr(ficha, "proficiencias", None) or []) +
        list(getattr(ficha.status, "proficiencias", None) or [])
    ).lower()
    mods_arma = efeitos_de_armas_especificas(ficha)
    for item in ficha.inventario.equipamentos:
        cat = catalogo_do_item(item.nome)
        if not cat or cat.get("_categoria") != "Arma" or not item.equipado:
            continue
        if cat.get("municao"):
            continue
        categoria_arma = cat.get("categoria", "Simples")
        mod_arma = mods_arma.get(item.nome.lower(), {})
        proficiente = (
            _proficiente_categoria(categoria_arma, profs)
            or (_proficiente_categoria("Marcial", profs) and cat.get("marcial_duas_maos"))
            or item.nome.lower() in profs  # proficiência concedida por nome (efeitos, ex.: tridente)
        )
        # Ex.: Mestre do Tridente: "para você, o tridente é uma arma simples".
        # Só MELHORA: guerreiro proficiente em marciais continua proficiente
        # no tridente; a racial socorre quem só tem armas simples.
        simples_pela_habilidade = False
        if mod_arma.get("simples") and not proficiente:
            simples_pela_habilidade = "simples" in profs
            proficiente = simples_pela_habilidade
        teste = "Luta" if cat.get("proposito") == "Corpo a Corpo" else "Pontaria"
        especial = []
        if cat.get("habilidades"):
            outras = [h for h in cat["habilidades"] if not (h == "versátil" and cat.get("versatil"))]
            if outras:
                especial.append(", ".join(outras))
        if cat.get("versatil"):
            especial.append(f"Versátil: {cat['versatil']} (manobra, não soma no dano)")
        if "desbalanceada" in cat.get("habilidades", []):
            especial.append("-2 ataque (desbalanceada)")
        if simples_pela_habilidade:
            especial.append(f"{mod_arma.get('fonte_simples', 'Habilidade')}: conta como arma simples")
        bonus_dano_arma = mod_arma.get("bonus_dano", 0)
        if bonus_dano_arma:
            especial.append(f"{mod_arma.get('fonte_dano', 'Habilidade')} (+{bonus_dano_arma} dano)")
        if not proficiente:
            especial.append("-5 ataque (não proficiente)")
        ataques.append(Ataque(
            nome=item.nome,
            bonus_ataque="+0",
            dano=(f"{cat['dano']}+{bonus_dano_arma}" if bonus_dano_arma and cat.get("dano") else cat.get("dano") or "-"),
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


def calcular_penalidade_armadura(ficha: Personagem) -> int:
    """Penalidade acumulada de armadura vestida + escudo empunhado + sobrecarga."""
    pen = 0
    for item in ficha.inventario.equipamentos:
        if not item.equipado:
            continue
        cat = catalogo_do_item(item.nome)
        if not cat:
            continue
        # Armadura vestida (tipo_armadura: Leve/Pesada/Escudo)
        tipo_arm = cat.get("tipo_armadura")
        if tipo_arm in ["Leve", "Pesada", "Escudo"]:
            pen += abs(cat.get("penalidade_armadura", 0))
    # Sobrecarga: -5 (regra p.141: "penalidade de armadura -5")
    if ficha.inventario.sobrecargado:
        pen += 5
    return pen
