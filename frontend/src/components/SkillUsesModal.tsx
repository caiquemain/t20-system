import React, { useState, useEffect } from 'react';
import { DADOS_PERICIAS_FRONTEND, type UsoPericia } from '../data/pericias';
import { T20Icon } from './T20Icon';

interface SkillUsesModalProps {
    pericia: string | null;
    total: number;
    treinada: boolean;
    atributoAtual: string;
    onClose: () => void;
}

interface ResultadoRolagem {
    uso: string;
    d20: number;
    bonus: number;
    total: number;
}

export const SkillUsesModal: React.FC<SkillUsesModalProps> = ({
    pericia,
    total,
    treinada,
    atributoAtual,
    onClose,
}) => {
    const [rolagem, setRolagem] = useState<ResultadoRolagem | null>(null);

    useEffect(() => {
        setRolagem(null);
    }, [pericia]);

    useEffect(() => {
        if (!pericia) return;
        const onKey = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose();
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [pericia, onClose]);

    if (!pericia) return null;

    const chaveBase = pericia.startsWith('Ofício') ? 'Ofício' : pericia;
    const meta = DADOS_PERICIAS_FRONTEND[chaveBase];
    const usos: UsoPericia[] = meta?.usos || [];

    const rolar = (nomeUso: string) => {
        const d20 = Math.floor(Math.random() * 20) + 1;
        setRolagem({
            uso: nomeUso,
            d20,
            bonus: total,
            total: d20 + total,
        });
    };

    const bloqueadaGlobal = Boolean(meta?.treino_apenas && !treinada);

    return (
        <div
            onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
            style={{
                position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.82)',
                zIndex: 2100, display: 'flex', alignItems: 'center', justifyContent: 'center',
                padding: 16
            }}
        >
            <div style={{
                background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
                border: '1px solid #3a3a5a', borderRadius: 12,
                width: '100%', maxWidth: 680, maxHeight: '85vh',
                display: 'flex', flexDirection: 'column',
                boxShadow: '0 20px 60px rgba(0,0,0,0.85)'
            }}>
                {/* Header */}
                <div style={{
                    padding: '14px 18px', borderBottom: '1px solid #2a2a4a',
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 10
                }}>
                    <div>
                        <h3 style={{ margin: 0, color: '#ffd700', fontSize: '1.15rem', display: 'flex', alignItems: 'center', gap: 8 }}>
                            <T20Icon name="pericia" size={18} color="#ffd700" />
                            {pericia}
                            <span style={{
                                fontSize: '0.85rem', background: 'rgba(255,215,0,0.15)',
                                border: '1px solid #ffd700', borderRadius: 6, padding: '1px 8px', color: '#ffd700'
                            }}>
                                {total >= 0 ? `+${total}` : total}
                            </span>
                        </h3>
                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 6 }}>
                            <span style={{ fontSize: '0.7rem', background: '#263238', color: '#90caf9', padding: '2px 7px', borderRadius: 12 }}>
                                Atributo: {atributoAtual.toUpperCase()}
                            </span>
                            <span style={{
                                fontSize: '0.7rem',
                                background: treinada ? 'rgba(76,175,80,0.2)' : 'rgba(158,158,158,0.15)',
                                color: treinada ? '#a5d6a7' : '#aaa',
                                padding: '2px 7px', borderRadius: 12
                            }}>
                                {treinada ? 'Treinada' : 'Não treinada'}
                            </span>
                            {meta?.treino_apenas && (
                                <span style={{ fontSize: '0.7rem', background: 'rgba(255,183,77,0.18)', color: '#ffb74d', padding: '2px 7px', borderRadius: 12 }}>
                                    Somente Treinada
                                </span>
                            )}
                            {meta?.penalidade_armadura && (
                                <span style={{ fontSize: '0.7rem', background: 'rgba(239,83,80,0.18)', color: '#ef9a9a', padding: '2px 7px', borderRadius: 12 }}>
                                    Penalidade de Armadura
                                </span>
                            )}
                        </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <button
                            disabled={bloqueadaGlobal}
                            onClick={() => rolar('Teste Geral')}
                            style={{
                                background: bloqueadaGlobal ? '#333' : '#ffd700',
                                color: bloqueadaGlobal ? '#777' : '#111',
                                border: 'none', borderRadius: 6, padding: '6px 12px',
                                fontWeight: 'bold', fontSize: '0.8rem',
                                cursor: bloqueadaGlobal ? 'not-allowed' : 'pointer',
                                display: 'inline-flex', alignItems: 'center', gap: 5
                            }}
                            title={bloqueadaGlobal ? 'Requer treinamento nesta perícia' : `Rolar 1d20 ${total >= 0 ? `+ ${total}` : total}`}
                        >
                            <T20Icon name="dado" size={14} /> Rolar
                        </button>
                        <button
                            onClick={onClose}
                            title="Fechar"
                            style={{
                                background: 'transparent', border: '1px solid #555',
                                color: '#aaa', borderRadius: 6, padding: '6px 8px',
                                cursor: 'pointer', display: 'inline-flex', alignItems: 'center'
                            }}
                        >
                            <T20Icon name="fechar" size={15} />
                        </button>
                    </div>
                </div>

                {/* Resultado da Rolagem */}
                {rolagem && (
                    <div style={{
                        padding: '10px 18px',
                        background: rolagem.d20 === 20
                            ? 'rgba(255,215,0,0.18)'
                            : rolagem.d20 === 1
                                ? 'rgba(239,83,80,0.18)'
                                : 'rgba(33,150,243,0.15)',
                        borderBottom: '1px solid #2a2a4a',
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 10
                    }}>
                        <div style={{ fontSize: '0.88rem', color: '#eee' }}>
                            <strong style={{ color: '#ffd700' }}>{rolagem.uso}</strong> ({pericia}):
                            {' '}d20(<strong style={{ color: rolagem.d20 === 20 ? '#ffd700' : rolagem.d20 === 1 ? '#ff5252' : '#fff' }}>{rolagem.d20}</strong>)
                            {' '}{rolagem.bonus >= 0 ? `+ ${rolagem.bonus}` : `- ${Math.abs(rolagem.bonus)}`}
                            {rolagem.d20 === 20 && <span style={{ color: '#ffd700', marginLeft: 8, fontWeight: 'bold' }}>★ NATURAL 20!</span>}
                            {rolagem.d20 === 1 && <span style={{ color: '#ff5252', marginLeft: 8, fontWeight: 'bold' }}>✕ NATURAL 1!</span>}
                        </div>
                        <div style={{
                            fontSize: '1.25rem', fontWeight: 'bold',
                            color: rolagem.d20 === 20 ? '#ffd700' : rolagem.d20 === 1 ? '#ff5252' : '#4fc3f7'
                        }}>
                            = {rolagem.total}
                        </div>
                    </div>
                )}

                {/* Corpo: Resumo + Nota + Lista de Usos */}
                <div style={{ padding: 18, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {meta?.resumo && (
                        <p style={{ margin: 0, fontSize: '0.85rem', color: '#bbb' }}>{meta.resumo}</p>
                    )}
                    {meta?.nota && (
                        <div style={{
                            padding: '8px 12px', borderRadius: 6,
                            background: 'rgba(255,193,7,0.1)', border: '1px solid rgba(255,193,7,0.35)',
                            color: '#ffe082', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 6
                        }}>
                            <T20Icon name="alerta" size={14} color="#ffc107" /> {meta.nota}
                        </div>
                    )}

                    {usos.map((uso) => {
                        const bloqueado = (uso.apenas_treinado || meta?.treino_apenas) && !treinada;
                        return (
                            <div
                                key={uso.nome}
                                style={{
                                    background: bloqueado ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.04)',
                                    border: `1px solid ${bloqueado ? '#2d2d3d' : '#3a3a5a'}`,
                                    borderRadius: 8, padding: 12,
                                    opacity: bloqueado ? 0.6 : 1,
                                    display: 'flex', flexDirection: 'column', gap: 6
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                                        <strong style={{ color: bloqueado ? '#999' : '#fff', fontSize: '0.95rem' }}>{uso.nome}</strong>
                                        {uso.acao && uso.acao !== '—' && (
                                            <span style={{ fontSize: '0.7rem', background: '#263238', color: '#80cbc4', padding: '2px 7px', borderRadius: 10 }}>
                                                Ação: {uso.acao}
                                            </span>
                                        )}
                                        {uso.cd && (
                                            <span style={{ fontSize: '0.7rem', background: 'rgba(100,181,246,0.15)', color: '#90caf9', padding: '2px 7px', borderRadius: 10 }}>
                                                {uso.cd}
                                            </span>
                                        )}
                                        {uso.apenas_treinado && (
                                            <span style={{ fontSize: '0.7rem', background: 'rgba(255,183,77,0.15)', color: '#ffb74d', padding: '2px 7px', borderRadius: 10 }}>
                                                Apenas Treinado
                                            </span>
                                        )}
                                    </div>
                                    <button
                                        disabled={bloqueado}
                                        onClick={() => rolar(uso.nome)}
                                        style={{
                                            background: bloqueado ? '#2a2a2a' : 'rgba(255,215,0,0.16)',
                                            border: `1px solid ${bloqueado ? '#444' : '#ffd700'}`,
                                            color: bloqueado ? '#777' : '#ffd700',
                                            borderRadius: 6, padding: '4px 10px',
                                            fontSize: '0.75rem', fontWeight: 'bold',
                                            cursor: bloqueado ? 'not-allowed' : 'pointer',
                                            display: 'inline-flex', alignItems: 'center', gap: 4
                                        }}
                                        title={bloqueado ? 'Requer treinamento nesta perícia' : `Usar ${uso.nome} (1d20 ${total >= 0 ? `+ ${total}` : total})`}
                                    >
                                        <T20Icon name="dado" size={12} /> {bloqueado ? 'Requer Treino' : 'Usar / Rolar'}
                                    </button>
                                </div>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: '#ccc', lineHeight: 1.4 }}>
                                    {uso.descricao}
                                </p>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};
