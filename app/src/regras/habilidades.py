import logging
from typing import Optional, Dict
from ..models import Personagem, Habilidade
from ..dados_racas import DADOS_RACAS
from ..dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from ..dados_habilidades import HABILIDADES_GERAIS
from ..dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from ..dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from ..dados_pericias import DADOS_PERICIAS
from ..dados_magias import DADOS_MAGIAS

logger = logging.getLogger("RegrasT20")


def limpar_habilidades_fixas(ficha: Personagem):
    """Remove habilidades de Raça, Classe e Origem antigas para recalcular."""
    habilidades_mantidas = []
    for hab in ficha.habilidades:
        if hab.tipo in ["Racial", "Classe", "Origem", "Raça"]:
            continue
        habilidades_mantidas.append(hab)
    ficha.habilidades = habilidades_mantidas
    ficha.proficiencias = []
    ficha.status.rd = []


def garantir_habilidades_iniciais(ficha: Personagem, escolhas_preservadas: Optional[Dict] = None):
    logger.info("--- [2] Garantindo Habilidades Iniciais ---")
    if escolhas_preservadas is None:
        escolhas_preservadas = {}

    nomes_existentes = {h.nome for h in ficha.habilidades}
    novas_habs = []

    # A. RACIAIS
    raca_nome = ficha.cabecalho.raca
    dados_raca = DADOS_RACAS.get(raca_nome)
    bloquear_origem = False

    if dados_raca and "habilidades" in dados_raca:
        for chave_hab in dados_raca["habilidades"]:
            dados_hab = DADOS_HABILIDADES_RACIAIS.get(
                chave_hab) or HABILIDADES_GERAIS.get(chave_hab)
            if dados_hab:
                if dados_hab.get("efeitos", {}).get("sem_origem"):
                    bloquear_origem = True

                nome_real = dados_hab["nome"]
                if nome_real not in nomes_existentes:
                    escolhas_anteriores = escolhas_preservadas.get(
                        nome_real, dados_hab.get("efeitos", {}))
                    novas_habs.append(Habilidade(
                        nome=nome_real, tipo="Racial", descricao=dados_hab.get("descricao", ""),
                        fonte=raca_nome, escolhas_aplicadas=escolhas_anteriores, efeitos=dados_hab.get(
                            "efeitos", {})
                    ))
                    nomes_existentes.add(nome_real)

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
                            nome=nome_hab, tipo="Classe", descricao=dados_hab.get("descricao", ""),
                            fonte=f"{classe.nome} ({nivel_req})", escolhas_aplicadas=dados_hab.get("efeitos", {}),
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
                dados_poder = next(
                    (v for k, v in HABILIDADES_GERAIS.items() if v["nome"] == escolha), None)
                descricao = dados_poder.get(
                    "descricao", "Benefício de Origem") if dados_poder else "Benefício único."
                efeitos_origem = dados_poder.get(
                    "efeitos", {}) if dados_poder else {}
                novas_habs.append(Habilidade(
                    nome=escolha, tipo="Origem", descricao=descricao, fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=efeitos_origem, efeitos=efeitos_origem
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
            if chave in escolhas and escolhas[chave]:
                poderes_permitidos[escolhas[chave]] = hab.nome

        for chave, valor in escolhas.items():
            if (chave.startswith("poder_") or "_poder" in chave or "habilidade_" in chave) and chave not in chaves_especificas:
                if isinstance(valor, str) and valor:
                    poderes_permitidos[valor] = hab.nome

    ficha.habilidades = [h for h in ficha.habilidades if not (
        h.fonte and h.fonte.startswith("Habilidade:")) or h.nome in poderes_permitidos]
    nomes_atuais = {h.nome for h in ficha.habilidades}
    novos_poderes = []

    for nome_poder, nome_origem in poderes_permitidos.items():
        if nome_poder not in nomes_atuais:
            dados = next((v for v in DADOS_PODERES_TORMENTA.values()
                         if v["nome"] == nome_poder), None)
            tipo_encontrado = "Poder da Tormenta"
            if not dados:
                dados = next((v for k, v in HABILIDADES_GERAIS.items()
                             if v["nome"] == nome_poder), None)
                tipo_encontrado = dados.get(
                    "tipo", "Poder Geral") if dados else "Poder Extra"
            if not dados:
                dados = next((v for k, v in DADOS_HABILIDADES_RACIAIS.items(
                ) if v["nome"] == nome_poder), None)
                tipo_encontrado = "Habilidade Racial (Memória Póstuma)"

            if dados:
                novos_poderes.append(Habilidade(
                    nome=dados["nome"], tipo=tipo_encontrado, descricao=dados["descricao"],
                    efeitos=dados.get("efeitos", {}), fonte=f"Habilidade: {nome_origem}"
                ))
                nomes_atuais.add(nome_poder)

    if novos_poderes:
        ficha.habilidades.extend(novos_poderes)


def processar_acumulo_habilidades(ficha: Personagem):
    contagem_nomes = {}
    for hab in ficha.habilidades:
        ativavel = (hab.efeitos or {}).get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            contagem_nomes[ativavel["nome_acumulo"]] = contagem_nomes.get(
                ativavel["nome_acumulo"], 0) + 1

    for hab in ficha.habilidades:
        ativavel = (hab.efeitos or {}).get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            if contagem_nomes.get(ativavel["nome_acumulo"], 0) >= 2:
                reducao = ativavel.get("reducao_se_acumular", 0)
                if reducao > 0:
                    custo_original = ativavel["custo"]
                    novo_custo = max(0, custo_original - reducao)
                    ativavel["custo"] = novo_custo
                    tag_reducao = f" [Custo reduzido por duplicata: {novo_custo} PM]"
                    if tag_reducao not in hab.descricao:
                        hab.descricao += tag_reducao


def atualizar_efeitos_ativos(ficha: Personagem):
    lista_efeitos = []
    for hab in ficha.habilidades:
        efeitos = (hab.efeitos or {}).copy()
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        if "magias_duradouras" in efeitos:
            for nome_magia in efeitos["magias_duradouras"]:
                dados_magia = next(
                    (m for m in DADOS_MAGIAS.values() if m.get("nome") == nome_magia), None)
                if dados_magia:
                    desc = dados_magia.get("descricao", "").rstrip('.')
                    lista_efeitos.append(f"✨ {nome_magia}: {desc}")
                else:
                    lista_efeitos.append(f"✨ {nome_magia}")

        if "imunidade" in efeitos:
            for imune in efeitos["imunidade"]:
                lista_efeitos.append(f"🛡️ Imune a {imune.capitalize()}")
        if "sentidos" in efeitos:
            for sentido in efeitos["sentidos"]:
                lista_efeitos.append(f"👁️ {sentido}")

    ficha.status.efeitos_ativos = sorted(list(set(lista_efeitos)))
