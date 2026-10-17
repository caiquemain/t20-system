import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchAmeaca } from '../services/api';
import type { Ameaca } from '../types';

const AmeacaDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [ameaca, setAmeaca] = useState<Ameaca | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (id) {
            fetchAmeaca(id)
                .then(res => {
                    setAmeaca(res.data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Erro ao carregar ameaça:", err);
                    setLoading(false);
                });
        }
    }, [id]);

    const enviarParaRoll20 = () => {
        if (!ameaca) return;
        
        // Envia a mensagem para o content script
        window.postMessage({ type: 'T20_ENVIAR_AMEACA_ROLL20', ameaca }, '*');

        // Escuta a resposta
        const handleResposta = (event: MessageEvent) => {
            if (event.source !== window) return;
            if (event.data && event.data.type === 'T20_RESPOSTA_ROLL20') {
                window.removeEventListener('message', handleResposta);
                if (event.data.ok) {
                    alert(`✅ ${ameaca.nome} enviado para o Roll20 com sucesso!`);
                } else {
                    alert(`❌ Erro ao enviar: ${event.data.err || 'Verifique se uma ficha do Roll20 está aberta.'}`);
                }
            }
        };
        window.addEventListener('message', handleResposta);

        setTimeout(() => {
            window.removeEventListener('message', handleResposta);
        }, 5000);
    };

    if (loading) return <p className="container">Carregando ficha...</p>;
    if (!ameaca) return <p className="container">Monstro não encontrado.</p>;

    return (
        <div className="container" style={{ maxWidth: '900px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                <Link to="/bestiario" style={{ color: 'var(--text-secondary)' }}>⬅ Voltar ao Bestiário</Link>
                <button onClick={enviarParaRoll20} style={{ background: '#9c27b0', color: '#fff', padding: '8px 16px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>
                    📤 Enviar pro Roll20
                </button>
            </div>

            <div className="card-form" style={{ padding: '30px' }}>
                <div style={{ borderBottom: '2px solid var(--accent-color)', paddingBottom: '10px', marginBottom: '20px' }}>
                    <h1 style={{ margin: 0, color: 'var(--accent-color)', fontSize: '2.5rem' }}>{ameaca.nome}</h1>
                    <div style={{ fontSize: '1.2rem', color: '#aaa', marginTop: '5px' }}>
                        {ameaca.tipo} {ameaca.subtipo ? `(${ameaca.subtipo})` : ''} {ameaca.tamanho} • <strong style={{ color: '#fff' }}>ND {ameaca.nd}</strong>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', textAlign: 'center', marginBottom: '20px' }}>
                    <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>PV</strong><br/>{ameaca.pontos_de_vida}</div>
                    <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Defesa</strong><br/>{ameaca.defesa}</div>
                    <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Deslocamento</strong><br/>{ameaca.deslocamento}</div>
                    <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Iniciativa</strong><br/>{ameaca.iniciativa > 0 ? `+${ameaca.iniciativa}` : ameaca.iniciativa}</div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', textAlign: 'center', marginBottom: '20px', color: '#ccc', fontSize: '0.9rem' }}>
                    <div><strong>Fort:</strong> {ameaca.fortitude > 0 ? `+${ameaca.fortitude}` : ameaca.fortitude}</div>
                    <div><strong>Ref:</strong> {ameaca.reflexos > 0 ? `+${ameaca.reflexos}` : ameaca.reflexos}</div>
                    <div><strong>Von:</strong> {ameaca.vontade > 0 ? `+${ameaca.vontade}` : ameaca.vontade}</div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-around', background: '#1a1a1a', padding: '15px', borderRadius: '8px', marginBottom: '30px', border: '1px solid #333' }}>
                    {Object.entries(ameaca.atributos).map(([key, val]) => (
                        <div key={key} style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '0.8rem', color: '#888', textTransform: 'uppercase' }}>{key}</div>
                            <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>{val ?? '—'}</div>
                        </div>
                    ))}
                </div>

                {ameaca.ataques && ameaca.ataques.length > 0 && (
                    <div style={{ marginBottom: '30px' }}>
                        <h2 style={{ color: 'var(--accent-color)', borderBottom: '1px solid #333', paddingBottom: '5px' }}>Ações de Combate</h2>
                        {ameaca.ataques.map((atk, i) => (
                            <div key={i} style={{ marginBottom: '10px', color: '#ccc' }}>
                                <strong style={{ color: '#fff' }}>{atk.nome}</strong> ({atk.modalidade}) — 
                                Ataque: <strong>+{atk.bonus_ataque}</strong>, 
                                Dano: <strong>{atk.dano} {atk.tipo_dano}</strong>, 
                                Crítico: {atk.margem_critico}/x{atk.multiplicador_critico}
                                {atk.descricao && <span style={{ color: '#888' }}> ({atk.descricao})</span>}
                            </div>
                        ))}
                    </div>
                )}

                {ameaca.habilidades && ameaca.habilidades.length > 0 && (
                    <div style={{ marginBottom: '30px' }}>
                        <h2 style={{ color: 'var(--accent-color)', borderBottom: '1px solid #333', paddingBottom: '5px' }}>Habilidades</h2>
                        {ameaca.habilidades.map((hab, i) => (
                            <div key={i} style={{ marginBottom: '15px', color: '#ccc', lineHeight: '1.5' }}>
                                <strong style={{ color: '#fff' }}>{hab.nome}</strong> 
                                <span style={{ fontSize: '0.8rem', color: '#888', marginLeft: '10px' }}>({hab.tipo_acao})</span> — 
                                {hab.descricao}
                                {hab.rolls && hab.rolls.length > 0 && (
                                    <span style={{ marginLeft: '5px', color: '#9c27b0', fontWeight: 'bold' }}>[{hab.rolls.join(', ')}]</span>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {ameaca.tesouro && (
                    <div style={{ marginTop: '30px', paddingTop: '15px', borderTop: '1px solid #333', color: '#aaa' }}>
                        <strong>Tesouro:</strong> {ameaca.tesouro}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AmeacaDetail;
