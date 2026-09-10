import React from 'react';

interface AtaqueView {
    nome: string; bonus_ataque: string; dano: string; critico: string;
    tipo: string; alcance: string; teste: string; especial?: string;
}

interface AttackListProps {
    ataques: AtaqueView[];
    fluxoDeMana?: boolean;
    focoVital?: boolean;
}

export const AttackList: React.FC<AttackListProps> = ({ ataques, fluxoDeMana, focoVital }) => (
    <div className="section-card" style={{ marginTop: 25 }}>
        <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <h3 className="section-title" style={{ margin: 0 }}>⚔️ Ataques</h3>
            <div style={{ display: 'flex', gap: 6 }}>
                {fluxoDeMana && (
                    <span style={{ fontSize: '0.7rem', color: '#80deea', background: 'rgba(0,188,212,0.1)', border: '1px solid rgba(0,188,212,0.4)', padding: '2px 8px', borderRadius: 4 }}>🌊 Fluxo de Mana</span>
                )}
                {focoVital && (
                    <span style={{ fontSize: '0.7rem', color: '#ef9a9a', background: 'rgba(244,67,54,0.1)', border: '1px solid rgba(244,67,54,0.4)', padding: '2px 8px', borderRadius: 4 }}>❤️ Foco Vital</span>
                )}
            </div>
        </div>
        {(!ataques || ataques.length === 0) ? (
            <p style={{ color: '#666', textAlign: 'center', fontSize: '0.85rem' }}>Nenhum ataque ou poder ofensivo.</p>
        ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                    <tr style={{ color: '#888', textTransform: 'uppercase', fontSize: '0.7rem' }}>
                        {['Arma / Poder', 'Bônus', 'Dano', 'Crít.', 'Tipo', 'Alcance', 'Teste'].map(h => (
                            <th key={h} style={{ textAlign: 'left', padding: '4px 6px', borderBottom: '1px solid #333' }}>{h}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {ataques.map((a, i) => (
                        <tr key={i} style={{ borderBottom: '1px solid #252525' }}>
                            <td style={{ padding: '6px' }}>
                                <strong style={{ color: '#e0e0e0' }}>{a.nome}</strong>
                                {a.especial && <div style={{ fontSize: '0.7rem', color: '#888', marginTop: 2 }}>{a.especial}</div>}
                            </td>
                            <td style={{ padding: '6px', color: '#ccc' }}>{a.bonus_ataque}</td>
                            <td style={{ padding: '6px', color: '#ffcc80', fontWeight: 'bold' }}>{a.dano}</td>
                            <td style={{ padding: '6px', color: '#ccc' }}>{a.critico}</td>
                            <td style={{ padding: '6px', color: '#ccc' }}>{a.tipo}</td>
                            <td style={{ padding: '6px', color: '#ccc' }}>{a.alcance}</td>
                            <td style={{ padding: '6px', color: '#ccc' }}>{a.teste}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        )}
    </div>
);
