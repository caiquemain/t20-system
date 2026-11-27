# -*- coding: utf-8 -*-
"""Equipamentos, Melhorias, Materiais Especiais, Recursos Naturais e Itens Mágicos
do suplemento Ameaças de Arton (Capítulo 3, p. 392–403).
"""

_F = "Ameaças de Arton"

# ── TABELA 3-1: NOVAS ARMAS (p. 392–394) ──
DADOS_ARMAS_AMEACAS = {
    # Simples
    "Porrete": {
        "fonte": _F, "categoria": "Simples", "proposito": "Corpo a Corpo", "empunhadura": "Leve",
        "preco": 2, "dano": "1d6", "critico": "x2", "alcance": "—", "tipo": "Impacto", "espaco": 1,
        "habilidades": ["não letal"],
        "descricao": "Pedaço sólido de madeira coberto por lã; causa dano não letal.",
    },
    "Zarabatana": {
        "fonte": _F, "categoria": "Simples", "proposito": "À Distância", "empunhadura": "Uma Mão",
        "preco": 5, "dano": "1d3", "critico": "x2", "alcance": "Curto", "tipo": "Perfuração", "espaco": 1,
        "habilidades": ["veneno +2 CD"],
        "descricao": "Dispara dardos (20 por T$ 2, 0,5 esp); +2 na CD de venenos aplicados nos dardos.",
    },
    # Marciais
    "Neko-te": {
        "fonte": _F, "categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Leve",
        "preco": 10, "dano": "1d4", "critico": "19", "alcance": "—", "tipo": "Corte", "espaco": 1,
        "habilidades": ["escalar +2"],
        "descricao": "Luva com garras metálicas. +2 em Atletismo para escalar (conta como mão livre); com duas, +1,5m deslocamento de escalada.",
    },
    "Gládio": {
        "fonte": _F, "categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 12, "dano": "1d6", "critico": "19/x3", "alcance": "—", "tipo": "Perfuração", "espaco": 1,
        "habilidades": [],
        "descricao": "Espada de lâmina curta e pesada sem guarda, padrão dos legionários do Império de Tauron.",
    },
    "Tetsubo": {
        "fonte": _F, "categoria": "Marcial", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos",
        "preco": 20, "dano": "1d10", "critico": "x2", "alcance": "—", "tipo": "Impacto", "espaco": 2,
        "habilidades": ["versátil"], "versatil": "derrubar ou empurrar",
        "descricao": "Tacape pesado reforçado com metal; versátil (+2 em testes para derrubar ou empurrar).",
    },
    # Armas de Fogo
    "Traque": {
        "fonte": _F, "categoria": "Fogo", "proposito": "À Distância", "empunhadura": "Leve",
        "preco": 75, "dano": "2d6", "critico": "19/x3", "alcance": "Curto", "tipo": "Perfuração", "espaco": 1,
        "habilidades": ["recarga padrão", "frágil (erro ímpar avaria)"],
        "descricao": "Arma de fogo feita de sucata; se errar ataque com resultado ímpar no d20, fica avariada. Recarga padrão.",
    },
    "Arcabuz": {
        "fonte": _F, "categoria": "Fogo", "proposito": "À Distância", "empunhadura": "Duas Mãos",
        "preco": 800, "dano": "2d10", "critico": "19/x3", "alcance": "Médio", "tipo": "Perfuração", "espaco": 2,
        "habilidades": ["desbalanceada", "recarga padrão"],
        "descricao": "Versão mais pesada e potente do mosquete; desbalanceada (-2 ataque). Recarga padrão.",
    },
    "Bacamarte": {
        "fonte": _F, "categoria": "Fogo", "proposito": "À Distância", "empunhadura": "Duas Mãos",
        "preco": 450, "dano": "4d6", "critico": "19/x3", "alcance": "Cone 6m", "tipo": "Perfuração", "espaco": 2,
        "habilidades": ["cone 6m", "recarga completa (2 balas)"],
        "descricao": "Espalha munição em cone de 6m (compara 1 ataque à distância contra Defesa de cada criatura). Recarga completa e 2 balas.",
    },
    # Exóticas
    "Açoite finntroll": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 30, "dano": "1d8", "critico": "x2", "alcance": "—", "tipo": "Corte", "espaco": 1,
        "habilidades": ["dor (-2 perícias/dano 1 rod.)"],
        "descricao": "Criatura que sofra dano sofre –2 em testes de perícia e rolagens de dano por 1 rodada (metabolismo).",
    },
    "Espada vespa": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 75, "dano": "2d4", "critico": "18", "alcance": "—", "tipo": "Corte ou Perfuração", "espaco": 1,
        "habilidades": [],
        "descricao": "Feita com três ferrões de vespas gigantes; pode causar dano de corte ou perfuração.",
    },
    "Pistola-punhal": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 300, "dano": "1d6", "critico": "18", "alcance": "Curto", "tipo": "Perfuração", "espaco": 1,
        "habilidades": ["ágil", "híbrida"],
        "modos": {
            "corpo_a_corpo": {"dano": "1d6", "critico": "18", "habilidades": ["ágil"]},
            "arma_de_fogo": {"dano": "2d6", "critico": "19/x3", "alcance": "Curto"},
        },
        "descricao": "Arma híbrida: corpo a corpo ágil (1d6, 18; pode disparar bala p/ +2d6) ou arma de fogo (2d6, 19/x3, curto; exige prof. fogo).",
    },
    "Mordida do diabo": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 30, "dano": "1d4", "critico": "x2", "alcance": "3m", "tipo": "Perfuração", "espaco": 1,
        "habilidades": ["ágil", "versátil"], "versatil": "agarrar e desarmar",
        "descricao": "Mandíbula em corrente (alcança 3m); ágil e versátil (+2 agarrar e desarmar).",
    },
    "Presa de serpente": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Uma Mão",
        "preco": 1000, "dano": "1d8", "critico": "17", "alcance": "—", "tipo": "Corte", "espaco": 1,
        "habilidades": ["ágil", "crítico +1 passo"],
        "descricao": "Espada de obsidiana ágil; em crítico, dano aumenta 1 passo antes de multiplicar. Não aceita material especial.",
    },
    "Lança de fogo": {
        "fonte": _F, "categoria": "Exótica", "proposito": "Corpo a Corpo", "empunhadura": "Duas Mãos",
        "preco": 1000, "dano": "1d10", "critico": "x3", "alcance": "Médio", "tipo": "Perfuração", "espaco": 2,
        "habilidades": ["alongada", "híbrida"],
        "modos": {
            "corpo_a_corpo": {"dano": "1d10", "critico": "x3", "habilidades": ["alongada"]},
            "arma_de_fogo": {"dano": "2d8", "critico": "19/x3", "alcance": "Médio"},
        },
        "descricao": "Arma híbrida: corpo a corpo alongada (1d10, x3; pode disparar bala p/ +2d8) ou arma de fogo (2d8, 19/x3, médio; +1d8 adjacente).",
    },
    "Shuriken": {
        "fonte": _F, "categoria": "Exótica", "proposito": "À Distância", "empunhadura": "Leve",
        "preco": 1, "dano": "1d4", "critico": "x2", "alcance": "Curto", "tipo": "Perfuração", "espaco": 0.5,
        "habilidades": ["arremesso", "1 PM ataque extra"],
        "descricao": "1x/rodada ao atacar, 1 PM p/ ataque extra no mesmo alvo (com Arremesso Múltiplo, sem custo de PM).",
    },
    "Arpão": {
        "fonte": _F, "categoria": "Exótica", "proposito": "À Distância", "empunhadura": "Uma Mão",
        "preco": 30, "dano": "1d10", "critico": "x3", "alcance": "Curto", "tipo": "Perfuração", "espaco": 1,
        "habilidades": ["arremesso", "permitida Oceano"],
        "descricao": "Prende no alvo (corda 9m, Força oposta; soltar gasta movimento e perde 1d10 PV). Permitida para devotos do Oceano.",
    },
}

# ── TABELA 3-2: NOVAS ARMADURAS E ESCUDOS (p. 395) ──
DADOS_ARMADURAS_AMEACAS = {
    "Armadura de ossos": {
        "fonte": _F, "tipo_armadura": "Leve", "preco": 120, "bonus_defesa": 3, "penalidade_armadura": -2, "espaco": 2,
        "bonus_pericia": {"Intimidação": 1},
        "descricao": "+1 em Intimidação e na CD de efeitos de medo (cumulativo com melhoria macabra).",
    },
    "Veste de teia de aranha": {
        "fonte": _F, "tipo_armadura": "Leve", "preco": 3000, "bonus_defesa": 4, "penalidade_armadura": 0, "espaco": 2,
        "bonus_pericia": {"Furtividade": 5},
        "descricao": "+5 em Furtividade. Não pode receber melhoria material especial.",
    },
    "Armadura de quitina": {
        "fonte": _F, "tipo_armadura": "Pesada", "preco": 350, "bonus_defesa": 7, "penalidade_armadura": -3, "espaco": 5,
        "sem_penalidade_deslocamento": True,
        "descricao": "Armadura pesada feita de carapaças de insetos gigantes; não reduz o deslocamento do usuário.",
    },
    "Escudo de couro": {
        "fonte": _F, "tipo_armadura": "Escudo", "preco": 3, "bonus_defesa": 1, "penalidade_armadura": -1, "espaco": 1,
        "descricao": "+2 adicional na Defesa contra ataques à distância. Muito leve para ser usado como arma.",
    },
}

# ── TABELA 3-3: NOVOS ITENS GERAIS (p. 396–399) ──
DADOS_GERAIS_AMEACAS = {
    # Equipamento de Aventura
    "Caixa de voz": {"fonte": _F, "categoria": "Aventura", "preco": 0, "espaco": 1, "descricao": "1d4 cargas; aumenta em 1 passo alcance curto/médio de habilidade de bardo ou nobre."},
    "Corda de teia": {"fonte": _F, "categoria": "Aventura", "preco": 50, "espaco": 1, "descricao": "Corda de 10m resistente (5 dano de corte ou Força CD 28 para arrebentar)."},
    "Dente de wisphago": {"fonte": _F, "categoria": "Aventura", "preco": 100, "espaco": 1, "descricao": "Amuleto consumível: rerrola teste de resistência contra magia arcana com +2."},
    "Gema de força": {"fonte": _F, "categoria": "Aventura", "preco": 100, "espaco": 1, "descricao": "1d4 cargas; ação padrão produz domo de Campo de Força ou reduz custo da magia em –2 PM."},
    # Vestuário
    "Garra feroz": {"fonte": _F, "categoria": "Vestuário", "preco": 60, "espaco": 1, "descricao": "Funciona como manopla e aplica benefícios a garras/armas naturais sob Forma Selvagem."},
    "Manto do mantor": {"fonte": _F, "categoria": "Vestuário", "preco": 450, "espaco": 1, "descricao": "Na escuridão completa fornece camuflagem total, mesmo contra visão no escuro."},
    "Manto pesado": {"fonte": _F, "categoria": "Vestuário", "preco": 10, "espaco": 1, "descricao": "Imunidade à condição ofuscado; não é considerado sob luz solar durante o dia."},
    "Sombreiro": {"fonte": _F, "categoria": "Vestuário", "preco": 10, "espaco": 1, "descricao": "Resistência a efeitos de sentidos +2."},
    "Traje selako": {"fonte": _F, "categoria": "Vestuário", "preco": 90, "espaco": 1, "descricao": "+2 em Atletismo para nadar e +3m em deslocamento de natação."},
    # Esotéricos
    "Ankh solar": {"fonte": _F, "categoria": "Esotérico", "preco": 450, "espaco": 1, "descricao": "Pode ser usado como arma leve simples (1d6, 19, corte). Aprimoramento +2 PM em magias com TR: falha impede cura por 1 rodada."},
    "Tomo de guerra": {"fonte": _F, "categoria": "Esotérico", "preco": 300, "espaco": 1, "descricao": "Ao lançar magia de evocação, recebe +1 PM para gastar em aprimoramentos."},
    "Tomo do rancor": {"fonte": _F, "categoria": "Esotérico", "preco": 750, "espaco": 1, "descricao": "Aprimoramento +2 PM em magias de dano: +2d8+2 dano de corte, impacto ou perfuração."},
    # Alquímicos — Preparados
    "Bálsamo de drogadora": {"fonte": _F, "categoria": "Alquímico", "preco": 60, "espaco": 0.5, "descricao": "Ação completa; cura 4d6+4 PV."},
    "Bomba de fumaça": {"fonte": _F, "categoria": "Alquímico", "preco": 15, "espaco": 0.5, "descricao": "Nuvem de fumaça raio 6m pela cena (camuflagem leve até 1,5m, total a partir de 3m)."},
    "Elixir quimérico": {"fonte": _F, "categoria": "Alquímico", "preco": 120, "espaco": 0.5, "descricao": "Ação padrão; pela cena ganha mordida 1d6 perfuração (ou +1 passo se já possuir)."},
    "Éter elemental": {"fonte": _F, "categoria": "Alquímico", "preco": 60, "espaco": 0.5, "descricao": "Ação padrão em arma ou 20 munições: +1d4 dano elemental pela cena."},
    "Isca putrefata": {"fonte": _F, "categoria": "Alquímico", "preco": 60, "espaco": 0.5, "descricao": "Arremesso alcance médio; atrai mortos-vivos não inteligentes em alcance curto por 1d6 rodadas."},
    "Lágrima pétrea": {"fonte": _F, "categoria": "Alquímico", "preco": 30, "espaco": 0.5, "descricao": "Ação padrão adjacente ou arremesso curto; remove efeitos de metamorfose (Ref CD Des evita)."},
    "Óleo de baleia": {"fonte": _F, "categoria": "Alquímico", "preco": 30, "espaco": 0.5, "descricao": "Ação padrão em arma/munição; ignora penalidades de combate submerso pela cena."},
    "Óleo de besouro": {"fonte": _F, "categoria": "Alquímico", "preco": 50, "espaco": 0.5, "descricao": "Explosivo alcance curto (raio 3m): 4d6 fogo e em chamas (Ref CD Des metade e evita)."},
    "Pó azul": {"fonte": _F, "categoria": "Alquímico", "preco": 150, "espaco": 0.5, "descricao": "Inalar (ação completa): recupera 2d4 PM."},
    # Alquímicos — Catalisadores
    "Corrosivo mineral": {"fonte": _F, "categoria": "Catalisador", "preco": 150, "espaco": 0.5, "descricao": "Aumenta dados de dano de magias de ácido em 1 categoria (até d12)."},
    "Gelo extremo": {"fonte": _F, "categoria": "Catalisador", "preco": 150, "espaco": 0.5, "descricao": "Aumenta dados de dano de magias de frio em 1 categoria (até d12)."},
    "Pedaço de língua": {"fonte": _F, "categoria": "Catalisador", "preco": 30, "espaco": 0.5, "descricao": "+1 na CD de testes de Fortitude contra suas magias."},
    "Raio cristalizado": {"fonte": _F, "categoria": "Catalisador", "preco": 150, "espaco": 0.5, "descricao": "Aumenta dados de dano de magias de eletricidade em 1 categoria (até d12)."},
    # Alquímicos — Venenos
    "Esporos de cogumelo": {"fonte": _F, "categoria": "Veneno", "preco": 75, "espaco": 0.5, "descricao": "Inalação: paralisada (lenta) por 1 rodada."},
    "Peçonha anciã": {"fonte": _F, "categoria": "Veneno", "preco": 1800, "espaco": 0.5, "descricao": "Contato: perde 3d12 PV/rodada por 3 rodadas e ignora imunidade a venenos (3d12 PV)."},
    "Peçonha irritante": {"fonte": _F, "categoria": "Veneno", "preco": 10, "espaco": 0.5, "descricao": "Contato: perde 1d6 PV (sem teste de resistência)."},
    "Veneno batráquio": {"fonte": _F, "categoria": "Veneno", "preco": 30, "espaco": 0.5, "descricao": "Contato: perde 1d12 PV e enjoado 1 rodada (1d6 PV)."},
    # Alimentação
    "Algravia": {"fonte": _F, "categoria": "Alimentação", "preco": 3, "espaco": 0.5, "descricao": "+1 em perícias de Carisma (cumulativo; doses extras exigem Fort CD 15+5/dose)."},
    "Banquete de canceronte": {"fonte": _F, "categoria": "Alimentação", "preco": 36, "espaco": 0.5, "descricao": "1d4+1 dados de auxílio (+1d4 em perícia; d6 com Mestre Cuca)."},
    "Coc-au-triz": {"fonte": _F, "categoria": "Alimentação", "preco": 54, "espaco": 0.5, "descricao": "Reduz custo de uma habilidade escolhida em –1 PM."},
    "Cozido de serpe": {"fonte": _F, "categoria": "Alimentação", "preco": 12, "espaco": 0.5, "descricao": "+1 em todos os testes de perícia (cumulativo; exige preparo estendido CD 20)."},
    "Gorlogg ensopado": {"fonte": _F, "categoria": "Alimentação", "preco": 6, "espaco": 0.5, "descricao": "Na próxima noite de sono, recuperação de PV e PM aumenta em +1 por nível."},
    "Omelete monstruosa": {"fonte": _F, "categoria": "Alimentação", "preco": 3, "espaco": 0.5, "descricao": "+2 dano e –2 em perícias de Sabedoria (+5 / –5 se ovos de dragão)."},
    "Sashimi de kraken": {"fonte": _F, "categoria": "Alimentação", "preco": 60, "espaco": 0.5, "descricao": "+2 em Diplomacia (cumulativo) e 5 PM temporários."},
    # Animais (Parceiros Iniciantes)
    "Bulette": {"fonte": _F, "categoria": "Animal", "preco": 500, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Capivara": {"fonte": _F, "categoria": "Animal", "preco": 60, "espaco": 0, "descricao": "Parceiro montaria iniciante (para Pequenos e Minúsculos)."},
    "Corcel do deserto": {"fonte": _F, "categoria": "Animal", "preco": 150, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Dromedário": {"fonte": _F, "categoria": "Animal", "preco": 75, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Elefante": {"fonte": _F, "categoria": "Animal", "preco": 1500, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Hiena": {"fonte": _F, "categoria": "Animal", "preco": 220, "espaco": 0, "descricao": "Parceiro especial (com Adestramento) ou montaria para Pequenos/Minúsculos."},
    "Leão": {"fonte": _F, "categoria": "Animal", "preco": 800, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Rinoceronte": {"fonte": _F, "categoria": "Animal", "preco": 600, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
    "Urso pardo": {"fonte": _F, "categoria": "Animal", "preco": 300, "espaco": 0, "descricao": "Parceiro montaria iniciante."},
}

# ── NOVAS MELHORIAS (p. 399) ──
DADOS_MELHORIAS_AMEACAS = {
    "Multifuncional": {
        "fonte": _F, "aplica_em": ["Ferramenta", "Vestuário"],
        "efeito": "Aplica o bônus/redução do item a uma segunda perícia do mesmo atributo-chave (não se aplica a ataques).",
    },
    "Penetrante": {
        "fonte": _F, "aplica_em": ["Arma"], "requisito": "Cruel",
        "efeito": "A arma ignora 5 pontos de redução de dano.",
    },
}

# ── TABELA 3-4: NOVOS MATERIAIS ESPECIAIS (p. 399–401) ──
DADOS_MATERIAIS_AMEACAS = {
    "Casco de monstro": {
        "fonte": _F, "precos": {"arma": 750, "armadura_leve": 750, "armadura_pesada": 6000, "escudo": 750, "esoterico": 3000},
        "arma": "Conta como arma primitiva para Armamento da Natureza e similares.",
        "armadura_escudo": "Penalidade de armadura –1; armaduras pesadas aplicam até 1 ponto de Destreza na Defesa.",
        "esoterico": "Ao lançar magia, recebe RD 5 contra o próximo dano até sua próxima rodada.",
    },
    "Couraça de kaiju": {
        "fonte": _F, "precos": None,
        "arma": "Dano +1 passo; 2 PM para ignorar efeitos de redução de dano (exceto RD), como Durão.",
        "armadura_escudo": "Leve/escudo: RD 10/mágico; Pesada: RD 20/mágico.",
        "esoterico": "2 PM em magia de dano para ignorar Durão/Evasão (exceto RD e TR).",
    },
    "Couro de bulette": {
        "fonte": _F, "precos": None,
        "armadura_escudo": "Escavação metade do deslocamento; Leve: RD ácido 5; Pesada: RD ácido 10.",
        "esoterico": "Em magias de ácido que causam dano, rerrola resultados 1.",
    },
    "Cristal de sol": {
        "fonte": _F, "precos": None,
        "arma": "Apenas corte/perfuração; +2 dano de fogo.",
        "armadura_escudo": "Rola 2 dados e usa o melhor em TR contra frio.",
        "esoterico": "1 PM em magia de fogo: quem falhar no TR fica em chamas (ou +1d6 cumulativo).",
    },
    "Lanajuste": {
        "fonte": _F, "precos": {"arma": 600, "armadura_leve": 1500, "armadura_pesada": 6000, "escudo": 1500, "esoterico": 3000},
        "arma": "Ignora penalidades de combate submerso; permitida para devotos do Oceano.",
        "armadura_escudo": "Leve/escudo: RD corte 5; Pesada: RD corte 10.",
        "esoterico": "Em magias de corte, rerrola resultados 1 na rolagem de dano.",
    },
    "Pena de kraken": {
        "fonte": _F, "precos": None,
        "arma": "Em acerto crítico, dano aumenta 2 passos antes de multiplicar.",
        "armadura_escudo": "Quando inimigo erra ataque corpo a corpo: perde 5 PV (leve/escudo) ou 10 PV (pesada).",
        "esoterico": "Se fornece bônus numérico, aumenta em +1.",
    },
    "Prata": {
        "fonte": _F, "precos": {"arma": 600, "armadura_leve": 1500, "armadura_pesada": 3000, "escudo": 1500, "esoterico": 400},
        "revestimento": True,
        "arma": "+2 dano em espíritos e mortos-vivos; conta como mágica contra eles.",
        "armadura_escudo": "RD 5 (leve/escudo) ou RD 10 (pesada) contra espíritos e mortos-vivos.",
        "esoterico": "Magias causam +2 dano em espíritos e mortos-vivos.",
    },
    "Quitina razza": {
        "fonte": _F, "precos": None,
        "arma": "Dado explosivo no dano básico da arma (resultado máximo rola dado extra).",
        "armadura_escudo": "Leve/escudo: +2 Percepção e +1 Defesa; Pesada: +5 Percepção e +2 Defesa.",
        "esoterico": "Dado explosivo no dano básico da magia.",
    },
}

# ── TABELAS 3-5 E 3-6: RECURSOS NATURAIS (REGRA OPCIONAL, p. 401–402) ──
RECURSOS_NATURAIS_PATAMAR = {
    "Iniciante": {"valor": 20, "qualidade": "itens normais"},
    "Veterano": {"valor": 100, "qualidade": "itens superiores"},
    "Campeão": {"valor": 500, "qualidade": "itens mágicos"},
    "Lenda": {"valor": 2500, "qualidade": "itens mágicos"},
}

RECURSOS_NATURAIS_UNIDADES_TAMANHO = {
    "Minúsculo": 0,
    "Pequeno": 1,
    "Médio": 1,
    "Grande": 2,
    "Enorme": 2,
    "Colossal": 5,
}

# ── NOVOS ITENS MÁGICOS & ARTEFATOS (p. 402–403) ──
DADOS_ITENS_MAGICOS_AMEACAS = {
    "Chifre de unicórnio": {
        "fonte": _F, "tipo": "Acessório Maior", "preco": 120000,
        "efeito": "Lança Curar Ferimentos e Purificação (-1 PM se já conhece); pode lançar Segunda Chance (perde poderes); espada curta formidável.",
    },
    "Fragmento de filactério": {
        "fonte": _F, "tipo": "Acessório Maior", "preco": 90000, "pm_bonus": 20,
        "efeito": "Costela de lich poderosa que fornece +20 PM (após 1 dia de uso).",
    },
    "Grilhão de descrença": {
        "fonte": _F, "tipo": "Armadura Específica Menor", "preco": 24000,
        "efeito": "Armadura completa reforçada e selada amaldiçoada; não pode ser retirada; a 0 PV vira guerreiro perpétuo.",
    },
    "Pilão conspurcado": {
        "fonte": _F, "tipo": "Acessório Médio", "preco": 21000,
        "reducao_pm_escolas": ["Encantamento", "Necromancia"], "cd_bonus_escolas": {"Encantamento": 2, "Necromancia": 2},
        "efeito": "Costela de lich; –1 PM e +2 CD em magias de encantamento e necromancia.",
    },
    "Pistola demoníaca": {
        "fonte": _F, "tipo": "Arma Específica Média", "preco": 72250,
        "efeito": "Pistola ameaçadora formidável profana sempre carregada; 1x/dia impulso homicida (Von CD 25).",
    },
    "Uyzrrak Da'ukthra": {
        "fonte": _F, "tipo": "Arma Específica Média", "preco": 78050,
        "efeito": "Machado de guerra magnífico aumentado atroz de adamante; +2d8 vs não-duyshidakk + encanto do Akzath.",
    },
    "Amuleto do Abutre": {
        "fonte": _F, "tipo": "Artefato", "preco": 0, "pm_bonus": 50, "cd_arcana_bonus": 5,
        "efeito": "+50 PM (após 1 dia), +5 CD magias arcanas, Conhecimento Sequestrado (CD Int); filactério de Ferren Asloth (Von CD 20+1/dia).",
    },
    "Rompedor da Realidade": {
        "fonte": _F, "tipo": "Artefato", "preco": 0,
        "efeito": "Machado de guerra gigante atroz pungente anticriatura (não lefeu) magnífico de matéria vermelha; ignora RD/fortificação/imunidade a crítico.",
    },
}

# Regra opcional: Lancinante Revisado (p. 403)
REGRA_OPCIONAL_LANCINANTE_REVISADO = {
    "id": "lancinante_revisado",
    "fonte": _F,
    "nome": "Lancinante Revisado",
    "descricao": "Quando faz um acerto crítico, o bônus em dano fornecido pelo encanto dilacerante também é multiplicado (pré-requisito: dilacerante).",
}
