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
    const [selecionada, setSelecionada] = useState('');
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

    const opcoesDisponiveis = useMemo(() => {
        const jaTem = new Set(distincoes.map(d => d.nome));
        const q = busca.trim().toLowerCase();
        return Object.keys(catalogo)
            .filter(nome => !jaTem.has(nome) && (!q || nome.toLowerCase().includes(q)))
            .sort((a, b) => a.localeCompare(b, 'pt-BR'));
    }, [catalogo, distincoes, busca]);

    const handleAdicionar = () => {
        const alvo = selecionada || opcoesDisponiveis[0];
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
        setSelecionada('');
        setBusca('');
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
                <h3 className="section-title" style={{ margin: 0 }}>
                    Distinções ({distincoes.length})
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    Heróis de Arton · Poderes disponíveis a partir do 5º nível (Patamar Veterano)
                </span>
            </div>

            {nivelTotal < 5 && (
                <div style={{ background: 'rgba(255, 183, 77, 0.1)', border: '1px solid rgba(255, 183, 77, 0.35)', color: '#ffb74d', padding: '8px 10px', borderRadius: 6, fontSize: '0.8rem', marginBottom: 12 }}>
                    Nível atual ({nivelTotal}): você já pode iniciar a admissão, mas poderes de distinção só podem ser obtidos a partir do 5º nível.
                </div>
            )}

            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
                <input
                    type="text"
                    value={busca}
                    onChange={e => setBusca(e.target.value)}
                    placeholder="Filtrar 36 distinções..."
                    style={{ flex: '1 1 180px', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                />
                <select
                    value={selecionada}
                    onChange={e => setSelecionada(e.target.value)}
                    disabled={carregando || opcoesDisponiveis.length === 0}
                    style={{ flex: '2 1 220px', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                >
                    <option value="">
                        {carregando ? 'Carregando...' : `Selecione uma distinção (${opcoesDisponiveis.length})`}
                    </option>
                    {opcoesDisponiveis.map(nome => (
                        <option key={nome} value={nome}>{nome}</option>
                    ))}
                </select>
                <button
                    type="button"
                    onClick={handleAdicionar}
                    disabled={carregando || opcoesDisponiveis.length === 0}
                    style={{ background: '#ffd700', color: '#111', border: 'none', borderRadius: 4, padding: '6px 14px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.85rem' }}
                >
                    + Adicionar
                </button>
            </div>

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
