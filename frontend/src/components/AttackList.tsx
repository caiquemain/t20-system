import React, { useState } from 'react';
import { T20Icon } from './T20Icon';
import { rolarAtaqueD20, rolarExpressao, type ResultadoD20, type ResultadoExpressao } from '../utils/diceRoller';

interface AtaqueView {
    nome: string; bonus_ataque: string; dano: string; critico: string;
    tipo: string; alcance: string; teste: string; especial?: string;
}

interface AttackListProps {
    ataques: AtaqueView[];
    fluxoDeMana?: boolean;
    focoVital?: boolean;
}

interface RollAtaqueState {
    nome: string;
    ehMagia: boolean;
    cdTexto?: string;
    ataque?: ResultadoD20;
    dano: ResultadoExpressao | null;
    tipoDano: string;
}

// Classificação visual dos efeitos (mesmo idioma de cores do sistema)
const ehPenalidade = (t: string) => /-\d/.test(t) || /não proficiente|penalidade|desbalanceada/i.test(t);
const ehBuff = (t: string) => /\+\d/.test(t) || /conta como/i.test(t);

export const AttackList: React.FC<AttackListProps> = ({ ataques, fluxoDeMana, focoVital }) => {
    const [ultimoRoll, setUltimoRoll] = useState<RollAtaqueState | null>(null);

    const handleRolarAtaque = (a: AtaqueView) => {
        const ehMagia = /^CD\s+\d+|^Auto$/i.test((a.bonus_ataque || '').trim());
        const danoRes = rolarExpressao(a.dano);
        if (ehMagia) {
            setUltimoRoll({
                nome: a.nome,
                ehMagia: true,
                cdTexto: a.bonus_ataque === 'Auto' ? 'Acerto Automático' : `${a.teste} ${a.bonus_ataque}`,
                dano: danoRes,
                tipoDano: a.tipo,
            });
        } else {
            setUltimoRoll({
                nome: a.nome,
                ehMagia: false,
                ataque: rolarAtaqueD20(a.bonus_ataque),
                dano: danoRes,
                tipoDano: a.tipo,
            });
        }
    };

    return (
        <div className="section-card" style={{ marginTop: 25 }}>
            <style>{`
                .ataque-tooltip {
                    visibility: hidden; opacity: 0;
                    position: absolute; bottom: 100%; left: 0;
                    transform: translateY(0);
                    width: 260px; background-color: #1a1a1a;
                    border: 1px solid #ffd700; border-radius: 6px;
                    padding: 10px; z-index: 9999;
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9);
                    transition: opacity 0.2s, transform 0.2s;
                    pointer-events: none; margin-bottom: 6px;
                    text-transform: none;
                }
                .tooltip-container:hover .ataque-tooltip {
                    visibility: visible; opacity: 1;
                    transform: translateY(-6px);
                }
            `}</style>
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <h3 className="section-title" style={{ margin: 0, display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                    <T20Icon name="ataque" size={18} /> Ataques
                </h3>
                <div style={{ display: 'flex', gap: 6 }}>
                    {fluxoDeMana && (
                        <span style={{ fontSize: '0.7rem', color: '#80deea', background: 'rgba(0,188,212,0.1)', border: '1px solid rgba(0,188,212,0.4)', padding: '2px 8px', borderRadius: 4, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                            <T20Icon name="natacao" size={12} /> Fluxo de Mana
                        </span>
                    )}
                    {focoVital && (
                        <span style={{ fontSize: '0.7rem', color: '#ef9a9a', background: 'rgba(244,67,54,0.1)', border: '1px solid rgba(244,67,54,0.4)', padding: '2px 8px', borderRadius: 4, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                            <T20Icon name="hp" size={12} /> Foco Vital
                        </span>
                    )}
                </div>
            </div>

            {ultimoRoll && (
                <div style={{
                    background: '#16161e',
                    border: '1px solid #ffd70066',
                    borderRadius: 6,
                    padding: '8px 12px',
                    marginBottom: 12,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: 10,
                    fontSize: '0.85rem',
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                        <strong style={{ color: '#ffd54f' }}>{ultimoRoll.nome}</strong>
                        {ultimoRoll.ehMagia ? (
                            <span style={{ color: '#ce93d8', fontWeight: 'bold' }}>{ultimoRoll.cdTexto}</span>
                        ) : ultimoRoll.ataque && (
                            <span>
                                Ataque:{' '}
                                <strong style={{
                                    color: ultimoRoll.ataque.criticoNatural === 'sucesso'
                                        ? '#81c784'
                                        : ultimoRoll.ataque.criticoNatural === 'falha'
                                            ? '#ff5252'
                                            : '#fff',
                                }}>
                                    {ultimoRoll.ataque.total}
                                </strong>{' '}
                                <span style={{ color: '#888', fontSize: '0.75rem' }}>
                                    (d20[{ultimoRoll.ataque.d20}] {ultimoRoll.ataque.bonus >= 0 ? `+${ultimoRoll.ataque.bonus}` : ultimoRoll.ataque.bonus})
                                </span>
                            </span>
                        )}
                        {ultimoRoll.dano && (
                            <span>
                                Dano ({ultimoRoll.tipoDano}):{' '}
                                <strong style={{ color: '#ffcc80' }}>{ultimoRoll.dano.total}</strong>{' '}
                                <span style={{ color: '#888', fontSize: '0.75rem' }}>
                                    ({ultimoRoll.dano.detalhes.map(d => `${d.dado}[${d.rolagens.join(',')}]`).join(' + ')}
                                    {ultimoRoll.dano.bonus !== 0 ? (ultimoRoll.dano.bonus > 0 ? `+${ultimoRoll.dano.bonus}` : ultimoRoll.dano.bonus) : ''})
                                </span>
                            </span>
                        )}
                    </div>
                    <button
                        onClick={() => setUltimoRoll(null)}
                        style={{ background: 'transparent', border: 'none', color: '#888', cursor: 'pointer', fontSize: '1rem' }}
                        title="Fechar resultado"
                    >
                        &times;
                    </button>
                </div>
            )}

            {(!ataques || ataques.length === 0) ? (
                <p style={{ color: '#666', textAlign: 'center', fontSize: '0.85rem' }}>Nenhum ataque ou poder ofensivo.</p>
            ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                    <thead>
                        <tr style={{ color: '#888', textTransform: 'uppercase', fontSize: '0.7rem' }}>
                            {['Arma / Magia', 'Bônus / CD', 'Dano', 'Crít.', 'Tipo', 'Alcance', 'Teste', ''].map(h => (
                                <th key={h} style={{ textAlign: 'left', padding: '4px 6px', borderBottom: '1px solid #333' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {ataques.map((a, i) => {
                            const ehMagia = strEhMagia(a.especial);
                            return (
                                <tr key={i} style={{ borderBottom: '1px solid #252525' }}>
                                    <td style={{ padding: '6px' }} className="tooltip-container">
                                        <strong style={{ color: ehMagia ? '#ce93d8' : '#e0e0e0' }}>{a.nome}</strong>
                                        {a.especial && (
                                            <>
                                                <span
                                                    style={{ marginLeft: 6, cursor: 'help', display: 'inline-flex', alignItems: 'center' }}
                                                    title={ehPenalidade(a.especial) ? 'Há penalidades neste ataque' : 'Efeitos especiais'}
                                                >
                                                    <T20Icon
                                                        name={ehPenalidade(a.especial) ? 'alerta' : ehMagia ? 'grimorio' : 'efeito'}
                                                        size={13}
                                                        color={ehPenalidade(a.especial) ? '#ffb74d' : ehMagia ? '#ce93d8' : '#80deea'}
                                                    />
                                                </span>
                                                <div className="ataque-tooltip">
                                                    {a.especial.split('; ').map((t, idx) => (
                                                        <div
                                                            key={idx}
                                                            className="tooltip-row"
                                                            style={{
                                                                color: ehPenalidade(t) ? '#ff8a80' : ehBuff(t) ? '#80deea' : '#ccc',
                                                                fontWeight: (ehPenalidade(t) || ehBuff(t)) ? 'bold' : 'normal',
                                                            }}
                                                        >
                                                            {t}
                                                        </div>
                                                    ))}
                                                </div>
                                            </>
                                        )}
                                    </td>
                                    <td style={{ padding: '6px', color: ehMagia ? '#ce93d8' : '#ccc', fontWeight: ehMagia ? 'bold' : 'normal' }}>{a.bonus_ataque}</td>
                                    <td style={{ padding: '6px', color: '#ffcc80', fontWeight: 'bold' }}>{a.dano}</td>
                                    <td style={{ padding: '6px', color: '#ccc' }}>{a.critico}</td>
                                    <td style={{ padding: '6px', color: '#ccc' }}>{a.tipo}</td>
                                    <td style={{ padding: '6px', color: '#ccc' }}>{a.alcance}</td>
                                    <td style={{ padding: '6px', color: '#ccc' }}>{a.teste}</td>
                                    <td style={{ padding: '6px', textAlign: 'right' }}>
                                        <button
                                            type="button"
                                            onClick={() => handleRolarAtaque(a)}
                                            title={`Rolar ${a.nome}`}
                                            style={{
                                                background: ehMagia ? 'rgba(156, 39, 176, 0.2)' : 'rgba(255, 193, 7, 0.12)',
                                                color: ehMagia ? '#ce93d8' : '#ffd54f',
                                                border: `1px solid ${ehMagia ? 'rgba(206, 147, 216, 0.45)' : 'rgba(255, 213, 79, 0.35)'}`,
                                                borderRadius: 4,
                                                padding: '3px 8px',
                                                cursor: 'pointer',
                                                fontSize: '0.75rem',
                                                display: 'inline-flex',
                                                alignItems: 'center',
                                                gap: 4,
                                            }}
                                        >
                                            <T20Icon name="dado" size={12} /> Rolar
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            )}
        </div>
    );
};

function strEhMagia(especial?: string): boolean {
    return Boolean(especial && especial.startsWith('Magia •'));
}
