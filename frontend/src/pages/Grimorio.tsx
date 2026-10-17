import React, { useEffect, useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { fetchDadosMagias } from '../services/api';
import type { Magia } from '../types';
import { getSchoolColor, getTypeColor } from '../utils/magicUtils';
import { SpellDetailsModal } from '../components/SpellDetailsModal';

const Grimorio: React.FC = () => {
    const [magias, setMagias] = useState<Magia[]>([]);
    const [loading, setLoading] = useState(true);
    const [busca, setBusca] = useState('');
    const [filtroCirculo, setFiltroCirculo] = useState('');
    const [filtroTipo, setFiltroTipo] = useState('');
    const [filtroEscola, setFiltroEscola] = useState('');
    const [magiaSelecionada, setMagiaSelecionada] = useState<Magia | null>(null);

    useEffect(() => {
        fetchDadosMagias()
            .then(res => {
                const lista = Object.values(res.data) as Magia[];
                lista.sort((a, b) => {
                    if (a.circulo !== b.circulo) return a.circulo - b.circulo;
                    return a.nome.localeCompare(b.nome);
                });
                setMagias(lista);
            })
            .catch(err => console.error('Erro ao carregar grimório:', err))
            .finally(() => setLoading(false));
    }, []);

    const escolasUnicas = useMemo(
        () => Array.from(new Set(magias.map(m => m.escola))).sort(),
        [magias]
    );

    const magiasFiltradas = useMemo(() => {
        return magias.filter(m => {
            const matchBusca = m.nome.toLowerCase().includes(busca.toLowerCase());
            const matchCirculo = filtroCirculo ? m.circulo.toString() === filtroCirculo : true;
            const matchTipo = filtroTipo ? (m.tipo || 'Universal') === filtroTipo : true;
            const matchEscola = filtroEscola ? m.escola === filtroEscola : true;
            return matchBusca && matchCirculo && matchTipo && matchEscola;
        });
    }, [magias, busca, filtroCirculo, filtroTipo, filtroEscola]);

    const renderCard = (magia: Magia) => {
        const schoolColor = getSchoolColor(magia.escola);
        const typeColor = getTypeColor(magia.tipo);

        return (
            <div
                key={magia.nome}
                onClick={() => setMagiaSelecionada(magia)}
                style={{
                    background: '#1e1e1e',
                    borderLeft: `4px solid ${schoolColor}`,
                    borderTop: '1px solid #333',
                    borderRight: '1px solid #333',
                    borderBottom: '1px solid #333',
                    borderRadius: '6px',
                    padding: '12px 14px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    minHeight: '110px'
                }}
                onMouseEnter={e => e.currentTarget.style.background = '#2a2a2a'}
                onMouseLeave={e => e.currentTarget.style.background = '#1e1e1e'}
            >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '10px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', minWidth: 0 }}>
                        <span style={{ fontWeight: 'bold', color: '#e0e0e0', fontSize: '1rem', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                            {magia.nome}
                        </span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                            <span style={{ fontSize: '0.7rem', color: schoolColor, textTransform: 'uppercase', fontWeight: 'bold' }}>
                                {magia.escola}
                            </span>
                            <span style={{
                                fontSize: '0.65rem',
                                textTransform: 'uppercase',
                                fontWeight: 'bold',
                                color: typeColor,
                                border: `1px solid ${typeColor}60`,
                                padding: '1px 5px',
                                borderRadius: '3px',
                                lineHeight: 1
                            }}>
                                {magia.tipo || 'UNIV'}
                            </span>
                        </div>
                    </div>
                    <span style={{
                        fontSize: '0.85rem',
                        color: '#ce93d8',
                        fontWeight: 'bold',
                        background: 'rgba(156, 39, 176, 0.15)',
                        padding: '3px 8px',
                        borderRadius: '4px',
                        border: '1px solid rgba(156, 39, 176, 0.3)',
                        whiteSpace: 'nowrap'
                    }}>
                        {magia.circulo}º Círculo
                    </span>
                </div>
                <div style={{ marginTop: '10px', fontSize: '0.75rem', color: '#888', display: 'flex', justifyContent: 'space-between' }}>
                    <span>{magia.execucao}</span>
                    <span>{magia.custo_pm} PM</span>
                </div>
            </div>
        );
    };

    return (
        <div style={{ maxWidth: '1600px', margin: '0 auto', padding: '0 20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', marginTop: '40px' }}>
                <h1 style={{ color: '#ce93d8', margin: 0 }}>📜 Grimório de Arton</h1>
                <Link to="/" style={{ color: '#aaa', textDecoration: 'none', padding: '10px', border: '1px solid #444', borderRadius: '8px' }}>
                    ⬅ Voltar para Home
                </Link>
            </div>

            <div style={{ display: 'flex', gap: '15px', marginBottom: '30px', padding: '15px 20px', background: '#1a1a1a', borderRadius: '8px', border: '1px solid #333', flexWrap: 'wrap' }}>
                <input
                    type="text"
                    placeholder="Buscar magia pelo nome..."
                    value={busca}
                    onChange={e => setBusca(e.target.value)}
                    style={{ flex: 2, minWidth: '200px', padding: '10px', background: '#252525', border: '1px solid #444', color: '#fff', borderRadius: '6px' }}
                />
                <select value={filtroCirculo} onChange={e => setFiltroCirculo(e.target.value)} style={{ flex: 1, minWidth: '120px', padding: '10px', background: '#252525', border: '1px solid #444', color: '#fff', borderRadius: '6px' }}>
                    <option value="">Todos os Círculos</option>
                    {[1, 2, 3, 4, 5].map(c => <option key={c} value={c}>{c}º Círculo</option>)}
                </select>
                <select value={filtroEscola} onChange={e => setFiltroEscola(e.target.value)} style={{ flex: 1, minWidth: '140px', padding: '10px', background: '#252525', border: '1px solid #444', color: '#fff', borderRadius: '6px' }}>
                    <option value="">Todas as Escolas</option>
                    {escolasUnicas.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
                <select value={filtroTipo} onChange={e => setFiltroTipo(e.target.value)} style={{ flex: 1, minWidth: '120px', padding: '10px', background: '#252525', border: '1px solid #444', color: '#fff', borderRadius: '6px' }}>
                    <option value="">Todos os Tipos</option>
                    <option value="Arcana">Arcana</option>
                    <option value="Divina">Divina</option>
                    <option value="Universal">Universal</option>
                </select>
            </div>

            {loading ? (
                <p style={{ textAlign: 'center', color: '#888', marginTop: '50px' }}>Consultando os tomos antigos...</p>
            ) : magiasFiltradas.length === 0 ? (
                <p style={{ textAlign: 'center', color: '#888', marginTop: '50px' }}>Nenhuma magia encontrada com esses filtros.</p>
            ) : (
                <>
                    <p style={{ color: '#888', marginBottom: '15px', fontSize: '0.9rem' }}>
                        {magiasFiltradas.length} magia(s) encontrada(s)
                    </p>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                        gap: '15px',
                        paddingBottom: '40px'
                    }}>
                        {magiasFiltradas.map(renderCard)}
                    </div>
                </>
            )}

            <SpellDetailsModal
                magia={magiaSelecionada}
                onClose={() => setMagiaSelecionada(null)}
                onRemove={() => {}}
                hideRemove={true}
            />
        </div>
    );
};

export default Grimorio;
