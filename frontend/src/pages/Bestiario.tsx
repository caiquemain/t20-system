import React, { useEffect, useState, useMemo } from 'react';
import { fetchAmeacas } from '../services/api';
import type { Ameaca } from '../types';
import { MonsterCard } from '../components/MonsterCard';
import { Link } from 'react-router-dom';

const Bestiario: React.FC = () => {
    const [ameacas, setAmeacas] = useState<Ameaca[]>([]);
    const [loading, setLoading] = useState(true);
    const [busca, setBusca] = useState('');
    const [filtroND, setFiltroND] = useState('');
    const [filtroTipo, setFiltroTipo] = useState('');

    useEffect(() => {
        fetchAmeacas()
            .then(res => {
                setAmeacas(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Erro ao carregar bestiário:", err);
                setLoading(false);
            });
    }, []);

    const ndsUnicos = useMemo(
        () => Array.from(new Set(ameacas.map(a => a.nd))).sort((a, b) => {
            const numA = parseFloat(a);
            const numB = parseFloat(b);
            if (isNaN(numA)) return 1;
            if (isNaN(numB)) return -1;
            return numA - numB;
        }),
        [ameacas]
    );

    const tiposUnicos = useMemo(
        () => Array.from(new Set(ameacas.map(a => a.tipo))).sort(),
        [ameacas]
    );

    const ameacasFiltradas = useMemo(() => {
        return ameacas.filter(a => {
            const matchBusca = a.nome.toLowerCase().includes(busca.toLowerCase());
            const matchND = filtroND ? a.nd === filtroND : true;
            const matchTipo = filtroTipo ? a.tipo === filtroTipo : true;
            return matchBusca && matchND && matchTipo;
        });
    }, [ameacas, busca, filtroND, filtroTipo]);

    return (
        <div style={{ width: '100%', maxWidth: '2200px', margin: '0 auto', padding: '0 40px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', marginTop: '40px' }}>
                <h1 style={{ color: '#d32f2f', margin: 0 }}>📖 Bestiário de Arton</h1>
                <Link to="/" style={{ color: '#aaa', textDecoration: 'none', padding: '10px', border: '1px solid #444', borderRadius: '8px' }}>
                    ⬅ Voltar para Home
                </Link>
            </div>

            {/* Filtros (mesmo estilo do Grimório) */}
            <div style={{
                display: 'flex',
                gap: '15px',
                marginBottom: '30px',
                padding: '15px 20px',
                background: '#1a1a1a',
                borderRadius: '8px',
                border: '1px solid #333',
                flexWrap: 'wrap',
                alignItems: 'center'
            }}>
                <input
                    type="text"
                    placeholder="Buscar monstro pelo nome..."
                    value={busca}
                    onChange={e => setBusca(e.target.value)}
                    style={{
                        flex: '2 1 250px',
                        minWidth: '250px',
                        padding: '12px',
                        background: '#252525',
                        border: '1px solid #444',
                        color: '#fff',
                        borderRadius: '6px',
                        outline: 'none',
                        boxSizing: 'border-box'
                    }}
                />
                <select
                    value={filtroND}
                    onChange={e => setFiltroND(e.target.value)}
                    style={{
                        flex: '1 1 160px',
                        minWidth: '160px',
                        padding: '12px',
                        background: '#252525',
                        border: '1px solid #444',
                        color: '#fff',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        outline: 'none',
                        boxSizing: 'border-box'
                    }}
                >
                    <option value="">Todos os NDs</option>
                    {ndsUnicos.map(nd => <option key={nd} value={nd}>ND {nd}</option>)}
                </select>
                <select
                    value={filtroTipo}
                    onChange={e => setFiltroTipo(e.target.value)}
                    style={{
                        flex: '1 1 200px',
                        minWidth: '200px',
                        padding: '12px',
                        background: '#252525',
                        border: '1px solid #444',
                        color: '#fff',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        outline: 'none',
                        boxSizing: 'border-box'
                    }}
                >
                    <option value="">Todos os Tipos</option>
                    {tiposUnicos.map(tipo => <option key={tipo} value={tipo}>{tipo}</option>)}
                </select>
            </div>

            {loading ? (
                <p style={{ textAlign: 'center', color: '#888', marginTop: '50px' }}>Invocando criaturas...</p>
            ) : ameacasFiltradas.length === 0 ? (
                <p style={{ textAlign: 'center', color: '#888', marginTop: '50px' }}>Nenhum monstro encontrado com esses filtros.</p>
            ) : (
                <>
                    <p style={{ color: '#888', marginBottom: '15px', fontSize: '0.9rem' }}>
                        {ameacasFiltradas.length} criatura(s) encontrada(s)
                    </p>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
                        gap: '15px',
                        paddingBottom: '40px'
                    }}>
                        {ameacasFiltradas.map(a => (
                            <MonsterCard key={a._id} ameaca={a} />
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default Bestiario;
