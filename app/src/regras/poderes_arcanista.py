# -*- coding: utf-8 -*-
"""Processador de Poderes de Arcanista (Lote 1) — efeitos numéricos na Pilha.

Cobre: Poder Mágico, Aumento de Atributo, Fortalecimento Arcano,
Especialista/Mestre em Escola, Alta Arcana, Arcano de Batalha,
Envolto em Mistério, Familiar (10 tipos) e Linhagens Dracônica/Feérica.
"""
import logging
from ..models import Personagem, StatCalculado
from ..dados_familiares import FAMILIARES_ARCANOS
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")

MAPA_ATTR_CURTO = {
    'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
    'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
}


def _efeitos(hab):
    ef = (hab.efeitos or {}).copy()
    if hab.escolhas_aplicadas:
        ef.update(hab.escolhas_aplicadas)
    return ef


def _habs_arcanista(ficha):
    return [h for h in ficha.habilidades
            if "Arcanista" in (h.tipo or "") or (h.fonte or "") == "Arcanista"]


def _nivel_arcanista(ficha):
    for cl in ficha.classes:
        if cl.nome == "Arcanista":
            return cl.nivel
    return ficha.classes[0].nivel if ficha.classes else 1


def _attr_chave(ficha):
    sub = ""
    for cl in ficha.classes:
        if cl.nome == "Arcanista":
            sub = (cl.subclasse or "").strip()
    return "carisma" if sub == "Feiticeiro" else "inteligencia"


def aplicar_poderes_arcanista(ficha: Personagem) -> Personagem:
    habs = _habs_arcanista(ficha)
    tem_linhagem = any("Linhagem" in (h.nome or "") for h in ficha.habilidades)
    nv = _nivel_arcanista(ficha)
    eh_arcanista = any(cl.nome == "Arcanista" for cl in ficha.classes)

    # Reset de campos derivados (idempotência entre recálculos)
    ficha.combate.cd_por_escola = {}
    ficha.combate.cd_por_resistencia = {}
    ficha.combate.custo_por_escola = {}
    ficha.combate.bonus_dano_magias = 0
    # Alta Arcana: habilidade de classe AUTOMÁTICA no nível 20 (independe de poderes)
    ficha.combate.custo_arcano_metade = eh_arcanista and nv >= 20

    if not habs and not tem_linhagem:
        return ficha

    nomes = [h.nome for h in habs]

    if ficha.status.pv_calc is None:
        ficha.status.pv_calc = StatCalculado()
    if ficha.status.pm_calc is None:
        ficha.status.pm_calc = StatCalculado()

    # ── Poder Mágico: +1 PM por nível de arcanista ──
    if "Poder Mágico" in nomes:
        ficha.status.pm_calc.adicionar_bonus(
            fonte="Poder Mágico", categoria="Poder de Classe", valor=nv)

    # ── Aumento de Atributo: +1 no atributo escolhido ──
    for h in habs:
        if h.nome == "Aumento de Atributo":
            attr = _efeitos(h).get("atributo")
            if attr:
                full = MAPA_ATTR_CURTO.get(attr, attr)
                if full in ficha.atributos_calc:
                    ficha.atributos_calc[full].adicionar_bonus(
                        fonte="Poder: Aumento de Atributo", categoria="Poder", valor=1)

    # ── Fortalecimento Arcano: +1 CD (+2 se lança 4º círculo) ──
    cd_calc = StatCalculado(base=10, total=10)
    if "Fortalecimento Arcano" in nomes:
        val = 2 if (ficha.combate.circulo_maximo or 0) >= 4 else 1
        cd_calc.adicionar_bonus(
            fonte="Poder: Fortalecimento Arcano", categoria="Poder", valor=val)
    ficha.combate.cd_magias_calc = cd_calc
    ficha.combate.cd_magias = cd_calc.total

    # ── Especialista / Mestre em Escola ──
    for h in habs:
        ef = _efeitos(h)
        escola = ef.get("escola")
        if not escola:
            continue
        if h.nome == "Especialista em Escola":
            ficha.combate.cd_por_escola[escola] = \
                ficha.combate.cd_por_escola.get(escola, 0) + 2
        elif h.nome == "Mestre em Escola":
            ficha.combate.custo_por_escola[escola] = \
                ficha.combate.custo_por_escola.get(escola, 0) + 1

    # ── Arcano de Batalha: +attr-chave no dano de magias ──
    if "Arcano de Batalha" in nomes:
        ficha.combate.bonus_dano_magias = calcular_modificador(
            getattr(ficha.atributos, _attr_chave(ficha)))

    # ── Envolto em Mistério: nota condicional nas perícias ──
    if "Envolto em Mistério" in nomes:
        for p in ("Enganação", "Intimidação"):
            info = ficha.pericias.get(p)
            if info is not None:
                nota = "+5 vs não treinados em Conhecimento/Misticismo (Envolto em Mistério)"
                if nota not in info.fontes_bonus:
                    info.fontes_bonus.append(nota)

    # ── Familiar: benefícios por tipo ──
    fam = None
    for h in habs:
        if h.nome == "Familiar":
            fam = _efeitos(h).get("familiar")
    if fam and fam in FAMILIARES_ARCANOS:
        ben = FAMILIARES_ARCANOS[fam]
        for res, val in ben.get("cd_resistencia", {}).items():
            ficha.combate.cd_por_resistencia[res] = \
                ficha.combate.cd_por_resistencia.get(res, 0) + val
        for im in ben.get("imunidades", []):
            if im not in ficha.status.imunidades:
                ficha.status.imunidades.append(im)
        for se in ben.get("sentidos", []):
            if se not in ficha.status.sentidos:
                ficha.status.sentidos.append(se)
        for p, val in ben.get("pericia_bonus", {}).items():
            info = ficha.pericias.get(p)
            if info is not None and info.calculo is not None:
                info.calculo.adicionar_bonus(
                    fonte=f"Familiar: {fam}", categoria="Poder", valor=val)
        if ben.get("pv_atributo_chave"):
            ficha.status.pv_calc.adicionar_bonus(
                fonte=f"Familiar: {fam}", categoria="Poder",
                valor=calcular_modificador(
                    getattr(ficha.atributos, _attr_chave(ficha))))

    # ── Linhagens do Feiticeiro ──
    heranca = ("superior" if "Herança Superior" in nomes else
               "aprimorada" if "Herança Aprimorada" in nomes else "basica")
    for h in ficha.habilidades:
        nome_h = h.nome or ""
        if "Linhagem" not in nome_h:
            continue
        ef = _efeitos(h)
        tipo_dano = ef.get("tipo_dano") or ef.get("dano")
        if "Dracônica" in nome_h:
            mod_car = calcular_modificador(ficha.atributos.carisma)
            if mod_car:
                ficha.status.pv_calc.adicionar_bonus(
                    fonte="Linhagem Dracônica (básica)", categoria="Poder", valor=mod_car)
            if tipo_dano:
                rd_str = f"{tipo_dano} 5"
                if rd_str not in ficha.status.rd:
                    ficha.status.rd.append(rd_str)
            if heranca == "superior":
                if mod_car:
                    ficha.status.pv_calc.adicionar_bonus(
                        fonte="Linhagem Dracônica (superior)", categoria="Poder", valor=mod_car)
                im = f"Imune a {tipo_dano}"
                if im not in ficha.status.imunidades:
                    ficha.status.imunidades.append(im)
        elif "Feérica" in nome_h:
            if heranca == "superior" and "carisma" in ficha.atributos_calc:
                ficha.atributos_calc["carisma"].adicionar_bonus(
                    fonte="Linhagem Feérica (superior)", categoria="Poder", valor=2)
            # Herança básica: +1 magia conhecida e treinado em Enganação
            if ficha.combate.magias_calc is not None:
                ficha.combate.magias_calc.adicionar_bonus(
                    fonte="Linhagem Feérica (básica)", categoria="Poder", valor=1)
                ficha.combate.limite_magias = ficha.combate.magias_calc.total
            info = ficha.pericias.get("Enganação")
            if info is not None:
                nota = "Treinado por Linhagem Feérica (básica)"
                if nota not in info.fontes_bonus:
                    info.fontes_bonus.append(nota)

    # ── Sincronização final (preservando estado "cheio" p/ Descansar) ──
    novo_pv_max = ficha.status.pv_calc.total
    novo_pm_max = ficha.status.pm_calc.total
    pv_estava_cheio = ficha.status.pv.maximo > 0 and ficha.status.pv.atual >= ficha.status.pv.maximo
    pm_estava_cheio = ficha.status.pm.maximo > 0 and ficha.status.pm.atual >= ficha.status.pm.maximo
    ficha.status.pv.maximo = novo_pv_max
    ficha.status.pm.maximo = novo_pm_max
    if pv_estava_cheio:
        ficha.status.pv.atual = novo_pv_max
    if pm_estava_cheio:
        ficha.status.pm.atual = novo_pm_max
    for stat in (ficha.status.pv, ficha.status.pm):
        if stat.atual == 0 or stat.atual > stat.maximo:
            stat.atual = stat.maximo
    for full, st in ficha.atributos_calc.items():
        if hasattr(ficha.atributos, full):
            setattr(ficha.atributos, full, st.total)

    return ficha
