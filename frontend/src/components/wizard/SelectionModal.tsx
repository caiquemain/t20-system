import { useState, useMemo } from 'react';

export interface SelectionItem {
    nome: string;
    descricao?: string;
    tags?: string[];
}

interface SelectionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSelect: (nome: string) => void;
    title: string;
    icon?: string;
    items: SelectionItem[];
    selected?: string;
}

const normalizar = (s: string) =>
    s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

export function SelectionModal({ isOpen, onClose, onSelect, title, icon = '🎯', items, selected }: SelectionModalProps) {
    const [busca, setBusca] = useState('');

    const filtrados = useMemo(() => {
        const termo = normalizar(busca);
        if (!termo) return items;
        return items.filter(i =>
            normalizar(i.nome).includes(termo) ||
            normalizar(i.descricao || '').includes(termo)
        );
    }, [busca, items]);

    if (!isOpen) return null;

    return (
        <div
            style={{
                position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)',
                zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20
            }}
            onClick={onClose}
        >
            <div
                style={{
                    background: '#1e1e1e', border: '1px solid #444', borderRadius: 12,
                    width: '100%', maxWidth: 950, maxHeight: '85vh', display: 'flex', flexDirection: 'column'
                }}
                onClick={e => e.stopPropagation()}
            >
                {/* Header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '18px 24px', borderBottom: '1px solid #333' }}>
                    <h2 style={{ margin: 0, color: '#ffd700', fontSize: '1.3rem' }}>{icon} {title}</h2>
                    <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#888', fontSize: '1.4rem', cursor: 'pointer' }}>✕</button>
                </div>

                {/* Busca */}
                <div style={{ padding: '14px 24px', borderBottom: '1px solid #333' }}>
                    <input
                        autoFocus
                        type="text"
                        placeholder="🔍 Buscar..."
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        style={{
                            width: '100%', padding: '10px 14px', background: '#141414',
                            border: '1px solid #444', borderRadius: 8, color: '#fff', fontSize: '1rem'
                        }}
                    />
                </div>

                {/* Grid de opções */}
                <div style={{ overflowY: 'auto', padding: 24, display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 14 }}>
                    {filtrados.map(item => {
                        const isSel = item.nome === selected;
                        return (
                            <div
                                key={item.nome}
                                onClick={() => { onSelect(item.nome); onClose(); }}
                                style={{
                                    background: isSel ? 'rgba(255,215,0,0.12)' : '#252525',
                                    border: `1px solid ${isSel ? '#ffd700' : '#333'}`,
                                    borderRadius: 10, padding: 16, cursor: 'pointer',
                                    transition: 'all 0.15s ease'
                                }}
                                onMouseEnter={e => { if (!isSel) e.currentTarget.style.borderColor = '#666'; }}
                                onMouseLeave={e => { if (!isSel) e.currentTarget.style.borderColor = '#333'; }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                                    <strong style={{ color: isSel ? '#ffd700' : '#eee', fontSize: '1.05rem' }}>{item.nome}</strong>
                                    {isSel && <span style={{ color: '#ffd700' }}>✓</span>}
                                </div>
                                {item.tags && item.tags.length > 0 && (
                                    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 6 }}>
                                        {item.tags.map(t => (
                                            <span key={t} style={{ fontSize: '0.7rem', background: '#333', color: '#aaa', padding: '2px 8px', borderRadius: 20 }}>{t}</span>
                                        ))}
                                    </div>
                                )}
                                {item.descricao && (
                                    <p style={{ margin: 0, color: '#999', fontSize: '0.85rem', lineHeight: 1.4, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                        {item.descricao}
                                    </p>
                                )}
                            </div>
                        );
                    })}
                    {filtrados.length === 0 && (
                        <p style={{ gridColumn: '1/-1', textAlign: 'center', color: '#666' }}>Nada encontrado para "{busca}".</p>
                    )}
                </div>
            </div>
        </div>
    );
}