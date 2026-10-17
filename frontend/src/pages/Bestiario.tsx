import React, { useEffect, useState } from 'react';
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

    const ameacasFiltradas = ameacas.filter(a => {
        const matchBusca = a.nome.toLowerCase().includes(busca.toLowerCase());
        const matchND = filtroND ? a.nd === filtroND : true;
        const matchTipo = filtroTipo ? a.tipo === filtroTipo : true;
        return matchBusca && matchND && matchTipo;
    });

    const ndsUnicos = Array.from(new Set(ameacas.map(a => a.nd))).sort((a, b) => {
        const numA = parseFloat(a);
        const numB = parseFloat(b);
        if (isNaN(numA)) return 1;
        if (isNaN(numB)) return -1;
        return numA - numB;
    });
    const tiposUnicos = Array.from(new Set(ameacas.map(a => a.tipo))).sort();

    return (
        // Aumentamos o maxWidth para 1600px para caber mais colunas
        <div className="container" style={{ maxWidth: '1600px', width: '100%', padding: '0 20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', marginTop: '40px' }}>
                <h1 style={{ color: 'var(--accent-color)', margin: 0 }}>📖 Bestiário de Arton</h1>
                <Link to="/" style={{ color: 'var(--text-secondary)', textDecoration: 'none', padding: '10px', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
                    ⬅ Voltar para Home
                </Link>
            </div>

            <div className="card-form" style={{ display: 'flex', gap: '15px', marginBottom: '30px', padding: '15px 20px', flexDirection: 'row', flexWrap: 'wrap' }}>
                <div style={{ flex: 2, minWidth: '200px' }}>
                    <input 
                        type="text" 
                        placeholder="Buscar monstro pelo nome..." 
                        value={busca}
                        onChange={e => setBusca(e.target.value)}
                        style={{ marginTop: 0 }}
                    />
                </div>
                <div style={{ flex: 1, minWidth: '120px' }}>
                    <select value={filtroND} onChange={e => setFiltroND(e.target.value)} style={{ marginTop: 0 }}>
                        <option value="">Todos os NDs</option>
                        {ndsUnicos.map(nd => <option key={nd} value={nd}>ND {nd}</option>)}
                    </select>
                </div>
                <div style={{ flex: 1, minWidth: '150px' }}>
                    <select value={filtroTipo} onChange={e => setFiltroTipo(e.target.value)} style={{ marginTop: 0 }}>
                        <option value="">Todos os Tipos</option>
                        {tiposUnicos.map(tipo => <option key={tipo} value={tipo}>{tipo}</option>)}
                    </select>
                </div>
            </div>

            {loading ? (
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '50px' }}>Invocando criaturas...</p>
            ) : ameacasFiltradas.length === 0 ? (
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '50px' }}>Nenhum monstro encontrado com esses filtros.</p>
            ) : (
                // Aqui está a mágica: minmax(280px) permite até 5 colunas em telas grandes, 
                // e quebra para 3, 2 ou 1 automaticamente em telas menores.
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
                    gap: '20px', 
                    paddingBottom: '40px' 
                }}>
                    {ameacasFiltradas.map(a => (
                        <MonsterCard key={a._id} ameaca={a} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default Bestiario;
