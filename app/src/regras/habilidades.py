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

def _sanitizar_escolhas_aplicadas(efeitos: Dict[str, Any], escolhas: Dict[str, Any]) -> Dict[str, Any]:
    """Remove gatilhos vazados de efeitos dentro de escolhas_aplicadas.

    Exemplo inválido:
      efeitos = {"pericia_escolha": 1}
      escolhas_aplicadas = {"pericia_escolha": 1}

    Exemplo válido:
      escolhas_aplicadas = {"pericia_escolha": "Diplomacia"}
    """
    limpas: Dict[str, Any] = {}
    for k, v in (escolhas or {}).items():
        # Remove valor idêntico ao gatilho do efeito.
        if k in efeitos and v == efeitos.get(k):
            continue

        # *_escolha só é escolha real se for string não vazia ou lista de strings não vazias.
        if k.endswith("_escolha"):
            if isinstance(v, str) and v.strip():
                limpas[k] = v
            elif isinstance(v, list):
                itens_validos = [x for x in v if isinstance(x, str) and x.strip()]
                if itens_validos:
                    limpas[k] = itens_validos
            continue

        # Preserva escolhas reais auxiliares: pericia_bonus_0, poder_ambicao_0 etc.
        if v is not None and v != "":
            limpas[k] = v

    return limpas


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

    # Classes atualmente ativas na ficha (incluindo classe base de variantes, ex.: Atleta -> Lutador)
    from ..dados_classes import DADOS_CLASSES
    from ..dados_variantes_herois import MAPA_VARIANTE_PARA_BASE
    classes_ativas = set()
    for c in (ficha.classes or []):
        cn = (c.nome or "").strip()
        if cn:
            classes_ativas.add(cn)
            if cn in MAPA_VARIANTE_PARA_BASE:
                classes_ativas.add(MAPA_VARIANTE_PARA_BASE[cn])

    # Índice reverso nome_poder -> conjunto de classes que o oferecem (para detectar poderes exclusivos)
    poderes_por_nome: Dict[str, set] = {}
    for _d_hc in DADOS_HABILIDADES_CLASSE.values():
        if isinstance(_d_hc, dict) and _d_hc.get("classe") and "Poder de" in (_d_hc.get("tipo") or ""):
            poderes_por_nome.setdefault(_d_hc["nome"], set()).add(_d_hc["classe"])

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
        if hab.tipo in ["Racial", "Classe", "Origem", "Raça", "Poder Racial", "Complicação", "Papel no Grupo", "Idade Variada"]:
            deletar = True
        elif is_sub_racial:
            deletar = True
        elif hab.fonte and ("Habilidade:" in hab.fonte or hab.fonte.startswith("Complicação:") or hab.fonte.startswith("Regra Opcional:")):
            deletar = True
        elif classes_ativas and not (hab.fonte or "").startswith(("Escolha:", "Origem")):
            # Poder exclusivo de uma classe que o personagem não possui mais
            tipo_hab = (hab.tipo or "").strip()
            if tipo_hab.startswith("Poder de "):
                classe_poder = tipo_hab[len("Poder de "):].strip()
                if classe_poder in DADOS_CLASSES and classe_poder not in classes_ativas:
                    deletar = True
            if not deletar and hab.nome in poderes_por_nome and hab.nome != "Aumento de Atributo":
                classes_do_poder = poderes_por_nome[hab.nome]
                if classes_do_poder and not (classes_do_poder & classes_ativas):
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
    # Reset tambem das listas derivadas para evitar duplicacao em reprocessamentos
    ficha.status.imunidades = []
    ficha.status.sentidos = []

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

                    # REGRA T20 (Versatil, p.19): no maximo 2 beneficios.
                    # Habilidades com 'pericia_ou_poder_escolha' permitem trocar
                    # 1 pericia por 1 poder geral. Quando o poder e escolhido,
                    # o slot de pericia flexivel (pericia_2) precisa ser descartado
                    # para nao somar 3 beneficios ao personagem.
                    if dados_hab.get("efeitos", {}).get("pericia_ou_poder_escolha"):
                        if escolhas_finais.get("poder_geral"):
                            escolhas_finais.pop("pericia_2", None)
                    # Resumo das escolhas aparece no card da habilidade
                    rotulos = {
                        "resistencia_rd_escolha": "Ascendência",
                        "imunidade_dano_escolha": "Espírito",
                        "pericia_escolha": "Perícia",
                        "pericia_bonus_0": "Bônus de perícia",
                        "memoria_postuma": "Memória",
                    }
                    partes = [f"{rot}: {escolhas_finais[k]}" for k, rot in rotulos.items()
                              if isinstance(escolhas_finais.get(k), str) and escolhas_finais[k]]
                    descricao_final = dados_hab.get("descricao", "")
                    if partes:
                        descricao_final += " ⭢ " + " • ".join(partes)

                    # Chave-espelho de EXIBIÇÃO: escolhas salvas na mesma chave
                    # do gatilho ficariam ocultas no chip do card (mecânica do
                    # card só mostra chaves que não existem em efeitos).
                    display_keys = {
                        "resistencia_rd_escolha": "ascendencia_elemental",
                        "imunidade_dano_escolha": "espirito_elemental",
                        "pericia_escolha": "pericia_treinada",
                    }
                    for src, dst in display_keys.items():
                        v = escolhas_finais.get(src)
                        if isinstance(v, str) and v:
                            escolhas_finais[dst] = v
                        else:
                            escolhas_finais.pop(dst, None)
                    novas_habs.append(Habilidade(
                        nome=nome_real,
                        tipo="Racial",
                        descricao=descricao_final,
                        fonte=raca_nome,
                        escolhas_aplicadas=_sanitizar_escolhas_aplicadas(dados_hab.get("efeitos", {}), escolhas_finais),
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
                    fonte_classe = f"{classe.nome} ({nivel_req})"
                    if nome_hab not in nomes_existentes:
                        esc_classe = dict(dados_hab.get("efeitos", {}))
                        if memoria_global.get(nome_hab):
                            esc_classe.update(memoria_global[nome_hab])
                        novas_habs.append(Habilidade(
                            nome=nome_hab, tipo="Classe", descricao=dados_hab.get("descricao", ""),
                            fonte=fonte_classe, escolhas_aplicadas=esc_classe,
                            efeitos=dict(dados_hab.get("efeitos", {}))
                        ))
                        nomes_existentes.add(nome_hab)
                    else:
                        existente = next(
                            (h for h in (*novas_habs, *ficha.habilidades) if h.nome == nome_hab),
                            None,
                        )
                        if existente and (existente.fonte or "") != fonte_classe:
                            efeitos_atual = dict(existente.efeitos or {})
                            efeitos_atual["_reaprendida"] = True
                            # Preserva bonus_pericia_se_duplicada caso só esteja na habilidade de classe
                            if "bonus_pericia_se_duplicada" in (dados_hab.get("efeitos") or {}):
                                efeitos_atual.setdefault(
                                    "bonus_pericia_se_duplicada",
                                    dict(dados_hab["efeitos"]["bonus_pericia_se_duplicada"]),
                                )
                            existente.efeitos = efeitos_atual
                            if fonte_classe not in (existente.fonte or ""):
                                existente.fonte = f"{existente.fonte} + {fonte_classe}" if existente.fonte else fonte_classe

    # C. ORIGEM (inclui poder_fixo de Amnésico e todas as Origens Regionais do Atlas de Arton)
    from ..dados_origens import DADOS_ORIGENS

    origem_nome = (ficha.cabecalho.origem or "").strip()
    dados_orig = DADOS_ORIGENS.get(origem_nome) or {}
    poder_fixo_origem = dados_orig.get("poder_fixo")

    # Remove poderes fixos de origens antigas caso o jogador tenha trocado de origem
    if ficha.habilidades:
        ficha.habilidades = [
            h for h in ficha.habilidades
            if not (
                (h.fonte or "").startswith("Origem: ")
                and (h.fonte or "") != f"Origem: {origem_nome}"
            )
        ]
        nomes_existentes = {h.nome for h in ficha.habilidades}

    if poder_fixo_origem and poder_fixo_origem not in nomes_existentes:
        dados_pf = next(
            (v for _, v in HABILIDADES_GERAIS.items() if v.get("nome") == poder_fixo_origem),
            None,
        )
        efeitos_pf = dict(dados_pf.get("efeitos", {})) if dados_pf else {}
        escolhas_pf = dict(efeitos_pf)
        if memoria_global and poder_fixo_origem in memoria_global:
            escolhas_pf.update(memoria_global[poder_fixo_origem])
        novas_habs.append(Habilidade(
            nome=poder_fixo_origem,
            tipo="Origem",
            descricao=dados_pf.get("descricao", "Benefício de Origem") if dados_pf else "Benefício único.",
            fonte=f"Origem: {origem_nome}",
            escolhas_aplicadas=escolhas_pf,
            efeitos=efeitos_pf,
        ))
        nomes_existentes.add(poder_fixo_origem)

    if ficha.escolhas_origem:
        for escolha in ficha.escolhas_origem:
            if escolha in DADOS_PERICIAS or escolha.startswith("Ofício"):
                continue
            if escolha not in nomes_existentes:
                dados_poder = next(
                    (v for k, v in HABILIDADES_GERAIS.items() if v["nome"] == escolha), None)
                efeitos_origem = dict(dados_poder.get(
                    "efeitos", {})) if dados_poder else {}
                escolhas_salvas = dict(efeitos_origem)
                if memoria_global and escolha in memoria_global:
                    escolhas_salvas.update(memoria_global[escolha])
                novas_habs.append(Habilidade(
                    nome=escolha, tipo="Origem",
                    descricao=dados_poder.get(
                        "descricao", "Benefício de Origem") if dados_poder else "Benefício único.",
                    fonte=f"Origem: {origem_nome}",
                    escolhas_aplicadas=escolhas_salvas,
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

        mp_val = escolhas.get("memoria_postuma")
        if isinstance(mp_val, str) and mp_val:
            poderes_permitidos[mp_val] = hab.nome
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
            if id_escolha not in nomes_atuais and id_escolha not in DADOS_PERICIAS and not id_escolha.startswith("Ofício"):
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

    from .escolhas_suplementos import processar_escolhas_suplementos
    processar_escolhas_suplementos(ficha)


def processar_acumulo_habilidades(ficha: Personagem):
    contagem_nomes: Dict[str, int] = {}
    contagem_por_nome: Dict[str, int] = {}
    for hab in ficha.habilidades:
        nome_norm = (hab.nome or "").strip().lower()
        if nome_norm:
            contagem_por_nome[nome_norm] = contagem_por_nome.get(nome_norm, 0) + 1
        ativavel = (hab.efeitos or {}).get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            chave = ativavel["nome_acumulo"]
            contagem_nomes[chave] = contagem_nomes.get(chave, 0) + 1

    duplicadas_bonificadas = set()

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        nome_norm = (hab.nome or "").strip().lower()
        reaprendida = bool(efeitos.get("_reaprendida"))

        # 1. Redução de custo PM em habilidade ativável acumulada (ex.: Kliren + Inventor)
        ativavel = efeitos.get("habilidade_ativavel")
        if ativavel and "nome_acumulo" in ativavel:
            chave = ativavel["nome_acumulo"]
            acumulou = reaprendida or contagem_nomes.get(chave, 0) >= 2 or contagem_por_nome.get(chave.lower(), 0) >= 2
            if acumulou:
                reducao = ativavel.get("reducao_se_acumular", 0)
                if reducao > 0 and "[Custo reduzido por duplicata:" not in (hab.descricao or ""):
                    efeitos_copia = dict(efeitos)
                    ativavel_copia = dict(ativavel)
                    custo_original = ativavel_copia["custo"]
                    novo_custo = max(0, custo_original - reducao)
                    ativavel_copia["custo"] = novo_custo
                    efeitos_copia["habilidade_ativavel"] = ativavel_copia
                    hab.efeitos = efeitos_copia
                    hab.descricao = (hab.descricao or "") + f" [Custo reduzido por duplicata: {novo_custo} PM]"

        # 2. Bônus de perícia por reaprendizado (ex.: Dahllan + Druida em Empatia Selvagem -> +2 Adestramento)
        efeitos = hab.efeitos or {}
        bonus_dup = efeitos.get("bonus_pericia_se_duplicada")
        if isinstance(bonus_dup, dict) and bonus_dup and nome_norm not in duplicadas_bonificadas:
            if reaprendida or contagem_por_nome.get(nome_norm, 0) >= 2:
                efeitos_copia = dict(efeitos)
                bonus_pericia = dict(efeitos_copia.get("bonus_pericia") or {})
                resumo_partes = []
                for pericia_nome, val in bonus_dup.items():
                    if isinstance(pericia_nome, str) and isinstance(val, (int, float)):
                        bonus_pericia[pericia_nome] = bonus_pericia.get(pericia_nome, 0) + int(val)
                        resumo_partes.append(f"+{int(val)} {pericia_nome}")
                efeitos_copia["bonus_pericia"] = bonus_pericia
                hab.efeitos = efeitos_copia
                duplicadas_bonificadas.add(nome_norm)
                if resumo_partes:
                    tag_reap = f" [Reaprendida: {', '.join(resumo_partes)}]"
                    if tag_reap not in (hab.descricao or ""):
                        hab.descricao = (hab.descricao or "") + tag_reap


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
                    lista_efeitos.append(f"{nome_magia}: {desc}")
                else:
                    lista_efeitos.append(f"{nome_magia}")

        if "imunidade" in efeitos:
            for imune in efeitos["imunidade"]:
                lista_efeitos.append(f"Imune a {imune.capitalize()}")
        if "sentidos" in efeitos:
            for sentido in efeitos["sentidos"]:
                lista_efeitos.append(f"{sentido}")
        rd_esc = efeitos.get("resistencia_rd_escolha")
        if isinstance(rd_esc, str) and rd_esc:
            lista_efeitos.append(f"RD 10 a {rd_esc} (ascendência)")
        imn_esc = efeitos.get("imunidade_dano_escolha")
        if isinstance(imn_esc, str) and imn_esc:
            lista_efeitos.append(f"Imune a {imn_esc} (fonte elemental)")
        if efeitos.get("resistencia_tormenta"):
            lista_efeitos.append(f"+{efeitos['resistencia_tormenta']} em resistências vs Tormenta/lefeu")
        if efeitos.get("resistencia_veneno"):
            lista_efeitos.append(f"+{efeitos['resistencia_veneno']} em resistências contra veneno")
        if efeitos.get("deslocamento_escalada_igual"):
            lista_efeitos.append(f"Deslocamento de escalada: {ficha.status.deslocamento}m")
        if efeitos.get("tipo_criatura"):
            lista_efeitos.append(f"Tipo de criatura: {efeitos['tipo_criatura']}")
        ba = efeitos.get("bonus_ataque_arma") or {}
        for vv in sorted(set(ba.values())):
            armas = ", ".join(k for k, v in ba.items() if v == vv)
            lista_efeitos.append(f"+{vv} ataque com: {armas}")
        bd = efeitos.get("bonus_dano_arma") or {}
        for vv in sorted(set(bd.values())):
            armas = ", ".join(k for k, v in bd.items() if v == vv)
            lista_efeitos.append(f"+{vv} dano com: {armas}")
        if efeitos.get("dano_arma_base"):
            lista_efeitos.append("Dano de arremesso/funda aumentado em 1 passo")
        if efeitos.get("furia_arremesso"):
            lista_efeitos.append("Fúria aplica bônus em ataque e dano também a armas de arremesso")
        if efeitos.get("inspiracao_aplica_dano"):
            lista_efeitos.append("Inspiração aplica bônus também em rolagens de dano (Inspiração Marcial)")
        if efeitos.get("cd_bardo_inspiracao"):
            lista_efeitos.append(f"+{efeitos['cd_bardo_inspiracao']} na CD de habilidades de bardo sob Inspiração (Arte Mágica)")
        if efeitos.get("artista_completo"):
            lista_efeitos.append("Inspiração como ação livre; custo em PM pela metade sob Inspiração (Artista Completo)")
        if efeitos.get("estrelato_bonus_carisma"):
            lista_efeitos.append(f"+{efeitos['estrelato_bonus_carisma']} em perícias de Carisma ao impressionar plateia (Estrelato)")
        if efeitos.get("golpe_magico_pm_temp"):
            lista_efeitos.append(f"+{efeitos['golpe_magico_pm_temp']} PM temporários ao acertar corpo a corpo sob Inspiração (Golpe Mágico)")
        vps = efeitos.get("vantagem_pericia_situacional")
        if isinstance(vps, dict) and vps:
            pares = ", ".join(f"{k} ({v})" for k, v in vps.items())
            lista_efeitos.append(f"Rola 2 dados e usa o melhor em: {pares}")
        if efeitos.get("evasao_aprimorada"):
            lista_efeitos.append("Evasão Aprimorada: sem dano ao passar em Reflexos; metade ao falhar")
        elif efeitos.get("evasao"):
            lista_efeitos.append("Evasão: sem dano ao passar em Reflexos para metade")
        if efeitos.get("panache_recupera_pm"):
            lista_efeitos.append(f"Panache: recupera {efeitos['panache_recupera_pm']} PM em crítico ou ao reduzir inimigo a 0 PV")
        if efeitos.get("sorte_de_nimb"):
            lista_efeitos.append("Sorte de Nimb: 5 PM para rolar teste novamente (11+ vira 20 natural)")
        if efeitos.get("pernas_do_mar"):
            lista_efeitos.append("Pernas do Mar: não fica desprevenido nem reduz deslocamento equilibrando/escalando")
        if efeitos.get("presenca_paralisante"):
            lista_efeitos.append("Presença Paralisante: ação padrão extra na 1ª rodada se for o primeiro na iniciativa")
        if efeitos.get("grudar_o_cano"):
            lista_efeitos.append("Grudar o Cano: sem penalidade de -5 e +1 passo de dano com arma de fogo contra adjacente")
        if efeitos.get("abusar_dos_fracos_passo_dano"):
            lista_efeitos.append("Abusar dos Fracos: +1 passo de dano contra criatura sob condição de medo")
        if efeitos.get("foliao_bonus_carisma"):
            lista_efeitos.append(f"Folião: +{efeitos['foliao_bonus_carisma']} em perícias de Carisma e +1 atitude em festas/tavernas")
        if efeitos.get("rastreador_sem_penalidade"):
            lista_efeitos.append("Rastreador: deslocamento normal enquanto rastreia sem penalidade")
        if efeitos.get("caminho_do_explorador"):
            lista_efeitos.append("Caminho do Explorador: ignora terreno difícil e +10 CD para rastreá-lo no terreno escolhido")
        if efeitos.get("mestre_cacador"):
            lista_efeitos.append("Mestre Caçador: Marca da Presa ação livre; recupera 5 PM ao abater criatura marcada")
        if efeitos.get("armadilheiro_soma_sab"):
            lista_efeitos.append("Armadilheiro: soma Sabedoria no dano e na CD das armadilhas")
        if efeitos.get("espreitar_marca_presa"):
            lista_efeitos.append("Espreitar: +1 em perícias contra criatura marcada (+1 por PM extra; dobra com Inimigo)")
        if efeitos.get("ponto_fraco_margem"):
            lista_efeitos.append(f"Ponto Fraco: +{efeitos['ponto_fraco_margem']} margem de ameaça contra criatura marcada (dobra com Inimigo)")
        if efeitos.get("marca_presa_alcance") == "Longo":
            lista_efeitos.append("Olho do Falcão: usa Marca da Presa em alcance longo")
        if efeitos.get("codigo_de_honra"):
            lista_efeitos.append("Código de Honra: não pode flanquear nem atacar caído/desprevenido/incapaz")
        if efeitos.get("resoluto"):
            lista_efeitos.append("Resoluto: 1 PM para refazer resistência contra condição com +5")
        if efeitos.get("bravura_final"):
            lista_efeitos.append("Bravura Final: 3 PM (sustentada) para continuar de pé com 0 ou menos PV")
        if efeitos.get("rd_condicional_covardes"):
            lista_efeitos.append(f"Desprezar os Covardes: RD {efeitos['rd_condicional_covardes']} se caído, desprevenido ou flanqueado")
        if efeitos.get("montaria_corajosa_dano"):
            lista_efeitos.append(f"Montaria Corajosa: +{efeitos['montaria_corajosa_dano']} em dano corpo a corpo montado")
        if efeitos.get("armadura_honra_pv_temp"):
            lista_efeitos.append("Armadura da Honra: PV temporários (Nível + Car) no início de cada cena")
        if efeitos.get("estandarte_pm_temp"):
            lista_efeitos.append("Estandarte: você e aliados recebem PM temporários (Car, mín 1) no início da cena")
        if efeitos.get("mao_da_divindade"):
            lista_efeitos.append("Mão da Divindade: 15 PM para lançar 3 magias divinas quaisquer como ação livre (atordoado 1d4 rodadas)")
        if efeitos.get("autoridade_eclesiastica"):
            lista_efeitos.append("Autoridade Eclesiástica: +5 Diplomacia/Intimidação com devotos e metade do preço em templos da divindade")
        if efeitos.get("mestre_celebrante"):
            lista_efeitos.append("Mestre Celebrante: Missas afetam 10x mais pessoas e dobram seus benefícios")
        if efeitos.get("comunhao_vital"):
            lista_efeitos.append("Comunhão Vital: +2 PM em magia de cura para curar metade em outro alvo em alcance curto")
        if efeitos.get("prece_de_combate"):
            lista_efeitos.append("Prece de Combate: +2 PM para lançar magia divina (padrão) em si mesmo como ação de movimento")
        if efeitos.get("magia_sagrada_profana"):
            lista_efeitos.append("Magia Sagrada/Profana: +1 PM para mudar dano de magia divina para luz ou trevas")
        if efeitos.get("imunidade_terreno_dificil_natural"):
            lista_efeitos.append("Caminho dos Ermos: ignora terreno difícil e +10 CD para rastreá-lo em terrenos naturais")
        if efeitos.get("forca_da_natureza"):
            lista_efeitos.append("Força da Natureza: -2 PM e +2 CD em magias (-4 PM e +4 CD em terrenos naturais)")
        if efeitos.get("bonus_dano_dado_frio"):
            lista_efeitos.append(f"Aspecto do Inverno: +{efeitos['bonus_dano_dado_frio']} dano por dado em magias de frio")
        if efeitos.get("veneno_cd_bonus"):
            lista_efeitos.append(f"Coração da Selva: +{efeitos['veneno_cd_bonus']} CD e +{efeitos.get('veneno_dano_por_dado', 1)} perda de vida/dado em venenos")
        if efeitos.get("magia_em_forma_selvagem"):
            lista_efeitos.append("Magia Natural: lança magias e empunha catalisadores/esotéricos em forma selvagem")
        if efeitos.get("armas_naturais_margem_ameaca"):
            lista_efeitos.append(f"Presas Afiadas: +{efeitos['armas_naturais_margem_ameaca']} margem de ameaça em armas naturais")
        if efeitos.get("forma_primal"):
            lista_efeitos.append("Forma Primal: combina benefícios de dois tipos de animais na Forma Selvagem")
        if efeitos.get("durao"):
            lista_efeitos.append("Durão: 3 PM ao sofrer dano para reduzir à metade")
        if efeitos.get("ataque_extra"):
            lista_efeitos.append("Ataque Extra: 2 PM ao agredir para 1 ataque adicional (1x/rodada)")
        if efeitos.get("campeao"):
            lista_efeitos.append("Campeão: +1 passo de dano em todos os ataques; recupera metade dos PM em Ataque Especial/Golpe Pessoal")
        if efeitos.get("destruidor_rerrolar_1_2"):
            lista_efeitos.append("Destruidor: rola novamente 1 ou 2 no dano com armas corpo a corpo de duas mãos")
        if efeitos.get("valentao_bonus"):
            lista_efeitos.append(f"Valentão: +{efeitos['valentao_bonus']} ataque e dano contra caídos, desprevenidos, flanqueados ou indefesos")
        if efeitos.get("romper_resistencias_rd"):
            lista_efeitos.append(f"Romper Resistências: +1 PM no Ataque Especial para ignorar {efeitos['romper_resistencias_rd']} de RD")
        if efeitos.get("golpe_de_raspao"):
            lista_efeitos.append("Golpe de Raspão: 2 PM ao errar ataque para causar metade do dano (1x/rodada)")
        if efeitos.get("comerciante_venda_pct"):
            lista_efeitos.append(f"Comerciante: vende itens {efeitos['comerciante_venda_pct']}% mais caro")
        if efeitos.get("olho_do_dragao"):
            lista_efeitos.append("Olho do Dragão: ação completa para identificar automaticamente item mágico")
        if efeitos.get("obra_prima"):
            lista_efeitos.append("Obra-Prima: item único (~5 melhorias e 4 encantos) sem custo")
        if efeitos.get("alquimista_batalha_soma_int"):
            lista_efeitos.append("Alquimista de Batalha: soma Inteligência no dano de alquímicos e poções")
        if efeitos.get("cano_raiado_margem"):
            lista_efeitos.append(f"Cano Raiado: +{efeitos['cano_raiado_margem']} margem de ameaça em arma de disparo fabricada por você")
        if efeitos.get("ferreiro_passo_dano"):
            lista_efeitos.append("Ferreiro: +1 passo de dano em arma corpo a corpo fabricada por você")
        if efeitos.get("granadeiro_alcance_medio"):
            lista_efeitos.append("Granadeiro: arremessa alquímicos/poções em alcance médio e usa Int na CD")
        if efeitos.get("mestre_cuca_bonus"):
            lista_efeitos.append(f"Mestre Cuca: +{efeitos['mestre_cuca_bonus']} no bônus numérico das comidas cozinhadas")
        if efeitos.get("sintese_rapida_dobro_doses"):
            lista_efeitos.append("Síntese Rápida: fabrica o dobro de doses de alquímico/poção no mesmo tempo")
        if efeitos.get("pessoa_certa_trabalho"):
            lista_efeitos.append("A Pessoa Certa para o Trabalho: 5 PM para +10 em ataque furtivo ou perícia de ladino")
        if efeitos.get("sombra_furtividade"):
            lista_efeitos.append("Sombra: sem penalidade de Furtividade ao mover normal; -10 para ações chamativas")
        if efeitos.get("gatuno_escalar"):
            lista_efeitos.append("Gatuno: não fica desprevenido e escala com deslocamento normal")
        if efeitos.get("escapista_bonus"):
            lista_efeitos.append(f"Escapista: +{efeitos['escapista_bonus']} em Acrobacia para escapar/passar e contra efeitos de movimento")
        if efeitos.get("saqueador_tumbas_bonus"):
            lista_efeitos.append(f"Saqueador de Tumbas: +{efeitos['saqueador_tumbas_bonus']} contra armadilhas; desabilita com ação padrão")
        if efeitos.get("veneno_duracao_ataques"):
            lista_efeitos.append(f"Veneno Persistente: veneno aplicado dura {efeitos['veneno_duracao_ataques']} ataques")
        if efeitos.get("mao_na_boca_agarrar"):
            lista_efeitos.append(f"Mão na Boca: +{efeitos['mao_na_boca_agarrar']} em agarrar; agarrar ação livre após ataque furtivo em desprevenido")
        if efeitos.get("dono_da_rua"):
            lista_efeitos.append("Dono da Rua: dano desarmado 2d10; ação agredir desarmada faz 2 ataques")
        if efeitos.get("resistencia_medo_mental"):
            lista_efeitos.append(f"Convencido: +{efeitos['resistencia_medo_mental']} em resistências contra medo e efeitos mentais")
        if efeitos.get("desarmado_ignora_rd"):
            lista_efeitos.append(f"Punhos de Adamante: ataques desarmados ignoram {efeitos['desarmado_ignora_rd']} de RD")
        if efeitos.get("lutador_chao_manobra"):
            lista_efeitos.append(f"Lutador de Chão: +{efeitos['lutador_chao_manobra']} para agarrar e derrubar; 1 PM derrubar livre")
        if efeitos.get("desarmado_soma_con_dano"):
            lista_efeitos.append("Trincado: soma Constituição nas rolagens de dano desarmado")
        if efeitos.get("ate_acertar_bonus"):
            lista_efeitos.append(f"Até Acertar: +{efeitos['ate_acertar_bonus']} cumulativo em ataque/dano desarmado ao errar")
        if efeitos.get("realeza"):
            lista_efeitos.append("Realeza: +5 CD Presença Aristocrática; inimigos reduzidos a 0 PV por Palavras Afiadas lutam ao seu lado")
        if efeitos.get("voz_poderosa_alcance"):
            lista_efeitos.append("Voz Poderosa: habilidades de nobre de alcance curto passam para alcance médio")
        if efeitos.get("presenca_majestosa"):
            lista_efeitos.append("Presença Majestosa: Presença Aristocrática afeta qualquer criatura com Int e mais de 1x/cena")
        if efeitos.get("lingua_rapida_penalidade"):
            lista_efeitos.append("Língua Rápida: mudar atitude como ação completa sofre -5 em vez de -10")
        if efeitos.get("general_pm_temp"):
            lista_efeitos.append(f"General: aliados direcionados por Estrategista recebem {efeitos['general_pm_temp']} PM temporários")

    ficha.status.efeitos_ativos = sorted(list(set(lista_efeitos)))


def sincronizar_escolhas_de_caminho(ficha: Personagem) -> Personagem:
    """Grava a subclasse atual na habilidade de Caminho (ex.: Caminho do Arcanista),
    para o frontend exibir a escolha como chip (padrão 'Aumento de Atributo').
    Também limpa gatilhos vazados de saves antigos (escolha_subclasse)."""
    if not ficha.classes:
        return ficha
    subclasse = ficha.classes[0].subclasse or ""
    for h in ficha.habilidades:
        efeitos = h.efeitos or {}
        if efeitos.get("escolha_subclasse"):
            escolhas = dict(h.escolhas_aplicadas or {})
            escolhas.pop("escolha_subclasse", None)  # limpa poluição antiga
            escolhas["subclasse"] = subclasse
            h.escolhas_aplicadas = escolhas
    return ficha
