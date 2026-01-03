import logging
from typing import Optional, Dict, List, Any
from ..models import Personagem, Habilidade
from ..dados_racas import DADOS_RACAS
from ..dados_habilidades_classe import DADOS_HABILIDADES_CLASSE
from ..dados_habilidades import HABILIDADES_GERAIS
from ..dados_habilidades_raciais import DADOS_HABILIDADES_RACIAIS
from ..dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from ..dados_pericias import DADOS_PERICIAS
from ..dados_magias import DADOS_MAGIAS

logger = logging.getLogger("RegrasT20")

# Lista de IDs ou partes de nomes que identificam sub-habilidades do Duende/Sátiro
PALAVRAS_CHAVE_SUB_RACIAIS = [
    "Natureza", "Tamanho", "Afinidade", "Encantar", "Enfeitiçar",
    "Invisibilidade", "Língua", "Maldição", "Mais Lá", "Metamorfose",
    "Sonhos", "Velocidade", "Visão", "Voo", "Tabu", "Chifres", "Marrada"
]


def limpar_habilidades_fixas(ficha: Personagem) -> Dict[str, Dict]:
    """
    Remove habilidades derivadas para recalcular.
    Retorna um dicionário com as 'escolhas internas' preservadas.
    """
    habilidades_mantidas = []
    memoria_escolhas = {}

    for hab in ficha.habilidades:
        deletar = False

        # 1. Identifica se é sub-habilidade racial
        is_sub_racial = False
        if "_" in hab.nome or any(k in hab.nome for k in PALAVRAS_CHAVE_SUB_RACIAIS):
            for id_db, dados_db in DADOS_HABILIDADES_RACIAIS.items():
                if hab.nome == dados_db["nome"] or hab.nome == id_db:
                    is_sub_racial = True
                    break

        # 2. Critérios de Remoção
        if hab.tipo in ["Racial", "Classe", "Origem", "Raça", "Poder Racial"]:
            deletar = True
        elif is_sub_racial:
            deletar = True
        elif hab.fonte and "Habilidade:" in hab.fonte:
            deletar = True

        if deletar:
            if hab.escolhas_aplicadas:
                memoria_escolhas[hab.nome] = hab.escolhas_aplicadas
                for k, v in DADOS_HABILIDADES_RACIAIS.items():
                    if v["nome"] == hab.nome:
                        memoria_escolhas[k] = hab.escolhas_aplicadas
        else:
            habilidades_mantidas.append(hab)

    ficha.habilidades = habilidades_mantidas
    ficha.proficiencias = []
    ficha.status.rd = []

    return memoria_escolhas


def garantir_habilidades_iniciais(ficha: Personagem, memoria_global: Optional[Dict] = None):
    logger.info("--- [2] Garantindo Habilidades Iniciais ---")
    if memoria_global is None:
        memoria_global = {}

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
                    # CORREÇÃO PYLANCE: Garante que é dict com "or {}"
                    escolhas_anteriores = memoria_global.get(
                        nome_real, memoria_global.get(chave_hab, {})) or {}

                    escolhas_finais = {
                        **dados_hab.get("efeitos", {}), **escolhas_anteriores}

                    novas_habs.append(Habilidade(
                        nome=nome_real,
                        tipo="Racial",
                        descricao=dados_hab.get("descricao", ""),
                        fonte=raca_nome,
                        escolhas_aplicadas=escolhas_finais,
                        efeitos=dados_hab.get("efeitos", {})
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
                efeitos_origem = dados_poder.get(
                    "efeitos", {}) if dados_poder else {}
                novas_habs.append(Habilidade(
                    nome=escolha, tipo="Origem",
                    descricao=dados_poder.get(
                        "descricao", "Benefício de Origem") if dados_poder else "Benefício único.",
                    fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=efeitos_origem,
                    efeitos=efeitos_origem
                ))
                nomes_existentes.add(escolha)

    if novas_habs:
        ficha.habilidades.extend(novas_habs)


def sincronizar_poderes_habilidades(ficha: Personagem, memoria_global: Optional[Dict] = None):
    logger.info("--- [X] Sincronizando Sub-Poderes (Filhos) ---")
    if memoria_global is None:
        memoria_global = {}
    poderes_permitidos = {}

    # 1. Varre as habilidades PAI
    for hab in ficha.habilidades:
        escolhas = hab.escolhas_aplicadas or {}
        chaves_de_busca = ["poder_geral", "poder_tormenta",
                           "poder_escolha", "habilidade_racial_escolha"]

        for chave in chaves_de_busca:
            if chave in escolhas:
                val = escolhas[chave]
                if isinstance(val, list):
                    for v in val:
                        if isinstance(v, str) and v:
                            poderes_permitidos[v] = hab.nome
                elif isinstance(val, str) and val:
                    poderes_permitidos[val] = hab.nome

        for chave, valor in escolhas.items():
            if (chave.startswith("poder_") or "_poder" in chave or "habilidade_" in chave) and chave not in chaves_de_busca:
                if isinstance(valor, str) and valor:
                    poderes_permitidos[valor] = hab.nome
                elif isinstance(valor, list):
                    for v in valor:
                        if isinstance(v, str) and v:
                            poderes_permitidos[v] = hab.nome

    # 2. Reconstrução
    nomes_atuais = {h.nome for h in ficha.habilidades}
    novos_poderes = []

    for id_escolha, nome_origem in poderes_permitidos.items():
        dados = None
        tipo_encontrado = "Poder Geral"

        # A. Prioridade Absoluta: Habilidades Raciais (Pelo ID)
        if id_escolha in DADOS_HABILIDADES_RACIAIS:
            dados = DADOS_HABILIDADES_RACIAIS[id_escolha]
            tipo_encontrado = "Racial"

        # B. Busca em Tormenta
        if not dados:
            for v in DADOS_PODERES_TORMENTA.values():
                if v["nome"] == id_escolha:
                    dados = v
                    tipo_encontrado = "Poder da Tormenta"
                    break

        # C. Busca em Gerais
        if not dados:
            for k, v in HABILIDADES_GERAIS.items():
                if v["nome"] == id_escolha:
                    dados = v
                    tipo_encontrado = v.get("tipo", "Poder Geral")
                    break

        # D. Fallback: Busca reversa por Nome
        if not dados:
            for k, v in DADOS_HABILIDADES_RACIAIS.items():
                if v["nome"] == id_escolha:
                    dados = v
                    tipo_encontrado = "Racial"
                    break

        # Criação da Habilidade
        if dados:
            nome_real = dados["nome"]
            if nome_real not in nomes_atuais:
                # CORREÇÃO PYLANCE: Garante dict com "or {}"
                escolhas_recuperadas = memoria_global.get(
                    nome_real, memoria_global.get(id_escolha, {})) or {}

                novos_poderes.append(Habilidade(
                    nome=nome_real,
                    tipo=tipo_encontrado,
                    descricao=dados.get("descricao", ""),
                    efeitos=dados.get("efeitos", {}),
                    fonte=f"Habilidade: {nome_origem}",
                    escolhas_aplicadas=escolhas_recuperadas
                ))
                nomes_atuais.add(nome_real)
        else:
            if id_escolha not in nomes_atuais:
                nome_formatado = id_escolha.replace(
                    "_", " ").title() if "_" in id_escolha else id_escolha
                novos_poderes.append(Habilidade(
                    nome=nome_formatado,
                    tipo="Poder Extra",
                    descricao="Habilidade selecionada.",
                    fonte=f"Habilidade: {nome_origem}"
                ))

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
            from ..dados_magias import DADOS_MAGIAS
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
