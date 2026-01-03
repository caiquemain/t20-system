import logging
from ..models import Personagem, Magia
from ..dados_magias import DADOS_MAGIAS

logger = logging.getLogger("RegrasT20")


def sincronizar_magias_habilidades(ficha: Personagem):
    logger.info("--- [X] Sincronizando Magias de Habilidades ---")
    magias_permitidas = {}

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        escolhas = hab.escolhas_aplicadas or {}

        # 1. Magia por Escolha (ex: Arcanista, Poder Mágico)
        config_magia = efeitos.get("magia_adicional_escolha")
        if config_magia:
            nomes_escolhidos = []
            if "magia_escolhida" in escolhas and isinstance(escolhas["magia_escolhida"], str):
                nomes_escolhidos.append(escolhas["magia_escolhida"])

            for k, v in escolhas.items():
                if k.startswith("magia_") and v and isinstance(v, str) and k not in ["magia_escolhida", "magia_adicional_escolha"]:
                    nomes_escolhidos.append(v)

            for nome in nomes_escolhidos:
                magias_permitidas[nome] = {
                    "hab_nome": hab.nome,
                    "attr": config_magia.get("atributo", ""),
                    "reducao": efeitos.get("reducao_custo_se_conhecida", 0),
                    "requisito": None
                }

        # 2. Magia Fixa (ex: Amiga das Plantas)
        magia_fixa = efeitos.get("magia_adicional")
        if magia_fixa and magia_fixa.get("nome"):
            magias_permitidas[magia_fixa["nome"]] = {
                "hab_nome": hab.nome,
                "attr": magia_fixa.get("atributo", ""),
                "reducao": efeitos.get("reducao_custo_magia", {}).get("valor", 0),
                "requisito": None
            }

        # 3. Lista de Magias Conhecidas (Racial: Sátiro, Qareen, Dahllan)
        if "magias_conhecidas" in efeitos:
            for nome in efeitos["magias_conhecidas"]:
                magias_permitidas[nome] = {
                    "hab_nome": hab.nome,
                    "attr": efeitos.get("atributo_magia_fixo", ""),
                    "reducao": 0,
                    "requisito": efeitos.get("requisito_magia")
                }

    # Limpeza: Remove magias de habilidade que não deveriam estar mais lá e preserva as manuais
    # CORREÇÃO PYLANCE: (m.fonte or "") garante que não chamaremos startswith em None
    ficha.combate.magias = [
        m for m in ficha.combate.magias
        if not str(m.fonte or "").startswith("Habilidade:") or m.nome in magias_permitidas
    ]

    nomes_conhecidos = {m.nome for m in ficha.combate.magias}
    novas_magias = []

    for nome_magia, info in magias_permitidas.items():
        if nome_magia not in nomes_conhecidos:
            dados = DADOS_MAGIAS.get(nome_magia)
            if dados:
                # Modifica textos se houver requisitos ou atributos fixos
                exec_txt = dados.get(
                    "execucao", "") + (f" (Req: {info['requisito']})" if info.get('requisito') else "")
                res_txt = dados.get(
                    "resistencia", "") + (f" (CD {info['attr'].upper()})" if info.get('attr') else "")

                nova = Magia(
                    nome=dados["nome"],
                    circulo=dados.get("circulo", 1),
                    escola=dados.get("escola", ""),
                    execucao=exec_txt,
                    alcance=dados.get("alcance", ""),
                    duracao=dados.get("duracao", ""),
                    resistencia=res_txt,
                    descricao=dados.get(
                        "descricao", "") or dados.get("efeito", ""),
                    custo_pm=max(1, dados.get("custo", 1) - info["reducao"]),
                    atributo_chave=info["attr"],
                    fonte=f"Habilidade: {info['hab_nome']}",
                    aprimoramentos=dados.get("aprimoramentos", [])
                )
                novas_magias.append(nova)
            else:
                # Fallback seguro
                novas_magias.append(Magia(
                    nome=nome_magia,
                    circulo=1,
                    descricao="Magia concedida por habilidade (dados não encontrados).",
                    custo_pm=1,
                    fonte=f"Habilidade: {info['hab_nome']}",
                    execucao=f"(Req: {info['requisito']})" if info.get(
                        'requisito') else "",
                    aprimoramentos=[]
                ))
            nomes_conhecidos.add(nome_magia)

    if novas_magias:
        ficha.combate.magias.extend(novas_magias)
