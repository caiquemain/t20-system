import React from 'react';

// Espelha o registro do backend (pericias.py)
const CONDICAO_POR_HABILIDADE: Record<string, string> = {
    'Conhecimento das Rochas': 'subterraneo',
    'Reptiliano': 'sem_armadura',
};
const CONDICOES: Record<string, { label: string; icone: string; desc: string }> = {
    subterraneo: { label: 'No subterrâneo', icone: '⛰️', desc: '+2 Percepção/Sobrevivência (Conhecimento das Rochas)' },
    sem_armadura: { label: 'Sem armadura ou roupas pesadas', icone: '🪽', desc: '+5 Furtividade (Reptiliano)' },
};

interface Props { ficha: any; updateFicha: (d: any) => void; }

export const CondicoesRaciais: React.FC<Props> = ({ ficha, updateFicha }) => {
    const nomesHabs = (ficha.habilidades || []).map((h: any) => h.nome);
    const relevantes = Object.entries(CONDICAO_POR_HABILIDADE).filter(([hab]) => nomesHabs.includes(hab));
    if (relevantes.length === 0) return null;
    const ativas: string[] = ficha.condicoes_ativas || [];
    const toggle = (id: string) => {
        const nova = ativas.includes(id) ? ativas.filter(x => x !== id) : [...ativas, id];
        updateFicha({ condicoes_ativas: nova });
    };
    return (
        <div className="section-card" style={{ padding: 12, marginBottom: 15 }}>
            <h3 style={{ margin: '0 0 10px 0', fontSize: '1rem', color: '#fff' }}>🎚️ Condições Situacionais</h3>
            {relevantes.map(([hab, id]) => {
                const ativa = ativas.includes(id);
                const meta = CONDICOES[id] || { label: id, icone: '❓', desc: '' };
                return (
                    <div key={id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', borderTop: '1px solid #333' }}>
                        <button onClick={() => toggle(id)} style={{
                            padding: '4px 12px', borderRadius: 4, border: '1px solid #444', cursor: 'pointer',
                            background: ativa ? '#4caf50' : '#333', color: ativa ? '#000' : '#888', fontWeight: 'bold'
                        }}>{ativa ? 'ON' : 'OFF'}</button>
                        <div>
                            <div style={{ color: ativa ? '#a5d6a7' : '#ccc', fontSize: '0.85rem' }}>{meta.icone} {meta.label}</div>
                            <div style={{ color: '#777', fontSize: '0.7rem' }}>{hab}: {meta.desc}</div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};
