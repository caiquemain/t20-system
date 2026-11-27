# -*- coding: utf-8 -*-
"""Novos Poderes Concedidos dos 20 Deuses Maiores — Deuses de Arton (Cap. 1, p. 42–47)."""
from typing import Any, Dict, List
from .dados_suplementos import FONTE_DEUSES

_F = FONTE_DEUSES


def _pc(
    nome: str,
    deuses: List[str],
    descricao: str,
    efeitos: Dict[str, Any] | None = None,
    custo_pm: int = 0,
    magico: bool = False,
) -> Dict[str, Any]:
    ef = dict(efeitos or {})
    if custo_pm and "custo_pm" not in ef:
        ef["custo_pm"] = custo_pm
    if magico:
        ef["magico"] = True
    if not ef:
        ef["nota"] = descricao
    reqs = [f"Devoto de {' ou '.join(deuses)}"]
    return {
        "nome": nome,
        "tipo": "Poder Concedido",
        "fonte": _F,
        "deuses": list(deuses),
        "requisitos": reqs,
        "descricao": descricao,
        "efeitos": ef,
    }


DADOS_PODERES_CONCEDIDOS_DEUSES: Dict[str, Dict[str, Any]] = {
    "Abraço da Fênix": _pc(
        "Abraço da Fênix",
        ["Thyatis"],
        "Imune a fogo; se fosse sofrer dano mágico de fogo, cura PV igual à metade desse dano (ou completo se já faz isso por outro efeito).",
        {"imunidade": ["Fogo"], "absorve_fogo_magico": True},
    ),
    "Adaga Noturna": _pc(
        "Adaga Noturna",
        ["Tenebra"],
        "1 PM: arma de perfuração em uso causa +1d6 de dano de frio até o fim da cena.",
        custo_pm=1,
        magico=True,
    ),
    "A Ferramenta Certa": _pc(
        "A Ferramenta Certa",
        ["Hyninn"],
        "1 PM: faz uma ferramenta ou equipamento de aventura de até T$ 400 aparecer em sua mão ou espaço adjacente até o fim da cena.",
        custo_pm=1,
        magico=True,
    ),
    "Alimentar-se do Pavor": _pc(
        "Alimentar-se do Pavor",
        ["Kallyadranoch", "Megalokk"],
        "Quando uma criatura em alcance curto sob medo morre, recebe PV temporários iguais ao dobro do ND dela até o fim da cena.",
    ),
    "Alma de Mudança": _pc(
        "Alma de Mudança",
        ["Thwor", "Valkaria"],
        "No início de cada aventura, pode trocar até Sabedoria poderes por outros cujos pré-requisitos cumpra (não pode trocar este poder).",
    ),
    "Andarilho Carregado": _pc(
        "Andarilho Carregado",
        ["Valkaria"],
        "Mochila de aventureiro não conta no limite de itens vestidos; vestindo-a, pode usar Sabedoria em vez de Força para limite de carga.",
    ),
    "Armadilha Divina": _pc(
        "Armadilha Divina",
        ["Hyninn"],
        "Recebe um poder de Armadilha do caçador à escolha, podendo prepará-la sem materiais propícios.",
        magico=True,
    ),
    "Armadura de Ossos": _pc(
        "Armadura de Ossos",
        ["Tenebra"],
        "Ação de movimento e 2 PM: +2 na Defesa e em Intimidação e RD corte/frio/trevas 5 até o fim da cena.",
        custo_pm=2,
        magico=True,
    ),
    "Armas da Destruição": _pc(
        "Armas da Destruição",
        ["Arsenal"],
        "Recebe +1 nas rolagens de dano e no multiplicador de crítico com armas nas quais é proficiente.",
        {"dano_armas_bonus": 1, "multiplicador_critico_bonus": 1},
    ),
    "Armas da Selvageria": _pc(
        "Armas da Selvageria",
        ["Megalokk"],
        "Armas naturais são armas favoritas de Megalokk: +2 em dano com elas e Abençoar Arma/Armamento da Natureza afetam todas sem custo adicional.",
        {"dano_armas_naturais_bonus": 2},
    ),
    "Aventureiro Inquieto": _pc(
        "Aventureiro Inquieto",
        ["Valkaria"],
        "1×/busca: rerrola um teste recém-realizado; em recompensas/castigos aleatórios de busca, rola dois dados e escolhe.",
    ),
    "Baforada Dracônica": _pc(
        "Baforada Dracônica",
        ["Kallyadranoch"],
        "Escolha um elemento: 1×/rodada, gaste até Con PM para sopro em alcance curto causando 1d10/PM (Ref CD Con metade). Recarga (movimento).",
        custo_pm=1,
    ),
    "Barreira de Coral": _pc(
        "Barreira de Coral",
        ["Oceano"],
        "Movimento e 3 PM: +5 na Defesa pela cena e atacantes corpo a corpo sofrem 1d6+Con perfuração (+1d6 por patamar acima de iniciante).",
        custo_pm=3,
        magico=True,
    ),
    "Belo Presente": _pc(
        "Belo Presente",
        ["Wynna"],
        "1×/cena, ação padrão e Religião (CD 15 + PM): pode lançar até o próximo turno uma magia vista nesta aventura (de círculo acessível).",
    ),
    "Biblioteca Divina": _pc(
        "Biblioteca Divina",
        ["Tanna-Toh"],
        "Recebe 1 perícia treinada (+1 perícia treinada a cada patamar acima de iniciante).",
        {"pericia_escolha_por_patamar": 1},
    ),
    "Cancioneiro da Esperança": _pc(
        "Cancioneiro da Esperança",
        ["Marah"],
        "Padrão e 2 PM: até Car criaturas em alcance curto recebem +2 em testes (exceto ataque) e +3m deslocamento pela cena (perde se agir hostilmente).",
        custo_pm=2,
    ),
    "Cerimonialista Divino": _pc(
        "Cerimonialista Divino",
        ["Lin-Wu"],
        "1×/dia, 1h: afeta 1+Car criaturas por 1 dia; teste de Religião (+Car) dá 1 dado de auxílio (+1d6, ou +1d8 com T$ 25) a cada 10 pontos.",
    ),
    "Chamado Monstruoso": _pc(
        "Chamado Monstruoso",
        ["Megalokk"],
        "Aprende e pode lançar Conjurar Monstro sem violar O&R (–1 PM se aprender novamente).",
        {"magia_adicional": {"nome": "Conjurar Monstro", "atributo": "Sab"}},
        magico=True,
    ),
    "Companheiro Celeste": _pc(
        "Companheiro Celeste",
        ["Lena", "Marah"],
        "Recebe um luminar parceiro iniciante (reposição: 1 dia e T$ 100).",
    ),
    "Companheiro Silvestre": _pc(
        "Companheiro Silvestre",
        ["Allihanna"],
        "Recebe um espírito da natureza parceiro perseguidor iniciante ou bogum iniciante (reposição: 1 dia e T$ 100).",
    ),
    "Convicção Ambiciosa": _pc(
        "Convicção Ambiciosa",
        ["Valkaria"],
        "Em desvantagem (dobro de inimigos ou ND maior que o grupo), +2 em perícias pela cena; se houver inimigo ND ≥ seu nível, +1 ação padrão no 1º turno.",
    ),
    "Corromper Equipamento": _pc(
        "Corromper Equipamento",
        ["Aharadak"],
        "2 PM: arma, escudo ou esotérico empunhado ganha benefícios de matéria vermelha pela cena (–1 PM em Armamento Aberrante).",
        custo_pm=2,
    ),
    "Curar o Espírito": _pc(
        "Curar o Espírito",
        ["Lena"],
        "Ação completa e Carisma CD 10: criatura tocada recupera 1d4+1 PM (1×/dia por criatura).",
    ),
    "Discurso Conciliador": _pc(
        "Discurso Conciliador",
        ["Marah"],
        "Em Diplomacia para mudar atitude, rola dois dados e usa o melhor ou ambos cumulativamente.",
    ),
    "Dom da Furtividade": _pc(
        "Dom da Furtividade",
        ["Hyninn"],
        "Soma Sabedoria em Furtividade e penalidade para se esconder após conjurar cai para –10.",
        {"pericia_soma_atributo": {"Furtividade": "sab"}},
    ),
    "Dom da Vontade": _pc(
        "Dom da Vontade",
        ["Khalmyr"],
        "+2 em Vontade e 1×/cena, ao passar em Vontade contra inimigo ou perigo, recebe 1d4 PM temporários.",
        {"bonus_pericia": {"Vontade": 2}},
    ),
    "Dom dos Segredos": _pc(
        "Dom dos Segredos",
        ["Sszzaas"],
        "Padrão e 2 PM: Carisma CD 10 (+2/uso no dia) para aprender e lançar 1 magia de 1º círculo pela cena.",
        custo_pm=2,
    ),
    "Égide dos Mares": _pc(
        "Égide dos Mares",
        ["Oceano"],
        "Recebe um espírito das águas parceiro guardião iniciante ou escudeiro iniciante (reposição: 1 dia e T$ 100).",
    ),
    "Espalhar a Corrupção": _pc(
        "Espalhar a Corrupção",
        ["Aharadak"],
        "1 dia e Religião CD 20 em comunidade: por 1 semana, atitude das pessoas entre si piora em 1 passo.",
    ),
    "Espírito Animal": _pc(
        "Espírito Animal",
        ["Allihanna"],
        "Movimento e 2 PM (+PM até Sab para +5 PV temp/PM): não pode ser flanqueado, +10 PV temporários e arma natural 1d6 (1 PM ataque extra 1×/rodada).",
        custo_pm=2,
        magico=True,
    ),
    "Espírito do Conhecimento": _pc(
        "Espírito do Conhecimento",
        ["Tanna-Toh"],
        "Padrão e 2 PM: invoca manifestação Minúscula (voo 6m, Def 15, 1 PV) pela cena; percebe por ela e lança magias a partir dela.",
        custo_pm=2,
        magico=True,
    ),
    "Estouro da Trobada": _pc(
        "Estouro da Trobada",
        ["Allihanna"],
        "Completa e 2 PM (sustentada): convoca manada Enorme em alcance curto; movimento move 12m causando 3d6 impacto e derrubando (Fort CD Sab metade/evita).",
        custo_pm=2,
    ),
    "Exaltar Honra": _pc(
        "Exaltar Honra",
        ["Lin-Wu"],
        "2 PM: aura 9m pela cena; devotos de Lin-Wu e códigos de conduta ganham +5 Diplomacia/Nobreza; todos sofrem –5 em Enganação/Furtividade/Ladinagem.",
        custo_pm=2,
    ),
    "Expurgar a Derrota": _pc(
        "Expurgar a Derrota",
        ["Arsenal"],
        "Com 0 PM, pode gastar PV (não temporários) no lugar de mana na taxa 3 PV = 1 PM (sem reduzir a 0 PV; só recupera com descanso).",
    ),
    "Familiar Elemental": _pc(
        "Familiar Elemental",
        ["Wynna"],
        "Recebe um familiar adepto iniciante ou familiar elemental iniciante (reposição: 1 dia e T$ 100).",
    ),
    "Ferramentas da Guerra": _pc(
        "Ferramentas da Guerra",
        ["Arsenal"],
        "1×/dia, 1h e T$ 10/item (até Sab itens): armas +2 dano, armaduras/escudos RD 2 por 1 dia (destruído se usuário for derrotado).",
        magico=True,
    ),
    "Golpe Semântico": _pc(
        "Golpe Semântico",
        ["Tanna-Toh"],
        "Pode substituir testes de Diplomacia e Intimidação por Conhecimento.",
    ),
    "Golpe Tempestuoso": _pc(
        "Golpe Tempestuoso",
        ["Oceano"],
        "Ao acertar ataque corpo a corpo, gaste 2 PM para empurrar 3m e deixar desprevenido por 1 rodada.",
        custo_pm=2,
    ),
    "Imolação Sagrada": _pc(
        "Imolação Sagrada",
        ["Azgher", "Thyatis"],
        "Padrão e 1 PM (sustentada): seus ataques corpo a corpo causam +1d6 pontos de dano de fogo.",
        custo_pm=1,
        magico=True,
    ),
    "Júbilo na Dor": _pc(
        "Júbilo na Dor",
        ["Aharadak"],
        "Quando causa ou sofre dano, recebe RD 1 cumulativa (máx. Sabedoria); termina se passar 1 rodada sem causar nem sofrer dano.",
    ),
    "Jurista Divino": _pc(
        "Jurista Divino",
        ["Lin-Wu", "Khalmyr"],
        "Usa Sabedoria em Nobreza (em vez de Inteligência) e pode usar Nobreza no lugar de Diplomacia e Intimidação.",
        {"pericia_atributo_opcao": {"Nobreza": "sab"}},
    ),
    "Magia Caótica": _pc(
        "Magia Caótica",
        ["Nimb"],
        "Ao lançar magia, gaste +2 PM para calcular a CD com 1d20 + modificadores (em vez de 10 + modificadores).",
        custo_pm=2,
    ),
    "Magia Piedosa": _pc(
        "Magia Piedosa",
        ["Lena", "Thyatis"],
        "Quando lança uma magia de dano, pode fazer com que ela cause dano não letal.",
    ),
    "Magia Venenosa": _pc(
        "Magia Venenosa",
        ["Sszzaas"],
        "Magias com resistência Fortitude ganham aprimoramento +1 PM: alvos que falhem perdem 1d12 PV por veneno (1d6 se passarem).",
        custo_pm=1,
    ),
    "Manto Ardiloso": _pc(
        "Manto Ardiloso",
        ["Sszzaas"],
        "Aprende Disfarce Ilusório (CD Car; –1 PM se aprender novamente) e +10 em Diplomacia para mudar atitude na 1ª interação disfarçado.",
        {"magia_adicional": {"nome": "Disfarce Ilusório", "atributo": "Car"}},
        magico=True,
    ),
    "Mar Revolto": _pc(
        "Mar Revolto",
        ["Oceano"],
        "1 PM (sustentada): aura 6m; no início de seus turnos, alvos escolhidos fazem Acrobacia (CD Sab, +5 na água) para não cair.",
        custo_pm=1,
        magico=True,
    ),
    "Mediador da Tempestade": _pc(
        "Mediador da Tempestade",
        ["Aharadak"],
        "Comunica-se livremente com lefeu inteligentes (Int –3+) e +5 em Diplomacia e Intuição com criaturas da Tormenta e devotos de Aharadak.",
    ),
    "Mestre de Si": _pc(
        "Mestre de Si",
        ["Lin-Wu"],
        "Passa automaticamente no primeiro teste de Vontade contra efeito de inimigo em cada cena.",
    ),
    "Mordida de Víbora": _pc(
        "Mordida de Víbora",
        ["Sszzaas"],
        "Arma natural mordida (1d6, x2, perfuração) que armazena até 2 venenos de contato; 1×/rodada, 1 PM para ataque extra de mordida.",
        {"arma_natural": {"nome": "Mordida de Víbora", "dano": "1d6", "critico": "x2", "tipo": "Perfuração"}},
        custo_pm=1,
    ),
    "Navegador Sagrado": _pc(
        "Navegador Sagrado",
        ["Oceano"],
        "Usa Sabedoria em Pilotagem e, em embarcação aquática, suas magias divinas custam –2 PM.",
        {"pericia_atributo_opcao": {"Pilotagem": "sab"}},
    ),
    "Nimb": _pc(
        "Nimb",
        ["Nimb"],
        "Padrão e 2 PM: rola 1d6 na coluna de Área/Alvo e 1d6 na coluna de Efeito para gerar uma habilidade caótica única.",
        custo_pm=2,
        magico=True,
    ),
    "O Dobro ou Nada": _pc(
        "O Dobro ou Nada",
        ["Hyninn", "Nimb"],
        "Em habilidade com custo PM (não magia), paga o dobro para +5 na CD; se algum alvo passar, fica alquebrado.",
    ),
    "O Futuro que Vier Disso": _pc(
        "O Futuro que Vier Disso",
        ["Thwor"],
        "Soma 1 dado à escolha (d4 a d20) em um teste; o mestre recebe o mesmo dado como penalidade em um teste futuro seu (até usá-lo).",
    ),
    "O Sol que nos Aquece": _pc(
        "O Sol que nos Aquece",
        ["Allihanna", "Azgher"],
        "Padrão e 2 PM: aura de luz solar 6m; habilidades mágicas de fogo/luz/plantas custam –1 PM e mortos-vivos/sensíveis à luz ficam vulneráveis.",
        custo_pm=2,
        magico=True,
    ),
    "Palavra de Poder": _pc(
        "Palavra de Poder",
        ["Tanna-Toh"],
        "Aprende e pode lançar Comando (–1 PM se aprender novamente).",
        {"magia_adicional": {"nome": "Comando", "atributo": "Sab"}},
        magico=True,
    ),
    "Passo Sombrio": _pc(
        "Passo Sombrio",
        ["Tenebra"],
        "1×/rodada, 2 PM: teleporta para espaço desocupado em alcance curto (–1 PM se ambos sob escuridão; não funciona se imóvel).",
        custo_pm=2,
        magico=True,
    ),
    "Perceber Farsas": _pc(
        "Perceber Farsas",
        ["Tanna-Toh"],
        "Recebe +5 em Intuição e imunidade a efeitos de ilusão.",
        {"bonus_pericia": {"Intuição": 5}, "imunidade": ["Ilusão"]},
    ),
    "Pilar de Heredrimm": _pc(
        "Pilar de Heredrimm",
        ["Khalmyr"],
        "2 PM: +2 na Defesa e RD 5 pela cena (ou até encerrar como livre), mas deslocamento reduzido à metade.",
        custo_pm=2,
    ),
    "Poder do Vínculo": _pc(
        "Poder do Vínculo",
        ["Wynna"],
        "Movimento e até círculo máximo em PM: toca conjurador para reduzir o custo da próxima magia dele no mesmo valor.",
        custo_pm=1,
    ),
    "Poder Sem Limites": _pc(
        "Poder Sem Limites",
        ["Kallyadranoch"],
        "CD e limites de PM de suas habilidades (exceto magias) aumentam em valor igual ao seu patamar.",
    ),
    "Proeminência Solar": _pc(
        "Proeminência Solar",
        ["Azgher"],
        "Magias de dano de fogo com resistência ganham aprimoramento +1 PM: alvos que falhem ficam em chamas e lentos até apagarem.",
        custo_pm=1,
    ),
    "Quebrar Encanto": _pc(
        "Quebrar Encanto",
        ["Khalmyr"],
        "+2 em ataque para quebrar; ao usar quebrar, gaste 2 PM para aplicar Dissipar Magia no item e portador.",
        custo_pm=2,
        magico=True,
    ),
    "Redirecionar Destino": _pc(
        "Redirecionar Destino",
        ["Thyatis"],
        "No início do dia rola 1d20; 1×/rodada, 3 PM para trocar o d20 de um teste em alcance curto pelo valor anotado.",
        custo_pm=3,
        magico=True,
    ),
    "Remorso do Belicista": _pc(
        "Remorso do Belicista",
        ["Marah"],
        "1×/rodada, ao sofrer dano de inimigo, 1 PM: ele sofre –2 cumulativo em ataques e dano pela cena (mental).",
        custo_pm=1,
    ),
    "Resplendor Divino": _pc(
        "Resplendor Divino",
        ["Azgher"],
        "2 PM: aura de luz solar 9m pela cena; remove toda camuflagem por escuridão e efeitos semelhantes.",
        custo_pm=2,
        magico=True,
    ),
    "Saque Celestial": _pc(
        "Saque Celestial",
        ["Lin-Wu"],
        "1 PM: saca/guarda arma como livre; se atacar corpo a corpo no mesmo turno, +2 ataque e +2 passos de dano (1×/cena por criatura).",
        custo_pm=1,
    ),
    "Só os Loucos Sabem": _pc(
        "Só os Loucos Sabem",
        ["Nimb"],
        "Rola duas perícias aleatórias e fica treinado nelas (+3 se já treinado); no início do dia, 3 PM para rolar novas.",
        custo_pm=3,
    ),
    "Sorvo de Mana": _pc(
        "Sorvo de Mana",
        ["Wynna"],
        "Sempre que falhar no teste de resistência contra uma magia de inimigo, recupera PM igual ao círculo dela.",
    ),
    "Temor Arcano": _pc(
        "Temor Arcano",
        ["Kallyadranoch"],
        "Quando inimigo em alcance médio sob medo falha em TR contra sua magia, ganha 1 PM temporário cumulativo (máx. nível/cena).",
    ),
    "Terror Profundo": _pc(
        "Terror Profundo",
        ["Kallyadranoch", "Megalokk", "Thwor"],
        "Recebe +2 em Intimidação e na CD de seus efeitos de medo.",
        {"bonus_pericia": {"Intimidação": 2}},
    ),
    "Toque de Não Vida": _pc(
        "Toque de Não Vida",
        ["Tenebra"],
        "Movimento e 2 PM: fornece a si mesmo ou adjacente 2d12 PV temporários e camuflagem leve enquanto durarem.",
        custo_pm=2,
        magico=True,
    ),
    "Transbordar Cura": _pc(
        "Transbordar Cura",
        ["Lena"],
        "PV excedentes de seus efeitos de cura viram PV temporários (máx. 2× nível do alvo).",
    ),
    "Trilha Desimpedida": _pc(
        "Trilha Desimpedida",
        ["Allihanna"],
        "Aprende e pode lançar Caminhos da Natureza (–1 PM se aprender novamente).",
        {"magia_adicional": {"nome": "Caminhos da Natureza", "atributo": "Sab"}},
        magico=True,
    ),
    "Ushultt": _pc(
        "Ushultt",
        ["Thwor"],
        "Escolhe 1 aliado como ushultt (troca 1×/aventura): em alcance curto um do outro, +2 ataque e dano (+3 se também duyshidakk).",
    ),
    "Vitória a Qualquer Custo": _pc(
        "Vitória a Qualquer Custo",
        ["Arsenal"],
        "Em teste de ataque, resistência ou Guerra, gaste 2 PM para rerrolar (+1 PM a cada rerrolagem adicional no mesmo teste).",
        custo_pm=2,
    ),
}
