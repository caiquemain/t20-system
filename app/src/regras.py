import math
import logging
from typing import Optional, Dict
from .models import Personagem, Habilidade, Magia, PericiaInfo, TamanhoEnum, DetalhesCalculo, Ataque
from src.dados_racas import DADOS_RACAS
from src.dados_classes import DADOS_CLASSES
from src.dados_pericias import DADOS_PERICIAS
from src.dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from src.dados_habilidades import HABILIDADES_GERAIS
from src.dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from src.dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from .dados_magias import DADOS_MAGIAS

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RegrasT20")


def calcular_modificador(valor_atributo: int) -> int:
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
        # Mantém apenas poderes gerais comprados manualmente ou itens
        if hab.tipo in ["Racial", "Classe", "Origem", "Raça"]:
            continue
        habilidades_mantidas.append(hab)
    ficha.habilidades = habilidades_mantidas

    # GARANTIA EXTRA: Limpa as listas que dependem dessas habilidades
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
                    escolhas_anteriores = escolhas_preservadas.get(
                        nome_real, dados_hab.get("efeitos", {}))

                    nova_hab = Habilidade(
                        nome=nome_real,
                        tipo="Racial",
                        descricao=dados_hab.get("descricao", ""),
                        fonte=raca_nome,
                        escolhas_aplicadas=escolhas_anteriores,
                        efeitos=dados_hab.get("efeitos", {})
                    )
                    novas_habs.append(nova_hab)
                    nomes_existentes.add(nome_real)

    # --- APLICA O BLOQUEIO DE ORIGEM ---
    if bloquear_origem:
        if ficha.escolhas_origem:
            for escolha_antiga in ficha.escolhas_origem:
                if escolha_antiga in ficha.pericias:
                    ficha.pericias[escolha_antiga].treino = 0

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
                            escolhas_aplicadas=dados_hab.get("efeitos", {}),
                            efeitos=dados_hab.get("efeitos", {})
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
                efeitos_origem = dados_poder.get(
                    "efeitos", {}) if dados_poder else {}

                novas_habs.append(Habilidade(
                    nome=escolha,
                    tipo="Origem",
                    descricao=descricao,
                    fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=efeitos_origem,
                    efeitos=efeitos_origem
                ))
                nomes_existentes.add(escolha)

    if novas_habs:
        ficha.habilidades.extend(novas_habs)


def sincronizar_poderes_habilidades(ficha: Personagem):
    logger.info("--- [X] Sincronizando Poderes de Habilidades ---")

    poderes_permitidos = {}

    for hab in ficha.habilidades:
        escolhas = hab.escolhas_aplicadas or {}
        chaves_especificas = ["poder_geral", "poder_tormenta",
                              "poder_escolha", "habilidade_racial_escolha"]

        for chave in chaves_especificas:
            if chave in escolhas:
                val = escolhas[chave]
                if isinstance(val, str) and val:
                    poderes_permitidos[val] = hab.nome

        for chave, valor in escolhas.items():
            if (chave.startswith("poder_") or "_poder" in chave or "habilidade_" in chave) and chave not in chaves_especificas:
                if isinstance(valor, str) and valor:
                    poderes_permitidos[valor] = hab.nome

    ficha.habilidades = [
        h for h in ficha.habilidades
        if not (h.fonte and h.fonte.startswith("Habilidade:")) or h.nome in poderes_permitidos
    ]

    nomes_atuais = {h.nome for h in ficha.habilidades}
    novos_poderes = []

    for nome_poder, nome_origem in poderes_permitidos.items():
        if nome_poder not in nomes_atuais:
            dados = None
            tipo_encontrado = "Poder Extra"

            for v in DADOS_PODERES_TORMENTA.values():
                if v["nome"] == nome_poder:
                    dados = v
                    tipo_encontrado = "Poder da Tormenta"
                    break

            if not dados:
                for k, v in HABILIDADES_GERAIS.items():
                    if v["nome"] == nome_poder:
                        dados = v
                        tipo_encontrado = v.get("tipo", "Poder Geral")
                        break

            if not dados:
                for k, v in DADOS_HABILIDADES_RACIAIS.items():
                    if v["nome"] == nome_poder:
                        dados = v
                        tipo_encontrado = "Habilidade Racial (Memória Póstuma)"
                        break

            if dados:
                novo = Habilidade(
                    nome=dados["nome"],
                    tipo=tipo_encontrado,
                    descricao=dados["descricao"],
                    efeitos=dados.get("efeitos", {}),
                    fonte=f"Habilidade: {nome_origem}"
                )
                novos_poderes.append(novo)
                nomes_atuais.add(nome_poder)
                logger.info(
                    f"💪 Poder/Habilidade adicionado: {nome_poder} (via {nome_origem})")
            else:
                logger.warning(
                    f"⚠️ Item escolhido não encontrado no banco: {nome_poder}")

    if novos_poderes:
        ficha.habilidades.extend(novos_poderes)


def calcular_atributos_finais(ficha: Personagem):
    logger.info("--- [2.5] Calculando Atributos Finais ---")
    mapa_attr = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
                 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}

    for hab in ficha.habilidades:
        # CORREÇÃO: Mescla efeitos passivos com escolhas
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        mods = efeitos.get("atributo_bonus")

        if mods:
            for attr_short, valor in mods.items():
                attr_full = str(mapa_attr.get(attr_short, attr_short))

                if (hab.fonte == "Habilidade: Deformidade"
                    and attr_short == "car"
                        and valor < 0):
                    continue

                if hasattr(ficha.atributos, attr_full):
                    valor_atual = getattr(ficha.atributos, attr_full)
                    setattr(ficha.atributos, attr_full, valor_atual + valor)


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

    # Cálculo de Penalidade de Armadura
    penalidade_armadura_valor = 0
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if "penalidade_armadura" in efeitos:
            penalidade_armadura_valor += efeitos["penalidade_armadura"]

    pericias_extras_gratis = []
    bonus_numerico_habilidades = {}
    bonus_por_atributo = {}

    qtd_poderes_tormenta = 0
    for hab in ficha.habilidades:
        if "Tormenta" in hab.tipo:
            qtd_poderes_tormenta += 1

    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if hab.nome == "Deformidade":
            bonus_lefou = 2 + (2 * qtd_poderes_tormenta)
            p1 = efeitos.get("pericia_1")
            p2 = efeitos.get("pericia_2")
            if p1:
                bonus_numerico_habilidades[p1] = bonus_numerico_habilidades.get(
                    p1, 0) + bonus_lefou
            if p2:
                bonus_numerico_habilidades[p2] = bonus_numerico_habilidades.get(
                    p2, 0) + bonus_lefou
            continue

        for chave in ["pericia_1", "pericia_2", "pericia_escolha"]:
            val = efeitos.get(chave)
            if val and isinstance(val, str):
                pericias_extras_gratis.append(val)

        if "bonus_pericia" in efeitos:
            for pericia, valor in efeitos["bonus_pericia"].items():
                bonus_numerico_habilidades[pericia] = bonus_numerico_habilidades.get(
                    pericia, 0) + valor

        if "bonus_pericia_atributo" in efeitos:
            for attr, valor in efeitos["bonus_pericia_atributo"].items():
                bonus_por_atributo[attr] = bonus_por_atributo.get(
                    attr, 0) + valor

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

        # Somas dos Bônus
        bonus_fixo = bonus_numerico_habilidades.get(nome_pericia, 0)
        bonus_dinamico = bonus_por_atributo.get(attr_chave, 0)

        # Total vindo de habilidades (Automático)
        total_automatico = bonus_fixo + bonus_dinamico

        penalidade_aplicada = penalidade_armadura_valor if dados_base["penalidade_armadura"] else 0

        total = bonus_metade_nivel + mod_attr + \
            bonus_treino + info_atual.outros + total_automatico + penalidade_aplicada

        # Agora passamos direto no construtor, pois atualizamos o models.py
        novas_pericias[nome_pericia] = PericiaInfo(
            treino=nivel_treino,
            bonus_nivel=bonus_metade_nivel,
            atributo_valor=mod_attr,
            outros=info_atual.outros,
            total=total,
            bonus_automatico=total_automatico  # <--- Campo oficial agora
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

        # [NOVO] Variável para PM em níveis ímpares (Sangue Élfico)
        bonus_pm_nivel_impar = 0

        for hab in ficha.habilidades:
            efeitos = (hab.efeitos or {}).copy()
            if hab.escolhas_aplicadas:
                efeitos.update(hab.escolhas_aplicadas)

            if "pv_max_ini" in efeitos:
                bonus_pv_ini += efeitos["pv_max_ini"]
            if "pv_max_nivel" in efeitos:
                bonus_pv_nivel += efeitos["pv_max_nivel"]
            if "pm_max_nivel" in efeitos:
                bonus_pm_nivel += efeitos["pm_max_nivel"]

            # [NOVO] Lógica do Sangue Élfico
            if "pm_por_nivel_impar" in efeitos:
                bonus_pm_nivel_impar += efeitos["pm_por_nivel_impar"]

        pv_inicial = pv_ini_base + mod_con + bonus_pv_ini
        pv_nivel_total = 0
        niveis_primaria_para_somar = max(0, classe_primaria.nivel - 1)
        pv_nivel_total += niveis_primaria_para_somar * \
            (pv_niv_base + mod_con + bonus_pv_nivel)

        for c in ficha.classes[1:]:
            d_classe = DADOS_CLASSES.get(c.nome, {})
            val_niv = d_classe.get("pv_nivel", 0)
            pv_nivel_total += c.nivel * (val_niv + mod_con + bonus_pv_nivel)

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

        # [NOVO] Cálculo Matemático dos Ímpares (Nível 1=1, 2=1, 3=2, 4=2...)
        qtd_niveis_impares = math.ceil(ficha.cabecalho.nivel_total / 2)
        total_pm_impar = qtd_niveis_impares * bonus_pm_nivel_impar

        detalhes_pm = DetalhesCalculo(
            inicial=pm_inicial,
            nivel=pm_nivel_total,
            atributo=mod_attr_chave,
            # [NOVO] Somamos o total ímpar aqui
            habilidades=(bonus_pm_nivel *
                         ficha.cabecalho.nivel_total) + total_pm_impar,
            outros=0,
            total=pm_inicial + pm_nivel_total +
            (bonus_pm_nivel * ficha.cabecalho.nivel_total) + total_pm_impar
        )

        ficha.status.pv.maximo = detalhes_pv.total
        ficha.status.pv.calculo = detalhes_pv
        ficha.status.pm.maximo = detalhes_pm.total
        ficha.status.pm.calculo = detalhes_pm

        if ficha.status.pv.atual == 0:
            ficha.status.pv.atual = detalhes_pv.total
        if ficha.status.pm.atual == 0:
            ficha.status.pm.atual = detalhes_pm.total
        if ficha.status.pv.atual > detalhes_pv.total:
            ficha.status.pv.atual = detalhes_pv.total
        if ficha.status.pm.atual > detalhes_pm.total:
            ficha.status.pm.atual = detalhes_pm.total

    except Exception as e:
        logger.error(f"Erro ao calcular PV/PM: {e}")


def calcular_defesa_e_deslocamento(ficha: Personagem):
    logger.info("--- [5] Calculando Defesa e Deslocamento ---")
    mod_des = calcular_modificador(ficha.atributos.destreza)

    bonus_defesa = 0
    deslocamento_final = ficha.status.deslocamento

    # 1. Passivos
    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if "defesa_bonus" in efeitos:
            bonus_defesa += efeitos["defesa_bonus"]
        if "deslocamento" in efeitos:
            deslocamento_final = efeitos["deslocamento"]
        if hab.nome == "Esquiva":
            bonus_defesa += 2

    # 2. Buffs Ativos
    if hasattr(ficha.status, 'buffs') and ficha.status.buffs:
        for buff in ficha.status.buffs:
            atributo_alvo = buff.atributo.lower()
            if atributo_alvo == "defesa":
                bonus_defesa += buff.valor
                logger.info(
                    f"🛡️ Buff Aplicado na Defesa: {buff.origem} (+{buff.valor})")
            elif atributo_alvo == "deslocamento":
                deslocamento_final += buff.valor
                logger.info(
                    f"🦶 Buff Aplicado no Deslocamento: {buff.origem} (+{buff.valor})")

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
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

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
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if "resistencia_rd" in efeitos:
            for tipo, valor in efeitos["resistencia_rd"].items():
                lista_rd.append(f"{tipo} {valor}")

        escolha_rd = efeitos.get("resistencia_rd_escolha")
        if escolha_rd and isinstance(escolha_rd, str):
            lista_rd.append(f"{escolha_rd} 10")

    ficha.status.rd = lista_rd


# --- NOVA FUNÇÃO DE ATAQUES (PARA MINOTAURO E TROG) ---
def sincronizar_ataques(ficha: Personagem):
    logger.info("--- [5.3] Sincronizando Ataques (Armas Naturais) ---")

    # 1. Filtra ataques manuais do usuário (que não sejam de "Fonte: Racial")
    # Isso evita que a gente duplique o ataque "Chifres" toda vez que salvar
    ataques_mantidos = [
        a for a in ficha.combate.ataques if "Racial" not in a.tipo]

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}

        # Procura pela chave "arma_natural" no JSON da habilidade
        # Ex: "arma_natural": "Chifres 1d6"
        if "arma_natural" in efeitos:
            texto_arma = efeitos["arma_natural"]
            partes = texto_arma.split(" ", 1)  # Separa "Chifres" de "1d6"

            nome_arma = partes[0]
            dano_arma = partes[1] if len(partes) > 1 else "1d4"

            novo_ataque = Ataque(
                nome=nome_arma,
                bonus_ataque="+0",  # Será calculado no frontend com Força/BBA
                dano=dano_arma,
                critico="x2",
                tipo="Racial",  # Tag importante para filtro
                alcance="Curto"
            )
            ataques_mantidos.append(novo_ataque)
            logger.info(f"⚔️ Arma Natural Adicionada: {nome_arma}")

    ficha.combate.ataques = ataques_mantidos


def sincronizar_magias_habilidades(ficha: Personagem):
    logger.info("--- [X] Sincronizando Magias de Habilidades ---")
    magias_permitidas = {}

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        escolhas = hab.escolhas_aplicadas or {}

        config_magia = efeitos.get("magia_adicional_escolha")

        if config_magia:
            nomes_escolhidos = []
            if "magia_escolhida" in escolhas and isinstance(escolhas["magia_escolhida"], str):
                nomes_escolhidos.append(escolhas["magia_escolhida"])

            for chave, valor in escolhas.items():
                if (chave.startswith("magia_")
                    and chave != "magia_escolhida"
                    and chave != "magia_adicional_escolha"
                    and isinstance(valor, str)
                        and valor):
                    nomes_escolhidos.append(valor)

            attr_chave = config_magia.get("atributo", "")
            reducao = efeitos.get("reducao_custo_se_conhecida", 0)

            for nome_magia in nomes_escolhidos:
                if nome_magia and isinstance(nome_magia, str):
                    magias_permitidas[nome_magia] = {
                        "hab_nome": hab.nome,
                        "attr": attr_chave,
                        "reducao": reducao
                    }

        # Suporte para magias fixas (Ex: Amiga das Plantas - Controlar Plantas)
        magia_fixa = efeitos.get("magia_adicional")
        if magia_fixa:
            nome_magia = magia_fixa.get("nome")
            attr_chave = magia_fixa.get("atributo", "")
            if nome_magia:
                magias_permitidas[nome_magia] = {
                    "hab_nome": hab.nome,
                    "attr": attr_chave,
                    "reducao": efeitos.get("reducao_custo_magia", {}).get("valor", 0)
                }

    ficha.combate.magias = [
        m for m in ficha.combate.magias
        if not m.fonte.startswith("Habilidade:") or m.nome in magias_permitidas
    ]

    nomes_conhecidos = {m.nome for m in ficha.combate.magias}
    novas_magias = []

    for nome_magia, info in magias_permitidas.items():
        if nome_magia not in nomes_conhecidos:
            dados_magia = DADOS_MAGIAS.get(nome_magia)

            if dados_magia:
                nova = Magia(
                    nome=dados_magia["nome"],
                    circulo=dados_magia["circulo"],
                    escola=dados_magia.get("escola", ""),
                    execucao=dados_magia.get("execucao", ""),
                    alcance=dados_magia.get("alcance", ""),
                    alvo=dados_magia.get("alvo", ""),
                    duracao=dados_magia.get("duracao", ""),
                    resistencia=dados_magia.get("resistencia", ""),
                    descricao=dados_magia.get(
                        "descricao", "") or dados_magia.get("efeito", ""),
                    aprimoramentos=dados_magia.get("aprimoramentos", []),
                    efeito=dados_magia.get("efeito", ""),
                    custo_pm=max(1, dados_magia.get(
                        "custo", 1) - info["reducao"]),
                    atributo_chave=info["attr"],
                    fonte=f"Habilidade: {info['hab_nome']}"
                )
                novas_magias.append(nova)
                nomes_conhecidos.add(nome_magia)

    if novas_magias:
        ficha.combate.magias.extend(novas_magias)


def processar_acumulo_habilidades(ficha: Personagem):
    contagem_nomes = {}
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        ativavel = efeitos.get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            nome_chave = ativavel["nome_acumulo"]
            contagem_nomes[nome_chave] = contagem_nomes.get(nome_chave, 0) + 1

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        ativavel = efeitos.get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            nome_chave = ativavel["nome_acumulo"]
            if contagem_nomes.get(nome_chave, 0) >= 2:
                reducao = ativavel.get("reducao_se_acumular", 0)
                if reducao > 0:
                    custo_original = ativavel["custo"]
                    novo_custo = max(0, custo_original - reducao)
                    ativavel["custo"] = novo_custo
                    tag_reducao = f" [Custo reduzido por duplicata: {novo_custo} PM]"
                    if tag_reducao not in hab.descricao:
                        hab.descricao += tag_reducao


def atualizar_ficha(ficha: Personagem) -> Personagem:
    logger.info(f"🔄 INICIANDO ATUALIZAÇÃO: {ficha.cabecalho.nome}")

    escolhas_preservadas = {}
    for h in ficha.habilidades:
        if h.escolhas_aplicadas:
            escolhas_preservadas[h.nome] = h.escolhas_aplicadas

    # 1. Limpeza
    limpar_habilidades_fixas(ficha)

    # 2. Reconstrução Básica
    ficha.cabecalho.nivel_total = calcular_nivel_personagem(ficha)
    ficha = aplicar_bonus_atributos_raciais(ficha)

    # 3. Habilidades (Traz escolhas de volta)
    garantir_habilidades_iniciais(ficha, escolhas_preservadas)

    # 4. Sincronizações (Poderes e Magias)
    sincronizar_poderes_habilidades(ficha)
    sincronizar_magias_habilidades(ficha)
    processar_acumulo_habilidades(ficha)

    # 5. Cálculos com Atributos Finais
    calcular_atributos_finais(ficha)

    # 6. Derivados
    inicializar_pericias(ficha)
    calcular_pv_pm(ficha)
    calcular_defesa_e_deslocamento(ficha)
    calcular_proficiencias_e_sentidos(ficha)
    calcular_reducoes_dano(ficha)

    # 7. NOVOS DERIVADOS: Ataques
    sincronizar_ataques(ficha)  # <--- ADICIONADO AQUI

    logger.info("✅ Ficha atualizada com sucesso.")
    return ficha
