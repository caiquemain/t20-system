import React from 'react';
import type { Ameaca } from '../types';
import { Link } from 'react-router-dom';

interface MonsterCardProps {
    ameaca: Ameaca;
}

const TYPE_COLORS: Record<string, string> = {
    'Morto-vivo': '#ba68c8', 'Dragão': '#e57373', 'Monstro': '#ffb74d',
    'Aberração': '#26c6da', 'Animal': '#81c784', 'Construto': '#9e9e9e',
    'Elemental': '#4fc3f7', 'Fada': '#f06292', 'Gigante': '#a1887f',
    'Humanoide': '#fff176', 'Espírito': '#9575cd', 'Lefou': '#a5d6a7',
};

const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#d32f2f';
    const key = Object.keys(TYPE_COLORS).find(k => tipo.toLowerCase().includes(k.toLowerCase()));
    return key ? TYPE_COLORS[key] : '#d32f2f';
};

export const MonsterCard: React.FC<MonsterCardProps> = ({ ameaca }) => {
    const typeColor = getTypeColor(ameaca.tipo);

    const enviarParaRoll20 = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();

        window.postMessage({ type: 'T20_ENVIAR_AMEACA_ROLL20', ameaca }, '*');

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
        setTimeout(() => window.removeEventListener('message', handleResposta), 5000);
    };

    return (
        <Link to={`/ameaca/${ameaca._id}`} style={{ textDecoration: 'none', color: 'inherit', height: '100%' }}>
            <div
                className="spell-card"
                style={{
                    background: '#1e1e1e',
                    borderLeft: `4px solid ${typeColor}`,
                    borderTop: '1px solid #333',
                    borderRight: '1px solid #333',
                    borderBottom: '1px solid #333',
                    borderRadius: '6px',
                    padding: '14px 16px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    height: '100%',
                    minHeight: '140px'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = '#2a2a2a'}
                onMouseLeave={(e) => e.currentTarget.style.background = '#1e1e1e'}
            >
                <div>
                    {/* Cabeçalho: Nome na esquerda, ND na direita */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px', marginBottom: '6px' }}>
                        <div style={{ flex: 1, minWidth: 0 }}>
                            <span style={{
                                fontWeight: 'bold',
                                color: '#e0e0e0',
                                fontSize: '1.05rem',
                                lineHeight: '1.2',
                                display: 'block'
                            }} title={ameaca.nome}>
                                {ameaca.nome}
                            </span>
                        </div>
                        <span style={{
                            fontSize: '0.75rem',
                            color: '#ff8a80',
                            fontWeight: 'bold',
                            background: 'rgba(211, 47, 47, 0.15)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(211, 47, 47, 0.4)',
                            whiteSpace: 'nowrap'
                        }}>
                            ND {ameaca.nd}
                        </span>
                    </div>

                    {/* Subtítulo: Tipo e Tamanho */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap', marginBottom: '12px' }}>
                        <span style={{ fontSize: '0.75rem', color: typeColor, textTransform: 'uppercase', fontWeight: 'bold' }}>
                            {ameaca.tipo}
                        </span>
                        <span style={{ fontSize: '0.65rem', color: '#888', textTransform: 'uppercase', border: '1px solid #444', padding: '1px 4px', borderRadius: '3px' }}>
                            {ameaca.tamanho}
                        </span>
                    </div>

                    {/* Stats Rápidos (Horizontal) */}
                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.85rem', color: '#aaa', marginBottom: '8px' }}>
                        <span>❤️ <strong style={{ color: '#ef9a9a' }}>{ameaca.pontos_de_vida}</strong></span>
                        <span>🛡️ <strong style={{ color: '#a5d6a7' }}>{ameaca.defesa}</strong></span>
                    </div>

                    {/* Atributos em linha única (igual ao rodapé do Grimório) */}
                    <div style={{ 
                        fontSize: '0.75rem', 
                        color: '#888', 
                        display: 'flex', 
                        flexWrap: 'wrap', 
                        gap: '8px'
                    }}>
                        <span><strong style={{ color: '#bbb' }}>FOR</strong> {ameaca.atributos.forca ?? '—'}</span>
                        <span><strong style={{ color: '#bbb' }}>DES</strong> {ameaca.atributos.destreza ?? '—'}</span>
                        <span><strong style={{ color: '#bbb' }}>CON</strong> {ameaca.atributos.constituicao ?? '—'}</span>
                        <span><strong style={{ color: '#bbb' }}>INT</strong> {ameaca.atributos.inteligencia ?? '—'}</span>
                        <span><strong style={{ color: '#bbb' }}>SAB</strong> {ameaca.atributos.sabedoria ?? '—'}</span>
                        <span><strong style={{ color: '#bbb' }}>CAR</strong> {ameaca.atributos.carisma ?? '—'}</span>
                    </div>
                </div>

                {/* Botão do Roll20 bem discreto (estilo badge) */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
                    <button
                        onClick={enviarParaRoll20}
                        title="Enviar para o Roll20"
                        style={{
                            padding: '4px 8px',
                            background: 'transparent',
                            color: '#888',
                            border: '1px solid #444',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '0.65rem',
                            textTransform: 'uppercase',
                            transition: 'all 0.2s',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.borderColor = '#d32f2f';
                            e.currentTarget.style.color = '#ff8a80';
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.borderColor = '#444';
                            e.currentTarget.style.color = '#888';
                        }}
                    >
                        📤 Roll20
                    </button>
                </div>
            </div>
        </Link>
    );
};
