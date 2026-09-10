// Opções fixas de escolhas secundárias de poderes (T20)
export const ESCOLAS_MAGIA = [
    "Abjuração", "Adivinhação", "Convocação", "Encantamento",
    "Evocação", "Ilusão", "Necromancia", "Transmutação"
];

export const FAMILIARES_ARCANOS = [
    "Borboleta", "Cobra", "Coruja", "Corvo", "Falcão",
    "Gato", "Lagarto", "Morcego", "Rato", "Sapo"
];

export const ATRIBUTOS = [
    { valor: "forca", rotulo: "Força" },
    { valor: "destreza", rotulo: "Destreza" },
    { valor: "constituicao", rotulo: "Constituição" },
    { valor: "inteligencia", rotulo: "Inteligência" },
    { valor: "sabedoria", rotulo: "Sabedoria" },
    { valor: "carisma", rotulo: "Carisma" },
];

// Poderes que exigem escolha secundária.
// A `chave` é o key salvo em escolhas_aplicadas (o backend lê exatamente estes).
export const PODERES_COM_ESCOLHA: Record<string, Array<{ chave: string; rotulo: string; opcoes: any[] }>> = {
    "Aumento de Atributo": [{ chave: "atributo", rotulo: "Atributo", opcoes: ATRIBUTOS }],
    "Especialista em Escola": [{ chave: "escola", rotulo: "Escola de Magia", opcoes: ESCOLAS_MAGIA }],
    "Mestre em Escola": [{ chave: "escola", rotulo: "Escola de Magia", opcoes: ESCOLAS_MAGIA }],
    "Familiar": [{ chave: "familiar", rotulo: "Familiar Arcano", opcoes: FAMILIARES_ARCANOS }],
};
