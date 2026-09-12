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
// 🆕 LOTE R5 — Tabela 4-1 + reduções (espelho de app/src/regras/custo_magia.py)
export const CUSTO_POR_CIRCULO: Record<number, number> = { 1: 1, 2: 3, 3: 6, 4: 10, 5: 15 };

export function calcularCustoMagiaView(magia: any, ficha: any) {
    const circ = parseInt(String(magia?.circulo), 10) || 1;
    const base = CUSTO_POR_CIRCULO[circ] ?? 1;
    const fontes: { label: string; valor: number }[] = [{ label: `Custo do ${circ}º círculo (Tabela 4-1)`, valor: base }];
    let total = base;
    for (const hab of ficha?.habilidades || []) {
        const ef: any = { ...(hab.efeitos || {}), ...(hab.escolhas_aplicadas || {}) };
        const mult = ef.reducao_custo_magia_global;
        if (typeof mult === 'number' && mult > 0 && mult < 1) {
            const antes = total;
            total = Math.floor(total * mult);
            fontes.push({ label: `${hab.nome} (×${mult})`, valor: total - antes });
        }
        const rc = ef.reducao_custo_magia;
        if (rc && Array.isArray(rc.nomes) && rc.nomes.includes(magia?.nome)) {
            const v = parseInt(rc.valor, 10) || 1;
            total -= v;
            fontes.push({ label: `${hab.nome} (−${v} PM)`, valor: -v });
        }
    }
    total = Math.max(1, total); // mínimo 1 PM (0 só para Truque)
    return { total, base, fontes };
}
