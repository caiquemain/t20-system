import React from 'react';
import { T20Icon, type IconName } from './T20Icon';

interface EntityDetailPanelProps {
    nome: string;
    icone?: IconName;
    bonus?: string;
    descricao?: string;
    tooltip?: string;
    bloqueado?: boolean;
    motivoBloqueio?: string;
    selecionado?: boolean;
    onConfirm?: () => void;
}

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

/**
 * Painel lateral de detalhes ricos para EntitySelectorModal e SelectionModal.
 * Interpreta automaticamente linhas estruturadas (ex.: Deuses: Energia, Arma, Símbolo,
 * Poderes Concedidos, Crenças e Objetivos, Obrigações & Restrições) com tipografia legível.
 */
export const EntityDetailPanel: React.FC<EntityDetailPanelProps> = ({
    nome,
    icone,
    bonus,
    descricao,
    tooltip,
    bloqueado,
    motivoBloqueio,
    selecionado,
    onConfirm,
}) => {
    const linhas = (tooltip || '').split('\n').map(l => l.trim()).filter(Boolean);

    let subtitulo = '';
    const badges: Array<{ label: string; value: string; color: string }> = [];
    let simbolo = '';
    let poderes: string[] = [];
    let crencas = '';
    let obrigacoes = '';
    const extras: string[] = [];

    linhas.forEach((linha, idx) => {
        if (idx === 0 && linha.includes('—')) {
            subtitulo = linha.split('—').slice(1).join('—').trim();
            return;
        }
        if (idx === 0 && linha.toLowerCase() === nome.toLowerCase()) {
            return;
        }
        if (linha.startsWith('Energia:')) {
            const partes = linha.split('|').map(p => p.trim());
            partes.forEach(p => {
                const [k, ...rest] = p.split(':');
                const v = rest.join(':').trim();
                if (!v) return;
                const kLow = k.trim().toLowerCase();
                let color = '#8be9fd';
                if (kLow.includes('energia')) {
                    color = v.toLowerCase().includes('negat') ? '#ef9a9a' : v.toLowerCase().includes('posit') ? '#ffe082' : '#ce93d8';
                }
                badges.push({ label: k.trim(), value: v, color });
            });
            return;
        }
        if (linha.startsWith('Símbolo Sagrado:')) {
            simbolo = linha.replace('Símbolo Sagrado:', '').trim();
            return;
        }
        if (linha.startsWith('Poderes Concedidos:')) {
            poderes = linha.replace('Poderes Concedidos:', '').split(',').map(p => p.trim()).filter(Boolean);
            return;
        }
        if (linha.startsWith('Crenças e Objetivos:')) {
            crencas = linha.replace('Crenças e Objetivos:', '').trim();
            return;
        }
        if (linha.startsWith('Obrigações & Restrições:')) {
            obrigacoes = linha.replace('Obrigações & Restrições:', '').trim();
            return;
        }
        extras.push(linha);
    });

    return (
        <div
            style={{
                width: 340,
                flexShrink: 0,
                borderLeft: '1px solid #2a2f4a',
                background: 'linear-gradient(180deg, rgba(13, 16, 30, 0.96) 0%, rgba(18, 22, 38, 0.98) 100%)',
                display: 'flex',
                flexDirection: 'column',
                fontFamily: FONT_BODY,
                textTransform: 'none',
            }}
        >
            <div style={{ padding: '18px 18px 14px', overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: 14 }}>
                {/* Título */}
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {icone && <T20Icon name={icone} size={20} color="#ffd700" />}
                        <h3 style={{ margin: 0, color: '#ffd700', fontSize: '1.2rem', fontFamily: 'Tormenta, serif', letterSpacing: '0.03em' }}>
                            {nome}
                        </h3>
                    </div>
                    {subtitulo && (
                        <div style={{ color: '#a5b4fc', fontSize: '0.85rem', fontWeight: 600, marginTop: 3 }}>
                            {subtitulo}
                        </div>
                    )}
                    {!subtitulo && bonus && (
                        <div style={{ color: '#8be9fd', fontSize: '0.82rem', fontWeight: 600, marginTop: 4 }}>
                            {bonus}
                        </div>
                    )}
                </div>

                {/* Badges estruturados (Energia, Arma Preferida, etc.) */}
                {badges.length > 0 && (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {badges.map((b, i) => (
                            <div
                                key={i}
                                style={{
                                    background: 'rgba(255,255,255,0.04)',
                                    border: `1px solid ${b.color}44`,
                                    borderRadius: 6,
                                    padding: '5px 9px',
                                    fontSize: '0.76rem',
                                }}
                            >
                                <span style={{ color: '#94a3b8', marginRight: 4 }}>{b.label}:</span>
                                <strong style={{ color: b.color }}>{b.value}</strong>
                            </div>
                        ))}
                    </div>
                )}

                {/* Símbolo Sagrado */}
                {simbolo && (
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid #2a2f4a', borderRadius: 8, padding: '9px 11px' }}>
                        <div style={{ fontSize: '0.68rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: '#94a3b8', fontWeight: 700, marginBottom: 3 }}>
                            Símbolo Sagrado
                        </div>
                        <div style={{ color: '#e2e8f0', fontSize: '0.83rem', lineHeight: 1.45 }}>
                            {simbolo}
                        </div>
                    </div>
                )}

                {/* Poderes Concedidos */}
                {poderes.length > 0 && (
                    <div>
                        <div style={{ fontSize: '0.68rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: '#94a3b8', fontWeight: 700, marginBottom: 6 }}>
                            Poderes Concedidos
                        </div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                            {poderes.map((p, i) => (
                                <span
                                    key={i}
                                    style={{
                                        background: 'rgba(168, 85, 247, 0.14)',
                                        border: '1px solid rgba(192, 132, 252, 0.35)',
                                        color: '#e9d5ff',
                                        borderRadius: 999,
                                        padding: '3px 10px',
                                        fontSize: '0.76rem',
                                        fontWeight: 500,
                                    }}
                                >
                                    {p}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Crenças e Objetivos */}
                {crencas && (
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid #2a2f4a', borderRadius: 8, padding: '10px 12px' }}>
                        <div style={{ fontSize: '0.68rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: '#93c5fd', fontWeight: 700, marginBottom: 4 }}>
                            Crenças e Objetivos
                        </div>
                        <p style={{ margin: 0, color: '#cbd5e1', fontSize: '0.83rem', lineHeight: 1.55 }}>
                            {crencas}
                        </p>
                    </div>
                )}

                {/* Obrigações & Restrições */}
                {obrigacoes && (
                    <div style={{ background: 'rgba(245, 158, 11, 0.08)', border: '1px solid rgba(245, 158, 11, 0.35)', borderRadius: 8, padding: '10px 12px' }}>
                        <div style={{ fontSize: '0.68rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: '#fbbf24', fontWeight: 700, marginBottom: 4, display: 'flex', alignItems: 'center', gap: 5 }}>
                            <T20Icon name="alerta" size={12} color="#fbbf24" /> Obrigações & Restrições
                        </div>
                        <p style={{ margin: 0, color: '#fde68a', fontSize: '0.82rem', lineHeight: 1.55 }}>
                            {obrigacoes}
                        </p>
                    </div>
                )}

                {/* Fallback para itens não-deus (raças, origens, etc.) */}
                {extras.length > 0 && (
                    <div style={{ color: '#cbd5e1', fontSize: '0.84rem', lineHeight: 1.55, whiteSpace: 'pre-line' }}>
                        {extras.join('\n')}
                    </div>
                )}
                {!tooltip && descricao && (
                    <p style={{ margin: 0, color: '#cbd5e1', fontSize: '0.84rem', lineHeight: 1.55 }}>
                        {descricao}
                    </p>
                )}

                {bloqueado && motivoBloqueio && (
                    <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: 6, padding: '8px 10px', color: '#fca5a5', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: 6 }}>
                        <T20Icon name="imunidade" size={14} color="#f87171" /> {motivoBloqueio}
                    </div>
                )}
            </div>

            {onConfirm && !bloqueado && (
                <div style={{ padding: '12px 18px', borderTop: '1px solid #2a2f4a', background: 'rgba(10, 12, 24, 0.7)' }}>
                    <button
                        type="button"
                        onClick={onConfirm}
                        style={{
                            width: '100%',
                            padding: '9px 14px',
                            borderRadius: 7,
                            border: 'none',
                            background: selecionado ? '#b45309' : 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
                            color: '#111827',
                            fontWeight: 700,
                            fontSize: '0.86rem',
                            cursor: 'pointer',
                            fontFamily: FONT_BODY,
                        }}
                    >
                        {selecionado ? `Selecionado: ${nome}` : `Escolher ${nome}`}
                    </button>
                </div>
            )}
        </div>
    );
};
