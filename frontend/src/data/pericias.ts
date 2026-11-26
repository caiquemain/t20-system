/**
 * Tabela 2-1: Perícias e Usos Oficiais (T20 Jogo do Ano p.114–123).
 * Alinhado 100% com app/src/dados_pericias.py e o Livro Básico.
 */

export interface UsoPericia {
  nome: string;
  acao?: string;
  cd?: string;
  apenas_treinado?: boolean;
  descricao: string;
}

export interface DadoPericia {
  atributo: 'for' | 'des' | 'con' | 'int' | 'sab' | 'car';
  treino_apenas: boolean;
  penalidade_armadura: boolean;
  resumo: string;
  nota?: string;
  usos: UsoPericia[];
}

export const DADOS_PERICIAS_FRONTEND: Record<string, DadoPericia> = {
  'Acrobacia': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: true,
    resumo: 'Proezas acrobáticas, equilíbrio, quedas e mobilidade.',
    usos: [
      {
        nome: 'Amortecer Queda',
        acao: 'Reação',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Reduz o dano de queda em 1d6 (+1d6 para cada 5 pontos acima da CD). Se reduzir a zero, cai de pé.',
      },
      {
        nome: 'Equilíbrio',
        acao: 'Movimento',
        cd: 'CD 10 / 15 / 20',
        descricao: 'Avança metade do deslocamento em piso escorregadio (10), estreito (15) ou corda (20). –5 para deslocamento total. Fica desprevenido; falhar por 5+ derruba.',
      },
      {
        nome: 'Escapar',
        acao: 'Completa',
        cd: 'CD Des+10 / 20 / 30',
        descricao: 'Escapa de amarras: cordas (teste Des de quem amarrou +10), redes (CD 20) ou algemas (CD 30).',
      },
      {
        nome: 'Levantar-se Rapidamente',
        acao: 'Livre (exige Mov.)',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Se passar, levanta-se como ação livre. Se falhar, gasta a ação de movimento e continua caído.',
      },
      {
        nome: 'Passar por Espaço Apertado',
        acao: 'Completa',
        cd: 'CD 25',
        apenas_treinado: true,
        descricao: 'Espreme-se por espaços suficientes para criaturas uma categoria menores, avançando metade do deslocamento.',
      },
      {
        nome: 'Passar por Inimigo',
        acao: 'Parte do movimento',
        cd: 'Oposto (Acrob./Inic./Luta)',
        descricao: 'Atravessa espaço ocupado por inimigo (conta como terreno difícil). Se falhar, o movimento termina.',
      },
    ],
  },
  'Adestramento': {
    atributo: 'car',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Lidar, acalmar e comandar animais.',
    usos: [
      {
        nome: 'Acalmar Animal',
        acao: 'Completa',
        cd: 'CD 25',
        apenas_treinado: true,
        descricao: 'Acalma um animal nervoso ou agressivo (como um cavalo assustado ou lobo hostil).',
      },
      {
        nome: 'Manejar Animal',
        acao: 'Movimento',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Faz um animal executar tarefa treinada (atacar, sentar, vigiar) ou conduz veículos de tração animal.',
      },
    ],
  },
  'Atletismo': {
    atributo: 'for',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Façanhas físicas de corrida, escalada, natação e saltos.',
    nota: 'Natação sofre penalidade de armadura.',
    usos: [
      {
        nome: 'Corrida',
        acao: 'Completa',
        cd: 'Resultado = quadrados',
        descricao: 'Avança quadrados de 1,5m igual ao resultado em linha reta (±2 por 1,5m de deslocamento acima/abaixo de 9m). Dura 1+Con rodadas antes de exigir Fortitude.',
      },
      {
        nome: 'Escalar',
        acao: 'Movimento',
        cd: 'CD 10 / 15 / 20 / 25',
        descricao: 'Avança metade do deslocamento (–5 para total). Apoios (10), árvore (15), muro com reentrâncias (20), muro liso (25). Fica desprevenido; falhar por 5+ cai.',
      },
      {
        nome: 'Natação',
        acao: 'Movimento',
        cd: 'CD 10 / 15 / 20+',
        descricao: 'Sofre penalidade de armadura. Calma (10), agitada (15), tempestuosa (20+). Passar avança metade; falhar por 5+ afunda (prende fôlego por 1+Con rodadas).',
      },
      {
        nome: 'Saltar',
        acao: 'Parte do movimento',
        cd: 'CD 5/1,5m (longo) • 15/1,5m (altura)',
        descricao: 'Exige 6m de impulso (sem impulso, CD +10). Salto longo: CD 5 por quadrado; salto em altura: CD 15 por quadrado.',
      },
    ],
  },
  'Atuação': {
    atributo: 'car',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Apresentações artísticas de música, dança e dramaturgia.',
    usos: [
      {
        nome: 'Apresentação',
        acao: '1 dia/noite',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Ganha T$ 1d6 (+1d6 para cada 5 pontos acima da CD). Metade em local inadequado; dobro em festival ou palácio.',
      },
      {
        nome: 'Impressionar',
        acao: 'Minutos a horas',
        cd: 'Oposto a Vontade',
        apenas_treinado: true,
        descricao: 'Passar dá +2 em perícias de Carisma contra o alvo no mesmo dia; falhar impõe –2 e impede nova tentativa no dia.',
      },
    ],
  },
  'Cavalgar': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Conduzir montarias em situações perigosas.',
    nota: 'Exige uma sela (sem ela, sofre –5 no teste).',
    usos: [
      {
        nome: 'Conduzir',
        acao: 'Parte do movimento',
        cd: 'CD 15 / 25',
        descricao: 'Terreno ruim ou obstáculos pequenos (CD 15); terreno perigoso ou obstáculos grandes (CD 25). Falhar derruba (1d6 dano).',
      },
      {
        nome: 'Galopar',
        acao: 'Completa',
        cd: 'Resultado = quadrados',
        descricao: 'Avança quadrados de 1,5m igual ao resultado (±2 por 1,5m de deslocamento acima/abaixo de 9m).',
      },
      {
        nome: 'Montar Rapidamente',
        acao: 'Livre',
        cd: 'CD 20',
        descricao: 'Monta ou desmonta como ação livre (em vez de movimento). Falhar por 5+ derruba no chão.',
      },
    ],
  },
  'Conhecimento': {
    atributo: 'int',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'História, geografia, astronomia, idiomas e saberes gerais.',
    usos: [
      {
        nome: 'Idiomas',
        acao: '—',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Entende idiomas desconhecidos (CD 20) ou exóticos/muito antigos (CD 30). Falhar por 5+ leva a conclusão falsa.',
      },
      {
        nome: 'Informação',
        acao: '—',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Dúvidas simples não exigem teste; complexas têm CD 20; mistérios e enigmas têm CD 30.',
      },
    ],
  },
  'Cura': {
    atributo: 'sab',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Tratar ferimentos, doenças, venenos e examinar cadáveres.',
    nota: 'Exige maleta de medicamentos (–5 sem). Usar em si mesmo impõe –5.',
    usos: [
      {
        nome: 'Primeiros Socorros',
        acao: 'Padrão',
        cd: 'CD 15',
        descricao: 'Estabiliza um personagem adjacente que esteja sangrando.',
      },
      {
        nome: 'Cuidados Prolongados',
        acao: '1 hora',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Aumenta a recuperação de PV do paciente em +1 por nível nesse dia (máximo de pacientes = seu nível).',
      },
      {
        nome: 'Necropsia',
        acao: '10 minutos',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Determina causa e momento aproximado da morte (CD 30 para venenos ou maldições raras).',
      },
      {
        nome: 'Tratamento',
        acao: 'Completa',
        cd: 'CD da doença/veneno',
        apenas_treinado: true,
        descricao: 'Se passar, o paciente recebe +5 no próximo teste de Fortitude contra a doença ou veneno contínuo.',
      },
    ],
  },
  'Diplomacia': {
    atributo: 'car',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Lábia, negociação e argumentação. Usos são efeitos mentais.',
    usos: [
      {
        nome: 'Barganha',
        acao: '—',
        cd: 'Oposto a Vontade',
        descricao: 'Muda o preço em 10% a seu favor (20% se passar por 10+). Falhar por 5+ ofende o negociante por 1 semana.',
      },
      {
        nome: 'Mudar Atitude',
        acao: '1 minuto (–10 Completa)',
        cd: 'Oposto a Vontade',
        descricao: 'Muda categoria de atitude do NPC em 1 passo (2 se passar por 10+). Falhar por 5+ piora 1 passo. 1x por dia por alvo.',
      },
      {
        nome: 'Persuasão',
        acao: '1 minuto+',
        cd: 'CD 20',
        descricao: 'Convence alguém a fazer algo (–5 se custoso, –10 ou falha automática se perigoso).',
      },
    ],
  },
  'Enganação': {
    atributo: 'car',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Blefar, disfarçar-se, falsificar documentos e fintar.',
    usos: [
      {
        nome: 'Disfarce',
        acao: '10 minutos',
        cd: 'Oposto a Percepção',
        descricao: 'Exige estojo de disfarces (–5 sem). Disfarce complexo –5; quem conhece o alvo recebe +10 em Percepção.',
      },
      {
        nome: 'Falsificação',
        acao: '—',
        cd: 'Oposto a Percepção',
        descricao: 'Falsifica documentos (–10 se muito complexo ou com selo/assinatura específica).',
      },
      {
        nome: 'Fintar',
        acao: 'Padrão',
        cd: 'Oposto a Reflexos',
        descricao: 'Alvo em alcance curto fica desprevenido contra seu próximo ataque até o fim do seu próximo turno.',
      },
      {
        nome: 'Insinuação',
        acao: '—',
        cd: 'CD 20',
        descricao: 'Transmite mensagem velada sem terceiros entenderem (terceiros podem fazer Intuição oposto).',
      },
      {
        nome: 'Intriga',
        acao: '1 dia+',
        cd: 'CD 20 / 30',
        descricao: 'Espalha fofoca (CD 30 se muito improvável). Falhar por 5+ revela que você é a fonte.',
      },
      {
        nome: 'Mentir',
        acao: '—',
        cd: 'Oposto a Intuição',
        descricao: 'Faz alguém acreditar numa mentira (–10 para mentiras muito implausíveis).',
      },
    ],
  },
  'Fortitude': {
    atributo: 'con',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Perícia de resistência para vitalidade, doenças, venenos e fôlego.',
    usos: [
      {
        nome: 'Resistir a Efeitos',
        acao: 'Reação',
        cd: 'CD do efeito',
        descricao: 'Resiste a venenos, doenças, fadiga e efeitos que testam vitalidade.',
      },
      {
        nome: 'Manter Fôlego',
        acao: '—',
        cd: 'CD 15 (+1/teste)',
        descricao: 'Mantém fôlego durante corrida prolongada ou submersão após 1+Con rodadas.',
      },
    ],
  },
  'Furtividade': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: true,
    resumo: 'Esconder-se nas sombras e seguir alvos sem ser notado.',
    usos: [
      {
        nome: 'Esconder-se',
        acao: 'Livre (fim do turno)',
        cd: 'Oposto a Percepção',
        descricao: 'Exige cobertura/esconderijo. Dá camuflagem total contra quem falhar. –5 se moveu (0 se metade do desl.); –20 se atacou.',
      },
      {
        nome: 'Seguir',
        acao: '—',
        cd: 'Oposto a Percepção',
        descricao: 'Segue alvo até o destino (–5 sem esconderijos; alvo atento recebe +5 em Percepção).',
      },
    ],
  },
  'Guerra': {
    atributo: 'int',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Tática, estratégia e logística militar.',
    usos: [
      {
        nome: 'Analisar Terreno',
        acao: 'Movimento',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Observa o campo de batalha e descobre uma vantagem (cobertura, camuflagem ou terreno elevado).',
      },
      {
        nome: 'Plano de Ação',
        acao: 'Padrão',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Orienta um aliado em alcance médio, fornecendo +5 na Iniciativa dele.',
      },
    ],
  },
  'Iniciativa': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Velocidade de reação para definir a ordem de ação em combate.',
    usos: [
      {
        nome: 'Ordem de Ação',
        acao: 'Início da cena',
        cd: 'Ordem decrescente',
        descricao: 'Define a ordem em que os personagens agem no início de uma cena de ação.',
      },
    ],
  },
  'Intimidação': {
    atributo: 'car',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Assustar ou coagir criaturas. Usos são efeitos de medo.',
    usos: [
      {
        nome: 'Assustar',
        acao: 'Padrão',
        cd: 'Oposto a Vontade',
        descricao: 'Alvo em alcance curto fica abalado pela cena (ou apavorado 1 rodada e depois abalado se passar por 10+).',
      },
      {
        nome: 'Coagir',
        acao: '1 minuto+',
        cd: 'Oposto a Vontade',
        descricao: 'Força criatura inteligente adjacente a obedecer uma ordem (+5 ou sucesso automático se perigosa). Alvo fica hostil.',
      },
    ],
  },
  'Intuição': {
    atributo: 'sab',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Empatia, leitura corporal e sexto sentido.',
    usos: [
      {
        nome: 'Perceber Mentira',
        acao: '—',
        cd: 'Oposto a Enganação',
        descricao: 'Descobre se alguém está mentindo ou tentando passar uma insinuação.',
      },
      {
        nome: 'Pressentimento',
        acao: '—',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Analisa a índole de uma pessoa ou detecta se há algo anormal em uma situação (sem revelar a causa).',
      },
    ],
  },
  'Investigação': {
    atributo: 'int',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Encontrar pistas, armadilhas, rastros e coletar informações.',
    usos: [
      {
        nome: 'Interrogar',
        acao: '1 hora + T$ 3d6',
        cd: 'CD 20 / 30',
        descricao: 'Obtém informações restritas (CD 20) ou confidenciais (CD 30) perguntando em locais movimentados.',
      },
      {
        nome: 'Procurar',
        acao: 'Completa a 1 dia',
        cd: 'CD 15 / 20 / 30',
        descricao: 'Encontra item em bagunça (15), escondido (20) ou muito bem escondido (30), além de armadilhas e rastros.',
      },
    ],
  },
  'Jogatina': {
    atributo: 'car',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Jogos de azar e apostas.',
    usos: [
      {
        nome: 'Apostar',
        acao: '1 noite + T$ 1d10',
        cd: 'Tabela (≤9: 0 | 10–14: ½ | 15–19: 1× | 20–29: 2× | 30–39: 3× | 40+: 5×)',
        apenas_treinado: true,
        descricao: 'Determina o retorno da aposta em uma noite de jogos de azar conforme o resultado do teste.',
      },
    ],
  },
  'Ladinagem': {
    atributo: 'des',
    treino_apenas: true,
    penalidade_armadura: true,
    resumo: 'Abrir fechaduras, punga, ocultar objetos e sabotar armadilhas.',
    usos: [
      {
        nome: 'Abrir Fechadura',
        acao: 'Completa',
        cd: 'CD 20 / 25 / 30',
        apenas_treinado: true,
        descricao: 'Exige gazua (–5 sem). Simples (20), média (25), superior/cofre (30).',
      },
      {
        nome: 'Ocultar',
        acao: 'Padrão',
        cd: 'Oposto a Percepção',
        apenas_treinado: true,
        descricao: 'Esconde objeto no corpo (+5 pequeno, –5 grande; quem revistar recebe +10 em Percepção).',
      },
      {
        nome: 'Punga',
        acao: 'Padrão',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Furta ou planta objeto em outra pessoa (vítima faz Percepção contra seu resultado para notar).',
      },
      {
        nome: 'Sabotar',
        acao: '1d4 rodadas (–5 Completa)',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Desabilita mecanismo/armadilha simples (20) ou avançada (30). Falhar por 5+ dispara ou engana.',
      },
    ],
  },
  'Luta': {
    atributo: 'for',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Ataques corpo a corpo e manobras de combate.',
    usos: [
      {
        nome: 'Ataque Corpo a Corpo',
        acao: 'Padrão',
        cd: 'Defesa do alvo',
        descricao: 'Realiza ataques corpo a corpo e manobras (agarrar, derrubar, desarmar, empurrar, quebrar).',
      },
    ],
  },
  'Misticismo': {
    atributo: 'int',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Magias, itens mágicos, criaturas mágicas e conjuração com armadura.',
    usos: [
      {
        nome: 'Detectar Magia',
        acao: 'Completa',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Detecta presença e intensidade de auras mágicas em alcance curto (–5 madeira/pedra, –10 ferro/chumbo).',
      },
      {
        nome: 'Identificar Criatura',
        acao: 'Padrão',
        cd: 'CD 15 + ND',
        apenas_treinado: true,
        descricao: 'Lembra 1 característica de criatura mágica (+1 a cada 5 acima da CD). Falhar por 5+ dá informação falsa.',
      },
      {
        nome: 'Identificar Item Mágico',
        acao: '1 hora (–10 Completa)',
        cd: 'CD 20 / 25 / 30',
        apenas_treinado: true,
        descricao: 'Identifica poderes de item mágico menor (20), médio (25) ou maior (30).',
      },
      {
        nome: 'Identificar Magia',
        acao: 'Reação',
        cd: 'CD 15 + PM',
        apenas_treinado: true,
        descricao: 'Identifica magia sendo lançada através de seus gestos e palavras.',
      },
      {
        nome: 'Informação',
        acao: '—',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Responde dúvidas sobre magias, runas, profecias e planos (complexas CD 20, mistérios CD 30).',
      },
      {
        nome: 'Lançar Magia de Armadura',
        acao: 'Parte da magia',
        cd: 'CD 20 + PM',
        apenas_treinado: true,
        descricao: 'Sofre penalidade de armadura. Exigido para lançar magia arcana usando armadura; se falhar, gasta PM sem efeito.',
      },
    ],
  },
  'Nobreza': {
    atributo: 'int',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Etiqueta aristocrática, leis, linhagens e heráldica.',
    usos: [
      {
        nome: 'Etiqueta',
        acao: '—',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Portar-se adequadamente em bailes, cortes e audiências aristocráticas.',
      },
      {
        nome: 'Informação',
        acao: '—',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Responde dúvidas sobre leis, tradições, linhagens e heráldica (complexas CD 20, mistérios CD 30).',
      },
    ],
  },
  'Ofício': {
    atributo: 'int',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Fabricar, consertar e identificar itens (Armeiro, Artesão, Alquimista, Cozinheiro, Alfaiate...).',
    nota: 'Exige instrumentos de ofício específicos (–5 sem).',
    usos: [
      {
        nome: 'Consertar',
        acao: '1 hora + 1/10 preço',
        cd: 'CD 15 / 20',
        apenas_treinado: true,
        descricao: 'Repara item destruído usando a mesma CD de fabricação (simples 15, complexos 20).',
      },
      {
        nome: 'Fabricar',
        acao: '1 dia / 1 sem / 1 mês',
        cd: 'CD 15 / 20',
        apenas_treinado: true,
        descricao: 'Custa 1/3 do preço em matéria-prima. Simples (CD 15), complexos (CD 20). Consumíveis: –5 para fazer 2 unidades.',
      },
      {
        nome: 'Identificar',
        acao: 'Completa',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Descobre propriedades e preço de itens raros ou exóticos ligados ao seu Ofício.',
      },
      {
        nome: 'Sustento',
        acao: '1 semana',
        cd: 'CD 15',
        apenas_treinado: true,
        descricao: 'Ganha T$ 1 (+T$ 1 por ponto acima da CD 15) por semana de trabalho.',
      },
    ],
  },
  'Percepção': {
    atributo: 'sab',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Notar detalhes, ler lábios, ouvir ruídos e detectar criaturas ocultas.',
    usos: [
      {
        nome: 'Observar',
        acao: '—',
        cd: 'CD 15–30 / Oposto',
        descricao: 'Vê coisas discretas (15) a quase invisíveis (30), ler lábios (20) ou oposto a Furtividade/Ladinagem.',
      },
      {
        nome: 'Ouvir',
        acao: '—',
        cd: 'CD 0 / 15 / 20',
        descricao: 'Conversa (0), sussurro (15), atrás de porta (+10), dormindo (–10), criatura invisível (CD 20 ou Furtividade+10).',
      },
    ],
  },
  'Pilotagem': {
    atributo: 'des',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Operar carroças, navios, dirigíveis e veículos.',
    usos: [
      {
        nome: 'Conduzir Veículo',
        acao: 'Movimento',
        cd: 'CD 15 / 25',
        apenas_treinado: true,
        descricao: 'Situações ruins (CD 15) ou extremas/tempestades (CD 25). Falhar avança metade; falhar por 5+ acidenta.',
      },
    ],
  },
  'Pontaria': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Ataques à distância com armas de disparo e arremesso.',
    usos: [
      {
        nome: 'Ataque à Distância',
        acao: 'Padrão',
        cd: 'Defesa do alvo',
        descricao: 'Realiza ataques à distância com arcos, bestas, armas de fogo e armas de arremesso.',
      },
    ],
  },
  'Reflexos': {
    atributo: 'des',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Perícia de resistência contra explosões, armadilhas e fintas.',
    usos: [
      {
        nome: 'Resistir a Efeitos',
        acao: 'Reação',
        cd: 'CD do efeito',
        descricao: 'Resiste a explosões, sopros, magias de área e armadilhas.',
      },
      {
        nome: 'Evitar Finta',
        acao: 'Reação',
        cd: 'Oposto a Enganação',
        descricao: 'Evita ficar desprevenido contra uma tentativa de Fintar.',
      },
    ],
  },
  'Religião': {
    atributo: 'sab',
    treino_apenas: true,
    penalidade_armadura: false,
    resumo: 'Conhecimento sobre deuses, criaturas divinas e cerimônias religiosas.',
    usos: [
      {
        nome: 'Identificar Criatura',
        acao: 'Padrão',
        cd: 'CD 15 + ND',
        apenas_treinado: true,
        descricao: 'Identifica criaturas de origem divina (anjos, demônios, alguns mortos-vivos/construtos).',
      },
      {
        nome: 'Identificar Item Mágico',
        acao: '1 hora (–10 Completa)',
        cd: 'CD 20 / 25 / 30',
        apenas_treinado: true,
        descricao: 'Identifica item mágico de origem divina menor (20), médio (25) ou maior (30).',
      },
      {
        nome: 'Informação',
        acao: '—',
        cd: 'CD 20 / 30',
        apenas_treinado: true,
        descricao: 'Dúvidas sobre deuses, profecias e planos (complexas CD 20, mistérios CD 30).',
      },
      {
        nome: 'Rito',
        acao: 'Cerimônia',
        cd: 'CD 20',
        apenas_treinado: true,
        descricao: 'Realiza batizados, casamentos, funerais ou penitência (T$ 100 × nível do devoto ou missão sagrada).',
      },
    ],
  },
  'Sobrevivência': {
    atributo: 'sab',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Acampar, orientar-se, identificar feras e rastrear nos ermos.',
    usos: [
      {
        nome: 'Acampamento',
        acao: '1 dia',
        cd: 'CD 15 / 20 / 25 / 30',
        descricao: 'Exige equipamento de viagem (–5 sem). Planícies (15), florestas (20), desertos/montanhas (25), Tormenta (30). Clima ruim –5.',
      },
      {
        nome: 'Identificar Criatura',
        acao: 'Padrão',
        cd: 'CD 15 + ND',
        descricao: 'Identifica animais ou monstros (lembra 1 característica +1 a cada 5 acima da CD).',
      },
      {
        nome: 'Orientar-se',
        acao: '1 dia',
        cd: 'CD 15–30 (terreno)',
        descricao: 'Passar avança deslocamento normal; falhar avança metade; falhar por 5+ se perde.',
      },
      {
        nome: 'Rastrear',
        acao: 'Metade do desl.',
        cd: 'CD 15 / 20 / 25',
        apenas_treinado: true,
        descricao: 'Solo macio (15), comum (20), duro (25). Grupo grande/Enorme –5; visibilidade precária +5; +1 por dia passado.',
      },
    ],
  },
  'Vontade': {
    atributo: 'sab',
    treino_apenas: false,
    penalidade_armadura: false,
    resumo: 'Perícia de resistência para determinação, medo e encantamentos.',
    usos: [
      {
        nome: 'Resistir a Efeitos Mentais',
        acao: 'Reação',
        cd: 'CD do efeito',
        descricao: 'Resiste a intimidação, medo, encantamentos, ilusões e efeitos mentais.',
      },
    ],
  },
};

export default DADOS_PERICIAS_FRONTEND;
