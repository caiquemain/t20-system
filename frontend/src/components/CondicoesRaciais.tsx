import React from 'react';
import { T20Icon, type IconName } from './T20Icon';

// Espelha o registro do backend (pericias.py / custo_magia.py)
const CONDICAO_POR_HABILIDADE: Record<string, string> = {
    'Conhecimento das Rochas': 'subterraneo',
    'Reptiliano': 'sem_armadura',
    'Magia Instintiva': 'magia_instintiva_sab',
};
const CONDICOES: Record<string, { label: string; icone: IconName; desc: string }> = {
    subterraneo: { label: 'No subterrâneo', icone: 'escalada', desc: '+2 Percepção/Sobrevivência (Conhecimento das Rochas)' },
    sem_armadura: { label: 'Sem armadura ou roupas pesadas', icone: 'voo', desc: '+5 Furtividade (Reptiliano)' },
    magia_instintiva_sab: { label: 'Usar Sabedoria (Magias Arcanas e Misticismo)', icone: 'magia', desc: 'Troca o atributo-chave de magias arcanas (CD e PM) e Misticismo para SAB' },
};

interface Props { ficha: any; updateFicha: (d: any) => void; }

export const CondicoesRaciais: React.FC<Props> = ({ ficha, updateFicha }) => {
    const nomesHabs = (ficha.habilidades || []).map((h: any) => h.nome);
    const relevantes = Object.entries(CONDICAO_POR_HABILIDADE).filter(([hab]) => nomesHabs.includes(hab));
    if (relevantes.length === 0) return null;
    const ativas: string[] = ficha.condicoes_ativas || [];
    const toggle = (id: string) => {
        const ligando = !ativas.includes(id);
        const nova = ligando ? [...ativas, id] : ativas.filter(x => x !== id);
        if (id === 'magia_instintiva_sab' && ficha.pericias?.Misticismo) {
            updateFicha({
                condicoes_ativas: nova,
                pericias: {
                    ...ficha.pericias,
                    Misticismo: {
                        ...ficha.pericias.Misticismo,
                        atributo_chave: ligando ? 'sab' : 'int',
                    },
                },
            });
            return;
        }
        updateFicha({ condicoes_ativas: nova });
    };
    return (
        <div className="section-card" style={{ padding: 12, marginBottom: 15 }}>
            <h3 style={{ margin: '0 0 10px 0', fontSize: '1rem', color: '#fff', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <T20Icon name="filtro" size={16} color="#2196f3" /> Condições Situacionais
            </h3>
            {relevantes.map(([hab, id]) => {
                const ativa = ativas.includes(id);
                const meta = CONDICOES[id] || { label: id, icone: 'info' as IconName, desc: '' };
                return (
                    <div key={id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', borderTop: '1px solid #333' }}>
                        <button onClick={() => toggle(id)} style={{
                            padding: '4px 12px', borderRadius: 4, border: '1px solid #444', cursor: 'pointer',
                            background: ativa ? '#4caf50' : '#333', color: ativa ? '#000' : '#888', fontWeight: 'bold'
                        }}>{ativa ? 'ON' : 'OFF'}</button>
                        <div>
                            <div style={{ color: ativa ? '#a5d6a7' : '#ccc', fontSize: '0.85rem', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                                <T20Icon name={meta.icone} size={14} /> {meta.label}
                            </div>
                            <div style={{ color: '#777', fontSize: '0.7rem' }}>{hab}: {meta.desc}</div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};
