"""Lote R5 — Motor de custo de magia (T20 JdA, Capítulo 4).

Regras oficiais implementadas:
- Base = Tabela 4-1 por círculo (1/3/6/10/15 PM)
- Aprimoramentos somam PM (cumulativos "aumenta" até o limite de PM = nível)
- Truque: custo 0 e não combina com outros aprimoramentos
- Reduções multiplicativas (Alta Arcana ×0.5, arredonda p/ baixo)
- Reduções fixas por magia (reducao_custo_magia racial)
- Custo mínimo 1 PM (0 apenas para Truque)
- CD = 10 + metade do nível + atributo-chave (exposta p/ tooltip)
"""
import math
import logging
from typing import Optional

from ..models import Personagem, StatCalculado, FonteBonus

logger = logging.getLogger("RegrasT20")

CUSTO_POR_CIRCULO = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}


def _circulo_int(magia) -> int:
    try:
        return int(magia.circulo)
    except Exception:
        return 1


def calcular_cd_magia(ficha: Personagem, magia) -> int:
    """CD = 10 + metade do nível + modificador do atributo-chave + bônus de escola.

    Se a magia tiver 'escola' preenchida, soma o bônus específico dessa escola
    (ex.: Especialista em Escola +2). Bônus por resistência (Familiar) NÃO entra
    aqui — vai nos testes de resistência, não na CD da magia.
    """
    from .utils import calcular_modificador
    attr = (magia.atributo_chave or "").lower()
    mapa = {'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'}
    val = getattr(ficha.atributos, mapa.get(attr, ''), 0) or 0
    cd_base = 10 + math.floor((ficha.cabecalho.nivel_total or 1) / 2) + calcular_modificador(val)
    escola = (magia.escola or "").strip()
    cd_escola = (getattr(ficha.combate, "cd_por_escola", None) or {}).get(escola, 0)

    # Arte Mágica (Bardo, T20 p.43): sob efeito de Inspiração, CD das habilidades de bardo +2
    cd_inspiracao = 0
    condicoes = getattr(ficha, "condicoes_ativas", None) or []
    if "inspiracao" in condicoes:
        for hab in ficha.habilidades:
            efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
            v_cd = efeitos.get("cd_bardo_inspiracao")
            if v_cd:
                cd_inspiracao += int(v_cd)
            elif (hab.nome or "") == "Arte Mágica":
                cd_inspiracao += 2

    # Liturgia Mágica (Clérigo, T20 p.58): +2 CD na próxima habilidade de clérigo
    cd_liturgia = 0
    if "liturgia_magica" in condicoes:
        for hab in ficha.habilidades:
            v_lit = (hab.efeitos or {}).get("cd_clerigo_liturgia")
            if v_lit:
                cd_liturgia += int(v_lit)
            elif (hab.nome or "") == "Liturgia Mágica":
                cd_liturgia += 2

    # Força da Natureza (Druida 20º, T20 p.62): +2 CD (+4 em terrenos naturais)
    cd_forca_nat = 0
    for hab in ficha.habilidades:
        if (hab.efeitos or {}).get("forca_da_natureza") or (hab.nome or "") == "Força da Natureza":
            cd_forca_nat += 4 if "terreno_natural" in condicoes else 2
            break

    return cd_base + cd_escola + cd_inspiracao + cd_liturgia + cd_forca_nat


def calcular_custo_magia(ficha: Personagem, magia,
                         aprimoramentos_pm: int = 0,
                         eh_truque: bool = False) -> StatCalculado:
    circulo = _circulo_int(magia)
    base = CUSTO_POR_CIRCULO.get(circulo, 1)
    calc = StatCalculado(base=base, total=base)
    calc.fontes.append(FonteBonus(
        fonte=f"Custo do {circulo}º círculo (Tabela 4-1)", categoria="Base", valor=base))

    # Truque: custo zero, sem outros aprimoramentos
    if eh_truque:
        calc.adicionar_bonus("Truque (versão simples)", "Truque", -base)
        calc.total = 0
        return calc

    total = base
    if aprimoramentos_pm:
        total += aprimoramentos_pm
        calc.adicionar_bonus("Aprimoramentos", "Aprimoramento", aprimoramentos_pm)

    # Reduções multiplicativas (Alta Arcana ×0.5) — arredonda p/ baixo
    for hab in ficha.habilidades:
        efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
        mult = efeitos.get("reducao_custo_magia_global")
        if isinstance(mult, (int, float)) and 0 < mult < 1:
            antes = total
            total = math.floor(total * mult)
            calc.adicionar_bonus(f"{hab.nome} (×{mult})", "Multiplicativo", total - antes)

    # Reduções fixas por magia (racial: reducao_custo_magia {"nomes": [...], "valor": N})
    for hab in ficha.habilidades:
        rc = (hab.efeitos or {}).get("reducao_custo_magia")
        if isinstance(rc, dict) and magia.nome in (rc.get("nomes") or []):
            valor = int(rc.get("valor", 1))
            total -= valor
            calc.adicionar_bonus(f"{hab.nome} (−{valor} PM)", "Redução", -valor)

    # Reduções se a magia já é conhecida de outra fonte (Qareen/Sereia/Bardo)
    for hab in ficha.habilidades:
        efeitos = {**(hab.efeitos or {}), **(hab.escolhas_aplicadas or {})}
        for chave in ("reducao_custo_se_conhecida", "reducao_custo_reaprendizado"):
            valor = efeitos.get(chave)
            if isinstance(valor, (int, float)) and valor and _ja_conhecida_de_outra_fonte(ficha, magia, f"Racial: {hab.nome}"):
                total -= int(valor)
                calc.adicionar_bonus(f"{hab.nome} (−{int(valor)} PM, reaprendizado)", "Reaprendizado", -int(valor))

    # Redução por tipo de dano (Linhagem Draconica Aprimorada: -1 PM em magias
    # do tipo escolhido, ex.: fogo, frio, eletricidade, acido).
    tipo_magia = (magia.tipo or "").strip().lower()
    reducoes_tipo = getattr(ficha.combate, "reducao_pm_tipo", None) or {}
    if tipo_magia and tipo_magia in reducoes_tipo:
        red = reducoes_tipo[tipo_magia]
        total -= red
        calc.adicionar_bonus(
            f"Linhagem Draconica ({tipo_magia}, -{red} PM)", "Reducao", -red)

    # Bônus por escola (Mestre em Escola: -1 PM na escola escolhida)
    escola = (magia.escola or "").strip()
    reducao_escola = (getattr(ficha.combate, "custo_por_escola", None) or {}).get(escola, 0)
    if reducao_escola:
        total += reducao_escola  # valores negativos em custo_por_escola
        calc.adicionar_bonus(
            f"Poder: Mestre em Escola ({escola})", "Poder", reducao_escola)

    # Símbolo Sagrado Energizado (Clérigo, T20 p.58): -1 PM em magias divinas
    condicoes = getattr(ficha, "condicoes_ativas", None) or []
    if "simbolo_energizado" in condicoes:
        eh_divina = (
            "divin" in tipo_magia
            or "universal" in tipo_magia
            or (not tipo_magia and any((c.nome or "") == "Clérigo" for c in (ficha.classes or [])))
        )
        if eh_divina:
            for hab in ficha.habilidades:
                red_simb = (hab.efeitos or {}).get("reducao_pm_magias_divinas_energizado")
                if red_simb:
                    total -= int(red_simb)
                    calc.adicionar_bonus(
                        f"Símbolo Sagrado Energizado (−{int(red_simb)} PM)", "Poder", -int(red_simb)
                    )
                    break

    # Força da Natureza (Druida 20º, T20 p.62): -2 PM (-4 PM em terrenos naturais)
    for hab in ficha.habilidades:
        if (hab.efeitos or {}).get("forca_da_natureza") or (hab.nome or "") == "Força da Natureza":
            red_fn = 4 if "terreno_natural" in condicoes else 2
            total -= red_fn
            calc.adicionar_bonus(f"Força da Natureza (−{red_fn} PM)", "Poder", -red_fn)
            break

    # Artista Completo (Bardo 20º, T20 p.44): sob Inspiração, custo em PM reduzido
    # pela metade APÓS aplicar aprimoramentos e quaisquer outras reduções.
    if "inspiracao" in condicoes:
        tem_artista = any(
            (hab.efeitos or {}).get("reducao_custo_inspiracao_metade")
            or (hab.efeitos or {}).get("artista_completo")
            or (hab.nome or "") == "Artista Completo"
            for hab in ficha.habilidades
        )
        if tem_artista and total > 0:
            antes = total
            total = math.floor(total / 2)
            calc.adicionar_bonus("Artista Completo (×0.5 sob Inspiração)", "Multiplicativo", total - antes)

    # Mínimo 1 PM (regra confirmada); limite de gasto por magia = nível
    total = max(1, total)
    limite_pm = max(1, ficha.cabecalho.nivel_total or 1)
    if total > limite_pm:
        total = limite_pm
        calc.adicionar_bonus(f"Limite de PM por magia (nível {limite_pm})", "Limite", total - max(1, total))
    calc.total = total
    return calc


# 🆕 Regras complementares (T20 JdA, cap. 4): redução se magia já é conhecida
# - reducao_custo_magia: sempre aplica (ex.: Dahllan, Suraggel, Dhampir)
# - reducao_custo_se_conhecida: aplica se a magia já está no Grimório
#   (ex.: Qareen/Sereia — "se aprender novamente, custo −1 PM")
# - reducao_custo_reaprendizado: idem (ex.: Bardo — reaprender reduz custo)
def _ja_conhecida_de_outra_fonte(ficha: Personagem, magia, fonte_atual: str) -> bool:
    """Verifica se a magia já existe no Grimório com uma fonte diferente."""
    for m in ficha.combate.magias:
        if m.nome == magia.nome and (m.fonte_origem or "") != fonte_atual:
            return True
    return False
