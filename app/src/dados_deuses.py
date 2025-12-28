# Mapeamento de "Duyshidakk" para raças goblinoide
DUYSHIDAKK = ["Goblin", "Hobgoblin", "Bugbear", "Orc", "Ogro"]

DADOS_DEUSES = {
    "Aharadak": {
        "nome": "Aharadak",
        "crencas": "Reverenciar a Tormenta, praticar a devassidão, abraçar a loucura.",
        "simbolo": "Olho macabro cercado de espinhos",
        "energia": "Negativa",
        "arma": "Corrente de espinhos",
        "devotos": ["Todos"], # Aceita tudo e todos
        "poderes": ["Afinidade com a Tormenta", "Êxtase da Loucura", "Percepção Temporal", "Rejeição Divina"]
    },
    "Allihanna": {
        "nome": "Allihanna",
        "crencas": "Proteger a natureza, vida selvagem, combater monstros.",
        "simbolo": "Animal ou árvore",
        "energia": "Positiva",
        "arma": "Bordão",
        "devotos": ["Dahllan", "Elfo", "Sílfide", "Bárbaro", "Caçador", "Druida"],
        "poderes": ["Compreender os Ermos", "Dedo Verde", "Descanso Natural", "Voz da Natureza"]
    },
    "Arsenal": {
        "nome": "Arsenal",
        "crencas": "Guerra, conflito, vitória a qualquer custo.",
        "simbolo": "Martelo e espada cruzados",
        "energia": "Qualquer",
        "arma": "Martelo de guerra",
        "devotos": ["Anão", "Minotauro", "Bárbaro", "Cavaleiro", "Guerreiro", "Lutador"],
        "poderes": ["Conjurar Arma", "Coragem Total", "Fé Guerreira", "Sangue de Ferro"]
    },
    "Azgher": {
        "nome": "Azgher",
        "crencas": "Honestidade, caridade, combater o mal e as trevas.",
        "simbolo": "Sol dourado",
        "energia": "Positiva",
        "arma": "Cimitarra",
        "devotos": ["Suraggel (Aggelus)", "Qareen", "Arcanista", "Bárbaro", "Caçador", "Cavaleiro", "Guerreiro", "Nobre", "Paladino"],
        "poderes": ["Espada Solar", "Fulgor Solar", "Habitante do Deserto", "Inimigo de Tenebra"]
    },
    "Hyninn": {
        "nome": "Hyninn",
        "crencas": "Astúcia, trapaça, desafiar a lei, levar vantagem.",
        "simbolo": "Adaga atravessando máscara ou raposa",
        "energia": "Qualquer",
        "arma": "Adaga",
        "devotos": ["Hynne", "Goblin", "Sílfide", "Bardo", "Bucaneiro", "Ladino", "Inventor", "Nobre"],
        "poderes": ["Apostar com o Trapaceiro", "Farsa do Fingidor", "Forma de Macaco", "Golpista Divino"]
    },
    "Kallyadranoch": {
        "nome": "Kallyadranoch",
        "crencas": "Soberania, orgulho, acumular riquezas, poder dos dragões.",
        "simbolo": "Escamas de cinco cores",
        "energia": "Negativa",
        "arma": "Lança",
        "devotos": ["Elfo", "Medusa", "Suraggel (Sulfure)", "Arcanista", "Cavaleiro", "Guerreiro", "Lutador", "Nobre"],
        "poderes": ["Aura de Medo", "Escamas Dracônicas", "Presas Primordiais", "Servos do Dragão"]
    },
    "Khalmyr": {
        "nome": "Khalmyr",
        "crencas": "Justiça, ordem, caridade, combater o mal.",
        "simbolo": "Espada sobre balança",
        "energia": "Positiva",
        "arma": "Espada longa",
        "devotos": ["Suraggel (Aggelus)", "Anão", "Cavaleiro", "Guerreiro", "Nobre", "Paladino"],
        "poderes": ["Coragem Total", "Dom da Verdade", "Espada Justiceira", "Reparar Injustiça"]
    },
    "Lena": {
        "nome": "Lena",
        "crencas": "Vida, fertilidade, cura, pacifismo total.",
        "simbolo": "Lua crescente prateada",
        "energia": "Positiva",
        "arma": None, # Não tem
        "devotos": ["Dahllan", "Qareen", "Nobre", "Paladino"], # Apenas mulheres (regra de validação extra)
        "poderes": ["Ataque Piedoso", "Aura Restauradora", "Cura Gentil", "Curandeira Perfeita"]
    },
    "Lin-Wu": {
        "nome": "Lin-Wu",
        "crencas": "Honra, integridade, lealdade.",
        "simbolo": "Dragão-serpente celestial",
        "energia": "Qualquer",
        "arma": "Katana",
        "devotos": ["Anão", "Cavaleiro", "Guerreiro", "Nobre", "Paladino"],
        "poderes": ["Coragem Total", "Kiai Divino", "Mente Vazia", "Tradição de Lin-Wu"]
    },
    "Marah": {
        "nome": "Marah",
        "crencas": "Paz, amor, alegria, não-violência.",
        "simbolo": "Coração vermelho",
        "energia": "Positiva",
        "arma": None,
        "devotos": ["Suraggel (Aggelus)", "Elfo", "Hynne", "Qareen", "Bardo", "Nobre", "Paladino"],
        "poderes": ["Aura de Paz", "Dom da Esperança", "Palavras de Bondade", "Talento Artístico"]
    },
    "Megalokk": {
        "nome": "Megalokk",
        "crencas": "Violência, lei do mais forte, destruir inimigos.",
        "simbolo": "Garra de monstro",
        "energia": "Negativa",
        "arma": "Maça",
        "devotos": ["Goblin", "Medusa", "Minotauro", "Suraggel (Sulfure)", "Trog", "Bárbaro", "Caçador", "Druida", "Lutador"],
        "poderes": ["Olhar Amedrontador", "Presas Primordiais", "Urro Divino", "Voz dos Monstros"]
    },
    "Nimb": {
        "nome": "Nimb",
        "crencas": "Caos, sorte, azar, loucura.",
        "simbolo": "Dado de seis faces",
        "energia": "Qualquer",
        "arma": "Adaga", # Simplificação, regra diz "qualquer"
        "devotos": ["Goblin", "Qareen", "Sílfide", "Arcanista", "Bárbaro", "Bardo", "Bucaneiro", "Inventor", "Ladino"],
        "poderes": ["Êxtase da Loucura", "Poder Oculto", "Sorte dos Loucos", "Transmissão da Loucura"]
    },
    "Oceano": {
        "nome": "Oceano",
        "crencas": "Mares, harmonia com oceano, respeito às tempestades.",
        "simbolo": "Concha",
        "energia": "Qualquer",
        "arma": "Tridente",
        "devotos": ["Dahllan", "Hynne", "Minotauro", "Sereia/Tritão", "Bárbaro", "Bucaneiro", "Caçador", "Druida"],
        "poderes": ["Anfíbio", "Arsenal das Profundezas", "Mestre dos Mares", "Sopro do Mar"]
    },
    "Sszzaas": {
        "nome": "Sszzaas",
        "crencas": "Traição, intriga, corrupção, inteligência maligna.",
        "simbolo": "Naja com veneno",
        "energia": "Negativa",
        "arma": "Adaga",
        "devotos": ["Medusa", "Arcanista", "Bardo", "Bucaneiro", "Inventor", "Ladino", "Nobre"],
        "poderes": ["Astúcia da Serpente", "Familiar Ofídico", "Presas Venenosas", "Sangue Ofídico"]
    },
    "Tanna-Toh": {
        "nome": "Tanna-Toh",
        "crencas": "Conhecimento, civilização, verdade, artes e ciências.",
        "simbolo": "Pergaminho e pena",
        "energia": "Qualquer",
        "arma": "Bordão",
        "devotos": ["Golem", "Kliren", "Arcanista", "Bardo", "Inventor", "Nobre", "Paladino"],
        "poderes": ["Conhecimento Enciclopédico", "Mente Analítica", "Pesquisa Abençoada", "Voz da Civilização"]
    },
    "Tenebra": {
        "nome": "Tenebra",
        "crencas": "Noite, escuridão, mortos-vivos, segredos.",
        "simbolo": "Estrela negra",
        "energia": "Negativa",
        "arma": "Adaga",
        "devotos": ["Anão", "Medusa", "Qareen", "Osteon", "Suraggel (Sulfure)", "Trog", "Arcanista", "Bardo", "Ladino"],
        "poderes": ["Carícia Sombria", "Manto da Penumbra", "Visão nas Trevas", "Zumbificar"]
    },
    "Thwor": {
        "nome": "Thwor",
        "crencas": "União goblinoide, força, caos, destruir elfos.",
        "simbolo": "Punho fechado",
        "energia": "Qualquer",
        "arma": "Machado de guerra",
        "devotos": DUYSHIDAKK, # Lista expandida
        "poderes": ["Almejar o Impossível", "Fúria Divina", "Olhar Amedrontador", "Tropas Duyshidakk"]
    },
    "Thyatis": {
        "nome": "Thyatis",
        "crencas": "Ressurreição, profecia, segundas chances, perdão.",
        "simbolo": "Fênix",
        "energia": "Positiva",
        "arma": "Espada longa",
        "devotos": ["Suraggel (Aggelus)", "Cavaleiro", "Guerreiro", "Inventor", "Lutador", "Paladino"],
        "poderes": ["Ataque Piedoso", "Dom da Imortalidade", "Dom da Profecia", "Dom da Ressurreição"]
    },
    "Valkaria": {
        "nome": "Valkaria",
        "crencas": "Ambição, liberdade, aventura, desafiar limites.",
        "simbolo": "Estátua ou seis faixas",
        "energia": "Positiva",
        "arma": "Mangual",
        "devotos": ["Todos"], # Aventureiros de todas as classes
        "poderes": ["Almejar o Impossível", "Armas da Ambição", "Coragem Total", "Liberdade Divina"]
    },
    "Wynna": {
        "nome": "Wynna",
        "crencas": "Magia, generosidade, proteger seres mágicos.",
        "simbolo": "Anel metálico",
        "energia": "Qualquer",
        "arma": "Adaga",
        "devotos": ["Elfo", "Golem", "Qareen", "Sílfide", "Arcanista", "Bardo"],
        "poderes": ["Bênção do Mana", "Centelha Mágica", "Escudo Mágico", "Teurgista Místico"]
    }
}