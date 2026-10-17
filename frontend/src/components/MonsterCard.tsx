import React from 'react';
import type { Ameaca } from '../types';
import { Link } from 'react-router-dom';

interface MonsterCardProps {
    ameaca: Ameaca;
}

export const MonsterCard: React.FC<MonsterCardProps> = ({ ameaca }) => {

    const enviarParaRoll20 = (e: React.MouseEvent) => {
        e.preventDefault(); 
        e.stopPropagation(); 

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

    return (
        <Link to={`/ameaca/${ameaca._id}`} style={{ textDecoration: 'none', color: 'inherit', height: '100%' }}>
            <div 
                className="char-card" 
                style={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column', 
                    justifyContent: 'space-between',
                    padding: '20px',
                    transition: 'all 0.2s ease',
                    border: '1px solid #333'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--accent-color)';
                    e.currentTarget.style.transform = 'translateY(-4px)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#333';
                    e.currentTarget.style.transform = 'translateY(0)';
                }}
            >
                <div>
                    {/* Cabeçalho: Nome e ND */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '10px', marginBottom: '8px' }}>
                        <h2 style={{ 
                            margin: 0, 
                            color: '#e0e0e0', 
                            fontSize: '1.3rem', 
                            whiteSpace: 'normal', // Permite quebra de linha para nomes longos
                            lineHeight: '1.2',
                            wordBreak: 'break-word'
                        }}>
                            {ameaca.nome}
                        </h2>
                        <div style={{ 
                            background: 'var(--accent-color)', 
                            color: 'white', 
                            padding: '4px 8px', 
                            borderRadius: '6px', 
                            fontWeight: 'bold', 
                            fontSize: '0.8rem',
                            whiteSpace: 'nowrap',
                            flexShrink: 0
                        }}>
                            ND {ameaca.nd}
                        </div>
                    </div>

                    {/* Subtítulo: Tipo, Subtipo e Tamanho */}
                    <div style={{ color: '#888', fontSize: '0.85rem', marginBottom: '15px' }}>
                        {ameaca.tipo} {ameaca.subtipo ? `(${ameaca.subtipo})` : ''} • {ameaca.tamanho}
                    </div>

                    {/* Stats Básicos */}
                    <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
                        <div style={{ flex: 1, background: 'rgba(211, 47, 47, 0.1)', color: '#ef9a9a', padding: '6px', borderRadius: '6px', textAlign: 'center', fontWeight: 'bold', fontSize: '0.85rem', border: '1px solid #d32f2f' }}>
                            PV: {ameaca.pontos_de_vida}
                        </div>
                        <div style={{ flex: 1, background: 'rgba(46, 125, 50, 0.1)', color: '#a5d6a7', padding: '6px', borderRadius: '6px', textAlign: 'center', fontWeight: 'bold', fontSize: '0.85rem', border: '1px solid #2e7d32' }}>
                            Defesa: {ameaca.defesa}
                        </div>
                    </div>

                    {/* Atributos */}
                    <div style={{ background: '#1a1a1a', padding: '10px', borderRadius: '6px', fontSize: '0.85rem', color: '#aaa', textAlign: 'center', lineHeight: '1.4', border: '1px solid #2a2a2a' }}>
                        <strong>FOR</strong> {ameaca.atributos.forca ?? '—'} &nbsp;•&nbsp; <strong>DES</strong> {ameaca.atributos.destreza ?? '—'} &nbsp;•&nbsp; <strong>CON</strong> {ameaca.atributos.constituicao ?? '—'}<br />
                        <strong>INT</strong> {ameaca.atributos.inteligencia ?? '—'} &nbsp;•&nbsp; <strong>SAB</strong> {ameaca.atributos.sabedoria ?? '—'} &nbsp;•&nbsp; <strong>CAR</strong> {ameaca.atributos.carisma ?? '—'}
                    </div>
                </div>

                {/* Botão do Roll20 */}
                <div style={{ marginTop: '20px' }}>
                    <button 
                        onClick={enviarParaRoll20}
                        style={{ 
                            width: '100%', 
                            padding: '10px', 
                            background: 'var(--accent-color)', // Vermelho Tormenta
                            color: '#fff', 
                            border: 'none', 
                            borderRadius: '6px', 
                            cursor: 'pointer', 
                            fontWeight: 'bold',
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px',
                            fontSize: '0.85rem',
                            transition: 'background 0.2s'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = 'var(--accent-hover)'}
                        onMouseLeave={(e) => e.currentTarget.style.background = 'var(--accent-color)'}
                    >
                        📤 Enviar pro Roll20
                    </button>
                </div>
            </div>
        </Link>
    );
};
