# -*- coding: utf-8 -*-
"""Catálogo oficial das 30 Novas Origens Especiais — Heróis de Arton (Cap. 1, p. 46–53).

Assim como as origens regionais do Atlas de Arton, cada origem especial fornece
um benefício único automático (poder_fixo + perícias fixas treinadas + efeitos reais).
"""
from __future__ import annotations
from .dados_suplementos import FONTE_HEROIS

DADOS_ORIGENS_HEROIS: dict[str, dict] = {}
DADOS_PODERES_ORIGEM_HEROIS: dict[str, dict] = {}


def _esp(
    nome: str,
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

    poder_nome = f"Origem Especial: {nome}"
    DADOS_ORIGENS_HEROIS[nome] = {
        "fonte": FONTE_HEROIS,
        "regional": True,
        "especial": True,
        "descricao": descricao,
        "beneficio_texto": beneficio,
        "itens": itens,
        "qtd_escolhas": 0,
        "pericias_fixas": p_fixas,
        "poder_fixo": poder_nome,
        "beneficios_lista": [],
    }
    DADOS_PODERES_ORIGEM_HEROIS[poder_nome] = {
        "nome": poder_nome,
        "tipo": "Origem",
        "fonte": FONTE_HEROIS,
        "descricao": beneficio,
        "efeitos": ef,
    }


_esp(
    "Bacharel",
    "Treinado para argumentar, debater e defender inocentes em tribunais do Reinado.",
    "Você é treinado em Conhecimento, Diplomacia e Nobreza. Além disso, uma vez por cena pode usar Diplomacia para mudar atitude como uma ação livre.",
    "Tabardo com o símbolo de Khalmyr, uma coleção de livros a sua escolha.",
    ["Conhecimento", "Diplomacia", "Nobreza"],
    {"mudar_atitude_livre_cena": True},
)

_esp(
    "Boticário",
    "Aprendiz de um especialista em ervas, poções e misturas alquímicas.",
    "Você é treinado em Cura e Ofício (alquimista). Além disso, pode fabricar poções de duas fórmulas de 1º círculo a sua escolha, como se tivesse o poder Alquimista Iniciado (T20 p. 68).",
    "Bálsamo restaurador, instrumentos de Ofício (alquimista), maleta de medicamentos.",
    ["Cura", "Ofício (Alquimista)"],
    {"alquimista_iniciado_formulas": 2},
)

_esp(
    "Caçador de Ratos",
    "Especialista em livrar porões e esgotos de ratos, morcegos, glops e outras pestes.",
    "Você é treinado em Furtividade, Investigação e Sobrevivência, e recebe +2 em testes de perícias contra criaturas de duas categorias de tamanho menor que a sua (mínimo Minúsculas).",
    "Clava, um gato (parceiro perseguidor iniciante), T$ 50.",
    ["Furtividade", "Investigação", "Sobrevivência"],
    {"bonus_contra_menores": 2},
)

_esp(
    "Cão de Briga",
    "Lutador brutal de torneios clandestinos no submundo do Reinado.",
    "Na primeira vez a cada cena em que você faz a ação agredir, pode fazer um ataque extra.",
    "Manoplas ou uma arma marcial.",
    [],
    {"ataque_extra_primeira_agredir_cena": True},
)

_esp(
    "Carcereiro",
    "Guarda experiente de calabouços e prisões com detentos perigosos e sobrenaturais.",
    "Você recebe +2 em testes contra efeitos mentais, Enganação, Furtividade e Intimidação.",
    "Algemas, lampião, uma arma de até T$ 500 a sua escolha.",
    [],
    {"bonus_pericia": {"Enganação": 2, "Furtividade": 2, "Intimidação": 2}, "bonus_vs_mental": 2},
)

_esp(
    "Carpinteiro de Guilda",
    "Artesão versátil de guilda, construtor de pontes, navios e estruturas de madeira.",
    "Você é treinado em Ofício (artesão). Além disso, recebe redução de corte 2 e, em suas mãos, armas de corte ignoram 5 pontos de redução de dano.",
    "Instrumentos de Ofício (carpinteiro), uma arma de corte a sua escolha.",
    ["Ofício (Artesão)"],
    {"resistencia_rd": {"Corte": 2}, "ignora_rd_corte": 5},
)

_esp(
    "Catador da Catástrofe",
    "Sobrevivente que vasculhou ruínas de grandes catástrofes de Arton em busca de sustento.",
    "Você é treinado em Fortitude e Percepção. No início de cada aventura, teste de Percepção (CD 15 + metade do nível) encontra um tesouro correspondente ao seu ND (Tabela 8-1).",
    "Dois equipamentos de aventura de até T$ 150 cada a sua escolha.",
    ["Fortitude", "Percepção"],
    {"catador_tesouro_inicio_aventura": True},
)

_esp(
    "Chef Hynne",
    "Guardião da tradição gastronômica de Hongari em castelos, tavernas ou navios.",
    "Você é treinado em Ofício (cozinheiro). Quando prepara um prato especial, seu benefício dura mais 1 dia (se for de uso diário, pode ser usado novamente nesse dia).",
    "Cutelo (estatísticas de foice), instrumentos de cozinheiro aprimorados.",
    ["Ofício (Cozinheiro)"],
    {"prato_especial_duracao_extra_dias": 1},
)

_esp(
    "Cirurgião-Barbeiro",
    "Barbeiro e médico prático de vilarejos, portos ou navios.",
    "Você é treinado em Cura e Ofício (barbeiro). Ação completa e 2 PM: remove 1 condição listada de criatura adjacente, mas a criatura perde 1d6 PV.",
    "Dente falso, instrumentos de barbeiro, maleta de medicamentos.",
    ["Cura", "Ofício (Barbeiro)"],
    {"remover_condicao_2pm_1d6_pv": True},
)

_esp(
    "Citadino Abastado",
    "Nascido em família rica de comerciantes ou artesãos de uma grande cidade.",
    "Você é treinado em Nobreza e em um Ofício a sua escolha. Em cidade grande, pode gastar T$ 10 × nível para usar um poder de combate, destino ou de uma de suas classes por 1 cena.",
    "Uma arma, armadura, ferramenta ou vestuário de até T$ 500.",
    ["Nobreza"],
    {"oficio_escolha": 1},
)

_esp(
    "Cocheiro",
    "Condutor confiável de carroças, carruagens e diligências pelos ermos.",
    "Você é treinado em Adestramento e Pilotagem e, quando está conduzindo um veículo, você e o veículo recebem +2 na Defesa e em testes de resistência.",
    "Cavalo ou trobo, carroça.",
    ["Adestramento", "Pilotagem"],
    {"bonus_veiculo_defesa_tr": 2},
)

_esp(
    "Construtor",
    "Pedreiro e mestre de obras que ergueu casas, castelos, pontes e muralhas.",
    "Você é treinado em Fortitude e Ofício (pedreiro). Pode pagar 2 PM para que você ou aliado em alcance curto ignore 5 pontos de RD de uma criatura ou objeto por uma cena.",
    "Instrumentos de pedreiro ou ferramenta pesada (maça ou lança).",
    ["Fortitude", "Ofício (Pedreiro)"],
    {"ignora_rd_2pm": 5},
)

_esp(
    "Contrabandista",
    "Transportador clandestino de mercadorias proibidas através de fronteiras e patrulhas.",
    "Você é treinado em Enganação e Ladinagem, recebe +5 em Ladinagem para ocultar itens em si ou em veículos, e sua capacidade de carga aumenta em +2 espaços.",
    "Uma arma de fogo ou 10 doses de venenos somando até T$ 500.",
    ["Enganação", "Ladinagem"],
    {"carga_max_bonus": 2, "bonus_ocultar_itens": 5},
)

_esp(
    "Coureiro",
    "Artesão especializado em tratamento e modelagem de peles e armaduras de couro.",
    "Você é treinado em Fortitude e Ofício (coureiro). Gaste 10 minutos e T$ 10 em uma armadura de couro (incl. couro batido, gibão de peles e brunea) para dar +1 Defesa e -2 PA por 1 dia.",
    "Faca de corte (adaga de corte), instrumentos de coureiro, T$ 100 em itens alquímicos.",
    ["Fortitude", "Ofício (Coureiro)"],
    {"aprimorar_couro_temporario": True},
)

_esp(
    "Escriba",
    "Copista de textos religiosos, literários, científicos e legais em mosteiros ou cortes.",
    "Você é treinado em Conhecimento e Ofício (escriba) e recebe o poder de bardo Lendas e Histórias (se receber novamente, ganha +5 ao rerrolar com seu efeito).",
    "Instrumentos de escriba, organizador de pergaminhos, uma coleção de livros a sua escolha.",
    ["Conhecimento", "Ofício (Escriba)"],
    {"concede_lendas_historias": True},
)

_esp(
    "Espião",
    "Agente infiltrado a serviço secreto de um governo, guilda, culto ou patrono.",
    "Você é treinado em Enganação e Ladinagem. Além disso, escolha uma de suas perícias (exceto Luta ou Pontaria): você pode usar Carisma como atributo-chave dessa perícia.",
    "Estojo de disfarces, gazua, luneta, três doses de cosmético.",
    ["Enganação", "Ladinagem"],
    {"espiao_pericia_carisma": True},
)

_esp(
    "Ferreiro Militar",
    "Forjador de armas e armaduras para soldados e oficiais em tempos de guerra.",
    "Você é treinado em Ofício (armeiro) e recebe +2 em rolagens de dano com martelos e marretas de qualquer tipo.",
    "Instrumentos de armeiro, martelo leve.",
    ["Ofício (Armeiro)"],
    {"dano_martelos_marretas": 2},
)

_esp(
    "Freira",
    "Dedicada ao serviço espiritual, caridade, ervas medicinais e proteção dos vulneráveis.",
    "Você é treinada em Cura. Pode gastar 1 PM para aumentar o bônus ao ajudar em +1d4 e 1 PM para aumentar efeitos de cura em +1 dado do mesmo tipo.",
    "Maleta de medicamentos, manto eclesiástico, símbolo sagrado.",
    ["Cura"],
    {"ajudar_extra_1pm": "1d4", "cura_dado_extra_1pm": 1},
)

_esp(
    "Goradista",
    "Mestre confeiteiro especialista em bolos, doces e receitas com gorad.",
    "Você é treinado em Ofício (cozinheiro). Ao preparar um prato especial, gaste +T$ 10 para adicionar cobertura de gorad, concedendo +2 PM temporários por patamar do comensal.",
    "Instrumentos de cozinheiro, T$ 36 em ingredientes para gorad quente.",
    ["Ofício (Cozinheiro)"],
    {"cobertura_gorad_pm_patamar": 2},
)

_esp(
    "Insciente",
    "Nascido em Wynlla sem aptidão mágica, acostumado a sobreviver sem auxílio arcano.",
    "Você é treinado em Sobrevivência e recebe resistência a magia +5.",
    "Uma arma simples ou ferramenta de até T$ 100.",
    ["Sobrevivência"],
    {"resistencia_magia_bonus": 5},
)

_esp(
    "Interrogador",
    "Antigo torturador ou agente implacável que busca redenção (ou fuga do passado).",
    "Você é treinado em Intimidação e Investigação e recebe +1 na margem de ameaça contra criaturas feridas (PV abaixo do total).",
    "Um ou mais itens somando T$ 100 pertencentes a antigos interrogados.",
    ["Intimidação", "Investigação"],
    {"margem_ameaca_vs_feridos": 1},
)

_esp(
    "Ladrão de Túmulos",
    "Saqueador de antigos campos de batalha e sepulturas pós-guerra.",
    "Você é treinado em Ladinagem e Sobrevivência, recebe +2 na Defesa e em testes de perícia contra mortos-vivos, e recebe redução de trevas 5 (ou recupera +1 PV/dado de trevas se for morto-vivo).",
    "Pá (estatísticas de lança), pé de cabra.",
    ["Ladinagem", "Sobrevivência"],
    {"resistencia_rd": {"Trevas": 5}, "bonus_vs_mortos_vivos": 2},
)

_esp(
    "Menestrel",
    "Músico itinerante de tavernas, festivais e cortes nobres.",
    "Você é treinado em Atuação e recebe um poder de Música de bardo escolhido entre Balada Fascinante, Canção Assustadora e Melodia Curativa.",
    "Um instrumento musical de até T$ 35 a sua escolha.",
    ["Atuação"],
    {"musica_bardo_escolha": ["Balada Fascinante", "Canção Assustadora", "Melodia Curativa"]},
)

_esp(
    "Mensageiro",
    "Portador veloz de cartas, tratados e pedidos de socorro por terras perigosas.",
    "Você recebe +3m em seu deslocamento e +2 em testes de resistência (Fortitude, Reflexos e Vontade).",
    "Cavalo com sela, mochila de aventureiro, traje de viajante.",
    [],
    {"deslocamento_bonus": 3, "bonus_pericia": {"Fortitude": 2, "Reflexos": 2, "Vontade": 2}},
)

_esp(
    "Náufrago",
    "Sobrevivente de naufrágio que aprendeu a improvisar tudo para sobreviver isolado.",
    "Você recebe +5 PV e +2 PM. Além disso, 1×/cena pode gastar 2 PM para receber treinamento em uma perícia, proficiência em arma/armadura/escudo ou usar uma ferramenta no lugar de outra pela cena.",
    "Arco curto, 20 flechas, uma bola (ou objeto simples) com cara pintada e nome.",
    [],
    {"pv_max_ini": 5, "pm_max_ini": 2},
)

_esp(
    "Padeiro",
    "Artesão de pães, bolos e tortas com braços fortalecidos pela massa e forno.",
    "Você é treinado em Ofício (cozinheiro), recebe +1 em rolagens de dano com armas de impacto e pode substituir testes de Atletismo por testes de Ofício (cozinheiro).",
    "Instrumentos de Ofício (cozinheiro), rolo de massa (estatísticas de clava).",
    ["Ofício (Cozinheiro)"],
    {"dano_armas_impacto": 1, "substitui_atletismo_por_cozinheiro": True},
)

_esp(
    "Pedinte",
    "Sobrevivente astuto das ruas que aprendeu a passar despercebido e aproveitar cada recurso.",
    "Você recebe +2 em Enganação e Furtividade. Ao usar alimento, preparado alquímico ou poção, pode rolar o efeito 2× e usar o melhor ou dividir 1 item com um aliado adjacente.",
    "Andrajos, 1 bálsamo restaurador e 1 essência de mana.",
    [],
    {"bonus_pericia": {"Enganação": 2, "Furtividade": 2}},
)

_esp(
    "Pescador",
    "Acostumado a aguardar o momento exato de puxar o anzol em rios e mares de Arton.",
    "Você é treinado em Ofício (pescador), recebe +2 em Iniciativa e +2 em testes para executar uma ação preparada.",
    "Bolsa cheia de minhocas, instrumentos de pescador.",
    ["Ofício (Pescador)"],
    {"bonus_pericia": {"Iniciativa": 2}, "bonus_acao_preparada": 2},
)

_esp(
    "Servo",
    "Serviçal de castelos ou palácios acostumado à etiqueta e intrigas da nobreza.",
    "Você é treinado em Diplomacia e Ofício (serviçal), recebe +2 em Diplomacia e Enganação contra alvos de status superior e pode substituir testes de Nobreza por Ofício (serviçal).",
    "Balde e vassoura (estatísticas de bordão), tabardo de seu patrono.",
    ["Diplomacia", "Ofício (Serviçal)"],
    {"substitui_nobreza_por_servical": True},
)

_esp(
    "Suporte de Tropas",
    "Apoiador logístico de exércitos em marcha e expedições aventureiras.",
    "Sempre que faz um teste para ajudar, o bônus fornecido aumenta em +2. Além disso, ao flanquear um inimigo, o bônus de ataque para você e aliados aumenta para +4.",
    "Equipamento de viagem, instrumentos de ofício, maleta de medicamentos.",
    [],
    {"ajudar_bonus_extra": 2, "flanquear_bonus_total": 4},
)
