import math
import logging
from ..models import Personagem, StatCalculado, FonteBonus
from ..dados_classes import DADOS_CLASSES
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")


def calcular_pv_pm(ficha: Personagem):
    logger.info("--- [4] Calculando PV e PM ---")
    if not ficha.classes:
        return

    c_prim = ficha.classes[0]
    dc = DADOS_CLASSES.get(c_prim.nome or "", {})

    mod_con = calcular_modificador(ficha.atributos.constituicao)
    attr_pm = dc.get("pm_atributo", "int")
    mapa_attr = {
        'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
        'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
    }
    mod_pm = calcular_modificador(getattr(ficha.atributos, mapa_attr.get(attr_pm, 'inteligencia')))

    # ═══════════════════════════════════════════
    # 🛡️ PV - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    pv_calc = StatCalculado()
    
    # Base da classe
    pv_inicial_classe = dc.get("pv_inicial", 20)
    pv_calc.adicionar_bonus(
        fonte=f"Classe: {c_prim.nome} (Inicial)",
        categoria="Classe",
        valor=pv_inicial_classe
    )
    
    # Constituição
    if mod_con != 0:
        pv_calc.adicionar_bonus(
            fonte="Constituição",
            categoria="Atributo",
            valor=mod_con
        )

    # Bônus de habilidades (PV inicial extra)
    b_pv_ini = 0
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        b_pv_ini += efeitos.get("pv_max_ini", 0)
    if b_pv_ini != 0:
        pv_calc.adicionar_bonus(
            fonte="Habilidades (Inicial)",
            categoria="Poder",
            valor=b_pv_ini
        )

    # PV por nível (níveis além do 1º)
    b_pv_nivel = 0
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        b_pv_nivel += efeitos.get("pv_max_nivel", 0)

    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pv_por_nivel = d.get("pv_nivel", 5) + mod_con + b_pv_nivel
            pv_calc.adicionar_bonus(
                fonte=f"Classe: {c.nome} ({n} nível{'is' if n > 1 else ''})",
                categoria="Classe",
                valor=n * pv_por_nivel
            )

    # ═══════════════════════════════════════════
    # ✨ PM - PILHA DE MODIFICADORES
    # ═══════════════════════════════════════════
    pm_calc = StatCalculado()
    
    # Base da classe
    pm_inicial_classe = dc.get("pm_inicial", 5)
    pm_calc.adicionar_bonus(
        fonte=f"Classe: {c_prim.nome} (Inicial)",
        categoria="Classe",
        valor=pm_inicial_classe
    )
    
    # Atributo de PM
    if mod_pm != 0:
        pm_calc.adicionar_bonus(
            fonte=f"Atributo: {attr_pm.upper()}",
            categoria="Atributo",
            valor=mod_pm
        )

    # PM por nível
    b_pm_niv = 0
    b_pm_impar = 0
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        b_pm_niv += efeitos.get("pm_max_nivel", 0)
        b_pm_impar += efeitos.get("pm_por_nivel_impar", 0)

    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pm_por_nivel = d.get("pm_nivel", 5) + b_pm_niv
            pm_calc.adicionar_bonus(
                fonte=f"Classe: {c.nome} ({n} nível{'is' if n > 1 else ''})",
                categoria="Classe",
                valor=n * pm_por_nivel
            )

    # PM por níveis ímpares (habilidades)
    if b_pm_impar > 0:
        impares = math.ceil(ficha.cabecalho.nivel_total / 2) * b_pm_impar
        if impares > 0:
            pm_calc.adicionar_bonus(
                fonte="Habilidades (Níveis Ímpares)",
                categoria="Poder",
                valor=impares
            )

    # ═══════════════════════════════════════════
    # 💾 SALVAR NA FICHA
    # ═══════════════════════════════════════════
    ficha.status.pv_calc = pv_calc
    ficha.status.pm_calc = pm_calc
    
    # Sincroniza com campos antigos (compatibilidade frontend)
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

    # Destreza
    if mod_des != 0:
        defesa_calc.adicionar_bonus(
            fonte="Destreza",
            categoria="Atributo",
            valor=mod_des
        )

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        val_fixo = efeitos.get("defesa_bonus", 0)
        if val_fixo != 0:
            defesa_calc.adicionar_bonus(
                fonte=f"Poder: {hab.nome}",
                categoria="Poder",
                valor=val_fixo
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


def calcular_reducoes_dano(ficha: Personagem):
    logger.info("--- [7] Calculando RD e Resistências ---")
    lista_rd = []

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if "resistencia_rd" in efeitos:
            for t, v in efeitos["resistencia_rd"].items():
                lista_rd.append(f"{t} {v}")

        if efeitos.get("resistencia_rd_escolha"):
            lista_rd.append(f"{efeitos['resistencia_rd_escolha']} 10")

        if "rd_escalavel_tormenta" in efeitos:
            dados = efeitos["rd_escalavel_tormenta"]
            elementos = dados.get("elementos", [])
            base = dados.get("base", 0)
            bonus_por_poder = dados.get("por_poder", 0)
            qtd_outros = max(0, qtd_tormenta - 1)
            total = base + (qtd_outros * bonus_por_poder)
            for elem in elementos:
                lista_rd.append(f"{elem} {total}")

    ficha.status.rd = lista_rd


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
            "proficiencia_exotica", "proficiencia_armadura", "proficiencia_escudo"
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

    ficha.status.proficiencias = sorted(list(proficiencias))
    ficha.status.imunidades = sorted(list(imunidades))
    ficha.status.sentidos = sorted(list(sentidos))