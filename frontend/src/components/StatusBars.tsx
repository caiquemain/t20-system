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
    // --- LOG DE DEBUG PARA VERIFICAR DADOS ---
    console.group("🔍 DEBUG STATUS BARS");
    console.log("Objeto Status Completo:", ficha.status);
    console.log("Proficiências:", ficha.status.proficiencias);
    console.log("Imunidades:", ficha.status.imunidades);
    console.log("Sentidos:", ficha.status.sentidos);
    console.groupEnd();
    // -----------------------------------------
    // Extrai os novos campos: proficiencias, imunidades, sentidos
    // @ts-ignore (Ignora erro se o tipo ainda não foi atualizado no types.ts)
    const { pv, pm, defesa, deslocamento, detalhes_deslocamento, rd, proficiencias, imunidades, sentidos } = ficha.status;

    const detalhesDefesa = defesa.detalhes || { "Base": 10 };

    // --- LÓGICA DE ÍCONES E TEXTOS ---
    let iconeDeslocamento = '🦵';
    let labelDeslocamento = 'Deslocamento';

    if (isFlying) {
        iconeDeslocamento = '🪽';
        labelDeslocamento = 'Voo Ativo';
    } else if (isAquatic) {
        iconeDeslocamento = '🧜‍♀️';
        labelDeslocamento = 'Natação';
    }

    const valorDeslocamento = overrideDeslocamento || deslocamento;
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));
    const calcPV = pv.calculo || pv.detalhes_pv;
    const calcPM = pm.calculo || pm.detalhes_pm;

    // Golem
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

    const renderTooltipDinamico = (detalhes: any, total: number) => {
        if (!detalhes) return null;
        const entries = Object.entries(detalhes);
        entries.sort((a, b) => {
            if (a[0] === 'Base') return -1;
            if (b[0] === 'Base') return 1;
            return a[0].localeCompare(b[0]);
        });

        return (
            <div className="status-custom-tooltip">
                {entries.map(([fonte, valor]: [string, any]) => {
                    const valStr = typeof valor === 'number' && valor >= 0 ? `+${valor}` : valor;
                    return (
                        <div key={fonte} className="tooltip-row">
                            <span>{fonte}</span>
                            <span>{valStr}</span>
                        </div>
                    );
                })}
                <div className="tooltip-total">
                    <span>Total</span>
                    <span>{total}</span>
                </div>
            </div>
        );
    };

    return (
        <div className="section-card" style={{ marginTop: '25px', position: 'relative' }}>

            {/* CABEÇALHO */}
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                <h3 className="section-title" style={{ margin: 0 }}>Status Vitais</h3>
                {onUpdate && (
                    <button onClick={handleDescansar} className="btn-descansar" title="Recuperar PV e PM totalmente">
                        💤 Descansar
                    </button>
                )}
            </div>

            {/* BARRAS DE VIDA E MANA */}
            <div className="bar-container tooltip-anchor">
                <div className="bar-header"><span>PV</span><span>{pv.atual}/{pv.maximo}</span></div>
                <div className="bar-track"><div className="bar-fill pv-fill" style={{ width: `${pvPerc}%` }}></div></div>
                {calcPV && (
                    <div className="status-custom-tooltip">
                        <div className="tooltip-row"><span>Inicial</span> <span>{calcPV.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível</span> <span>+{calcPV.nivel}</span></div>
                        <div className="tooltip-row"><span>Con</span> <span>+{calcPV.con}</span></div>
                        {calcPV.habilidades !== 0 && <div className="tooltip-row"><span>Habilidades</span> <span>+{calcPV.habilidades}</span></div>}
                        <div className="tooltip-total"><span>Total</span> <span>{pv.maximo}</span></div>
                    </div>
                )}
            </div>

            <div className="bar-container tooltip-anchor">
                <div className="bar-header"><span>PM</span><span>{pm.atual}/{pm.maximo}</span></div>
                <div className="bar-track"><div className="bar-fill pm-fill" style={{ width: `${pmPerc}%` }}></div></div>
                {calcPM && (
                    <div className="status-custom-tooltip">
                        <div className="tooltip-row"><span>Inicial</span> <span>{calcPM.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível</span> <span>+{calcPM.nivel}</span></div>
                        <div className="tooltip-row"><span>Atributo</span> <span>+{calcPM.atributo}</span></div>
                        {calcPM.habilidades !== 0 && <div className="tooltip-row"><span>Habilidades</span> <span>+{calcPM.habilidades}</span></div>}
                        <div className="tooltip-total"><span>Total</span> <span>{pm.maximo}</span></div>
                    </div>
                )}
            </div>

            {/* STATUS SECUNDÁRIOS */}
            <div className="stats-row-container">
                <div className="stat-box tooltip-anchor">
                    <span className="stat-value">🛡️ {defesa.total}</span>
                    <span className="stat-label">Defesa</span>
                    {renderTooltipDinamico(detalhesDefesa, defesa.total)}
                </div>

                <div className="stat-box tooltip-anchor">
                    <span className="stat-value" style={{ color: (isFlying || isAquatic) ? '#42a5f5' : 'inherit' }}>
                        {iconeDeslocamento} {valorDeslocamento}m
                    </span>
                    <span className="stat-label">{labelDeslocamento}</span>
                    {detalhes_deslocamento && (
                        <div className="status-custom-tooltip">
                            <div className="tooltip-row"><span>Base</span> <span>{detalhes_deslocamento.base}m</span></div>
                            {isFlying && <div className="tooltip-row" style={{ color: '#42a5f5' }}><span>Voo</span> <span>12m</span></div>}
                            {detalhes_deslocamento.armadura !== 0 && <div className="tooltip-row"><span>Armadura</span> <span>{detalhes_deslocamento.armadura}m</span></div>}
                            <div className="tooltip-total"><span>Total</span> <span>{valorDeslocamento}m</span></div>
                        </div>
                    )}
                </div>
            </div>

            {/* --- NOVA SEÇÃO: PROFICIÊNCIAS --- */}
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

            {/* --- NOVA SEÇÃO: IMUNIDADES E SENTIDOS E RD --- */}
            {(rd?.length > 0 || elementoGolem || imunidades?.length > 0 || sentidos?.length > 0) && (
                <div className="rd-section" style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #333' }}>
                    <span className="status-section-label">Resistências & Sentidos</span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>

                        {/* Golem */}
                        {elementoGolem && (
                            <span className="rd-tag" style={{ background: '#1b5e20', color: '#a5d6a7', borderColor: '#2e7d32' }}>
                                🔋 Absorve: {elementoGolem}
                            </span>
                        )}

                        {/* RDs */}
                        {rd?.map((item: string, idx: number) => (
                            <span key={`rd-${idx}`} className="rd-tag">🛡️ {item}</span>
                        ))}

                        {/* Imunidades */}
                        {imunidades?.map((item: string, idx: number) => (
                            <span key={`imun-${idx}`} className="rd-tag" style={{ background: '#4a148c', color: '#e1bee7', borderColor: '#7b1fa2' }}>
                                🚫 {item}
                            </span>
                        ))}

                        {/* Sentidos */}
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
                    border-radius: 4px; padding: 4px 10px; fontSize: 0.75rem; fontWeight: bold;
                    cursor: pointer; display: flex; alignItems: center; gap: 5px; transition: all 0.2s;
                }
                .btn-descansar:hover { background: rgba(76, 175, 80, 0.1); }

                .status-section-label {
                    fontSize: 0.7rem; color: #888; textTransform: uppercase; letterSpacing: 0.5px;
                    display: block; marginBottom: 5px; fontWeight: bold;
                }

                .tooltip-anchor { position: relative; cursor: help; }
                .status-custom-tooltip {
                    visibility: hidden; opacity: 0; position: absolute; bottom: 100%; left: 50%;
                    transform: translateX(-50%) translateY(5px); width: 220px; background-color: #1a1a1a;
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
                    padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; fontWeight: bold;
                    display: flex; alignItems: center; gap: 5px;
                }
                .prof-tag {
                    background: #263238; color: #cfd8dc; border: 1px solid #455a64;
                    padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;
                }
            `}</style>
        </div>
    );
};