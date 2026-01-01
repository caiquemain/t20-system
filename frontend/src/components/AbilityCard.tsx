import React from 'react';
import type { Habilidade } from '../types';

interface AbilityCardProps {
    habilidade: Habilidade;
    pmAtual: number;
    onAtivar: (custo: number, nome: string) => void;
}

export const AbilityCard: React.FC<AbilityCardProps> = ({ habilidade, pmAtual, onAtivar }) => {
    const ativavel = habilidade.efeitos?.habilidade_ativavel;
    const podePagar = ativavel ? pmAtual >= ativavel.custo : false;

    // Define cor baseada no tipo de ação (Visual T20)
    const getActionColor = (acao?: string) => {
        const a = acao?.toLowerCase() || '';
        if (a.includes('padrão')) return '#d32f2f'; // Vermelho
        if (a.includes('movimento')) return '#fbc02d'; // Amarelo/Dourado
        if (a.includes('livre') || a.includes('reac')) return '#388e3c'; // Verde
        if (a.includes('completa')) return '#7b1fa2'; // Roxo
        return '#666';
    };

    console.log(`Habilidade: ${habilidade.nome}`, habilidade.efeitos);

    return (
        <div style={{
            background: '#1e1e1e',
            borderRadius: '8px',
            marginBottom: '10px',
            border: '1px solid #333',
            overflow: 'hidden'
        }}>
            {/* Cabeçalho */}
            <div style={{
                padding: '10px 15px',
                background: '#252525',
                borderBottom: '1px solid #333',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <span style={{ fontWeight: 'bold', color: '#e0e0e0' }}>{habilidade.nome}</span>
                <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase' }}>
                    {habilidade.tipo}
                </span>
            </div>

            {/* Descrição */}
            <div style={{ padding: '15px', color: '#ccc', fontSize: '0.9rem', lineHeight: '1.5' }}>
                {habilidade.descricao}

                {/* Seção de Regras Extras (Alcance, CD, etc) se for ativável */}
                {ativavel && (
                    <div style={{ marginTop: '10px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                        {ativavel.alcance && <Badge label="Alcance" value={ativavel.alcance} />}
                        {ativavel.duracao && <Badge label="Duração" value={ativavel.duracao} />}
                        {ativavel.resistencia && <Badge label="Resistência" value={ativavel.resistencia} />}
                    </div>
                )}
            </div>

            {/* Botão de Ativação (Só renderiza se for ativável) */}
            {ativavel && (
                <div style={{
                    padding: '10px 15px',
                    background: '#1a1a1a',
                    borderTop: '1px solid #333',
                    display: 'flex',
                    justifyContent: 'flex-end'
                }}>
                    <button
                        onClick={() => onAtivar(ativavel.custo, habilidade.nome)}
                        disabled={!podePagar}
                        style={{
                            background: podePagar ? 'transparent' : 'rgba(255,255,255,0.05)',
                            border: `1px solid ${podePagar ? getActionColor(ativavel.acao) : '#444'}`,
                            color: podePagar ? getActionColor(ativavel.acao) : '#666',
                            padding: '6px 12px',
                            borderRadius: '4px',
                            cursor: podePagar ? 'pointer' : 'not-allowed',
                            fontWeight: 'bold',
                            fontSize: '0.85rem',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.2s'
                        }}
                        onMouseOver={(e) => {
                            if (podePagar) {
                                e.currentTarget.style.background = getActionColor(ativavel.acao);
                                e.currentTarget.style.color = '#111';
                            }
                        }}
                        onMouseOut={(e) => {
                            if (podePagar) {
                                e.currentTarget.style.background = 'transparent';
                                e.currentTarget.style.color = getActionColor(ativavel.acao);
                            }
                        }}
                    >
                        <span>⚡ {ativavel.custo} PM</span>
                        <span style={{
                            borderLeft: `1px solid ${podePagar ? 'currentColor' : '#444'}`,
                            paddingLeft: '8px',
                            opacity: 0.8
                        }}>
                            {ativavel.acao || 'Livre'}
                        </span>
                    </button>
                </div>
            )}
        </div>
    );
};

const Badge = ({ label, value }: { label: string, value: string }) => (
    <span style={{ fontSize: '0.75rem', color: '#888', background: '#222', padding: '2px 6px', borderRadius: '4px', border: '1px solid #333' }}>
        <strong>{label}:</strong> {value}
    </span>
);