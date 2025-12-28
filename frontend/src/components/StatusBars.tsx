import React from 'react';
import type { Personagem } from '../types';
import '../Ficha.css';

interface StatusBarsProps {
    ficha: Personagem;
}

export const StatusBars: React.FC<StatusBarsProps> = ({ ficha }) => {
    const { pv, pm, defesa, deslocamento, detalhes_deslocamento, rd } = ficha.status;
    const detalhesDefesa = defesa.detalhes;

    // Cálculos de Porcentagem
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));

    // Helpers para compatibilidade (Novo Backend vs Velho Backend)
    const calcPV = pv.calculo || pv.detalhes_pv;
    const calcPM = pm.calculo || pm.detalhes_pm;

    return (
        <div className="section-card" style={{ marginTop: '25px' }}>
            <h3 className="section-title">Status Vitais</h3>

            {/* --- BARRA DE VIDA (PV) --- */}
            <div className="bar-container tooltip-container">
                <div className="bar-header">
                    <span>PV</span>
                    <span>{pv.atual}/{pv.maximo}</span>
                </div>
                <div className="bar-track">
                    <div className="bar-fill pv-fill" style={{ width: `${pvPerc}%` }}></div>
                </div>

                {/* Tooltip PV */}
                {calcPV && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Inicial:</span> <span>{calcPV.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{calcPV.nivel}</span></div>
                        <div className="tooltip-row"><span>Con:</span> <span>{calcPV.con}</span></div>
                        {calcPV.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{calcPV.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{pv.maximo}</span></div>
                    </div>
                )}
            </div>

            {/* --- BARRA DE MANA (PM) --- */}
            <div className="bar-container tooltip-container">
                <div className="bar-header">
                    <span>PM</span>
                    <span>{pm.atual}/{pm.maximo}</span>
                </div>
                <div className="bar-track">
                    <div className="bar-fill pm-fill" style={{ width: `${pmPerc}%` }}></div>
                </div>

                {/* Tooltip PM */}
                {calcPM && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{calcPM.nivel}</span></div>
                        <div className="tooltip-row"><span>Atributo:</span> <span>{calcPM.atributo}</span></div>
                        {calcPM.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{calcPM.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{pm.maximo}</span></div>
                    </div>
                )}
            </div>

            {/* --- STATUS SECUNDÁRIOS --- */}
            <div className="stats-row-container">
                {/* DEFESA */}
                <div className="stat-box tooltip-container">
                    <span className="stat-value">🛡️ {defesa.total}</span>
                    <span className="stat-label">Defesa</span>
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Base:</span> <span>10</span></div>
                        <div className="tooltip-row"><span>Des/Atributo:</span> <span>{detalhesDefesa.des_mod}</span></div>
                        {detalhesDefesa.armadura > 0 && <div className="tooltip-row"><span>Armadura:</span> <span>{detalhesDefesa.armadura}</span></div>}
                        {detalhesDefesa.escudo > 0 && <div className="tooltip-row"><span>Escudo:</span> <span>{detalhesDefesa.escudo}</span></div>}
                        {detalhesDefesa.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{detalhesDefesa.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{defesa.total}</span></div>
                    </div>
                </div>

                {/* DESLOCAMENTO */}
                <div className="stat-box tooltip-container">
                    <span className="stat-value">🦵 {deslocamento}m</span>
                    <span className="stat-label">Deslocamento</span>
                    {detalhes_deslocamento && (
                        <div className="attr-tooltip">
                            <div className="tooltip-row"><span>Base:</span> <span>{detalhes_deslocamento.base}m</span></div>
                            {detalhes_deslocamento.armadura !== 0 && <div className="tooltip-row"><span>Armadura:</span> <span>{detalhes_deslocamento.armadura}m</span></div>}
                            {detalhes_deslocamento.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{detalhes_deslocamento.outros}m</span></div>}
                            <div className="tooltip-total"><span>Total:</span> <span>{deslocamento}m</span></div>
                        </div>
                    )}
                </div>
            </div>

            {/* --- REDUÇÃO DE DANO (RD) --- */}
            {rd && rd.length > 0 && (
                <div className="rd-section" style={{ marginTop: '15px', paddingTop: '10px', borderTop: '1px solid #333' }}>
                    <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px', display: 'block', marginBottom: '8px' }}>
                        Resistências / RD
                    </span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        {rd.map((item: string, idx: number) => (
                            <span key={idx} style={{
                                background: '#3e2723',
                                color: '#ffccbc',
                                border: '1px solid #5d4037',
                                padding: '3px 10px',
                                borderRadius: '4px',
                                fontSize: '0.8rem',
                                fontWeight: 'bold',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '5px'
                            }}>
                                🛡️ {item}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};