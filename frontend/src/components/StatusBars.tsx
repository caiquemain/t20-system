import React from 'react';
import type { Personagem } from '../types';
import '../Ficha.css';

interface StatusBarsProps {
    ficha: Personagem;
}

export const StatusBars: React.FC<StatusBarsProps> = ({ ficha }) => {

    // Agora o TypeScript reconhecerá 'detalhes_deslocamento'
    const { pv, pm, defesa, deslocamento, detalhes_deslocamento } = ficha.status;
    const detalhesDefesa = defesa.detalhes;

    // Cálculos de Porcentagem
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));

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
                {pv.detalhes_pv && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Inicial:</span> <span>{pv.detalhes_pv.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{pv.detalhes_pv.nivel}</span></div>
                        <div className="tooltip-row"><span>Con:</span> <span>{pv.detalhes_pv.con}</span></div>
                        {pv.detalhes_pv.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{pv.detalhes_pv.outros}</span></div>}
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
                {pm.detalhes_pm && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{pm.detalhes_pm.nivel}</span></div>
                        <div className="tooltip-row"><span>Atributo:</span> <span>{pm.detalhes_pm.atributo}</span></div>
                        {pm.detalhes_pm.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{pm.detalhes_pm.outros}</span></div>}
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

                    {/* Tooltip Deslocamento */}
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
        </div>
    );
};