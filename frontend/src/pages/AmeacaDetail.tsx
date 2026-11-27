import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchAmeaca, updateAmeaca } from '../services/api';
import type { Ameaca } from '../types';
import { T20Icon } from '../components/T20Icon';

const AmeacaDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [ameaca, setAmeaca] = useState<Ameaca | null>(null);
    const [loading, setLoading] = useState(true);
    const [editando, setEditando] = useState(false);
    const [salvando, setSalvando] = useState(false);
    const [draft, setDraft] = useState<Ameaca | null>(null);

    useEffect(() => {
        if (id) {
            fetchAmeaca(id)
                .then(res => {
                    setAmeaca(res.data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Erro ao carregar ameaça:", err);
                    setLoading(false);
                });
        }
    }, [id]);

    const iniciarEdicao = () => {
        if (!ameaca) return;
        setDraft(JSON.parse(JSON.stringify(ameaca)));
        setEditando(true);
    };

    const handleSalvar = async () => {
        if (!draft || !id) return;
        setSalvando(true);
        try {
            const payload = { ...draft };
            delete (payload as any)._id;
            const res = await updateAmeaca(id, payload);
            setAmeaca(res.data || draft);
            setEditando(false);
        } catch (err) {
            alert("Erro ao salvar alterações da ameaça: " + (err as Error).message);
        } finally {
            setSalvando(false);
        }
    };

    const enviarParaRoll20 = () => {
        if (!ameaca) return;
        window.postMessage({ type: 'T20_ENVIAR_AMEACA_ROLL20', ameaca }, '*');

        const handleResposta = (event: MessageEvent) => {
            if (event.source !== window) return;
            if (event.data && event.data.type === 'T20_RESPOSTA_ROLL20') {
                window.removeEventListener('message', handleResposta);
                if (event.data.ok) {
                    alert(`${ameaca.nome} enviado para o Roll20 com sucesso!`);
                } else {
                    alert(`Erro ao enviar: ${event.data.err || 'Verifique se uma ficha do Roll20 está aberta.'}`);
                }
            }
        };
        window.addEventListener('message', handleResposta);
        setTimeout(() => window.removeEventListener('message', handleResposta), 5000);
    };

    if (loading) return <p className="container">Carregando ficha...</p>;
    if (!ameaca) return <p className="container">Monstro não encontrado.</p>;

    const inputStyle: React.CSSProperties = {
        background: '#16161c',
        border: '1px solid #444',
        color: '#fff',
        borderRadius: 5,
        padding: '6px 8px',
        fontSize: '0.9rem',
        width: '100%',
        boxSizing: 'border-box',
    };

    return (
        <div className="container" style={{ maxWidth: '940px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: 10 }}>
                <Link to="/bestiario" style={{ color: 'var(--text-secondary)', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                    <T20Icon name="voltar" size={16} /> Voltar ao Bestiário
                </Link>
                <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                    {!editando ? (
                        <button
                            onClick={iniciarEdicao}
                            style={{ background: '#f59e0b', color: '#111', padding: '8px 16px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                            ✏️ Editar Estatísticas
                        </button>
                    ) : (
                        <>
                            <button
                                onClick={handleSalvar}
                                disabled={salvando}
                                style={{ background: '#4caf50', color: '#fff', padding: '8px 16px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
                            >
                                {salvando ? 'Salvando...' : '💾 Salvar Alterações'}
                            </button>
                            <button
                                onClick={() => { setEditando(false); setDraft(null); }}
                                style={{ background: '#333', color: '#ccc', padding: '8px 14px', border: '1px solid #555', borderRadius: '6px', cursor: 'pointer' }}
                            >
                                Cancelar
                            </button>
                        </>
                    )}
                    <button onClick={enviarParaRoll20} style={{ background: '#9c27b0', color: '#fff', padding: '8px 16px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <T20Icon name="roll20" size={16} /> Enviar pro Roll20
                    </button>
                </div>
            </div>

            {editando && draft ? (
                <div className="card-form" style={{ padding: '26px' }}>
                    <h2 style={{ marginTop: 0, color: '#ffd700' }}>Editando Estatísticas — {draft.nome}</h2>

                    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr', gap: 10, marginBottom: 16 }}>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Nome</label>
                            <input style={inputStyle} value={draft.nome} onChange={e => setDraft({ ...draft, nome: e.target.value })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>ND</label>
                            <input style={inputStyle} value={draft.nd} onChange={e => setDraft({ ...draft, nd: e.target.value })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Tipo / Tema</label>
                            <input style={inputStyle} value={draft.tipo} onChange={e => setDraft({ ...draft, tipo: e.target.value })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Subtipo</label>
                            <input style={inputStyle} value={draft.subtipo || ''} onChange={e => setDraft({ ...draft, subtipo: e.target.value })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Tamanho</label>
                            <select
                                style={inputStyle}
                                value={draft.tamanho}
                                onChange={e => setDraft({ ...draft, tamanho: e.target.value as Ameaca['tamanho'] })}
                            >
                                {(['Minúsculo', 'Pequeno', 'Médio', 'Grande', 'Enorme', 'Colossal'] as const).map(t => (
                                    <option key={t} value={t}>{t}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginBottom: 16 }}>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>PV</label>
                            <input type="number" style={inputStyle} value={draft.pontos_de_vida} onChange={e => setDraft({ ...draft, pontos_de_vida: Number(e.target.value) })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Defesa</label>
                            <input type="number" style={inputStyle} value={draft.defesa} onChange={e => setDraft({ ...draft, defesa: Number(e.target.value) })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Deslocamento</label>
                            <input style={inputStyle} value={draft.deslocamento} onChange={e => setDraft({ ...draft, deslocamento: e.target.value })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Iniciativa</label>
                            <input type="number" style={inputStyle} value={draft.iniciativa} onChange={e => setDraft({ ...draft, iniciativa: Number(e.target.value) })} />
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, marginBottom: 16 }}>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Fortitude</label>
                            <input type="number" style={inputStyle} value={draft.fortitude} onChange={e => setDraft({ ...draft, fortitude: Number(e.target.value) })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Reflexos</label>
                            <input type="number" style={inputStyle} value={draft.reflexos} onChange={e => setDraft({ ...draft, reflexos: Number(e.target.value) })} />
                        </div>
                        <div>
                            <label style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Vontade</label>
                            <input type="number" style={inputStyle} value={draft.vontade} onChange={e => setDraft({ ...draft, vontade: Number(e.target.value) })} />
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, marginBottom: 20 }}>
                        {Object.entries(draft.atributos || {}).map(([k, v]) => (
                            <div key={k}>
                                <label style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>{k.slice(0, 3)}</label>
                                <input
                                    type="number"
                                    style={inputStyle}
                                    value={v ?? 0}
                                    onChange={e => setDraft({
                                        ...draft,
                                        atributos: { ...draft.atributos, [k]: e.target.value === '' ? null : Number(e.target.value) },
                                    })}
                                />
                            </div>
                        ))}
                    </div>

                    {/* Ataques */}
                    <div style={{ marginBottom: 20 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                            <h3 style={{ margin: 0, color: '#ffd700' }}>Ataques</h3>
                            <button
                                type="button"
                                onClick={() => setDraft({
                                    ...draft,
                                    ataques: [
                                        ...(draft.ataques || []),
                                        { nome: 'Novo Ataque', modalidade: 'Corpo a corpo', bonus_ataque: 5, dano: '1d8+3', tipo_dano: 'Corte', margem_critico: 20, multiplicador_critico: 2, descricao: '' } as any,
                                    ],
                                })}
                                style={{ background: '#333', color: '#ffd700', border: '1px solid #555', borderRadius: 4, padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem' }}
                            >
                                + Adicionar Ataque
                            </button>
                        </div>
                        {(draft.ataques || []).map((atk, idx) => (
                            <div key={idx} style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr 0.7fr 1fr 0.9fr 0.6fr 0.6fr auto', gap: 6, marginBottom: 8, alignItems: 'center' }}>
                                <input style={inputStyle} value={atk.nome} placeholder="Nome" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, nome: e.target.value }; setDraft({ ...draft, ataques: next });
                                }} />
                                <select style={inputStyle} value={atk.modalidade} onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, modalidade: e.target.value as 'corpo a corpo' | 'à distância' }; setDraft({ ...draft, ataques: next });
                                }}>
                                    <option value="corpo a corpo">corpo a corpo</option>
                                    <option value="à distância">à distância</option>
                                </select>
                                <input type="number" style={inputStyle} value={atk.bonus_ataque} title="Bônus de ataque" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, bonus_ataque: Number(e.target.value) }; setDraft({ ...draft, ataques: next });
                                }} />
                                <input style={inputStyle} value={atk.dano} placeholder="Dano" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, dano: e.target.value }; setDraft({ ...draft, ataques: next });
                                }} />
                                <input style={inputStyle} value={atk.tipo_dano} placeholder="Tipo" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, tipo_dano: e.target.value }; setDraft({ ...draft, ataques: next });
                                }} />
                                <input type="number" style={inputStyle} value={atk.margem_critico} title="Margem" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, margem_critico: Number(e.target.value) }; setDraft({ ...draft, ataques: next });
                                }} />
                                <input type="number" style={inputStyle} value={atk.multiplicador_critico} title="Multiplicador" onChange={e => {
                                    const next = [...draft.ataques]; next[idx] = { ...atk, multiplicador_critico: Number(e.target.value) }; setDraft({ ...draft, ataques: next });
                                }} />
                                <button
                                    type="button"
                                    onClick={() => setDraft({ ...draft, ataques: draft.ataques.filter((_, j) => j !== idx) })}
                                    style={{ background: '#3a2222', color: '#ff8a80', border: '1px solid #663333', borderRadius: 4, padding: '6px 8px', cursor: 'pointer' }}
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>

                    {/* Habilidades */}
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                            <h3 style={{ margin: 0, color: '#ffd700' }}>Habilidades</h3>
                            <button
                                type="button"
                                onClick={() => setDraft({
                                    ...draft,
                                    habilidades: [
                                        ...(draft.habilidades || []),
                                        { nome: 'Nova Habilidade', tipo_acao: 'Padrão', descricao: '', rolls: [] } as any,
                                    ],
                                })}
                                style={{ background: '#333', color: '#ffd700', border: '1px solid #555', borderRadius: 4, padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem' }}
                            >
                                + Adicionar Habilidade
                            </button>
                        </div>
                        {(draft.habilidades || []).map((hab, idx) => (
                            <div key={idx} style={{ background: '#1a1a22', border: '1px solid #333', borderRadius: 6, padding: 10, marginBottom: 8 }}>
                                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr auto', gap: 8, marginBottom: 6 }}>
                                    <input style={inputStyle} value={hab.nome} placeholder="Nome" onChange={e => {
                                        const next = [...draft.habilidades]; next[idx] = { ...hab, nome: e.target.value }; setDraft({ ...draft, habilidades: next });
                                    }} />
                                    <input style={inputStyle} value={hab.tipo_acao} placeholder="Ação (Padrão, Livre...)" onChange={e => {
                                        const next = [...draft.habilidades]; next[idx] = { ...hab, tipo_acao: e.target.value }; setDraft({ ...draft, habilidades: next });
                                    }} />
                                    <button
                                        type="button"
                                        onClick={() => setDraft({ ...draft, habilidades: draft.habilidades.filter((_, j) => j !== idx) })}
                                        style={{ background: '#3a2222', color: '#ff8a80', border: '1px solid #663333', borderRadius: 4, padding: '6px 8px', cursor: 'pointer' }}
                                    >
                                        ✕
                                    </button>
                                </div>
                                <textarea
                                    rows={2}
                                    style={{ ...inputStyle, resize: 'vertical' }}
                                    value={hab.descricao}
                                    placeholder="Descrição da habilidade..."
                                    onChange={e => {
                                        const next = [...draft.habilidades]; next[idx] = { ...hab, descricao: e.target.value }; setDraft({ ...draft, habilidades: next });
                                    }}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
                <div className="card-form" style={{ padding: '30px' }}>
                    <div style={{ borderBottom: '2px solid var(--accent-color)', paddingBottom: '10px', marginBottom: '20px' }}>
                        <h1 style={{ margin: 0, color: 'var(--accent-color)', fontSize: '2.5rem' }}>{ameaca.nome}</h1>
                        <div style={{ fontSize: '1.2rem', color: '#aaa', marginTop: '5px' }}>
                            {ameaca.tipo} {ameaca.subtipo ? `(${ameaca.subtipo})` : ''} {ameaca.tamanho} • <strong style={{ color: '#fff' }}>ND {ameaca.nd}</strong>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', textAlign: 'center', marginBottom: '20px' }}>
                        <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>PV</strong><br/>{ameaca.pontos_de_vida}</div>
                        <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Defesa</strong><br/>{ameaca.defesa}</div>
                        <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Deslocamento</strong><br/>{ameaca.deslocamento}</div>
                        <div style={{ background: '#252525', padding: '10px', borderRadius: '8px' }}><strong>Iniciativa</strong><br/>{ameaca.iniciativa > 0 ? `+${ameaca.iniciativa}` : ameaca.iniciativa}</div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', textAlign: 'center', marginBottom: '20px', color: '#ccc', fontSize: '0.9rem' }}>
                        <div><strong>Fort:</strong> {ameaca.fortitude > 0 ? `+${ameaca.fortitude}` : ameaca.fortitude}</div>
                        <div><strong>Ref:</strong> {ameaca.reflexos > 0 ? `+${ameaca.reflexos}` : ameaca.reflexos}</div>
                        <div><strong>Von:</strong> {ameaca.vontade > 0 ? `+${ameaca.vontade}` : ameaca.vontade}</div>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-around', background: '#1a1a1a', padding: '15px', borderRadius: '8px', marginBottom: '30px', border: '1px solid #333' }}>
                        {Object.entries(ameaca.atributos).map(([key, val]) => (
                            <div key={key} style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: '0.8rem', color: '#888', textTransform: 'uppercase' }}>{key}</div>
                                <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>{val ?? '—'}</div>
                            </div>
                        ))}
                    </div>

                    {ameaca.ataques && ameaca.ataques.length > 0 && (
                        <div style={{ marginBottom: '30px' }}>
                            <h2 style={{ color: 'var(--accent-color)', borderBottom: '1px solid #333', paddingBottom: '5px' }}>Ações de Combate</h2>
                            {ameaca.ataques.map((atk, i) => (
                                <div key={i} style={{ marginBottom: '10px', color: '#ccc' }}>
                                    <strong style={{ color: '#fff' }}>{atk.nome}</strong> ({atk.modalidade}) — 
                                    Ataque: <strong>+{atk.bonus_ataque}</strong>, 
                                    Dano: <strong>{atk.dano} {atk.tipo_dano}</strong>, 
                                    Crítico: {atk.margem_critico}/x{atk.multiplicador_critico}
                                    {atk.descricao && <span style={{ color: '#888' }}> ({atk.descricao})</span>}
                                </div>
                            ))}
                        </div>
                    )}

                    {ameaca.habilidades && ameaca.habilidades.length > 0 && (
                        <div style={{ marginBottom: '30px' }}>
                            <h2 style={{ color: 'var(--accent-color)', borderBottom: '1px solid #333', paddingBottom: '5px' }}>Habilidades</h2>
                            {ameaca.habilidades.map((hab, i) => (
                                <div key={i} style={{ marginBottom: '15px', color: '#ccc', lineHeight: '1.5' }}>
                                    <strong style={{ color: '#fff' }}>{hab.nome}</strong> 
                                    <span style={{ fontSize: '0.8rem', color: '#888', marginLeft: '10px' }}>({hab.tipo_acao})</span> — 
                                    {hab.descricao}
                                    {hab.rolls && hab.rolls.length > 0 && (
                                        <span style={{ marginLeft: '5px', color: '#9c27b0', fontWeight: 'bold' }}>[{hab.rolls.join(', ')}]</span>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    {ameaca.tesouro && (
                        <div style={{ marginTop: '20px', color: '#aaa', fontSize: '0.9rem' }}>
                            <strong>Tesouro:</strong> {ameaca.tesouro}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default AmeacaDetail;
