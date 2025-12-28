import math
import logging
from src.models import Personagem, TamanhoEnum, PericiaInfo, Habilidade, DetalhesPV, DetalhesPM, DetalhesDeslocamento
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_pericias import DADOS_PERICIAS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_habilidades import HABILIDADES_GERAIS

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RegrasT20")


def calcular_modificador(valor_atributo: int) -> int:
    # CORREÇÃO CRUCIAL: Assume que os valores na ficha JÁ SÃO os modificadores
    # Se você quiser voltar ao sistema de Score (10, 12, 18), use: math.floor((valor_atributo - 10) / 2)
    return valor_atributo


def calcular_nivel_personagem(ficha: Personagem) -> int:
    total = 0
    for classe in ficha.classes:
        total += classe.nivel
    return max(total, 1)


def limpar_habilidades_fixas(ficha: Personagem):
    """Remove habilidades de Raça e Classe antigas para recalcular."""
    habilidades_mantidas = []
    for hab in ficha.habilidades:
        if hab.tipo in ["Racial", "Classe"]:
            continue
        habilidades_mantidas.append(hab)
    ficha.habilidades = habilidades_mantidas


def aplicar_bonus_atributos_raciais(ficha: Personagem):
    logger.info(f"--- [1] Aplicando Raça: {ficha.cabecalho.raca} ---")

    # 1. Reseta atributos e Deslocamento
    ficha.atributos = ficha.atributos_base.model_copy()
    ficha.status.deslocamento = 9.0

    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)

    ficha.modificadores_raciais = {}

    if dados_raca:
        # A. Atributos Fixos (Chave 'attrs' conforme seu arquivo)
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

        # B. Escolhas
        for key_escolha in ficha.escolhas_atributos_raciais:
            chave_segura = str(key_escolha)
            if hasattr(ficha.atributos, chave_segura):
                atual = getattr(ficha.atributos, chave_segura)
                setattr(ficha.atributos, chave_segura, int(atual) + 1)
                prev = ficha.modificadores_raciais.get(chave_segura, 0)
                ficha.modificadores_raciais[chave_segura] = prev + 1

        # C. Tamanho
        tamanho = dados_raca.get("tamanho", TamanhoEnum.MEDIO)
        ficha.descricao.tamanho = tamanho

    return ficha


def inicializar_pericias(ficha: Personagem):
    logger.info("--- [2] Inicializando Perícias ---")

    # 1. Calcula Modificadores de Atributos
    modificadores = {
        'for': calcular_modificador(ficha.atributos.forca),
        'des': calcular_modificador(ficha.atributos.destreza),
        'con': calcular_modificador(ficha.atributos.constituicao),
        'int': calcular_modificador(ficha.atributos.inteligencia),
        'sab': calcular_modificador(ficha.atributos.sabedoria),
        'car': calcular_modificador(ficha.atributos.carisma),
    }

    # 2. Dados básicos
    nivel = max(1, ficha.cabecalho.nivel_total)
    bonus_metade_nivel = math.floor(nivel / 2)
    penalidade_armadura_valor = 0  # Futuramente ler do inventário

    # --- LÓGICA DE ORIGEM ---
    pericias_origem = []
    if ficha.escolhas_origem:
        for escolha in ficha.escolhas_origem:
            if escolha in DADOS_PERICIAS or escolha.startswith("Ofício"):
                pericias_origem.append(escolha)

    # --- NOVO: LÓGICA DE CLASSE (PERÍCIAS FIXAS) ---
    pericias_fixas_classe = []
    if ficha.classes:
        # Pega a primeira classe (classe inicial define as perícias fixas)
        classe_inicial = ficha.classes[0].nome
        dados_classe = DADOS_CLASSES.get(classe_inicial)
        if dados_classe:
            # Pega lista de fixas (ex: Fortitude para Guerreiro, Vontade para Clérigo)
            fixas = dados_classe.get("pericias_fixas", []) or dados_classe.get(
                "pericias_iniciais", [])
            pericias_fixas_classe.extend(fixas)

    # 3. Lista para processar
    novas_pericias = {}
    lista_para_processar = list(DADOS_PERICIAS.keys())

    # Adiciona Ofícios do usuário
    for pericia_usuario in ficha.pericias.keys():
        if pericia_usuario.startswith("Ofício") and pericia_usuario not in lista_para_processar:
            lista_para_processar.append(pericia_usuario)

    # Adiciona Ofícios da Origem
    for pericia_origem in pericias_origem:
        if pericia_origem not in lista_para_processar:
            lista_para_processar.append(pericia_origem)

    # 4. Loop de Cálculo
    for nome_pericia in lista_para_processar:
        chave_dados = "Ofício" if nome_pericia.startswith(
            "Ofício") else nome_pericia
        dados_base = DADOS_PERICIAS.get(chave_dados, {
                                        "atributo": "int", "treino_apenas": False, "penalidade_armadura": False})

        info_atual = ficha.pericias.get(nome_pericia, PericiaInfo())

        # --- VERIFICAÇÕES DE TREINO ---
        ganhou_na_origem = nome_pericia in pericias_origem
        ganhou_na_classe = nome_pericia in pericias_fixas_classe  # <--- AQUI ESTAVA FALTANDO

        # O personagem é treinado se:
        # 1. Marcou manualmente (info_atual.treino > 0)
        # 2. Ganhou pela Origem
        # 3. É fixa da Classe
        esta_treinado = (info_atual.treino >
                         0) or ganhou_na_origem or ganhou_na_classe

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

        penalidade = penalidade_armadura_valor if dados_base["penalidade_armadura"] else 0

        total = bonus_metade_nivel + mod_attr + \
            bonus_treino + info_atual.outros - penalidade

        novas_pericias[nome_pericia] = PericiaInfo(
            treino=nivel_treino,  # Salva como treinado
            bonus_nivel=bonus_metade_nivel,
            atributo_valor=mod_attr,
            outros=info_atual.outros,
            total=total
        )

    ficha.pericias = novas_pericias


def calcular_pv_pm(ficha: Personagem):
    logger.info("--- [3] Calculando PV e PM ---")
    if not ficha.classes:
        return

    classe_primaria = ficha.classes[0]
    nome_classe = classe_primaria.nome
    dados_classe_primaria = DADOS_CLASSES.get(nome_classe, {})

    # Busca chaves com fallback (pv_inicial ou pv_ini)
    pv_ini_base = dados_classe_primaria.get(
        "pv_inicial", dados_classe_primaria.get("pv_ini", 0))
    pv_niv_base = dados_classe_primaria.get(
        "pv_nivel", dados_classe_primaria.get("pv_niv", 0))
    pm_ini_base = dados_classe_primaria.get(
        "pm_inicial", dados_classe_primaria.get("pm_ini", 0))
    pm_niv_base = dados_classe_primaria.get(
        "pm_nivel", dados_classe_primaria.get("pm_niv", 0))

    # Atributo chave
    attr_chave = dados_classe_primaria.get(
        "pm_atributo", dados_classe_primaria.get("attr_chave", "int"))

    try:
        mod_con = calcular_modificador(ficha.atributos.constituicao)

        # --- PV ---
        pv_inicial = pv_ini_base + mod_con
        pv_nivel = 0
        niveis_primaria_para_somar = max(0, classe_primaria.nivel - 1)
        pv_nivel += niveis_primaria_para_somar * (pv_niv_base + mod_con)

        for c in ficha.classes[1:]:
            d_classe = DADOS_CLASSES.get(c.nome, {})
            val_niv = d_classe.get("pv_nivel", d_classe.get("pv_niv", 0))
            pv_nivel += c.nivel * (val_niv + mod_con)

        detalhes_pv = DetalhesPV(inicial=pv_inicial, nivel=pv_nivel,
                                 con=0, habilidades=0, outros=0, total=pv_inicial + pv_nivel)

        # --- PM ---
        mapa_attr = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                     'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
        chave_full = mapa_attr.get(attr_chave, 'inteligencia')
        val_attr_chave = getattr(ficha.atributos, chave_full)
        mod_attr_chave = calcular_modificador(val_attr_chave)

        pm_inicial = pm_ini_base + mod_attr_chave
        pm_nivel = 0
        pm_nivel += niveis_primaria_para_somar * pm_niv_base

        for c in ficha.classes[1:]:
            d_classe = DADOS_CLASSES.get(c.nome, {})
            val_pm = d_classe.get("pm_nivel", d_classe.get("pm_niv", 0))
            pm_nivel += c.nivel * val_pm

        detalhes_pm = DetalhesPM(inicial=pm_inicial, nivel=pm_nivel, atributo=mod_attr_chave,
                                 habilidades=0, outros=0, total=pm_inicial + pm_nivel)

        ficha.status.pv.maximo = detalhes_pv.total
        ficha.status.pv.calculo = detalhes_pv
        ficha.status.pm.maximo = detalhes_pm.total
        ficha.status.pm.calculo = detalhes_pm

    except Exception:
        pass


def calcular_defesa_base(ficha: Personagem):
    logger.info("--- [4] Calculando Defesa ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)

    # 10 + Destreza
    total = 10 + mod_des

    ficha.status.defesa.detalhes = {
        "base": 10,
        "destreza": mod_des,
        "armadura": 0,
        "escudo": 0,
        "outros": 0
    }
    ficha.status.defesa.total = total


def garantir_habilidades_iniciais(ficha: Personagem):
    logger.info("--- [5] Garantindo Habilidades Iniciais ---")

    # Conjunto para evitar duplicatas (usa o nome da habilidade)
    nomes_existentes = {h.nome for h in ficha.habilidades}
    novas_habs = []

    # A. RACIAIS
    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)

    if dados_raca and "habilidades" in dados_raca:
        for chave_hab in dados_raca["habilidades"]:
            dados_hab = HABILIDADES_GERAIS.get(chave_hab)
            if dados_hab:
                nome_real = dados_hab["nome"]
                if nome_real not in nomes_existentes:
                    novas_habs.append(Habilidade(
                        nome=nome_real,
                        tipo="Racial",
                        descricao=dados_hab.get("descricao", ""),
                        fonte=raca_nome,
                        escolhas_aplicadas=dados_hab.get("efeitos", {})
                    ))
                    nomes_existentes.add(nome_real)

    # B. CLASSE (Habilidades fixas)
    for classe in ficha.classes:
        for key_hab, dados_hab in DADOS_HABILIDADES_CLASSE.items():
            if dados_hab.get("classe") == classe.nome:
                nivel_req = dados_hab.get("nivel", 1)
                # Adiciona habilidade fixa se nível alcançado e não for Poder de Escolha
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

    # C. ORIGEM (Poderes e Benefícios únicos)
    if ficha.escolhas_origem:
        origem_nome = ficha.cabecalho.origem
        for escolha in ficha.escolhas_origem:
            # Ignora se for Perícia ou Ofício (já tratado em inicializar_pericias)
            if escolha in DADOS_PERICIAS or escolha.startswith("Ofício"):
                continue

            # Se ainda não tem esse poder/benefício na lista
            if escolha not in nomes_existentes:
                # Tenta buscar os dados completos do poder em HABILIDADES_GERAIS
                # (Muitos benefícios de origem são Poderes Gerais, ex: "Vontade de Ferro")
                dados_poder = None

                # Busca pelo nome exato no dicionário de Habilidades Gerais
                for k, v in HABILIDADES_GERAIS.items():
                    if v["nome"] == escolha:
                        dados_poder = v
                        break

                # Prepara dados (se achou ou cria genérico)
                descricao = dados_poder.get(
                    "descricao", "Benefício de Origem") if dados_poder else "Benefício único da Origem."
                efeitos = dados_poder.get("efeitos", {}) if dados_poder else {}

                novas_habs.append(Habilidade(
                    nome=escolha,
                    tipo="Origem",
                    descricao=descricao,
                    fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=efeitos
                ))
                nomes_existentes.add(escolha)

    # Adiciona tudo o que foi encontrado de novo
    if novas_habs:
        ficha.habilidades.extend(novas_habs)


def aplicar_habilidades_efeitos_numericos(ficha: Personagem):
    logger.info("--- [6] Aplicando Efeitos Numéricos ---")
    bonus_pv = 0
    bonus_pm = 0
    bonus_defesa = 0

    for hab in ficha.habilidades:
        efeitos = hab.escolhas_aplicadas or {}

        # 1. DESLOCAMENTO (Ex: Anão)
        if "deslocamento" in efeitos:
            ficha.status.deslocamento = float(efeitos["deslocamento"])

        # 2. PV (Ex: Duro como Pedra)
        if "pv_max_ini" in efeitos:
            pv_extra = efeitos["pv_max_ini"] + \
                (efeitos.get("pv_max_nivel", 0) *
                 (ficha.cabecalho.nivel_total - 1))
            bonus_pv += pv_extra
        elif hab.nome == "Vitalidade":
            bonus_pv += 1 * ficha.cabecalho.nivel_total

        # 3. PM
        if hab.nome == "Vontade de Ferro":
            bonus_pm += 1 + (ficha.cabecalho.nivel_total // 2)

        # 4. Defesa
        if hab.nome == "Esquiva":
            bonus_defesa += 2

    # Aplica
    if ficha.status.pv.calculo:
        ficha.status.pv.calculo.habilidades = bonus_pv
        ficha.status.pv.calculo.total += bonus_pv
        ficha.status.pv.maximo = ficha.status.pv.calculo.total

    if ficha.status.pm.calculo:
        ficha.status.pm.calculo.habilidades = bonus_pm
        ficha.status.pm.calculo.total += bonus_pm
        ficha.status.pm.maximo = ficha.status.pm.calculo.total

    if "outros" not in ficha.status.defesa.detalhes:
        ficha.status.defesa.detalhes["outros"] = 0

    ficha.status.defesa.detalhes["outros"] += bonus_defesa
    ficha.status.defesa.total += bonus_defesa


def atualizar_ficha(ficha: Personagem) -> Personagem:
    logger.info(f"🔄 INICIANDO ATUALIZAÇÃO: {ficha.cabecalho.nome}")
    limpar_habilidades_fixas(ficha)
    ficha.cabecalho.nivel_total = calcular_nivel_personagem(ficha)
    ficha = aplicar_bonus_atributos_raciais(ficha)
    inicializar_pericias(ficha)
    calcular_pv_pm(ficha)
    calcular_defesa_base(ficha)
    garantir_habilidades_iniciais(ficha)
    aplicar_habilidades_efeitos_numericos(ficha)
    logger.info("✅ Ficha atualizada com sucesso.")
    return ficha
