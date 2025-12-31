import React, { useState, useEffect } from 'react';
import type { Magia } from '../types';
import { getSchoolColor, getCircleColor, getTypeColor } from '../utils/magicUtils'; // <--- IMPORT NOVO

interface GrimorioModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAddMagia: (magia: Magia) => void;
    dadosMagias: Record<string, Magia>;
    magiasConhecidas: Magia[];
    pmAtual: number;
    pmMaximo: number;
}

export const GrimorioModal: React.FC<GrimorioModalProps> = ({
    isOpen, onClose, onAddMagia,
    dadosMagias, magiasConhecidas, pmAtual, pmMaximo
}) => {
    const [busca, setBusca] = useState('');
    const [filtroCirculo, setFiltroCirculo] = useState<number | 'todos'>('todos');
    const [filtroTipo, setFiltroTipo] = useState<string>('todos'); // <--- NOVO ESTADO

    const [magiaSelecionada, setMagiaSelecionada] = useState<Magia | null>(null);

    useEffect(() => {
        if (!isOpen) {
            setBusca('');
            setFiltroCirculo('todos');
            setFiltroTipo('todos'); // Resetar
            setMagiaSelecionada(null);
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const todasMagias = Object.values(dadosMagias);
    const magiasFiltradas = todasMagias.filter(m => {
        const matchNome = m.nome.toLowerCase().includes(busca.toLowerCase());
        const matchCirculo = filtroCirculo === 'todos' || m.circulo === filtroCirculo;

        // --- NOVO FILTRO DE TIPO ---
        const tipoAtual = m.tipo || 'Universal';
        const matchTipo = filtroTipo === 'todos' || tipoAtual === filtroTipo;

        const naoConhecida = !magiasConhecidas.some(k => k.nome === m.nome);
        return matchNome && matchCirculo && matchTipo && naoConhecida;
    }).sort((a, b) => a.circulo - b.circulo || a.nome.localeCompare(b.nome));

    const handleAprender = () => {
        if (magiaSelecionada) {
            onAddMagia(magiaSelecionada);
            setMagiaSelecionada(null);
        }
    };

    const selectedTypeColor = getTypeColor(magiaSelecionada?.tipo);
    const selectedSchoolColor = getSchoolColor(magiaSelecionada?.escola); // Cor da escola selecionada

    return (
        <div className="modal-overlay" style={{ zIndex: 3000 }}>
            <div className="modal-content large" style={{ display: 'flex', flexDirection: 'column', height: '85vh' }}>

                <div className="modal-header">
                    <h3>📖 Estudo Arcano</h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                {/* BARRA DE FILTROS */}
                <div style={{ display: 'flex', gap: '10px', padding: '12px 20px', background: '#181818', borderBottom: '1px solid #333' }}>
                    <input
                        className="input-dark"
                        placeholder="Buscar magia..."
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        style={{ flex: 1.5 }}
                        autoFocus
                    />

                    {/* FILTRO DE TIPO */}
                    <select
                        className="input-dark"
                        value={filtroTipo}
                        onChange={e => setFiltroTipo(e.target.value)}
                        style={{ width: '130px' }}
                    >
                        <option value="todos">Todos Tipos</option>
                        <option value="Arcana">Arcana</option>
                        <option value="Divina">Divina</option>
                        <option value="Universal">Universal</option>
                    </select>

                    {/* FILTRO DE CÍRCULO */}
                    <select
                        className="input-dark"
                        value={filtroCirculo}
                        onChange={e => setFiltroCirculo(e.target.value === 'todos' ? 'todos' : Number(e.target.value))}
                        style={{ width: '130px' }}
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

                    {/* LISTA LATERAL */}
                    <div style={{ flex: 1, overflowY: 'auto', borderRight: '1px solid #333', background: '#121212' }}>
                        {magiasFiltradas.length === 0 ? (
                            <div style={{ padding: 30, textAlign: 'center', color: '#666' }}>Nenhuma magia encontrada.</div>
                        ) : (
                            magiasFiltradas.map(m => {
                                const isSelected = magiaSelecionada?.nome === m.nome;
                                const schoolColor = getSchoolColor(m.escola);

                                return (
                                    <div
                                        key={m.nome}
                                        onClick={() => setMagiaSelecionada(m)}
                                        style={{
                                            padding: '10px 15px',
                                            borderBottom: '1px solid #252525',
                                            cursor: 'pointer',
                                            background: isSelected ? '#2e2e2e' : 'transparent',
                                            // Borda esquerda colorida pela ESCOLA
                                            borderLeft: isSelected ? `4px solid ${schoolColor}` : '4px solid transparent',
                                            transition: 'background 0.1s'
                                        }}
                                    >
                                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                            <span style={{ fontWeight: 'bold', color: isSelected ? '#fff' : '#ccc' }}>{m.nome}</span>
                                            <span style={{ fontSize: '0.75rem', color: getCircleColor(m.circulo), fontWeight: 'bold' }}>{m.circulo}º</span>
                                        </div>
                                        <div style={{ fontSize: '0.75rem', color: schoolColor, marginTop: '2px', textTransform: 'uppercase' }}>
                                            {m.escola}
                                        </div>
                                    </div>
                                );
                            })
                        )}
                    </div>

                    {/* DETALHES (DIREITA) */}
                    <div style={{ flex: 1.6, padding: '25px', overflowY: 'auto', background: '#1a1a1a' }}>
                        {magiaSelecionada ? (
                            <div>
                                <div style={{ marginBottom: '20px' }}>
                                    <h2 style={{ margin: '0 0 10px 0', color: '#fff', fontSize: '1.5rem' }}>{magiaSelecionada.nome}</h2>
                                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                                        {/* Badge TIPO */}
                                        <span style={{ background: `${selectedTypeColor}15`, color: selectedTypeColor, border: `1px solid ${selectedTypeColor}60`, padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }}>{magiaSelecionada.tipo || 'Universal'}</span>

                                        {/* Badge PM */}
                                        <span style={{ background: 'rgba(156, 39, 176, 0.15)', color: '#ce93d8', border: '1px solid rgba(156, 39, 176, 0.4)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold' }}>{magiaSelecionada.custo_pm} PM</span>

                                        {/* Badge ESCOLA (Agora Colorido) */}
                                        <span style={{ background: `${selectedSchoolColor}20`, color: selectedSchoolColor, border: `1px solid ${selectedSchoolColor}40`, padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold' }}>{magiaSelecionada.escola}</span>

                                        {/* Badge CIRCULO (Agora Colorido) */}
                                        <span style={{ color: getCircleColor(magiaSelecionada.circulo), border: `1px solid ${getCircleColor(magiaSelecionada.circulo)}`, padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold' }}>{magiaSelecionada.circulo}º Círculo</span>
                                    </div>
                                </div>

                                {/* ... (GRID E DESCRIÇÃO MANTÉM IGUAL) ... */}
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', background: '#222', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #333' }}>
                                    <DetailRow label="Execução" value={magiaSelecionada.execucao} />
                                    <DetailRow label="Alcance" value={magiaSelecionada.alcance} />
                                    <DetailRow label="Duração" value={magiaSelecionada.duracao} />
                                    <DetailRow label="Alvo/Área" value={magiaSelecionada.alvo || magiaSelecionada.alvo_area || '-'} />
                                    <DetailRow label="Resistência" value={magiaSelecionada.resistencia || '-'} />
                                </div>
                                <div style={{ color: '#ddd', lineHeight: '1.6', whiteSpace: 'pre-wrap', fontSize: '0.95rem', borderLeft: `2px solid ${selectedTypeColor}80`, paddingLeft: '15px' }}>
                                    {magiaSelecionada.descricao}
                                </div>

                                {magiaSelecionada.aprimoramentos && magiaSelecionada.aprimoramentos.length > 0 && (
                                    <div style={{ marginTop: '25px' }}>
                                        <h4 style={{ color: '#aaa', fontSize: '0.85rem', textTransform: 'uppercase', borderBottom: '1px solid #333', paddingBottom: '5px', marginBottom: '10px' }}>Aprimoramentos</h4>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                            {magiaSelecionada.aprimoramentos.map((ap, idx) => (
                                                <div key={idx} style={{ display: 'flex', gap: '10px', background: '#222', padding: '10px', borderRadius: '4px', border: '1px solid #333' }}>
                                                    <div style={{ color: '#ce93d8', fontWeight: 'bold', fontSize: '0.85rem', whiteSpace: 'nowrap', minWidth: '60px' }}>{ap.custo}</div>
                                                    <div style={{ color: '#ccc', fontSize: '0.9rem', lineHeight: '1.4' }}>{ap.descricao}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#555', flexDirection: 'column' }}>
                                <span style={{ fontSize: '4rem', marginBottom: '15px', opacity: 0.5 }}>🔮</span>
                                <p style={{ fontSize: '1.1rem' }}>Selecione uma magia para ver os detalhes.</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="modal-footer" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.9rem', color: '#888' }}>Seus PM: <strong style={{ color: '#ce93d8' }}>{pmAtual}</strong> / {pmMaximo}</span>
                    <div>
                        <button className="btn-cancel" onClick={onClose} style={{ marginRight: '10px' }}>Cancelar</button>
                        <button className="btn-save" disabled={!magiaSelecionada} onClick={handleAprender} style={{ opacity: !magiaSelecionada ? 0.5 : 1, background: !magiaSelecionada ? '#333' : '#4caf50', color: !magiaSelecionada ? '#888' : 'white' }}>+ Adicionar ao Grimório</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

const DetailRow = ({ label, value }: { label: string, value: string }) => (
    <div><span style={{ color: '#888', fontSize: '0.75rem', textTransform: 'uppercase', display: 'block', marginBottom: '3px' }}>{label}</span><div style={{ color: '#eee', fontWeight: '500', fontSize: '0.9rem' }}>{value}</div></div>
);