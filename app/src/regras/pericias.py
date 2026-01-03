import math
import logging
from typing import Dict, List, Any, Optional, Union

from ..models import Personagem, PericiaInfo, TamanhoEnum
from ..dados_classes import DADOS_CLASSES
from ..dados_pericias import DADOS_PERICIAS
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")


def _garantir_chave_str(valor: Any) -> str:
    """Função auxiliar para garantir chaves de dicionário como string para o Pylance."""
    if valor is None:
        return ""
    return str(valor)


def inicializar_pericias(ficha: Personagem):
    logger.info("--- [3] Inicializando Perícias (Refatorado & Genérico) ---")

    # 1. Modificadores de Atributo
    modificadores: Dict[str, int] = {}
    mapa_atributos = {
        'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
        'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
    }

    for k_short, k_full in mapa_atributos.items():
        val_attr = getattr(ficha.atributos, k_full)
        modificadores[k_short] = calcular_modificador(val_attr)

    nivel = max(1, ficha.cabecalho.nivel_total)
    bonus_metade_nivel = math.floor(nivel / 2)

    # 2. Coleta de Dados de Habilidades
    opcoes_atributos_extras: Dict[str, List[str]] = {}
    detalhamento_bonus: Dict[str, List[Dict[str, Any]]] = {}
    bonus_por_atributo: Dict[str, int] = {}

    tamanho = getattr(ficha.descricao, "tamanho", TamanhoEnum.MEDIO)
    penalidade_tamanho_furt = - \
        2 if tamanho == TamanhoEnum.GRANDE else (
            -5 if tamanho == TamanhoEnum.ENORME else 0)
    penalidade_armadura = 0

    # Conta quantos poderes da Tormenta o personagem tem
    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        # Penalidade de Armadura
        if "penalidade_armadura" in efeitos:
            penalidade_armadura += int(efeitos["penalidade_armadura"])

        # Opções de troca de atributo (ex: Atuação com Sabedoria)
        if "pericia_atributo_opcao" in efeitos and isinstance(efeitos["pericia_atributo_opcao"], dict):
            for p_alvo, novo_attr in efeitos["pericia_atributo_opcao"].items():
                if isinstance(p_alvo, str) and isinstance(novo_attr, str):
                    if p_alvo not in opcoes_atributos_extras:
                        opcoes_atributos_extras[p_alvo] = []
                    opcoes_atributos_extras[p_alvo].append(novo_attr)

        # ---------------------------------------------------------------------
        # REMOVIDO MOCK "if hab.nome == 'Deformidade'"
        # Agora usamos as lógicas genéricas abaixo:
        # ---------------------------------------------------------------------

        # 1. Bônus Específicos Diretos (Fixo) - Ex: Foco em Arma
        if "bonus_pericia" in efeitos and isinstance(efeitos["bonus_pericia"], dict):
            for p_nome, v_bonus in efeitos["bonus_pericia"].items():
                if isinstance(p_nome, str) and isinstance(v_bonus, (int, float)):
                    if p_nome not in detalhamento_bonus:
                        detalhamento_bonus[p_nome] = []
                    detalhamento_bonus[p_nome].append(
                        {"fonte": hab.nome, "valor": v_bonus})

        # 2. Bônus Genéricos por Atributo
        if "bonus_pericia_atributo" in efeitos and isinstance(efeitos["bonus_pericia_atributo"], dict):
            for attr_chave, v_bonus in efeitos["bonus_pericia_atributo"].items():
                if isinstance(attr_chave, str) and isinstance(v_bonus, (int, float)):
                    bonus_por_atributo[attr_chave] = bonus_por_atributo.get(
                        attr_chave, 0) + int(v_bonus)

        # 3. Bônus de Tormenta Escalável (Ex: Antenas)
        # Aplica +1 por poder da Tormenta nas perícias listadas
        if "bonus_pericia_tormenta" in efeitos:
            lista_alvos = efeitos["bonus_pericia_tormenta"]
            if isinstance(lista_alvos, list):
                bonus_val = qtd_tormenta
                for p_nome in lista_alvos:
                    if isinstance(p_nome, str):
                        if p_nome not in detalhamento_bonus:
                            detalhamento_bonus[p_nome] = []
                        detalhamento_bonus[p_nome].append(
                            {"fonte": f"{hab.nome} (Tormenta)", "valor": bonus_val})

        # 4. Bônus em Perícias à Escolha (Genérico) - Ex: Deformidade
        if "pericia_bonus_escolha" in efeitos:
            try:
                qtd_slots = int(efeitos["pericia_bonus_escolha"])
                # Padrão +2 se não especificado
                valor_do_bonus = int(efeitos.get("valor_bonus_escolha", 2))

                pericias_alvo = set()

                # Busca nas chaves padrão novas (pericia_bonus_0, pericia_bonus_1...)
                for i in range(qtd_slots):
                    escolha = efeitos.get(f"pericia_bonus_{i}")
                    if escolha and isinstance(escolha, str):
                        pericias_alvo.add(escolha)

                # Fallback legado para Deformidade antiga (opcional, para não quebrar fichas velhas)
                if hab.nome == "Deformidade":
                    legacy_1 = efeitos.get("pericia_1")
                    legacy_2 = efeitos.get("pericia_2")
                    if legacy_1:
                        pericias_alvo.add(legacy_1)
                    if legacy_2:
                        pericias_alvo.add(legacy_2)

                for p_nome in pericias_alvo:
                    if p_nome not in detalhamento_bonus:
                        detalhamento_bonus[p_nome] = []
                    detalhamento_bonus[p_nome].append(
                        {"fonte": hab.nome, "valor": valor_do_bonus}
                    )
            except Exception as e:
                logger.error(
                    f"Erro ao processar bônus de escolha em {hab.nome}: {e}")

    # 3. Lista de Perícias Treinadas/Extras
    pericias_extras: List[str] = []

    # De Habilidades (Versátil, Raciais, Poderes)
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        # Varre todas as chaves possíveis onde uma perícia pode estar escondida
        chaves_busca = ["pericia_1", "pericia_2", "pericia_escolha",
                        "memoria_postuma", "poder_ambicao_0", "poder_ambicao_1"]
        for k_escolha in chaves_busca:
            val = efeitos.get(k_escolha)
            if val and isinstance(val, str):
                chave_teste = _garantir_chave_str(val)
                chave_base = "Ofício" if chave_teste.startswith(
                    "Ofício") else chave_teste
                if chave_base in DADOS_PERICIAS:
                    pericias_extras.append(val)

    # De Origem
    if ficha.escolhas_origem:
        for e in ficha.escolhas_origem:
            if isinstance(e, str):
                chave_teste = _garantir_chave_str(e)
                chave_base = "Ofício" if chave_teste.startswith(
                    "Ofício") else chave_teste
                if chave_base in DADOS_PERICIAS:
                    pericias_extras.append(e)

    # De Classe
    fixas_classe: List[str] = []
    if ficha.classes:
        nome_classe_safe = _garantir_chave_str(ficha.classes[0].nome)
        dados_classe = DADOS_CLASSES.get(nome_classe_safe, {})

        fixas = dados_classe.get("pericias_fixas", []) or dados_classe.get(
            "pericias_iniciais", [])
        if isinstance(fixas, list):
            for f in fixas:
                if isinstance(f, str):
                    fixas_classe.append(f)

    # 4. Construção da Lista Final de Perícias
    novas_pericias: Dict[str, PericiaInfo] = {}

    set_chaves = set(DADOS_PERICIAS.keys())
    for k in ficha.pericias.keys():
        if k.startswith("Ofício"):
            set_chaves.add(k)
    for k in pericias_extras:
        if k.startswith("Ofício"):
            set_chaves.add(k)

    lista_ordenada = sorted(list(set_chaves))

    for nome_pericia in lista_ordenada:
        chave_base = "Ofício" if nome_pericia.startswith(
            "Ofício") else nome_pericia
        chave_base_safe = _garantir_chave_str(chave_base)
        dados_base = DADOS_PERICIAS.get(
            chave_base_safe, {"atributo": "int", "penalidade_armadura": False})

        info_antiga = ficha.pericias.get(nome_pericia, PericiaInfo())

        esta_treinado = (nome_pericia in pericias_extras) or (
            nome_pericia in fixas_classe)

        # Definição do Atributo
        attr_padrao = str(dados_base.get("atributo", "int"))
        possiveis = [attr_padrao]

        if nome_pericia in opcoes_atributos_extras:
            for opt in opcoes_atributos_extras[nome_pericia]:
                if opt not in possiveis:
                    possiveis.append(opt)

        attr_final = attr_padrao
        if info_antiga.atributo_selecionado and info_antiga.atributo_selecionado in possiveis:
            attr_final = info_antiga.atributo_selecionado

        # Cálculos Numéricos
        mod_attr = modificadores.get(attr_final, 0)

        bonus_treino = 0
        if esta_treinado:
            if nivel >= 15:
                bonus_treino = 6
            elif nivel >= 7:
                bonus_treino = 4
            else:
                bonus_treino = 2

        # Somatório de Bônus Automáticos
        total_automatico = 0
        fontes_bonus: List[str] = []

        # Aplica os bônus calculados na etapa 2
        if nome_pericia in detalhamento_bonus:
            for item in detalhamento_bonus[nome_pericia]:
                val = int(item["valor"])
                total_automatico += val
                sinal = "+" if val >= 0 else ""
                fontes_bonus.append(f"{item['fonte']} ({sinal}{val})")

        bonus_attr_geral = bonus_por_atributo.get(attr_final, 0)
        if bonus_attr_geral != 0:
            total_automatico += bonus_attr_geral
            sinal = "+" if bonus_attr_geral >= 0 else ""
            fontes_bonus.append(f"Racial/Geral ({sinal}{bonus_attr_geral})")

        penalidade_aplicada = 0
        if dados_base.get("penalidade_armadura"):
            penalidade_aplicada += penalidade_armadura

        if nome_pericia == "Furtividade" and penalidade_tamanho_furt != 0:
            penalidade_aplicada += penalidade_tamanho_furt
            fontes_bonus.append(f"Tamanho ({penalidade_tamanho_furt})")

        # Soma tudo
        total_final = bonus_metade_nivel + mod_attr + bonus_treino + \
            info_antiga.outros + total_automatico + penalidade_aplicada

        novas_pericias[nome_pericia] = PericiaInfo(
            treino=1 if esta_treinado else 0,
            bonus_nivel=bonus_metade_nivel,
            atributo_valor=mod_attr,
            outros=info_antiga.outros,
            total=total_final,
            bonus_automatico=total_automatico,
            atributo_selecionado=attr_final,
            atributos_possiveis=possiveis,
            fontes_bonus=fontes_bonus
        )

    ficha.pericias = novas_pericias
