import { useState, useMemo, useEffect } from 'react';
import { T20Icon, type IconName } from '../T20Icon';
import { EntityDetailPanel } from '../EntityDetailPanel';
import { useEscapeKey } from '../../hooks/useEscapeKey';
import { obterInfoSuplemento } from '../../utils/suplementos';

export interface SelectionItem {
    nome: string;
    descricao?: string;
    tags?: string[];
    tooltip?: string;
    fonte?: string;
}

interface SelectionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSelect: (nome: string) => void;
    title: string;
    icon?: IconName;
    items: SelectionItem[];
    selected?: string;
}

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

const normalizar = (s: string) =>
    s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

export function SelectionModal({ isOpen, onClose, onSelect, title, icon = 'arco', items, selected }: SelectionModalProps) {
    const [busca, setBusca] = useState('');
    const [filtroFonte, setFiltroFonte] = useState<string>('TODOS');
    const [hoveredItem, setHoveredItem] = useState<SelectionItem | null>(null);
    useEscapeKey(isOpen, onClose);

    useEffect(() => {
        if (!isOpen) {
            setBusca('');
            setFiltroFonte('TODOS');
            setHoveredItem(null);
        }
    }, [isOpen]);

    const fontesDisponiveis = useMemo(() => {
        const set = new Set<string>();
        items.forEach(it => {
            if (it.fonte) set.add(it.fonte);
        });
        return Array.from(set);
    }, [items]);

    const filtrados = useMemo(() => {
        const termo = normalizar(busca);
        return items.filter(i => {
            if (filtroFonte !== 'TODOS' && i.nome !== '' && (i.fonte || 'T20 JdA') !== filtroFonte) return false;
            if (!termo) return true;
            return (
                normalizar(i.nome).includes(termo) ||
                normalizar(i.descricao || '').includes(termo) ||
                normalizar(i.tooltip || '').includes(termo) ||
                normalizar(i.fonte || '').includes(termo)
            );
        });
    }, [busca, items, filtroFonte]);

    const temDetalhesRicos = useMemo(
        () => items.some(it => Boolean(it.tooltip)),
        [items]
    );

    const itemEmFoco = hoveredItem
        || filtrados.find(i => i.nome === selected)
        || filtrados[0]
        || null;

    if (!isOpen) return null;

    return (
        <div
            style={{
                position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.82)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                zIndex: 1000, padding: 20,
            }}
            onClick={onClose}
        >
            <div
                style={{
                    background: 'linear-gradient(135deg, #161829 0%, #111526 100%)',
                    border: '1px solid #32385a', borderRadius: 12,
                    width: '100%', maxWidth: temDetalhesRicos ? 1040 : 760,
                    height: '80vh', maxHeight: 720,
                    display: 'flex', flexDirection: 'column', overflow: 'hidden',
                    boxShadow: '0 24px 64px rgba(0,0,0,0.85)',
                }}
                onClick={e => e.stopPropagation()}
            >
                {/* Header */}
                <div style={{ padding: '14px 20px', borderBottom: '1px solid #262b45', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, background: 'rgba(12, 14, 24, 0.6)' }}>
                    <h3 style={{ margin: 0, color: '#ffd700', fontSize: '1.15rem', fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                        <T20Icon name={icon} size={18} color="#ffd700" /> {title}
                    </h3>
                    <input
                        type="text"
                        placeholder="Buscar..."
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        autoFocus
                        style={{
                            flex: 1, maxWidth: 280, padding: '8px 12px',
                            background: '#0f1220', border: '1px solid #32385a',
                            borderRadius: 6, color: '#fff', fontSize: '0.88rem',
                            fontFamily: FONT_BODY, textTransform: 'none',
                        }}
                    />
                    <button
                        onClick={onClose}
                        title="Fechar (ESC)"
                        style={{ background: 'transparent', border: '1px solid #444b6e', color: '#cbd5e1', borderRadius: 6, padding: '6px 10px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center' }}
                    >
                        <T20Icon name="fechar" size={16} />
                    </button>
                </div>

                {/* Barra de Filtro por Livro */}
                {fontesDisponiveis.length > 1 && (
                    <div style={{
                        padding: '8px 18px',
                        borderBottom: '1px solid #222742',
                        display: 'flex',
                        gap: 6,
                        flexWrap: 'wrap',
                        alignItems: 'center',
                        background: 'rgba(10, 12, 22, 0.45)',
                        fontFamily: FONT_BODY,
                        textTransform: 'none',
                    }}>
                        <span style={{ fontSize: '0.72rem', color: '#94a3b8', marginRight: 4 }}>Livro:</span>
                        <button
                            type="button"
                            onClick={() => setFiltroFonte('TODOS')}
                            style={{
                                fontSize: '0.72rem',
                                padding: '3px 10px',
                                borderRadius: 999,
                                cursor: 'pointer',
                                border: filtroFonte === 'TODOS' ? '1px solid #ffd700' : '1px solid #32385a',
                                background: filtroFonte === 'TODOS' ? 'rgba(255,215,0,0.18)' : 'transparent',
                                color: filtroFonte === 'TODOS' ? '#ffd700' : '#cbd5e1',
                                fontWeight: filtroFonte === 'TODOS' ? 700 : 500,
                            }}
                        >
                            Todos
                        </button>
                        {fontesDisponiveis.map(f => {
                            const info = obterInfoSuplemento(f);
                            const ativo = filtroFonte === f;
                            return (
                                <button
                                    key={f}
                                    type="button"
                                    onClick={() => setFiltroFonte(f)}
                                    style={{
                                        fontSize: '0.72rem',
                                        padding: '3px 10px',
                                        borderRadius: 999,
                                        cursor: 'pointer',
                                        border: `1px solid ${ativo ? info.cor : '#32385a'}`,
                                        background: ativo ? `${info.cor}44` : 'transparent',
                                        color: ativo ? '#fff' : '#cbd5e1',
                                        fontWeight: ativo ? 700 : 500,
                                    }}
                                >
                                    {info.sigla}
                                </button>
                            );
                        })}
                    </div>
                )}

                {/* Corpo Master-Detail */}
                <div style={{ display: 'flex', flex: 1, minHeight: 0, overflow: 'hidden' }}>
                    <div style={{
                        flex: 1, overflowY: 'auto', padding: 16,
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))',
                        gap: 10, alignContent: 'start',
                        fontFamily: FONT_BODY, textTransform: 'none',
                    }}>
                        {filtrados.map(item => {
                            const isSel = selected === item.nome;
                            const isHover = itemEmFoco?.nome === item.nome;
                            const infoFonte = item.fonte && item.fonte !== 'T20 JdA' ? obterInfoSuplemento(item.fonte) : null;
                            return (
                                <button
                                    key={item.nome}
                                    type="button"
                                    onClick={() => { onSelect(item.nome); onClose(); }}
                                    onMouseEnter={() => setHoveredItem(item)}
                                    style={{
                                        textAlign: 'left',
                                        padding: 12,
                                        background: isSel
                                            ? 'rgba(255, 215, 0, 0.14)'
                                            : isHover
                                                ? 'rgba(56, 65, 102, 0.55)'
                                                : 'rgba(26, 30, 48, 0.72)',
                                        border: isSel
                                            ? '2px solid #ffd700'
                                            : isHover
                                                ? '1px solid #6366f1'
                                                : '1px solid #2d3352',
                                        borderRadius: 8,
                                        cursor: 'pointer',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: 5,
                                        transition: 'border-color 0.15s, background 0.15s',
                                    }}
                                >
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, width: '100%' }}>
                                        <span style={{ color: isSel ? '#ffd700' : '#f1f5f9', fontWeight: 700, fontSize: '0.96rem', fontFamily: 'Tormenta, serif' }}>
                                            {item.nome || 'Sem seleção'}
                                        </span>
                                        {infoFonte && (
                                            <span style={{
                                                marginLeft: 'auto',
                                                fontSize: '0.62rem',
                                                fontWeight: 700,
                                                padding: '1px 6px',
                                                borderRadius: 999,
                                                background: `${infoFonte.cor}33`,
                                                border: `1px solid ${infoFonte.cor}`,
                                                color: '#e2e8f0',
                                                flexShrink: 0,
                                            }}>
                                                {infoFonte.sigla}
                                            </span>
                                        )}
                                    </div>
                                    {item.descricao && (
                                        <div style={{ color: '#94a3b8', fontSize: '0.76rem', lineHeight: 1.4, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                            {item.descricao}
                                        </div>
                                    )}
                                    {item.tags && item.tags.length > 0 && (
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 2 }}>
                                            {item.tags.slice(0, 3).map(t => (
                                                <span key={t} style={{ fontSize: '0.68rem', padding: '2px 6px', borderRadius: 4, background: 'rgba(125,211,252,0.12)', color: '#7dd3fc' }}>
                                                    {t}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </button>
                            );
                        })}
                        {filtrados.length === 0 && (
                            <p style={{ gridColumn: '1/-1', color: '#94a3b8', textAlign: 'center', marginTop: 30 }}>
                                Nenhum item encontrado para "{busca}".
                            </p>
                        )}
                    </div>

                    {temDetalhesRicos && itemEmFoco && (
                        <EntityDetailPanel
                            nome={itemEmFoco.nome}
                            icone={icon}
                            descricao={itemEmFoco.descricao}
                            tooltip={itemEmFoco.tooltip}
                            fonte={itemEmFoco.fonte}
                            selecionado={selected === itemEmFoco.nome}
                            onConfirm={() => { onSelect(itemEmFoco.nome); onClose(); }}
                        />
                    )}
                </div>

                {/* Footer */}
                <div style={{
                    padding: '10px 20px', borderTop: '1px solid #262b45',
                    display: 'flex', justifyContent: 'space-between',
                    alignItems: 'center', fontSize: '0.78rem', color: '#94a3b8',
                    fontFamily: FONT_BODY, textTransform: 'none',
                    background: 'rgba(12, 14, 24, 0.6)',
                }}>
                    <span>{filtrados.length} de {items.length} itens</span>
                    <span>Passe o mouse para ver detalhes • ESC para fechar</span>
                </div>
            </div>
        </div>
    );
}