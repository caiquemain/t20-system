"""Catálogo do Capítulo 8 — Recompensas & Itens Mágicos (T20 Jogo do Ano, p.326–348).

Inclui:
- Tabela 8-6: Tesouro Médio por Cena
- Tabela 8-7: Preço de Encantos (e bônus de destruição/resistência/sacrifício de PM)
- Tabela 8-8: Encantos de Armas (29 encantos)
- Tabela 8-9: Armas Específicas (18 armas)
- Tabela 8-10: Encantos de Armaduras & Escudos (25 encantos)
- Tabela 8-11: Armaduras & Escudos Específicos (13 itens)
- Tabela 8-12: Poções (38 entradas)
- Tabelas 8-13, 8-14 e 8-15: Acessórios Menores (21), Médios (22) e Maiores (21)
- Artefatos (4 relíquias) e Tabela do Baralho do Caos (22 cartas)
"""

# Tabela 8-6: Tesouro Médio por Cena (T20 JdA p.332)
TESOURO_MEDIO_POR_CENA = {
    1: 300, 2: 300, 3: 400, 4: 1000, 5: 1000,
    6: 2000, 7: 2000, 8: 3000, 9: 3000, 10: 6000,
    11: 8000, 12: 9000, 13: 13000, 14: 17000, 15: 22000,
    16: 22000, 17: 40000, 18: 50000, 19: 60000, 20: 72000,
}

# Tabela 8-7: Preço de Encantos e categorias de itens mágicos (T20 JdA p.334–335)
PRECO_ENCANTOS = {
    1: {"categoria": "Menor", "aumento_preco": 18000, "aumento_cd": 10, "sacrificio_pm": 1, "pv_rd_bonus": 10, "resistencia_item": 5},
    2: {"categoria": "Médio", "aumento_preco": 36000, "aumento_cd": 15, "sacrificio_pm": 2, "pv_rd_bonus": 20, "resistencia_item": 10},
    3: {"categoria": "Maior", "aumento_preco": 72000, "aumento_cd": 20, "sacrificio_pm": 3, "pv_rd_bonus": 40, "resistencia_item": 20},
}

CATEGORIAS_ITEM_MAGICO = {
    "Menor": {"cd_oficio": 30, "sacrificio_pm": 1, "pv_rd_bonus": 10, "resistencia_item": 5},
    "Médio": {"cd_oficio": 40, "sacrificio_pm": 2, "pv_rd_bonus": 20, "resistencia_item": 10},
    "Maior": {"cd_oficio": 50, "sacrificio_pm": 3, "pv_rd_bonus": 40, "resistencia_item": 20},
}

# Tabela 8-8: Encantos de Armas Mágicas (T20 JdA p.335–336 — 29 encantos)
ENCANTOS_ARMAS = {
    "Ameaçadora": {"d100": "01-05", "conta_como": 1, "efeito": "Duplica margem de ameaça", "descricao": "A margem de ameaça da arma duplica (aplicado antes de aumentos)."},
    "Anticriatura": {"d100": "06-10", "conta_como": 1, "efeito": "Bônus contra tipo de criatura", "descricao": "1/rodada ao atacar o tipo escolhido, gaste 2 PM para causar +4d8 de dano."},
    "Arremesso": {"d100": "11-12", "conta_como": 1, "efeito": "Pode ser arremessada", "descricao": "Pode ser arremessada em alcance curto (ou aumenta alcance em 1 categoria) e volta voando (pegá-la é reação)."},
    "Assassina": {"d100": "13-14", "conta_como": 1, "efeito": "Aumenta ataque furtivo", "descricao": "Dados de Ataque Furtivo viram d8; por 2 PM, rola novamente resultados 1 nos dados extras."},
    "Caçadora": {"d100": "15-16", "conta_como": 1, "efeito": "Ignora camuflagem leve/total e cobertura leve", "descricao": "Anula penalidades por camuflagem leve/total e cobertura leve; aumenta alcance de armas à distância em 1 categoria."},
    "Congelante": {"d100": "17-21", "conta_como": 1, "efeito": "+1d6 de dano de frio", "descricao": "+1d6 dano de frio; 1/rodada, gaste 2 PM ao acertar para deixar a vítima enredada por 1 rodada."},
    "Conjuradora": {"d100": "22-23", "conta_como": 1, "efeito": "Pode guardar e lançar magias", "descricao": "Guarda uma magia de alvo ou área; ao acertar um ataque, descarrega como ação livre sem pagar PM."},
    "Corrosiva": {"d100": "24-28", "conta_como": 1, "efeito": "+1d6 de dano de ácido", "descricao": "+1d6 dano de ácido; 1/rodada, gaste 2 PM ao acertar para causar +4d4 ácido na próxima rodada."},
    "Dançarina": {"d100": "29-30", "conta_como": 1, "efeito": "Ataca sozinha", "descricao": "Ação de movimento e 1 PM (sustentada): flutua e ataca em alcance curto com suas estatísticas."},
    "Defensora": {"d100": "31-34", "conta_como": 1, "efeito": "Defesa +2", "descricao": "Você recebe +2 na Defesa."},
    "Destruidora": {"d100": "35-36", "conta_como": 1, "efeito": "Bônus contra construtos", "descricao": "Contra construtos e objetos (quebrar): +2 no ataque e +2d8 de dano."},
    "Dilacerante": {"d100": "37-38", "conta_como": 1, "efeito": "+10 de dano em acertos críticos", "descricao": "Em acertos críticos, causa +10 pontos de dano."},
    "Drenante": {"d100": "39-40", "conta_como": 1, "efeito": "Crítico drena vítima", "descricao": "Em acerto crítico contra criatura viva, ela fica fraca e você ganha 2d10 PV temporários."},
    "Elétrica": {"d100": "41-45", "conta_como": 1, "efeito": "+1d6 de dano de eletricidade", "descricao": "+1d6 dano de eletricidade; 1/rodada, gaste 2 PM ao acertar para raio atingir outra criatura em alcance curto (3d8 eletricidade)."},
    "Energética": {"d100": "46", "conta_como": 2, "prerequisito": "Formidável", "efeito": "Bônus em ataque", "descricao": "+4 ataque, ignora 20 RD, converte todo dano para essência e emana luz como tocha."},
    "Excruciante": {"d100": "47-48", "conta_como": 1, "efeito": "Causa fraqueza", "descricao": "Criatura viva atingida fica fraca (ou debilitada se já estiver fraca)."},
    "Flamejante": {"d100": "49-53", "conta_como": 1, "efeito": "+1d6 de dano de fogo", "descricao": "+1d6 dano de fogo; 1/rodada, gaste 2 PM em vez do ataque normal para Bola de Fogo (6d6, alcance médio, Ref CD For ou Des reduz à metade)."},
    "Formidável": {"d100": "54-63", "conta_como": 1, "efeito": "Ataque e dano +2", "descricao": "+2 em testes de ataque e rolagens de dano."},
    "Lancinante": {"d100": "64", "conta_como": 2, "prerequisito": "Dilacerante", "efeito": "Causa crítico terrível", "descricao": "Em acerto crítico, +10 dano ou multiplica também bônus numéricos (substitui Dilacerante)."},
    "Magnífica": {"d100": "65-72", "conta_como": 2, "prerequisito": "Formidável", "efeito": "Ataque e dano +4", "descricao": "+4 em testes de ataque e rolagens de dano."},
    "Piedosa": {"d100": "73-74", "conta_como": 1, "efeito": "Dano não letal", "descricao": "+1d8 de dano, todo dano é não letal (1 PM ativa/desativa)."},
    "Profana": {"d100": "75-76", "conta_como": 1, "efeito": "Bônus contra devotos do Bem", "descricao": "+2d8 de dano contra devotos de deuses de energia positiva e criaturas bondosas."},
    "Sagrada": {"d100": "77-78", "conta_como": 1, "efeito": "Bônus contra devotos do Mal", "descricao": "+2d8 de dano contra devotos de deuses de energia negativa e criaturas malignas."},
    "Sanguinária": {"d100": "79-80", "conta_como": 1, "efeito": "Causa sangramento", "descricao": "Criatura viva atingida fica sangrando (perda de PV cumulativa)."},
    "Trovejante": {"d100": "81-82", "conta_como": 1, "efeito": "Causa atordoamento", "descricao": "Em acerto crítico, vítima fica atordoada por 1 rodada (1/cena, Fort CD For ou Des evita)."},
    "Tumular": {"d100": "83-84", "conta_como": 1, "efeito": "+1d8 de dano de trevas", "descricao": "+1d8 dano de trevas; 1/rodada, gaste 2 PM para +2d8, mas perde 1d8 PV."},
    "Veloz": {"d100": "85-88", "conta_como": 1, "efeito": "Fornece ataque extra", "descricao": "Recebe Ataque Extra com esta arma (ou reduz seu custo em –1 PM se já possuir)."},
    "Venenosa": {"d100": "89-90", "conta_como": 1, "efeito": "Causa envenenamento", "descricao": "1/rodada, gaste 2 PM ao acertar para envenenar a vítima (1d12 PV/rodada por 3 rodadas)."},
}

# Tabela 8-9: Armas Específicas (T20 JdA p.336–338 — 18 armas, todas categoria Maior)
ARMAS_ESPECIFICAS = {
    "Azagaia dos relâmpagos": {"d100": "01-05", "preco": 30000, "categoria": "Maior", "descricao": "Ao ser arremessada, vira Relâmpago (8d6 eletricidade em linha média, CD For/Des) e retorna no fim do turno."},
    "Espada baronial": {"d100": "06-15", "preco": 30000, "categoria": "Maior", "descricao": "Espada longa +1 ataque/dano (+1 cumulativo por código de conduta, devoto de Khalmyr e treinado em Nobreza; até +4)."},
    "Lâmina da luz": {"d100": "16-25", "preco": 45000, "categoria": "Maior", "descricao": "Espada bastarda formidável; ação de movimento e 2 PM irradia luz em alcance médio pela cena (inimigos ofuscados)."},
    "Lança animalesca": {"d100": "26-30", "preco": 45000, "categoria": "Maior", "descricao": "Lança formidável; aplica +2 ataque e dano às armas naturais em Forma Selvagem."},
    "Maça do terror": {"d100": "31-35", "preco": 45000, "categoria": "Maior", "descricao": "Maça formidável; permite lançar Amedrontar (CD For/Car; –1 PM se já conhecer)."},
    "Florete fugaz": {"d100": "36-40", "preco": 50000, "categoria": "Maior", "descricao": "Florete formidável; ao agredir, gaste 1 PM para fazer ataque adicional se acertar crítico no turno."},
    "Cajado da destruição": {"d100": "41-45", "preco": 60000, "categoria": "Maior", "descricao": "Bordão formidável e cajado arcano; magias de dano causam +1 dano por dado."},
    "Cajado da vida": {"d100": "46-50", "preco": 60000, "categoria": "Maior", "descricao": "Bordão formidável (cajado arcano para magias divinas); magias de cura curam +2 PV por dado."},
    "Machado silvestre": {"d100": "51-55", "preco": 70000, "categoria": "Maior", "descricao": "Machado de batalha formidável; em ermos ao ar livre, +1d8 dano e Trespassar (ou 0 PM se já possuir)."},
    "Martelo de Doherimm": {"d100": "56-60", "preco": 70000, "categoria": "Maior", "descricao": "Martelo de guerra formidável; em mãos de anão, ganha Arremesso e +1d8 dano (+2d8 contra Grandes ou maiores)."},
    "Arco do poder": {"d100": "61-67", "preco": 90000, "categoria": "Maior", "descricao": "Arco longo formidável sem corda; dispara flechas energéticas: Normal (3d8 essência), Piedosa (4d8 não letal), Explosiva (3d6 fogo em área) ou Rede (agarrado CD 25)."},
    "Língua do deserto": {"d100": "68-72", "preco": 90000, "categoria": "Maior", "descricao": "Cimitarra formidável; 1 PM +1 passo/fogo pela cena; 2 PM deixa inimigos em alcance curto desprevenidos por 1 rodada."},
    "Besta explosiva": {"d100": "73-77", "preco": 100000, "categoria": "Maior", "descricao": "Besta pesada formidável; por 3 PM transforma virote em Bola de Fogo (6d6 fogo em raio 6m, Ref CD Des metade)."},
    "Punhal sszzaazita": {"d100": "78-82", "preco": 100000, "categoria": "Maior", "descricao": "Adaga assassina formidável venenosa; 2 PM disfarça em objeto inofensivo indetectável (ação livre volta a ser arma)."},
    "Espada sortuda": {"d100": "83-87", "preco": 110000, "categoria": "Maior", "descricao": "Espada curta formidável; +2 resistências e 3 PM para rolar teste novamente (–1 PM se tiver Sortudo)."},
    "Avalanche": {"d100": "88-92", "preco": 140000, "categoria": "Maior", "descricao": "Machado de guerra de gelo eterno congelante formidável; RD Fogo 10; 6 PM invoca tempestade de gelo (3d6 impacto + 3d6 frio/rodada, 1 PM/turno manter)."},
    "Cajado do poder": {"d100": "93-95", "preco": 180000, "categoria": "Maior", "descricao": "Bordão defensor magnífico e cajado arcano; –1 PM em magias arcanas (cumulativo com Mestre em Escola) e +2 CD (total +3)."},
    "Vingadora sagrada": {"d100": "96-100", "preco": 200000, "categoria": "Maior", "descricao": "Espada longa formidável; para paladino: +5 ataque/dano, Golpe Divino –1 PM e resistência a magia +5 para si e aliados em alcance curto."},
}

# Tabela 8-10: Encantos de Armaduras & Escudos Mágicos (T20 JdA p.338–339 — 25 encantos)
ENCANTOS_ARMADURAS_ESCUDOS = {
    "Abascanto": {"d100": "01-06", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra magia", "descricao": "Resistência a magia +5."},
    "Abençoado": {"d100": "07-10", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra trevas", "descricao": "RD Trevas 10 e +5 em testes de resistência contra necromancia."},
    "Acrobático": {"d100": "11-12", "conta_como": 1, "apenas_escudo": False, "efeito": "Bônus em Acrobacia", "descricao": "+5 em Acrobacia e ignora penalidade de armadura do item nessa perícia."},
    "Alado": {"d100": "13-14", "conta_como": 1, "apenas_escudo": False, "efeito": "Deslocamento de voo 12m", "descricao": "2 PM (sustentada): deslocamento de voo 12m."},
    "Animado": {"d100": "15-16", "conta_como": 1, "apenas_escudo": True, "efeito": "Escudo defende sozinho", "descricao": "Ação de movimento e 1 PM: escudo flutua pela cena mantendo bônus na Defesa com as mãos livres."},
    "Assustador": {"d100": "17-18", "conta_como": 1, "apenas_escudo": False, "efeito": "Causa efeito de medo", "descricao": "Ação de movimento e 2 PM: inimigos em alcance curto ficam abalados pela cena (Von CD Car evita)."},
    "Cáustica": {"d100": "19-22", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra ácido", "descricao": "RD Ácido 10; ação de movimento e 2 PM: ataques causam +1d4 ácido pela cena."},
    "Defensor": {"d100": "23-32", "conta_como": 1, "apenas_escudo": False, "efeito": "Defesa +2", "descricao": "Bônus na Defesa do item aumenta em +2."},
    "Escorregadio": {"d100": "33-34", "conta_como": 1, "apenas_escudo": False, "efeito": "Bônus para escapar", "descricao": "+10 em Acrobacia para escapar e testes de manobra contra agarrar."},
    "Esmagador": {"d100": "35-36", "conta_como": 1, "apenas_escudo": True, "efeito": "Escudo causa mais dano", "descricao": "Escudo fornece +2 em ataques e dano e dano aumentado em um passo."},
    "Fantasmagórico": {"d100": "37-38", "conta_como": 1, "apenas_escudo": False, "efeito": "Lança Manto de Sombras", "descricao": "Permite lançar a magia Manto de Sombras."},
    "Fortificado": {"d100": "39-40", "conta_como": 1, "apenas_escudo": False, "efeito": "Chance de ignorar crítico", "descricao": "25% (escudo) ou 50% (armadura) de chance de ignorar dano extra de críticos e ataques furtivos."},
    "Gélido": {"d100": "41-44", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra frio", "descricao": "RD Frio 10; ação de movimento e 2 PM: recebe 10 PV temporários pela cena."},
    "Guardião": {"d100": "45-54", "conta_como": 2, "apenas_escudo": False, "prerequisito": "Defensor", "efeito": "Defesa +4", "descricao": "Bônus na Defesa do item aumenta em +4."},
    "Hipnótico": {"d100": "55-56", "conta_como": 1, "apenas_escudo": False, "efeito": "Fascina inimigos", "descricao": "Ação padrão e 3 PM: inimigos em alcance curto ficam fascinados por 1d6 rodadas (Von CD Car evita)."},
    "Ilusório": {"d100": "57-58", "conta_como": 1, "apenas_escudo": False, "efeito": "Camufla-se como item comum", "descricao": "Ação de movimento e 1 PM: adquire aparência de roupa comum mantendo propriedades."},
    "Incandescente": {"d100": "59-62", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra fogo", "descricao": "RD Fogo 10; ação de movimento e 2 PM: causa 1d6 fogo em adjacentes no início de cada turno pela cena."},
    "Invulnerável": {"d100": "63-68", "conta_como": 1, "apenas_escudo": False, "efeito": "Redução de dano", "descricao": "RD 2 (escudos) ou RD 5 (armaduras)."},
    "Opaco": {"d100": "69-72", "conta_como": 1, "apenas_escudo": False, "efeito": "Redução de energia", "descricao": "RD Ácido, Eletricidade, Fogo e Frio 10."},
    "Protetor": {"d100": "73-78", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência +2", "descricao": "+2 em testes de resistência."},
    "Refletor": {"d100": "79-80", "conta_como": 1, "apenas_escudo": False, "efeito": "Reflete magia", "descricao": "1/rodada, quando alvo de magia, gaste PM igual ao custo dela para refleti-la ao conjurador."},
    "Relampejante": {"d100": "81-84", "conta_como": 1, "apenas_escudo": False, "efeito": "Resistência contra eletricidade", "descricao": "RD Eletricidade 10; ação de movimento e 2 PM: atacantes corpo a corpo sofrem 2d6 eletricidade pela cena."},
    "Reluzente": {"d100": "85-86", "conta_como": 1, "apenas_escudo": False, "efeito": "Causa efeito de cegueira", "descricao": "Ação de movimento e 2 PM: inimigos em alcance curto ficam cegos por 1 rodada (Ref CD Car evita)."},
    "Sombrio": {"d100": "87-88", "conta_como": 1, "apenas_escudo": False, "efeito": "Bônus em Furtividade", "descricao": "+5 em Furtividade e ignora penalidade de armadura do item nessa perícia."},
    "Zeloso": {"d100": "89-90", "conta_como": 1, "apenas_escudo": False, "efeito": "Atrai ataques em aliados", "descricao": "1/rodada, se aliado adjacente for atacado, gaste 1 PM para se tornar o alvo."},
}

# Tabela 8-11: Armaduras & Escudos Específicos (T20 JdA p.340 — 13 itens, todos categoria Maior)
ARMADURAS_ESCUDOS_ESPECIFICOS = {
    "Cota élfica": {"d100": "01-10", "tipo": "Armadura", "preco": 30000, "categoria": "Maior", "descricao": "Cota de malha defensora de mitral; permite aplicar Destreza na Defesa como armadura leve."},
    "Couro de monstro": {"d100": "11-20", "tipo": "Armadura", "preco": 36000, "categoria": "Maior", "descricao": "Gibão de peles defensor; +2d6 dano ao usar Ataque Poderoso ou investida."},
    "Escudo do conjurador": {"d100": "21-25", "tipo": "Escudo", "preco": 45000, "categoria": "Maior", "descricao": "Escudo leve defensor; armazena uma magia em tira de couro que pode ser lida como pergaminho."},
    "Loriga do centurião": {"d100": "26-32", "tipo": "Armadura", "preco": 45000, "categoria": "Maior", "descricao": "Loriga segmentada defensora; sob Comandar ou liderança, ataques corpo a corpo causam +2d6 fogo."},
    "Manto da noite": {"d100": "33-42", "tipo": "Armadura", "preco": 45000, "categoria": "Maior", "descricao": "Couro batido ajustado defensor sombrio; sem penalidade em Furtividade ao se mover normalmente e –10 por atacar."},
    "Couraça do comando": {"d100": "43-49", "tipo": "Armadura", "preco": 45000, "categoria": "Maior", "descricao": "Couraça banhada a ouro sob medida defensora; +1 Carisma e Comandar dá +2."},
    "Baluarte anão": {"d100": "50-59", "tipo": "Armadura", "preco": 50000, "categoria": "Maior", "descricao": "Armadura completa reforçada defensora de adamante; se não se deslocar no turno, RD sobe para 10."},
    "Escudo espinhoso": {"d100": "60-66", "tipo": "Escudo", "preco": 50000, "categoria": "Maior", "descricao": "Escudo pesado defensor; ação de movimento e 2 PM dispara espinho (acerto automático, 1d10+2 perfuração, alcance curto)."},
    "Escudo do leão": {"d100": "67-76", "tipo": "Escudo", "preco": 50000, "categoria": "Maior", "descricao": "Escudo pesado defensor; 1/rodada e 2 PM morde criatura adjacente (acerto automático, 2d6+2 perfuração)."},
    "Carapaça demoníaca": {"d100": "77-83", "tipo": "Armadura", "preco": 63000, "categoria": "Maior", "descricao": "Armadura completa macabra reforçada guardiã; devoto de energia negativa causa +1d8 dano de trevas corpo a corpo."},
    "Escudo do eclipse": {"d100": "84-88", "tipo": "Escudo", "preco": 70000, "categoria": "Maior", "descricao": "Escudo pesado defensor; RD Trevas 10, +1d8 trevas num ataque e ação de movimento + 2 PM lança Escuridão."},
    "Escudo de Azgher": {"d100": "89-93", "tipo": "Escudo", "preco": 140000, "categoria": "Maior", "descricao": "Escudo pesado guardião; 10 PM emite cone de luz curto com Visão da Verdade e 6d6 fogo (6d8 contra mortos-vivos/vulneráveis; 1 PM/turno manter)."},
    "Armadura da luz": {"d100": "94-100", "tipo": "Armadura", "preco": 150000, "categoria": "Maior", "descricao": "Armadura completa banhada a ouro reforçada guardiã zelosa; código de conduta ou devoto de energia positiva dá RD igual ao Carisma."},
}

# Tabela 8-12: Poções (T20 JdA p.341 — 38 entradas)
POCOES_MAGICAS = [
    {"d100": "01", "nome": "Abençoar Alimentos (óleo)", "preco": 30, "espacos": 0.5},
    {"d100": "02-03", "nome": "Área Escorregadia (granada)", "preco": 30, "espacos": 0.5},
    {"d100": "04-06", "nome": "Arma Mágica (óleo)", "preco": 30, "espacos": 0.5},
    {"d100": "07", "nome": "Compreensão", "preco": 30, "espacos": 0.5},
    {"d100": "08-15", "nome": "Curar Ferimentos (2d8+2 PV)", "preco": 30, "espacos": 0.5},
    {"d100": "16-18", "nome": "Disfarce Ilusório", "preco": 30, "espacos": 0.5},
    {"d100": "19-20", "nome": "Escuridão (óleo)", "preco": 30, "espacos": 0.5},
    {"d100": "21-22", "nome": "Luz (óleo)", "preco": 30, "espacos": 0.5},
    {"d100": "23-24", "nome": "Névoa (granada)", "preco": 30, "espacos": 0.5},
    {"d100": "25-26", "nome": "Primor Atlético", "preco": 30, "espacos": 0.5},
    {"d100": "27-28", "nome": "Proteção Divina", "preco": 30, "espacos": 0.5},
    {"d100": "29-30", "nome": "Resistência a Energia", "preco": 30, "espacos": 0.5},
    {"d100": "31-32", "nome": "Sono", "preco": 30, "espacos": 0.5},
    {"d100": "33", "nome": "Suporte Ambiental", "preco": 30, "espacos": 0.5},
    {"d100": "34", "nome": "Tranca Arcana (óleo)", "preco": 30, "espacos": 0.5},
    {"d100": "35", "nome": "Visão Mística", "preco": 30, "espacos": 0.5},
    {"d100": "36", "nome": "Vitalidade Fantasma", "preco": 30, "espacos": 0.5},
    {"d100": "37-38", "nome": "Escudo da Fé (duração cena)", "preco": 120, "espacos": 0.5},
    {"d100": "39-40", "nome": "Alterar Tamanho", "preco": 270, "espacos": 0.5},
    {"d100": "41-42", "nome": "Aparência Perfeita", "preco": 270, "espacos": 0.5},
    {"d100": "43", "nome": "Armamento da Natureza (óleo)", "preco": 270, "espacos": 0.5},
    {"d100": "44-49", "nome": "Bola de Fogo (granada)", "preco": 270, "espacos": 0.5},
    {"d100": "50-51", "nome": "Camuflagem Ilusória", "preco": 270, "espacos": 0.5},
    {"d100": "52-53", "nome": "Concentração de Combate (duração cena)", "preco": 270, "espacos": 0.5},
    {"d100": "54-62", "nome": "Curar Ferimentos (4d8+4 PV)", "preco": 270, "espacos": 0.5},
    {"d100": "63-66", "nome": "Físico Divino", "preco": 270, "espacos": 0.5},
    {"d100": "67-68", "nome": "Mente Divina", "preco": 270, "espacos": 0.5},
    {"d100": "69-70", "nome": "Metamorfose", "preco": 270, "espacos": 0.5},
    {"d100": "71-75", "nome": "Purificação", "preco": 270, "espacos": 0.5},
    {"d100": "76-77", "nome": "Velocidade", "preco": 270, "espacos": 0.5},
    {"d100": "78-79", "nome": "Vestimenta da Fé (óleo)", "preco": 270, "espacos": 0.5},
    {"d100": "80", "nome": "Voz Divina", "preco": 270, "espacos": 0.5},
    {"d100": "81-82", "nome": "Arma Mágica (óleo; bônus +3)", "preco": 750, "espacos": 0.5},
    {"d100": "83-88", "nome": "Curar Ferimentos (7d8+7 PV)", "preco": 1080, "espacos": 0.5},
    {"d100": "89", "nome": "Físico Divino (três atributos)", "preco": 1080, "espacos": 0.5},
    {"d100": "90-92", "nome": "Invisibilidade (duração cena)", "preco": 1080, "espacos": 0.5},
    {"d100": "93-96", "nome": "Bola de Fogo (granada; 10d6 dano)", "preco": 1470, "espacos": 0.5},
    {"d100": "97-100", "nome": "Curar Ferimentos (11d8+11 PV)", "preco": 3000, "espacos": 0.5},
]

# Tabelas 8-13, 8-14 e 8-15: Acessórios Mágicos (T20 JdA p.342–345 — 64 itens)
ACESSORIOS_MAGICOS = {
    # ── Menores (21) ──
    "Anel do sustento": {"categoria": "Menor", "d100": "01-02", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Não precisa comer/beber e dorme apenas 2h/noite (após 1 semana de uso)."},
    "Bainha mágica": {"categoria": "Menor", "d100": "03-07", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Lança Arma Mágica em qualquer arma corpo a corpo na bainha sem pagar PM."},
    "Corda da escalada": {"categoria": "Menor", "d100": "08-12", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Corda de 15m (suporta 6 criaturas Médias / 120 espaços) que se move e se fixa por comando."},
    "Ferraduras da velocidade": {"categoria": "Menor", "d100": "13-14", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Aumenta o deslocamento de uma montaria em +3m."},
    "Garrafa da fumaça eterna": {"categoria": "Menor", "d100": "15-19", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Abrir a tampa lança Névoa sem pagar PM até ser tampada."},
    "Gema da luminosidade": {"categoria": "Menor", "d100": "20-24", "preco": 3000, "espacos": 1, "efeitos": {}, "descricao": "Emite luz como tocha ou raio brilhante que cega 1 alvo em alcance curto por 1d4 rodadas (Fort CD Car evita)."},
    "Manto élfico": {"categoria": "Menor", "d100": "25-29", "preco": 3000, "espacos": 1, "efeitos": {"bonus_pericia": {"Furtividade": 5}}, "descricao": "+5 em Furtividade quando usado com o capuz cobrindo o rosto."},
    "Mochila de carga": {"categoria": "Menor", "d100": "30-34", "preco": 3000, "espacos": 0, "efeitos": {"bonus_carga": 10}, "descricao": "Aumenta capacidade de carga em +10 espaços (ela própria ocupa 0 espaços)."},
    "Brincos da sagacidade": {"categoria": "Menor", "d100": "35-40", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"inteligencia": 1}}, "descricao": "+1 em Inteligência (após 1 dia de uso)."},
    "Luvas da delicadeza": {"categoria": "Menor", "d100": "41-46", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"destreza": 1}}, "descricao": "+1 em Destreza (após 1 dia de uso)."},
    "Manoplas da força do ogro": {"categoria": "Menor", "d100": "47-52", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"forca": 1}}, "descricao": "+1 em Força (após 1 dia de uso)."},
    "Manto da resistência": {"categoria": "Menor", "d100": "53-59", "preco": 4500, "espacos": 1, "efeitos": {"bonus_resistencias": 2}, "descricao": "+2 em testes de resistência."},
    "Manto do fascínio": {"categoria": "Menor", "d100": "60-65", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"carisma": 1}}, "descricao": "+1 em Carisma (após 1 dia de uso)."},
    "Pingente da sensatez": {"categoria": "Menor", "d100": "66-71", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"sabedoria": 1}}, "descricao": "+1 em Sabedoria (após 1 dia de uso)."},
    "Torque do vigor": {"categoria": "Menor", "d100": "72-77", "preco": 4500, "espacos": 1, "efeitos": {"bonus_atributo": {"constituicao": 1}}, "descricao": "+1 em Constituição (após 1 dia de uso)."},
    "Chapéu do disfarce": {"categoria": "Menor", "d100": "78-82", "preco": 6000, "espacos": 1, "efeitos": {}, "descricao": "Lança Disfarce Ilusório (CD Car, +20 Enganação com odores/sensações) sem pagar PM."},
    "Flauta fantasma": {"categoria": "Menor", "d100": "83-84", "preco": 6000, "espacos": 1, "efeitos": {}, "descricao": "Se treinado em Atuação, lança Esculpir Sons (CD Car) sem pagar PM."},
    "Lanterna da revelação": {"categoria": "Menor", "d100": "85-89", "preco": 6000, "espacos": 1, "efeitos": {}, "descricao": "Lampião cuja luz revela criaturas e objetos invisíveis no alcance."},
    "Anel da proteção": {"categoria": "Menor", "d100": "90-96", "preco": 9000, "espacos": 1, "efeitos": {"bonus_defesa": 2}, "descricao": "+2 na Defesa."},
    "Anel do escudo mental": {"categoria": "Menor", "d100": "97-98", "preco": 9000, "espacos": 1, "efeitos": {}, "descricao": "Imunidade a magias de adivinhação."},
    "Pingente da saúde": {"categoria": "Menor", "d100": "99-100", "preco": 9000, "espacos": 1, "efeitos": {}, "descricao": "Imunidade a doenças e venenos (após 1 semana de uso)."},

    # ── Médios (22) ──
    "Anel de telecinesia": {"categoria": "Médio", "d100": "01-04", "preco": 10500, "espacos": 1, "efeitos": {}, "descricao": "Permite lançar Telecinesia (CD Int; –1 PM se já conhecer)."},
    "Bola de cristal": {"categoria": "Médio", "d100": "05-08", "preco": 10500, "espacos": 1, "efeitos": {}, "descricao": "Ação completa: gera a magia Vidência (CD Sab)."},
    "Caveira maldita": {"categoria": "Médio", "d100": "09-10", "preco": 10500, "espacos": 1, "efeitos": {}, "descricao": "Gera Profanar; mortos-vivos e devotos de energia negativa na área recebem +2 em testes e Defesa."},
    "Botas aladas": {"categoria": "Médio", "d100": "11-14", "preco": 15000, "espacos": 1, "efeitos": {}, "descricao": "2 PM: deslocamento de voo 12m por 1 rodada (1 PM/turno para manter)."},
    "Braceletes de bronze": {"categoria": "Médio", "d100": "15-18", "preco": 16500, "espacos": 1, "efeitos": {"bonus_defesa_sem_armadura": 4}, "descricao": "+4 na Defesa (cumulativo com outros itens mágicos, mas não com armaduras)."},
    "Anel da energia": {"categoria": "Médio", "d100": "19-24", "preco": 21000, "espacos": 1, "efeitos": {"bonus_pm": 5}, "descricao": "+5 PM (após 1 dia de uso)."},
    "Anel da vitalidade": {"categoria": "Médio", "d100": "25-30", "preco": 21000, "espacos": 1, "efeitos": {"bonus_pv": 10}, "descricao": "+10 PV (após 1 dia de uso)."},
    "Anel de invisibilidade": {"categoria": "Médio", "d100": "31-34", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "Colocar o anel concede Invisibilidade até atacar ou lançar magia ofensiva."},
    "Braçadeiras do arqueiro": {"categoria": "Médio", "d100": "35-38", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "+2 em rolagens de dano com armas de ataque à distância (cumulativo com outros itens)."},
    "Brincos de Marah": {"categoria": "Médio", "d100": "39-42", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "1ª criatura que o atacar na cena faz Vontade (CD Car) ou perde a ação (cumula com Aparência Inofensiva)."},
    "Faixas do pugilista": {"categoria": "Médio", "d100": "43-46", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "+2 em ataques e dano com ataques desarmados (cumulativo com outros itens)."},
    "Manto da aranha": {"categoria": "Médio", "d100": "47-50", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "Escalada igual ao deslocamento, +5 contra venenos, imune a teias e lança Teia (CD Des; –1 PM se já conhecer)."},
    "Vassoura voadora": {"categoria": "Médio", "d100": "51-54", "preco": 21000, "espacos": 1, "efeitos": {}, "descricao": "Deslocamento de voo 12m por comando; carrega 2 pessoas (40 espaços)."},
    "Símbolo abençoado": {"categoria": "Médio", "d100": "55-58", "preco": 21000, "espacos": 1, "efeitos": {"bonus_resistencias_devoto": 1}, "descricao": "Conta como símbolo sagrado; –1 PM em magias divinas do devoto (cumulativo com Símbolo Sagrado Energizado)."},
    "Amuleto da robustez": {"categoria": "Médio", "d100": "59-64", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"constituicao": 2}}, "descricao": "+2 em Constituição (após 1 dia de uso)."},
    "Botas velozes": {"categoria": "Médio", "d100": "65-68", "preco": 25500, "espacos": 1, "efeitos": {"bonus_deslocamento": 3}, "descricao": "+3m de deslocamento e permite lançar Velocidade em si mesmo."},
    "Cinto da força do gigante": {"categoria": "Médio", "d100": "69-74", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"forca": 2}}, "descricao": "+2 em Força (após 1 dia de uso)."},
    "Coroa majestosa": {"categoria": "Médio", "d100": "75-80", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"carisma": 2}}, "descricao": "+2 em Carisma (após 1 dia de uso)."},
    "Estola da serenidade": {"categoria": "Médio", "d100": "81-86", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"sabedoria": 2}}, "descricao": "+2 em Sabedoria (após 1 dia de uso)."},
    "Manto do morcego": {"categoria": "Médio", "d100": "87-88", "preco": 25500, "espacos": 1, "efeitos": {"bonus_pericia": {"Furtividade": 5}}, "descricao": "+5 Furtividade, pendura no teto e ação padrão transforma em morcego à noite/escuro (Minúsculo, voo 12m, mordida 1d4)."},
    "Pulseiras da celeridade": {"categoria": "Médio", "d100": "89-94", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"destreza": 2}}, "descricao": "+2 em Destreza (após 1 dia de uso)."},
    "Tiara da sapiência": {"categoria": "Médio", "d100": "95-100", "preco": 25500, "espacos": 1, "efeitos": {"bonus_atributo": {"inteligencia": 2}}, "descricao": "+2 em Inteligência (após 1 dia de uso)."},

    # ── Maiores (21) ──
    "Elmo do teletransporte": {"categoria": "Maior", "d100": "01-02", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Lança Salto Dimensional e Teletransporte em si mesmo (–1 PM se já conhecer)."},
    "Gema da telepatia": {"categoria": "Maior", "d100": "03-04", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Lança Compreensão e Enfeitiçar (CD Car) sem pagar PM."},
    "Gema elemental": {"categoria": "Maior", "d100": "05-09", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Lança Conjurar Elemental sem pagar PM."},
    "Manual da saúde corporal": {"categoria": "Maior", "d100": "10-15", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Constituição em +1 permanentemente (uso único)."},
    "Manual do bom exercício": {"categoria": "Maior", "d100": "16-21", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Força em +1 permanentemente (uso único)."},
    "Manual dos movimentos precisos": {"categoria": "Maior", "d100": "22-27", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Destreza em +1 permanentemente (uso único)."},
    "Medalhão de Lena": {"categoria": "Maior", "d100": "28-34", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "1/dia, ao cair a 0 ou menos PV, cura 100 PV antes que você caia."},
    "Tomo da compreensão": {"categoria": "Maior", "d100": "35-40", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Sabedoria em +1 permanentemente (uso único)."},
    "Tomo da liderança e influência": {"categoria": "Maior", "d100": "41-46", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Carisma em +1 permanentemente (uso único)."},
    "Tomo dos grandes pensamentos": {"categoria": "Maior", "d100": "47-52", "preco": 30000, "espacos": 1, "efeitos": {}, "descricao": "Ler por 1 semana aumenta Inteligência em +1 permanentemente (uso único)."},
    "Anel refletor": {"categoria": "Maior", "d100": "53-57", "preco": 51000, "espacos": 1, "efeitos": {}, "descricao": "1/rodada, quando alvo de magia, gaste PM igual ao custo para refleti-la ao conjurador."},
    "Cinto do campeão": {"categoria": "Maior", "d100": "58-60", "preco": 51000, "espacos": 1, "efeitos": {"bonus_atributo": {"forca": 1}}, "descricao": "+1 Força, Briga (+4 níveis de lutador se já possuir, máx 2d12) e Torcida dá +3 (após 1 dia de uso)."},
    "Colar guardião": {"categoria": "Maior", "d100": "61-67", "preco": 51000, "espacos": 1, "efeitos": {"bonus_defesa": 5}, "descricao": "+5 na Defesa."},
    "Estatueta animista": {"categoria": "Maior", "d100": "68-72", "preco": 51000, "espacos": 1, "efeitos": {}, "descricao": "Invoca parceiro animal veterano pela cena (raposa/ajudante, onça/assassino, águia/atirador, lobo/combatente, leão/fortão ou urso/guardião)."},
    "Anel da liberdade": {"categoria": "Maior", "d100": "73-77", "preco": 60000, "espacos": 1, "efeitos": {}, "descricao": "Permanentemente sob efeito de Libertação."},
    "Tapete voador": {"categoria": "Maior", "d100": "78-82", "preco": 60000, "espacos": 1, "efeitos": {}, "descricao": "Deslocamento de voo 12m por comando; 3m×3m, carrega 6 criaturas Médias (120 espaços)."},
    "Braceletes de ouro": {"categoria": "Maior", "d100": "83-87", "preco": 64500, "espacos": 1, "efeitos": {"bonus_defesa_sem_armadura": 8}, "descricao": "+8 na Defesa (não cumulativo com armaduras nem braceletes de bronze)."},
    "Espelho da oposição": {"categoria": "Maior", "d100": "88-89", "preco": 75000, "espacos": 1, "efeitos": {}, "descricao": "Cria cópia hostil de quem observar seu reflexo."},
    "Robe do arquimago": {"categoria": "Maior", "d100": "90-94", "preco": 90000, "espacos": 1, "efeitos": {"robe_arquimago": True}, "descricao": "Para conjurador arcano: Defesa +(5 + círculo máximo) e resistências +(metade do bônus na Defesa)."},
    "Orbe das tempestades": {"categoria": "Maior", "d100": "95-96", "preco": 97500, "espacos": 1, "efeitos": {}, "descricao": "Lança Controlar o Clima e Fúria do Panteão (CD Sab; –1 PM se já conhecer) e Suporte Ambiental a si e aliados adjacentes."},
    "Anel da regeneração": {"categoria": "Maior", "d100": "97-98", "preco": 150000, "espacos": 1, "efeitos": {}, "descricao": "Cura Acelerada 5 (após 1 dia de uso)."},
    "Espelho do aprisionamento": {"categoria": "Maior", "d100": "99-100", "preco": 150000, "espacos": 1, "efeitos": {}, "descricao": "Criatura em alcance curto que veja o reflexo faz Reflexos (CD Int) ou fica presa em espaço extradimensional."},
}

# Tabela do Baralho do Caos (T20 JdA p.347 — 22 cartas)
BARALHO_DO_CAOS_CARTAS = [
    {"d100": "01-05", "carta": "Abismo", "efeito": "Receba redução de dano 10 a um tipo aleatório."},
    {"d100": "06-09", "carta": "Amigo", "efeito": "Um de seus parceiros racionais o trai em até 1 ano."},
    {"d100": "10-14", "carta": "Anel", "efeito": "+5 pontos de mana permanentemente."},
    {"d100": "15-19", "carta": "Árvore", "efeito": "+10 pontos de vida permanentemente."},
    {"d100": "20-24", "carta": "Coração", "efeito": "+1 em um atributo a sua escolha permanentemente."},
    {"d100": "25-28", "carta": "Crânio", "efeito": "Enfrente cópia sombria imune a ataques de terceiros."},
    {"d100": "29-33", "carta": "Donzela", "efeito": "Derrote um monstro (ND = nível – 1) sozinho e suba de nível."},
    {"d100": "34-38", "carta": "Fogo", "efeito": "Ressuscite com PV e PM totais quando morrer."},
    {"d100": "39-43", "carta": "Gema", "efeito": "Role 10 vezes na coluna Maior da Tabela 8-2: Riquezas."},
    {"d100": "44-48", "carta": "Lua", "efeito": "Receba 1d4 Desejos até o fim da cena."},
    {"d100": "49-52", "carta": "Martelo", "efeito": "Perca todos os itens mágicos que estiverem com você."},
    {"d100": "53-56", "carta": "Noite", "efeito": "–1 em todos os testes de resistência (ou arma mágica maior para devoto de Tenebra/morto-vivo)."},
    {"d100": "57-60", "carta": "Presas", "efeito": "Perca todo o dinheiro e itens mundanos."},
    {"d100": "61-65", "carta": "Servo", "efeito": "Receba os serviços de um espírito (parceiro veterano)."},
    {"d100": "66-70", "carta": "Sol", "efeito": "Receba uma arma mágica maior (ou –1 resistências para devoto de Tenebra/morto-vivo)."},
    {"d100": "71-75", "carta": "Tentáculo", "efeito": "–1 em um atributo aleatório (1d6) permanentemente."},
    {"d100": "76-80", "carta": "Tolo", "efeito": "Perca 10.000 XP (mín. 0) e saque outra carta."},
    {"d100": "81-85", "carta": "Trono", "efeito": "+2 em Diplomacia permanentemente e recebe feudo (Título)."},
    {"d100": "86-90", "carta": "Vizir", "efeito": "Receba a resposta verdadeira para uma pergunta em até 1 ano."},
    {"d100": "91-94", "carta": "Nada", "efeito": "Anule qualquer ataque/efeito e receba imunidade a tudo por 1 rodada (usar em até 1 ano)."},
    {"d100": "95-98", "carta": "Vazio", "efeito": "Sua alma deixa seu corpo (coma entre os Planos)."},
    {"d100": "99-100", "carta": "Curinga", "efeito": "Ganhe 10.000 XP ou saque mais duas cartas."},
]

# Artefatos (T20 JdA p.346–348 — 4 artefatos)
ARTEFATOS = {
    "A Espada-Deus": {
        "tipo": "Artefato",
        "descricao": "Espada longa atroz precisa pungente ameaçadora magnífica veloz (dano básico 2d12), indestrutível; ignora RD e acerta críticos mesmo em imunes. Exige 15+ níveis em classes com Luta inicial.",
    },
    "A Joia da Alma": {
        "tipo": "Artefato",
        "descricao": "Gema indestrutível de 20 faces; +3 Inteligência (após 1 dia) e magos lançam magias arcanas por 0 PM (aprimoramentos ainda pagos). Exige Vontade CD 25 (+1/dia) para não enlouquecer.",
    },
    "O Baralho do Caos": {
        "tipo": "Artefato",
        "descricao": "+10 em Jogatina (ou –10 se abusar da sorte). Dizer 'Eu aposto tudo' permite sacar 1 a 4 cartas da tabela de 22 cartas (Jogatina CD 30 ignora 1 carta).",
        "cartas": BARALHO_DO_CAOS_CARTAS,
    },
    "O Olho de Sszzaas": {
        "tipo": "Artefato",
        "descricao": "Cajado com gema; lança qualquer magia conhecida ou ouvida falar por 0 PM (aprimoramentos pagos), exigindo Misticismo CD 20 + custo em PM (falha entrega controle a Sszzaas). Conhecimento CD 30 reconhece.",
    },
}
