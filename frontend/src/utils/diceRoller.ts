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

interface TermosFormula {
    dados: Map<number, number>; // faces -> quantidade
    bonus: number;
}

function parseTermos(formula: string, mult = 1): TermosFormula {
    const dados = new Map<number, number>();
    let bonus = 0;
    const limpa = (formula || '').replace(/\s+/g, '');
    const tokens = limpa.match(/[+-]?[^+-]+/g) || [];
    for (const token of tokens) {
        const sinal = token.startsWith('-') ? -1 : 1;
        const corpo = token.replace(/^[+-]/, '');
        const md = corpo.match(/^(\d*)d(\d+)$/i);
        if (md) {
            const qtd = parseInt(md[1] || '1', 10) * sinal * mult;
            const faces = parseInt(md[2], 10);
            dados.set(faces, (dados.get(faces) || 0) + qtd);
        } else if (/^\d+$/.test(corpo)) {
            bonus += parseInt(corpo, 10) * sinal * mult;
        }
    }
    return { dados, bonus };
}

function formatarTermos(termos: TermosFormula): string {
    const partes: string[] = [];
    const facesOrdenadas = Array.from(termos.dados.entries()).filter(([, q]) => q !== 0);
    for (const [faces, qtd] of facesOrdenadas) {
        if (partes.length === 0) {
            partes.push(`${qtd}d${faces}`);
        } else {
            partes.push(qtd > 0 ? `+${qtd}d${faces}` : `${qtd}d${faces}`);
        }
    }
    if (termos.bonus !== 0) {
        if (partes.length === 0) {
            partes.push(String(termos.bonus));
        } else {
            partes.push(termos.bonus > 0 ? `+${termos.bonus}` : String(termos.bonus));
        }
    }
    return partes.join('');
}

/**
 * Aplica incrementos de dados/bônus dos aprimoramentos selecionados à fórmula base da magia.
 * Ex.: Infligir Ferimentos (2d8+2) + 3× (+1d8+1) => "5d8+5"
 * Ex.: Bola de Fogo (6d6) + 2× (+2d6) => "10d6"
 */
export function aplicarAprimoramentosNaFormula(
    formulaBase: string | null,
    aprimoramentos: Array<{ custo: string; descricao: string }> = [],
    aprimoramentosQtd: Record<number, number> = {},
    truqueAtivo = false,
    bonusExtra = 0
): string | null {
    if (truqueAtivo) {
        const truque = aprimoramentos.find(a => /truque/i.test(a.custo || ''));
        const fTruque = truque ? extrairFormulaDeTexto(truque.descricao || '') : null;
        return fTruque || null;
    }

    if (!formulaBase) return null;
    const acc = parseTermos(formulaBase, 1);

    aprimoramentos.forEach((ap, idx) => {
        const qtd = aprimoramentosQtd[idx] || 0;
        if (qtd <= 0) return;
        const desc = (ap.descricao || '').trim();
        // Apenas aprimoramentos que aumentam dano/cura/PV (ignora parênteses de alternativas)
        if (!/^aumenta/i.test(desc)) return;
        const semParenteses = desc.replace(/\([^)]*\)/g, '');
        // Ignora cláusulas secundárias após "dano mínimo" ou "dano em chamas" ou "mista"
        const partePrincipal = semParenteses.split(/dano mínimo|dano em chamas|e mista/i)[0];
        const matches = partePrincipal.match(/\+?\d+d\d+(?:\s*[+-]\s*\d+)?/gi);
        if (!matches) return;
        for (const m of matches) {
            const inc = parseTermos(m, qtd);
            inc.dados.forEach((q, faces) => {
                acc.dados.set(faces, (acc.dados.get(faces) || 0) + q);
            });
            acc.bonus += inc.bonus;
        }
    });

    if (bonusExtra) {
        acc.bonus += bonusExtra;
    }
    return formatarTermos(acc) || formulaBase;
}

