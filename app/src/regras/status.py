import math
import logging
from ..models import Personagem, DetalhesCalculo
from ..dados_classes import DADOS_CLASSES
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")


def calcular_pv_pm(ficha: Personagem):
    logger.info("--- [4] Calculando PV e PM ---")
    if not ficha.classes:
        return

    c_prim = ficha.classes[0]
    dc = DADOS_CLASSES.get(c_prim.nome or "", {})  # Proteção contra None

    mod_con = calcular_modificador(ficha.atributos.constituicao)
    attr_pm = dc.get("pm_atributo", "int")
    mod_pm = calcular_modificador(getattr(ficha.atributos, {
                                  'for': 'forca', 'des': 'destreza', 'con': 'constituicao', 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}.get(attr_pm, 'inteligencia')))

    # --- CORREÇÃO AQUI: b_pv_nivel (estava b_pv_niv) ---
    b_pv_ini, b_pv_nivel, b_pm_niv, b_pm_impar = 0, 0, 0, 0

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        b_pv_ini += efeitos.get("pv_max_ini", 0)
        # Agora a variável existe!
        b_pv_nivel += efeitos.get("pv_max_nivel", 0)
        b_pm_niv += efeitos.get("pm_max_nivel", 0)
        b_pm_impar += efeitos.get("pm_por_nivel_impar", 0)

    # PV
    pv_ini = dc.get("pv_inicial", 20) + mod_con + b_pv_ini
    pv_niv = 0
    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})  # Proteção contra None
            pv_niv += n * (d.get("pv_nivel", 5) + mod_con + b_pv_nivel)

    # PM
    pm_ini = dc.get("pm_inicial", 5) + mod_pm
    pm_niv = 0
    for c in ficha.classes:
        n = c.nivel - 1 if c == c_prim else c.nivel
        if n > 0:
            d = DADOS_CLASSES.get(c.nome or "", {})  # Proteção contra None
            pm_niv += n * (d.get("pm_nivel", 5) + b_pm_niv)

    impares = math.ceil(ficha.cabecalho.nivel_total / 2) * b_pm_impar

    ficha.status.pv.maximo = pv_ini + pv_niv
    ficha.status.pm.maximo = pm_ini + pm_niv + impares

    # Ajuste de atual se zerado ou excedente
    for stat in [ficha.status.pv, ficha.status.pm]:
        if stat.atual == 0 or stat.atual > stat.maximo:
            stat.atual = stat.maximo


def calcular_defesa_e_deslocamento(ficha: Personagem):
    logger.info("--- [5] Defesa/Deslocamento ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)
    bonus_def, desl = 0, ficha.status.deslocamento

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        bonus_def += efeitos.get("defesa_bonus", 0)
        if "deslocamento" in efeitos:
            desl = efeitos["deslocamento"]
        if hab.nome == "Esquiva":
            bonus_def += 2

    if hasattr(ficha.status, 'buffs'):
        for b in ficha.status.buffs:
            if b.atributo.lower() == "defesa":
                bonus_def += b.valor
            elif b.atributo.lower() == "deslocamento":
                desl += b.valor

    ficha.status.defesa.total = 10 + mod_des + bonus_def
    ficha.status.deslocamento = desl


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
