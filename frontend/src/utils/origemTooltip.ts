export interface DadosOrigem {
    fonte?: string;
    regiao?: string;
    regional?: boolean;
    descricao?: string;
    beneficio_texto?: string;
    itens?: string;
    qtd_escolhas?: number;
    pericias_fixas?: string[];
    poder_fixo?: string;
    beneficios_lista?: string[];
}

export function formatarResumoOrigem(o?: DadosOrigem): string | undefined {
    if (!o) return undefined;
    if (o.regional || o.qtd_escolhas === 0) {
        const partes: string[] = [];
        if (o.regiao) partes.push(o.regiao);
        partes.push('Benefício Único');
        if (o.pericias_fixas && o.pericias_fixas.length > 0) {
            partes.push(o.pericias_fixas.join(', '));
        }
        return partes.join(' • ');
    }
    const qtd = o.qtd_escolhas ?? 2;
    const bens = (o.beneficios_lista || []).slice(0, 4).join(', ');
    return bens ? `Escolha ${qtd}: ${bens}${(o.beneficios_lista?.length || 0) > 4 ? '…' : ''}` : `Escolha ${qtd} benefícios`;
}

export function formatarTooltipOrigem(nome: string, o?: DadosOrigem): string | undefined {
    if (!o) return undefined;
    const linhas: string[] = [];
    if (o.regional || o.qtd_escolhas === 0) {
        linhas.push(`${nome} — Origem Regional${o.regiao ? ` (${o.regiao})` : ''}`);
        if (o.beneficio_texto) {
            linhas.push(`Benefício Único: ${o.beneficio_texto}`);
        }
        if (o.pericias_fixas && o.pericias_fixas.length > 0) {
            linhas.push(`Perícias Treinadas: ${o.pericias_fixas.join(', ')}`);
        }
    } else {
        const qtd = o.qtd_escolhas ?? 2;
        linhas.push(`${nome} — Origem Básica (escolha ${qtd} benefícios)`);
        if (o.beneficios_lista && o.beneficios_lista.length > 0) {
            linhas.push(`Benefícios Disponíveis: ${o.beneficios_lista.join(', ')}`);
        }
    }
    if (o.itens) {
        linhas.push(`Itens Iniciais: ${o.itens}`);
    }
    if (o.descricao) {
        linhas.push(`Descrição: ${o.descricao}`);
    }
    return linhas.join('\n');
}
