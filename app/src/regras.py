import math
from src.models import Personagem, TamanhoEnum, PericiaInfo, Habilidade, DetalhesPV, DetalhesPM, DetalhesDeslocamento
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_pericias import DADOS_PERICIAS
from src.dados_itens import DADOS_ITENS
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_origens import DADOS_ORIGENS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE

# --- FUNÇÕES AUXILIARES ---


def calcular_atributos_totais(ficha: Personagem):
    """
    Soma Base + Racial + Envelhecimento + Outros para obter o valor final.
    """
    map_keys = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}

    mods = {}

    for key_short, key_full in map_keys.items():
        base = getattr(ficha.atributos_base, key_full)

        # Pega modificador racial (que já inclui as escolhas processadas em aplicar_dados_raciais)
        racial = ficha.modificadores_raciais.get(key_full, 0)
        if racial == 0:
            racial = ficha.modificadores_raciais.get(key_short, 0)

        idade = ficha.modificadores_envelhecimento.get(key_short, 0)
        outros = ficha.modificadores_outros.get(key_short, 0)

        total_modificador = base + racial + idade + outros

        setattr(ficha.atributos, key_full, total_modificador)
        mods[key_short] = total_modificador

    return mods


def aplicar_dados_raciais(ficha: Personagem):
    mapa_atributos = {
        'forca': 'for', 'destreza': 'des', 'constituicao': 'con',
        'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car'
    }

    if ficha.cabecalho.raca in DADOS_RACAS:
        dados_raca = DADOS_RACAS[ficha.cabecalho.raca]

        if "tamanho" in dados_raca:
            ficha.descricao.tamanho = dados_raca["tamanho"]

        mods_finais = dados_raca.get("attrs", {}).copy()

        for escolha in ficha.escolhas_atributos_raciais:
            key_short = mapa_atributos.get(escolha)
            if key_short:
                valor_atual = mods_finais.get(key_short, 0)
                mods_finais[key_short] = valor_atual + 1

        ficha.modificadores_raciais = mods_finais


def calcular_envelhecimento(ficha: Personagem):
    try:
        idade = int(ficha.descricao.idade or 0)
    except:
        idade = 0

    mods = {}
    if idade >= 70:
        mods = {"for": -3, "des": -3, "con": -3, "int": 2, "sab": 2, "car": 2}
    elif idade >= 45:
        mods = {"for": -1, "des": -1, "con": -1, "int": 1, "sab": 1, "car": 1}

    ficha.modificadores_envelhecimento = mods


def calcular_pv_pm(ficha: Personagem, mod_con: int, mods: dict, pv_ini_racial: int, pv_niv_racial: int, pm_niv_racial: int, pm_atributo_bonus: int):
    detalhes_pv = DetalhesPV()
    detalhes_pm = DetalhesPM()

    pv_total = 0
    pm_total = 0

    # Aplica bônus raciais/globais iniciais
    pv_total += pv_ini_racial
    detalhes_pv.outros += pv_ini_racial

    for i, classe_info in enumerate(ficha.classes):
        nome = classe_info.nome
        nivel = classe_info.nivel

        if nome in DADOS_CLASSES:
            dados = DADOS_CLASSES[nome]

            # --- CÁLCULO DE PV ---
            if i == 0:  # Classe Inicial
                valor_classe_ini = dados["pv_ini"] + mod_con
                pv_total += valor_classe_ini

                detalhes_pv.inicial += dados["pv_ini"]
                detalhes_pv.con += mod_con

                if nivel > 1:
                    ganho_por_nivel = (
                        nivel - 1) * (dados["pv_niv"] + pv_niv_racial + mod_con)
                    pv_total += ganho_por_nivel

                    detalhes_pv.nivel += (nivel - 1) * dados["pv_niv"]
                    detalhes_pv.con += (nivel - 1) * mod_con
                    detalhes_pv.outros += (nivel - 1) * pv_niv_racial
            else:
                # Multiclasse
                ganho = nivel * (dados["pv_niv"] + pv_niv_racial + mod_con)
                pv_total += ganho

                detalhes_pv.nivel += nivel * dados["pv_niv"]
                detalhes_pv.con += nivel * mod_con
                detalhes_pv.outros += nivel * pv_niv_racial

            # --- CÁLCULO DE PM ---
            pm_ganho = nivel * (dados["pm_niv"] + pm_niv_racial)
            pm_total += pm_ganho

            detalhes_pm.nivel += nivel * dados["pm_niv"]
            detalhes_pm.outros += nivel * pm_niv_racial

            # CORREÇÃO: Removida a soma automática do atributo chave da classe.
            # Agora isso depende de habilidades (processado via pm_atributo_bonus)

    # Soma bônus de atributos vindos de habilidades (ex: Abençoado do Paladino)
    pm_total += pm_atributo_bonus
    detalhes_pm.atributo += pm_atributo_bonus

    # Salvar Detalhes
    ficha.status.pv.detalhes_pv = detalhes_pv
    ficha.status.pm.detalhes_pm = detalhes_pm

    # Finalizar Totais
    ficha.status.pv.maximo = max(1, pv_total)
    ficha.status.pm.maximo = max(0, pm_total)

    # Resetar atuais para máximo (Regra de atualização de ficha)
    ficha.status.pv.atual = ficha.status.pv.maximo
    ficha.status.pm.atual = ficha.status.pm.maximo


def calcular_bonus_treino(grau: int, nivel: int) -> int:
    if grau == 0:
        return 0
    if nivel >= 15:
        return 6
    if nivel >= 7:
        return 4
    return 2


def inicializar_pericias_fixas(ficha: Personagem):
    classe_nome = ficha.classes[0].nome if ficha.classes else None

    if classe_nome and classe_nome in DADOS_CLASSES:
        dados = DADOS_CLASSES[classe_nome]
        pericias_fixas = dados.get("pericias_fixas", [])

        for nome_pericia in pericias_fixas:
            if nome_pericia in ficha.pericias:
                if ficha.pericias[nome_pericia].treino < 1:
                    ficha.pericias[nome_pericia].treino = 1
            elif nome_pericia:
                attr_chave = DADOS_PERICIAS.get(nome_pericia, 'int')
                ficha.pericias[nome_pericia] = PericiaInfo(
                    treino=1, atributo_chave=attr_chave)


def aplicar_habilidades_efeitos_numericos(ficha: Personagem, mods: dict):
    """
    Calcula bônus numéricos passivos de habilidades.
    Agora recebe 'mods' para calcular bônus baseados em atributos.
    """
    for nome_pericia, pericia_info in ficha.pericias.items():
        pericia_info.outros = 0
        pericia_info.bonus_item = 0
    ficha.status.defesa.detalhes.outros = 0

    pv_ini_bonus_global = 0
    pv_niv_bonus_global = 0
    pm_niv_bonus_global = 0
    pm_atributo_bonus_global = 0  # Novo acumulador

    if ficha.habilidades:
        for hab_info in ficha.habilidades:
            def_hab = HABILIDADES_GERAIS.get(hab_info.nome)

            if not def_hab:
                for k, v in DADOS_HABILIDADES_CLASSE.items():
                    if v.get('nome') == hab_info.nome:
                        def_hab = v
                        break

            if not def_hab:
                for k, v in HABILIDADES_GERAIS.items():
                    if v.get('nome') == hab_info.nome:
                        def_hab = v
                        break

            if def_hab and def_hab.get("efeitos"):
                efeitos = def_hab["efeitos"]

                pv_ini_bonus_global += efeitos.get("pv_max_ini", 0)
                pv_niv_bonus_global += efeitos.get("pv_max_nivel", 0)
                pm_niv_bonus_global += efeitos.get("pm_max_nivel", 0)

                # Lógica para "pm_soma_atributo" (ex: Paladino soma Carisma)
                if "pm_soma_atributo" in efeitos:
                    attr = efeitos["pm_soma_atributo"]
                    valor_attr = mods.get(attr, 0)
                    if valor_attr > 0:
                        pm_atributo_bonus_global += valor_attr

                ficha.status.defesa.detalhes.outros += efeitos.get(
                    "defesa_bonus", 0)

                if 'bonus_pericia' in efeitos:
                    for pericia, bonus in efeitos['bonus_pericia'].items():
                        if pericia in ficha.pericias:
                            ficha.pericias[pericia].outros += bonus

    return pv_ini_bonus_global, pv_niv_bonus_global, pm_niv_bonus_global, pm_atributo_bonus_global


def aplicar_origem(ficha: Personagem):
    nome_origem = ficha.cabecalho.origem
    dados = DADOS_ORIGENS.get(nome_origem)

    if dados:
        ficha.habilidades.append(Habilidade(
            nome=nome_origem,
            tipo="Origem",
            descricao=dados.get("descricao", "Origem."),
            fonte="Origem"
        ))

        pericias_origem_fixas = dados.get("pericias_fixas", [])
        for nome_pericia in pericias_origem_fixas:
            if nome_pericia in DADOS_PERICIAS:
                if nome_pericia in ficha.pericias:
                    ficha.pericias[nome_pericia].treino = max(
                        ficha.pericias[nome_pericia].treino, 1)
                else:
                    attr_chave = DADOS_PERICIAS.get(nome_pericia, 'int')
                    ficha.pericias[nome_pericia] = PericiaInfo(
                        treino=1, atributo_chave=attr_chave)

        for beneficio in getattr(ficha, 'escolhas_origem', []):
            if beneficio in DADOS_PERICIAS:
                if beneficio in ficha.pericias:
                    ficha.pericias[beneficio].treino = max(
                        ficha.pericias[beneficio].treino, 1)
                else:
                    attr_chave = DADOS_PERICIAS.get(beneficio, 'int')
                    ficha.pericias[beneficio] = PericiaInfo(
                        treino=1, atributo_chave=attr_chave)
            else:
                def_poder = None
                if beneficio in HABILIDADES_GERAIS:
                    def_poder = HABILIDADES_GERAIS[beneficio]
                else:
                    for k, v in HABILIDADES_GERAIS.items():
                        if v.get('nome') == beneficio:
                            def_poder = v
                            break

                if def_poder:
                    if not any(h.nome == def_poder["nome"] for h in ficha.habilidades):
                        ficha.habilidades.append(Habilidade(
                            nome=def_poder["nome"],
                            tipo=f"Poder (Origem: {nome_origem})",
                            descricao=def_poder["descricao"],
                            fonte=def_poder.get("fonte", "Origem")
                        ))


def aplicar_habilidades_raciais(ficha: Personagem, escolhas_salvas: dict = None):
    if ficha.cabecalho.raca in DADOS_RACAS:
        infoRaca = DADOS_RACAS[ficha.cabecalho.raca]

        if infoRaca and infoRaca.get("habilidades"):
            for hab_key in infoRaca["habilidades"]:
                def_hab = HABILIDADES_GERAIS.get(hab_key)
                if def_hab:
                    nova_hab = Habilidade(
                        nome=def_hab["nome"],
                        tipo=def_hab["tipo"],
                        descricao=def_hab["descricao"],
                        fonte=def_hab["fonte"]
                    )
                    if escolhas_salvas and nova_hab.nome in escolhas_salvas:
                        nova_hab.escolhas_aplicadas = escolhas_salvas[nova_hab.nome]

                    ficha.habilidades.append(nova_hab)


def aplicar_habilidades_classe(ficha: Personagem):
    for classe_info in ficha.classes:
        nome_classe = classe_info.nome
        nivel = classe_info.nivel

        for key, hab_data in DADOS_HABILIDADES_CLASSE.items():
            if hab_data.get('classe') == nome_classe and hab_data.get('tipo') == 'Habilidade de Classe':
                nivel_req = hab_data.get('nivel', 1)

                if nivel >= nivel_req:
                    if not any(h.nome == hab_data['nome'] for h in ficha.habilidades):
                        ficha.habilidades.append(Habilidade(
                            nome=hab_data['nome'],
                            tipo="Habilidade de Classe",
                            descricao=hab_data['descricao'],
                            fonte=f"{nome_classe} ({nivel_req})"
                        ))


def processar_escolhas_habilidades(ficha: Personagem):
    novos_poderes = []
    for hab in ficha.habilidades:
        escolhas = getattr(hab, "escolhas_aplicadas", None)
        if escolhas:
            for tipo, valor in escolhas.items():
                if not valor:
                    continue
                valor = str(valor)

                if "pericia" in tipo:
                    if valor in DADOS_PERICIAS:
                        if valor in ficha.pericias:
                            if "bonus" in tipo:
                                ficha.pericias[valor].outros += 2
                            else:
                                ficha.pericias[valor].treino = max(
                                    ficha.pericias[valor].treino, 1)
                        else:
                            attr = DADOS_PERICIAS.get(valor, 'int')
                            if "bonus" in tipo:
                                ficha.pericias[valor] = PericiaInfo(
                                    treino=0, atributo_chave=attr, outros=2)
                            else:
                                ficha.pericias[valor] = PericiaInfo(
                                    treino=1, atributo_chave=attr)

                if ("poder" in tipo) and (valor not in DADOS_PERICIAS):
                    def_poder = None
                    for k, v in HABILIDADES_GERAIS.items():
                        if v.get('nome') == valor:
                            def_poder = v
                            break

                    if def_poder:
                        if not any(h.nome == def_poder["nome"] for h in ficha.habilidades):
                            novos_poderes.append(Habilidade(
                                nome=def_poder["nome"],
                                tipo=def_poder["tipo"],
                                descricao=def_poder["descricao"],
                                fonte=f"Escolha ({hab.nome})"
                            ))
    ficha.habilidades.extend(novos_poderes)


def calcular_pericias(ficha: Personagem, metade_nivel: int, mods: dict, nivel_total: int):
    inicializar_pericias_fixas(ficha)
    for nome_pericia, attr_chave in DADOS_PERICIAS.items():
        if nome_pericia not in ficha.pericias:
            ficha.pericias[nome_pericia] = PericiaInfo(
                treino=0, atributo_chave=attr_chave)

        pericia = ficha.pericias[nome_pericia]
        pericia.atributo_chave = attr_chave
        mod_attr = mods.get(attr_chave, 0)
        bonus_nivel = metade_nivel if pericia.treino > 0 else 0
        bonus_treino = calcular_bonus_treino(pericia.treino, nivel_total)
        bonus_outros = pericia.outros + pericia.bonus_item

        pericia.total = bonus_nivel + mod_attr + bonus_treino + bonus_outros


def calcular_deslocamento(ficha: Personagem):
    detalhes = DetalhesDeslocamento()
    deslocamento_base = 9.0

    if ficha.cabecalho.raca in DADOS_RACAS:
        infoRaca = DADOS_RACAS[ficha.cabecalho.raca]
        if "habilidades" in infoRaca:
            for hab_key in infoRaca["habilidades"]:
                def_hab = HABILIDADES_GERAIS.get(hab_key)
                if def_hab and def_hab.get("efeitos"):
                    efeitos = def_hab["efeitos"]
                    if 'deslocamento' in efeitos:
                        deslocamento_base = efeitos['deslocamento']
                        break

    detalhes.base = deslocamento_base
    bonus_outros = 0
    detalhes.outros = bonus_outros

    ficha.status.deslocamento = max(0, deslocamento_base + bonus_outros)
    ficha.status.detalhes_deslocamento = detalhes


def atualizar_ficha(ficha: Personagem) -> Personagem:
    aplicar_dados_raciais(ficha)
    calcular_envelhecimento(ficha)

    escolhas_salvas = {}
    if ficha.habilidades:
        for h in ficha.habilidades:
            escolhas_atuais = getattr(h, "escolhas_aplicadas", None)
            if escolhas_atuais:
                escolhas_salvas[h.nome] = escolhas_atuais

    poderes_manuais = [h for h in ficha.habilidades if "Poder de" in h.tipo]
    ficha.habilidades = []

    aplicar_habilidades_raciais(ficha, escolhas_salvas)
    aplicar_origem(ficha)
    aplicar_habilidades_classe(ficha)

    ficha.habilidades.extend(poderes_manuais)

    mods = calcular_atributos_totais(ficha)

    # Agora passamos 'mods' para a função de efeitos
    pv_ini_bonus, pv_niv_bonus, pm_niv_bonus, pm_atributo_bonus = aplicar_habilidades_efeitos_numericos(
        ficha, mods)

    processar_escolhas_habilidades(ficha)

    nivel_total = sum([c.nivel for c in ficha.classes])
    if nivel_total < 1:
        nivel_total = 1
    ficha.cabecalho.nivel_total = nivel_total
    metade_nivel = math.floor(nivel_total / 2)

    # Passamos o bônus de atributo calculado para o cálculo de PM
    calcular_pv_pm(ficha, mods["con"], mods, pv_ini_bonus,
                   pv_niv_bonus, pm_niv_bonus, pm_atributo_bonus)
    calcular_deslocamento(ficha)
    calcular_pericias(ficha, metade_nivel, mods, nivel_total)

    defesa = ficha.status.defesa
    defesa.detalhes.des_mod = mods["des"]
    defesa.total = defesa.detalhes.base + defesa.detalhes.des_mod + \
        defesa.detalhes.armadura + defesa.detalhes.escudo + defesa.detalhes.outros

    maior_atributo_mental = max(mods["int"], mods["sab"], mods["car"])
    ficha.combate.cd_magias = 10 + metade_nivel + maior_atributo_mental

    forca_modificador = ficha.atributos.forca
    limite_carga = 10 + \
        (2 * forca_modificador) if forca_modificador >= 0 else 10 + \
        (1 * forca_modificador)
    ficha.inventario.carga_maxima = max(0, limite_carga)

    return ficha
