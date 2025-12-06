import React, { useState, useMemo, useEffect } from 'react';
import '../Ficha.css';
import { PowerListItem } from './PowerListItem';
import { validarTodosRequisitos } from '../utils/validators';
import type { Personagem } from '../types';

interface PowerSelectorModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSelect: (valor: string) => void;
    ficha: Personagem;
    listaPoderes: any[];
    listaPericias: string[];
    tipoEscolha: string;
    titulo: string;
    listaRestrita?: string[];
    categoriaFixa?: string;
    itensBloqueados?: string[];
    subclasse?: string;
}

// CORREÇÃO DE EXPORTAÇÃO: Garante que 'export const' está claro
export const PowerSelectorModal: React.FC<PowerSelectorModalProps> = ({
    isOpen, onClose, onSelect, ficha,subclasse,
    listaPoderes, listaPericias, tipoEscolha, titulo,
    listaRestrita = [], categoriaFixa, itensBloqueados = []
}) => {
    const [filtro, setFiltro] = useState('');
    const [categoriaFiltro, setCategoriaFiltro] = useState(categoriaFixa || 'Todos');

    useEffect(() => {
        if (isOpen) {
            setFiltro('');
            setCategoriaFiltro(categoriaFixa || 'Todos');
        }
    }, [isOpen, categoriaFixa]);

    // 1. PROCESSAMENTO DA LISTA
    const itensProcessados = useMemo(() => {
        let itens: any[] = [];

        const formatarItem = (nome: string) => {
            // A. Perícias
            if (listaPericias.includes(nome)) {
                return {
                    nome, type: 'Perícia', categoria: 'Perícias',
                    descricao: 'Treinamento em perícia.', tagClass: 'tag-skill',
                    requisitos: [], isBlocked: false
                };
            }

            // B. Poderes (Tenta achar na lista completa que veio do backend)
            const poder = listaPoderes.find(p => p.nome === nome);
            if (poder) {
                // VALIDAÇÃO: Usa os requisitos vindos da API
                const requisitos = poder.requisitos || [];
                const validacao = validarTodosRequisitos(ficha, requisitos);

                return {
                    nome,
                    type: 'Poder',
                    categoria: poder.categoria || 'Geral',
                    descricao: poder.descricao,
                    tagClass: 'tag-power',
                    requisitos: requisitos,
                    isBlocked: !validacao.apto, // Bloqueia se não cumprir requisitos
                    blockReason: validacao.erros
                };
            }

            // C. Outros
            return { nome, type: 'Especial', categoria: 'Outros', descricao: 'Habilidade especial.', tagClass: 'tag-other', isBlocked: false };
        };

        // MODO A: LISTA RESTRITA (Origem, etc)
        if (listaRestrita && listaRestrita.length > 0) {
            itens = listaRestrita.map(formatarItem);
        }
        // MODO B: LISTA GERAL (Poderes Gerais)
        else {
            if (tipoEscolha === 'pericia' || tipoEscolha === 'ambos') {
                itens = itens.concat(listaPericias.map(nome => ({
                    nome, type: 'Perícia', categoria: 'Perícias', descricao: 'Treinamento.', tagClass: 'tag-skill', requisitos: [], isBlocked: false
                })));
            }
            if (tipoEscolha === 'poder' || tipoEscolha === 'ambos') {
                // Filtra origem fora da lista geral
                const poderesPermitidos = listaPoderes.filter(p => p.categoria !== 'Origem');

                itens = itens.concat(poderesPermitidos.map(p => {
                    // Validação aqui também!
                    const requisitos = p.requisitos || [];
                    const validacao = validarTodosRequisitos(ficha, requisitos);

                    return {
                        ...p,
                        type: 'Poder',
                        tagClass: 'tag-power',
                        categoria: p.categoria || 'Geral',
                        requisitos: requisitos,
                        isBlocked: !validacao.apto,
                        blockReason: validacao.erros
                    };
                }));
            }
        }

        // FILTRO DE BLOQUEADOS (O que já tem)
        if (itensBloqueados && itensBloqueados.length > 0) {
            const blacklist = new Set(itensBloqueados.map(i => i.trim().toLowerCase()));
            itens = itens.filter(i => !blacklist.has(i.nome.trim().toLowerCase()));
        }

        return itens.sort((a, b) => a.nome.localeCompare(b.nome));
    }, [listaRestrita, listaPoderes, listaPericias, tipoEscolha, itensBloqueados, ficha]);

    // 2. FILTRAGEM VISUAL
    const itensExibidos = useMemo(() => {
        return itensProcessados.filter(item => {
            const matchTexto = item.nome.toLowerCase().includes(filtro.toLowerCase());
            const matchCategoria = categoriaFiltro === 'Todos' || item.categoria === categoriaFiltro;
            const matchFixa = !categoriaFixa || item.categoria === categoriaFixa;
            return matchTexto && matchCategoria && matchFixa;
        });
    }, [itensProcessados, filtro, categoriaFiltro, categoriaFixa]);

    const categoriasDisponiveis = useMemo(() => {
        const cats = new Set<string>(['Todos']);
        itensProcessados.forEach(item => {
            if (item.categoria) cats.add(item.categoria);
        });
        return Array.from(cats).sort();
    }, [itensProcessados]);

    if (!isOpen) return null;

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content selector-modal-content">
                <div className="modal-header">
                    <h3>{titulo}</h3>
                    <button onClick={onClose} className="btn-close-panel">X</button>
                </div>

                <div className="modal-controls">
                    <input
                        type="text"
                        placeholder="🔍 Filtrar..."
                        value={filtro}
                        onChange={(e) => setFiltro(e.target.value)}
                        className="modal-search-input"
                        autoFocus
                    />

                    {!categoriaFixa && categoriasDisponiveis.length > 2 && (
                        <select value={categoriaFiltro} onChange={(e) => setCategoriaFiltro(e.target.value)} className="modal-category-select">
                            {categoriasDisponiveis.map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    )}
                </div>

                <div className="modal-list">
                    {itensExibidos.map((item) => (
                        <PowerListItem
                            key={item.nome}
                            item={item}
                            isBlocked={item.isBlocked}
                            blockReason={item.blockReason}
                            onClick={() => onSelect(item.nome)}
                        />
                    ))}
                    {itensExibidos.length === 0 && <p className="no-results">Nenhuma opção encontrada.</p>}
                </div>

                <div className="modal-footer-info" style={{ marginTop: 10, fontSize: '0.8rem', color: '#666', textAlign: 'right' }}>
                    Mostrando {itensExibidos.length} opções
                </div>
            </div>
        </div>
    );
};