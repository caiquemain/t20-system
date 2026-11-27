export interface SuplementoInfo {
    id: string;
    nome: string;
    sigla: string;
    cor: string;
    basico?: boolean;
}

export const FONTE_LIVRO_BASICO = 'T20 JdA';

export const SUPLEMENTOS_OFICIAIS: SuplementoInfo[] = [
    { id: 'T20 JdA', nome: 'Tormenta20 — Jogo do Ano', sigla: 'JdA', cor: '#b71c1c', basico: true },
    { id: 'Ameaças de Arton', nome: 'Ameaças de Arton', sigla: 'Ameaças', cor: '#7b1fa2' },
    { id: 'Heróis de Arton', nome: 'Heróis de Arton', sigla: 'Heróis', cor: '#1565c0' },
    { id: 'Deuses de Arton', nome: 'Deuses de Arton', sigla: 'Deuses', cor: '#c77800' },
    { id: 'Atlas de Arton', nome: 'Atlas de Arton', sigla: 'Atlas', cor: '#2e7d32' },
];

export const TODOS_SUPLEMENTOS_IDS = SUPLEMENTOS_OFICIAIS.map(s => s.id);

export function obterInfoSuplemento(fonte?: string): SuplementoInfo {
    const id = (fonte || FONTE_LIVRO_BASICO).trim();
    return (
        SUPLEMENTOS_OFICIAIS.find(s => s.id === id) || {
            id,
            nome: id,
            sigla: id,
            cor: '#475569',
        }
    );
}

/**
 * Verifica se uma entidade (com tag `fonte`) está liberada pelos suplementos ativos da ficha.
 * Por padrão (quando `suplementosAtivos` não foi definido ou está vazio), todos os livros ficam ativos.
 */
export function entidadePermitidaPorSuplementos(
    fonte?: string,
    suplementosAtivos?: string[] | null,
): boolean {
    if (!suplementosAtivos || suplementosAtivos.length === 0) return true;
    const f = (fonte || FONTE_LIVRO_BASICO).trim();
    if (f === FONTE_LIVRO_BASICO) return true;
    return suplementosAtivos.includes(f);
}
