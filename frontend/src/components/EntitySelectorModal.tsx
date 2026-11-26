import React, { useState, useMemo, useEffect } from 'react';
import { T20Icon, type IconName } from './T20Icon';
import { EntityDetailPanel } from './EntityDetailPanel';
import { useEscapeKey } from '../hooks/useEscapeKey';

export interface EntityItem {
    nome: string;
    tooltip?: string;
    icone?: IconName;
    descricao?: string;
    bonus?: string;  // ex: "+2 FOR, +1 CON" ou "Benefícios: 2 escolhas"
    bloqueado?: boolean;  // ex: origem bloqueada pelo Golem
    motivoBloqueio?: string;
}

interface EntitySelectorModalProps {
    aberto: boolean;
    titulo: string;
    iconeTitulo?: IconName;
    itens: EntityItem[];
    selecionado?: string;
    onConfirm: (nome: string) => void;
    onFechar: () => void;
    permitirVazio?: boolean;
    labelVazio?: string;
}

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

export const EntitySelectorModal: React.FC<EntitySelectorModalProps> = ({
    aberto, titulo, iconeTitulo, itens, selecionado,
    onConfirm, onFechar, permitirVazio = false, labelVazio = 'Nenhum'
}) => {
    const [busca, setBusca] = useState('');
    const [hoveredItem, setHoveredItem] = useState<EntityItem | null>(null);

    useEscapeKey(aberto, onFechar);

    useEffect(() => {
        if (!aberto) {
            setBusca('');
            setHoveredItem(null);
        }
    }, [aberto]);

    const itensFiltrados = useMemo(() => {
        if (!busca.trim()) return itens;
        const q = busca.toLowerCase();
        return itens.filter(it =>
            it.nome.toLowerCase().includes(q) ||
            (it.descricao || '').toLowerCase().includes(q) ||
            (it.bonus || '').toLowerCase().includes(q)
        );
    }, [itens, busca]);

    const temDetalhesRicos = useMemo(
        () => itens.some(it => Boolean(it.tooltip)),
        [itens]
    );

    const itemEmFoco = hoveredItem
        || itensFiltrados.find(i => i.nome === selecionado)
        || itensFiltrados[0]
        || null;

    if (!aberto) return null;

    return (
        <div
            className="modal-overlay"
            onClick={(e) => { if (e.target === e.currentTarget) onFechar(); }}
            style={{
                position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                background: 'rgba(0,0,0,0.85)', display: 'flex',
                alignItems: 'center', justifyContent: 'center', zIndex: 2000,
                padding: 20,
            }}
        >
            <div style={{
                background: 'linear-gradient(135deg, #161829 0%, #111526 100%)',
                border: '1px solid #32385a', borderRadius: 12,
                width: '100%', maxWidth: temDetalhesRicos ? 1080 : 900,
                height: '82vh', maxHeight: 740,
                display: 'flex', flexDirection: 'column',
                overflow: 'hidden',
                boxShadow: '0 24px 64px rgba(0,0,0,0.85)',
            }}>
                {/* Header */}
                <div style={{
                    padding: '14px 20px', borderBottom: '1px solid #262b45',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    gap: 12, flexWrap: 'wrap',
                    background: 'rgba(12, 14, 24, 0.6)',
                }}>
                    <h2 style={{ margin: 0, color: '#ffd700', fontSize: '1.25rem', fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                        {iconeTitulo && <T20Icon name={iconeTitulo} size={20} color="#ffd700" />}
                        {titulo}
                    </h2>
                    <input
                        type="text"
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        placeholder="Buscar..."
                        autoFocus
                        className="input-dark"
                        style={{ flex: 1, maxWidth: 320, minWidth: 180, fontFamily: FONT_BODY, textTransform: 'none' }}
                    />
                    <button
                        onClick={onFechar}
                        title="Fechar (ESC)"
                        style={{
                            background: 'transparent', border: '1px solid #444b6e',
                            color: '#cbd5e1', borderRadius: 6, padding: '6px 10px',
                            cursor: 'pointer', display: 'inline-flex', alignItems: 'center',
                        }}
                    ><T20Icon name="fechar" size={16} /></button>
                </div>

                {/* Corpo Master-Detail */}
                <div style={{ display: 'flex', flex: 1, minHeight: 0, overflow: 'hidden' }}>
                    {/* Coluna Esquerda: Grid de Cards */}
                    <div style={{
                        padding: 18, overflowY: 'auto', flex: 1,
                        display: 'grid',
                        gridTemplateColumns: temDetalhesRicos
                            ? 'repeat(auto-fill, minmax(215px, 1fr))'
                            : 'repeat(auto-fill, minmax(240px, 1fr))',
                        gap: 10,
                        alignContent: 'start',
                        fontFamily: FONT_BODY,
                        textTransform: 'none',
                    }}>
                        {permitirVazio && (
                            <div
                                onClick={() => onConfirm('')}
                                style={{
                                    background: !selecionado ? 'rgba(255,215,0,0.14)' : 'rgba(30,34,54,0.55)',
                                    border: !selecionado ? '2px solid #ffd700' : '1px solid #32385a',
                                    borderRadius: 8, padding: 12, cursor: 'pointer',
                                    transition: 'border-color 0.15s, background 0.15s',
                                    display: 'flex', alignItems: 'center', gap: 10,
                                }}
                            >
                                <span style={{ fontSize: '1.2rem', color: '#94a3b8' }}>—</span>
                                <span style={{ color: '#e2e8f0', fontSize: '0.9rem', fontWeight: 600 }}>{labelVazio}</span>
                                {!selecionado && <span style={{ marginLeft: 'auto', color: '#ffd700' }}><T20Icon name="check" size={16} /></span>}
                            </div>
                        )}
                        {itensFiltrados.map(it => {
                            const isSel = selecionado === it.nome;
                            const isHover = itemEmFoco?.nome === it.nome;
                            return (
                                <div
                                    key={it.nome}
                                    onClick={() => !it.bloqueado && onConfirm(it.nome)}
                                    onMouseEnter={() => setHoveredItem(it)}
                                    style={{
                                        background: isSel
                                            ? 'rgba(255, 215, 0, 0.13)'
                                            : isHover
                                                ? 'rgba(56, 65, 102, 0.55)'
                                                : 'rgba(26, 30, 48, 0.72)',
                                        border: isSel
                                            ? '2px solid #ffd700'
                                            : isHover
                                                ? '1px solid #6366f1'
                                                : '1px solid #2d3352',
                                        borderRadius: 8, padding: 12,
                                        cursor: it.bloqueado ? 'not-allowed' : 'pointer',
                                        opacity: it.bloqueado ? 0.45 : 1,
                                        transition: 'border-color 0.15s, background 0.15s',
                                        display: 'flex', flexDirection: 'column', gap: 5,
                                    }}
                                >
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
                                        {it.icone && <T20Icon name={it.icone} size={16} color={isSel ? '#ffd700' : '#94a3b8'} />}
                                        <span style={{
                                            color: isSel ? '#ffd700' : '#f1f5f9',
                                            fontWeight: 700, fontSize: '0.98rem',
                                            fontFamily: 'Tormenta, serif',
                                            letterSpacing: '0.02em',
                                        }}>
                                            {it.nome}
                                        </span>
                                        {isSel && <span style={{ marginLeft: 'auto', color: '#ffd700' }}><T20Icon name="check" size={15} /></span>}
                                    </div>
                                    {it.bonus && (
                                        <div style={{ color: '#7dd3fc', fontSize: '0.76rem', fontWeight: 500, lineHeight: 1.35 }}>
                                            {it.bonus}
                                        </div>
                                    )}
                                    {it.descricao && (
                                        <div style={{
                                            color: '#94a3b8', fontSize: '0.76rem', lineHeight: 1.4,
                                            display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden',
                                        }}>
                                            {it.descricao}
                                        </div>
                                    )}
                                    {it.bloqueado && it.motivoBloqueio && (
                                        <div style={{ color: '#f87171', fontSize: '0.74rem', marginTop: 2, display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                                            <T20Icon name="imunidade" size={12} /> {it.motivoBloqueio}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                        {itensFiltrados.length === 0 && (
                            <div style={{ gridColumn: '1/-1', textAlign: 'center', color: '#94a3b8', padding: 40 }}>
                                Nenhum item encontrado para "{busca}"
                            </div>
                        )}
                    </div>

                    {/* Coluna Direita: Painel de Detalhes Estruturado */}
                    {temDetalhesRicos && itemEmFoco && (
                        <EntityDetailPanel
                            nome={itemEmFoco.nome}
                            icone={itemEmFoco.icone}
                            bonus={itemEmFoco.bonus}
                            descricao={itemEmFoco.descricao}
                            tooltip={itemEmFoco.tooltip}
                            bloqueado={itemEmFoco.bloqueado}
                            motivoBloqueio={itemEmFoco.motivoBloqueio}
                            selecionado={selecionado === itemEmFoco.nome}
                            onConfirm={() => onConfirm(itemEmFoco.nome)}
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
                    <span>{itensFiltrados.length} de {itens.length} itens</span>
                    <span>Passe o mouse para ver detalhes • Clique para escolher • ESC para fechar</span>
                </div>
            </div>
        </div>
    );
};
