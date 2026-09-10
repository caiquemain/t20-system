import React from 'react';
import type { Personagem } from '../types';
import '../Ficha.css';

interface StatusBarsProps {
    ficha: Personagem;
    onUpdate?: (data: Partial<Personagem>) => void;
    overrideDeslocamento?: number;
    isFlying?: boolean;
    isAquatic?: boolean;
}

export const StatusBars: React.FC<StatusBarsProps> = ({
    ficha,
    onUpdate,
    overrideDeslocamento,
    isFlying,
    isAquatic
}) => {
    const { pv, pm, defesa, deslocamento, rd, proficiencias, imunidades, sentidos } = ficha.status;
    const statusAny = ficha.status as any;

    let iconeDeslocamento = '🦵';
    let labelDeslocamento = 'Deslocamento';
    if (isFlying) { iconeDeslocamento = '🪽'; labelDeslocamento = 'Voo Ativo'; }
    else if (isAquatic) { iconeDeslocamento = '🧜‍♀️'; labelDeslocamento = 'Natação'; }

    const valorDeslocamento = overrideDeslocamento || deslocamento;
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));

    const habGolem = ficha.habilidades.find(h => h.nome === "Espírito Elemental" || h.nome === "Fonte Elemental");
    // @ts-ignore
    const elementoGolem = habGolem?.escolhas_aplicadas?.["elemento_escolha"];

    const handleDescansar = () => {
        if (onUpdate) {
            if (window.confirm("Deseja realizar um Descanso Completo? Isso recuperará todo seu PV e PM.")) {
                onUpdate({
                    status: {
                        ...ficha.status,
                        pv: { ...pv, atual: pv.maximo },
                        pm: { ...pm, atual: pm.maximo }
                    }
                });
            }
        }
    };

    const getIconeResistencia = (texto: string) => {
        const t = texto.toLowerCase();
        if (t.includes('fogo')) return '🔥';
        if (t.includes('frio') || t.includes('gelo')) return '❄️';
        if (t.includes('eletricidade') || t.includes('elétrico')) return '⚡';
        if (t.includes('ácido')) return '🧪';
        if (t.includes('veneno')) return '☠️';
        if (t.includes('luz')) return '🔆';
        if (t.includes('trevas') || t.includes('sombra')) return '🌑';
        if (t.includes('mental') || t.includes('psíquico')) return '🧠';
        if (t.includes('corte') || t.includes('perfura') || t.includes('impacto')) return '⚔️';
        if (t.includes('magia')) return '✨';
        return '🛡️';
    };

    // ✨ TOOLTIP GENÉRICO DA PILHA DE MODIFICADORES (funciona p/ PV, PM, Defesa e Deslocamento)
    const renderTooltipPilha = (calc: any, total: number | string, unidade = '') => {
        if (!calc) return null;
        const fontes: any[] = calc.fontes || [];
        if (fontes.length === 0 && !calc.base) return null;
        return (
            <div className="status-custom-tooltip">
                {calc.base !== 0 && (
                    <div className="tooltip-row"><span>Base</span><span>{calc.base}{unidade}</span></div>
                )}
                {fontes.map((f: any, i: number) => (
                    <div key={i} className="tooltip-row">
                        <span>{f.fonte}</span>
                        <span>{f.valor >= 0 ? `+${f.valor}` : f.valor}{unidade}</span>
                    </div>
                ))}
                <div className="tooltip-total"><span>Total</span><span>{total}{unidade}</span></div>
            </div>
        );
    };

    return (
        <div className="section-card" style={{ marginTop: '25px', position: 'relative' }}>
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                <h3 className="section-title" style={{ margin: 0 }}>Status Vitais</h3>
                {onUpdate && (
                    <button onClick={handleDescansar} className="btn-descansar" title="Recuperar todo PV e PM">
                        💤 Descansar
                    </button>
                )}
            </div>

            {/* PV */}
            <div className="bar-container tooltip-anchor">
                <div className="bar-header"><span>PV</span><span>{pv.atual}/{pv.maximo}</span></div>
                <div className="bar-track"><div className="bar-fill pv-fill" style={{ width: `${pvPerc}%` }}></div></div>
                {renderTooltipPilha(statusAny.pv_calc, pv.maximo)}
            </div>

            {/* PM */}
            <div className="bar-container tooltip-anchor">
                <div className="bar-header"><span>PM</span><span>{pm.atual}/{pm.maximo}</span></div>
                <div className="bar-track"><div className="bar-fill pm-fill" style={{ width: `${pmPerc}%` }}></div></div>
                {renderTooltipPilha(statusAny.pm_calc, pm.maximo)}
            </div>

            {/* DEFESA + DESLOCAMENTO */}
            <div className="stats-row-container">
                <div className="stat-box tooltip-anchor">
                    <span className="stat-value">🛡️ {defesa.total}</span>
                    <span className="stat-label">Defesa</span>
                    {renderTooltipPilha(statusAny.defesa_calc, defesa.total)}
                </div>
                <div className="stat-box tooltip-anchor">
                    <span className="stat-value" style={{ color: (isFlying || isAquatic) ? '#42a5f5' : 'inherit' }}>
                        {iconeDeslocamento} {valorDeslocamento}m
                    </span>
                    <span className="stat-label">{labelDeslocamento}</span>
                    {renderTooltipPilha(statusAny.deslocamento_calc, valorDeslocamento, 'm')}
                </div>
            </div>

            {/* PROFICIÊNCIAS */}
            {proficiencias && proficiencias.length > 0 && (
                <div className="rd-section" style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #333' }}>
                    <span className="status-section-label">Proficiências</span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {proficiencias.map((item: string, idx: number) => (
                            <span key={idx} className="prof-tag">{item}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* RD, IMUNIDADES & SENTIDOS */}
            {((rd && rd.length > 0) || elementoGolem || (imunidades && imunidades.length > 0) || (sentidos && sentidos.length > 0)) && (
                <div className="rd-section" style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #333' }}>
                    <span className="status-section-label">Resistências & Sentidos</span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {elementoGolem && (
                            <span className="rd-tag" style={{ background: '#1b5e20', color: '#a5d6a7', borderColor: '#2e7d32' }}>
                                🔋 Absorve: {elementoGolem}
                            </span>
                        )}
                        {rd?.map((item: string, idx: number) => (
                            <span key={`rd-${idx}`} className="rd-tag">
                                <span style={{ fontSize: '1.1em', marginRight: '4px' }}>{getIconeResistencia(item)}</span>
                                {item}
                            </span>
                        ))}
                        {imunidades?.map((item: string, idx: number) => (
                            <span key={`imun-${idx}`} className="rd-tag" style={{ background: '#4a148c', color: '#e1bee7', borderColor: '#7b1fa2' }}>
                                🚫 {item}
                            </span>
                        ))}
                        {sentidos?.map((item: string, idx: number) => (
                            <span key={`sens-${idx}`} className="rd-tag" style={{ background: '#01579b', color: '#b3e5fc', borderColor: '#0277bd' }}>
                                👁️ {item}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            <style>{`
                .btn-descansar {
                    background: transparent; border: 1px solid #4caf50; color: #4caf50;
                    border-radius: 4px; padding: 4px 10px; fontSize: 0.75rem; font-weight: bold;
                    cursor: pointer; display: flex; alignItems: center; gap: 5px; transition: all 0.2s;
                }
                .btn-descansar:hover { background: rgba(76, 175, 80, 0.1); }
                .status-section-label {
                    font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.5px;
                    display: block; margin-bottom: 5px; font-weight: bold;
                }
                .tooltip-anchor { position: relative; cursor: help; }
                .status-custom-tooltip {
                    visibility: hidden; opacity: 0; position: absolute; bottom: 100%; left: 50%;
                    transform: translateX(-50%) translateY(5px); width: 240px; background-color: #1a1a1a;
                    border: 1px solid #ffd700; border-radius: 6px; padding: 10px; z-index: 9999;
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9); transition: opacity 0.2s, transform 0.2s;
                    pointer-events: none;
                }
                .tooltip-anchor:hover .status-custom-tooltip {
                    visibility: visible; opacity: 1; transform: translateX(-50%) translateY(-10px);
                }
                .tooltip-row { display: flex; justify-content: space-between; font-size: 0.75rem; color: #ccc; margin-bottom: 3px; border-bottom: 1px dashed #333; }
                .tooltip-total { border-top: 1px solid #fca311; margin-top: 5px; padding-top: 2px; font-weight: bold; color: #fca311; display: flex; justify-content: space-between; }
                .rd-tag {
                    background: #3e2723; color: #ffccbc; border: 1px solid #5d4037;
                    padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;
                    display: flex; align-items: center; gap: 5px;
                }
                .prof-tag {
                    background: #263238; color: #cfd8dc; border: 1px solid #455a64;
                    padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;
                }
            `}</style>
        </div>
    );
};
