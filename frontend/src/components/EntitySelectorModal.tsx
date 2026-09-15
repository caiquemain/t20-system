import React, { useState, useMemo, useEffect } from 'react';

export interface EntityItem {
    nome: string;
    icone?: string;
    descricao?: string;
    bonus?: string;  // ex: "+2 FOR, +1 CON" ou "Benefícios: 2 escolhas"
    bloqueado?: boolean;  // ex: origem bloqueada pelo Golem
    motivoBloqueio?: string;
}

interface EntitySelectorModalProps {
    aberto: boolean;
    titulo: string;
    iconeTitulo?: string;
    itens: EntityItem[];
    selecionado?: string;
    onConfirm: (nome: string) => void;
    onFechar: () => void;
    permitirVazio?: boolean;
    labelVazio?: string;
}

export const EntitySelectorModal: React.FC<EntitySelectorModalProps> = ({
    aberto, titulo, iconeTitulo, itens, selecionado,
    onConfirm, onFechar, permitirVazio = false, labelVazio = 'Nenhum'
}) => {
    const [busca, setBusca] = useState('');

    // Limpa busca ao fechar
    useEffect(() => { if (!aberto) setBusca(''); }, [aberto]);

    // ESC fecha o modal
    useEffect(() => {
        if (!aberto) return;
        const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onFechar(); };
        window.addEventListener('keydown', handler);
        return () => window.removeEventListener('keydown', handler);
    }, [aberto, onFechar]);

    const itensFiltrados = useMemo(() => {
        if (!busca.trim()) return itens;
        const q = busca.toLowerCase();
        return itens.filter(it =>
            it.nome.toLowerCase().includes(q) ||
            (it.descricao || '').toLowerCase().includes(q) ||
            (it.bonus || '').toLowerCase().includes(q)
        );
    }, [itens, busca]);

    if (!aberto) return null;

    return (
        <div
            className="modal-overlay"
            onClick={(e) => { if (e.target === e.currentTarget) onFechar(); }}
            style={{
                position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                background: 'rgba(0,0,0,0.85)', display: 'flex',
                alignItems: 'center', justifyContent: 'center', zIndex: 2000,
                padding: 20
            }}
        >
            <div style={{
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
                border: '1px solid #3a3a5a', borderRadius: 12,
                width: '100%', maxWidth: 900, maxHeight: '85vh',
                display: 'flex', flexDirection: 'column',
                boxShadow: '0 20px 60px rgba(0,0,0,0.8)'
            }}>
                {/* Header */}
                <div style={{
                    padding: '16px 20px', borderBottom: '1px solid #2a2a4a',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    gap: 12, flexWrap: 'wrap'
                }}>
                    <h2 style={{ margin: 0, color: '#ffd700', fontSize: '1.3rem', fontFamily: 'Tormenta, serif' }}>
                        {iconeTitulo && <span style={{ marginRight: 8 }}>{iconeTitulo}</span>}
                        {titulo}
                    </h2>
                    <input
                        type="text"
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        placeholder="🔍 Buscar..."
                        autoFocus
                        className="input-dark"
                        style={{ flex: 1, maxWidth: 300, minWidth: 180 }}
                    />
                    <button
                        onClick={onFechar}
                        style={{
                            background: 'transparent', border: '1px solid #555',
                            color: '#aaa', borderRadius: 6, padding: '6px 12px',
                            cursor: 'pointer', fontSize: '1rem'
                        }}
                    >✕</button>
                </div>

                {/* Grid de cards */}
                <div style={{
                    padding: 20, overflowY: 'auto', flex: 1,
                    display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
                    gap: 12
                }}>
                    {permitirVazio && (
                        <div
                            onClick={() => onConfirm('')}
                            style={{
                                background: !selecionado ? 'rgba(255,215,0,0.15)' : 'rgba(40,40,60,0.5)',
                                border: !selecionado ? '2px solid #ffd700' : '1px solid #444',
                                borderRadius: 8, padding: 14, cursor: 'pointer',
                                transition: 'all 0.2s',
                                display: 'flex', alignItems: 'center', gap: 10
                            }}
                        >
                            <span style={{ fontSize: '1.5rem' }}>—</span>
                            <span style={{ color: '#ccc', fontSize: '0.95rem' }}>{labelVazio}</span>
                            {!selecionado && <span style={{ marginLeft: 'auto', color: '#ffd700' }}>✓</span>}
                        </div>
                    )}
                    {itensFiltrados.map(it => {
                        const isSel = selecionado === it.nome;
                        return (
                            <div
                                key={it.nome}
                                onClick={() => !it.bloqueado && onConfirm(it.nome)}
                                style={{
                                    background: isSel ? 'rgba(255,215,0,0.15)' : 'rgba(40,40,60,0.5)',
                                    border: isSel ? '2px solid #ffd700' : '1px solid #444',
                                    borderRadius: 8, padding: 14,
                                    cursor: it.bloqueado ? 'not-allowed' : 'pointer',
                                    opacity: it.bloqueado ? 0.45 : 1,
                                    transition: 'all 0.2s',
                                    display: 'flex', flexDirection: 'column', gap: 4
                                }}
                                onMouseEnter={e => { if (!it.bloqueado) (e.currentTarget as HTMLDivElement).style.transform = 'translateY(-2px)'; }}
                                onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.transform = 'translateY(0)'; }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                    {it.icone && <span style={{ fontSize: '1.4rem' }}>{it.icone}</span>}
                                    <span style={{
                                        color: isSel ? '#ffd700' : '#e0e0e0',
                                        fontWeight: 'bold', fontSize: '1.05rem',
                                        fontFamily: 'Tormenta, serif'
                                    }}>
                                        {it.nome}
                                    </span>
                                    {isSel && <span style={{ marginLeft: 'auto', color: '#ffd700' }}>✓</span>}
                                </div>
                                {it.bonus && (
                                    <div style={{ color: '#8be9fd', fontSize: '0.8rem', marginTop: 2 }}>
                                        {it.bonus}
                                    </div>
                                )}
                                {it.descricao && (
                                    <div style={{ color: '#999', fontSize: '0.78rem', lineHeight: 1.3, marginTop: 2 }}>
                                        {it.descricao}
                                    </div>
                                )}
                                {it.bloqueado && it.motivoBloqueio && (
                                    <div style={{ color: '#ff5252', fontSize: '0.75rem', marginTop: 4 }}>
                                        🚫 {it.motivoBloqueio}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                    {itensFiltrados.length === 0 && (
                        <div style={{ gridColumn: '1/-1', textAlign: 'center', color: '#777', padding: 40 }}>
                            Nenhum item encontrado para "{busca}"
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div style={{
                    padding: '12px 20px', borderTop: '1px solid #2a2a4a',
                    display: 'flex', justifyContent: 'space-between',
                    alignItems: 'center', fontSize: '0.85rem', color: '#888'
                }}>
                    <span>{itensFiltrados.length} de {itens.length} itens</span>
                    <span>ESC ou clique fora para fechar</span>
                </div>
            </div>
        </div>
    );
};
