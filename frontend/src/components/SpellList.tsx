import React, { useState, useMemo } from 'react';
import type { Magia } from '../types';

interface SpellListProps {
    magias: Magia[];
    onRemove: (nome: string) => void;
}

// Cores por Escola (Identidade Visual T20)
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

// Função auxiliar para definir a cor baseada no Tipo
const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#e0e0e0';
    const t = tipo.toLowerCase();
    if (t.includes('arcana')) return '#d236d2'; // Roxo/Magenta
    if (t.includes('divina')) return '#ffc107'; // Dourado
    return '#ff5252'; // Universal
};

export const SpellList: React.FC<SpellListProps> = ({ magias, onRemove }) => {
    const [expanded, setExpanded] = useState<string | null>(null);

    // Agrupamento por Círculo
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
        const key = Object.keys(SCHOOL_COLORS).find(k => escola && escola.includes(k)) || 'default';
        return SCHOOL_COLORS[key];
    };

    const renderMagiaCard = (magia: Magia) => {
        const isExpanded = expanded === magia.nome;
        const schoolColor = getSchoolColor(magia.escola);
        const typeColor = getTypeColor(magia.tipo);

        return (
            <div
                key={magia.nome}
                className="spell-card"
                onClick={() => toggleExpand(magia.nome)}
                style={{
                    position: 'relative',
                    background: isExpanded ? '#252525' : '#1e1e1e',
                    borderLeft: `4px solid ${schoolColor}`, // Identidade da Escola
                    borderBottom: '1px solid #333',
                    marginBottom: '2px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    padding: '10px 14px'
                }}
            >
                {/* CABEÇALHO DO CARD */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>

                    {/* Lado Esquerdo: Nome + Tipo + Escola */}
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontWeight: 'bold', color: '#e0e0e0', fontSize: '1rem' }}>
                                {magia.nome}
                            </span>

                            {/* Badge de Tipo (Arcana/Divina) */}
                            <span style={{
                                fontSize: '0.65rem', textTransform: 'uppercase', fontWeight: 'bold',
                                color: typeColor, border: `1px solid ${typeColor}60`,
                                padding: '1px 5px', borderRadius: '3px', lineHeight: 1
                            }}>
                                {magia.tipo || 'UNIV'}
                            </span>
                        </div>

                        <span style={{ fontSize: '0.75rem', color: schoolColor, opacity: 0.9, marginTop: '2px' }}>
                            {magia.escola} • {magia.execucao}
                        </span>
                    </div>

                    {/* Lado Direito: PM e Botão Remover */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <span style={{
                            fontSize: '0.85rem', color: '#ce93d8', fontWeight: 'bold',
                            background: 'rgba(156, 39, 176, 0.15)', padding: '3px 8px', borderRadius: '4px',
                            border: '1px solid rgba(156, 39, 176, 0.3)'
                        }}>
                            {magia.custo_pm} PM
                        </span>

                        {/* Botão de Remover (Aparece sempre ou só no hover/expandido) */}
                        {isExpanded && (
                            <button
                                onClick={(e) => { e.stopPropagation(); onRemove(magia.nome); }}
                                style={{
                                    background: 'transparent', border: 'none', color: '#666',
                                    cursor: 'pointer', fontSize: '1.2rem', padding: '0 5px',
                                    lineHeight: '1', display: 'flex', alignItems: 'center'
                                }}
                                title="Esquecer Magia"
                                onMouseOver={(e) => e.currentTarget.style.color = '#ef5350'}
                                onMouseOut={(e) => e.currentTarget.style.color = '#666'}
                            >
                                ✕
                            </button>
                        )}
                    </div>
                </div>

                {/* CONTEÚDO EXPANDIDO (Detalhes Completos) */}
                {isExpanded && (
                    <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #333', animation: 'slideDown 0.2s ease-out' }}>

                        {/* Grid de Stats */}
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
                            gap: '10px', marginBottom: '15px'
                        }}>
                            <MiniDetail label="Alcance" value={magia.alcance} />
                            <MiniDetail label="Alvo/Área" value={magia.alvo || magia.alvo_area || '-'} />
                            <MiniDetail label="Duração" value={magia.duracao} />
                            <MiniDetail label="Resistência" value={magia.resistencia || "-"} />
                        </div>

                        {/* Descrição */}
                        <div style={{
                            background: '#111', padding: '12px', borderRadius: '6px',
                            borderLeft: `2px solid ${schoolColor}50`, // Borda sutil interna
                            border: '1px solid #333'
                        }}>
                            <p style={{ margin: 0, fontSize: '0.9rem', color: '#ccc', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                                {magia.descricao}
                            </p>
                        </div>
                    </div>
                )}
            </div>
        );
    };

    const circulosAtivos = Object.entries(magiasPorCirculo).filter(([_, lista]) => lista.length > 0);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {magias.length === 0 && (
                <div style={{ padding: '40px', textAlign: 'center', color: '#666', border: '2px dashed #333', borderRadius: '8px' }}>
                    <p style={{ fontSize: '1.1rem', marginBottom: '5px' }}>O Grimório está vazio.</p>
                    <p style={{ fontSize: '0.9rem' }}>Utilize o botão "Adicionar" para escrever novas magias.</p>
                </div>
            )}

            {/* Renderização por Blocos (Estantes) */}
            {circulosAtivos.map(([circulo, lista]) => (
                <div key={circulo} className="circle-block" style={{
                    background: '#151515',
                    border: '1px solid #333',
                    borderRadius: '8px',
                    overflow: 'hidden'
                }}>
                    {/* Cabeçalho do Bloco */}
                    <div style={{
                        background: '#202020',
                        padding: '10px 15px',
                        borderBottom: '1px solid #333',
                        display: 'flex', alignItems: 'center', gap: '12px'
                    }}>
                        <span style={{
                            background: '#9c27b0', color: 'white', width: '26px', height: '26px',
                            borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontSize: '0.85rem', fontWeight: 'bold', boxShadow: '0 2px 5px rgba(0,0,0,0.3)'
                        }}>{circulo}</span>

                        <h4 style={{ margin: 0, color: '#e0e0e0', fontSize: '0.95rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
                            {circulo}º Círculo
                        </h4>

                        <span style={{ marginLeft: 'auto', fontSize: '0.8rem', color: '#666' }}>
                            {lista.length} magia(s)
                        </span>
                    </div>

                    {/* Lista de Magias */}
                    <div>
                        {lista.map(m => renderMagiaCard(m))}
                    </div>
                </div>
            ))}

            <style>{`
                @keyframes slideDown { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
                .spell-card:hover { background-color: #2a2a2a !important; }
            `}</style>
        </div>
    );
};

// Subcomponente de Detalhes
const MiniDetail = ({ label, value }: { label: string, value: string }) => (
    <div style={{ background: '#222', padding: '6px 10px', borderRadius: '4px', border: '1px solid #333' }}>
        <div style={{ fontSize: '0.7rem', color: '#888', textTransform: 'uppercase', fontWeight: 'bold', marginBottom: '2px' }}>
            {label}
        </div>
        <div style={{ fontSize: '0.85rem', color: '#eee', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={value}>
            {value}
        </div>
    </div>
);