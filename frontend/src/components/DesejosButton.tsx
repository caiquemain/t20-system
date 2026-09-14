import React, { useState } from 'react';

interface DesejosButtonProps {
    magiaAtual: string;
    magiasConhecidas: string[];
    reducao: number;
    onEscolher: (nome: string) => void;
}

export const DesejosButton: React.FC<DesejosButtonProps> = ({ magiaAtual, magiasConhecidas, reducao, onEscolher }) => {
    const [aberto, setAberto] = useState(false);
    const [busca, setBusca] = useState('');
    const filtradas = magiasConhecidas.filter(m => m.toLowerCase().includes(busca.toLowerCase())).sort();

    return (
        <div style={{ marginTop: 8 }}>
            <button className="btn-action" style={{ background: '#ff9800', color: '#000', fontWeight: 'bold' }} onClick={() => setAberto(true)}>
                {magiaAtual ? `🧞 Desejo ativo: ${magiaAtual} (trocar)` : '🧞 Solicitar Desejo'}
            </button>
            {magiaAtual && (
                <button className="btn-action" style={{ background: '#d32f2f', marginLeft: 6 }} onClick={() => onEscolher('')}>
                    Remover
                </button>
            )}
            {aberto && (
                <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 9999 }} onClick={() => setAberto(false)}>
                    <div style={{ background: '#1a1a1a', border: '1px solid #ff9800', padding: 20, borderRadius: 8, maxWidth: 480, width: '90%', maxHeight: '80vh', display: 'flex', flexDirection: 'column' }} onClick={e => e.stopPropagation()}>
                        <h3 style={{ margin: '0 0 6px 0', color: '#ff9800' }}>🧞 Magia Desejada</h3>
                        <p style={{ fontSize: '0.8rem', color: '#ccc', margin: '0 0 10px 0' }}>
                            Se lançar a magia que alguém pediu, o custo diminui em −{reducao} PM.
                        </p>
                        <input className="input-dark" placeholder="Buscar magia conhecida..." value={busca} onChange={e => setBusca(e.target.value)} style={{ marginBottom: 8 }} />
                        <div style={{ overflowY: 'auto', flex: 1, border: '1px solid #333', borderRadius: 4 }}>
                            {filtradas.length === 0 && <p style={{ color: '#888', padding: 12, textAlign: 'center' }}>Nenhuma magia conhecida no Grimório.</p>}
                            {filtradas.map(nome => (
                                <div key={nome} onClick={() => { onEscolher(nome); setAberto(false); setBusca(''); }}
                                    style={{ padding: '8px 12px', cursor: 'pointer', borderBottom: '1px solid #2a2a2a', background: nome === magiaAtual ? 'rgba(255,152,0,0.25)' : 'transparent', color: nome === magiaAtual ? '#ff9800' : '#eee' }}>
                                    {nome === magiaAtual ? '🧞 ' : ''}{nome}
                                </div>
                            ))}
                        </div>
                        <button className="btn-action" style={{ marginTop: 10, background: '#444' }} onClick={() => setAberto(false)}>Fechar</button>
                    </div>
                </div>
            )}
        </div>
    );
};
