# -*- coding: utf-8 -*-
"""Novas Magias Arcanas e Universais — Heróis de Arton (Cap. 3, p. 252–255)."""
from .dados_suplementos import FONTE_HEROIS

_F = FONTE_HEROIS

DADOS_MAGIAS_HEROIS = {
    "Armadura Elemental": {
        "nome": "Armadura Elemental",
        "fonte": _F,
        "circulo": 1,
        "escola": "Evocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Escolha um tipo de energia entre ácido, eletricidade, fogo ou frio. "
            "Uma aura faiscante dessa energia emana de seu corpo — sempre que uma criatura adjacente "
            "acertar um ataque corpo a corpo em você, ela sofre 2d6 pontos de dano do tipo escolhido."
        ),
        "rolagem": {"formula": "2d6", "tipo": "dano", "tipo_dano": "elemental"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda o alcance para toque e o alvo para 1 criatura. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o dano em +1d6 (total de dados limitado pelo círculo máximo de magia que você pode lançar). Requer 3º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Muda a energia para essência. Requer 2º círculo.", "efeitos": {}},
        ],
    },
    "Assobio Perigoso": {
        "nome": "Assobio Perigoso",
        "fonte": _F,
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Efeito: grupo de criaturas conjuradas",
        "duracao": "Especial",
        "resistencia": "Nenhuma",
        "descricao": (
            "Conjura um grupo de criaturas agressivas feitas de energia (encontro de ND igual ao nível do conjurador) "
            "em alcance curto que agem imediatamente após seu turno, atacando quem estiver por perto (inclusive você e aliados) "
            "até a morte ou por 1 minuto. Componente Material: miniaturas em metal de criaturas (T$ 25 por nível do conjurador)."
        ),
        "efeitos": {},
        "aprimoramentos": [],
    },
    "Aura de Morte": {
        "nome": "Aura de Morte",
        "fonte": _F,
        "circulo": 2,
        "escola": "Necromancia",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Esfera com 6m de raio",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Uma aura de frio necrótico emana a partir do seu corpo. Quando lança a magia, e no início de cada um "
            "dos seus turnos, você perde 1d6 pontos de vida e cada outra criatura na área perde 2d8 pontos de vida."
        ),
        "rolagem": {"formula": "2d8", "tipo": "dano", "tipo_dano": "trevas"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta a perda de vida para outras criaturas em +1d8 (máximo de dados limitado pelo círculo máximo de magia). Requer 3º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Adiciona resistência (Fortitude parcial): outras criaturas que percam PV e falhem não podem recuperar PV por 1 rodada. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Conjurar Armadilha": {
        "nome": "Conjurar Armadilha",
        "fonte": _F,
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Completa",
        "alcance": "Curto",
        "alvo_area": "Efeito: 1 armadilha conjurada",
        "duracao": "Permanente",
        "resistencia": "Especial",
        "descricao": (
            "Modifica o terreno/arquitetura em um ponto no alcance, transformando-o em uma armadilha de caçador "
            "à sua escolha (CD para encontrar e resistir igual à CD da magia). Após ativada, torna-se inerte."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Seus poderes que afetam armadilhas também afetam a armadilha criada pela magia.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "(Apenas Armadilheiros Mestres e Caçadores) Reduz a execução para movimento.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "Quando lança a magia, pode escolher qualquer número de criaturas no alcance para não serem afetadas pela armadilha. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "(Apenas Armadilheiros Mestres) Em vez do normal, pode conjurar uma das suas armadilhas de armadilheiro mestre.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda a execução para padrão; pode ser conjurada diretamente na área de uma criatura, acionando-a imediatamente. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Coração Imortal": {
        "nome": "Coração Imortal",
        "fonte": _F,
        "circulo": 3,
        "escola": "Necromancia",
        "tipo": "Universal",
        "custo_pm": 6,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Concentra sua força vital em uma parte específica do corpo: você recebe fortificação 100% e imunidade a sangramento."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda a duração para 1 dia.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta a cura do aprimoramento de 0 PV em +10 PV.", "efeitos": {}},
            {"custo": "+4 PM", "descricao": "Adiciona componente material (coração de pedra de T$ 100): quando reduzido a 0 PV ou menos, cura 30 PV e a magia se encerra (1×/dia).", "efeitos": {}},
        ],
    },
    "Desafio Corajoso": {
        "nome": "Desafio Corajoso",
        "fonte": _F,
        "circulo": 2,
        "escola": "Encantamento",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 criatura voluntária",
        "duracao": "Sustentada",
        "resistencia": "Vontade anula",
        "descricao": (
            "Cria uma aura de influência de 9m ao redor do alvo. Outras criaturas que iniciarem seus turnos na aura "
            "devem passar em Vontade ou quaisquer ações hostis nesse turno devem ser feitas contra o alvo."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+3 PM", "descricao": "Muda o alvo para 1 criatura ou objeto. Requer 4º círculo.", "efeitos": {}},
        ],
    },
    "Descobrir Fraqueza": {
        "nome": "Descobrir Fraqueza",
        "fonte": _F,
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Movimento",
        "alcance": "Curto",
        "alvo_area": "1 criatura",
        "duracao": "Instantânea",
        "resistencia": "Vontade evita",
        "descricao": (
            "Analisa a criatura em busca de pontos fracos: como parte da magia, faz um teste de Misticismo para "
            "identificar criatura (independente do tipo) com bônus de +10."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Aumenta o bônus no teste em +5.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Sua próxima rolagem de dano contra a criatura nessa cena ignora 10 pontos de RD dela. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Você recebe +2 em testes contra a criatura até o fim da cena. Requer 2º círculo.", "efeitos": {}},
        ],
    },
    "Desfazer Engenhoca": {
        "nome": "Desfazer Engenhoca",
        "fonte": _F,
        "circulo": 2,
        "escola": "Abjuração",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Médio",
        "alvo_area": "Esfera com 3m de raio ou 1 criatura ou engenhoca",
        "duracao": "Instantânea",
        "resistencia": "Especial",
        "descricao": (
            "Dissipa efeitos ativos de engenhocas com teste de Misticismo (CD igual à CD da engenhoca). "
            "Diretamente contra engenhoca: +10 na CD para ativá-la pela cena. Contra construto: teste oposto à Vontade; "
            "se vencer, o construto fica fraco e vulnerável (mesmo se imune)."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Recebe +5 em Misticismo para dissipar uma engenhoca por cada vez que a viu ser usada na cena.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Ignora qualquer efeito ativo gerado por engenhocas (ex.: Campo Antimagia).", "efeitos": {}},
            {"custo": "+12 PM", "descricao": "Área muda para esfera 9m: efeito de disjunção dissipa automaticamente todos os efeitos de engenhocas e faz engenhocas na área enguiçarem pela cena (Vontade evita para carregadas). Requer 5º círculo.", "efeitos": {}},
        ],
    },
    "Discrição": {
        "nome": "Discrição",
        "fonte": _F,
        "circulo": 1,
        "escola": "Encantamento",
        "tipo": "Universal",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal ou toque",
        "alvo_area": "Você ou 1 objeto",
        "duracao": "Cena",
        "resistencia": "Vontade anula",
        "descricao": (
            "Torna a aparência do alvo desinteressante: testes de Investigação e Percepção contra o alvo sofrem –10. "
            "Em combate, inimigos que iniciem o turno a até 9m devem passar em Vontade ou suas ações hostis ignoram o alvo. "
            "Dissipa se causar dano."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Muda o alvo para 1 criatura. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta a penalidade em testes para –15. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "O alvo não pode ser detectado por magias de adivinhação. Requer 4º círculo.", "efeitos": {}},
        ],
    },
    "Distração Fugaz": {
        "nome": "Distração Fugaz",
        "fonte": _F,
        "circulo": 1,
        "escola": "Ilusão",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 humanoide",
        "duracao": "Instantânea",
        "resistencia": "Vontade anula",
        "descricao": (
            "Produz uma breve ilusão de algo de grande interesse pessoal do alvo. Se falhar em Vontade, o alvo fica desprevenido por 1 rodada."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Se falhar em Vontade, sofre –5 em Diplomacia e Intimidação pela cena.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "Muda o alvo para 1 criatura. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Em vez de desprevenido, fica atordoado (1×/cena).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Afeta todos os alvos válidos à escolha no alcance. Requer 2º círculo.", "efeitos": {}},
        ],
    },
    "Emular Magia": {
        "nome": "Emular Magia",
        "fonte": _F,
        "circulo": 2,
        "escola": "Evocação",
        "tipo": "Universal",
        "custo_pm": 3,
        "execucao": "Movimento",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Pela duração, você pode lançar uma única magia que tenha visto ser lançada em alcance curto desde sua última rodada "
            "(do seu tipo e de um círculo a que tenha acesso)."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "A magia emulada pode ser de qualquer tipo, arcana ou divina.", "efeitos": {}},
        ],
    },
    "Espírito Balístico": {
        "nome": "Espírito Balístico",
        "fonte": _F,
        "circulo": 1,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "Efeito: 1 criatura conjurada",
        "duracao": "Sustentada",
        "resistencia": "Nenhuma",
        "descricao": (
            "Invoca um espírito fixo de energia (Defesa igual à sua, 20 PV, imune a Fortitude/Vontade, falha automática em Reflexos). "
            "No início dos seus turnos, dispara um projétil mágico no inimigo mais próximo em alcance médio causando 1d6+1 de perfuração."
        ),
        "rolagem": {"formula": "1d6+1", "tipo": "dano", "tipo_dano": "perfuração"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o dano em +1 dado (limitado pelo círculo máximo de magia).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda o número de espíritos para dois. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+3 PM", "descricao": "(Golem energia elemental, Qareen ou Kallyanach) Muda o dado de dano para d8 e o tipo para o elemento racial.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda o número de espíritos para três. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Farejar Fortuna": {
        "nome": "Farejar Fortuna",
        "fonte": _F,
        "circulo": 1,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Descobre se existe algum tesouro não carregado/vestido por criatura inteligente em alcance longo (sem revelar localização ou valor exato)."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Alcance toque, alvo 1 item recém-encontrado, duração instantânea: +5 em testes para identificar o item.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Recebe +5 em testes de perícia para localizar o tesouro.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Ao rolar qualquer dado para definir um tesouro, rola dois dados e escolhe qual resultado usar.", "efeitos": {}},
        ],
    },
    "Maaais Klunc": {
        "nome": "Maaais Klunc",
        "fonte": _F,
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Você recebe +10 em Força, mas sua Inteligência cai para o valor –3 (penalidades aplicadas depois). "
            "Não pode lançar magias nem encerrar esta magia voluntariamente."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura voluntária. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda alcance para curto e alvo para 1 criatura involuntária (Vontade evita). Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Máquina de Combate": {
        "nome": "Máquina de Combate",
        "fonte": _F,
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 construto",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Sobrecarrega a fonte de energia de um construto: recebe +5 em Atletismo e Luta, mas perde 1d4 PV "
            "no fim de cada turno em que executar uma ação padrão."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Ataques corpo a corpo do alvo causam +1d6 de dano.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "O alvo recebe +2 na Defesa.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus na Defesa em +1.", "efeitos": {}},
        ],
    },
    "Ossos de Adamante": {
        "nome": "Ossos de Adamante",
        "fonte": _F,
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Recebe redução de impacto 5 e fortificação 25%, mas não pode mudar de forma; se sofrer metamorfose, "
            "perde 1d6 PV/PM gasto e fica lento. Não afeta construtos."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda redução de impacto para RD 5 e fortificação para 50%. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura viva.", "efeitos": {}},
        ],
    },
    "Piscar": {
        "nome": "Piscar",
        "fonte": _F,
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Você pisca entre o Plano Material e o Etéreo: ataques e habilidades de outras criaturas têm 50% de chance de falhar; "
            "você recebe +2 em ataques, mas seus próprios ataques e habilidades têm 25% de chance de falhar. Pode interagir com criaturas etéreas."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura voluntária. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Poção Explosiva": {
        "nome": "Poção Explosiva",
        "fonte": _F,
        "circulo": 2,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "1 poção",
        "duracao": "Cena",
        "resistencia": "Reflexos evita (se carregada)",
        "descricao": (
            "Torna uma poção explosiva: quando usada, em vez do efeito normal causa 2d6 de essência por círculo da magia contida "
            "(se ingerida, dano máximo sem resistência). Identificar exige Misticismo ou Ofício (alquimista) CD 25."
        ),
        "rolagem": {"formula": "2d6", "tipo": "dano", "tipo_dano": "essência"},
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+5 PM", "descricao": "Define uma palavra-chave que, pronunciada em alcance curto, faz a poção explodir. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+7 PM", "descricao": "Alcance pessoal, esfera 9m: afeta até poções carregadas na área. Requer 4º círculo.", "efeitos": {}},
        ],
    },
    "Punho de Mitral": {
        "nome": "Punho de Mitral",
        "fonte": _F,
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Transforma uma mão em mitral: se livre, +1 em ataques e margem de ameaça com ataques desarmados (dano letal ou não letal) "
            "e pode manipular venenos sem risco de se envenenar."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Muda o bônus em ataque e margem de ameaça para +2.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Muda alcance para toque e alvo para 1 criatura. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Arma ou item esotérico empunhado nessa mão recebe os benefícios de mitral (mesmo já tendo outro material especial). Requer 2º círculo.", "efeitos": {}},
        ],
    },
    "Toque do Horizonte": {
        "nome": "Toque do Horizonte",
        "fonte": _F,
        "circulo": 1,
        "escola": "Transmutação",
        "tipo": "Arcana",
        "custo_pm": 1,
        "execucao": "Padrão",
        "alcance": "Toque",
        "alvo_area": "1 arma de ataque à distância",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Aumenta o alcance da arma em 1 passo (curto→médio→longo; se já longo, dobra). Conta como bônus de encanto."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+1 PM", "descricao": "Ignora camuflagem leve e penalidades por cobertura leve.", "efeitos": {}},
            {"custo": "+1 PM", "descricao": "A arma fornece +1 em ataques e dano dentro do alcance original.", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "Aumenta o bônus de ataque e dano acima em +1 (máximo limitado pelo círculo máximo de magia).", "efeitos": {}},
            {"custo": "+2 PM", "descricao": "A margem de ameaça da arma aumenta em +1. Requer 2º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Alvo: 1 arma de arremesso; duração: sustentada. Recebe o benefício do encanto dançarina. Requer 3º círculo.", "efeitos": {}},
        ],
    },
    "Transposição": {
        "nome": "Transposição",
        "fonte": _F,
        "circulo": 2,
        "escola": "Convocação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Curto",
        "alvo_area": "2 criaturas voluntárias",
        "duracao": "Instantânea",
        "resistencia": "Nenhuma",
        "descricao": (
            "Teletransporta duas criaturas (incluindo equipamento), fazendo com que troquem de lugar imediatamente."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Aumenta o número de alvos em +2 (você escolhe quem troca com quem).", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "A troca não exige linha de efeito (ainda dentro do alcance). Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Muda o alvo para 2 criaturas do tipo lacaio e adiciona resistência (Vontade anula). Requer 4º círculo.", "efeitos": {}},
        ],
    },
    "Viagem Onírica": {
        "nome": "Viagem Onírica",
        "fonte": _F,
        "circulo": 2,
        "escola": "Adivinhação",
        "tipo": "Arcana",
        "custo_pm": 3,
        "execucao": "Padrão",
        "alcance": "Pessoal",
        "alvo_area": "Você",
        "duracao": "Cena",
        "resistencia": "Nenhuma",
        "descricao": (
            "Você adormece e abandona seu corpo como espírito incorpóreo translúcido com voo 18m (pode ver e ouvir, "
            "mas não falar, atacar, lançar magias ou interagir fisicamente). Sofre –10 em Percepção para ruídos perto do corpo; "
            "se o corpo for perturbado, a magia acaba."
        ),
        "efeitos": {},
        "aprimoramentos": [
            {"custo": "+2 PM", "descricao": "Você pode falar em sua forma incorpórea. Requer 3º círculo.", "efeitos": {}},
            {"custo": "+5 PM", "descricao": "Você pode lançar magias em sua forma incorpórea. Requer 4º círculo.", "efeitos": {}},
        ],
    },
}
