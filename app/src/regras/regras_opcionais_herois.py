"""Motor de Regras Opcionais — Heróis de Arton (Capítulo 4, p. 280–328).

Todas as funções aqui respeitam rigorosamente o modelo opt-in: fichas sem
regras opcionais, complicações ou papel no grupo permanecem 100% inalteradas.
"""
import random
from typing import Dict, Any, List, Optional
from ..models import Personagem, Habilidade, TamanhoEnum
from ..dados_habilidades import HABILIDADES_GERAIS
from ..dados_poderes_tormenta import DADOS_PODERES_TORMENTA
from ..dados_regras_opcionais_herois import (
    DADOS_COMPLICACOES,
    DADOS_IDADES_VARIADAS,
    DADOS_PAPEIS_GRUPO,
    ARMAS_AGEIS_EXTRA_HEROIS,
)

_ORDEM_TAMANHOS = [
    TamanhoEnum.MINUSCULO,
    TamanhoEnum.PEQUENO,
    TamanhoEnum.MEDIO,
    TamanhoEnum.GRANDE,
    TamanhoEnum.ENORME,
    TamanhoEnum.COLOSSAL,
]

_MULT_LONGEVIDADE_IDADES = {
    "Anão": 2,
    "Qareen": 2,
    "Dahllan": 5,
    "Elfo": 5,
    "Golem": 5,
    "Osteon": 5,
    "Sílfide": 5,
}


def regra_opcional_ativa(ficha: Personagem, slug: str) -> bool:
    """Retorna True se a regra opcional identificada por `slug` estiver ativa na ficha."""
    ativas = getattr(ficha, "regras_opcionais_ativas", None) or []
    return slug in ativas


def _buscar_complicacao(nome: str) -> Optional[Dict[str, Any]]:
    if not nome:
        return None
    if nome in DADOS_COMPLICACOES:
        return DADOS_COMPLICACOES[nome]
    alvo = nome.strip().lower()
    for k, v in DADOS_COMPLICACOES.items():
        if k.lower() == alvo or (v.get("nome") or "").strip().lower() == alvo:
            return v
    return None


def _buscar_poder_geral(nome: str) -> Optional[Dict[str, Any]]:
    if not nome:
        return None
    if nome in HABILIDADES_GERAIS:
        return HABILIDADES_GERAIS[nome]
    if nome in DADOS_PODERES_TORMENTA:
        return DADOS_PODERES_TORMENTA[nome]
    alvo = nome.strip().lower()
    for d in (HABILIDADES_GERAIS, DADOS_PODERES_TORMENTA):
        for k, v in d.items():
            if k.lower() == alvo or (v.get("nome") or "").strip().lower() == alvo:
                return v
    return None


def validar_complicacao_classe(ficha: Personagem, nome_complicacao: str) -> Dict[str, Any]:
    """Valida a regra de Complicações de Classe (Heróis de Arton, p. 285):
    para usufruir do poder bônus, pelo menos metade dos níveis totais do personagem
    deve pertencer à classe da complicação (e à subclasse, se houver).
    """
    dados = _buscar_complicacao(nome_complicacao)
    if not dados or dados.get("tipo") != "Classe":
        return {"valida": True, "motivo": ""}

    classe_req = dados.get("classe", "")
    subclasse_req = dados.get("subclasse", "")
    nivel_total = max(1, sum(int(c.nivel or 0) for c in (ficha.classes or [])))
    nivel_classe = sum(
        int(c.nivel or 0)
        for c in (ficha.classes or [])
        if (c.nome or "").strip().lower() == classe_req.lower()
    )

    if nivel_classe * 2 < nivel_total:
        return {
            "valida": False,
            "motivo": f"Requer ao menos metade dos níveis ({(nivel_total + 1) // 2}) em {classe_req} (atual: {nivel_classe}/{nivel_total}).",
        }

    if subclasse_req:
        tem_sub = any(
            (c.nome or "").strip().lower() == classe_req.lower()
            and (c.subclasse or "").strip().lower() == subclasse_req.lower()
            for c in (ficha.classes or [])
        )
        if not tem_sub:
            return {
                "valida": False,
                "motivo": f"Requer subclasse {subclasse_req} de {classe_req}.",
            }

    return {"valida": True, "motivo": ""}


def sincronizar_complicacoes(
    ficha: Personagem,
    memoria_global: Optional[Dict[str, Dict[str, Any]]] = None,
) -> None:
    """Injeta as complicações escolhidas em `ficha.complicacoes` e seus poderes bônus."""
    if not getattr(ficha, "complicacoes", None):
        return

    memoria_global = memoria_global or {}
    nomes_existentes = {(h.nome or "").strip().lower() for h in ficha.habilidades}

    for comp in ficha.complicacoes:
        dados = _buscar_complicacao(comp.nome)
        nome_canon = dados["nome"] if dados else comp.nome
        efeitos = dict((dados or {}).get("efeitos") or {})

        # Fracote (condição fraco permanente): -2 em perícias de For, Des e Con
        if efeitos.get("condicao_permanente") == "fraco":
            bpa = dict(efeitos.get("bonus_pericia_atributo") or {})
            for a in ("for", "des", "con"):
                bpa[a] = bpa.get(a, 0) - 2
            efeitos["bonus_pericia_atributo"] = bpa

        ficha.habilidades.append(
            Habilidade(
                nome=nome_canon,
                tipo="Complicação",
                fonte=f"Complicação: {nome_canon}",
                descricao=comp.descricao or (dados or {}).get("descricao", ""),
                efeitos=efeitos,
            )
        )
        nomes_existentes.add(nome_canon.lower())

        # Injeta o poder geral bônus se preenchido e elegível
        poder_nome = (comp.poder_bonus or "").strip()
        if poder_nome and poder_nome.lower() not in nomes_existentes:
            check = validar_complicacao_classe(ficha, nome_canon)
            if check["valida"]:
                dados_poder = _buscar_poder_geral(poder_nome)
                nome_poder = dados_poder["nome"] if dados_poder else poder_nome
                if nome_poder.lower() not in nomes_existentes:
                    ficha.habilidades.append(
                        Habilidade(
                            nome=nome_poder,
                            tipo=(dados_poder or {}).get("tipo", "Poder Geral"),
                            fonte=f"Complicação: {nome_canon}",
                            descricao=(dados_poder or {}).get("descricao", ""),
                            custo_pm=int((dados_poder or {}).get("custo_pm", 0) or 0),
                            efeitos=dict((dados_poder or {}).get("efeitos") or {}),
                            escolhas_aplicadas=dict(memoria_global.get(nome_poder) or {}),
                        )
                    )
                    nomes_existentes.add(nome_poder.lower())


def sincronizar_papel_grupo(ficha: Personagem) -> None:
    """Injeta o bônus mecânico de `ficha.papel_grupo` (Heróis de Arton, p. 294-295)."""
    papel_raw = (getattr(ficha, "papel_grupo", None) or "").strip()
    if not papel_raw:
        return

    # Suporta "Tesoureiro (Ofício)" ou "Tesoureiro (Nobreza)" além do nome exato
    escolha_pericia = None
    papel_base = papel_raw
    if "(" in papel_raw and papel_raw.endswith(")"):
        papel_base, _, resto = papel_raw.partition("(")
        papel_base = papel_base.strip()
        escolha_pericia = resto[:-1].strip()

    dados = DADOS_PAPEIS_GRUPO.get(papel_base)
    if not dados:
        for k, v in DADOS_PAPEIS_GRUPO.items():
            if k.lower() == papel_base.lower():
                dados = v
                break
    if not dados:
        return

    efeitos = dict(dados.get("efeitos") or {})
    if dados["nome"] == "Tesoureiro" and escolha_pericia:
        if escolha_pericia.lower().startswith("of"):
            efeitos = {"bonus_pericia": {"Ofício": 1}}
        elif escolha_pericia.lower().startswith("nob"):
            efeitos = {"bonus_pericia": {"Nobreza": 1}}

    ficha.habilidades.append(
        Habilidade(
            nome=f"Papel no Grupo: {dados['nome']}",
            tipo="Papel no Grupo",
            fonte="Regra Opcional: Papel no Grupo",
            descricao=dados.get("descricao", ""),
            efeitos=efeitos,
        )
    )


def resolver_faixa_etaria_variada(ficha: Personagem) -> str:
    """Determina a faixa etária da Tabela 4-2 (Heróis de Arton, p. 288)."""
    raca = (ficha.cabecalho.raca or "").strip()
    mult = _MULT_LONGEVIDADE_IDADES.get(raca, 1)
    idade = getattr(ficha.descricao, "idade", None)

    if isinstance(idade, int) and idade > 0:
        idade_eq = idade / mult
        if idade_eq < 13:
            return "Criança"
        if idade_eq < 18:
            return "Adolescente"
        if idade_eq < 25:
            return "Jovem"
        if idade_eq < 40:
            return "Adulto"
        if idade_eq < 60:
            return "Maduro"
        if idade_eq < 80:
            return "Velho"
        return "Ancião"

    faixa = getattr(ficha.descricao, "faixa_etaria", "Adulto") or "Adulto"
    return faixa if faixa in DADOS_IDADES_VARIADAS else "Adulto"


def sincronizar_idades_variadas(ficha: Personagem) -> None:
    """Aplica efeitos não-atributo de Idades Variadas (Tabela 4-2) quando opt-in ativo."""
    if not regra_opcional_ativa(ficha, "idades_variadas"):
        return

    faixa = resolver_faixa_etaria_variada(ficha)
    ficha.descricao.faixa_etaria = faixa
    dados = DADOS_IDADES_VARIADAS.get(faixa)
    if not dados:
        return

    # Ajuste de tamanho (ex.: Criança diminui 1 categoria de tamanho)
    delta = int(dados.get("tamanho_delta", 0) or 0)
    if delta != 0:
        try:
            idx = _ORDEM_TAMANHOS.index(ficha.descricao.tamanho)
            novo_idx = max(0, min(len(_ORDEM_TAMANHOS) - 1, idx + delta))
            ficha.descricao.tamanho = _ORDEM_TAMANHOS[novo_idx]
        except ValueError:
            pass

    # Habilidades especiais da faixa (Protegido dos Deuses / Ímpeto Juvenil)
    for hab_esp in dados.get("habilidades_especiais", []):
        ficha.habilidades.append(
            Habilidade(
                nome=hab_esp["nome"],
                tipo="Idade Variada",
                fonte=f"Regra Opcional: Idades Variadas ({faixa})",
                descricao=hab_esp.get("descricao", ""),
                efeitos=dict(hab_esp.get("efeitos") or {}),
            )
        )


def arma_e_agil_com_regra_opcional(ficha: Personagem, nome_arma: str) -> bool:
    """Retorna True se a arma se torna ágil via regra opcional 'mais_armas_ageis' (p. 303)."""
    if not regra_opcional_ativa(ficha, "mais_armas_ageis"):
        return False
    alvo = (nome_arma or "").strip().lower()
    return any(a.lower() == alvo for a in ARMAS_AGEIS_EXTRA_HEROIS)


# =====================================================================
# HELPERS DE MESA (Geração de Atributos, Morte Alternativa, Domínios)
# =====================================================================

def _valor_3d6_para_mod(total: int) -> int:
    """Converte resultado de 3d6 (ou 3..18) para modificador T20 JdA."""
    if total <= 7:
        return -2
    if total <= 9:
        return -1
    if total <= 11:
        return 0
    if total <= 13:
        return 1
    if total <= 15:
        return 2
    if total <= 17:
        return 3
    return 4


def _d20_nimb_para_mod(valor: int) -> int:
    """Converte resultado de 1d20 do método Nimb (Heróis de Arton, p. 281)."""
    if valor <= 3:
        return -3
    if valor <= 5:
        return -2
    if valor <= 8:
        return -1
    if valor <= 11:
        return 0
    if valor <= 14:
        return 1
    if valor <= 16:
        return 2
    if valor == 17:
        return 3
    if valor <= 19:
        return 4
    return 5


def gerar_atributos_metodo(
    metodo: str,
    seed: Optional[int] = None,
    pontos: int = 10,
) -> Dict[str, Any]:
    """Gera conjunto de 6 atributos segundo um dos 6 métodos oficiais (p. 280–281)."""
    rng = random.Random(seed)
    m = (metodo or "").strip().lower()

    if m == "khalmyr":
        return {"metodo": "Khalmyr", "valores": [3, 3, 2, 1, 0, -1]}

    if m in ("clássica", "classica"):
        rolagens = [sum(rng.randint(1, 6) for _ in range(3)) for _ in range(6)]
        mods = sorted([_valor_3d6_para_mod(r) for r in rolagens], reverse=True)
        return {"metodo": "Clássica", "rolagens": rolagens, "valores": mods}

    if m in ("épica", "epica"):
        rolagens = []
        for _ in range(6):
            dados = sorted(rng.randint(1, 6) for _ in range(3))
            rolagens.append(sum(dados[1:]) + 6)
        mods = sorted([_valor_3d6_para_mod(r) for r in rolagens], reverse=True)
        return {"metodo": "Épica", "rolagens": rolagens, "valores": mods}

    if m == "valkaria":
        dados = [rng.randint(1, 6) for _ in range(7)]
        return {
            "metodo": "Valkaria",
            "base": [8, 8, 8, 8, 8, 8],
            "dados_7d6": dados,
            "limite_mod_maximo": 4,
        }

    if m == "nimb":
        dados = [rng.randint(1, 20) for _ in range(7)]
        mantidos = sorted(dados, reverse=True)[:6]
        mods = [_d20_nimb_para_mod(v) for v in mantidos]
        return {"metodo": "Nimb", "dados_7d20": dados, "mantidos": mantidos, "valores": mods}

    if m in ("pontos variados", "pontos_variados"):
        pts = pontos if pontos in (5, 10, 15) else 10
        return {"metodo": "Pontos Variados", "pontos_disponiveis": pts}

    raise ValueError(f"Método de geração desconhecido: {metodo}")


def calcular_pm_dominio_mistico(nivel_dominio: int) -> int:
    """Domínios Místicos (Heróis de Arton, p. 324): concede nível² PM extras."""
    nv = max(0, int(nivel_dominio or 0))
    return nv * nv


def avaliar_teste_morte_alternativa(resultado_d20: int, bonus: int = 0, cd: int = 10) -> Dict[str, Any]:
    """Avalia um Teste de Morte (regra opcional Morte Alternativa, p. 302)."""
    total = int(resultado_d20) + int(bonus)
    if resultado_d20 == 20:
        return {"resultado": "critico_sucesso", "estabilizado": True, "recupera_1_pv": True, "total": total}
    if resultado_d20 == 1:
        return {"resultado": "falha_critica", "estabilizado": False, "falhas_adicionadas": 2, "total": total}
    if total >= cd:
        return {"resultado": "sucesso", "estabilizado": False, "sucessos_adicionados": 1, "total": total}
    return {"resultado": "falha", "estabilizado": False, "falhas_adicionadas": 1, "total": total}
