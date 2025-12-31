import React, { useMemo } from 'react';
import type { Magia } from '../types';
import { getCircleColor } from '../utils/magicUtils'; // Importando cor do Círculo
import './SpellSummary.css';

interface SpellSummaryProps {
    magias: Magia[];
    onOpenDetalhes: () => void;
    onSpellClick: (magia: Magia) => void;
}

const CUSTO_PADRAO: Record<number, number> = {
    1: 1, 2: 3, 3: 6, 4: 10, 5: 15
};

export const SpellSummary: React.FC<SpellSummaryProps> = ({ magias, onOpenDetalhes, onSpellClick }) => {

    const magiasPorCirculo = useMemo(() => {
        const grupos: Record<number, Magia[]> = {};
        [1, 2, 3, 4, 5].forEach(c => grupos[c] = []);

        magias.forEach(m => {
            const c = m.circulo || 1;
            if (!grupos[c]) grupos[c] = [];
            grupos[c].push(m);
        });
        return grupos;
    }, [magias]);

    const circulosAtivos = Object.entries(magiasPorCirculo).filter(([_, lista]) => lista.length > 0);

    return (
        <div className="spell-summary-container">
            {magias.length === 0 ? (
                <div className="spell-summary-empty">
                    Grimório vazio. Adicione magias para começar.
                </div>
            ) : (
                <div className="summary-grid">
                    {circulosAtivos.map(([circuloStr, lista]) => {
                        const circulo = Number(circuloStr);
                        const circleColor = getCircleColor(circulo); // Cor dinâmica baseada no nível

                        return (
                            <div key={circulo} className="circle-summary-card">
                                <div className="circle-header">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                        {/* APLICANDO A COR DO CÍRCULO AQUI */}
                                        <div
                                            className="circle-badge"
                                            style={{
                                                background: circleColor,
                                                color: '#111', // Texto escuro para contraste com cores claras
                                                boxShadow: `0 0 10px ${circleColor}40`
                                            }}
                                        >
                                            {circulo}º
                                        </div>
                                        <span style={{ fontWeight: 'bold', color: '#ddd', textTransform: 'uppercase', fontSize: '0.9rem' }}>
                                            Círculo
                                        </span>
                                    </div>
                                    <span className="pm-cost">
                                        {CUSTO_PADRAO[circulo] || '?'} PM
                                    </span>
                                </div>

                                <div className="spell-names-list">
                                    {lista.map(m => (
                                        <div
                                            key={m.nome}
                                            className="spell-name-item"
                                            onClick={() => onSpellClick(m)}
                                            title="Clique para ver detalhes"
                                        >
                                            {m.nome}
                                            <span style={{ fontSize: '0.8rem', color: '#666' }}>ℹ️</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            <div className="summary-footer">
                <button className="btn-view-all" onClick={onOpenDetalhes}>
                    📖 Gerenciar Grimório Completo
                </button>
            </div>
        </div>
    );
};