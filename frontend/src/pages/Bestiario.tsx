import React, { useEffect, useState, useMemo } from 'react';
import { fetchAmeacas } from '../services/api';
import type { Ameaca } from '../types';
import { MonsterCard } from '../components/MonsterCard';
import { ConstrutorAmeacaModal } from '../components/ConstrutorAmeacaModal';
import { Link } from 'react-router-dom';
import { T20Icon } from '../components/T20Icon';

const Bestiario: React.FC = () => {
    const [ameacas, setAmeacas] = useState<Ameaca[]>([]);
    const [loading, setLoading] = useState(true);
    const [busca, setBusca] = useState('');
    const [filtroND, setFiltroND] = useState('');
    const [filtroTipo, setFiltroTipo] = useState('');
    const [agruparPorTema, setAgruparPorTema] = useState(true);
    const [abrirConstrutor, setAbrirConstrutor] = useState(false);

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

    const obterTema = (a: Ameaca): string => {
        if ((a._id || '').startsWith('custom-')) return 'Criaturas Customizadas';
        return (a.tipo || 'Outros').trim();
    };

    const temasComContagem = useMemo(() => {
        const map = new Map<string, number>();
        ameacas.forEach(a => {
            const t = obterTema(a);
            map.set(t, (map.get(t) || 0) + 1);
        });
        return Array.from(map.entries()).sort((a, b) => {
            if (a[0] === 'Criaturas Customizadas') return -1;
            if (b[0] === 'Criaturas Customizadas') return 1;
            return a[0].localeCompare(b[0], 'pt-BR');
        });
    }, [ameacas]);

    const ameacasFiltradas = useMemo(() => {
        const q = busca.trim().toLowerCase();
        return ameacas.filter(a => {
            const tema = obterTema(a);
            const matchBusca = !q
                || a.nome.toLowerCase().includes(q)
                || (a.tipo || '').toLowerCase().includes(q)
                || (a.subtipo || '').toLowerCase().includes(q)
                || tema.toLowerCase().includes(q);
            const matchND = filtroND ? a.nd === filtroND : true;
            const matchTipo = filtroTipo ? tema === filtroTipo : true;
            return matchBusca && matchND && matchTipo;
        });
    }, [ameacas, busca, filtroND, filtroTipo]);

    const gruposPorTema = useMemo(() => {
        const map = new Map<string, Ameaca[]>();
        ameacasFiltradas.forEach(a => {
            const t = obterTema(a);
            if (!map.has(t)) map.set(t, []);
            map.get(t)!.push(a);
        });
        return Array.from(map.entries()).sort((a, b) => {
            if (a[0] === 'Criaturas Customizadas') return -1;
            if (b[0] === 'Criaturas Customizadas') return 1;
            return a[0].localeCompare(b[0], 'pt-BR');
        });
    }, [ameacasFiltradas]);

    return (
        <div style={{ width: '100%', maxWidth: '2200px', margin: '0 auto', padding: '0 40px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', marginTop: '40px', flexWrap: 'wrap', gap: '12px' }}>
                <h1 style={{ color: '#d32f2f', margin: 0, display: 'inline-flex', alignItems: 'center', gap: '10px' }}>
                    <T20Icon name="bestiario" size={28} /> Bestiário de Arton
                </h1>
                <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <button
                        onClick={() => setAbrirConstrutor(true)}
                        style={{
                            background: '#d32f2f',
                            color: '#fff',
                            border: 'none',
                            padding: '10px 16px',
                            borderRadius: '8px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                        }}
                    >
                        + Criar Ameaça (Manual Oficial)
                    </button>
                    <Link to="/" style={{ color: '#aaa', textDecoration: 'none', padding: '10px', border: '1px solid #444', borderRadius: '8px', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <T20Icon name="voltar" size={16} /> Voltar para Home
                    </Link>
                </div>
            </div>

            {abrirConstrutor && (
                <ConstrutorAmeacaModal
                    onClose={() => setAbrirConstrutor(false)}
                    onCreated={(nova) => {
                        setAmeacas(prev => [nova, ...prev]);
                        setAbrirConstrutor(false);
                    }}
                />
            )}

            {/* Barra de Pesquisa + Filtros + Agrupamento por Tema */}
            <div style={{
                marginBottom: '26px',
                padding: '15px 20px',
                background: '#1a1a1a',
                borderRadius: '8px',
                border: '1px solid #333',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
            }}>
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
                    <input
                        type="text"
                        placeholder="Buscar monstro por nome, tipo ou tema..."
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
                            flex: '1 1 150px',
                            minWidth: '150px',
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
                            flex: '1 1 190px',
                            minWidth: '190px',
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
                        <option value="">Todos os Temas / Tipos</option>
                        {temasComContagem.map(([tema, qtd]) => (
                            <option key={tema} value={tema}>{tema} ({qtd})</option>
                        ))}
                    </select>
                    <button
                        type="button"
                        onClick={() => setAgruparPorTema(v => !v)}
                        style={{
                            padding: '11px 14px',
                            borderRadius: '6px',
                            border: `1px solid ${agruparPorTema ? '#d32f2f' : '#444'}`,
                            background: agruparPorTema ? 'rgba(211, 47, 47, 0.2)' : '#252525',
                            color: agruparPorTema ? '#ffcdd2' : '#ccc',
                            fontWeight: 600,
                            cursor: 'pointer',
                            whiteSpace: 'nowrap',
                        }}
                    >
                        {agruparPorTema ? '📂 Agrupado por Tema' : '📋 Lista Corrida'}
                    </button>
                </div>

                {/* Chips rápidos de Tema */}
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
                    <button
                        type="button"
                        onClick={() => setFiltroTipo('')}
                        style={{
                            fontSize: '0.76rem',
                            padding: '4px 10px',
                            borderRadius: 999,
                            border: `1px solid ${filtroTipo === '' ? '#ffd700' : '#444'}`,
                            background: filtroTipo === '' ? 'rgba(255, 215, 0, 0.16)' : '#222',
                            color: filtroTipo === '' ? '#ffd700' : '#aaa',
                            cursor: 'pointer',
                            fontWeight: filtroTipo === '' ? 700 : 400,
                        }}
                    >
                        Todos ({ameacas.length})
                    </button>
                    {temasComContagem.map(([tema, qtd]) => {
                        const ativo = filtroTipo === tema;
                        return (
                            <button
                                key={tema}
                                type="button"
                                onClick={() => setFiltroTipo(ativo ? '' : tema)}
                                style={{
                                    fontSize: '0.76rem',
                                    padding: '4px 10px',
                                    borderRadius: 999,
                                    border: `1px solid ${ativo ? '#d32f2f' : '#3a3a3a'}`,
                                    background: ativo ? 'rgba(211, 47, 47, 0.25)' : '#222',
                                    color: ativo ? '#ffcdd2' : '#bbb',
                                    cursor: 'pointer',
                                    fontWeight: ativo ? 700 : 400,
                                }}
                            >
                                {tema} ({qtd})
                            </button>
                        );
                    })}
                </div>
            </div>

            {loading ? (
                <p style={{ color: '#888' }}>Carregando monstros...</p>
            ) : ameacasFiltradas.length === 0 ? (
                <p style={{ color: '#888', textAlign: 'center', marginTop: 40 }}>Nenhuma criatura encontrada com esses filtros.</p>
            ) : agruparPorTema && !filtroTipo ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '28px', paddingBottom: '50px' }}>
                    {gruposPorTema.map(([tema, lista]) => (
                        <section key={tema}>
                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                borderBottom: '1px solid #333',
                                paddingBottom: '6px',
                                marginBottom: '14px',
                            }}>
                                <h2 style={{ margin: 0, color: tema === 'Criaturas Customizadas' ? '#ffd700' : '#ef9a9a', fontSize: '1.15rem' }}>
                                    {tema} <span style={{ color: '#888', fontSize: '0.85rem', fontWeight: 'normal' }}>({lista.length})</span>
                                </h2>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))', gap: '20px' }}>
                                {lista.map(a => <MonsterCard key={a._id || a.nome} ameaca={a} />)}
                            </div>
                        </section>
                    ))}
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))', gap: '20px', paddingBottom: '50px' }}>
                    {ameacasFiltradas.map(a => <MonsterCard key={a._id || a.nome} ameaca={a} />)}
                </div>
            )}
        </div>
    );
};

export default Bestiario;
