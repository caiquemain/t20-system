# -*- coding: utf-8 -*-
"""Processamento mecânico das escolhas interativas de suplementos (Ameaças + Atlas).

Executa dentro de `garantir_habilidades_iniciais` (antes de atributos, status,
perícias, combate e magias) para que toda escolha salva em `escolhas_aplicadas`
aplique efeitos reais no motor e limpe escolhas antigas ao ser alterada.
"""
from __future__ import annotations

from ..dados_habilidades import HABILIDADES_GERAIS
from ..dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from ..dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from ..models import Habilidade, Personagem

_ATTR_FULL_TO_SHORT = {
    "forca": "For",
    "destreza": "Des",
    "constituicao": "Con",
    "inteligencia": "Int",
    "sabedoria": "Sab",
    "carisma": "Car",
}


def _buscar_poder_catalogo(nome: str) -> dict | None:
    if not nome:
        return None
    for dic in (DADOS_HABILIDADES_CLASSE, HABILIDADES_GERAIS, DADOS_PODERES_TORMENTA):
        if nome in dic and isinstance(dic[nome], dict):
            return dic[nome]
        for v in dic.values():
            if isinstance(v, dict) and v.get("nome") == nome:
                return v
    return None


def processar_escolhas_suplementos(ficha: Personagem) -> None:
    """Resolve escolhas interativas de raças/origens de suplementos em efeitos reais."""
    if not ficha.habilidades:
        return

    # Remove sub-habilidades derivadas de escolhas anteriores para recalcular do zero
    ficha.habilidades = [
        h for h in ficha.habilidades
        if not (h.fonte or "").startswith("Escolha: ")
    ]
    nomes_existentes = {h.nome for h in ficha.habilidades}
    extras: list[Habilidade] = []

    def _injetar(nome: str, tipo: str, descricao: str, origem_hab: str, efeitos: dict, nivel: int | None = None):
        if not nome or nome in nomes_existentes:
            return
        h = Habilidade(
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            fonte=f"Escolha: {origem_hab}",
            efeitos=dict(efeitos),
            escolhas_aplicadas={},
        )
        if nivel is not None and hasattr(h, "nivel"):
            h.nivel = nivel
        extras.append(h)
        nomes_existentes.add(nome)

    # Detecta se Kallyanach escolheu Escamas Elementais (aumenta RD da Herança Dracônica para 10)
    tem_escamas_elementais = False
    for hab in ficha.habilidades:
        if hab.nome == "Bênção de Kallyadranoch":
            esc = hab.escolhas_aplicadas or {}
            if "Escamas Elementais" in (esc.get("bencao_1"), esc.get("bencao_2")):
                tem_escamas_elementais = True

    for hab in list(ficha.habilidades):
        esc = hab.escolhas_aplicadas or {}
        if not esc:
            continue
        ef = dict(hab.efeitos or {})

        # ── ATLAS: DUPLO FEÉRICO ──
        if hab.nome == "Origem Regional: Duplo Feérico":
            hab_val = str(esc.get("habilidade_nv1") or "").strip()
            if hab_val:
                if "::" in hab_val:
                    classe_orig, nome_hab = hab_val.split("::", 1)
                else:
                    classe_orig, nome_hab = "", hab_val

                if nome_hab.lower() == "magias":
                    ef_mag: dict = {"pm_max_ini": 1}
                    magia_1 = str(esc.get("magia_1") or "").strip()
                    if magia_1:
                        ef_mag["magia_adicional"] = {"nome": magia_1, "atributo": "Car"}
                    _injetar(
                        nome=f"Magias ({classe_orig or 'Duplo Feérico'})",
                        tipo="Origem",
                        descricao="Duplo Feérico: aprende 1 magia de 1º círculo e recebe +1 PM (sem somar atributo-chave nos PM).",
                        origem_hab=hab.nome,
                        efeitos=ef_mag,
                        nivel=1,
                    )
                else:
                    dados_h = None
                    for d in DADOS_HABILIDADES_CLASSE.values():
                        if isinstance(d, dict) and d.get("nome") == nome_hab and (not classe_orig or d.get("classe") == classe_orig):
                            dados_h = d
                            break
                    _injetar(
                        nome=nome_hab,
                        tipo="Origem",
                        descricao=(dados_h or {}).get("descricao", f"Habilidade de 1º nível copiada via Duplo Feérico ({classe_orig})."),
                        origem_hab=hab.nome,
                        efeitos=dict((dados_h or {}).get("efeitos") or {}),
                        nivel=1,
                    )

        # ── ATLAS: ASPIRANTE A HERÓI (+1 em 1 atributo — já processado por atributos.py via atributo_bonus_escolha) ──
        elif hab.nome == "Origem Regional: Aspirante a Herói":
            continue

        # ── ATLAS: FUTURA LENDA / COSMOPOLITA / ESTANDARTE VIVO ──
        elif hab.nome in (
            "Origem Regional: Futura Lenda",
            "Origem Regional: Cosmopolita",
            "Origem Regional: Estandarte Vivo",
        ):
            chave = (
                "poder_classe" if "Futura Lenda" in hab.nome
                else "poder_geral" if "Cosmopolita" in hab.nome
                else "poder_combate_tormenta"
            )
            nome_p = str(esc.get(chave) or "").strip()
            if nome_p:
                d_p = _buscar_poder_catalogo(nome_p)
                _injetar(
                    nome=(d_p or {}).get("nome", nome_p),
                    tipo=(d_p or {}).get("tipo", "Origem"),
                    descricao=(d_p or {}).get("descricao", f"Poder concedido por {hab.nome}."),
                    origem_hab=hab.nome,
                    efeitos=dict((d_p or {}).get("efeitos") or {}),
                )

        # ── ATLAS: ESTUDANTE DA ACADEMIA ──
        elif hab.nome == "Origem Regional: Estudante da Academia":
            magia_1 = str(esc.get("magia_1") or "").strip()
            if magia_1:
                ef["magia_adicional"] = {"nome": magia_1, "atributo": "Int"}
                hab.efeitos = ef

        # ── ATLAS: DE OUTRO MUNDO ──
        elif hab.nome == "Origem Regional: De Outro Mundo":
            magia_1 = str(esc.get("magia_1") or "").strip()
            attr_full = str(esc.get("atributo") or "inteligencia").strip().lower()
            attr_short = _ATTR_FULL_TO_SHORT.get(attr_full, "Int")
            if magia_1:
                ef["magia_adicional"] = {"nome": magia_1, "atributo": attr_short}
                if esc.get("formato") == "tecnologia":
                    ef["limite_pm_magia_extra"] = 2
                hab.efeitos = ef

        # ── ATLAS: TAMALU ──
        elif hab.nome == "Origem Regional: Tamalu":
            tat = str(esc.get("tatuagem") or "").strip()
            ef.pop("defesa_bonus", None)
            ef.pop("resistencia_magia_bonus", None)
            ef.pop("magia_adicional", None)
            if tat == "defesa":
                ef["defesa_bonus"] = 1
            elif tat == "resistencia_magia":
                ef["resistencia_magia_bonus"] = 2
            elif tat == "magia_1":
                magia_1 = str(esc.get("magia_1") or "").strip()
                if magia_1:
                    ef["magia_adicional"] = {"nome": magia_1, "atributo": "Sab"}
            hab.efeitos = ef

        # ── AMEAÇAS: HERANÇA DRACÔNICA (KALLYANACH) ──
        elif hab.nome == "Herança Dracônica":
            elem = str(esc.get("elemento") or "").strip().lower()
            if elem:
                ef["rd_tipo"] = {elem: 10 if tem_escamas_elementais else 5}
                hab.efeitos = ef

        # ── AMEAÇAS: BÊNÇÃO DE KALLYADRANOCH (KALLYANACH) ──
        elif hab.nome == "Bênção de Kallyadranoch":
            mapa_bencaos = {
                "Armamento Kallyanach": {
                    "descricao": "Arma natural 1d6, crítico x2 (cauda, chifres ou mordida); 1 PM ataque extra.",
                    "efeitos": {"arma_natural": {"nome": "Armamento Kallyanach", "dano": "1d6", "critico": "x2", "tipo": "Perfuração"}, "ataque_extra_pm": 1},
                },
                "Asas Dracônicas": {
                    "descricao": "Pode gastar 1 PM/rodada para voar 9m (fica vulnerável enquanto voa).",
                    "efeitos": {"deslocamento_voo": 9},
                },
                "Escamas Elementais": {
                    "descricao": "+2 na Defesa e aumenta a RD da Herança Dracônica para 10.",
                    "efeitos": {"defesa_bonus": 2},
                },
                "Prática Arcana": {
                    "descricao": "Pode lançar uma magia arcana de 1º círculo do elemento da Herança Dracônica (Int; -1 PM se aprender de novo).",
                    "efeitos": {},
                },
                "Sentidos Dracônicos": {
                    "descricao": "Você recebe faro e visão no escuro.",
                    "efeitos": {"faro": True, "visao_escuro": True},
                },
                "Sopro de Dragão": {
                    "descricao": "Ação padrão, 1 PM: cone 6m causando 1d12 do elemento da Herança Dracônica (Ref CD Con metade).",
                    "efeitos": {},
                },
            }
            for k in ("bencao_1", "bencao_2"):
                b = str(esc.get(k) or "").strip()
                if b in mapa_bencaos:
                    _injetar(b, "Racial", mapa_bencaos[b]["descricao"], hab.nome, mapa_bencaos[b]["efeitos"])

        # ── AMEAÇAS: TALENTOS DO BANDO (KOBOLDS) ──
        elif hab.nome == "Talentos do Bando":
            mapa_talentos = {
                "Ex-Familiar": {"descricao": "+2 PM e benefícios de um familiar arcano básico.", "efeitos": {"pm_max_ini": 2}},
                "Organizadinhos": {"descricao": "Usa Destreza para limite de carga e +1 item vestido adicional.", "efeitos": {"carga_atributo": "des"}},
            }
            for k in ("talento_1", "talento_2"):
                t = str(esc.get(k) or "").strip()
                if t:
                    meta = mapa_talentos.get(t, {"descricao": f"Talento do Bando: {t}.", "efeitos": {}})
                    _injetar(t, "Racial", meta["descricao"], hab.nome, meta["efeitos"])

        # ── AMEAÇAS: MARAVILHA MECÂNICA (MASHIN) ──
        elif hab.nome == "Maravilha Mecânica":
            m = str(esc.get("maravilha_1") or "").strip()
            if m:
                _injetar(m, "Racial", f"Maravilha Mecânica do Mashin: {m}.", hab.nome, {})

        # ── AMEAÇAS: TERROR VIVO (KAIJIN) ──
        elif hab.nome == "Terror Vivo":
            pt = str(esc.get("poder_tormenta") or "").strip()
            if pt:
                d_pt = _buscar_poder_catalogo(pt)
                ef_pt = dict((d_pt or {}).get("efeitos") or {})
                ef_pt["conta_poder_tormenta_sem_perda_car"] = True
                _injetar(
                    nome=(d_pt or {}).get("nome", pt),
                    tipo="Poder da Tormenta",
                    descricao=(d_pt or {}).get("descricao", "Poder da Tormenta concedido por Terror Vivo (sem perda de Carisma)."),
                    origem_hab=hab.nome,
                    efeitos=ef_pt,
                )

        # ── AMEAÇAS: SAPIÊNCIA (MOREAU CORUJA) ──
        elif hab.nome == "Sapiência":
            magia_1 = str(esc.get("magia_1") or "").strip()
            if magia_1:
                ef["magia_adicional"] = {"nome": magia_1, "atributo": "Sab"}
                ef["reducao_custo_magia"] = {"nomes": [magia_1], "valor": 1}
                hab.efeitos = ef

        # ── AMEAÇAS: ESPERTEZA VULPINA (MOREAU RAPOSA) ──
        elif hab.nome == "Esperteza Vulpina":
            bp = {}
            for k in ("pericia_bonus_1", "pericia_bonus_2"):
                p = str(esc.get(k) or "").strip()
                if p:
                    bp[p] = 2
            if bp:
                ef["bonus_pericia"] = bp
                hab.efeitos = ef

        # ── AMEAÇAS: PAPEL TRIBAL (CERATOPS) ──
        elif hab.nome == "Papel Tribal":
            p1 = str(esc.get("pericia_1") or "").strip()
            if p1:
                ef["pericia_treino"] = [p1]
                hab.efeitos = ef

    if extras:
        ficha.habilidades.extend(extras)
