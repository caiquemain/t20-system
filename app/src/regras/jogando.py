"""Regras do Capítulo 5 — Jogando (T20 Jogo do Ano, p.220–239).

Inclui:
- Tabela 5-1 (Dificuldades), Tabela 5-2 (Testes Estendidos), Tabela 5-3 (Situações Especiais) e Tabela 5-4 (Estatísticas de Objetos)
- Avaliação de testes (20 natural / 1 natural), Ajudar, Escolher 0/10/20
- Clarificações de regras: arredondamento para baixo, ordem de operações de dano,
  multiplicações combinadas (x2+x2=x3), teto de chance de falha (75%)
- CD de habilidades (10 + metade do nível + atributo), Tipos de Efeitos (18) e Tipos de Dano (11)
- Ferimentos & Morte (limiar de morte = min(-10, -floor(PV_max / 2)))
"""
import math
from typing import Iterable, List

# Tabela 5-1: Dificuldades (T20 JdA p.220)
TABELA_DIFICULDADES = {
    "Fácil": 5,
    "Média": 10,
    "Difícil": 15,
    "Desafiadora": 20,
    "Formidável": 25,
    "Heroica": 30,
    "Quase Impossível": 40,
}

# Tabela 5-2: Testes Estendidos (T20 JdA p.223)
TESTES_ESTENDIDOS = {
    "Baixa": {"sucessos": 3, "falhas_max": 3},
    "Média": {"sucessos": 5, "falhas_max": 3},
    "Alta": {"sucessos": 7, "falhas_max": 3},
}

# Alcances padrão (T20 JdA p.224)
ALCANCES_PADRAO = {
    "Pessoal": {"metros": 0, "quadrados": 0},
    "Toque": {"metros": 1.5, "quadrados": 1},
    "Curto": {"metros": 9, "quadrados": 6},
    "Médio": {"metros": 30, "quadrados": 20},
    "Longo": {"metros": 90, "quadrados": 60},
    "Ilimitado": {"metros": None, "quadrados": None},
}

# Tipos de Efeitos (T20 JdA p.228 — 18 tipos)
TIPOS_DE_EFEITO = (
    "Arcano", "Atordoamento", "Cansaço", "Climático", "Cura", "Dano",
    "Divino", "Luz", "Mágico", "Medo", "Mental", "Metabolismo",
    "Metamorfose", "Movimento", "Perda de Vida", "Sentidos", "Trevas", "Veneno",
)

# Tipos de Dano (T20 JdA p.230 — 11 tipos)
TIPOS_DE_DANO = (
    "Ácido", "Corte", "Eletricidade", "Essência", "Fogo", "Frio",
    "Impacto", "Luz", "Perfuração", "Psíquico", "Trevas",
)

# Manobras de Combate (T20 JdA p.234)
MANOBRAS_COMBATE = {
    "Agarrar": "Alvo fica desprevenido e imóvel, –2 ataque, só ataca com armas leves; apenas com ataque desarmado ou arma natural.",
    "Derrubar": "Deixa o alvo caído; vencer por 5+ também empurra 1 quadrado.",
    "Desarmar": "Derruba item segurado; vencer por 5+ também empurra o item 1 quadrado.",
    "Empurrar": "Empurra 1,5m (+1,5m para cada 5 pontos de diferença); ação de movimento pode avançar junto.",
    "Quebrar": "Atinge um item segurado pelo oponente (veja Tabela 5-4).",
}

# Tabela 5-3: Situações Especiais (T20 JdA p.238)
SITUACOES_ESPECIAIS = {
    "atacante": {
        "Caído": {"ataque_corpo_a_corpo": -5},
        "Cego": {"chance_falha": 50},
        "Em posição elevada": {"ataque": 2},
        "Flanqueando": {"ataque_corpo_a_corpo": 2},
        "Invisível": {"defesa_alvo": -5},
        "Ofuscado": {"ataque": -2},
    },
    "alvo": {
        "Caído": {"defesa_corpo_a_corpo": -5, "defesa_distancia": 5},
        "Cego": {"defesa": -5},
        "Desprevenido": {"defesa": -5},
        "Camuflagem leve": {"chance_falha": 20},
        "Camuflagem total": {"chance_falha": 50},
        "Cobertura leve": {"defesa": 5},
        "Cobertura total": {"nao_pode_ser_atacado": True},
    },
}

# Tabela 5-4: Estatísticas de Objetos (T20 JdA p.239)
ESTATISTICAS_OBJETOS = {
    # Objetos Gerais (11)
    "Pergaminho": {"categoria": "Geral", "tamanho": "Minúsculo", "defesa": 15, "rd": 0, "pv": 1},
    "Corda": {"categoria": "Geral", "tamanho": "Minúsculo", "defesa": 15, "rd": 0, "pv": 2},
    "Corrente": {"categoria": "Geral", "tamanho": "Minúsculo", "defesa": 15, "rd": 10, "pv": 2},
    "Cadeira": {"categoria": "Geral", "tamanho": "Pequeno", "defesa": 12, "rd": 5, "pv": 5},
    "Barril": {"categoria": "Geral", "tamanho": "Médio", "defesa": 10, "rd": 5, "pv": 10},
    "Porta de madeira": {"categoria": "Geral", "tamanho": "Grande", "defesa": 8, "rd": 5, "pv": 20},
    "Porta de pedra": {"categoria": "Geral", "tamanho": "Grande", "defesa": 8, "rd": 8, "pv": 100},
    "Porta de ferro": {"categoria": "Geral", "tamanho": "Grande", "defesa": 8, "rd": 10, "pv": 100},
    "Carroça": {"categoria": "Geral", "tamanho": "Grande", "defesa": 8, "rd": 5, "pv": 50},
    "Casebre": {"categoria": "Geral", "tamanho": "Enorme", "defesa": 5, "rd": 5, "pv": 100},
    "Celeiro": {"categoria": "Geral", "tamanho": "Colossal", "defesa": 0, "rd": 5, "pv": 200},
    # Armas, Armaduras e Escudos (10)
    "Arma leve de madeira": {"categoria": "Equipamento", "rd": 5, "pv": 2},
    "Arma de uma mão de madeira": {"categoria": "Equipamento", "rd": 5, "pv": 5},
    "Arma de duas mãos de madeira": {"categoria": "Equipamento", "rd": 5, "pv": 10},
    "Arma leve de metal": {"categoria": "Equipamento", "rd": 10, "pv": 2},
    "Arma de uma mão de metal": {"categoria": "Equipamento", "rd": 10, "pv": 5},
    "Arma de duas mãos de metal": {"categoria": "Equipamento", "rd": 10, "pv": 10},
    "Escudo leve": {"categoria": "Equipamento", "rd": 5, "pv": 10},
    "Escudo pesado": {"categoria": "Equipamento", "rd": 10, "pv": 20},
    "Armadura leve": {"categoria": "Equipamento", "rd": 5, "pv": 20},
    "Armadura pesada": {"categoria": "Equipamento", "rd": 10, "pv": 40},
}


def avaliar_teste(d20: int, modificador: int, cd: int) -> dict:
    """Avalia um teste de 1d20 + modificador contra CD (T20 JdA p.220–221).

    20 natural é sempre sucesso automático; 1 natural é sempre falha automática.
    """
    total = int(d20) + int(modificador)
    if d20 == 20:
        sucesso = True
        critico = "sucesso_automatico"
    elif d20 == 1:
        sucesso = False
        critico = "falha_automatica"
    else:
        sucesso = total >= int(cd)
        critico = None
    return {"d20": int(d20), "total": total, "cd": int(cd), "sucesso": sucesso, "critico": critico}


def calcular_bonus_ajuda(resultado_ajudante: int) -> int:
    """Calcula o bônus fornecido ao líder pela regra Ajudar (T20 JdA p.221).

    CD 10 concede +1, e +1 adicional para cada 10 pontos acima da CD (+2 em 20, +3 em 30...).
    """
    if resultado_ajudante < 10:
        return 0
    return 1 + (int(resultado_ajudante) - 10) // 10


def pode_escolher_zero(bonus_total: int, cd: int) -> bool:
    """Escolher 0 (T20 JdA p.222): passa automaticamente se bônus total >= CD."""
    return int(bonus_total) >= int(cd)


def calcular_cd_habilidade(nivel_total: int, mod_atributo: int) -> int:
    """CD de teste de resistência de habilidade (T20 JdA p.227): 10 + floor(nível/2) + atributo."""
    return 10 + math.floor(max(1, int(nivel_total or 1)) / 2) + int(mod_atributo or 0)


def combinar_multiplicadores(multiplicadores: Iterable[int]) -> int:
    """Combina múltiplos multiplicadores conforme T20 JdA p.226 (x2 + x2 = x3)."""
    lista: List[int] = [int(m) for m in multiplicadores if int(m) > 1]
    if not lista:
        return 1
    total = lista[0]
    for m in lista[1:]:
        total += (m - 1)
    return total


def limitar_chance_falha(chances: Iterable[int]) -> int:
    """Chance de falha nunca acumula acima de 75% (T20 JdA p.226)."""
    return min(75, sum(max(0, int(c)) for c in chances))


def calcular_dano_recebido(
    dano_bruto: int,
    passou_resistencia_metade: bool = False,
    divisores_metade: int = 0,
    vulneravel: bool = False,
    rd: int = 0,
    perda_de_vida: bool = False,
) -> int:
    """Calcula o dano final seguindo a ordem oficial de operações (T20 JdA p.226, 228–229):

    1. Teste de resistência (reduz à metade, arredondando para baixo)
    2. Multiplicações/divisões (ex.: Durão /2, Vulnerabilidade ×1,5 arredondado para baixo)
    3. Somas/subtrações (RD — ignorada se perda_de_vida=True)
    """
    dano = max(0, int(dano_bruto or 0))
    if passou_resistencia_metade:
        dano = math.floor(dano / 2)
    for _ in range(max(0, int(divisores_metade or 0))):
        dano = math.floor(dano / 2)
    if vulneravel:
        dano = math.floor(dano * 1.5)
    if not perda_de_vida and rd > 0:
        dano = max(0, dano - int(rd))
    return dano


def calcular_limiar_morte(pv_maximo: int) -> int:
    """Limiar de morte (T20 JdA p.236): –10 ou metade negativa dos PV máximos (o que for mais baixo)."""
    metade_neg = -(max(0, int(pv_maximo or 0)) // 2)
    return min(-10, metade_neg)


def calcular_pv_objeto(pv_base: int, tamanho_item: str = "Comum") -> int:
    """Ajusta PV de equipamento por tamanho (Tabela 5-4, T20 JdA p.239)."""
    t = (tamanho_item or "Comum").strip().lower()
    if t == "reduzido":
        return max(1, math.floor(pv_base / 2))
    if t == "aumentado":
        return pv_base * 2
    if t == "gigante":
        return pv_base * 5
    return pv_base
