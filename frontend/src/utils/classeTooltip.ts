export interface DadosClasseResumo {
    pv_inicial?: number;
    pv_nivel?: number;
    pm_inicial?: number;
    pm_nivel?: number;
    pm_atributo?: string;
    pericias_iniciais?: string[];
    pericias_escolha?: number;
    proficiencias?: string[];
    classe_base?: string;
    fonte?: string;
    descricao?: string;
}

const NOME_ATTR_CURTO: Record<string, string> = {
    for: 'For',
    des: 'Des',
    con: 'Con',
    int: 'Int',
    sab: 'Sab',
    car: 'Car',
};

export function formatarResumoClasse(c?: DadosClasseResumo): string | undefined {
    if (!c) return undefined;
    const partes: string[] = [];
    if (c.classe_base) {
        partes.push(`Variante de ${c.classe_base}`);
    }
    if (c.pv_inicial !== undefined) {
        partes.push(`PV ${c.pv_inicial} (+${c.pv_nivel ?? 0}/nv)`);
    }
    if (c.pm_inicial !== undefined) {
        const attrPm = c.pm_atributo ? ` +${NOME_ATTR_CURTO[c.pm_atributo] || c.pm_atributo.toUpperCase()}` : '';
        partes.push(`PM ${c.pm_inicial}${attrPm} (+${c.pm_nivel ?? 0}/nv)`);
    }
    return partes.length > 0 ? partes.join(' • ') : undefined;
}

export function formatarDescricaoClasse(c?: DadosClasseResumo): string | undefined {
    if (!c) return undefined;
    if (c.descricao) return c.descricao;
    const partes: string[] = [];
    const fixas = c.pericias_iniciais || [];
    const esc = c.pericias_escolha ?? 0;
    if (fixas.length > 0 || esc > 0) {
        partes.push(`Perícias: ${fixas.join(', ')}${esc > 0 ? ` + ${esc} à escolha` : ''}`);
    }
    const profs = c.proficiencias || [];
    partes.push(`Proficiências: ${profs.length > 0 ? profs.join(', ') : 'Nenhuma'}`);
    return partes.join(' | ');
}

export function formatarTooltipClasse(nome: string, c?: DadosClasseResumo): string | undefined {
    if (!c) return undefined;
    const linhas: string[] = [];
    linhas.push(c.classe_base ? `${nome} (Variante de ${c.classe_base})` : nome);
    const attrPm = c.pm_atributo ? ` + ${NOME_ATTR_CURTO[c.pm_atributo] || c.pm_atributo.toUpperCase()}` : '';
    if (c.pv_inicial !== undefined && c.pm_inicial !== undefined) {
        linhas.push(`PV: ${c.pv_inicial} + Con (+${c.pv_nivel ?? 0} + Con/nv) | PM: ${c.pm_inicial}${attrPm} (+${c.pm_nivel ?? 0}/nv)`);
    }
    const fixas = c.pericias_iniciais || [];
    const esc = c.pericias_escolha ?? 0;
    if (fixas.length > 0 || esc > 0) {
        linhas.push(`Perícias: ${fixas.join(', ')}${esc > 0 ? ` + ${esc} à escolha` : ''}`);
    }
    const profs = c.proficiencias || [];
    linhas.push(`Proficiências: ${profs.length > 0 ? profs.join(', ') : 'Nenhuma'}`);
    if (c.fonte) {
        linhas.push(`Livro: ${c.fonte}`);
    }
    return linhas.join('\n');
}
