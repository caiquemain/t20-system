import math
import logging
from ..models import Personagem
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
    mod_pm = calcular_modificador(getattr(ficha.atributos, {
                                  'for': 'forca', 'des': 'destreza', 'con': 'constituicao', 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}.get(attr_pm, 'inteligencia')))

    b_pv_ini, b_pv_nivel, b_pm_niv, b_pm_impar = 0, 0, 0, 0

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        b_pv_ini += efeitos.get("pv_max_ini", 0)
        b_pv_nivel += efeitos.get("pv_max_nivel", 0)
        b_pm_niv += efeitos.get("pm_max_nivel", 0)
        b_pm_impar += efeitos.get("pm_por_nivel_impar", 0)

    # PV
    pv_ini = dc.get("pv_inicial", 20) + mod_con + b_pv_ini
    pv_niv = 0
    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pv_niv += n * (d.get("pv_nivel", 5) + mod_con + b_pv_nivel)

    # PM
    pm_ini = dc.get("pm_inicial", 5) + mod_pm
    pm_niv = 0
    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})
            pm_niv += n * (d.get("pm_nivel", 5) + b_pm_niv)

    impares = math.ceil(ficha.cabecalho.nivel_total / 2) * b_pm_impar

    ficha.status.pv.maximo = pv_ini + pv_niv
    ficha.status.pm.maximo = pm_ini + pm_niv + impares

    for stat in [ficha.status.pv, ficha.status.pm]:
        if stat.atual == 0 or stat.atual > stat.maximo:
            stat.atual = stat.maximo


def calcular_defesa_e_deslocamento(ficha: Personagem):
    logger.info("--- [5] Defesa/Deslocamento Detalhada ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)

    bonus_def = 0
    desl = ficha.status.deslocamento

    # IMPORTANTE: Dicionário para compatibilidade com o modelo
    detalhes_defesa = {"Base": 10}

    if mod_des != 0:
        detalhes_defesa["Destreza"] = mod_des

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        val_fixo = efeitos.get("defesa_bonus", 0)
        if val_fixo != 0:
            bonus_def += val_fixo
            detalhes_defesa[hab.nome] = val_fixo

        if "defesa_bonus_tormenta" in efeitos:
            val_tormenta = qtd_tormenta
            bonus_def += val_tormenta
            chave = f"{hab.nome} (Tormenta)" if hab.nome in detalhes_defesa else hab.nome
            detalhes_defesa[chave] = val_tormenta

        if "deslocamento" in efeitos:
            desl = efeitos["deslocamento"]

        if hab.nome == "Esquiva":
            bonus_def += 2
            detalhes_defesa["Esquiva"] = 2

    if hasattr(ficha.status, 'buffs'):
        for b in ficha.status.buffs:
            if b.atributo.lower() == "defesa":
                bonus_def += b.valor
                detalhes_defesa[b.origem or 'Buff'] = b.valor
            elif b.atributo.lower() == "deslocamento":
                desl += b.valor

    ficha.status.defesa.total = 10 + mod_des + bonus_def
    ficha.status.deslocamento = desl

    try:
        setattr(ficha.status.defesa, "detalhes", detalhes_defesa)
    except AttributeError:
        pass


def calcular_reducoes_dano(ficha: Personagem):
    lista = []
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        if "resistencia_rd" in efeitos:
            for t, v in efeitos["resistencia_rd"].items():
                lista.append(f"{t} {v}")
        if efeitos.get("resistencia_rd_escolha"):
            lista.append(f"{efeitos['resistencia_rd_escolha']} 10")
    ficha.status.rd = lista


# --- NOVA FUNÇÃO: CALCULA PROFICIÊNCIAS E EXTRAS ---
def calcular_proficiencias_e_extras(ficha: Personagem):
    logger.info("--- [6] Proficiências e Extras (Anão/Guerreiro) ---")

    proficiencias = set()
    imunidades = set()
    sentidos = set()

    # 1. Proficiências Básicas da Classe (Guerreiro)
    if ficha.classes:
        for c in ficha.classes:
            dc = DADOS_CLASSES.get(c.nome or "", {})
            # Tenta pegar de 'proficiencias' ou 'proficiencias_iniciais'
            lista_prof = dc.get("proficiencias", []) or dc.get(
                "proficiencias_iniciais", [])
            for p in lista_prof:
                proficiencias.add(p)

    # 2. Varre Habilidades (Anão: Heredrimm, Rochas, etc)
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        # --- A. PROFICIÊNCIAS ---
        keys_prof = [
            "proficiencia_add",
            "proficiencia_simples",
            "proficiencia_marcial",
            "proficiencia_exotica",
            "proficiencia_armadura",
            "proficiencia_escudo"
        ]

        for k in keys_prof:
            if k in efeitos:
                val = efeitos[k]
                if isinstance(val, list):
                    # Ex: ["Machado de Batalha", "Marreta"]
                    proficiencias.update([str(v) for v in val])
                elif isinstance(val, str):
                    proficiencias.add(val)
                elif val is True:
                    # Ex: proficiencia_escudo: true -> "Escudo"
                    nome_legivel = k.replace("proficiencia_", "").capitalize()
                    if nome_legivel == "Simples":
                        nome_legivel = "Armas Simples"
                    if nome_legivel == "Marcial":
                        nome_legivel = "Armas Marciais"
                    proficiencias.add(nome_legivel)

        # --- B. IMUNIDADES ---
        if "imunidade" in efeitos:
            val = efeitos["imunidade"]
            if isinstance(val, list):
                imunidades.update(val)
            else:
                imunidades.add(str(val))

        # Devagar e Sempre (Anão): "imunidade_penalidade_mov"
        if "imunidade_penalidade_mov" in efeitos:
            imunidades.add("Deslocamento (Armadura/Carga)")

        # --- C. SENTIDOS ---
        if "sentido" in efeitos:
            val = efeitos["sentido"]
            if isinstance(val, list):
                sentidos.update(val)
            else:
                sentidos.add(str(val))

        # Conhecimento das Rochas: "visao_escuro": true
        if efeitos.get("visao_escuro"):
            sentidos.add("Visão no Escuro")

        if efeitos.get("faro"):
            sentidos.add("Faro")

    # Salva no objeto status (para o Frontend ler)
    ficha.status.proficiencias = sorted(list(proficiencias))
    ficha.status.imunidades = sorted(list(imunidades))
    ficha.status.sentidos = sorted(list(sentidos))
