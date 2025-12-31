// frontend/src/utils/magicUtils.ts

// Cores das Escolas (Inspirado em convenções de RPG)
export const SCHOOL_COLORS: Record<string, string> = {
    'Abjuração': '#4fc3f7',   // Azul Claro (Proteção)
    'Adivinhação': '#26c6da', // Ciano (Visão)
    'Convocação': '#ffb74d',  // Laranja (Invocação)
    'Encantamento': '#f06292',// Rosa (Mente)
    'Evocação': '#e57373',    // Vermelho Claro (Fogo/Dano)
    'Ilusão': '#ba68c8',      // Roxo (Mistério)
    'Necromancia': '#81c784', // Verde (Vida/Morte)
    'Transmutação': '#fff176',// Amarelo (Mudança)
    'default': '#9e9e9e'      // Cinza
};

// Cores dos Círculos (Raridade/Poder)
export const CIRCLE_COLORS: Record<number, string> = {
    1: '#ffffff', // Comum (Branco)
    2: '#66bb6a', // Incomum (Verde)
    3: '#42a5f5', // Raro (Azul)
    4: '#ab47bc', // Épico (Roxo)
    5: '#ffca28'  // Lendário (Dourado)
};

export const getSchoolColor = (escola?: string) => {
    if (!escola) return SCHOOL_COLORS['default'];
    // Busca parcial (ex: "Evocação" encontra a chave)
    const key = Object.keys(SCHOOL_COLORS).find(k => escola.includes(k));
    return key ? SCHOOL_COLORS[key] : SCHOOL_COLORS['default'];
};

export const getCircleColor = (circulo: number) => {
    return CIRCLE_COLORS[circulo] || '#ffffff';
};

export const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#ff5252'; // Padrão/Universal agora é Vermelho
    const t = tipo.toLowerCase();
    if (t.includes('arcana')) return '#d236d2'; // Roxo/Magenta
    if (t.includes('divina')) return '#ffc107'; // Dourado/Amarelo
    return '#ff5252'; // Vermelho (Universal)
};