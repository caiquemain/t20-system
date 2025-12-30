import math
import logging
from typing import Optional, Dict
from src.models import Personagem, TamanhoEnum, PericiaInfo, Habilidade, DetalhesCalculo
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_pericias import DADOS_PERICIAS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RegrasT20")


def calcular_modificador(valor_atributo: int) -> int:
    # Em T20 JdA, o valor do atributo JÁ É o modificador
    return valor_atributo


def calcular_nivel_personagem(ficha: Personagem) -> int:
    total = 0
    for classe in ficha.classes:
        total += classe.nivel
    return max(total, 1)


def limpar_habilidades_fixas(ficha: Personagem):
    """
    Remove habilidades de Raça, Classe e Origem antigas para recalcular.
    """
    habilidades_mantidas = []
    for hab in ficha.habilidades:
        if hab.tipo in ["Racial", "Classe", "Origem", "Raça"]:
            continue
        habilidades_mantidas.append(hab)
    ficha.habilidades = habilidades_mantidas

    # GARANTIA EXTRA: Limpa as listas que dependem dessas habilidades
    # Elas serão repovoadas pelas funções calcular_... logo em seguida
    ficha.proficiencias = []
    ficha.status.rd = []


def aplicar_bonus_atributos_raciais(ficha: Personagem):
    logger.info(f"--- [1] Aplicando Raça: {ficha.cabecalho.raca} ---")

    # Reseta para base
    ficha.atributos = ficha.atributos_base.model_copy()
    ficha.status.deslocamento = 9.0

    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)

    ficha.modificadores_raciais = {}

    if dados_raca:
        # A. Atributos Fixos
        if "attrs" in dados_raca:
            for attr, val in dados_raca["attrs"].items():
                if not attr:
                    continue
                short_key = str(attr).lower()[:3]
                mapa = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                        'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
                full_key = str(mapa.get(short_key, short_key))

                if hasattr(ficha.atributos, full_key):
                    atual = getattr(ficha.atributos, full_key)
                    setattr(ficha.atributos, full_key, int(atual) + int(val))
                    ficha.modificadores_raciais[full_key] = int(val)

        # B. Escolhas Variáveis
        for key_escolha in ficha.escolhas_atributos_raciais:
            chave_segura = str(key_escolha)
            if hasattr(ficha.atributos, chave_segura):
                atual = getattr(ficha.atributos, chave_segura)
                setattr(ficha.atributos, chave_segura, int(atual) + 1)
                prev = ficha.modificadores_raciais.get(chave_segura, 0)
                ficha.modificadores_raciais[chave_segura] = prev + 1

        tamanho = dados_raca.get("tamanho", TamanhoEnum.MEDIO)
        ficha.descricao.tamanho = tamanho

    return ficha


def garantir_habilidades_iniciais(ficha: Personagem, escolhas_preservadas: Optional[Dict] = None):
    """
    Assegura habilidades inicias, restaurando escolhas salvas se houver.
    """
    logger.info("--- [2] Garantindo Habilidades Iniciais ---")
    if escolhas_preservadas is None:
        escolhas_preservadas = {}

    nomes_existentes = {h.nome for h in ficha.habilidades}
    novas_habs = []

    # A. RACIAIS
    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)

    # Variável de controle para bloquear origem (ex: Golem)
    bloquear_origem = False

    if dados_raca and "habilidades" in dados_raca:
        for chave_hab in dados_raca["habilidades"]:
            dados_hab = DADOS_HABILIDADES_RACIAIS.get(
                chave_hab) or HABILIDADES_GERAIS.get(chave_hab)

            if dados_hab:
                # 1. Verifica se essa habilidade bloqueia a Origem
                efeitos_base = dados_hab.get("efeitos", {})
                if efeitos_base.get("sem_origem"):
                    bloquear_origem = True

                nome_real = dados_hab["nome"]

                if nome_real not in nomes_existentes:
                    # Recupera backup das escolhas (ex: Elemento do Qareen)
                    escolhas_anteriores = escolhas_preservadas.get(
                        nome_real, dados_hab.get("efeitos", {}))

                    nova_hab = Habilidade(
                        nome=nome_real,
                        tipo="Racial",
                        descricao=dados_hab.get("descricao", ""),
                        fonte=raca_nome,
                        escolhas_aplicadas=escolhas_anteriores
                    )
                    novas_habs.append(nova_hab)
                    nomes_existentes.add(nome_real)

                # Verifica se essa habilidade concede Poderes Extras (Versátil/Qareen)
                habilidade_atual = next(
                    (h for h in ficha.habilidades if h.nome == nome_real), None)
                if not habilidade_atual and novas_habs:
                    for h in reversed(novas_habs):
                        if h.nome == nome_real:
                            habilidade_atual = h
                            break

                if habilidade_atual:
                    efeitos = habilidade_atual.escolhas_aplicadas or {}

                    # Versátil (Poder Geral)
                    poder_escolhido = efeitos.get(
                        "poder_geral") or efeitos.get("poder_escolha")

                    # --- CORREÇÃO DE ERRO 500 (GOLEM) ---
                    # Só processa se poder_escolhido for TEXTO (nome do poder).
                    # Se for número (ex: 1), é apenas a quantidade de slots, então ignoramos.
                    if poder_escolhido and isinstance(poder_escolhido, str) and poder_escolhido not in nomes_existentes:
                        dados_poder = None
                        for p in HABILIDADES_GERAIS.values():
                            if p["nome"] == poder_escolhido:
                                dados_poder = p
                                break

                        descricao_poder = dados_poder["descricao"] if dados_poder else "Poder extra."
                        efeitos_poder = dados_poder.get(
                            "efeitos", {}) if dados_poder else {}

                        novas_habs.append(Habilidade(
                            nome=poder_escolhido,
                            tipo="Poder Geral",
                            descricao=descricao_poder,
                            fonte=f"Habilidade: {nome_real}",
                            escolhas_aplicadas=efeitos_poder
                        ))
                        nomes_existentes.add(poder_escolhido)

    # --- APLICA O BLOQUEIO DE ORIGEM ---
    if bloquear_origem:
        # Antes de limpar, remove o "Treino" das perícias que vieram da origem antiga.
        # Isso evita que elas fiquem presas como se fossem escolhas manuais.
        if ficha.escolhas_origem:
            for escolha_antiga in ficha.escolhas_origem:
                # Se a escolha antiga for uma perícia que existe na ficha...
                if escolha_antiga in ficha.pericias:
                    # ...reseta o treino para 0.
                    # Nota: Se essa perícia também for fixa da Classe (ex: Luta pro Guerreiro),
                    # a função 'inicializar_pericias' vai treiná-la novamente logo em seguida.
                    ficha.pericias[escolha_antiga].treino = 0

        # Agora sim, limpa a origem
        ficha.cabecalho.origem = ""
        ficha.escolhas_origem = []

    # B. CLASSE
    for classe in ficha.classes:
        for key_hab, dados_hab in DADOS_HABILIDADES_CLASSE.items():
            if dados_hab.get("classe") == classe.nome:
                nivel_req = dados_hab.get("nivel", 1)
                if nivel_req > 0 and nivel_req <= classe.nivel and "Poder de" not in dados_hab.get("tipo", ""):
                    nome_hab = dados_hab["nome"]
                    if nome_hab not in nomes_existentes:
                        novas_habs.append(Habilidade(
                            nome=nome_hab,
                            tipo="Classe",
                            descricao=dados_hab.get("descricao", ""),
                            fonte=f"{classe.nome} ({nivel_req})",
                            escolhas_aplicadas=dados_hab.get("efeitos", {})
                        ))
                        nomes_existentes.add(nome_hab)

    # C. ORIGEM
    if ficha.escolhas_origem:
        origem_nome = ficha.cabecalho.origem
        for escolha in ficha.escolhas_origem:
            if escolha in DADOS_PERICIAS or escolha.startswith("Ofício"):
                continue

            if escolha not in nomes_existentes:
                dados_poder = None
                for k, v in HABILIDADES_GERAIS.items():
                    if v["nome"] == escolha:
                        dados_poder = v
                        break

                descricao = dados_poder.get(
                    "descricao", "Benefício de Origem") if dados_poder else "Benefício único."
                efeitos = dados_poder.get("efeitos", {}) if dados_poder else {}

                novas_habs.append(Habilidade(
                    nome=escolha,
                    tipo="Origem",
                    descricao=descricao,
                    fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=efeitos
                ))
                nomes_existentes.add(escolha)

    if novas_habs:
        ficha.habilidades.extend(novas_habs)


def inicializar_pericias(ficha: Personagem):
    logger.info("--- [3] Inicializando Perícias ---")
    modificadores = {
        'for': calcular_modificador(ficha.atributos.forca),
        'des': calcular_modificador(ficha.atributos.destreza),
        'con': calcular_modificador(ficha.atributos.constituicao),
        'int': calcular_modificador(ficha.atributos.inteligencia),
        'sab': calcular_modificador(ficha.atributos.sabedoria),
        'car': calcular_modificador(ficha.atributos.carisma),
    }

    nivel = max(1, ficha.cabecalho.nivel_total)
    bonus_metade_nivel = math.floor(nivel / 2)
    penalidade_armadura_valor = 0

    pericias_extras_gratis = []
    bonus_numerico_habilidades = {}

    for hab in ficha.habilidades:
        efeitos = hab.escolhas_aplicadas or {}

        # Coleta treinos extras (Strings)
        for chave in ["pericia_1", "pericia_2", "pericia_escolha"]:
            val = efeitos.get(chave)
            if val and isinstance(val, str):
                pericias_extras_gratis.append(val)

        # Coleta bônus numéricos
        if "bonus_pericia" in efeitos:
            for pericia, valor in efeitos["bonus_pericia"].items():
                bonus_numerico_habilidades[pericia] = bonus_numerico_habilidades.get(
                    pericia, 0) + valor

    if ficha.escolhas_origem:
        for escolha in ficha.escolhas_origem:
            if escolha in DADOS_PERICIAS or escolha.startswith("Ofício"):
                pericias_extras_gratis.append(escolha)

    pericias_fixas_classe = []
    if ficha.classes:
        classe_inicial = ficha.classes[0].nome
        dados_classe = DADOS_CLASSES.get(classe_inicial)
        if dados_classe:
            fixas = dados_classe.get("pericias_fixas", []) or dados_classe.get(
                "pericias_iniciais", [])
            pericias_fixas_classe.extend(fixas)

    novas_pericias = {}
    lista_para_processar = list(DADOS_PERICIAS.keys())

    todos_oficios = [k for k in ficha.pericias.keys() if k.startswith("Ofício")] + \
                    [k for k in pericias_extras_gratis if k.startswith(
                        "Ofício")]

    for of in set(todos_oficios):
        if of not in lista_para_processar:
            lista_para_processar.append(of)

    for nome_pericia in lista_para_processar:
        chave_dados = "Ofício" if nome_pericia.startswith(
            "Ofício") else nome_pericia
        dados_base = DADOS_PERICIAS.get(chave_dados, {
                                        "atributo": "int", "treino_apenas": False, "penalidade_armadura": False})

        info_atual = ficha.pericias.get(nome_pericia, PericiaInfo())

        ganhou_extra = nome_pericia in pericias_extras_gratis
        ganhou_na_classe = nome_pericia in pericias_fixas_classe
        esta_treinado = (info_atual.treino >
                         0) or ganhou_extra or ganhou_na_classe

        attr_chave = getattr(info_atual, "atributo_override",
                             None) or dados_base["atributo"]
        mod_attr = modificadores.get(attr_chave, 0)

        nivel_treino = 1 if esta_treinado else 0
        bonus_treino = 0
        if esta_treinado:
            if nivel >= 15:
                bonus_treino = 6
            elif nivel >= 7:
                bonus_treino = 4
            else:
                bonus_treino = 2

        bonus_habilidade = bonus_numerico_habilidades.get(nome_pericia, 0)
        penalidade = penalidade_armadura_valor if dados_base["penalidade_armadura"] else 0

        outros_total = info_atual.outros + bonus_habilidade
        total = bonus_metade_nivel + mod_attr + bonus_treino + outros_total - penalidade

        novas_pericias[nome_pericia] = PericiaInfo(
            treino=nivel_treino,
            bonus_nivel=bonus_metade_nivel,
            atributo_valor=mod_attr,
            outros=outros_total,
            total=total
        )

    ficha.pericias = novas_pericias


def calcular_pv_pm(ficha: Personagem):
    logger.info("--- [4] Calculando PV e PM ---")
    if not ficha.classes:
        return

    classe_primaria = ficha.classes[0]
    nome_classe = classe_primaria.nome
    dados_classe_primaria = DADOS_CLASSES.get(nome_classe, {})

    pv_ini_base = dados_classe_primaria.get("pv_inicial", 20)
    pv_niv_base = dados_classe_primaria.get("pv_nivel", 5)
    pm_ini_base = dados_classe_primaria.get("pm_inicial", 5)
    pm_niv_base = dados_classe_primaria.get("pm_nivel", 5)
    attr_chave = dados_classe_primaria.get("pm_atributo", "int")

    try:
        mod_con = calcular_modificador(ficha.atributos.constituicao)

        bonus_pv_ini = 0
        bonus_pv_nivel = 0
        bonus_pm_nivel = 0

        for hab in ficha.habilidades:
            efeitos = hab.escolhas_aplicadas or {}

            if "pv_max_ini" in efeitos:
                bonus_pv_ini += efeitos["pv_max_ini"]
            if "pv_max_nivel" in efeitos:
                bonus_pv_nivel += efeitos["pv_max_nivel"]
            if "pm_max_nivel" in efeitos:
                bonus_pm_nivel += efeitos["pm_max_nivel"]

        pv_inicial = pv_ini_base + mod_con + bonus_pv_ini

        pv_nivel_total = 0
        niveis_primaria_para_somar = max(0, classe_primaria.nivel - 1)
        pv_nivel_total += niveis_primaria_para_somar * \
            (pv_niv_base + mod_con + bonus_pv_nivel)

        for c in ficha.classes[1:]:
            d_classe = DADOS_CLASSES.get(c.nome, {})
            val_niv = d_classe.get("pv_nivel", 0)
            pv_nivel_total += c.nivel * (val_niv + mod_con + bonus_pv_nivel)

        # Atualizado para usar DetalhesCalculo
        detalhes_pv = DetalhesCalculo(
            inicial=pv_inicial,
            nivel=pv_nivel_total,
            con=0,
            habilidades=bonus_pv_ini +
            (bonus_pv_nivel * ficha.cabecalho.nivel_total),
            outros=0,
            total=pv_inicial + pv_nivel_total
        )

        mapa_attr = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                     'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
        chave_full = mapa_attr.get(attr_chave, 'inteligencia')
        val_attr_chave = getattr(ficha.atributos, chave_full)
        mod_attr_chave = calcular_modificador(val_attr_chave)

        pm_inicial = pm_ini_base + mod_attr_chave
        pm_nivel_total = 0
        pm_nivel_total += niveis_primaria_para_somar * \
            (pm_niv_base + bonus_pm_nivel)

        for c in ficha.classes[1:]:
            d_classe = DADOS_CLASSES.get(c.nome, {})
            val_pm = d_classe.get("pm_nivel", 0)
            pm_nivel_total += c.nivel * (val_pm + bonus_pm_nivel)

        # Atualizado para usar DetalhesCalculo
        detalhes_pm = DetalhesCalculo(
            inicial=pm_inicial,
            nivel=pm_nivel_total,
            atributo=mod_attr_chave,
            habilidades=bonus_pm_nivel * ficha.cabecalho.nivel_total,
            outros=0,
            total=pm_inicial + pm_nivel_total
        )

        ficha.status.pv.maximo = detalhes_pv.total
        ficha.status.pv.calculo = detalhes_pv
        ficha.status.pm.maximo = detalhes_pm.total
        ficha.status.pm.calculo = detalhes_pm

    except Exception as e:
        logger.error(f"Erro ao calcular PV/PM: {e}")


def calcular_defesa_e_deslocamento(ficha: Personagem):
    logger.info("--- [5] Calculando Defesa e Deslocamento ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)

    bonus_defesa = 0
    deslocamento_final = ficha.status.deslocamento

    for hab in ficha.habilidades:
        efeitos = hab.escolhas_aplicadas or {}
        if "defesa_bonus" in efeitos:
            bonus_defesa += efeitos["defesa_bonus"]
        if "deslocamento" in efeitos:
            deslocamento_final = efeitos["deslocamento"]
        if hab.nome == "Esquiva":
            bonus_defesa += 2

    ficha.status.defesa.detalhes = {
        "base": 10,
        "des_mod": mod_des,
        "armadura": 0,
        "escudo": 0,
        "outros": bonus_defesa
    }
    ficha.status.defesa.total = 10 + mod_des + bonus_defesa
    ficha.status.deslocamento = deslocamento_final


def calcular_proficiencias_e_sentidos(ficha: Personagem):
    logger.info("--- [5.1] Calculando Proficiências ---")
    lista_final = set()

    for classe in ficha.classes:
        d_classe = DADOS_CLASSES.get(classe.nome, {})
        profs_classe = d_classe.get("proficiencias", [])
        for p in profs_classe:
            lista_final.add(p)

    for hab in ficha.habilidades:
        efeitos = hab.escolhas_aplicadas or {}
        if efeitos.get("visao_escuro"):
            lista_final.add("Visão no Escuro")
        if efeitos.get("visao_penumbra"):
            lista_final.add("Visão na Penumbra")
        if efeitos.get("visao_faro_desprevenido") or efeitos.get("sentido") == "Faro":
            lista_final.add("Faro")
        if "proficiencia_armas" in efeitos:
            for p in efeitos["proficiencia_armas"]:
                lista_final.add(p)
        if "proficiencia_simples" in efeitos:
            for p in efeitos["proficiencia_simples"]:
                lista_final.add(p.capitalize())
        if "imunidade_penalidade_mov" in efeitos:
            if "armadura" in efeitos["imunidade_penalidade_mov"]:
                lista_final.add("Movimento s/ Pen. Armadura")
            if "carga" in efeitos["imunidade_penalidade_mov"]:
                lista_final.add("Movimento s/ Pen. Carga")

    ficha.proficiencias = sorted(list(lista_final))


def calcular_reducoes_dano(ficha: Personagem):
    logger.info("--- [5.2] Calculando RD ---")
    lista_rd = []

    for hab in ficha.habilidades:
        efeitos = hab.escolhas_aplicadas or {}
        # RD Fixa
        if "resistencia_rd" in efeitos:
            for tipo, valor in efeitos["resistencia_rd"].items():
                lista_rd.append(f"{tipo} {valor}")

        # RD Escolhida (Qareen)
        escolha_rd = efeitos.get("resistencia_rd_escolha")
        if escolha_rd and isinstance(escolha_rd, str):
            lista_rd.append(f"{escolha_rd} 10")

    ficha.status.rd = lista_rd


def atualizar_ficha(ficha: Personagem) -> Personagem:
    logger.info(f"🔄 INICIANDO ATUALIZAÇÃO: {ficha.cabecalho.nome}")

    # 1. Backup das escolhas para não perder ao limpar
    escolhas_preservadas = {}
    for h in ficha.habilidades:
        if h.escolhas_aplicadas:
            escolhas_preservadas[h.nome] = h.escolhas_aplicadas

    # 2. Limpeza
    limpar_habilidades_fixas(ficha)

    # 3. Reconstrução
    ficha.cabecalho.nivel_total = calcular_nivel_personagem(ficha)
    ficha = aplicar_bonus_atributos_raciais(ficha)

    # Passamos o backup!
    garantir_habilidades_iniciais(ficha, escolhas_preservadas)

    inicializar_pericias(ficha)
    calcular_pv_pm(ficha)
    calcular_defesa_e_deslocamento(ficha)
    calcular_proficiencias_e_sentidos(ficha)
    calcular_reducoes_dano(ficha)

    logger.info("✅ Ficha atualizada com sucesso.")
    return ficha
