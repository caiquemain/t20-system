import React, { useEffect, useMemo, useState } from 'react';
import type { DistincaoPersonagem, Personagem } from '../../types';
import { fetchDadosDistincoes } from '../../services/api';

interface PoderDistincaoInfo {
    nome: string;
    descricao: string;
    requisitos?: string[];
    custo_pm?: number;
}

interface DistincaoInfo {
    nome: string;
    fonte: string;
    admissao: string;
    marca: { nome: string; descricao: string };
    poderes: PoderDistincaoInfo[];
}

interface Props {
    ficha: Personagem;
    onUpdate: (dados: Partial<Personagem>) => void;
}

export const DistincoesPanel: React.FC<Props> = ({ ficha, onUpdate }) => {
    const [catalogo, setCatalogo] = useState<Record<string, DistincaoInfo>>({});
    const [busca, setBusca] = useState('');
    const [filtroFonte, setFiltroFonte] = useState<'Todas' | 'Heróis de Arton' | 'Deuses de Arton'>('Todas');
    const [modalAberto, setModalAberto] = useState(false);
    const [focoModal, setFocoModal] = useState<string>('');
    const [expandida, setExpandida] = useState<Record<string, boolean>>({});
    const [carregando, setCarregando] = useState(true);

    useEffect(() => {
        fetchDadosDistincoes()
            .then(res => setCatalogo(res.data?.distincoes || {}))
            .catch(() => {})
            .finally(() => setCarregando(false));
    }, []);

    const distincoes = ficha.distincoes || [];
    const nivelTotal = ficha.cabecalho?.nivel_total || 1;
    const totalCatalogo = Object.keys(catalogo).length;

    const opcoesDisponiveis = useMemo(() => {
        const jaTem = new Set(distincoes.map(d => d.nome));
        const q = busca.trim().toLowerCase();
        return Object.keys(catalogo)
            .filter(nome => {
                if (jaTem.has(nome)) return false;
                const info = catalogo[nome];
                if (filtroFonte !== 'Todas' && info?.fonte !== filtroFonte) return false;
                if (!q) return true;
                return (
                    nome.toLowerCase().includes(q) ||
                    (info?.marca?.nome || '').toLowerCase().includes(q) ||
                    (info?.poderes || []).some(p => p.nome.toLowerCase().includes(q))
                );
            })
            .sort((a, b) => a.localeCompare(b, 'pt-BR'));
    }, [catalogo, distincoes, busca, filtroFonte]);

    const itemEmFoco: DistincaoInfo | null = useMemo(() => {
        if (focoModal && catalogo[focoModal] && opcoesDisponiveis.includes(focoModal)) {
            return catalogo[focoModal];
        }
        return opcoesDisponiveis[0] ? catalogo[opcoesDisponiveis[0]] : null;
    }, [focoModal, catalogo, opcoesDisponiveis]);

    const handleAdicionar = (nomeAlvo?: string) => {
        const alvo = nomeAlvo || itemEmFoco?.nome;
        if (!alvo || !catalogo[alvo]) return;
        const info = catalogo[alvo];
        const nova: DistincaoPersonagem = {
            nome: info.nome,
            admitido: true,
            marca: info.marca?.nome || '',
            poderes: [],
            fonte: info.fonte || 'Heróis de Arton',
        };
        onUpdate({ distincoes: [...distincoes, nova] });
        setModalAberto(false);
        setBusca('');
        setFocoModal('');
    };

    const handleRemover = (nome: string) => {
        onUpdate({ distincoes: distincoes.filter(d => d.nome !== nome) });
    };

    const handleToggleAdmitido = (nome: string) => {
        onUpdate({
            distincoes: distincoes.map(d =>
                d.nome === nome ? { ...d, admitido: !d.admitido } : d
            ),
        });
    };

    const handleTogglePoder = (distNome: string, poderNome: string) => {
        onUpdate({
            distincoes: distincoes.map(d => {
                if (d.nome !== distNome) return d;
                const atual = d.poderes || [];
                const existe = atual.includes(poderNome);
                return {
                    ...d,
                    poderes: existe ? atual.filter(p => p !== poderNome) : [...atual, poderNome],
                };
            }),
        });
    };

    return (
        <div className="section-card" style={{ marginBottom: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 12 }}>
                <div>
                    <h3 className="section-title" style={{ margin: 0 }}>
                        Distinções ({distincoes.length})
                    </h3>
                    <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        Heróis de Arton &amp; Deuses de Arton · Poderes disponíveis a partir do 5º nível (Patamar Veterano)
                    </span>
                </div>
                <button
                    type="button"
                    onClick={() => setModalAberto(true)}
                    disabled={carregando || opcoesDisponiveis.length === 0}
                    style={{
                        background: '#ffd700',
                        color: '#111',
                        border: 'none',
                        borderRadius: 6,
                        padding: '8px 16px',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        fontSize: '0.85rem',
                    }}
                >
                    {carregando ? 'Carregando...' : `+ Escolher Distinção (${totalCatalogo})`}
                </button>
            </div>

            {nivelTotal < 5 && (
                <div style={{ background: 'rgba(255, 183, 77, 0.1)', border: '1px solid rgba(255, 183, 77, 0.35)', color: '#ffb74d', padding: '8px 10px', borderRadius: 6, fontSize: '0.8rem', marginBottom: 12 }}>
                    Nível atual ({nivelTotal}): você já pode iniciar a admissão, mas poderes de distinção só podem ser obtidos a partir do 5º nível.
                </div>
            )}

            {/* MODAL DE SELEÇÃO DE DISTINÇÕES (MESMO MOLDE DE DEUSES / CLASSES) */}
            {modalAberto && (
                <div
                    onClick={() => setModalAberto(false)}
                    style={{
                        position: 'fixed',
                        inset: 0,
                        background: 'rgba(0,0,0,0.82)',
                        zIndex: 10000,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: 16,
                    }}
                >
                    <div
                        onClick={e => e.stopPropagation()}
                        style={{
                            width: '100%',
                            maxWidth: 960,
                            height: '82vh',
                            background: '#16161c',
                            border: '1px solid #ffd700',
                            borderRadius: 10,
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden',
                            color: '#eee',
                        }}
                    >
                        <div style={{ padding: '14px 18px', borderBottom: '1px solid #2c2c36', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                            <div>
                                <h3 style={{ margin: 0, color: '#ffd700' }}>Selecionar Distinção</h3>
                                <small style={{ color: '#94a3b8' }}>
                                    Explore a Marca, Admissão e Poderes de cada uma das {totalCatalogo} Distinções oficiais
                                </small>
                            </div>
                            <button
                                type="button"
                                onClick={() => setModalAberto(false)}
                                style={{ background: '#2c2c36', color: '#fff', border: '1px solid #444', borderRadius: 6, padding: '6px 12px', cursor: 'pointer' }}
                            >
                                Fechar
                            </button>
                        </div>

                        <div style={{ padding: '10px 18px', borderBottom: '1px solid #2c2c36', display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center' }}>
                            <input
                                type="text"
                                value={busca}
                                onChange={e => setBusca(e.target.value)}
                                placeholder="Buscar por distinção, marca ou poder..."
                                autoFocus
                                style={{ flex: '1 1 240px', background: '#101015', border: '1px solid #444', color: '#fff', borderRadius: 6, padding: '8px 12px', fontSize: '0.88rem' }}
                            />
                            <div style={{ display: 'flex', gap: 6 }}>
                                {(['Todas', 'Heróis de Arton', 'Deuses de Arton'] as const).map(f => (
                                    <button
                                        key={f}
                                        type="button"
                                        onClick={() => setFiltroFonte(f)}
                                        style={{
                                            background: filtroFonte === f ? '#ffd700' : '#22222c',
                                            color: filtroFonte === f ? '#111' : '#ccc',
                                            border: '1px solid #444',
                                            borderRadius: 6,
                                            padding: '6px 10px',
                                            fontSize: '0.78rem',
                                            fontWeight: filtroFonte === f ? 'bold' : 'normal',
                                            cursor: 'pointer',
                                        }}
                                    >
                                        {f}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '290px 1fr', overflow: 'hidden' }}>
                            {/* Lista esquerda */}
                            <div style={{ borderRight: '1px solid #2c2c36', overflowY: 'auto', padding: 10, display: 'flex', flexDirection: 'column', gap: 6 }}>
                                {opcoesDisponiveis.length === 0 ? (
                                    <p style={{ color: '#777', textAlign: 'center', fontSize: '0.85rem', marginTop: 20 }}>
                                        Nenhuma distinção encontrada.
                                    </p>
                                ) : (
                                    opcoesDisponiveis.map(nome => {
                                        const d = catalogo[nome];
                                        const ativo = itemEmFoco?.nome === nome;
                                        const ehDeuses = d?.fonte === 'Deuses de Arton';
                                        return (
                                            <button
                                                key={nome}
                                                type="button"
                                                onClick={() => setFocoModal(nome)}
                                                style={{
                                                    textAlign: 'left',
                                                    background: ativo ? 'rgba(255,215,0,0.14)' : '#1c1c24',
                                                    border: `1px solid ${ativo ? '#ffd700' : '#2e2e3a'}`,
                                                    borderRadius: 6,
                                                    padding: '9px 11px',
                                                    cursor: 'pointer',
                                                    color: '#fff',
                                                }}
                                            >
                                                <div style={{ fontWeight: 'bold', fontSize: '0.88rem', color: ativo ? '#ffd700' : '#eee' }}>
                                                    {nome}
                                                </div>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4, fontSize: '0.72rem', color: '#94a3b8' }}>
                                                    <span style={{ color: ehDeuses ? '#ce93d8' : '#80deea' }}>
                                                        {ehDeuses ? 'Deuses de Arton' : 'Heróis de Arton'}
                                                    </span>
                                                    <span>{d?.poderes?.length || 0} poderes</span>
                                                </div>
                                            </button>
                                        );
                                    })
                                )}
                            </div>

                            {/* Detalhes direita */}
                            <div style={{ overflowY: 'auto', padding: 18 }}>
                                {itemEmFoco ? (
                                    <>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, flexWrap: 'wrap', marginBottom: 14 }}>
                                            <div>
                                                <h2 style={{ margin: 0, color: '#ffd700', fontSize: '1.25rem' }}>{itemEmFoco.nome}</h2>
                                                <span style={{ fontSize: '0.78rem', color: itemEmFoco.fonte === 'Deuses de Arton' ? '#ce93d8' : '#80deea' }}>
                                                    {itemEmFoco.fonte}
                                                </span>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => handleAdicionar(itemEmFoco.nome)}
                                                style={{
                                                    background: '#ffd700',
                                                    color: '#111',
                                                    border: 'none',
                                                    borderRadius: 6,
                                                    padding: '9px 18px',
                                                    fontWeight: 'bold',
                                                    cursor: 'pointer',
                                                    fontSize: '0.88rem',
                                                }}
                                            >
                                                + Adicionar Distinção
                                            </button>
                                        </div>

                                        <div style={{ background: 'rgba(129,199,132,0.08)', border: '1px solid rgba(129,199,132,0.3)', borderRadius: 6, padding: 12, marginBottom: 14 }}>
                                            <div style={{ fontSize: '0.75rem', color: '#81c784', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: 4 }}>
                                                Marca da Distinção — {itemEmFoco.marca?.nome}
                                            </div>
                                            <p style={{ margin: 0, fontSize: '0.84rem', color: '#ddd', lineHeight: 1.5 }}>
                                                {itemEmFoco.marca?.descricao}
                                            </p>
                                        </div>

                                        <div style={{ marginBottom: 16 }}>
                                            <div style={{ fontSize: '0.76rem', color: '#ffb74d', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: 4 }}>
                                                Admissão
                                            </div>
                                            <p style={{ margin: 0, fontSize: '0.82rem', color: '#bbb', lineHeight: 1.5 }}>
                                                {itemEmFoco.admissao}
                                            </p>
                                        </div>

                                        <div>
                                            <div style={{ fontSize: '0.76rem', color: '#ffd700', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: 8 }}>
                                                Poderes da Distinção ({itemEmFoco.poderes.length})
                                            </div>
                                            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                                                {itemEmFoco.poderes.map(p => (
                                                    <div key={p.nome} style={{ background: '#1e1e26', border: '1px solid #30303e', borderRadius: 6, padding: 10 }}>
                                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                                                            <strong style={{ color: '#fff', fontSize: '0.88rem' }}>{p.nome}</strong>
                                                            {p.custo_pm && (
                                                                <span style={{ fontSize: '0.72rem', color: '#ce93d8', background: 'rgba(156,39,176,0.2)', padding: '1px 6px', borderRadius: 4 }}>
                                                                    {p.custo_pm} PM
                                                                </span>
                                                            )}
                                                        </div>
                                                        <p style={{ margin: 0, fontSize: '0.8rem', color: '#ccc', lineHeight: 1.45 }}>
                                                            {p.descricao}
                                                        </p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <p style={{ color: '#777', textAlign: 'center', marginTop: 40 }}>
                                        Selecione uma distinção na lista à esquerda para ver os detalhes.
                                    </p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {distincoes.length === 0 ? (
                <p style={{ color: '#666', fontSize: '0.85rem', margin: 0 }}>
                    Nenhuma distinção conquistada ainda.
                </p>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {distincoes.map(dist => {
                        const info = catalogo[dist.nome];
                        const aberta = !!expandida[dist.nome];
                        const poderesEscolhidos = new Set(dist.poderes || []);
                        return (
                            <div key={dist.nome} style={{ background: '#16161c', border: '1px solid #333', borderRadius: 6, padding: 12 }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
                                    <div>
                                        <strong style={{ color: '#ffd700', fontSize: '1rem' }}>{dist.nome}</strong>
                                        <span style={{ marginLeft: 8, fontSize: '0.75rem', color: dist.admitido ? '#81c784' : '#ffb74d' }}>
                                            {dist.admitido ? `✓ Admitido · Marca: ${info?.marca?.nome || dist.marca}` : '⏳ Em admissão'}
                                        </span>
                                    </div>
                                    <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                                        <label style={{ fontSize: '0.78rem', color: '#ccc', display: 'inline-flex', alignItems: 'center', gap: 4, cursor: 'pointer' }}>
                                            <input
                                                type="checkbox"
                                                checked={dist.admitido}
                                                onChange={() => handleToggleAdmitido(dist.nome)}
                                            />
                                            Admitido
                                        </label>
                                        <button
                                            type="button"
                                            onClick={() => setExpandida(prev => ({ ...prev, [dist.nome]: !aberta }))}
                                            style={{ background: 'transparent', border: '1px solid #444', color: '#ccc', borderRadius: 4, padding: '2px 8px', cursor: 'pointer', fontSize: '0.75rem' }}
                                        >
                                            {aberta ? 'Ocultar Admissão' : 'Ver Admissão'}
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => handleRemover(dist.nome)}
                                            style={{ background: 'rgba(229,57,53,0.15)', border: '1px solid rgba(229,57,53,0.4)', color: '#ef9a9a', borderRadius: 4, padding: '2px 8px', cursor: 'pointer', fontSize: '0.75rem' }}
                                        >
                                            Remover
                                        </button>
                                    </div>
                                </div>

                                {info?.marca && (
                                    <div style={{ marginTop: 8, padding: '6px 10px', background: 'rgba(255,215,0,0.06)', borderLeft: '3px solid #ffd700', fontSize: '0.8rem', color: '#ddd' }}>
                                        <strong style={{ color: '#ffd700' }}>Marca — {info.marca.nome}:</strong> {info.marca.descricao}
                                    </div>
                                )}

                                {aberta && info?.admissao && (
                                    <div style={{ marginTop: 8, padding: '6px 10px', background: 'rgba(255,255,255,0.03)', borderRadius: 4, fontSize: '0.78rem', color: '#aaa' }}>
                                        <strong>Admissão:</strong> {info.admissao}
                                    </div>
                                )}

                                {info?.poderes && (
                                    <div style={{ marginTop: 10 }}>
                                        <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: 6, textTransform: 'uppercase' }}>
                                            Poderes da Distinção ({poderesEscolhidos.size}/{info.poderes.length})
                                        </div>
                                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 6 }}>
                                            {info.poderes.map(p => {
                                                const marcado = poderesEscolhidos.has(p.nome);
                                                return (
                                                    <label
                                                        key={p.nome}
                                                        title={p.descricao}
                                                        style={{
                                                            display: 'flex',
                                                            alignItems: 'flex-start',
                                                            gap: 6,
                                                            padding: '6px 8px',
                                                            borderRadius: 4,
                                                            cursor: dist.admitido ? 'pointer' : 'not-allowed',
                                                            opacity: dist.admitido ? 1 : 0.5,
                                                            background: marcado ? 'rgba(255,215,0,0.12)' : 'rgba(255,255,255,0.03)',
                                                            border: marcado ? '1px solid rgba(255,215,0,0.45)' : '1px solid #2a2a32',
                                                            fontSize: '0.8rem',
                                                        }}
                                                    >
                                                        <input
                                                            type="checkbox"
                                                            disabled={!dist.admitido}
                                                            checked={marcado}
                                                            onChange={() => handleTogglePoder(dist.nome, p.nome)}
                                                            style={{ marginTop: 2 }}
                                                        />
                                                        <div>
                                                            <div style={{ fontWeight: 'bold', color: marcado ? '#ffd700' : '#e0e0e0' }}>
                                                                {p.nome}
                                                                {p.custo_pm ? (
                                                                    <span style={{ marginLeft: 6, fontSize: '0.7rem', color: '#ce93d8' }}>{p.custo_pm} PM</span>
                                                                ) : null}
                                                            </div>
                                                            <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: 2 }}>
                                                                {p.descricao.length > 120 ? `${p.descricao.slice(0, 120)}…` : p.descricao}
                                                            </div>
                                                        </div>
                                                    </label>
                                                );
                                            })}
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};
