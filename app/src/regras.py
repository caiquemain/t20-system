import math
from src.models import Personagem, TamanhoEnum, PericiaInfo
# Importações das tabelas
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_pericias import DADOS_PERICIAS

# --- FUNÇÕES AUXILIARES ---


def calcular_modificador(valor_atributo: int) -> int:
    """
    Regra T20 Jogo do Ano:
    O valor do atributo JÁ É o modificador.
    """
    return valor_atributo


def aplicar_dados_raciais(ficha: Personagem):
    """Aplica TAMANHO automaticamente ao detectar a raça."""
    if ficha.cabecalho.raca in DADOS_RACAS:
        dados = DADOS_RACAS[ficha.cabecalho.raca]
        if "tamanho" in dados:
            ficha.descricao.tamanho = dados["tamanho"]


def calcular_pv_pm(ficha: Personagem, mod_con: int, mods: dict):
    """Calcula PV e PM Máximos baseados nas classes e níveis."""
    pv_total = 0
    pm_total = 0

    for classe_info in ficha.classes:
        nome = classe_info.nome
        nivel = classe_info.nivel

        if nome in DADOS_CLASSES:
            dados = DADOS_CLASSES[nome]

            # PV
            if classe_info.primaria:
                pv_classe = (dados["pv_ini"] + mod_con)
                if nivel > 1:
                    pv_classe += (nivel - 1) * (dados["pv_niv"] + mod_con)

                # PM (Nível 1)
                pm_classe = dados["pm_ini"]
                if nivel > 1:
                    pm_classe += (nivel - 1) * dados["pm_niv"]

                # Soma atributo chave nos PMs se for classe primária
                attr_key = dados.get("attr_chave")
                if attr_key in mods:
                    pm_classe += mods[attr_key]

            else:
                # Classes secundárias
                pv_classe = nivel * (dados["pv_niv"] + mod_con)
                pm_classe = nivel * dados["pm_niv"]

            pv_total += pv_classe
            pm_total += pm_classe

    ficha.status.pv.maximo = pv_total
    ficha.status.pm.maximo = pm_total

    if ficha.status.pv.atual == 0:
        ficha.status.pv.atual = pv_total
    if ficha.status.pm.atual == 0:
        ficha.status.pm.atual = pm_total


def calcular_bonus_treino(grau: int) -> int:
    if grau == 0:
        return 0
    if grau == 1:
        return 2
    if grau == 2:
        return 4
    if grau >= 3:
        return 6
    return 0


def calcular_pericias(ficha: Personagem, metade_nivel: int, mods: dict):
    for nome_pericia, attr_chave in DADOS_PERICIAS.items():
        if nome_pericia not in ficha.pericias:
            ficha.pericias[nome_pericia] = PericiaInfo(
                treino=0,
                atributo_chave=attr_chave
            )

        pericia = ficha.pericias[nome_pericia]
        pericia.atributo_chave = attr_chave

        mod_attr = mods.get(attr_chave, 0)
        bonus_treino = calcular_bonus_treino(pericia.treino)

        pericia.total = (
            metade_nivel +
            mod_attr +
            bonus_treino +
            pericia.bonus_item +
            pericia.outros
        )


def atualizar_ficha(ficha: Personagem) -> Personagem:
    aplicar_dados_raciais(ficha)

    nivel_total = sum([c.nivel for c in ficha.classes])
    ficha.cabecalho.nivel_total = nivel_total
    metade_nivel = math.floor(nivel_total / 2)

    mods = {
        "for": calcular_modificador(ficha.atributos.forca),
        "des": calcular_modificador(ficha.atributos.destreza),
        "con": calcular_modificador(ficha.atributos.constituicao),
        "int": calcular_modificador(ficha.atributos.inteligencia),
        "sab": calcular_modificador(ficha.atributos.sabedoria),
        "car": calcular_modificador(ficha.atributos.carisma),
    }

    calcular_pv_pm(ficha, mods["con"], mods)
    calcular_pericias(ficha, metade_nivel, mods)

    defesa = ficha.status.defesa
    defesa.detalhes.des_mod = mods["des"]
    defesa.total = (
        defesa.detalhes.base +
        defesa.detalhes.des_mod +
        defesa.detalhes.armadura +
        defesa.detalhes.escudo +
        defesa.detalhes.outros
    )

    maior_atributo_mental = max(mods["int"], mods["sab"], mods["car"])
    ficha.combate.cd_magias = 10 + metade_nivel + maior_atributo_mental

    # --- NOVA REGRA DE CARGA (ESPAÇOS) ---
    # Base: 10 espaços
    # Se Força positiva: +2 por ponto
    # Se Força negativa: -1 por ponto

    forca_valor = ficha.atributos.forca
    limite_carga = 10

    if forca_valor > 0:
        limite_carga += (2 * forca_valor)
    else:
        # Se for negativo (ex: -2), somar -2 é o mesmo que subtrair 2 (1 ponto por ponto negativo)
        limite_carga += forca_valor

    # Garante que não fique negativo (mínimo 0 espaços)
    ficha.inventario.carga_maxima = max(0, limite_carga)

    peso_total = sum(
        [item.espaco * item.qtd for item in ficha.inventario.equipamentos])
    ficha.inventario.carga_total = peso_total

    return ficha
