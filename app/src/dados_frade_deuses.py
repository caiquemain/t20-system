# -*- coding: utf-8 -*-
"""Classe Frade — Deuses de Arton (Cap. 1, p. 38–41).

Conjurador divino focado em suporte, cura, conhecimento e sacrários:
- PV: 12 (+ Con) inicial, +3 (+ Con) por nível
- PM: 6 por nível + Sabedoria
- Perícias: Religião, Vontade + 4 à escolha (15 opções)
- Proficiências: Nenhuma
- 6 Habilidades de Classe fixas (Tabela 1-1) + 29 Poderes de Frade (incl. 8 Sacrários)
"""
from typing import Any, Dict, List
from .dados_suplementos import FONTE_DEUSES

_F = FONTE_DEUSES

REGRAS_SACRARIOS_FRADE: Dict[str, Any] = {
    "fonte": _F,
    "acao": "padrão",
    "custo_pm": 3,
    "alcance": "curto",
    "raio_m": 3,
    "duracao": "cena",
    "max_ativos_attr": "sab",
    "resumo": (
        "Criar um sacrário gasta uma ação padrão e 3 PM, ocupa esfera de 3m de raio em alcance curto "
        "e dura até o fim da cena (salvo indicação contrária). Máximo de sacrários simultâneos = Sabedoria. "
        "Não pode sobrepor outro sacrário nem símbolo visível de outra divindade; criaturas precisam estar "
        "inteiramente dentro da área."
    ),
}


def _fixa(
    chave: str,
    nome: str,
    nivel: int,
    descricao: str,
    efeitos: Dict[str, Any] | None = None,
) -> tuple[str, Dict[str, Any]]:
    ef = dict(efeitos or {})
    if not ef:
        ef["nota"] = descricao
    return chave, {
        "nome": nome,
        "tipo": "Habilidade de Classe",
        "classe": "Frade",
        "nivel": nivel,
        "fonte": _F,
        "descricao": descricao,
        "efeitos": ef,
    }


def _pf(
    nome: str,
    descricao: str,
    requisitos: List[str] | None = None,
    efeitos: Dict[str, Any] | None = None,
    custo_pm: int = 0,
    sacrario: bool = False,
    duracao_sacrario: str = "cena",
) -> Dict[str, Any]:
    ef = dict(efeitos or {})
    if sacrario:
        ef.setdefault(
            "sacrario",
            {
                "acao": "padrão",
                "custo_pm": 3,
                "alcance": "curto",
                "raio_m": 3,
                "duracao": duracao_sacrario,
            },
        )
        ef.setdefault("custo_pm", 3)
        custo_pm = custo_pm or 3
    elif custo_pm and "custo_pm" not in ef:
        ef["custo_pm"] = custo_pm
    if not ef:
        ef["nota"] = descricao
    d: Dict[str, Any] = {
        "nome": nome,
        "tipo": "Poder de Frade",
        "classe": "Frade",
        "nivel": 0,
        "fonte": _F,
        "descricao": descricao,
        "requisitos": list(requisitos or []),
        "efeitos": ef,
    }
    if custo_pm:
        d["custo_pm"] = custo_pm
    return d


DADOS_HABILIDADES_FRADE: Dict[str, Dict[str, Any]] = dict(
    [
        # ── HABILIDADES FIXAS (Tabela 1-1, p. 39) ──
        _fixa(
            "FRADE_DEVOTO_FIEL",
            "Devoto Fiel (Frade)",
            1,
            (
                "Você se torna devoto de um deus maior e recebe dois poderes concedidos (em vez de um). "
                "Como alternativa, pode cultuar o Panteão como um todo: não recebe poderes concedidos, "
                "sua única O&R é não usar armas cortantes ou perfurantes, sua arma preferida é a maça "
                "e escolhe canalizar energia positiva ou negativa."
            ),
            {"poderes_concedidos_devoto": 2, "permite_panteao": True},
        ),
        _fixa(
            "FRADE_ERUDICAO",
            "Erudição",
            1,
            (
                "Quando faz um teste de perícia (exceto ataque), pode gastar PM à sua escolha "
                "(limitado por sua Inteligência) para receber +2 no teste por PM gasto."
            ),
            {"erudicao_pm_max_attr": "int", "bonus_por_pm": 2, "custo_pm": 1},
        ),
        _fixa(
            "FRADE_MAGIAS",
            "Magias (Frade)",
            1,
            (
                "Lança magias divinas de 1º círculo (2º no 5º nível, 3º no 9º, 4º no 13º, 5º no 17º). "
                "Começa com 3 magias de 1º círculo e aprende +1 magia por nível. Atributo-chave: Sabedoria "
                "(soma Sabedoria no total de PM). Pode lançar de armadura leve; armadura pesada exige "
                "teste de Misticismo como conjurador arcano."
            ),
            {
                "habilita_magia": {"tipo": "Divina", "circulo_max": 1, "atributo_chave": "sab"},
                "armadura_pesada_exige_misticismo": True,
            },
        ),
        _fixa(
            "FRADE_VERSICULARIO",
            "Versiculário",
            2,
            (
                "Recebe um versiculário. 1×/dia gasta 1 hora estudando e escolhe até Inteligência magias "
                "(limitado pelo nível): até o próximo dia, ao lançá-las recebe +1 PM para gastar em aprimoramentos. "
                "Reposição: 1 semana e T$ 100."
            ),
            {"versiculario_pm_aprimoramento": 1, "versiculario_max_attr": "int"},
        ),
        _fixa(
            "FRADE_DADIVA_FE",
            "Dádiva da Fé",
            5,
            (
                "Recebe Proteção Sagrada (divindade de energia positiva: movimento + até 2 PM/círculo, "
                "aura 9m pela cena concedendo RD = metade dos PM gastos) ou Cólera Divina (energia negativa: "
                "mesma ativação concedendo bônus em rolagens de dano = metade dos PM gastos)."
            ),
            {"dadiva_da_fe": True, "raio_m": 9, "custo_pm": 2},
        ),
        _fixa(
            "FRADE_SOLO_SANTIFICADO",
            "Solo Santificado",
            20,
            (
                "O raio de sua Dádiva da Fé muda para 30m e criaturas afetadas por ela também somam "
                "o bônus concedido pela habilidade na CD de suas próprias habilidades."
            ),
            {"solo_santificado": True, "dadiva_raio_m": 30},
        ),
    ]
)

# ── 29 PODERES DE FRADE (p. 39–41) ──
DADOS_HABILIDADES_FRADE.update(
    {
        "FRADE_ACELERAR_SACRARIO": _pf(
            "Acelerar Sacrário",
            "Ao criar um sacrário, pode gastar +2 PM para criá-lo como ação de movimento (em vez de padrão).",
            ["5º nível de frade"],
            custo_pm=2,
        ),
        "FRADE_AMPLIAR_SACRARIO": _pf(
            "Ampliar Sacrário",
            "Pode criar sacrários em alcance médio e eles passam a ocupar uma esfera de 6m de raio.",
            ["10º nível de frade"],
            {"sacrario_alcance": "médio", "sacrario_raio_m": 6},
        ),
        "FRADE_AUMENTO_ATRIBUTO": _pf(
            "Aumento de Atributo",
            "Recebe +1 em um atributo. Pode escolher várias vezes (1× por patamar por atributo).",
            [],
            {"atributo_bonus_escolha": 1},
        ),
        "FRADE_AUTORIDADE_ECLESIASTICA": _pf(
            "Autoridade Eclesiástica",
            "Possui posição formal em uma igreja reconhecida pelos outros membros de sua fé (efeitos variam por divindade).",
            ["5º nível de frade", "Devoto de um deus maior"],
        ),
        "FRADE_BENCAO_FORTALECEDORA": _pf(
            "Bênção Fortalecedora",
            "Ao lançar Bênção, aliados abençoados recebem PV temporários iguais a 5× o bônus de ataque da magia pela duração.",
            ["Bênção"],
        ),
        "FRADE_CANTO_MONASTICO": _pf(
            "Canto Monástico",
            "Ação padrão e 1 PM: teste de Atuação para ajudar; aliados em alcance curto somam esse bônus em 1 perícia ou CD de 1 habilidade na cena.",
            ["Treinado em Atuação"],
            custo_pm=1,
        ),
        "FRADE_COMUNHAO_VITAL": _pf(
            "Comunhão Vital",
            "Ao lançar magia que cure uma criatura, pague +2 PM para outra criatura em alcance curto (ou você) recuperar metade dos PV curados.",
            [],
            custo_pm=2,
        ),
        "FRADE_COPISTA": _pf(
            "Copista",
            "Pode criar pergaminhos como Escrever Pergaminho; se possuir ambos, fabrica o dobro de pergaminhos ao mesmo tempo.",
            ["Treinado em Ofício (escriba)"],
            {"escrever_pergaminho": True},
        ),
        "FRADE_CONHECIMENTO_MAGICO": _pf(
            "Conhecimento Mágico",
            "Aprende duas magias de qualquer círculo que possa lançar. Pode escolher quantas vezes quiser.",
            [],
            {"magias_adicionais_escolha": 2},
        ),
        "FRADE_COZINHEIRO_ABADIA": _pf(
            "Cozinheiro da Abadia",
            "Ao preparar prato especial, pode combinar efeitos de dois pratos com um único teste de Ofício (pagando o custo de ambos).",
            ["Treinado em Ofício (cozinheiro)"],
        ),
        "FRADE_ESTUDANTE_DILIGENTE": _pf(
            "Estudante Diligente",
            "No começo do dia, escolha 1 perícia não treinada: sofre –2 PM até o fim do dia, mas faz testes dessa perícia como se fosse treinado.",
            [],
        ),
        "FRADE_FE_E_RAZAO": _pf(
            "Fé e Razão",
            "Ao usar uma habilidade de frade, pode gastar PM (até Inteligência) para aumentar a CD em +1 por PM gasto.",
            [],
            custo_pm=1,
        ),
        "FRADE_MAGO_BRANCO": _pf(
            "Mago Branco",
            "Suas magias de cura de luz custam –1 PM e curam +1 PV por dado de cura.",
            ["3º nível de frade"],
            {"reducao_pm_cura_luz": 1, "cura_luz_bonus_por_dado": 1},
        ),
        "FRADE_MEMORIZAR_LITURGIA": _pf(
            "Memorizar Liturgia",
            "1×/dia gasta 1h e até Inteligência pergaminhos divinos: até o fim do dia lança essas magias como conhecidas (ou +Int no limite de PM se já conhecia).",
            ["Copista", "8º nível de frade"],
        ),
        "FRADE_OFICIO_MOSTEIRO": _pf(
            "Ofício do Mosteiro",
            "Pode fabricar itens de vestuário com Ofício (artesão) e fabricar itens com uma melhoria usando essa perícia.",
            ["Treinado em Ofício (artesão)"],
        ),
        "FRADE_PSICOGRAFIA": _pf(
            "Psicografia",
            "Pode fabricar pergaminhos de qualquer magia divina (mesmo desconhecida) de círculos a que tenha acesso (CD +5).",
            ["Copista", "5º nível de frade"],
        ),
        "FRADE_SACRARIO_ERUDICAO": _pf(
            "Sacrário da Erudição",
            "Sacrário (padrão, 3 PM, 3m, cena): ao lançar magias de pergaminhos dentro da área, você e aliados recebem +1 PM para aprimoramentos.",
            [],
            sacrario=True,
        ),
        "FRADE_SACRARIO_MISERICORDIA": _pf(
            "Sacrário da Misericórdia",
            "Sacrário sustentado (padrão, 3 PM, 3m): no início dos seus turnos, criaturas escolhidas na área recuperam 5 + Sabedoria PV.",
            ["5º nível de frade"],
            sacrario=True,
            duracao_sacrario="sustentada",
        ),
        "FRADE_SACRARIO_RESILIENCIA": _pf(
            "Sacrário da Resiliência",
            "Sacrário (padrão, 3 PM, 3m, cena): você e aliados na área recebem +2 em TR e na Defesa (+1 a cada +2 PM extras, máx. círculo máximo).",
            ["5º nível de frade"],
            sacrario=True,
        ),
        "FRADE_SACRARIO_SOLENIDADE": _pf(
            "Sacrário da Solenidade",
            "Sacrário (padrão, 3 PM, 3m, cena): criaturas na área ficam sob condição terrível para lançar magias e sofrem –2 na Defesa (–1 a cada +2 PM extras, máx. círculo máximo).",
            [],
            sacrario=True,
        ),
        "FRADE_SACRARIO_VERDADE": _pf(
            "Sacrário da Verdade",
            "Sacrário (padrão, 3 PM, 3m, cena): criatura na área que passe em Acrobacia, Enganação, Furtividade ou Ladinagem, ou acerte alvo sob condição, sofre 2d6 psíquico por círculo máximo.",
            [],
            sacrario=True,
        ),
        "FRADE_SACRARIO_SOMBRAS": _pf(
            "Sacrário das Sombras",
            "Sacrário (padrão, 3 PM, 3m, cena): área coberta por sombras (camuflagem leve; mortos-vivos também recebem +2 na Defesa e em perícias).",
            [],
            sacrario=True,
        ),
        "FRADE_SACRARIO_COMPARTILHAMENTO": _pf(
            "Sacrário do Compartilhamento",
            "Sacrário sustentado (padrão, 3 PM, 3m): ao lançar magia pessoal de 1º ou 2º círculo em alcance curto, gaste 2 PM para 1 aliado dentro receber o efeito básico.",
            ["7º nível de frade"],
            sacrario=True,
            duracao_sacrario="sustentada",
        ),
        "FRADE_SACRARIO_OCASO": _pf(
            "Sacrário do Ocaso",
            "Sacrário (padrão, 3 PM, 3m): criado com 60 pontos de ocaso (+20/PM extra); no início dos seus turnos perde 1d10 (+1d10/círculo acima do 1º) e cada criatura na área perde esse valor em PV.",
            [],
            sacrario=True,
        ),
        "FRADE_SERMAO_CELERIDADE": _pf(
            "Sermão da Celeridade",
            "1×/rodada, gaste 5 PM para um aliado em alcance curto ganhar 1 ação padrão adicional no próximo turno dele (1×/cena por aliado).",
            ["8º nível de frade"],
            custo_pm=5,
        ),
        "FRADE_SERMAO_EGIDE": _pf(
            "Sermão da Égide",
            "Ação padrão e 3 PM: protege uma criatura em alcance curto até seu próximo turno; ao sofrer dano, pode gastar a proteção para reduzir o dano à metade.",
            [],
            custo_pm=3,
        ),
        "FRADE_TEOLOGIA_APLICADA": _pf(
            "Teologia Aplicada",
            "Escolha duas perícias (exceto ataque): gaste 1 PM para rolar novamente um teste dessas perícias usando Religião. Pode escolher novamente.",
            [],
            custo_pm=1,
        ),
        "FRADE_TRANSFERIR_SACRARIO": _pf(
            "Transferir Sacrário",
            "Ação de movimento e 1 PM: transfere um de seus sacrários para outro ponto dentro do alcance de criação.",
            [],
            custo_pm=1,
        ),
        "FRADE_ZELADOR_VINHEDOS": _pf(
            "Zelador dos Vinhedos",
            "Usa Ofício (cozinheiro) para preparar poções de magias conhecidas (alvo 1 criatura) em forma de bebidas comuns ou especiais (ingerir é ação padrão).",
            ["Treinado em Ofício (cozinheiro)"],
        ),
    }
)
