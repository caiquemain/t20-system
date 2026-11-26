"""Motor de inventário (T20 JdA, Capítulo 3): carga e ataques de equipamento."""
from typing import Dict, List, Optional

from ..models import Personagem, Ataque
from ..dados_equipamentos import DADOS_ARMAS, DADOS_ARMADURAS, DADOS_GERAIS


def catalogo_do_item(nome: str) -> Optional[Dict]:
    """Retorna os dados do catálogo (arma ou armadura/escudo) pelo nome."""
    if nome in DADOS_ARMAS:
        return {"_categoria": "Arma", **DADOS_ARMAS[nome]}
    if nome in DADOS_ARMADURAS:
        d = DADOS_ARMADURAS[nome]
        return {"_categoria": d.get("tipo_armadura", "Armadura"), **d}
    if nome in DADOS_GERAIS:
        return {"_categoria": "Geral", **DADOS_GERAIS[nome]}
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


def espacos_item(item, inventario_organizado: bool = False) -> float:
    """Espaços de um item (catálogo sobrepõe item.espaco), vezes quantidade.
    Com Inventário Organizado (T20 p.130), itens de 0,5 espaço passam a ocupar 0,25."""
    cat = catalogo_do_item(item.nome)
    esp = float(cat.get("espacos", item.espaco) if cat else item.espaco)
    if inventario_organizado and esp == 0.5:
        esp = 0.25
    return esp * max(1, item.qtd)


def sincronizar_carga(ficha: Personagem) -> None:
    """Limite = 10 + 2 por FOR (ou -1 por FOR negativo) + bônus de habilidades/itens.
    Moedas: cada 1.000 moedas = 1 espaço (T20 JdA p.141). Sobrecarga > limite."""
    inv = ficha.inventario
    for_ = mod_atributo(ficha, "for")
    base_carga = max(0, 10 + 2 * for_) if for_ >= 0 else max(0, 10 + for_)
    bonus_carga = sum(
        int((h.efeitos or {}).get("carga_max_bonus", 0) or 0)
        for h in (ficha.habilidades or [])
    )
    tem_inv_org = any(
        (h.efeitos or {}).get("carga_soma_int")
        or (h.efeitos or {}).get("carga_soma_atributo") == "int"
        or (h.nome or "") == "Inventário Organizado"
        for h in (ficha.habilidades or [])
    )
    if tem_inv_org:
        bonus_carga += max(0, mod_atributo(ficha, "int"))
    # Mochila de aventureiro vestida/equipada: +2 espaços de carga (T20 p.156)
    # Mochila de carga equipada: +10 espaços de carga (T20 p.345)
    bonus_mochila = 0
    for it in (inv.equipamentos or []):
        if not it.equipado:
            continue
        nome_low = (it.nome or "").strip().lower()
        if nome_low == "mochila de carga":
            bonus_mochila = max(bonus_mochila, 10)
        elif nome_low == "mochila de aventureiro":
            bonus_mochila = max(bonus_mochila, 2)
    bonus_carga += bonus_mochila

    inv.carga_maxima = base_carga + bonus_carga
    espacos_itens = sum(
        0 if (i.nome or "").strip().lower() == "mochila de carga" else espacos_item(i, inventario_organizado=tem_inv_org)
        for i in inv.equipamentos
    )
    total_moedas = max(0, int(inv.dinheiro.tl or 0)) + max(0, int(inv.dinheiro.tp or 0)) + max(0, int(inv.dinheiro.to or 0))
    espacos_moedas = total_moedas // 1000
    inv.carga_total = int(espacos_itens + espacos_moedas)
    inv.sobrecargado = (espacos_itens + espacos_moedas) > inv.carga_maxima


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

        # Esgrima Mágica (Bardo, T20 p.43): sob Inspiração, substitui Luta por Atuação
        # em armas corpo a corpo leves ou de uma mão (usa Atuação se for melhor).
        if (
            teste == "Luta"
            and cat.get("empunhadura") in ("Leve", "Uma Mão")
            and "inspiracao" in (getattr(ficha, "condicoes_ativas", None) or [])
            and any((h.nome or "") == "Esgrima Mágica" for h in ficha.habilidades)
        ):
            p_luta = (ficha.pericias or {}).get("Luta")
            p_atuacao = (ficha.pericias or {}).get("Atuação")
            total_luta = p_luta.total if p_luta else 0
            total_atuacao = p_atuacao.total if p_atuacao else 0
            if total_atuacao >= total_luta:
                teste = "Atuação"
                especial.append("Esgrima Mágica (Atuação)")

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

        # Esgrimista (Bucaneiro, T20 p.48): soma Inteligência no dano com armas corpo a corpo
        # leves ou ágeis (limitado pelo nível).
        eh_leve_ou_agil = (
            cat.get("proposito") == "Corpo a Corpo"
            and (cat.get("empunhadura") == "Leve" or "ágil" in (cat.get("habilidades") or []))
        )
        if eh_leve_ou_agil:
            for hab in ficha.habilidades:
                d_extra = (hab.efeitos or {}).get("dano_soma_atributo_extra")
                if isinstance(d_extra, dict) and d_extra.get("atributo"):
                    attr_cod = str(d_extra["atributo"]).lower()[:3]
                    val_attr = mod_atributo(ficha, attr_cod)
                    if d_extra.get("limite_por_nivel", True):
                        val_attr = min(val_attr, int(ficha.cabecalho.nivel_total or 1))
                    if val_attr > 0:
                        bonus_dano_arma += val_attr
                        especial.append(f"{hab.nome} (+{val_attr} dano)")

        # Pistoleiro (Bucaneiro, T20 p.48): +2 nas rolagens de dano com armas de fogo
        if categoria_arma == "Fogo":
            for hab in ficha.habilidades:
                dbc = (hab.efeitos or {}).get("dano_bonus_condicional")
                if isinstance(dbc, dict) and dbc.get("tipo") == "arma_fogo" and dbc.get("valor"):
                    v_fogo = int(dbc["valor"])
                    bonus_dano_arma += v_fogo
                    especial.append(f"{hab.nome} (+{v_fogo} dano)")

        # En Garde (Bucaneiro, T20 p.48): +2 margem de ameaça com armas leves/ágeis sob postura
        conds = getattr(ficha, "condicoes_ativas", None) or []
        if eh_leve_ou_agil and "en_garde" in conds and any((h.nome or "") == "En Garde" for h in ficha.habilidades):
            especial.append("En Garde (+2 margem de ameaça)")

        # Bravata Imprudente (Bucaneiro, T20 p.48): +2 ataque e margem de ameaça quando cumprida
        if "bravata_imprudente" in conds and any((h.nome or "") == "Bravata Imprudente" for h in ficha.habilidades):
            especial.append("Bravata Imprudente (+2 ataque e margem de ameaça)")

        # Arqueiro (Caçador/Guerreiro, T20 p.50): soma Sabedoria no dano com armas à distância (limitado pelo nível)
        if cat.get("proposito") == "À Distância":
            for hab in ficha.habilidades:
                ddsa = (hab.efeitos or {}).get("dano_distancia_soma_atributo")
                if ddsa:
                    if isinstance(ddsa, dict):
                        attr_cod = str(ddsa.get("atributo", "")).lower()[:3]
                        limite_nv = bool(ddsa.get("limite_por_nivel", True))
                    else:
                        attr_cod = str(ddsa).lower()[:3]
                        limite_nv = True
                    val_attr = mod_atributo(ficha, attr_cod)
                    if limite_nv:
                        val_attr = min(val_attr, int(ficha.cabecalho.nivel_total or 1))
                    if val_attr > 0:
                        bonus_dano_arma += val_attr
                        especial.append(f"{hab.nome} (+{val_attr} dano)")

        # Escaramuça / Escaramuça Superior (Caçador, T20 p.50): +1d8 / +1d12 dano quando ativa (sem armadura pesada)
        if "escaramuca" in conds:
            usa_pesada_inv = any(
                it.equipado and (catalogo_do_item(it.nome) or {}).get("tipo_armadura") == "Pesada"
                for it in ficha.inventario.equipamentos
            )
            if not usa_pesada_inv:
                if any((h.efeitos or {}).get("escaramuca_superior") or (h.nome or "") == "Escaramuça Superior" for h in ficha.habilidades):
                    especial.append("Escaramuça Superior (+1d12 dano)")
                elif any((h.efeitos or {}).get("escaramuca") or (h.nome or "") == "Escaramuça" for h in ficha.habilidades):
                    especial.append("Escaramuça (+1d8 dano)")

        # Especialização em Arma / Mestre em Arma / Campeão (Guerreiro, T20 p.65-66)
        nome_arma_low = item.nome.strip().lower()
        for hab in ficha.habilidades:
            ef_h = hab.efeitos or {}
            arma_esc = str((hab.escolhas_aplicadas or {}).get("arma", "")).strip().lower()
            if ef_h.get("especializacao_arma_dano") and arma_esc == nome_arma_low:
                v_esp = int(ef_h["especializacao_arma_dano"])
                bonus_dano_arma += v_esp
                especial.append(f"Especialização em Arma (+{v_esp} dano)")
            if ef_h.get("mestre_arma_passo_dano") and arma_esc == nome_arma_low:
                especial.append("Mestre em Arma (+1 passo de dano)")
            if ef_h.get("passo_dano_global"):
                especial.append("Campeão (+1 passo de dano)")

        # Armeiro / Balística (Inventor, T20 p.68-69): usa Int no lugar de For/Des
        mod_int = mod_atributo(ficha, "int")
        if cat.get("proposito") == "Corpo a Corpo" and any(
            (h.efeitos or {}).get("armeiro_int_corpo_a_corpo") for h in ficha.habilidades
        ):
            if mod_int > mod_atributo(ficha, "for"):
                especial.append(f"Armeiro (Int +{mod_int} ataque/dano)")
        elif cat.get("proposito") == "À Distância" and any(
            (h.efeitos or {}).get("balistica_int_distancia") for h in ficha.habilidades
        ):
            if mod_int > mod_atributo(ficha, "des"):
                especial.append(f"Balística (Int +{mod_int} ataque)")

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
        elif (item.nome or "").strip().lower() == "casaco longo":
            pen += 2
    # Sobrecarga: -5 (regra p.141: "penalidade de armadura -5")
    if ficha.inventario.sobrecargado:
        pen += 5
    return pen
