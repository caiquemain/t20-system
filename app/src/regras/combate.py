import logging
from ..models import Personagem, Ataque
from ..dados_classes import DADOS_CLASSES

logger = logging.getLogger("RegrasT20")


def calcular_proficiencias_e_sentidos(ficha: Personagem):
    logger.info("--- [5.1] Proficiências ---")
    lista = set()
    for c in ficha.classes:
        for p in DADOS_CLASSES.get(c.nome, {}).get("proficiencias", []):
            lista.add(p)

    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)
        if efeitos.get("visao_escuro"):
            lista.add("Visão no Escuro")
        if efeitos.get("visao_penumbra"):
            lista.add("Visão na Penumbra")
        if efeitos.get("sentido") == "Faro":
            lista.add("Faro")
        for k in ["proficiencia_armas", "proficiencia_simples"]:
            for p in efeitos.get(k, []):
                lista.add(p.capitalize())
        if "imunidade_penalidade_mov" in efeitos:
            if "armadura" in efeitos["imunidade_penalidade_mov"]:
                lista.add("Movimento s/ Pen. Armadura")

    ficha.proficiencias = sorted(list(lista))


def sincronizar_ataques(ficha: Personagem):
    logger.info("--- [5.3] Ataques Naturais ---")
    novos = []
    for hab in ficha.habilidades:
        efeitos = hab.efeitos or {}
        if hab.escolhas_aplicadas:
            efeitos.update(hab.escolhas_aplicadas)

        raw = efeitos.get("arma_natural")
        if raw:
            if isinstance(raw, dict):
                novos.append(Ataque(
                    nome=raw.get("nome", "Arma"), teste="Luta", dano=raw.get("dano", "1d4"),
                    critico=raw.get("critico", "x2"), tipo=raw.get("tipo", "Impacto"), alcance=raw.get("alcance", "Curto")
                ))
            elif isinstance(raw, str):
                partes = raw.split(" ", 1)
                novos.append(Ataque(
                    nome=partes[0], teste="Luta", dano=partes[1] if len(partes) > 1 else "1d4",
                    critico="x2", tipo="Impacto", alcance="Curto"
                ))

    existentes = [a.nome for a in ficha.combate.ataques]
    for n in novos:
        if n.nome not in existentes:
            ficha.combate.ataques.append(n)
