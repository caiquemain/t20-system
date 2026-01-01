import React, { useState, useMemo, useEffect, useRef } from 'react';
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
    dadosMagias?: any;
    dadosHabilidades?: any;
    tipoEscolha: string;
    titulo: string;
    listaRestrita?: string[];
    categoriaFixa?: string;
    itensBloqueados?: string[];
    subclasse?: string;
}

export const PowerSelectorModal: React.FC<PowerSelectorModalProps> = ({
    isOpen, onClose, onSelect, ficha, subclasse,
    listaPoderes, listaPericias,
    dadosMagias = {}, dadosHabilidades = {},
    tipoEscolha, titulo,
    listaRestrita = [], categoriaFixa, itensBloqueados = []
}) => {
    const [filtro, setFiltro] = useState('');
    const [categoriaFiltro, setCategoriaFiltro] = useState(categoriaFixa || 'Todos');

    // Estados para Tooltip
    const [hoveredItem, setHoveredItem] = useState<string | null>(null);
    const [tooltipData, setTooltipData] = useState<any | null>(null);
    const hoverTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        if (isOpen) {
            setFiltro('');
            setCategoriaFiltro(categoriaFixa || 'Todos');
            setHoveredItem(null);
            setTooltipData(null);
        }
    }, [isOpen, categoriaFixa]);

    useEffect(() => {
        return () => {
            if (hoverTimeoutRef.current) clearTimeout(hoverTimeoutRef.current);
        };
    }, []);

    // --- TOOLTIP ---
    const handleMouseEnter = (itemNome: string, itemType: string) => {
        if (itemType === 'Magia' && dadosMagias[itemNome]) {
            hoverTimeoutRef.current = setTimeout(() => {
                setHoveredItem(itemNome);
                setTooltipData(dadosMagias[itemNome]);
            }, 1000);
        }
    };

    const handleMouseLeave = () => {
        if (hoverTimeoutRef.current) {
            clearTimeout(hoverTimeoutRef.current);
            hoverTimeoutRef.current = null;
        }
        setHoveredItem(null);
        setTooltipData(null);
    };

    const blacklist = useMemo(() => {
        const set = new Set<string>();
        if (itensBloqueados && itensBloqueados.length > 0) {
            itensBloqueados.forEach(item => {
                if (typeof item === 'string') set.add(item.trim().toLowerCase());
            });
        }
        return set;
    }, [itensBloqueados]);

    // --- PROCESSAMENTO DA LISTA ---
    const itensProcessados = useMemo(() => {
        let itens: any[] = [];

        const formatarItem = (nome: string) => {
            // A. Magias
            if (dadosMagias && dadosMagias[nome]) {
                const m = dadosMagias[nome];
                let cssClass = 'tag-arcane';
                if (m.tipo === 'Divina') cssClass = 'tag-divine';
                if (m.tipo === 'Universal') cssClass = 'tag-universal';

                return {
                    nome, type: 'Magia', categoria: m.tipo || 'Universal',
                    descricao: `${m.escola} • ${m.custo_pm} PM. ${m.descricao}`,
                    tagClass: cssClass, requisitos: [], isBlocked: false, dadosCompletos: m
                };
            }

            // B. Perícias
            if (listaPericias.includes(nome)) {
                return {
                    nome, type: 'Perícia', categoria: 'Perícias',
                    descricao: 'Treinamento em perícia.', tagClass: 'tag-skill',
                    requisitos: [], isBlocked: false
                };
            }

            // C. Poderes (Busca Inteligente)
            let poder = listaPoderes.find(p => p.nome === nome);

            // Se não achou na lista principal, busca no Dicionário Mestre
            if (!poder && dadosHabilidades) {
                // 1. Tenta acesso direto pela chave (caso a chave seja igual ao nome)
                poder = dadosHabilidades[nome];

                // 2. Se falhar, busca varrendo os valores pelo campo 'nome' (CORREÇÃO FUNDAMENTAL)
                if (!poder) {
                    poder = Object.values(dadosHabilidades).find((h: any) => h.nome === nome);
                }
            }

            if (poder) {
                const requisitos = poder.requisitos || [];
                const validacao = validarTodosRequisitos(ficha, requisitos);
                const tipoRaw = (poder.tipo || poder.categoria || "Geral").toString();

                let cssClass = 'tag-power'; // Default Azul
                let catExibicao = 'Geral';

                if (tipoRaw.includes('Origem')) {
                    cssClass = 'tag-origin'; // Laranja
                    catExibicao = 'Origem';
                } else if (tipoRaw.includes('Tormenta')) {
                    cssClass = 'tag-tormenta'; // Vermelho
                    catExibicao = 'Tormenta';
                } else if (tipoRaw.includes('Classe') || tipoRaw.includes('Poder de')) {
                    cssClass = 'tag-class'; // Roxo
                    catExibicao = 'Classe';
                } else if (tipoRaw.includes('Concedido')) {
                    cssClass = 'tag-divine'; // Dourado
                    catExibicao = 'Concedido';
                } else if (tipoRaw.includes('Destino')) {
                    catExibicao = 'Destino';
                } else if (tipoRaw.includes('Combate')) {
                    catExibicao = 'Combate';
                } else if (tipoRaw.includes('Magia')) {
                    catExibicao = 'Magia';
                }

                return {
                    nome,
                    type: 'Poder',
                    categoria: catExibicao,
                    descricao: poder.descricao || "Sem descrição disponível.",
                    tagClass: cssClass,
                    requisitos: requisitos,
                    isBlocked: !validacao.apto,
                    blockReason: validacao.erros
                };
            }

            // E. Fallback
            return {
                nome, type: 'Especial', categoria: 'Outros',
                descricao: 'Habilidade especial não listada.',
                tagClass: 'tag-other', isBlocked: false
            };
        };

        if (listaRestrita && listaRestrita.length > 0) {
            itens = listaRestrita.map(formatarItem);
        } else {
            if (tipoEscolha === 'pericia' || tipoEscolha === 'ambos') {
                itens = itens.concat(listaPericias.map(nome => ({
                    nome, type: 'Perícia', categoria: 'Perícias',
                    descricao: 'Treinamento.', tagClass: 'tag-skill',
                    requisitos: [], isBlocked: false
                })));
            }
            if (tipoEscolha === 'poder' || tipoEscolha === 'ambos') {
                const poderesPermitidos = listaPoderes.filter(p => !p.tipo?.includes('Origem'));
                itens = itens.concat(poderesPermitidos.map(p => formatarItem(p.nome)));
            }
        }

        if (blacklist.size > 0) {
            itens = itens.filter(i => !blacklist.has(i.nome.trim().toLowerCase()));
        }

        return itens.sort((a, b) => a.nome.localeCompare(b.nome));
    }, [listaRestrita, listaPoderes, listaPericias, tipoEscolha, blacklist, ficha, dadosMagias, dadosHabilidades]);

    // Filtragem Visual
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
            <div className="habilidades-panel-content selector-modal-content" style={{ position: 'relative' }}>

                {hoveredItem && tooltipData && (
                    <div className="magic-tooltip" style={{
                        position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
                        width: '320px', background: '#1a1a1a', border: '1px solid #ffd700',
                        padding: '15px', borderRadius: '8px', zIndex: 1300, pointerEvents: 'none',
                        boxShadow: '0 10px 40px rgba(0,0,0,0.9)'
                    }}>
                        <h4 style={{ color: '#ffd700', marginTop: 0, borderBottom: '1px solid #444', marginBottom: 5 }}>
                            {tooltipData.nome}
                        </h4>
                        <div style={{ fontSize: '0.8rem', color: '#ccc', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px', marginBottom: '10px' }}>
                            <span><strong>Círculo:</strong> {tooltipData.circulo}º</span>
                            <span><strong>Custo:</strong> {tooltipData.custo_pm} PM</span>
                        </div>
                        <p style={{ fontSize: '0.85rem', lineHeight: '1.4', color: '#eee' }}>{tooltipData.descricao}</p>
                    </div>
                )}

                <div className="modal-header">
                    <h3>{titulo}</h3>
                    <button onClick={onClose} className="btn-close-panel">X</button>
                </div>

                <div className="modal-controls">
                    <input type="text" placeholder="🔍 Filtrar..." value={filtro}
                        onChange={(e) => setFiltro(e.target.value)} className="modal-search-input" autoFocus />

                    {!categoriaFixa && categoriasDisponiveis.length > 2 && (
                        <select value={categoriaFiltro} onChange={(e) => setCategoriaFiltro(e.target.value)} className="modal-category-select">
                            {categoriasDisponiveis.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                        </select>
                    )}
                </div>

                <div className="modal-list">
                    {itensExibidos.map((item) => (
                        <div key={item.nome} onMouseEnter={() => handleMouseEnter(item.nome, item.type)} onMouseLeave={handleMouseLeave}>
                            <PowerListItem item={item} isBlocked={item.isBlocked} blockReason={item.blockReason} onClick={() => onSelect(item.nome)} />
                        </div>
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