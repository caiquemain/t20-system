import math
import logging
from typing import Dict, List, Any, Optional, Union

from ..models import Personagem, PericiaInfo, TamanhoEnum, StatCalculado, FonteBonus
from ..dados_classes import DADOS_CLASSES
from ..dados_pericias import DADOS_PERICIAS
from .utils import calcular_modificador

logger = logging.getLogger("RegrasT20")

# ── Bônus condicionais de perícia (T20 JdA) ──
CONDICOES_BONUS_PERICIA = {
    "Conhecimento das Rochas": "no subterrâneo",
    "Reptiliano": "sem armadura ou roupas pesadas",
}
# Condições situacionais ativáveis pelo jogador (aba Efeitos & Condições)
CONDICAO_POR_HABILIDADE = {
    "Conhecimento das Rochas": "subterraneo",
    "Reptiliano": "sem_armadura",
}
CONDICOES_DISPONIVEIS = {
    "subterraneo": "No subterrâneo",
    "sem_armadura": "Sem armadura ou roupas pesadas",
}


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
    bonus_condicional: Dict[str, List[Dict[str, Any]]] = {}

    tamanho = getattr(ficha.descricao, "tamanho", TamanhoEnum.MEDIO)
    penalidade_tamanho_furt = -2 if tamanho == TamanhoEnum.GRANDE else (
        -5 if tamanho == TamanhoEnum.ENORME else 0)
    penalidade_armadura = 0

    qtd_tormenta = sum(
        1 for h in ficha.habilidades if h.tipo and "Tormenta" in h.tipo)

    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if "penalidade_armadura" in efeitos:
            penalidade_armadura += int(efeitos["penalidade_armadura"])

        if "pericia_atributo_opcao" in efeitos and isinstance(efeitos["pericia_atributo_opcao"], dict):
            for p_alvo, novo_attr in efeitos["pericia_atributo_opcao"].items():
                if isinstance(p_alvo, str) and isinstance(novo_attr, str):
                    if p_alvo not in opcoes_atributos_extras:
                        opcoes_atributos_extras[p_alvo] = []
                    opcoes_atributos_extras[p_alvo].append(novo_attr)

        # 1. Bônus Específicos Diretos (Fixo)
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

        # 2b. Bônus CONDICIONAIS (Anão subterrâneo, Trog sem armadura)
        if "bonus_pericia_condicional" in efeitos and isinstance(efeitos["bonus_pericia_condicional"], dict):
            condicao_txt = CONDICOES_BONUS_PERICIA.get(hab.nome, "condição especial")
            for p_nome, v_bonus in efeitos["bonus_pericia_condicional"].items():
                if isinstance(p_nome, str) and isinstance(v_bonus, (int, float)):
                    if p_nome not in bonus_condicional:
                        bonus_condicional[p_nome] = []
                    bonus_condicional[p_nome].append(
                        {"fonte": hab.nome, "valor": int(v_bonus),
                         "condicao": condicao_txt,
                         "condicao_id": CONDICAO_POR_HABILIDADE.get(hab.nome, "")})

        # 3. Bônus de Tormenta Escalável
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

        # 4. Bônus em Perícias à Escolha (Genérico; aceita dict {"Ofício": 2})
        if "pericia_bonus_escolha" in efeitos:
            try:
                raw_bpe = efeitos["pericia_bonus_escolha"]
                if isinstance(raw_bpe, dict):
                    qtd_slots = 1
                    valor_do_bonus = int(list(raw_bpe.values())[0]) if raw_bpe else 2
                else:
                    qtd_slots = int(raw_bpe)
                    valor_do_bonus = int(efeitos.get("valor_bonus_escolha", 2))

                pericias_alvo = set()
                for i in range(qtd_slots):
                    escolha = efeitos.get(f"pericia_bonus_{i}")
                    if escolha and isinstance(escolha, str):
                        pericias_alvo.add(escolha)

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

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
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

    if ficha.escolhas_origem:
        for e in ficha.escolhas_origem:
            if isinstance(e, str):
                chave_teste = _garantir_chave_str(e)
                chave_base = "Ofício" if chave_teste.startswith(
                    "Ofício") else chave_teste
                if chave_base in DADOS_PERICIAS:
                    pericias_extras.append(e)

    fixas_classe: List[str] = []
    selecao_fixa: List[str] = []
    if ficha.classes:
        nome_classe_safe = _garantir_chave_str(ficha.classes[0].nome)
        dados_classe = DADOS_CLASSES.get(nome_classe_safe, {})
        fixas = dados_classe.get("pericias_fixas", []) or dados_classe.get(
            "pericias_iniciais", [])
        if isinstance(fixas, list):
            for f in fixas:
                if isinstance(f, str):
                    fixas_classe.append(f)
        sel = dados_classe.get("pericias_fixas_selecao", []) or []
        if isinstance(sel, list):
            selecao_fixa = [x for x in sel if isinstance(x, str)]

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

        # Treinado: habilidades/origem, fixas da classe, OU escolha manual
        # validada no frontend (slots de classe/INT, requisito Luta/Pontaria)
        esta_treinado = (nome_pericia in pericias_extras) or (
            nome_pericia in fixas_classe) or (info_antiga.treino > 0)

        attr_padrao = str(dados_base.get("atributo", "int"))
        possiveis = [attr_padrao]
        if nome_pericia in opcoes_atributos_extras:
            for opt in opcoes_atributos_extras[nome_pericia]:
                if opt not in possiveis:
                    possiveis.append(opt)

        attr_final = attr_padrao
        if info_antiga.atributo_selecionado and info_antiga.atributo_selecionado in possiveis:
            attr_final = info_antiga.atributo_selecionado

        mod_attr = modificadores.get(attr_final, 0)

        bonus_treino = 0
        if esta_treinado:
            if nivel >= 15:
                bonus_treino = 6
            elif nivel >= 7:
                bonus_treino = 4
            else:
                bonus_treino = 2

        total_automatico = 0
        fontes_bonus: List[str] = []

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

        # Bônus condicionais com condição ATIVADA pelo jogador entram no total
        itens_cond = bonus_condicional.get(nome_pericia, [])
        condicoes_ativas = getattr(ficha, "condicoes_ativas", None) or []
        for item in itens_cond:
            if item.get("condicao_id") and item["condicao_id"] in condicoes_ativas:
                val = int(item["valor"])
                total_automatico += val
                sinal = "+" if val >= 0 else ""
                fontes_bonus.append(f"{item['fonte']} ({sinal}{val}, condição ativa)")

        total_final = bonus_metade_nivel + mod_attr + bonus_treino + \
            info_antiga.outros + total_automatico + penalidade_aplicada

        # Bônus condicionais INATIVOS: linha informativa com total situacional
        for item in itens_cond:
            if item.get("condicao_id") and item["condicao_id"] in condicoes_ativas:
                continue
            sinal = "+" if item["valor"] >= 0 else ""
            fontes_bonus.append(
                "⛰️ " + item["fonte"] + ": " + sinal + str(item["valor"]) +
                " se " + item["condicao"] +
                " (não somado ao total base; total situacional: " +
                str(total_final + item["valor"]) + ")")

        # ═══ PILHA DE MODIFICADORES DA PERÍCIA ═══
        calc = StatCalculado(base=mod_attr, total=0)
        calc.fontes.append(FonteBonus(
            fonte=f"Atributo: {attr_final.upper()}", categoria="Atributo", valor=mod_attr
        ))
        calc.total = mod_attr

        if bonus_metade_nivel != 0:
            calc.adicionar_bonus(f"Nível (½ de {nivel})", "Nível", bonus_metade_nivel)
        if bonus_treino != 0:
            calc.adicionar_bonus("Treinamento", "Treino", bonus_treino)
        if info_antiga.outros != 0:
            calc.adicionar_bonus("Outros (manual)", "Outros", info_antiga.outros)
        for item in detalhamento_bonus.get(nome_pericia, []):
            calc.adicionar_bonus(item["fonte"], "Poder", int(item["valor"]))
        if bonus_attr_geral != 0:
            calc.adicionar_bonus("Bônus Geral", "Racial", bonus_attr_geral)
        if penalidade_aplicada != 0:
            calc.adicionar_bonus("Penalidade (Armadura/Tamanho)", "Penalidade", penalidade_aplicada)
        for item in itens_cond:
            if item.get("condicao_id") and item["condicao_id"] in condicoes_ativas:
                calc.adicionar_bonus(item["fonte"], "Condicional", int(item["valor"]))

        novas_pericias[nome_pericia] = PericiaInfo(
            treino=1 if esta_treinado else 0,
            bonus_nivel=bonus_metade_nivel,
            atributo_valor=mod_attr,
            outros=info_antiga.outros,
            total=total_final,
            bonus_automatico=total_automatico,
            atributo_selecionado=attr_final,
            atributos_possiveis=possiveis,
            fontes_bonus=fontes_bonus,
            calculo=calc
        )

    ficha.pericias = novas_pericias
