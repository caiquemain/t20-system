export interface DadosDeus {
    nome?: string;
    titulo?: string;
    crencas?: string;
    descricao?: string;
    simbolo?: string;
    energia?: string;
    arma?: string | null;
    devotos?: string[];
    poderes?: string[];
    obrigacoes?: string;
}

export function formatarResumoDeus(d?: DadosDeus): string | undefined {
    if (!d) return undefined;
    const partes: string[] = [];
    if (d.titulo) partes.push(d.titulo);
    if (d.energia) partes.push(`Energia: ${d.energia}`);
    partes.push(`Arma: ${d.arma || 'Nenhuma'}`);
    return partes.join(' • ');
}

export function formatarTooltipDeus(nome: string, d?: DadosDeus): string | undefined {
    if (!d) return undefined;
    const linhas: string[] = [];
    linhas.push(d.titulo ? `${nome} — ${d.titulo}` : nome);
    linhas.push(`Energia: ${d.energia || '—'} | Arma Preferida: ${d.arma || 'Nenhuma'}`);
    if (d.simbolo) linhas.push(`Símbolo Sagrado: ${d.simbolo}`);
    if (d.poderes && d.poderes.length > 0) {
        linhas.push(`Poderes Concedidos: ${d.poderes.join(', ')}`);
    }
    if (d.crencas) linhas.push(`Crenças e Objetivos: ${d.crencas}`);
    if (d.obrigacoes) linhas.push(`Obrigações & Restrições: ${d.obrigacoes}`);
    return linhas.join('\n');
}
