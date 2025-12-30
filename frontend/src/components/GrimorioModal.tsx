import React, { useState, useEffect } from 'react';
import type { Magia } from '../types';

interface GrimorioModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAddMagia: (magia: Magia) => void;
    dadosMagias: Record<string, Magia>;
    magiasConhecidas: Magia[];
    pmAtual: number;
    pmMaximo: number;
}

// Função auxiliar de cor (Mesma usada nos outros componentes)
const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#e0e0e0';
    const t = tipo.toLowerCase();
    if (t.includes('arcana')) return '#d236d2'; // Roxo
    if (t.includes('divina')) return '#ffc107'; // Dourado
    return '#ff5252' // Universal
};

export const GrimorioModal: React.FC<GrimorioModalProps> = ({
    isOpen, onClose, onAddMagia,
    dadosMagias, magiasConhecidas, pmAtual, pmMaximo
}) => {
    const [busca, setBusca] = useState('');
    const [filtroCirculo, setFiltroCirculo] = useState<number | 'todos'>('todos');
    const [magiaSelecionada, setMagiaSelecionada] = useState<Magia | null>(null);

    // Limpa estados ao abrir/fechar
    useEffect(() => {
        if (!isOpen) {
            setBusca('');
            setFiltroCirculo('todos');
            setMagiaSelecionada(null);
        }
    }, [isOpen]);

    if (!isOpen) return null;

    // Processa a lista de magias
    const todasMagias = Object.values(dadosMagias);
    const magiasFiltradas = todasMagias.filter(m => {
        const matchNome = m.nome.toLowerCase().includes(busca.toLowerCase());
        const matchCirculo = filtroCirculo === 'todos' || m.circulo === filtroCirculo;
        // Exclui magias que já estão no grimório
        const naoConhecida = !magiasConhecidas.some(k => k.nome === m.nome);

        return matchNome && matchCirculo && naoConhecida;
    }).sort((a, b) => a.circulo - b.circulo || a.nome.localeCompare(b.nome));

    const handleAprender = () => {
        if (magiaSelecionada) {
            onAddMagia(magiaSelecionada);
            setMagiaSelecionada(null); // Limpa para permitir nova seleção
        }
    };

    // Cor do tema da magia selecionada
    const selectedTypeColor = getTypeColor(magiaSelecionada?.tipo);

    return (
        <div className="modal-overlay" style={{ zIndex: 3000 }}>
            <div className="modal-content large" style={{ display: 'flex', flexDirection: 'column', height: '85vh' }}>

                <div className="modal-header">
                    <h3>📖 Estudo Arcano</h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                {/* BARRA DE BUSCA E FILTRO */}
                <div style={{ display: 'flex', gap: '10px', padding: '12px 20px', background: '#181818', borderBottom: '1px solid #333' }}>
                    <input
                        className="input-dark"
                        placeholder="Buscar magia pelo nome..."
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        style={{ flex: 1 }}
                        autoFocus
                    />
                    <select
                        className="input-dark"
                        value={filtroCirculo}
                        onChange={e => setFiltroCirculo(e.target.value === 'todos' ? 'todos' : Number(e.target.value))}
                        style={{ width: '140px' }}
                    >
                        <option value="todos">Todos Círculos</option>
                        <option value="1">1º Círculo</option>
                        <option value="2">2º Círculo</option>
                        <option value="3">3º Círculo</option>
                        <option value="4">4º Círculo</option>
                        <option value="5">5º Círculo</option>
                    </select>
                </div>

                <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>

                    {/* COLUNA ESQUERDA: LISTA */}
                    <div style={{ flex: 1, overflowY: 'auto', borderRight: '1px solid #333', background: '#121212' }}>
                        {magiasFiltradas.length === 0 ? (
                            <div style={{ padding: 30, textAlign: 'center', color: '#666' }}>
                                Nenhuma magia encontrada com estes filtros.
                            </div>
                        ) : (
                            magiasFiltradas.map(m => (
                                <div
                                    key={m.nome}
                                    onClick={() => setMagiaSelecionada(m)}
                                    style={{
                                        padding: '12px 15px',
                                        borderBottom: '1px solid #252525',
                                        cursor: 'pointer',
                                        background: magiaSelecionada?.nome === m.nome ? '#2e2e2e' : 'transparent',
                                        borderLeft: magiaSelecionada?.nome === m.nome ? `4px solid ${getTypeColor(m.tipo)}` : '4px solid transparent',
                                        transition: 'background 0.1s'
                                    }}
                                >
                                    <div style={{ fontWeight: 'bold', color: magiaSelecionada?.nome === m.nome ? '#fff' : '#ccc' }}>
                                        {m.nome}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '4px', textTransform: 'uppercase' }}>
                                        {m.circulo}º Círculo • {m.escola}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>

                    {/* COLUNA DIREITA: DETALHES */}
                    <div style={{ flex: 1.6, padding: '25px', overflowY: 'auto', background: '#1a1a1a' }}>
                        {magiaSelecionada ? (
                            <div>
                                {/* CABEÇALHO DA MAGIA */}
                                <div style={{ marginBottom: '20px' }}>
                                    <h2 style={{ margin: '0 0 10px 0', color: '#fff', fontSize: '1.5rem' }}>
                                        {magiaSelecionada.nome}
                                    </h2>

                                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                                        {/* Badge TIPO */}
                                        <span style={{
                                            background: `${selectedTypeColor}15`,
                                            color: selectedTypeColor,
                                            border: `1px solid ${selectedTypeColor}60`,
                                            padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase'
                                        }}>
                                            {magiaSelecionada.tipo || 'Universal'}
                                        </span>

                                        {/* Badge PM */}
                                        <span style={{
                                            background: 'rgba(156, 39, 176, 0.15)', color: '#ce93d8',
                                            border: '1px solid rgba(156, 39, 176, 0.4)',
                                            padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold'
                                        }}>
                                            {magiaSelecionada.custo_pm} PM
                                        </span>

                                        {/* Badge Escola */}
                                        <span style={{ background: '#333', color: '#aaa', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>
                                            {magiaSelecionada.escola}
                                        </span>
                                    </div>
                                </div>

                                {/* GRID DE INFO */}
                                <div style={{
                                    display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px',
                                    background: '#222', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #333'
                                }}>
                                    <DetailRow label="Execução" value={magiaSelecionada.execucao} />
                                    <DetailRow label="Alcance" value={magiaSelecionada.alcance} />
                                    <DetailRow label="Duração" value={magiaSelecionada.duracao} />
                                    <DetailRow label="Alvo/Área" value={magiaSelecionada.alvo || '-'} />
                                    <DetailRow label="Resistência" value={magiaSelecionada.resistencia || '-'} />
                                </div>

                                {/* DESCRIÇÃO */}
                                <div style={{
                                    color: '#ddd', lineHeight: '1.6', whiteSpace: 'pre-wrap', fontSize: '0.95rem',
                                    borderLeft: `2px solid ${selectedTypeColor}80`, paddingLeft: '15px'
                                }}>
                                    {magiaSelecionada.descricao}
                                </div>
                            </div>
                        ) : (
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#555', flexDirection: 'column' }}>
                                <span style={{ fontSize: '4rem', marginBottom: '15px', opacity: 0.5 }}>🔮</span>
                                <p style={{ fontSize: '1.1rem' }}>Selecione uma magia ao lado para ver os detalhes.</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="modal-footer" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.9rem', color: '#888' }}>
                        Seus PM: <strong style={{ color: '#ce93d8' }}>{pmAtual}</strong> / {pmMaximo}
                    </span>
                    <div>
                        <button className="btn-cancel" onClick={onClose} style={{ marginRight: '10px' }}>Cancelar</button>
                        <button
                            className="btn-save"
                            disabled={!magiaSelecionada}
                            onClick={handleAprender}
                            style={{
                                opacity: !magiaSelecionada ? 0.5 : 1,
                                background: !magiaSelecionada ? '#333' : '#4caf50',
                                color: !magiaSelecionada ? '#888' : 'white'
                            }}
                        >
                            + Adicionar ao Grimório
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

const DetailRow = ({ label, value }: { label: string, value: string }) => (
    <div>
        <span style={{ color: '#888', fontSize: '0.75rem', textTransform: 'uppercase', display: 'block', marginBottom: '3px' }}>{label}</span>
        <div style={{ color: '#eee', fontWeight: '500', fontSize: '0.9rem' }}>{value}</div>
    </div>
);