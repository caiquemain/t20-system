from .inventario import catalogo_do_item, calcular_penalidade_armadura
import math
import logging
from typing import Optional, Dict, Any, List
from ..models import Personagem, StatCalculado, FonteBonus
from ..dados_classes import DADOS_CLASSES
from .utils import calcular_modificador
from ..dados_progressao_magias import MAPA_SUBCLASSE_PARA_CLASSE

logger = logging.getLogger("RegrasT20")


def calcular_pv_pm(ficha: Personagem):
    logger.info("--- [4] Calculando PV e PM ---")
    if not ficha.classes:
        return

    c_prim = ficha.classes[0]
    dc = DADOS_CLASSES.get(c_prim.nome or "", {})
    if not dc:
        base = MAPA_SUBCLASSE_PARA_CLASSE.get(c_prim.nome or "")
        if base:
            dc = DADOS_CLASSES.get(base, {})

    mod_con = calcular_modificador(ficha.atributos.constituicao)
    mapa_attr = {
        'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
        'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
    }

    # Bônus de habilidades (coletados com rastreio de fonte)
    b_pv_ini = 0
    fontes_pv_ini = []
    fontes_pv_nivel = []
    fontes_pm_nivel = []
    fontes_pm_impar = []
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        nome = hab.nome or "Habilidade"
        v = efeitos.get("pv_max_ini", 0)
        if v:
            b_pv_ini += v
            fontes_pv_ini.append((nome, v))
        v = efeitos.get("pv_max_nivel", 0)
        if v:
            fontes_pv_nivel.append((nome, v))
        v = efeitos.get("pm_max_nivel", 0)
        if v:
            fontes_pm_nivel.append((nome, v))
        v = efeitos.get("pm_por_nivel_impar", 0)
        if v:
            fontes_pm_impar.append((nome, v))

    # ═══════════════════════════════════════════
    # 🛡️ PV - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    pv_calc = StatCalculado()
    pv_calc.adicionar_bonus(
        fonte=f"Classe: {c_prim.nome} (Inicial)",
        categoria="Classe",
        valor=dc.get("pv_inicial", 20)
    )
    if mod_con != 0:
        pv_calc.adicionar_bonus(fonte="Constituição", categoria="Atributo", valor=mod_con)
    for nome, v in fontes_pv_ini:
        pv_calc.adicionar_bonus(fonte=f"{nome} (PV inicial)", categoria="Poder", valor=v)

    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pv_calc.adicionar_bonus(
                fonte=f"Classe: {c.nome} ({n} nível{'is' if n > 1 else ''})",
                categoria="Classe",
                valor=n * (d.get("pv_nivel", 5) + mod_con)
            )

    # ═══════════════════════════════════════════
    # ✨ PM - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    pm_calc = StatCalculado()
    pm_calc.adicionar_bonus(
        fonte=f"Classe: {c_prim.nome} (Inicial)",
        categoria="Classe",
        valor=dc.get("pm_inicial", 5)
    )

    attr_pm = dc.get("pm_atributo")
    classe_nome = c_prim.nome or ""
    subclasse = (c_prim.subclasse or "").strip()

    if classe_nome == "Arcanista" and subclasse == "Feiticeiro":
        attr_pm = "car"
    elif classe_nome == "Arcanista" and subclasse in ("Bruxo", "Mago"):
        attr_pm = "int"

    if attr_pm:
        mod_pm = calcular_modificador(
            getattr(ficha.atributos, mapa_attr.get(str(attr_pm), 'inteligencia'))
        )
        if mod_pm != 0:
            pm_calc.adicionar_bonus(
                fonte=f"Atributo-chave: {str(attr_pm).upper()}",
                categoria="Atributo",
                valor=mod_pm
            )

    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pm_calc.adicionar_bonus(
                fonte=f"Classe: {c.nome} ({n} nível{'is' if n > 1 else ''})",
                categoria="Classe",
                valor=n * d.get("pm_nivel", 5)
            )

    # ═══════════════════════════════════════════
    # 🌟 BÔNUS GLOBAIS POR NÍVEL (Habilidades)
    # ═══════════════════════════════════════════
    nivel_total = sum(c.nivel for c in ficha.classes)
    
    for nome, v in fontes_pv_nivel:
        pv_calc.adicionar_bonus(
            fonte=f"{nome} (+{v} PV/nível)",
            categoria="Poder",
            valor=nivel_total * v
        )
    for nome, v in fontes_pm_nivel:
        pm_calc.adicionar_bonus(
            fonte=f"{nome} (+{v} PM/nível)",
            categoria="Poder",
            valor=nivel_total * v
        )
    impares = (nivel_total + 1) // 2
    for nome, v in fontes_pm_impar:
        pm_calc.adicionar_bonus(
            fonte=f"{nome} (+{v} PM/nível ímpar)",
            categoria="Poder",
            valor=impares * v
        )

    # Totem Espiritual (T20 p.42): soma SAB no total de PM
    mapa_attr_pm = {
        "for": "forca", "des": "destreza", "con": "constituicao",
        "int": "inteligencia", "sab": "sabedoria", "car": "carisma"
    }
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        attr_pm = efeitos.get("pm_soma_atributo")
        if attr_pm:
            full = mapa_attr_pm.get(str(attr_pm).lower()[:3], str(attr_pm))
            val = getattr(ficha.atributos, full, 0)
            if val != 0:
                pm_calc.adicionar_bonus(
                    fonte=f"Poder: {hab.nome} (PM)",
                    categoria="Poder",
                    valor=val
                )

        # Bravata Audaz (Bucaneiro, T20 p.47): se cumprida, +2 PM por nível de bucaneiro
        pm_bravata = efeitos.get("pm_por_nivel_se_cumprida")
        if pm_bravata and "bravata_audaz" in (getattr(ficha, "condicoes_ativas", None) or []):
            nivel_buc = next((int(c.nivel or 0) for c in (ficha.classes or []) if (c.nome or "") == "Bucaneiro"), nivel_total)
            if nivel_buc > 0:
                pm_calc.adicionar_bonus(
                    fonte=f"Poder: {hab.nome} (+{pm_bravata} PM/nível)",
                    categoria="Poder",
                    valor=int(pm_bravata) * nivel_buc
                )

    ficha.status.pm_calc = pm_calc
    ficha.status.pv_calc = pv_calc
    ficha.status.pv.maximo = pv_calc.total
    ficha.status.pm.maximo = pm_calc.total

    for stat in [ficha.status.pv, ficha.status.pm]:
        if stat.atual == 0 or stat.atual > stat.maximo:
            stat.atual = stat.maximo


def calcular_defesa_e_deslocamento(ficha: Personagem):
    logger.info("--- [5] Defesa/Deslocamento Detalhada ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)

    # ═══════════════════════════════════════════
    # 🛡️ DEFESA - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    defesa_calc = StatCalculado(base=10, total=10)

    # Destreza (só se não usar armadura pesada)
    usa_pesada = any(
        item.equipado and 
        (catalogo_do_item(item.nome) or {}).get("tipo_armadura") == "Pesada"
        for item in ficha.inventario.equipamentos
    )
    condicoes_ativas = getattr(ficha, "condicoes_ativas", None) or []
    tem_liberdade_mov = (not usa_pesada) and ("imovel" not in condicoes_ativas)
    nivel_total = int(ficha.cabecalho.nivel_total or 1)

    if mod_des != 0 and not usa_pesada:
        defesa_calc.adicionar_bonus(
            fonte="Destreza",
            categoria="Atributo",
            valor=mod_des
        )
    
    # Armadura vestida e escudo empunhado
    for item in ficha.inventario.equipamentos:
        if not item.equipado:
            continue
        cat = catalogo_do_item(item.nome)
        if not cat:
            continue
        tipo_arm = cat.get("tipo_armadura")
        if tipo_arm in ["Leve", "Pesada", "Escudo"]:
            bonus_def = cat.get("bonus_defesa", 0)
            if bonus_def > 0:
                defesa_calc.adicionar_bonus(
                    fonte=f"Equipamento: {item.nome}",
                    categoria="Equipamento",
                    valor=bonus_def
                )

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    # Pele de Aço substitui Pele de Ferro (T20 p.42)
    tem_pele_aco = any(
        (h.nome == "Pele de Aço") for h in ficha.habilidades
    )

    mapa_attr_def = {
        "for": "forca", "des": "destreza", "con": "constituicao",
        "int": "inteligencia", "sab": "sabedoria", "car": "carisma",
    }

    for hab in ficha.habilidades:
        efeitos = dict(hab.efeitos or {})
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        exige_lib = bool(efeitos.get("exige_liberdade_movimento"))

        val_fixo = efeitos.get("defesa_bonus", 0)
        if val_fixo != 0:
            # Pele de Ferro/Aço so valem sem armadura pesada (T20 p.42)
            aplicar_defesa = True
            if hab.nome == "Pele de Ferro" and (usa_pesada or tem_pele_aco):
                aplicar_defesa = False
            elif hab.nome == "Pele de Aço" and usa_pesada:
                aplicar_defesa = False
            elif exige_lib and not tem_liberdade_mov:
                aplicar_defesa = False

            if aplicar_defesa:
                val_final = int(val_fixo)
                escala = efeitos.get("escala_nivel")
                if isinstance(escala, dict) and escala.get("cada"):
                    inicio = int(escala.get("inicio", 1) or 1)
                    cada = int(escala.get("cada", 0) or 0)
                    passo = int(escala.get("bonus", 1) or 1)
                    classe_esc = escala.get("classe")
                    nivel_ref = nivel_total
                    if classe_esc:
                        nivel_ref = next(
                            (int(c.nivel or 0) for c in (ficha.classes or []) if (c.nome or "") == classe_esc),
                            nivel_total,
                        )
                    if nivel_ref >= inicio and cada > 0:
                        val_final = int(val_fixo) + ((nivel_ref - inicio) // cada) * passo
                defesa_calc.adicionar_bonus(
                    fonte=f"Poder: {hab.nome}",
                    categoria="Poder",
                    valor=val_final
                )

        # Soma de atributo na Defesa (ex.: Insolência do Bucaneiro = Car, limitado pelo nível)
        dsa = efeitos.get("defesa_soma_atributo")
        if dsa:
            if isinstance(dsa, dict):
                attr_cod = str(dsa.get("atributo", "")).lower()[:3]
                limite_nivel = bool(dsa.get("limite_por_nivel"))
                exige_lib_dsa = bool(dsa.get("exige_liberdade_movimento", exige_lib))
            else:
                attr_cod = str(dsa).lower()[:3]
                limite_nivel = False
                exige_lib_dsa = exige_lib
            if not exige_lib_dsa or tem_liberdade_mov:
                campo = mapa_attr_def.get(attr_cod)
                if campo:
                    mod_val = calcular_modificador(getattr(ficha.atributos, campo, 0))
                    if limite_nivel:
                        mod_val = min(mod_val, nivel_total)
                    if mod_val > 0:
                        defesa_calc.adicionar_bonus(
                            fonte=f"Poder: {hab.nome}",
                            categoria="Poder",
                            valor=mod_val
                        )

        # En Garde (Bucaneiro, T20 p.48): +2 Defesa quando postura ativa
        if (hab.nome or "") == "En Garde" and "en_garde" in condicoes_ativas:
            defesa_calc.adicionar_bonus(
                fonte="Poder: En Garde",
                categoria="Poder",
                valor=2
            )

        # Explorador (Caçador, T20 p.51): +Sab (mínimo +1) na Defesa no terreno escolhido
        if efeitos.get("explorador_terreno") and "terreno_explorador" in condicoes_ativas:
            mod_sab = max(1, calcular_modificador(ficha.atributos.sabedoria))
            defesa_calc.adicionar_bonus(
                fonte="Poder: Explorador (terreno)",
                categoria="Poder",
                valor=mod_sab
            )

        # Escaramuça / Escaramuça Superior (Caçador, T20 p.50): +2/+5 Defesa (sem armadura pesada)
        if "escaramuca" in condicoes_ativas and not usa_pesada:
            if efeitos.get("escaramuca_superior"):
                defesa_calc.adicionar_bonus(
                    fonte="Poder: Escaramuça Superior",
                    categoria="Poder",
                    valor=5
                )
            elif efeitos.get("escaramuca") and not any(
                (h.efeitos or {}).get("escaramuca_superior") or (h.nome or "") == "Escaramuça Superior"
                for h in ficha.habilidades
            ):
                defesa_calc.adicionar_bonus(
                    fonte="Poder: Escaramuça",
                    categoria="Poder",
                    valor=2
                )

        # Escudeiro (Cavaleiro, T20 p.54): sua armadura concede +1 na Defesa
        def_arm = efeitos.get("defesa_bonus_armadura", 0)
        if def_arm:
            usa_armadura = any(
                it.equipado and (catalogo_do_item(it.nome) or {}).get("tipo_armadura") in ("Leve", "Pesada")
                for it in ficha.inventario.equipamentos
            )
            if usa_armadura:
                defesa_calc.adicionar_bonus(
                    fonte=f"Poder: {hab.nome} (armadura)",
                    categoria="Poder",
                    valor=int(def_arm)
                )

        # Postura de Combate: Torre Inabalável (Cavaleiro, T20 p.54): soma Con na Defesa
        if (hab.nome or "") == "Postura de Combate: Torre Inabalável" and "torre_inabalavel" in condicoes_ativas:
            mod_con = calcular_modificador(ficha.atributos.constituicao)
            if mod_con > 0:
                defesa_calc.adicionar_bonus(
                    fonte="Postura: Torre Inabalável",
                    categoria="Poder",
                    valor=mod_con
                )

        # Postura de Combate: Muralha Intransponível (Cavaleiro, T20 p.54): +1 Defesa com escudo
        if (hab.nome or "") == "Postura de Combate: Muralha Intransponível" and "muralha_intransponivel" in condicoes_ativas:
            usa_escudo = any(
                it.equipado and (catalogo_do_item(it.nome) or {}).get("tipo_armadura") == "Escudo"
                for it in ficha.inventario.equipamentos
            )
            if usa_escudo:
                defesa_calc.adicionar_bonus(
                    fonte="Postura: Muralha Intransponível",
                    categoria="Poder",
                    valor=1
                )

        # Missa: Escudo Divino (Clérigo, T20 p.58): +1 Defesa (dobra com Mestre Celebrante)
        if (hab.nome or "") == "Missa: Escudo Divino" and "missa_escudo_divino" in condicoes_ativas:
            mult_missa = 2 if any(
                (h.efeitos or {}).get("mestre_celebrante") or (h.nome or "") == "Mestre Celebrante"
                for h in ficha.habilidades
            ) else 1
            defesa_calc.adicionar_bonus(
                fonte="Missa: Escudo Divino",
                categoria="Poder",
                valor=1 * mult_missa
            )

        # Couraceiro (Inventor, T20 p.69): usando armadura leve, usa Int no lugar de Des se for maior
        if efeitos.get("couraceiro_int_defesa") and not usa_pesada:
            usa_leve = any(
                it.equipado and (catalogo_do_item(it.nome) or {}).get("tipo_armadura") == "Leve"
                for it in ficha.inventario.equipamentos
            )
            if usa_leve:
                mod_int = calcular_modificador(ficha.atributos.inteligencia)
                if mod_int > mod_des:
                    defesa_calc.adicionar_bonus(
                        fonte="Poder: Couraceiro (Int no lugar de Des)",
                        categoria="Poder",
                        valor=mod_int - mod_des
                    )

        # Blindagem (Inventor, T20 p.69): usando armadura pesada, soma Int na Defesa
        if efeitos.get("blindagem_int_pesada") and usa_pesada:
            mod_int = calcular_modificador(ficha.atributos.inteligencia)
            if mod_int > 0:
                defesa_calc.adicionar_bonus(
                    fonte="Poder: Blindagem (Int)",
                    categoria="Poder",
                    valor=mod_int
                )

        if "defesa_bonus_tormenta" in efeitos:
            defesa_calc.adicionar_bonus(
                fonte=f"Poder: {hab.nome} (Tormenta x{qtd_tormenta})",
                categoria="Poder",
                valor=qtd_tormenta
            )

        if hab.nome == "Esquiva":
            defesa_calc.adicionar_bonus(
                fonte="Poder: Esquiva",
                categoria="Poder",
                valor=2
            )

    # Buffs ativos
    if hasattr(ficha.status, 'buffs'):
        for b in ficha.status.buffs:
            if b.atributo.lower() == "defesa":
                defesa_calc.adicionar_bonus(
                    fonte=f"Buff: {b.origem}",
                    categoria="Magia",
                    valor=b.valor
                )

    # ═══════════════════════════════════════════
    # 🏃 DESLOCAMENTO - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    desl_base = ficha.status.deslocamento  # Valor racial (setado em aplicar_bonus_atributos_raciais)
    deslocamento_calc = StatCalculado(base=desl_base, total=desl_base)
    deslocamento_calc.fontes.append(FonteBonus(
        fonte="Deslocamento Racial", categoria="Racial", valor=desl_base
    ))

    desl = desl_base
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        if "deslocamento" in efeitos:
            novo_val = int(efeitos["deslocamento"])
            desl = novo_val  # Sobrescrita
            deslocamento_calc.fontes.append(FonteBonus(
                fonte=f"Poder: {hab.nome}", categoria="Poder",
                valor=novo_val, descricao="Define o deslocamento"
            ))
            deslocamento_calc.total = novo_val
        if "deslocamento_bonus" in efeitos:
            bonus_desl = int(efeitos["deslocamento_bonus"])
            desl += bonus_desl
            deslocamento_calc.adicionar_bonus(
                fonte=f"Poder: {hab.nome}",
                categoria="Poder",
                valor=bonus_desl
            )

    # Posturas de Cavaleiro que alteram deslocamento
    if "torre_inabalavel" in condicoes_ativas and any(
        (h.nome or "") == "Postura de Combate: Torre Inabalável" for h in ficha.habilidades
    ):
        desl = 0
        deslocamento_calc.total = 0
    elif "muralha_intransponivel" in condicoes_ativas and any(
        (h.nome or "") == "Postura de Combate: Muralha Intransponível" for h in ficha.habilidades
    ):
        desl = 3
        deslocamento_calc.total = 3

    # Armadura pesada vestida: -3m deslocamento (respeita imunidade)
    if usa_pesada:
        # Verificar imunidade
        tem_imunidade = any(
            "imunidade_penalidade_mov" in (h.efeitos or {})
            for h in ficha.habilidades
        )
        if not tem_imunidade:
            deslocamento_calc.total -= 3
            deslocamento_calc.fontes.append(FonteBonus(
                fonte="Armadura Pesada", categoria="Equipamento",
                valor=-3, descricao="Reduz deslocamento em 3m"
            ))
    
    # Sobrecarga: -3m deslocamento (respeita imunidade)
    if ficha.inventario.sobrecargado:
        tem_imunidade = any(
            "imunidade_penalidade_mov" in (h.efeitos or {})
            for h in ficha.habilidades
        )
        if not tem_imunidade:
            deslocamento_calc.total -= 3
            deslocamento_calc.fontes.append(FonteBonus(
                fonte="Sobrecarga", categoria="Inventário",
                valor=-3, descricao="Reduz deslocamento em 3m"
            ))
    
    if hasattr(ficha.status, 'buffs'):
        for b in ficha.status.buffs:
            if b.atributo.lower() == "deslocamento":
                desl += b.valor
                deslocamento_calc.adicionar_bonus(
                    fonte=f"Buff: {b.origem}", categoria="Magia", valor=b.valor
                )

    # 💾 SALVAR
    ficha.status.deslocamento_calc = deslocamento_calc
    ficha.status.defesa_calc = defesa_calc
    ficha.status.defesa.total = defesa_calc.total
    ficha.status.deslocamento = desl

    # Mantém o dicionário de detalhes antigo (compatibilidade)
    detalhes_defesa = {"Base": 10}
    if mod_des != 0:
        detalhes_defesa["Destreza"] = mod_des
    for fonte in defesa_calc.fontes:
        if fonte.fonte != "Destreza":
            detalhes_defesa[fonte.fonte] = fonte.valor
    try:
        setattr(ficha.status.defesa, "detalhes", detalhes_defesa)
    except AttributeError:
        pass
    # ═══════════════════════════════════════════
    # 💾 SALVAR NA FICHA
    # ═══════════════════════════════════════════
    ficha.status.defesa_calc = defesa_calc
    
    # Sincroniza com campos antigos (compatibilidade frontend)
    ficha.status.defesa.total = defesa_calc.total
    ficha.status.deslocamento = desl

    # Mantém o dicionário de detalhes antigo para não quebrar nada
    detalhes_defesa = {"Base": 10}
    if mod_des != 0:
        detalhes_defesa["Destreza"] = mod_des
    for fonte in defesa_calc.fontes:
        if fonte.fonte not in ["Destreza"]:
            detalhes_defesa[fonte.fonte] = fonte.valor
    try:
        setattr(ficha.status.defesa, "detalhes", detalhes_defesa)
    except AttributeError:
        pass


def calcular_furia(ficha: Personagem) -> Optional[Dict[str, int]]:
    """Calcula o bônus/custo ativo de Fúria do Bárbaro.

    Livro (T20 p.41):
        Fúria (1º): 2 PM para +2 ataque/dano corpo a corpo.
        A cada 5 níveis, pode gastar +1 PM para aumentar o bônus em +1.
        Fúria Titânica (20º): o bônus é dobrado.

    Retorna None se o personagem não tem a habilidade Fúria.
    """
    furia = next(
        (h for h in ficha.habilidades if (h.nome or "") == "Fúria"), None)
    if furia is None:
        return None
    efeitos = furia.efeitos or {}
    ativavel = efeitos.get("acao_ativavel") or efeitos.get("habilidade_ativavel")
    if not isinstance(ativavel, dict):
        return None

    bonus_base = int(ativavel.get("ataque_bonus", 0) or 0)
    custo_base = int(ativavel.get("custo_pm", 0) or 0)
    escala = ativavel.get("escala_nivel") or {}
    cada = int(escala.get("cada", 0) or 0)
    passo = int(escala.get("bonus", 0) or 0)

    # Nível de classe do Bárbaro (habilidade é de classe)
    nivel_classe = 1
    if ficha.classes:
        c = ficha.classes[0]
        if (c.nome or "") == "Bárbaro":
            nivel_classe = int(c.nivel or 1)

    if cada > 0 and nivel_classe >= 1:
        passos = (nivel_classe - 1) // cada
        bonus = bonus_base + passos * passo
        custo = custo_base + passos * passo
    else:
        bonus = bonus_base
        custo = custo_base

    # Fúria Titânica (20º): dobra o bônus
    if any((h.nome or "") == "Fúria Titânica" for h in ficha.habilidades):
        bonus *= 2

    aplica_arremesso = any(
        (h.efeitos or {}).get("furia_arremesso") or (h.nome or "") == "Fúria da Savana"
        for h in ficha.habilidades
    )

    return {"bonus": bonus, "custo": custo, "aplica_arremesso": aplica_arremesso}


def calcular_inspiracao(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula os parâmetros ativos de Inspiração do Bardo (T20 JdA, p. 43-44).

    Regras oficiais:
        - Nível 1: ação padrão, 2 PM, alcance curto, cena, +1 em testes de perícia.
        - A cada 4 níveis (5º, 9º, 13º, 17º): +2 PM para +1 bônus (+1..+5, 2..10 PM).
        - Inspiração Marcial: aplica o bônus também em rolagens de dano.
        - Arte Mágica: sob Inspiração, CD das habilidades de bardo +2.
        - Artista Completo (20º): ação livre; sob Inspiração, habilidades de bardo
          (incluindo magias) custam metade dos PM (após aprimoramentos e reduções).
        - Golpe Elemental: sob Inspiração, 1 PM (+1 PM a cada 4 níveis) para +1d6/PM.

    Retorna None se o personagem não possui a habilidade Inspiração.
    """
    insp = next(
        (h for h in ficha.habilidades if (h.nome or "") == "Inspiração"), None
    )
    if insp is None:
        return None
    efeitos = insp.efeitos or {}
    ativavel = efeitos.get("acao_ativavel") or efeitos.get("habilidade_ativavel")
    if not isinstance(ativavel, dict):
        return None

    bonus_base = int(ativavel.get("bonus_pericias_aliados", 1) or 1)
    custo_base = int(ativavel.get("custo_pm", 2) or 2)
    escala = ativavel.get("escala_nivel") or {}
    if isinstance(escala, dict):
        cada = int(escala.get("cada", 4) or 4)
        passo_bonus = int(escala.get("bonus", 1) or 1)
        passo_custo = int(escala.get("custo_pm_extra", 2) or 2)
    else:
        cada = int(escala or 4)
        passo_bonus = 1
        passo_custo = 2

    # Nível de classe do Bardo (suporta multiclasse)
    nivel_classe = 1
    for c in ficha.classes or []:
        if (c.nome or "") == "Bardo":
            nivel_classe = int(c.nivel or 1)
            break

    passos = (nivel_classe - 1) // cada if cada > 0 and nivel_classe >= 1 else 0
    bonus = bonus_base + passos * passo_bonus
    custo = custo_base + passos * passo_custo

    artista_completo = any(
        (h.efeitos or {}).get("artista_completo") or (h.nome or "") == "Artista Completo"
        for h in ficha.habilidades
    )
    aplica_dano = any(
        (h.efeitos or {}).get("inspiracao_aplica_dano") or (h.nome or "") == "Inspiração Marcial"
        for h in ficha.habilidades
    )
    cd_bonus = 0
    for h in ficha.habilidades:
        v = (h.efeitos or {}).get("cd_bardo_inspiracao")
        if v:
            cd_bonus += int(v)
        elif (h.nome or "") == "Arte Mágica":
            cd_bonus += 2

    tem_golpe_elemental = any(
        (h.nome or "") == "Golpe Elemental" for h in ficha.habilidades
    )
    golpe_elemental_max_dados = (1 + (nivel_classe - 1) // 4) if tem_golpe_elemental else 0

    condicoes = getattr(ficha, "condicoes_ativas", None) or []
    ativa = "inspiracao" in condicoes

    return {
        "bonus": bonus,
        "custo": custo,
        "acao": "Livre" if artista_completo else "Padrão",
        "alcance": "Curto",
        "duracao": "Cena",
        "ativa": ativa,
        "aplica_dano": aplica_dano,
        "cd_bonus": cd_bonus,
        "reduz_custo_metade": artista_completo,
        "golpe_elemental_max_dados": golpe_elemental_max_dados,
    }


def calcular_marca_presa(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula os parâmetros de Marca da Presa do Caçador (T20 JdA, p. 49-51).

    Tabela 1-9:
        1º-4º: +1d4 (1 PM)
        5º-8º: +1d8 (2 PM)
        9º-12º: +1d12 (3 PM)
        13º-16º: +2d8 (4 PM)
        17º-20º: +2d10 (5 PM)
    """
    marca = next(
        (h for h in ficha.habilidades if (h.nome or "") == "Marca da Presa"), None
    )
    if marca is None:
        return None

    nivel_classe = 1
    for c in ficha.classes or []:
        if (c.nome or "") == "Caçador":
            nivel_classe = int(c.nivel or 1)
            break

    progressao = ["1d4", "1d8", "1d12", "2d8", "2d10"]
    degrau = min(len(progressao) - 1, max(0, (nivel_classe - 1) // 4))
    dado = progressao[degrau]
    custo_max = degrau + 1

    mestre = any(
        (h.efeitos or {}).get("mestre_cacador") or (h.nome or "") == "Mestre Caçador"
        for h in ficha.habilidades
    )
    olho_falcao = any(
        (h.efeitos or {}).get("marca_presa_alcance") == "Longo" or (h.nome or "") == "Olho do Falcão"
        for h in ficha.habilidades
    )
    tem_espreitar = any(
        (h.efeitos or {}).get("espreitar_marca_presa") or (h.nome or "") == "Espreitar"
        for h in ficha.habilidades
    )
    ponto_fraco_margem = 2 if any(
        (h.efeitos or {}).get("ponto_fraco_margem") or (h.nome or "") == "Ponto Fraco"
        for h in ficha.habilidades
    ) else 0

    return {
        "dado": dado,
        "custo_base": 1,
        "custo_max": custo_max,
        "acao": "Livre" if mestre else "Movimento",
        "alcance": "Longo" if olho_falcao else "Curto",
        "duracao": "Cena",
        "espreitar_bonus_max": custo_max if tem_espreitar else 0,
        "ponto_fraco_margem": ponto_fraco_margem,
        "mestre_cacador": mestre,
    }


def calcular_cavaleiro(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula parâmetros de Baluarte, Duelo, Armadura da Honra e Estandarte (T20 JdA p.52-55)."""
    baluarte_hab = next(
        (h for h in ficha.habilidades if (h.nome or "") == "Baluarte"), None
    )
    if baluarte_hab is None:
        return None

    nivel_classe = 1
    for c in ficha.classes or []:
        if (c.nome or "") == "Cavaleiro":
            nivel_classe = int(c.nivel or 1)
            break

    # Baluarte: +2 (1º), +4 (5º), +6 (9º), +8 (13º), +10 (17º); custo 1..5 PM
    passos_bal = min(4, max(0, (nivel_classe - 1) // 4))
    baluarte = {
        "bonus": 2 + passos_bal * 2,
        "custo": 1 + passos_bal,
        "aliados_adjacentes": nivel_classe >= 7,
        "aliados_alcance_curto": nivel_classe >= 15,
    }

    # Duelo (2º): +2 (2º), +3 (7º), +4 (12º), +5 (17º); custo 2..5 PM
    duelo = None
    if any((h.nome or "") == "Duelo" for h in ficha.habilidades) and nivel_classe >= 2:
        passos_duelo = min(3, max(0, (nivel_classe - 2) // 5))
        duelo = {
            "bonus": 2 + passos_duelo,
            "custo": 2 + passos_duelo,
        }

    mod_car = calcular_modificador(ficha.atributos.carisma)
    nivel_total = int(ficha.cabecalho.nivel_total or 1)
    armadura_honra = (
        max(0, nivel_total + mod_car)
        if any((h.efeitos or {}).get("armadura_honra_pv_temp") or (h.nome or "") == "Armadura da Honra" for h in ficha.habilidades)
        else 0
    )
    estandarte = (
        max(1, mod_car)
        if any((h.efeitos or {}).get("estandarte_pm_temp") or (h.nome or "") == "Estandarte" for h in ficha.habilidades)
        else 0
    )

    return {
        "baluarte": baluarte,
        "duelo": duelo,
        "armadura_honra_pv_temp": armadura_honra,
        "estandarte_pm_temp": estandarte,
    }


def calcular_clerigo(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula parâmetros de Missas, Mestre Celebrante e Canalizar Energia do Clérigo (T20 JdA p.56-58)."""
    eh_clerigo = any((c.nome or "") == "Clérigo" for c in (ficha.classes or []))
    if not eh_clerigo:
        return None

    mod_sab = calcular_modificador(ficha.atributos.sabedoria)
    nivel_total = int(ficha.cabecalho.nivel_total or 1)
    mestre_cel = any(
        (h.efeitos or {}).get("mestre_celebrante") or (h.nome or "") == "Mestre Celebrante"
        for h in ficha.habilidades
    )
    mult_benef = 2 if mestre_cel else 1
    mult_pessoas = 10 if mestre_cel else 1

    tem_canalizar = any(
        "Canalizar Energia" in (h.nome or "") for h in ficha.habilidades
    )
    canalizar_amplo = any(
        (h.efeitos or {}).get("canalizar_alcance_medio") or (h.nome or "") == "Canalizar Amplo"
        for h in ficha.habilidades
    )

    return {
        "canalizar_alcance": ("Médio" if canalizar_amplo else "Curto") if tem_canalizar else None,
        "missa_pessoas": max(1, 1 + mod_sab) * mult_pessoas,
        "missa_multiplicador": mult_benef,
        "missa_bencao_pv_temp": max(0, nivel_total + mod_sab) * mult_benef,
        "missa_elevacao_pm_temp": max(0, mod_sab) * mult_benef,
        "missa_escudo_bonus": 1 * mult_benef,
        "missa_chamado_bonus": 1 * mult_benef,
    }


def calcular_ataque_especial(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula parâmetros de Ataque Especial, Romper Resistências e Campeão (T20 JdA p.64-66).

    Tabela 1-13:
        1º-4º: +4 (1 PM)
        5º-8º: +8 (2 PM)
        9º-12º: +12 (3 PM)
        13º-16º: +16 (4 PM)
        17º-20º: +20 (5 PM)
    """
    ae = next(
        (h for h in ficha.habilidades if (h.nome or "") == "Ataque Especial"), None
    )
    if ae is None:
        return None

    nivel_classe = 1
    for c in ficha.classes or []:
        if (c.nome or "") == "Guerreiro":
            nivel_classe = int(c.nivel or 1)
            break

    passos = min(4, max(0, (nivel_classe - 1) // 4))
    bonus = 4 + passos * 4
    custo = 1 + passos

    romper = any(
        (h.efeitos or {}).get("romper_resistencias_rd") or (h.nome or "") == "Romper Resistências"
        for h in ficha.habilidades
    )
    campeao = any(
        (h.efeitos or {}).get("campeao") or (h.nome or "") == "Campeão"
        for h in ficha.habilidades
    )

    return {
        "bonus": bonus,
        "custo": custo,
        "romper_resistencias": romper,
        "campeao_recupera_metade": campeao,
        "campeao_passo_dano": campeao,
    }


def calcular_inventor(ficha: Personagem) -> Optional[Dict[str, Any]]:
    """Calcula parâmetros do Inventor (T20 JdA p.67-71): melhorias, item mágico, engenhocas e fórmulas."""
    nivel_inv = 0
    for c in ficha.classes or []:
        if (c.nome or "") == "Inventor":
            nivel_inv = int(c.nivel or 0)
            break
    if nivel_inv <= 0:
        return None

    # Fabricar Item Superior: 1 (2º), 2 (5º), 3 (8º), 4 (11º)
    melhorias_max = 0
    for nv_req, qtd in ((2, 1), (5, 2), (8, 3), (11, 4)):
        if nivel_inv >= nv_req:
            melhorias_max = qtd

    # Fabricar Item Mágico: Menor (9º), Médio (13º), Maior (17º)
    item_magico = None
    if nivel_inv >= 17:
        item_magico = "Maior"
    elif nivel_inv >= 13:
        item_magico = "Médio"
    elif nivel_inv >= 9:
        item_magico = "Menor"

    mod_int = calcular_modificador(ficha.atributos.inteligencia)

    # Engenhoqueiro: limite = Int (+3 com Manutenção Eficiente); círculo = 1 (1º), 2 (6º), 3 (10º), 4 (14º), 5 (18º)
    tem_eng = any((h.efeitos or {}).get("fabricar_engenhoca") or (h.nome or "") == "Engenhoqueiro" for h in ficha.habilidades)
    limite_eng = 0
    circulo_eng = 0
    if tem_eng:
        bonus_eng = sum(int((h.efeitos or {}).get("limite_engenhocas_bonus", 0) or 0) for h in ficha.habilidades)
        limite_eng = max(0, mod_int) + bonus_eng
        circulo_eng = 1
        for nv_req, circ in ((6, 2), (10, 3), (14, 4), (18, 5)):
            if nivel_inv >= nv_req:
                circulo_eng = circ

    # Alquimista Iniciado / Mestre Alquimista: fórmulas = 3 + (nivel - 1) + 3 * Conhecimento de Fórmulas
    tem_alq = any((h.efeitos or {}).get("fabricar_pocao") or (h.nome or "") == "Alquimista Iniciado" for h in ficha.habilidades)
    mestre_alq = any((h.efeitos or {}).get("mestre_alquimista") or (h.nome or "") == "Mestre Alquimista" for h in ficha.habilidades)
    circulo_pocao = 0
    formulas_total = 0
    if tem_alq:
        circulo_pocao = 2 if nivel_inv >= 6 else 1
        if mestre_alq:
            for nv_req, circ in ((10, 3), (14, 4), (18, 5)):
                if nivel_inv >= nv_req:
                    circulo_pocao = circ
        extras = sum(int((h.efeitos or {}).get("formulas_adicionais", 0) or 0) for h in ficha.habilidades)
        formulas_total = 3 + max(0, nivel_inv - 1) + extras

    return {
        "melhorias_max": melhorias_max,
        "item_magico": item_magico,
        "limite_engenhocas": limite_eng,
        "circulo_engenhoca": circulo_eng,
        "circulo_pocao": circulo_pocao,
        "formulas_total": formulas_total,
    }


def _nivel_inicio_da_habilidade(hab) -> int:
    """Extrai o nível de início de uma habilidade de classe a partir da
    fonte. Ex.: 'Bárbaro (5)' -> 5; 'Bárbaro' -> 1."""
    fonte = hab.fonte or ""
    if "(" in fonte and fonte.endswith(")"):
        try:
            return int(fonte.rsplit("(", 1)[1].rstrip(")"))
        except ValueError:
            pass
    return 1


def calcular_reducoes_dano(ficha: Personagem):
    logger.info("--- [7] Calculando RD e Resistências ---")
    lista_rd = []
    bonus_dano_geral = 0
    rd_armadura_pesada_total = 0
    nivel_total = int(ficha.cabecalho.nivel_total or 1)
    ficha.status.resistencia_magia = 0  # reset idempotente

    usa_pesada_rd = any(
        it.equipado and (catalogo_do_item(it.nome) or {}).get("tipo_armadura") == "Pesada"
        for it in ficha.inventario.equipamentos
    )

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = dict(hab.efeitos or {})
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        rmag = efeitos.get("resistencia_magia_bonus", 0)
        if rmag:
            ficha.status.resistencia_magia += int(rmag)

        if "resistencia_rd" in efeitos:
            for t, v in efeitos["resistencia_rd"].items():
                lista_rd.append(f"{t} {v}")

        rd_esc = efeitos.get("resistencia_rd_escolha")
        if isinstance(rd_esc, str) and rd_esc:
            lista_rd.append(f"{rd_esc} 10")

        if "rd_escalavel_tormenta" in efeitos:
            dados = efeitos["rd_escalavel_tormenta"]
            elementos = dados.get("elementos", [])
            base = dados.get("base", 0)
            bonus_por_poder = dados.get("por_poder", 0)
            qtd_outros = max(0, qtd_tormenta - 1)
            total = base + (qtd_outros * bonus_por_poder)
            for elem in elementos:
                lista_rd.append(f"{elem} {total}")

        # ── RD FIXA ESCALÁVEL (Bárbaro, Cavaleiro, Lutador) ──
        # Ex.: {"rd_fixa": 2, "escala_nivel": {"cada": 3, "bonus": 2}}
        # Bárbaro nv 5 = RD 2; nv 8 = RD 4; nv 17 = RD 10.
        if "rd_fixa" in efeitos:
            rd_base = int(efeitos["rd_fixa"])
            escala = efeitos.get("escala_nivel") or {}
            cada = int(escala.get("cada", 0) or 0)
            passo = int(escala.get("bonus", 0) or 0)
            rd_max = efeitos.get("rd_max")
            nivel_inicio = _nivel_inicio_da_habilidade(hab)
            if nivel_total >= nivel_inicio and cada > 0:
                extra = (nivel_total - nivel_inicio) // cada
                rd_total = rd_base + extra * passo
                if isinstance(rd_max, (int, float)) and rd_total > rd_max:
                    rd_total = int(rd_max)
                lista_rd.append(f"geral {rd_total}")

        # ── RD DE ARMADURA PESADA ACUMULATIVA (Bastião + Especialização em Armadura) ──
        if usa_pesada_rd:
            if efeitos.get("rd_armadura_pesada"):
                rd_armadura_pesada_total += int(efeitos["rd_armadura_pesada"])
            if (hab.nome or "") == "Caminho do Cavaleiro":
                escolha_cam = (hab.escolhas_aplicadas or {}).get("caminho") or (
                    ficha.classes[0].subclasse if ficha.classes else ""
                )
                if str(escolha_cam).strip() == "Bastião":
                    rd_armadura_pesada_total += 5

        # ── BÔNUS DE DANO GERAL (Instinto Selvagem do Bárbaro, Escudeiro do Cavaleiro) ──
        if "dano_bonus" in efeitos:
            dano_base = int(efeitos["dano_bonus"])
            escala = efeitos.get("escala_nivel") or {}
            cada = int(escala.get("cada", 0) or 0)
            passo = int(escala.get("bonus", 0) or 0)
            nivel_inicio = _nivel_inicio_da_habilidade(hab)
            if cada > 0:
                if nivel_total >= nivel_inicio:
                    extra = (nivel_total - nivel_inicio) // cada
                    bonus_dano_geral += dano_base + extra * passo
            else:
                bonus_dano_geral += dano_base

    if rd_armadura_pesada_total > 0:
        lista_rd.append(f"geral {rd_armadura_pesada_total}")

    # Append (nao overwrite): preserva RD vinda de outras fontes (linhagens)
    ficha.status.rd = sorted(set(ficha.status.rd + lista_rd))
    if bonus_dano_geral > 0:
        ficha.combate.bonus_dano_geral = bonus_dano_geral


def calcular_proficiencias_e_extras(ficha: Personagem):
    logger.info("--- [6] Proficiências e Extras ---")

    proficiencias = set()
    imunidades = set()
    sentidos = set()

    if ficha.classes:
        for c in ficha.classes:
            dc = DADOS_CLASSES.get(c.nome or "", {})
            lista_prof = dc.get("proficiencias", []) or dc.get(
                "proficiencias_iniciais", [])
            for p in lista_prof:
                proficiencias.add(p)

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        keys_prof = [
            "proficiencia_add", "proficiencia_simples", "proficiencia_marcial",
            "proficiencia_exotica", "proficiencia_armadura", "proficiencia_escudo",
            "proficiencia_adicional"
        ]

        for k in keys_prof:
            if k in efeitos:
                val = efeitos[k]
                if isinstance(val, list):
                    proficiencias.update([str(v) for v in val])
                elif isinstance(val, str):
                    proficiencias.add(val)
                elif val is True:
                    nome_legivel = k.replace("proficiencia_", "").capitalize()
                    if nome_legivel == "Simples":
                        nome_legivel = "Armas Simples"
                    if nome_legivel == "Marcial":
                        nome_legivel = "Armas Marciais"
                    proficiencias.add(nome_legivel)

        if "imunidade" in efeitos:
            val = efeitos["imunidade"]
            if isinstance(val, list):
                imunidades.update(val)
            else:
                imunidades.add(str(val))
        # Golem: espírito elemental escolhido vira imunidade a dano
        val_imn_elem = efeitos.get("imunidade_dano_escolha")
        if isinstance(val_imn_elem, str) and val_imn_elem:
            imunidades.add(f"Imune a {val_imn_elem}")

        if "imunidade_penalidade_mov" in efeitos:
            imunidades.add("Deslocamento (Armadura/Carga)")

        if "sentido" in efeitos:
            val = efeitos["sentido"]
            if isinstance(val, list):
                sentidos.update(val)
            else:
                sentidos.add(str(val))

        if efeitos.get("visao_escuro"):
            sentidos.add("Visão no Escuro")

        if efeitos.get("visao_penumbra"):
            sentidos.add("Visão na Penumbra")

        if efeitos.get("faro"):
            sentidos.add("Faro")

    # ── VULNERABILIDADES (Kliren/Trog) ──
    vulnerabilidades = []
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        vuln = efeitos.get("vulnerabilidade_dado")
        if vuln and isinstance(vuln, dict):
            tipo = vuln.get("tipo", "")
            valor = vuln.get("valor", 1)
            vulnerabilidades.append(f"{tipo.capitalize()} +{valor}/dado")

    # Append (nao overwrite): preserva valores de outras fontes (ex.: familiares)
    ficha.status.proficiencias = sorted(set(ficha.status.proficiencias + list(proficiencias)))
    ficha.status.imunidades = sorted(set(ficha.status.imunidades + list(imunidades)))
    ficha.status.sentidos = sorted(set(ficha.status.sentidos + list(sentidos)))
    ficha.status.vulnerabilidades = sorted(list(set(vulnerabilidades)))