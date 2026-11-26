/** Utilitário de rolagem de dados (T20 JdA) para magias, ataques e habilidades. */

export interface DadoRolado {
    dado: string;
    rolagens: number[];
    sinal: 1 | -1;
}

export interface ResultadoExpressao {
    formula: string;
    total: number;
    detalhes: DadoRolado[];
    bonus: number;
}

export interface ResultadoD20 {
    d20: number;
    bonus: number;
    total: number;
    criticoNatural: 'sucesso' | 'falha' | null;
}

export function rolarExpressao(formula: string): ResultadoExpressao | null {
    const limpa = (formula || '').replace(/\s+/g, '');
    if (!limpa) return null;

    const tokens = limpa.match(/[+-]?[^+-]+/g);
    if (!tokens) return null;

    const detalhes: DadoRolado[] = [];
    let bonus = 0;
    let total = 0;
    let achouTermo = false;

    for (const token of tokens) {
        const sinal: 1 | -1 = token.startsWith('-') ? -1 : 1;
        const corpo = token.replace(/^[+-]/, '');
        const matchDado = corpo.match(/^(\d*)d(\d+)$/i);
        if (matchDado) {
            achouTermo = true;
            const qtd = Math.min(100, Math.max(1, parseInt(matchDado[1] || '1', 10)));
            const faces = Math.min(1000, Math.max(2, parseInt(matchDado[2], 10)));
            const rolagens: number[] = [];
            for (let i = 0; i < qtd; i++) {
                const r = Math.floor(Math.random() * faces) + 1;
                rolagens.push(r);
                total += sinal * r;
            }
            detalhes.push({ dado: `${qtd}d${faces}`, rolagens, sinal });
        } else if (/^\d+$/.test(corpo)) {
            achouTermo = true;
            const val = sinal * parseInt(corpo, 10);
            bonus += val;
            total += val;
        }
    }

    if (!achouTermo) return null;
    return { formula: limpa, total, detalhes, bonus };
}

export function rolarAtaqueD20(bonusStr: string): ResultadoD20 {
    const match = (bonusStr || '').match(/[+-]?\d+/);
    const bonus = match ? parseInt(match[0], 10) : 0;
    const d20 = Math.floor(Math.random() * 20) + 1;
    return {
        d20,
        bonus,
        total: d20 + bonus,
        criticoNatural: d20 === 20 ? 'sucesso' : d20 === 1 ? 'falha' : null,
    };
}

export function extrairFormulaDeTexto(texto: string): string | null {
    const m = (texto || '').match(/\b\d+d\d+(?:\s*[+-]\s*\d+)?/i);
    return m ? m[0].replace(/\s+/g, '') : null;
}

export function parseCustoAprimoramento(custoStr: string): { ehTruque: boolean; pm: number } {
    const raw = (custoStr || '').trim();
    if (/truque/i.test(raw)) return { ehTruque: true, pm: 0 };
    const m = raw.match(/\+?\s*(\d+)\s*PM/i);
    return { ehTruque: false, pm: m ? parseInt(m[1], 10) : 0 };
}
