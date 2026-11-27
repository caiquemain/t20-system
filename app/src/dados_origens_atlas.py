# -*- coding: utf-8 -*-
"""Catálogo oficial das 66 Origens Regionais do Atlas de Arton (Apêndice, p. 470–479).

Diferente das origens básicas (2 escolhas), cada origem regional concede um benefício
único automático (poder_fixo + perícias fixas treinadas + efeitos automáticos).
"""
from __future__ import annotations

_F = "Atlas de Arton"

DADOS_ORIGENS_ATLAS: dict[str, dict] = {}
DADOS_PODERES_ORIGEM_ATLAS: dict[str, dict] = {}


def _reg(
    nome: str,
    regiao: str,
    descricao: str,
    beneficio: str,
    itens: str,
    pericias_fixas: list[str] | None = None,
    efeitos: dict | None = None,
) -> None:
    p_fixas = list(pericias_fixas or [])
    ef = dict(efeitos or {})
    if p_fixas:
        ef["pericia_treino"] = list(dict.fromkeys([*(ef.get("pericia_treino") or []), *p_fixas]))

    poder_nome = f"Origem Regional: {nome}"
    DADOS_ORIGENS_ATLAS[nome] = {
        "fonte": _F,
        "regiao": regiao,
        "regional": True,
        "descricao": f"[{regiao}] {descricao}",
        "beneficio_texto": beneficio,
        "itens": itens,
        "qtd_escolhas": 0,
        "pericias_fixas": p_fixas,
        "poder_fixo": poder_nome,
        "beneficios_lista": [],
    }
    DADOS_PODERES_ORIGEM_ATLAS[poder_nome] = {
        "nome": poder_nome,
        "tipo": "Origem",
        "fonte": _F,
        "regiao": regiao,
        "descricao": beneficio,
        "efeitos": ef,
    }


# ── TODAS AS 66 ORIGENS REGIONAIS DO ATLAS DE ARTON (p. 470–479) ──

_reg(
    "Agricultor Sambur", "Sambúrdia",
    "Você trabalhou nos campos férteis das Repúblicas Livres, aprendendo sobre animais, natureza e trabalho duro.",
    "Você é treinado em Adestramento e Sobrevivência e, uma vez por cena, pode gastar 1 PM para receber +1d6 em um teste de perícia.",
    "Ferramenta agrícola (lança), T$ 100.",
    pericias_fixas=["Adestramento", "Sobrevivência"],
)
_reg(
    "Amazona de Hippion", "Deheon, Namalkah",
    "Você é uma das orgulhosas amazonas de Hippion, um dos povos nativos de Arton Norte.",
    "Você é treinada em Cavalgar e, se não estiver usando armadura pesada, soma seu Carisma nos PM, limitado pelo seu nível (após um dia).",
    "Arma simples ou marcial, cavalo de guerra.",
    pericias_fixas=["Cavalgar"],
)
_reg(
    "Amoque Púrpura", "Ermos Púrpuras",
    "Você cresceu entre os lutadores imprevisíveis dos Ermos Púrpuras.",
    "Você é treinado em Intimidação e, quando está sob efeito de Fúria, Fúria Divina ou Poder Oculto, recebe +2 em rolagens de dano.",
    "Arma simples, estandarte da sua tribo.",
    pericias_fixas=["Intimidação"],
)
_reg(
    "Anão de Armas", "Doherimm",
    "Você foi treinado pela Guilda dos Armeiros, tendo aprendido a fabricar e usar armas anãs.",
    "Você é treinado em Ofício (armeiro) e recebe +2 em rolagens de dano com armas tradicionais anãs (machados, martelos, marretas e picaretas).",
    "Arma marcial tradicional anã, instrumentos de Ofício (armeiro).",
    pericias_fixas=["Ofício (Armeiro)"],
    efeitos={"bonus_dano_arma": {
        "machadinha": 2, "machado de batalha": 2, "machado de guerra": 2,
        "machado anão": 2, "machado táurico": 2, "martelo de guerra": 2, "marreta": 2, "picareta": 2,
    }},
)
_reg(
    "Andarilho Ubaneri", "Ubani",
    "Sonhando em ser membro da Patrulha da Fronteira, você pratica técnicas de lança e escudo com um alikunhá.",
    "Você recebe um alikunhá (parceiro iniciante que não conta no limite de parceiros) e proficiência com escudos (ou +1 na Defesa do escudo se já tiver).",
    "Escudo pesado, lança.",
    efeitos={"proficiencia_escudos": True},
)
_reg(
    "Aprendiz de Dragoeiro", "Sckharshantallas",
    "Você aprendeu técnicas para enfrentar dragões e grandes feras em Sckharshantallas.",
    "Você recebe +2 na Defesa contra criaturas maiores que você e +2 em Reflexos. Se passar em um teste de Reflexos, seus ataques contra a fonte causam +1d8 de dano até o fim da cena.",
    "Arma simples ou marcial, troféu de caça, treckod.",
    efeitos={"bonus_pericia": {"Reflexos": 2}},
)
_reg(
    "Aprendiz de Drogadora", "Galrasia",
    "Você era discípula de uma voracis drogadora e estudou as artes de cura em Galrasia.",
    "Você é treinada em Cura e Ofício (alquimista) e gasta apenas 1/4 do preço em matérias-primas para fabricar preparados alquímicos e poções.",
    "Bálsamo restaurador x2, poção de curar ferimentos x2, maleta de medicamentos.",
    pericias_fixas=["Cura", "Ofício (Alquimista)"],
)
_reg(
    "Aristocrata Dai'zenshi", "Tamu-ra",
    "Você faz parte da nobreza tamuraniana, descendente de um dos três Grandes Clãs ou vassalo samurai.",
    "Você é treinado em Nobreza. Ao completar um descanso sem ter feito testes de Enganação, Furtividade ou Ladinagem desde o último descanso, recebe +1 PM temporário para cada 2 níveis.",
    "Traje da corte, katana superior com uma melhoria (exceto material especial).",
    pericias_fixas=["Nobreza"],
)
_reg(
    "Armeiro Armado", "Zakharov",
    "Você aprendeu o ofício mais tradicional e respeitado de Zakharov.",
    "Você é treinado em Ofício (armeiro) e pode fabricar armas com uma melhoria (se já souber, gasta apenas 1/4 do preço das melhorias em armas).",
    "Arma marcial, instrumentos de Ofício (armeiro).",
    pericias_fixas=["Ofício (Armeiro)"],
)
_reg(
    "Aspirante a Herói", "Deheon",
    "Você nasceu para ser herói, com potencial para protagonizar canções épicas.",
    "Você recebe +1 em um atributo à sua escolha.",
    "Essência de mana, mochila de aventureiro.",
    efeitos={"atributo_bonus_escolha": 1},
)
_reg(
    "Assistente Forense", "Salistick",
    "Você teve contato com a ciência forense mais avançada de Salistick.",
    "Você é treinado em Investigação e pode usá-la para necropsia, identificar alquímicos, rastrear e identificar criaturas em cenas de crime.",
    "Lupa (+1 em Investigação).",
    pericias_fixas=["Investigação"],
)
_reg(
    "Bandoleiro da Fortaleza", "Khalifor",
    "Você cresceu se esgueirando pelos becos de Khalifor.",
    "Você é treinado em Furtividade e Intimidação, e recebe resistência a medo +5.",
    "Adaga, gazua, manto camuflado (urbano).",
    pericias_fixas=["Furtividade", "Intimidação"],
)
_reg(
    "Barão Arruinado", "Feudos de Trebuck",
    "Você estava destinado a ser senhor de um feudo, mas seu título se perdeu.",
    "Você é treinado em Nobreza. Sempre que falha em um teste de perícia com consequência negativa, recebe +2 nessa perícia até o fim da cena.",
    "Anel com símbolo da família (T$ 200), títulos de terras expirados (+2 Diplomacia com nobres/burocratas), traje da corte.",
    pericias_fixas=["Nobreza"],
)
_reg(
    "Catador da Cidade Velha", "Nova Malpetrim",
    "Você cresceu vasculhando as ruínas inundadas da Velha Malpetrim.",
    "Você é treinado em Fortitude e Percepção e pode gastar 1 PM para receber deslocamento de natação igual ao básico (+3m se já tiver) por uma cena e dobrar o tempo de fôlego.",
    "Luneta, luvas de pelica, tranqueiras resgatadas do mar (2 esp, T$ 100).",
    pericias_fixas=["Fortitude", "Percepção"],
)
_reg(
    "Cativo das Fadas", "Pondsmânia",
    "Quando bebê, você foi levado para a Pondsmânia e cresceu entre jogos feéricos.",
    "Você recebe resistência a espíritos e magia +2 e +1 PV por nível de personagem.",
    "Corda, ração de viagem x10, essência de mana.",
    efeitos={"resistencia_magia_bonus": 2, "pv_max_nivel": 1},
)
_reg(
    "Competidor do Circuito", "Feudos de Trebuck",
    "Você percorreu o grande Circuito de Torneios de Trebuck.",
    "Você recebe o poder Torcida. Sob efeito desse poder, sempre que reduz um inimigo a 0 PV com ataque corpo a corpo, recupera 1 PM.",
    "Arma marcial, T$ 100.",
)
_reg(
    "Cosmopolita", "Valkaria",
    "Tendo crescido na maior cidade de Arton, você já viu de tudo.",
    "Escolha um poder geral ou de uma classe na qual tenha pelo menos 2 níveis (exceto concedidos/Tormenta). 1x/aventura após descanso pode trocar esse poder.",
    "Equipamento de viagem, traje de viajante, item artístico (0,5 esp, T$ 100).",
)
_reg(
    "Cria da Favela", "Valkaria",
    "A Favela dos Goblins em Valkaria o tornou resistente e incansável.",
    "Você recebe +1 em Constituição e sua recuperação por descanso é sempre pelo menos normal.",
    "Andrajos de aldeão, corda, vara de madeira.",
    efeitos={"atributo_bonus": {"constituicao": 1}},
)
_reg(
    "Criado pelas Voracis", "Galrasia",
    "Você foi encontrado e criado por um grupo de voracis em Galrasia.",
    "Você recebe +2 na Defesa e em Sobrevivência e +3m em seu deslocamento.",
    "Arma simples, armadura leve, lança.",
    efeitos={"defesa_bonus": 2, "bonus_pericia": {"Sobrevivência": 2}, "deslocamento_bonus": 3},
)
_reg(
    "De Outro Mundo", "Éter Divino",
    "Você veio de outro mundo através do Éter Divino ou de uma fenda planar.",
    "Escolha uma magia de 1º círculo e um atributo-chave (habilidade ou tecnologia com item Minúsculo de 1 esp e +2 limite de PM).",
    "Trajes exóticos, item de até T$ 100 do seu mundo natal.",
)
_reg(
    "Descendente Colleniano", "Ahlen",
    "Você descende do antigo povo de Collen, com olhos de cores incomuns e poderes ligados à visão.",
    "Você recebe +2 em Percepção e pode lançar a magia Visão Mística (–1 PM se aprender novamente).",
    "Arma simples, estojo de disfarces, ração de viagem x5.",
    efeitos={
        "bonus_pericia": {"Percepção": 2},
        "magia_adicional": {"nome": "Visão Mística", "atributo": "Int"},
        "reducao_custo_magia": {"nomes": ["Visão Mística"], "valor": 1},
    },
)
_reg(
    "Desertor da Supremacia", "Supremacia Purista",
    "Você passou pelo treinamento dos batalhões puristas e decidiu se voltar contra a Supremacia.",
    "Você é treinado em Guerra e recebe proficiência com espadas bastardas e escudos. Empunhando espada bastarda e escudo pesado, recebe +2 em ataques.",
    "Brunea com símbolo purista raspado, escudo pesado, espada bastarda, ração x10.",
    pericias_fixas=["Guerra"],
    efeitos={"proficiencia_escudos": True, "proficiencia_simples": ["espada bastarda"]},
)
_reg(
    "Duplo Feérico", "Pondsmânia",
    "Você é a cópia de alguém existente em Arton, criada por uma fada.",
    "Escolha uma habilidade de classe de 1º nível de outra classe (usada como 1º nível; se Magias, aprende 1 magia e +1 PM).",
    "Essência de mana, marca física única.",
)
_reg(
    "Duyshidakk Infiltrado", "Ruínas de Tyrondir",
    "Você viveu entre o povo do Reinado, secretamente devotado ao Mundo Como Deve Ser.",
    "Você recebe +2 em Furtividade e Vontade e pode usar Sabedoria como atributo-chave de Enganação.",
    "Arma marcial, peças sobressalentes (T$ 100).",
    efeitos={"bonus_pericia": {"Furtividade": 2, "Vontade": 2}, "pericia_atributo_opcao": {"Enganação": "sab"}},
)
_reg(
    "Emissário Ubaneri", "Ubani",
    "Você foi preparado para percorrer terras distantes acompanhado de um alikunhá.",
    "Você recebe um alikunhá (parceiro iniciante que não conta no limite) e pode usar Sabedoria como atributo-chave de Misticismo.",
    "Essência de mana, mochila de aventureiro.",
    efeitos={"pericia_atributo_opcao": {"Misticismo": "sab"}},
)
_reg(
    "Escudeiro da Luz", "Bielefeld",
    "Você serviu a um nobre e honrado cavaleiro da Ordem da Luz.",
    "Você é treinado em Nobreza. Além disso, recebe +2 na Defesa e +3 PM.",
    "Cota de malha ou escudo pesado, enfeite de elmo com símbolo da Ordem da Luz.",
    pericias_fixas=["Nobreza"],
    efeitos={"defesa_bonus": 2, "pm_max_ini": 3},
)
_reg(
    "Escudeiro Solitário", "Bielefeld",
    "Seu mestre era membro dos Cavaleiros Solitários, adeptos de subterfúgios para ajudar heróis.",
    "Você é treinado em Enganação e Ladinagem, recebe +10 em Enganação para se disfarçar de cavaleiro da Luz e atacar pelas costas não viola Código de Honra.",
    "Cota de malha, escudo pesado, enfeite de elmo.",
    pericias_fixas=["Enganação", "Ladinagem"],
)
_reg(
    "Estandarte Vivo", "Ermos Púrpuras",
    "Sua tribo nos Ermos Púrpuras foi extinta, mas você permanece como prova viva dela.",
    "Você recebe +2 em Sobrevivência e um poder de combate ou da Tormenta à sua escolha.",
    "Arma simples ou marcial, gibão de peles, fragmento do estandarte (+1 Vontade se vestido).",
    efeitos={"bonus_pericia": {"Sobrevivência": 2}},
)
_reg(
    "Estudante da Academia", "Academia Arcana",
    "Você frequentou a Academia Arcana e aprendeu fundamentos de conjuração.",
    "Você aprende uma magia arcana de 1º círculo (Int) e pode fazer testes de Misticismo sem treino (ou +2 se treinado).",
    "Coleção de livros, essência de mana x2.",
)
_reg(
    "Estudante do Colégio Real", "Salistick",
    "Você estudou no Colégio Real de Médicos de Salistick, combinando ceticismo e ciência.",
    "Você é treinado em Cura e seus efeitos de cura recuperam +2 PV por dado. Perde esse benefício se tornar-se devoto.",
    "Bálsamo restaurador x3, maleta de medicamentos.",
    pericias_fixas=["Cura"],
)
_reg(
    "Explorador de Ruínas", "Ruínas de Tyrondir",
    "Você explorou as ruínas deixadas pela queda da Flecha de Fogo em Tyrondir.",
    "Você recebe +2 em Ladinagem, Percepção e Reflexos e +3m em seu deslocamento.",
    "Mochila de aventureiro, tocha, vara de madeira (3m).",
    efeitos={"bonus_pericia": {"Ladinagem": 2, "Percepção": 2, "Reflexos": 2}, "deslocamento_bonus": 3},
)
_reg(
    "Filhote da Revoada", "Lamnor",
    "Você passou a juventude entre a Revoada Carnívora e seus engenhos voadores.",
    "Você é treinado em Acrobacia e Pilotagem e pode gastar 1 PM para rolar um dado adicional e usar o melhor resultado nessas perícias.",
    "Instrumentos de Ofício (artesão), T$ 100.",
    pericias_fixas=["Acrobacia", "Pilotagem"],
)
_reg(
    "Futura Lenda", "Nova Malpetrim",
    "Você cresceu ouvindo histórias sobre heróis e decidiu superá-los.",
    "Escolha um dos poderes de sua classe normalmente disponível a partir do 2º nível.",
    "Arma simples ou marcial com nome pomposo, essência de mana x2.",
)
_reg(
    "Ginete de Tumarkhân", "Khubar",
    "Você estabeleceu um elo com um lagarto tumarkhân de Khubar.",
    "Você é treinado em Cavalgar e possui um parceiro tumarkhân iniciante (+2 em Adestramento e Cavalgar; acumulável com Montaria especial).",
    "Bálsamo restaurador, sela.",
    pericias_fixas=["Cavalgar"],
    efeitos={"bonus_pericia": {"Adestramento": 2, "Cavalgar": 2}},
)
_reg(
    "Grumete Pirata", "Três Mares",
    "Você serviu em uma embarcação pirata nos Três Mares.",
    "Você é treinado em Acrobacia, Atletismo e Reflexos; só cai/afunda ao equilibrar, escalar ou nadar se falhar por 10 ou mais.",
    "Adaga, corda, tatuagem da tripulação (+1 Intimidação).",
    pericias_fixas=["Acrobacia", "Atletismo", "Reflexos"],
)
_reg(
    "Guardião Glacial", "Montanhas Uivantes",
    "Você treinou com os protetores das Montanhas Uivantes.",
    "Você recebe redução de frio 5 e proficiência em arco longo e machado de batalha (ou +2 dano com essas armas se já tiver).",
    "Casaco longo, cavalo glacial.",
    efeitos={"rd_tipo": {"frio": 5}, "proficiencia_simples": ["arco longo", "machado de batalha"]},
)
_reg(
    "Iniciado dos Caça-Monstros", "Montanhas Sanguinárias",
    "Você foi iniciado na Guilda dos Caça-Monstros.",
    "Você identifica criaturas com ação de movimento e, ao acertar ataque em não-humanoide, pode gastar 1 PM para causar +1d8 de dano.",
    "Arma simples ou marcial, gibão de peles.",
)
_reg(
    "Insurgente Tapistano", "Império de Tauron",
    "Você luta para punir os antigos generais e escravagistas do Império de Tauron.",
    "Você recebe +1 em Fortitude, Reflexos e Vontade, +3 PV no 1º nível e +1 PV por nível seguinte.",
    "Amuleto da resistência, arma simples.",
    efeitos={"bonus_pericia": {"Fortitude": 1, "Reflexos": 1, "Vontade": 1}, "pv_max_ini": 2, "pv_max_nivel": 1},
)
_reg(
    "Irmão sem Esporas", "Namalkah",
    "Você cresceu ao lado de um cavalo de guerra desde a infância.",
    "Você possui um irmão cavalo (parceiro iniciante que fornece +1 em ataque e Reflexos; acumulável com Montaria especial).",
    "Bálsamo restaurador, sela.",
    efeitos={"bonus_pericia": {"Reflexos": 1}},
)
_reg(
    "Legionário", "Império de Tauron",
    "Você serviu nas legiões do Império de Tauron.",
    "Você é treinado em Guerra e recebe proficiência com gládios e escudos. Empunhando gládio e escudo pesado, recebe +1 margem de ameaça e +1 na Defesa.",
    "Brunea da legião, escudo pesado, gládio, ração x10.",
    pericias_fixas=["Guerra"],
    efeitos={"proficiencia_escudos": True, "proficiencia_simples": ["gládio"]},
)
_reg(
    "Lenhador de Tollon", "Floresta de Tollon",
    "Você foi criado entre as imponentes árvores da Floresta de Tollon.",
    "Você é treinado em Ofício (artesão), recebe +5 em perícias (exceto ataque) relacionadas a madeira e proficiência com machadinhas e machados de batalha (ou +2 dano se já tiver).",
    "Item superior de madeira Tollon.",
    pericias_fixas=["Ofício (Artesão)"],
    efeitos={"proficiencia_simples": ["machadinha", "machado de batalha"]},
)
_reg(
    "Liricista de Lenórienn", "Lamnor",
    "Inspirado pelas tradições élficas, você transformou sua magia em arte.",
    "Você é treinado em Atuação, recebe +2 nessa perícia e pode usar Carisma como atributo-chave de Misticismo.",
    "Alaúde élfico, réplica artística élfica (1 esp, T$ 50).",
    pericias_fixas=["Atuação"],
    efeitos={"bonus_pericia": {"Atuação": 2}, "pericia_atributo_opcao": {"Misticismo": "car"}},
)
_reg(
    "Membro do Principado", "Sambúrdia",
    "Você faz parte do Principado Mercante das Repúblicas Livres.",
    "Você é treinado em Diplomacia e Intuição. Ao chegar numa cidade pela 1ª vez na aventura, Diplomacia CD 20 garante 10% de desconto cumulativo com barganha.",
    "Carroça, mercadorias sortidas (8 esp, T$ 400).",
    pericias_fixas=["Diplomacia", "Intuição"],
)
_reg(
    "Nitamuraniano", "Valkaria",
    "Você foi criado na comunidade tamuraniana de Valkaria.",
    "Você recebe proficiência em katana e arco longo (ou +2 dano se já tiver) e pode gastar 2 PM para refazer um teste de perícia de Sabedoria falho (1x/teste).",
    "Arco longo ou katana, camisa bufante ou traje de seda.",
    efeitos={"proficiencia_simples": ["katana", "arco longo"]},
)
_reg(
    "Nobre Zakharoviano", "Zakharov",
    "Você descende de uma tradicional família de nobres armeiros zakharovianos.",
    "Você é treinado em Ofício (armeiro) e recebe uma arma superior com 1 melhoria (exceto material especial); de posse dela recebe +2 PM por patamar (após 1 dia).",
    "Traje da corte.",
    pericias_fixas=["Ofício (Armeiro)"],
)
_reg(
    "Nômade Sar-Allan", "Halak-Tûr",
    "Você cresceu entre os sar-allan no Deserto da Perdição.",
    "Você recebe +2 em Fortitude, Sobrevivência e nas rolagens de dano com alfanges, arcos curtos e cimitarras.",
    "Arma simples ou marcial, corcel do deserto ou dromedário, manto camuflado (deserto).",
    efeitos={
        "bonus_pericia": {"Fortitude": 2, "Sobrevivência": 2},
        "bonus_dano_arma": {"alfange": 2, "arco curto": 2, "cimitarra": 2},
    },
)
_reg(
    "Pescador Parrudo", "Khubar",
    "Você pesca nas águas profundas de Khubar desde criança.",
    "Você recebe +2 em Atletismo, Fortitude e Sobrevivência, +3 PV e avança seu deslocamento inteiro ao nadar com Atletismo.",
    "Vara de pesca, peixes raros salgados (1 esp, T$ 50).",
    efeitos={"bonus_pericia": {"Atletismo": 2, "Fortitude": 2, "Sobrevivência": 2}, "pv_max_ini": 3},
)
_reg(
    "Plebeu Arcano", "Wynlla",
    "Crescer em Wynlla o deixou acostumado aos aspectos místicos de Arton.",
    "Você recebe +2 PM e, 1x/rodada, ao falhar em TR contra efeito mágico, pode gastar 1 PM para rolar novamente.",
    "Bandoleira de poções, gorro de ervas, poção arcana de 1º círculo.",
    efeitos={"pm_max_ini": 2},
)
_reg(
    "Prisioneiro das Catacumbas", "Catacumbas de Leverick",
    "Você sobreviveu e escapou das Catacumbas de Leverick.",
    "Você é treinado em Percepção e Reflexos e recebe resistência a armadilhas e efeitos de movimento +5.",
    "Arma marcial encontrada nas Catacumbas.",
    pericias_fixas=["Percepção", "Reflexos"],
)
_reg(
    "Procurado: Vivo ou Morto", "Smokestone",
    "Você é um pistoleiro infame com a cabeça a prêmio nas cercanias de Smokestone.",
    "Você recebe proficiência com armas de fogo, +5 em Intimidação e –5 em Diplomacia contra quem o reconheça.",
    "Pistola, balas cruéis (20).",
    efeitos={"proficiencia_fogo": True},
)
_reg(
    "Profeta do Akzath", "Lamnor",
    "Você conhece a verdade sobre o tempo e o destino na forma do Akzath.",
    "Você é treinado em Religião e pode lançar magias mesmo sob o efeito de Fúria Divina.",
    "Arma simples ou marcial, bordão, pergaminho com diagrama do Akzath.",
    pericias_fixas=["Religião"],
)
_reg(
    "Querido Filho", "Aslothia",
    "Você passou a juventude em Aslothia e abraçou a dádiva das trevas.",
    "Você recebe redução de frio e trevas 5 e visão no escuro (ou +2 em Percepção se já tiver visão no escuro).",
    "Essência de sombra, manto camuflado (urbano).",
    efeitos={"rd_tipo": {"frio": 5, "trevas": 5}, "visao_escuro": True},
)
_reg(
    "Rebelde Agitador", "Sckharshantallas",
    "Você fez parte de grupos rebeldes contra o Dragão-Rei em Sckharshantallas.",
    "Você é treinado em Iniciativa e, 1x/aventura (1 dia, Diplomacia CD 10), convence pessoas comuns (+1 por 10 acima da CD) como parceiros iniciantes por uma cena.",
    "Arma simples ou marcial, panfleto revolucionário, T$ 6d12.",
    pericias_fixas=["Iniciativa"],
)
_reg(
    "Receptador das Nuvens", "Vectora",
    "Você cresceu nos bazares e becos de Vectora, o Mercado nas Nuvens.",
    "Pode gastar 1 dia em cidade para obter um aparato mágico (1 esp, lança uma magia de 1º círculo, Int; até 2 aparatos simultâneos).",
    "Mercadorias raras e variadas (2 esp, T$ 300).",
)
_reg(
    "Recruta Arcano", "Wynlla",
    "Você serviu entre os Magos de Batalha de Wynlla.",
    "A CD para resistir a suas magias arcanas aumenta em +1 e elas causam +1 ponto de dano.",
    "Essência de mana x2, varinha arcana.",
    efeitos={"cd_magias_arcana_bonus": 1},
)
_reg(
    "Recruta da Fênix", "Triunphus",
    "Você treinou montado em grifo para combater a Horda Moóck em Triunphus.",
    "Você recebe +1 PV por nível, redução de fogo 5 e é treinado em Cavalgar.",
    "Arma marcial, brunea, grifo iniciante.",
    pericias_fixas=["Cavalgar"],
    efeitos={"pv_max_nivel": 1, "rd_tipo": {"fogo": 5}},
)
_reg(
    "Sábio Matemático", "Halak-Tûr",
    "Você estudou as equações sar-allan para resolver problemas através da matemática.",
    "Você é treinado em Conhecimento e aprende Concentração de Combate e Orientação (efeitos mundanos, não contam como magia exceto acúmulo).",
    "Coleção de livros, luneta.",
    pericias_fixas=["Conhecimento"],
)
_reg(
    "Selvagem Sanguinário", "Montanhas Sanguinárias",
    "Você sobreviveu nas brutais Montanhas Sanguinárias pela força bruta.",
    "Você é treinado em Sobrevivência e, sem armadura pesada, recebe +1 em rolagens de dano com armas e redução de dano 1.",
    "Arma marcial, gibão de peles.",
    pericias_fixas=["Sobrevivência"],
)
_reg(
    "Sucateiro de Batalhas", "Conflagração do Aço",
    "Você se especializou em pilhar armas e itens nos campos de batalha da Conflagração.",
    "Você é treinado em Guerra e Investigação e pode rolar novamente resultados na Tabela 8-1: Tesouro por ND.",
    "Arma simples ou marcial, bálsamo restaurador, escudo leve ou pesado, essência de mana, ração x5, T$ 4d6.",
    pericias_fixas=["Guerra", "Investigação"],
)
_reg(
    "Tamalu", "Khubar",
    "Você nasceu entre os tamalus, a casta política tatuada de Khubar.",
    "Você é treinado em Diplomacia e Nobreza e recebe uma tatuagem mística à sua escolha (+1 Defesa, res. magia +2 ou magia de 1º círculo Sab).",
    "Traje da corte.",
    pericias_fixas=["Diplomacia", "Nobreza"],
)
_reg(
    "Tocado pela Dama Altiva", "Moreania",
    "Nascido em Moreania, você entende as vozes da natureza.",
    "Você é treinado em Adestramento e pode gastar 1 min e 1 PM para convocar um animal Minúsculo (+2 em uma perícia adequada pela cena; até Sab simultâneos).",
    "Bordão, ração de viagem x5.",
    pericias_fixas=["Adestramento"],
)
_reg(
    "Tocado pelo Indomável", "Moreania",
    "Agraciado pelo poder dos monstros de Moreania.",
    "Você é treinado em Atletismo e recebe +2 em rolagens de dano com armas naturais e ataques desarmados.",
    "Trapos surrados, carcaça de couro (gibão de peles).",
    pericias_fixas=["Atletismo"],
)
_reg(
    "Tradicionalista Svalano", "Svalas",
    "Você é fruto da tradição oral de Svalas.",
    "Você pode usar Sabedoria como atributo-chave de Conhecimento e Nobreza, pode fazê-las sem treinamento e recebe +1 em Fortitude e Vontade.",
    "Arma simples ou marcial, corda, mochila de aventureiro, vara de madeira (3m).",
    efeitos={
        "bonus_pericia": {"Fortitude": 1, "Vontade": 1},
        "pericia_atributo_opcao": {"Conhecimento": "sab", "Nobreza": "sab"},
    },
)
_reg(
    "Trapaceiro Ahleniense", "Ahlen",
    "Em Ahlen você aprendeu muito bem como não ser o otário.",
    "Você recebe +2 em Enganação e Furtividade e pode usar Carisma como atributo-chave de Ladinagem.",
    "Essência de sombra, gazua, estojo de disfarces.",
    efeitos={"bonus_pericia": {"Enganação": 2, "Furtividade": 2}, "pericia_atributo_opcao": {"Ladinagem": "car"}},
)
_reg(
    "Turista da Academia", "Academia Arcana",
    "Você assistiu a algumas aulas na Academia Arcana e aprendeu alguns truques.",
    "Você recebe resistência a magia +2 e pode ativar pergaminhos de todas as magias arcanas de 1º círculo como se as conhecesse.",
    "Três pergaminhos de magias arcanas de 1º círculo à sua escolha.",
    efeitos={"resistencia_magia_bonus": 2},
)
_reg(
    "Um com os Kami", "Tamu-ra",
    "Desde novo você vê e ouve os kami, espíritos divinos de Tamu-ra.",
    "Você pode usar Sabedoria como atributo-chave de Misticismo e é acompanhado por um kami (parceiro especial fora do limite: vê incorpóreos invisíveis, ataques/habilidades contam como mágicos, 1 PM ação mov. manipula objeto solto em alcance curto).",
    "Bálsamo restaurador, essência de mana.",
    efeitos={"pericia_atributo_opcao": {"Misticismo": "sab"}},
)
