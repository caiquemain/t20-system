import React, { useState, useMemo } from 'react';
import type { Magia } from '../types';

interface SpellListProps {
    magias: Magia[];
    onRemove: (nome: string) => void;
}

// Mapa de cores por Escola de Magia (Tormenta 20)
const SCHOOL_COLORS: Record<string, string> = {
    'Abjuração': '#2196f3',   // Azul Protetor
    'Adivinhação': '#00bcd4', // Ciano Etéreo
    'Convocação': '#ff9800',  // Laranja Invocação
    'Encantamento': '#e91e63',// Rosa Mental
    'Evocação': '#f44336',    // Vermelho Destrutivo
    'Ilusão': '#9c27b0',      // Roxo Misterioso
    'Necromancia': '#4caf50', // Verde Tóxico
    'Transmutação': '#ffeb3b',// Amarelo Mudança
    'default': '#9e9e9e'      // Cinza Padrão
};

export const SpellList: React.FC<SpellListProps> = ({ magias, onRemove }) => {
    const [expanded, setExpanded] = useState<string | null>(null);

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

    const toggleExpand = (nome: string) => {
        setExpanded(prev => prev === nome ? null : nome);
    };

    const getSchoolColor = (escola: string) => {
        // Tenta achar a cor exata ou pega a default
        const key = Object.keys(SCHOOL_COLORS).find(k => escola.includes(k)) || 'default';
        return SCHOOL_COLORS[key];
    };

    const renderMagiaCard = (magia: Magia) => {
        const isExpanded = expanded === magia.nome;
        const schoolColor = getSchoolColor(magia.escola);

        return (
            <div
                key={magia.nome}
                onClick={() => toggleExpand(magia.nome)}
                className="spell-card"
                style={{
                    marginBottom: '10px',
                    borderRadius: '8px',
                    background: isExpanded ? 'linear-gradient(145deg, #1e1e1e, #252525)' : '#1a1a1a',
                    border: '1px solid #333',
                    borderLeft: `4px solid ${schoolColor}`, // Identidade visual da escola
                    boxShadow: isExpanded ? `0 4px 15px -5px ${schoolColor}40` : 'none', // Glow sutil
                    cursor: 'pointer',
                    overflow: 'hidden',
                    transition: 'all 0.3s ease'
                }}
            >
                {/* CABEÇALHO */}
                <div style={{ padding: '12px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        {/* Ícone do Círculo */}
                        <div style={{
                            width: '28px', height: '28px', borderRadius: '6px',
                            background: '#111', border: `1px solid ${schoolColor}80`, color: schoolColor,
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontWeight: '900', fontSize: '0.9rem', boxShadow: `inset 0 0 5px ${schoolColor}20`
                        }}>
                            {magia.circulo}
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            <span style={{ fontWeight: 'bold', color: '#f0f0f0', fontSize: '1rem', letterSpacing: '0.5px' }}>
                                {magia.nome}
                            </span>
                            <span style={{ fontSize: '0.7rem', color: schoolColor, textTransform: 'uppercase', opacity: 0.8 }}>
                                {magia.escola}
                            </span>
                        </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <span style={{
                            background: '#111', color: '#ce93d8', padding: '2px 8px', borderRadius: '4px',
                            fontSize: '0.75rem', fontWeight: 'bold', border: '1px solid #333'
                        }}>
                            {magia.custo_pm} PM
                        </span>

                        <button
                            onClick={(e) => { e.stopPropagation(); onRemove(magia.nome); }}
                            title="Esquecer Magia"
                            className="btn-remove"
                        >
                            ✕
                        </button>
                    </div>
                </div>

                {/* CONTEÚDO EXPANDIDO */}
                {isExpanded && (
                    <div style={{
                        padding: '0 16px 16px 16px',
                        borderTop: '1px solid #333',
                        animation: 'slideDown 0.3s ease-out'
                    }}>
                        {/* Grid de Informações Técnicas */}
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))',
                            gap: '8px', margin: '15px 0'
                        }}>
                            <DetailItem label="Execução" value={magia.execucao} icon="⚡" />
                            <DetailItem label="Alcance" value={magia.alcance} icon="📏" />
                            <DetailItem label="Alvo/Área" value={magia.alvo || "—"} icon="🎯" />
                            <DetailItem label="Duração" value={magia.duracao} icon="⏳" />
                            <DetailItem label="Resistência" value={magia.resistencia || "Nenhuma"} icon="🛡️" />
                        </div>

                        {/* Descrição Textual */}
                        <div style={{
                            background: '#111', padding: '12px', borderRadius: '6px',
                            borderLeft: `2px solid ${schoolColor}`, color: '#ccc',
                            fontSize: '0.9rem', lineHeight: '1.6', whiteSpace: 'pre-wrap'
                        }}>
                            {magia.descricao}
                        </div>
                    </div>
                )}
            </div>
        );
    };

    const circulosAtivos = Object.entries(magiasPorCirculo).filter(([_, lista]) => lista.length > 0);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            {magias.length === 0 && (
                <div style={{ padding: '30px', textAlign: 'center', color: '#666', border: '2px dashed #333', borderRadius: '8px' }}>
                    <p style={{ fontSize: '1.2rem', marginBottom: '5px' }}>Grimório Vazio</p>
                    <p style={{ fontSize: '0.9rem' }}>Clique em "+ Adicionar Magias" para estudar novos feitiços.</p>
                </div>
            )}

            {circulosAtivos.map(([circulo, lista]) => (
                <div key={circulo}>
                    <div style={{
                        display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px',
                        borderBottom: '1px solid #333', paddingBottom: '5px'
                    }}>
                        <span style={{
                            background: '#9c27b0', color: 'white', width: '20px', height: '20px',
                            borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '0.7rem', fontWeight: 'bold'
                        }}>{circulo}</span>
                        <h4 style={{ margin: 0, color: '#e0e0e0', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
                            {circulo}º Círculo
                        </h4>
                    </div>
                    <div>
                        {lista.map(m => renderMagiaCard(m))}
                    </div>
                </div>
            ))}

            <style>{`
                @keyframes slideDown { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
                .btn-remove {
                    background: transparent; border: none; color: #555; cursor: pointer;
                    font-size: 1.1rem; padding: 4px; transition: color 0.2s;
                    display: flex; align-items: center; justify-content: center;
                    border-radius: 4px;
                }
                .btn-remove:hover { color: #ff5252; background: rgba(255, 82, 82, 0.1); }
                .spell-card:hover { border-color: #555 !important; }
            `}</style>
        </div>
    );
};

// Subcomponente para os Detalhes do Grid
const DetailItem = ({ label, value, icon }: { label: string, value: string, icon: string }) => (
    <div style={{ background: '#222', padding: '8px', borderRadius: '4px', border: '1px solid #333' }}>
        <div style={{ fontSize: '0.7rem', color: '#888', marginBottom: '2px', textTransform: 'uppercase', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span>{icon}</span> {label}
        </div>
        <div style={{ fontSize: '0.85rem', color: '#eee', fontWeight: '500', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={value}>
            {value}
        </div>
    </div>
);