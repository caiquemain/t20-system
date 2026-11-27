# -*- coding: utf-8 -*-
"""Novos Poderes Gerais — Heróis de Arton (Cap. 1, p. 78–95).

Inclui:
- 24 Poderes de Combate (Tabela 1-18, p. 78–79)
- 14 Poderes de Destino (Tabela 1-19, p. 80–82)
- 14 Poderes de Magia (Tabela 1-20, p. 82–83)
- 6 Poderes da Tormenta (Tabela 1-21, p. 83)
- 56 Poderes de Raça (Tabela 1-22, p. 84–91)
- 19 Poderes de Grupo (Tabela 1-23, p. 92–95)
"""
from typing import Dict, Any, List
from .dados_suplementos import FONTE_HEROIS


def _pg(
    nome: str,
    tipo: str,
    descricao: str,
    requisitos: List[str] | None = None,
    efeitos: Dict[str, Any] | None = None,
    custo_pm: int = 0,
    racas: List[str] | None = None,
) -> Dict[str, Any]:
    ef: Dict[str, Any] = dict(efeitos or {})
    if custo_pm and "custo_pm" not in ef:
        ef["custo_pm"] = custo_pm
    if not ef:
        ef["nota"] = descricao
    d: Dict[str, Any] = {
        "nome": nome,
        "tipo": tipo,
        "descricao": descricao,
        "fonte": FONTE_HEROIS,
        "requisitos": list(requisitos or []),
        "efeitos": ef,
    }
    if custo_pm:
        d["custo_pm"] = custo_pm
    if racas:
        d["racas"] = list(racas)
    return d


# =====================================================================
# 1. PODERES DE COMBATE (24 — Tabela 1-18, p. 78–79)
# =====================================================================

_COMBATE: Dict[str, Dict[str, Any]] = {
    "HA_Arremesso_Devastador": _pg("Arremesso Devastador", "Poder Geral (Combate)", "Em ataque à distância com arma de arremesso, gaste 1 PM: se acertar, faz manobra derrubar ou empurrar usando o resultado do ataque.", ["Arremesso Potente"], custo_pm=1),
    "HA_Ataque_com_o_Cabo": _pg("Ataque com o Cabo", "Poder Geral (Combate)", "1×/rodada, ao agredir com arma alongada, gaste 1 PM para ataque extra com o cabo (1d6 impacto, x2).", ["Estilo de Arma Longa"], custo_pm=1),
    "HA_Ataque_em_Arco": _pg("Ataque em Arco", "Poder Geral (Combate)", "Em ataque corpo a corpo, gaste 2 PM para acertar até 3 criaturas adjacentes entre si no alcance (ou +50% dano contra bando).", ["Treinado em Luta", "4º nível"], custo_pm=2),
    "HA_Bravura_Indomita": _pg("Bravura Indômita", "Poder Geral (Combate)", "Adjacente a 2+ inimigos aptos a atacá-lo, recebe +2 em ataques e na margem de ameaça.", ["Treinado em Vontade"]),
    "HA_Briga_de_Rua": _pg("Briga de Rua", "Poder Geral (Combate)", "1×/rodada, ao fintar, gaste 1 PM: se vencer, faz ataque desarmado como ação livre causando +2d6 dano.", ["Briga ou Estilo Desarmado"], custo_pm=1),
    "HA_Chuva_de_Golpes": _pg("Chuva de Golpes", "Poder Geral (Combate)", "Ao atacar com duas armas via Estilo de Duas Armas, pode fazer 1 ataque desarmado adicional.", ["Briga ou Estilo Desarmado", "Estilo de Duas Armas"]),
    "HA_Catafractario": _pg("Catafractário", "Poder Geral (Combate)", "Montado e de armadura pesada, recebe +1 Defesa por nível de parceiro da montaria.", ["Encouraçado", "Ginete"]),
    "HA_Contra_Ataque": _pg("Contra-Ataque", "Poder Geral (Combate)", "1×/rodada, se uma criatura atacá-lo e errar, gaste 2 PM para fazer 1 ataque corpo a corpo contra ela.", ["Combate Defensivo"], custo_pm=2),
    "HA_Coragem_Aguerrida": _pg("Coragem Aguerrida", "Poder Geral (Combate)", "Com metade ou menos dos PV totais, recebe +2 em testes de perícia e na Defesa.", ["Treinado em Vontade"]),
    "HA_Corte_Lacerante": _pg("Corte Lacerante", "Poder Geral (Combate)", "Com arma corpo a corpo de corte, gaste 2 PM: se acertar, causa +1d10 dano e deixa o alvo sangrando.", ["Treinado em Luta"], custo_pm=2),
    "HA_Defesa_Armada": _pg("Defesa Armada", "Poder Geral (Combate)", "Usando arma corpo a corpo de duas mãos, recebe +2 na Defesa e em Fortitude.", ["Estilo de Duas Mãos"]),
    "HA_Encastelado": _pg("Encastelado", "Poder Geral (Combate)", "Usando armadura pesada, recebe RD 2 (+1 por outro poder que tenha Encouraçado como pré-requisito).", ["Encouraçado", "5º nível"]),
    "HA_Escudo_Heroico": _pg("Escudo Heroico", "Poder Geral (Combate)", "Empunha/solta escudo como livre e pode arremessá-lo (alcance curto); 1 PM para retornar ou ricochetear (-5 cumulativo).", ["Ataque com Escudo"], custo_pm=1),
    "HA_Estocada_Pungente": _pg("Estocada Pungente", "Poder Geral (Combate)", "Com arma corpo a corpo de perfuração, gaste 2 PM: se acertar, alvo sofre -5 em rolagens de dano por 1 rodada.", ["Treinado em Luta"], custo_pm=2),
    "HA_Estudar_Adversario": _pg("Estudar o Adversário", "Poder Geral (Combate)", "Na 1ª vez/rodada em que erra um ataque, recebe +2 cumulativo em ataques contra o mesmo alvo até o fim da cena.", ["Int 1"]),
    "HA_Firula_Inspiradora": _pg("Firula Inspiradora", "Poder Geral (Combate)", "Ação de movimento e 1 PM: teste de Atuação CD 10 dá +1 (+1 a cada 10 acima) em perícias e Defesa até o próximo turno.", [], custo_pm=1),
    "HA_Matador_Monstros": _pg("Matador de Monstros", "Poder Geral (Combate)", "+1d10 em dano contra criaturas Grandes ou maiores; elas não recebem bônus de tamanho em manobras contra você.", ["5º nível"]),
    "HA_Mobilidade": _pg("Mobilidade", "Poder Geral (Combate)", "Ao usar movimentar-se por pelo menos 6m, recebe +2 em ataques e Defesa até o próximo turno.", ["Esquiva"]),
    "HA_Na_Mosca": _pg("Na Mosca", "Poder Geral (Combate)", "Em ataque à distância, gaste 1 PM: se acertar, causa +1 dado extra de dano do mesmo tipo.", ["Estilo de Arremesso ou Estilo de Disparo"], custo_pm=1),
    "HA_Pancada_Estonteante": _pg("Pancada Estonteante", "Poder Geral (Combate)", "Com arma corpo a corpo de impacto, gaste 2 PM: se acertar, alvo fica desprevenido por 1 rodada.", ["Treinado em Luta"], custo_pm=2),
    "HA_Precisao_Letal": _pg("Precisão Letal", "Poder Geral (Combate)", "A margem de ameaça de seus ataques aumenta em +1.", ["11º nível"], {"margem_ameaca_bonus": 1}),
    "HA_Sanguinario": _pg("Sanguinário", "Poder Geral (Combate)", "Sempre que causar 10+ de dano, recebe +1 cumulativo em rolagens de dano pela cena (máx. Força).", []),
    "HA_Sentinela_Implacavel": _pg("Sentinela Implacável", "Poder Geral (Combate)", "1×/rodada, com arma de disparo carregada, gaste 2 PM para atacar inimigo que se mova dentro do alcance.", ["Sab 1", "Treinado em Iniciativa", "Treinado em Percepção", "Estilo de Disparo"], custo_pm=2),
    "HA_Sequencia_de_Golpes": _pg("Sequência de Golpes", "Poder Geral (Combate)", "Ao acertar ataque corpo a corpo, recebe +1 cumulativo em ataque e dano contra o mesmo alvo no turno (máx. Força).", []),
    "HA_Truque_Mao_Lesta": _pg("Truque da Mão Lesta", "Poder Geral (Combate)", "Com arma corpo a corpo em 1 mão e nada na outra, 1×/cena por inimigo adjacente: deixa desprevenido no turno e +2 passos de dano.", ["Estilo de Uma Arma"]),
}


# =====================================================================
# 2. PODERES DE DESTINO (14 — Tabela 1-19, p. 80–82)
# =====================================================================

_DESTINO: Dict[str, Dict[str, Any]] = {
    "HA_Alma_Livre": _pg("Alma Livre", "Poder Geral (Destino)", "Escolha uma classe: você pode escolher um poder dessa classe usando seu nível de personagem -4 como nível na classe.", []),
    "HA_Andarilho_Urbano": _pg("Andarilho Urbano", "Poder Geral (Destino)", "Em uma cidade, recebe +2 na Defesa, em Enganação e em Investigação.", []),
    "HA_Caricias_Revigorantes": _pg("Carícias Revigorantes", "Poder Geral (Destino)", "1 minuto e 2 PM: recupera 2d4 PM de criatura adjacente (1×/dia por criatura).", ["Car 2", "Sedução Lasciva"], custo_pm=2),
    "HA_Diligente": _pg("Diligente", "Poder Geral (Destino)", "Ação de movimento: +2 em um teste de perícia (exceto ataques, máx. ação completa) até o fim do próximo turno.", []),
    "HA_Foco_em_Habilidade": _pg("Foco em Habilidade", "Poder Geral (Destino)", "Escolha uma habilidade (não magia): a CD para resistir a ela aumenta em +2. Pode escolher várias vezes para habilidades diferentes.", []),
    "HA_Grandao": _pg("Grandão", "Poder Geral (Destino)", "Conta como 1 categoria de tamanho maior para Furtividade, manobras, espaço e alcance natural, e capacidade de carga +5 espaços.", ["Con 2"], {"carga_max_bonus": 5}),
    "HA_Heroi_Sete_Instrumentos": _pg("Herói dos Sete Instrumentos", "Poder Geral (Destino)", "Recebe +1 em testes de perícias nas quais não é treinado (+2 no 7º nível, +3 no 15º).", []),
    "HA_Impostor": _pg("Impostor", "Poder Geral (Destino)", "1×/cena, gaste 2 PM para usar Enganação no lugar de outra perícia (máx. ação completa).", ["Car 3", "Foco em Perícia (Enganação)"], custo_pm=2),
    "HA_Lideranca_Inspiradora": _pg("Liderança Inspiradora", "Poder Geral (Destino)", "Posiciona capangas como ação padrão e 1×/rodada gasta ação livre para movê-los ou causar dano.", ["Car 1"]),
    "HA_Meditacao_Autoafirmativa": _pg("Meditação Autoafirmativa", "Poder Geral (Destino)", "Medita por 1+ dias (fascinado) e testa Carisma (CD 15–25) para ganhar bônus de ataque, Defesa, TR, perícia ou poder por 1 semana.", ["Sab 1", "Car 1", "5º nível"]),
    "HA_Pose_Assustadora": _pg("Pose Assustadora", "Poder Geral (Destino)", "Recebe +2 em Intimidação e pode gastar 1 PM para assustar como ação de movimento.", ["Car 1", "Treinado em Intimidação"], {"bonus_pericia": {"Intimidação": 2}}, custo_pm=1),
    "HA_Seducao_Lasciva": _pg("Sedução Lasciva", "Poder Geral (Destino)", "Minutos de interação e 3 PM: Enganação oposta a Vontade deixa alvo enfeitiçado por 1 dia.", ["Car 1", "Treinado em Enganação"], custo_pm=3),
    "HA_Ventriloquismo": _pg("Ventriloquismo", "Poder Geral (Destino)", "1 PM: faz sua voz parecer vir de outro lugar por 1 rodada.", ["Treinado em Atuação", "Treinado em Enganação"], custo_pm=1),
}


# =====================================================================
# 3. PODERES DE MAGIA (14 — Tabela 1-20, p. 82–83)
# =====================================================================

_MAGIA: Dict[str, Dict[str, Any]] = {
    "HA_Barreira_Mistica": _pg("Barreira Mística", "Poder Geral (Magia)", "Ao lançar uma magia, gaste 1 PM para receber +4 na Defesa até o início do próximo turno.", ["Lançar magias"], custo_pm=1),
    "HA_Esoterismo": _pg("Esoterismo", "Poder Geral (Magia)", "Ao lançar magia, pague 2 PM para canalizá-la através de dois itens esotéricos diferentes simultaneamente.", ["Lançar magias de 2º círculo"], custo_pm=2),
    "HA_Estilo_Esoterico": _pg("Estilo Esotérico", "Poder Geral (Magia)", "1×/rodada, ao agredir em corpo a corpo empunhando item esotérico, gaste 2 PM para lançar uma magia como ação livre.", ["Treinado em Luta", "Treinado em Misticismo", "5º nível"], custo_pm=2),
    "HA_Encantar_Itens_Menores": _pg("Encantar Itens Menores", "Poder Geral (Magia)", "Encanta itens mágicos menores permanentes usando Misticismo (arcano) ou Religião (divino) sobre item base existente.", ["Lançar magias de 3º círculo", "Treinado em Misticismo ou Religião"]),
    "HA_Encantar_Itens_Medios": _pg("Encantar Itens Médios", "Poder Geral (Magia)", "Como Encantar Itens Menores, para itens mágicos médios permanentes.", ["Lançar magias de 4º círculo", "Encantar Itens Menores"]),
    "HA_Encantar_Itens_Maiores": _pg("Encantar Itens Maiores", "Poder Geral (Magia)", "Como Encantar Itens Menores, para itens mágicos maiores permanentes.", ["Lançar magias de 5º círculo", "Encantar Itens Médios"]),
    "HA_Especializacao_em_Magia": _pg("Especialização em Magia", "Poder Geral (Magia)", "Escolha uma magia com Foco em Magia: a CD para resistir a ela aumenta em +2.", ["Foco em Magia"]),
    "HA_Explosao_Fulgente": _pg("Explosão Fulgente", "Poder Geral (Magia)", "Aprimoramento (+1 PM, dano de fogo com TR): alvo que falhar fica cego por 1 rodada (ou ofuscado se já cegado na cena).", ["Lançar magias"], {"aprimoramento_magia": True}, custo_pm=1),
    "HA_Genese_Elemental": _pg("Gênese Elemental", "Poder Geral (Magia)", "Aprimoramento (+3 PM): cria 1d4 (+1/círculo) capangas elementais Pequenos (Def 15, 1d6+1 do elemento).", ["Lançar magias de 2º círculo"], {"aprimoramento_magia": True}, custo_pm=3),
    "HA_Magia_Dividida": _pg("Magia Dividida", "Poder Geral (Magia)", "Aprimoramento (+2 PM): divide a área da magia em duas áreas com metade do tamanho original sem sobreposição.", ["Lançar magias de 2º círculo"], {"aprimoramento_magia": True}, custo_pm=2),
    "HA_Magia_Suspensa": _pg("Magia Suspensa", "Poder Geral (Magia)", "Aumenta execução de magia (movimento/padrão) para completa (+1 CD), 2 rodadas (+2 CD) ou 3 rodadas (+5 CD).", ["Lançar magias"]),
    "HA_Miasma_Toxico": _pg("Miasma Tóxico", "Poder Geral (Magia)", "Aprimoramento (+1 PM, dano de ácido com TR): alvo que falhar fica enjoado por 1 rodada.", ["Lançar magias"], {"aprimoramento_magia": True}, custo_pm=1),
    "HA_Prisao_Gelida": _pg("Prisão Gélida", "Poder Geral (Magia)", "Aprimoramento (+1 PM, dano de frio com TR): alvo que falhar fica enredado por 1 rodada.", ["Lançar magias"], {"aprimoramento_magia": True}, custo_pm=1),
    "HA_Trovao_Retumbante": _pg("Trovão Retumbante", "Poder Geral (Magia)", "Aprimoramento (+1 PM, dano de eletricidade com TR): alvo que falhar fica caído (1×/cena) e surdo.", ["Lançar magias"], {"aprimoramento_magia": True}, custo_pm=1),
}


# =====================================================================
# 4. PODERES DA TORMENTA (6 — Tabela 1-21, p. 83)
# =====================================================================

DADOS_PODERES_TORMENTA_HEROIS: Dict[str, Dict[str, Any]] = {
    "Bolsoes_Insanos": _pg("Bolsões Insanos", "Poder da Tormenta", "Limite de carga +2 espaços (+1 por outro poder da Tormenta) e +5 em Ladinagem para ocultar itens nesses espaços.", [], {"carga_max_bonus": 2}),
    "Carapaca_Corrompida": _pg("Carapaça Corrompida", "Poder da Tormenta", "Recebe RD 1 (+1 para cada dois outros poderes da Tormenta).", ["Carapaça"], {"rd_escalavel_tormenta": {"elementos": ["geral"], "base": 1, "por_poder": 1}}),
    "Repulsivo": _pg("Repulsivo", "Poder da Tormenta", "O 1º ataque de cada inimigo contra você na cena sofre penalidade igual ao total de poderes da Tormenta.", ["Car -1 ou menor"]),
    "Secrecao_Cicatrizante": _pg("Secreção Cicatrizante", "Poder da Tormenta", "Ação padrão e 2 PM: cura 2d6+2 PV (+1d6+1 a cada 2 outros poderes da Tormenta) mas deixa alvo enjoado 1 rodada (Fort CD Con evita).", [], custo_pm=2),
    "Simetria_Radial": _pg("Simetria Radial", "Poder da Tormenta", "Não pode ser flanqueado nem ficar caído e recebe +5 para evitar ser agarrado.", ["Quatro outros poderes da Tormenta"]),
    "Tempo_Mistico": _pg("Tempo Místico", "Poder da Tormenta", "1×/rodada ao lançar magia, gaste 2 PM e perca 1d6/1d8/1d12 PV (só cura com descanso) para reduzir execução em 1/2/3 passos.", ["Dois outros poderes da Tormenta"], custo_pm=2),
}


# =====================================================================
# 5. PODERES DE RAÇA (56 — Tabela 1-22, p. 84–91)
# =====================================================================

def _pr(nome: str, racas: List[str], descricao: str, reqs: List[str] | None = None, efeitos: Dict[str, Any] | None = None, custo_pm: int = 0) -> Dict[str, Any]:
    r_full = [f"Raça: {', '.join(racas)}", *(reqs or [])]
    return _pg(nome, "Poder Geral (Raça)", descricao, r_full, efeitos, custo_pm=custo_pm, racas=racas)


_RACA: Dict[str, Dict[str, Any]] = {
    "HA_Raca_Ajudante_Nato": _pr("Ajudante Nato", ["Qareen"], "Bônus ao ajudar +1; ao flanquear, aliados recebem +3 no ataque."),
    "HA_Raca_Amo": _pr("Amo", ["Qareen"], "Desejos a pedido do amo custa -2 PM, mas sofre -2 em perícias quando o amo está em perigo ou sob condição."),
    "HA_Raca_Arma_Amada": _pr("Arma Amada", ["Anão", "Hobgoblin"], "Escolha uma arma: +2 dano e +5 em manobras contra desarmar e quebrar."),
    "HA_Raca_Arma_Natural_Aprimorada": _pr("Arma Natural Aprimorada", ["Várias"], "Uma arma natural racial aumenta dano em +1 passo e margem de ameaça em +1.", ["Arma natural racial"]),
    "HA_Raca_Arma_Natural_Habil": _pr("Arma Natural Hábil", ["Várias"], "Não precisa gastar 1 PM para ataque extra 1×/rodada com uma arma natural racial.", ["Arma natural racial"]),
    "HA_Raca_Arquearia_Elfica": _pr("Arquearia Élfica", ["Elfo"], "Arcos contam como armas simples e causam +2 de dano."),
    "HA_Raca_Arsenal_Lisandra": _pr("Arsenal de Lisandra", ["Dahllan"], "Aprende Armamento da Natureza (-1 PM se reaprender) e Armadura de Allihanna dá +1 Defesa extra por patamar.", [], {"magias_conhecidas": ["Armamento da Natureza"]}),
    "HA_Raca_Asas_de_Aco": _pr("Asas de Aço", ["Harpia", "Kallyanach", "Pteros", "Suraggel"], "+2 na Defesa e asas viram arma natural (2d4, x2, impacto; 1 PM ataque extra se não voando).", ["Possuir asas"], {"defesa_bonus": 2}),
    "HA_Raca_Asas_Extraplanares": _pr("Asas Extraplanares", ["Suraggel"], "Gaste 1 PM/rodada para voar 12m (fica vulnerável enquanto voa).", [], custo_pm=1),
    "HA_Raca_Atracao_Polvora": _pr("Atração pela Pólvora", ["Anão", "Goblin", "Hobgoblin", "Kliren"], "+1 ataque e +2 dano com armas de fogo; +1 dano/dado com bombas e pólvora.", ["Treinado em Ofício (alquimista)"]),
    "HA_Raca_Camuflagem_Mimetica": _pr("Camuflagem Mimética", ["Sereia/Tritão", "Trog"], "Ação de movimento e 2 PM: +10/+5/+2 em Furtividade pela cena conforme armadura/itens vestidos.", [], custo_pm=2),
    "HA_Raca_Canto_Sereia": _pr("Canto da Sereia", ["Sereia/Tritão"], "+2 em Atuação; magias de Canção dos Mares ganham +1 passo de alcance e +2 CD.", [], {"bonus_pericia": {"Atuação": 2}}),
    "HA_Raca_Cascos_Poderosos": _pr("Cascos Poderosos", ["Centauro", "Minotauro", "Sátiro"], "1 PM em ataque desarmado para usar cascos (+1 dado de dano, apenas letal).", [], custo_pm=1),
    "HA_Raca_Chassi_Gracioso": _pr("Chassi Gracioso", ["Golem"], "+2 em Diplomacia e remove penalidade de armadura de Chassi.", [], {"bonus_pericia": {"Diplomacia": 2}}),
    "HA_Raca_Citadino": _pr("Citadino", ["Humano", "Hynne", "Kliren", "Meio-Elfo"], "+2 em perícias baseadas em Carisma (exceto Adestramento).", [], {"bonus_pericia": {"Atuação": 2, "Diplomacia": 2, "Enganação": 2, "Intimidação": 2, "Jogatina": 2}}),
    "HA_Raca_Comandar_Aprimorado": _pr("Comandar Aprimorado", ["Humano"], "Ao usar Comandar, gaste +2 PM para aumentar o bônus em +1.", ["Car 2", "Comandar"], custo_pm=2),
    "HA_Raca_Conforto_Aco": _pr("Conforto do Aço", ["Anão"], "Sem penalidade de armadura por armaduras (escudos ainda aplicam) e +2 Defesa usando armadura pesada.", [], {"defesa_bonus_armadura_pesada": 2}),
    "HA_Raca_Constricao_Atroz": _pr("Constrição Atroz", ["Dahllan"], "Ação de movimento e 1 PM (sustentada): inimigos em alcance curto testam Ref CD Sab ou ficam enredados.", [], custo_pm=1),
    "HA_Raca_Coracao_Pedra": _pr("Coração de Pedra", ["Anão", "Medusa"], "+1 PV por nível e imunidade a petrificação.", [], {"pv_max_nivel": 1, "imunidade": ["Petrificação"]}),
    "HA_Raca_Coro_Sibilante": _pr("Coro Sibilante", ["Medusa"], "1 PM: +2 em perícias originalmente baseadas em Carisma pela cena.", [], custo_pm=1),
    "HA_Raca_Crescimento_Feerico": _pr("Crescimento Feérico", ["Duende", "Sílfide"], "Ação de movimento e 1 PM: +1 categoria de tamanho e +1 For (máx. Grande); 3 PM veterano +2 categorias e +2 For (máx. Enorme).", [], custo_pm=1),
    "HA_Raca_Crianca_Luz": _pr("Criança da Luz", ["Suraggel (Aggelus)"], "Bônus racial em Diplomacia e Intuição sobe para +5 e recebe RD Eletricidade e Frio 5.", [], {"resistencia_rd": {"Eletricidade": 5, "Frio": 5}}),
    "HA_Raca_Crianca_Trevas": _pr("Criança das Trevas", ["Suraggel (Sulfure)"], "Bônus racial em Enganação e Furtividade sobe para +5 e recebe RD Fogo e Trevas 5.", [], {"resistencia_rd": {"Fogo": 5, "Trevas": 5}}),
    "HA_Raca_Devocao_Iluminada": _pr("Devoção Iluminada", ["Várias"], "+2 em Vontade, perde sensibilidade a luz racial e não pode ficar ofuscado.", ["Sensibilidade a luz", "Devoto de energia positiva"], {"bonus_pericia": {"Vontade": 2}, "imunidade": ["Ofuscado"]}),
    "HA_Raca_Duas_Cabecas": _pr("Duas Cabeças", ["Gnoll", "Kaijin", "Lefou", "Orc", "Trog"], "1 PM em Vontade para rolar 2 dados e usar o melhor; ganha 2ª mordida se tiver mordida racial.", [], custo_pm=1),
    "HA_Raca_Dupla_Conjuracao": _pr("Dupla Conjuração", ["Gnoll", "Kaijin", "Lefou", "Orc", "Trog"], "1×/rodada, ao lançar magia padrão, gaste 5 PM (com 2 mãos livres) para lançar magia adicional.", ["Des 2", "Lançar magias", "Dupla Inteligência"], custo_pm=5),
    "HA_Raca_Dupla_Inteligencia": _pr("Dupla Inteligência", ["Gnoll", "Kaijin", "Lefou", "Orc", "Trog"], "2 PM em teste de Inteligência ou perícia de Int para rolar 2 dados e usar o melhor.", ["Int 2", "Duas Cabeças"], custo_pm=2),
    "HA_Raca_Dupla_Prontidao": _pr("Dupla Prontidão", ["Gnoll", "Kaijin", "Lefou", "Orc", "Trog"], "+2 em Percepção, nunca fica desprevenido e não pode ser flanqueado.", ["Sab 2", "Duas Cabeças"], {"bonus_pericia": {"Percepção": 2}}),
    "HA_Raca_Duro_Como_Aco": _pr("Duro Como Aço", ["Anão"], "Usando armadura pesada, soma Con na Defesa (sem somar Destreza).", ["11º nível"]),
    "HA_Raca_Entre_Pernas": _pr("Entre as Pernas", ["Goblin", "Hynne", "Kobolds"], "Ocupa espaço de criaturas 2+ categorias maiores; 25% de ataques contra você acertam a criatura maior.", ["Treinado em Acrobacia"]),
    "HA_Raca_Escapada_Criativa": _pr("Escapada Criativa", ["Goblin", "Meio-Elfo"], "2 PM em teste de resistência para somar Inteligência.", [], custo_pm=2),
    "HA_Raca_Esgrima_Elfica": _pr("Esgrima Élfica", ["Elfo"], "+1 em ataques com espadas e todas as espadas contam como ágeis."),
    "HA_Raca_Estilo_Classico": _pr("Estilo Clássico", ["Humano"], "Empunhando espada e escudo, recebe +2 dano e +2 na Defesa."),
    "HA_Raca_Estirpe_Arcana": _pr("Estirpe Arcana", ["Elfo", "Eiradaan", "Nagah"], "+2 PM por patamar e +2 em Misticismo.", [], {"pm_por_patamar": 2, "bonus_pericia": {"Misticismo": 2}}),
    "HA_Raca_Exaltacao_Rejeitado": _pr("Exaltação do Rejeitado", ["Kaijin", "Lefou"], "Ao lançar magia divina, ganha bônus em TR igual ao círculo até o próximo turno.", ["Lançar magias divinas"]),
    "HA_Raca_Explosao_Ossea": _pr("Explosão Óssea", ["Osteon"], "2 PM ao sofrer dano para reduzir à metade, mas fica fraco (2× debilitado, 3× inconsciente até recolher ossos).", [], custo_pm=2),
    "HA_Raca_Falatorio_Criativo": _pr("Falatório Criativo", ["Goblin"], "Escolha uma perícia originalmente baseada em Carisma para usar Inteligência como atributo-chave."),
    "HA_Raca_Familiar_Elemento": _pr("Familiar de Elemento", ["Qareen"], "Familiar vira elemental imune ao elemento; +1 PM para aprimoramentos em magias desse elemento.", ["Possuir um familiar"]),
    "HA_Raca_Familiar_Luz": _pr("Familiar de Luz", ["Suraggel (Aggelus)", "Qareen"], "Familiar vira celestial imune a luz; +1 PM para aprimoramentos em magias de luz.", ["Possuir um familiar"]),
    "HA_Raca_Familiar_Trevas": _pr("Familiar de Trevas", ["Suraggel (Sulfure)", "Qareen"], "Familiar vira abissal imune a trevas; +1 PM para aprimoramentos em magias de trevas.", ["Possuir um familiar"]),
    "HA_Raca_Faro_Aprimorado": _pr("Faro Aprimorado", ["Minotauro", "Moreau do Lobo"], "+2 em Intuição, Investigação e Percepção, +5 Sobrevivência para rastrear e percebe criaturas em alcance curto.", [], {"bonus_pericia": {"Intuição": 2, "Investigação": 2, "Percepção": 2}}),
    "HA_Raca_Fragrancia_Rosas": _pr("Fragrância de Rosas", ["Dahllan", "Duende"], "+2 em Diplomacia; ação padrão e 2 PM deixa criaturas em alcance curto pasmas 1 rodada (Fort CD Car evita).", [], {"bonus_pericia": {"Diplomacia": 2}}, custo_pm=2),
    "HA_Raca_Furia_Aterrorizante": _pr("Fúria Aterrorizante", ["Galokk", "Ogro"], "Ao entrar em fúria, inimigos em alcance curto ficam abalados pela cena (Von CD Con reduz para 1 rodada).", ["Fúria ou Fúria Divina"]),
    "HA_Raca_Furia_Natural": _pr("Fúria Natural", ["Várias"], "Em fúria, armas naturais raciais ganham +1 passo de dano e +1 margem de ameaça.", ["Fúria", "Arma natural racial"]),
    "HA_Raca_Gavinhas": _pr("Gavinhas", ["Dahllan"], "Sob Armadura de Allihanna, ganha 2 gavinhas (1d4, x2, impacto, 3m, versátil; 1 PM ataque extra cada).", ["5º nível"]),
    "HA_Raca_Ginete_Javali": _pr("Ginete de Javali", ["Anão"], "Recebe javali doherita iniciante (+2 Adestramento e Cavalgar com ele)."),
    "HA_Raca_Glamour": _pr("Glamour", ["Duende", "Eiradaan", "Sílfide"], "Aprende 3 magias de 1º círculo (Car) lançadas como glamour (ilusão; d6=1 falha; TR pode ser Von)."),
    "HA_Raca_Glamour_Maior": _pr("Glamour Maior", ["Duende", "Eiradaan", "Sílfide"], "Aprende mais 3 magias de 1º ou 2º círculo como glamour.", ["Glamour", "5º nível"]),
    "HA_Raca_Golpe_Titas": _pr("Golpe dos Titãs", ["Galokk"], "Força dos Titãs explode também em resultados 1 ponto abaixo do máximo."),
    "HA_Raca_Golpe_Joelho": _pr("Golpe no Joelho", ["Goblin", "Hynne", "Kobolds"], "Atacando criatura maior cujo espaço você ocupa: +1 passo de dano e +2 margem de ameaça.", ["Entre as Pernas"]),
    "HA_Raca_Grande_Marca_Wynna": _pr("Grande Marca de Wynna", ["Qareen"], "+1 magia de 1º círculo (Car) e aprimora ambas como feiticeiro do seu nível."),
    "HA_Raca_Heranca_Erudita": _pr("Herança Erudita", ["Eiradaan", "Elfo", "Kallyanach"], "Escolha uma perícia originalmente baseada em Inteligência: soma seu Carisma nela."),
    "HA_Raca_Logica_Gnomica": _pr("Lógica Gnômica", ["Kliren"], "1×/cena, 3 PM para usar Inteligência em um teste de perícia (exceto ataques).", [], custo_pm=3),
    "HA_Raca_Magia_Ofidica": _pr("Magia Ofídica", ["Medusa", "Moreau da Serpente", "Nagah"], "+1 CD e +1 perda de PV/dado em venenos por círculo de magia que puder lançar.", ["Lançar magias"]),
    "HA_Raca_Manipulacao_Esqueletica": _pr("Manipulação Esquelética", ["Osteon"], "Ação de movimento e 1 PM: +1,5m alcance, +3m deslocamento ou pilha de ossos (+5 Furtividade).", [], custo_pm=1),
    "HA_Raca_Marrada_Poderosa": _pr("Marrada Poderosa", ["Minotauro", "Sátiro"], "Em investida com chifres, +1 passo de dano e 1 PM para ataque extra com arma ou desarmado.", [], custo_pm=1),
    "HA_Raca_Meditacao_Mistica": _pr("Meditação Mística", ["Eiradaan", "Elfo"], "1×/dia, medita 1d4 minutos (fascinado) para recuperar PM iguais ao seu nível.", ["Sab 1", "Treinado em Vontade"]),
    "HA_Raca_Olhar_Petrificante": _pr("Olhar Petrificante", ["Medusa"], "Ação padrão e 3 PM: alcance curto, Fort CD Car ou lento 1d4 rodadas (petrificado permanente se já lento por este efeito).", ["9º nível"], custo_pm=3),
    "HA_Raca_Ossos_Afiados": _pr("Ossos Afiados", ["Osteon"], "+2 em Intimidação e +2 em dano com armas naturais e ataques desarmados.", [], {"bonus_pericia": {"Intimidação": 2}}),
    "HA_Raca_Pirata_Oceanico": _pr("Pirata Oceânico", ["Sereia/Tritão"], "Mestre do Tridente afeta arpões; +2 ataque e contam como ágeis."),
    "HA_Raca_Programacao_Combate": _pr("Programação de Combate", ["Golem"], "Ação de movimento e 3 PM (sustentada): rola 2 dados nos ataques e usa o melhor.", [], custo_pm=3),
    "HA_Raca_Programacao_Holistica": _pr("Programação Holística", ["Golem"], "Ação completa e 2 PM: torna-se treinado em 1 perícia até o fim do dia (1 em 1d4 fica frustrado).", [], custo_pm=2),
    "HA_Raca_Protetor_Eterno": _pr("Protetor Eterno", ["Minotauro"], "Com aliado adjacente, continua consciente mesmo com 0 ou menos PV.", ["Protetor Táurico"]),
    "HA_Raca_Protetor_Taurico": _pr("Protetor Táurico", ["Minotauro"], "Ação de movimento: carrega aliado Médio ou menor (cobertura leve +5 Def e 50% de ataques acertam você)."),
    "HA_Raca_Quadridestria": _pr("Quadridestria", ["Kaijin", "Lefou", "Nagah", "Orc", "Trog"], "1×/rodada com Estilo de Duas Armas, 2 PM para atacar com todas as armas empunhadas (leves exceto 1).", ["Estilo de Duas Armas", "Quatro Braços", "5º nível"], custo_pm=2),
    "HA_Raca_Quatro_Bracos": _pr("Quatro Braços", ["Kaijin", "Lefou", "Nagah", "Orc", "Trog"], "Par de braços extras: empunha até 4 objetos."),
    "HA_Raca_Saliva_Corrosiva": _pr("Saliva Corrosiva", ["Trog"], "Mordida causa +1d6 ácido; ação de movimento cobre arma com +1d6 ácido."),
    "HA_Raca_Sangue_Magico": _pr("Sangue Mágico (Poder de Raça)", ["Eiradaan", "Qareen", "Sílfide"], "1×/dia ganha PM até Con (pode exceder limite no turno), perdendo 1d4 PV/PM no fim do turno."),
    "HA_Raca_Saraivada_Florestal": _pr("Saraivada Florestal", ["Dahllan"], "Sob Armadura de Allihanna, movimento e 2 PM: cone 9m causa 2d8+2 corte (+1d8+1/patamar por +1 PM; Ref CD Sab metade).", [], custo_pm=2),
    "HA_Raca_Soco_Foguete": _pr("Soco Foguete", ["Golem"], "1 PM em ataque corpo a corpo para atingir alvo em alcance curto.", [], custo_pm=1),
    "HA_Raca_Tradicao_Ayrelynn": _pr("Tradição de Ayrelynn", ["Anão"], "Proficiência com armas de fogo e usa Sabedoria em ataques (e dano com Estilo de Disparo).", [], {"proficiencia_add": ["Armas de fogo"]}),
    "HA_Raca_Tradicao_Perdida": _pr("Tradição Perdida", ["Várias"], "Escolhe atributo e classe conjuradora: soma o atributo escolhido nos PM da classe (máx. 6 + 2/patamar).", ["Não humano", "Habilidade Magias"]),
    "HA_Raca_Tradicao_Perdida_Aprimorada": _pr("Tradição Perdida Aprimorada", ["Várias"], "Atributo escolhido em Tradição Perdida passa a ser seu atributo-chave de magias da classe.", ["Tradição Perdida"]),
    "HA_Raca_Valentia_Nata": _pr("Valentia Nata", ["Hynne"], "Imunidade a medo e +5 em Iniciativa.", [], {"imunidade": ["Medo"], "bonus_pericia": {"Iniciativa": 5}}),
    "HA_Raca_Veneno_Aprimorado": _pr("Veneno Aprimorado", ["Medusa"], "Veneno de Natureza Venenosa passa a causar perda de 2d12 PV.", ["Con 1"]),
    "HA_Raca_Vigilancia_Elfica": _pr("Vigilância Élfica", ["Elfo", "Meio-Elfo", "Naidora"], "No 1º turno de cada combate, recebe uma ação de movimento adicional."),
    "HA_Raca_Vitalidade_Fadas": _pr("Vitalidade das Fadas", ["Dahllan", "Duende", "Sátiro", "Sílfide"], "Soma Carisma nos PV iniciais e em Fortitude, e recebe +1 PV por nível a partir do 2º.", [], {"pv_soma_atributo": "car", "pv_max_nivel": 1, "pericia_atributo_opcao": {"Fortitude": "car"}}),
}


# =====================================================================
# 6. PODERES DE GRUPO (19 — Tabela 1-23, p. 92–95)
# =====================================================================

_GRUPO: Dict[str, Dict[str, Any]] = {
    "HA_Grupo_Abrir_Guarda": _pg("Abrir a Guarda", "Poder Geral (Grupo)", "Quando agarra ou derruba inimigo, aliados com este poder em alcance curto podem gastar 2 PM para atacá-lo (1×/rodada).", ["Treinado em Luta ou Pontaria"], custo_pm=2),
    "HA_Grupo_Ajuda_Amador": _pg("Ajuda do Amador", "Poder Geral (Grupo)", "Ação padrão: teste de ajuda para atrapalhar inimigo em alcance curto; aliados com este poder aplicam o bônus em ataques por 1 rodada.", []),
    "HA_Grupo_Apontar_Fraqueza": _pg("Apontar Fraqueza", "Poder Geral (Grupo)", "Ao fazer acerto crítico, aliados com este poder podem gastar 2 PM para que seu 1º ataque no mesmo alvo seja crítico (1×/cena).", [], custo_pm=2),
    "HA_Grupo_Barragem_Golpes": _pg("Barragem de Golpes", "Poder Geral (Grupo)", "Ao causar dano, aliados com este poder recebem +1 cumulativo em dano contra o alvo (máx. nível) pela cena.", []),
    "HA_Grupo_Bode_Expiatorio": _pg("Bode Expiatório", "Poder Geral (Grupo)", "Quando atitude de NPC piora com aliado com este poder, assume a culpa automaticamente no lugar dele.", []),
    "HA_Grupo_Bote_Coletivo": _pg("Bote Coletivo", "Poder Geral (Grupo)", "Bônus igual ao nº de aliados com este poder em Iniciativa e, na 1ª rodada, em perícias e CD de habilidades.", ["Treinado em Iniciativa"]),
    "HA_Grupo_Conforto_Familiar": _pg("Conforto Familiar", "Poder Geral (Grupo)", "Dormindo perto de aliados com este poder, inicia o dia com +3 PV e +1 PM temporários por patamar por aliado.", []),
    "HA_Grupo_Conselhos_Salvadores": _pg("Conselhos Salvadores", "Poder Geral (Grupo)", "2 PM: faz teste de resistência usando o valor de perícia de um aliado em alcance curto com este poder.", [], custo_pm=2),
    "HA_Grupo_Corrente_Corpos": _pg("Corrente de Corpos", "Poder Geral (Grupo)", "1×/rodada, entrega item empunhado como ação livre a aliado com este poder em alcance curto (ou em cadeia).", []),
    "HA_Grupo_Defesa_Martir": _pg("Defesa do Mártir", "Poder Geral (Grupo)", "1×/rodada, 2 PM para sofrer dano no lugar de aliado em alcance curto com este poder.", [], custo_pm=2),
    "HA_Grupo_Dinheiro_Atrai_Dinheiro": _pg("Dinheiro Atrai Dinheiro", "Poder Geral (Grupo)", "Cada personagem com este poder adiciona +5% nas rolagens de tabelas de tesouro do grupo.", []),
    "HA_Grupo_Escudo_Vivo": _pg("Escudo Vivo", "Poder Geral (Grupo)", "2 PM para sofrer dano em área no lugar de aliados em alcance curto com este poder.", [], custo_pm=2),
    "HA_Grupo_Espirito_Uniao": _pg("Espírito de União", "Poder Geral (Grupo)", "Requer todo o grupo: 2 PM cada no início da rodada para compartilhar um pool único de PV pela cena.", ["Exército de Um Grupo Só", "Outro poder de grupo"], custo_pm=2),
    "HA_Grupo_Exercito_Grupo_So": _pg("Exército de Um Grupo Só", "Poder Geral (Grupo)", "Ação padrão e 2 PM cada: formam bando (+2 ataque por aliado; metade dano se errar; +10 soma ataques dos aliados).", ["Treinado em Guerra"], custo_pm=2),
    "HA_Grupo_Magia_Comunitaria": _pg("Magia Comunitária", "Poder Geral (Grupo)", "1×/rodada ao lançar magia alvo você/1 criatura, pague o custo novamente por aliado em alcance curto com este poder para afetá-lo.", []),
    "HA_Grupo_Mao_Amiga": _pg("Mão Amiga", "Poder Geral (Grupo)", "Aliados com este poder gastam 1 semana simultânea para acelerar ações que exigem mais de uma semana.", []),
    "HA_Grupo_Parede_Escudos": _pg("Parede de Escudos", "Poder Geral (Grupo)", "Com escudo, ação de movimento com aliados adjacentes de escudo com este poder: +5 Defesa e RD 5.", []),
    "HA_Grupo_Presenca_Luminosa": _pg("Presença Luminosa", "Poder Geral (Grupo)", "2 PM cada: pela cena todos usam o maior valor de cada perícia baseada em Carisma do grupo.", [], custo_pm=2),
    "HA_Grupo_Saude_Coletiva": _pg("Saúde Coletiva", "Poder Geral (Grupo)", "Ao curar membro do grupo com este poder, cura +2 PV por dado de cura.", []),
    "HA_Grupo_Uma_Mao_Lava_Outra": _pg("Uma Mão Lava a Outra", "Poder Geral (Grupo)", "Fora de combate, 1 PM para rerrolar teste de perícia (usos/cena = total de membros com este poder).", ["Mão Amiga"], custo_pm=1),
}


DADOS_PODERES_GERAIS_HEROIS: Dict[str, Dict[str, Any]] = {
    **_COMBATE,
    **_DESTINO,
    **_MAGIA,
    **_RACA,
    **_GRUPO,
}
