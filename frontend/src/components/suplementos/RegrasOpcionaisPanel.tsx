import React, { useEffect, useMemo, useState } from 'react';
import type { ComplicacaoPersonagem, Personagem } from '../../types';
import { fetchDadosRegrasOpcionais } from '../../services/api';

interface Props {
    ficha: Personagem;
    onUpdate: (dados: Partial<Personagem>) => void;
}

export const RegrasOpcionaisPanel: React.FC<Props> = ({ ficha, onUpdate }) => {
    const [catalogo, setCatalogo] = useState<any>(null);
    const [compSelecionada, setCompSelecionada] = useState('');
    const [buscaComp, setBuscaComp] = useState('');

    useEffect(() => {
        fetchDadosRegrasOpcionais()
            .then(res => setCatalogo(res.data))
            .catch(() => {});
    }, []);

    const regrasAtivas: string[] = ficha.regras_opcionais_ativas || [];
    const complicacoes: ComplicacaoPersonagem[] = ficha.complicacoes || [];
    const papelGrupo = ficha.papel_grupo || '';
    const objetivoAtual = (ficha.objetivo_heroico as any)?.nome || '';

    const toggleRegra = (chave: string) => {
        const existe = regrasAtivas.includes(chave);
        onUpdate({
            regras_opcionais_ativas: existe
                ? regrasAtivas.filter(r => r !== chave)
                : [...regrasAtivas, chave],
        });
    };

    const listaComplicacoes = useMemo(() => {
        if (!catalogo?.complicacoes) return [];
        const jaTem = new Set(complicacoes.map(c => c.nome));
        const q = buscaComp.trim().toLowerCase();
        return Object.keys(catalogo.complicacoes)
            .filter(n => !jaTem.has(n) && (!q || n.toLowerCase().includes(q)))
            .sort((a, b) => a.localeCompare(b, 'pt-BR'));
    }, [catalogo, complicacoes, buscaComp]);

    const handleAddComp = () => {
        const alvo = compSelecionada || listaComplicacoes[0];
        if (!alvo || !catalogo?.complicacoes?.[alvo]) return;
        const info = catalogo.complicacoes[alvo];
        const nova: ComplicacaoPersonagem = {
            nome: alvo,
            descricao: info.descricao || '',
            poder_bonus: '',
            fonte: 'Heróis de Arton',
        };
        onUpdate({ complicacoes: [...complicacoes, nova] });
        setCompSelecionada('');
        setBuscaComp('');
    };

    const handleRemComp = (nome: string) => {
        onUpdate({ complicacoes: complicacoes.filter(c => c.nome !== nome) });
    };

    const papeis = catalogo?.papeis_grupo ? Object.keys(catalogo.papeis_grupo) : [];
    const objetivos = catalogo?.objetivos_heroicos ? Object.keys(catalogo.objetivos_heroicos) : [];

    return (
        <div className="section-card" style={{ marginBottom: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 12 }}>
                <h3 className="section-title" style={{ margin: 0 }}>
                    Regras Opcionais (Heróis de Arton, Cap. 4)
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                    Estritamente opt-in — nenhuma regra altera a ficha sem ser ativada
                </span>
            </div>

            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 14 }}>
                <label style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 10px', background: '#16161c', border: '1px solid #333', borderRadius: 4, cursor: 'pointer', fontSize: '0.82rem' }}>
                    <input
                        type="checkbox"
                        checked={regrasAtivas.includes('defesa_epica')}
                        onChange={() => toggleRegra('defesa_epica')}
                    />
                    <span><strong>Defesa Épica</strong> (+½ nível na Defesa)</span>
                </label>
                <label style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 10px', background: '#16161c', border: '1px solid #333', borderRadius: 4, cursor: 'pointer', fontSize: '0.82rem' }}>
                    <input
                        type="checkbox"
                        checked={regrasAtivas.includes('idades_variadas')}
                        onChange={() => toggleRegra('idades_variadas')}
                    />
                    <span><strong>Idades Variadas</strong></span>
                </label>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 12, marginBottom: 14 }}>
                <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', color: '#94a3b8', marginBottom: 4 }}>
                        Papel no Grupo
                    </label>
                    <select
                        value={papelGrupo}
                        onChange={e => onUpdate({ papel_grupo: e.target.value || null })}
                        style={{ width: '100%', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                    >
                        <option value="">Nenhum</option>
                        {papeis.map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                </div>
                <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', color: '#94a3b8', marginBottom: 4 }}>
                        Objetivo Heroico
                    </label>
                    <select
                        value={objetivoAtual}
                        onChange={e => {
                            const val = e.target.value;
                            onUpdate({
                                objetivo_heroico: val
                                    ? { nome: val, ...(catalogo?.objetivos_heroicos?.[val] || {}) }
                                    : null,
                            });
                        }}
                        style={{ width: '100%', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                    >
                        <option value="">Nenhum</option>
                        {objetivos.map(o => <option key={o} value={o}>{o}</option>)}
                    </select>
                </div>
            </div>

            <div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: 6, textTransform: 'uppercase' }}>
                    Complicações ({complicacoes.length}) — cada complicação concede +1 Poder Geral
                </div>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
                    <input
                        type="text"
                        value={buscaComp}
                        onChange={e => setBuscaComp(e.target.value)}
                        placeholder="Filtrar 73 complicações..."
                        style={{ flex: '1 1 160px', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.82rem' }}
                    />
                    <select
                        value={compSelecionada}
                        onChange={e => setCompSelecionada(e.target.value)}
                        style={{ flex: '2 1 200px', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.82rem' }}
                    >
                        <option value="">Selecione uma complicação ({listaComplicacoes.length})</option>
                        {listaComplicacoes.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                    <button
                        type="button"
                        onClick={handleAddComp}
                        disabled={listaComplicacoes.length === 0}
                        style={{ background: '#ffd700', color: '#111', border: 'none', borderRadius: 4, padding: '6px 12px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.82rem' }}
                    >
                        + Adicionar
                    </button>
                </div>
                {complicacoes.length > 0 && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {complicacoes.map(c => (
                            <div key={c.nome} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 8, background: '#16161c', border: '1px solid #2d2d36', borderRadius: 4, padding: '6px 10px', fontSize: '0.8rem' }}>
                                <div>
                                    <strong style={{ color: '#ffab91' }}>{c.nome}</strong>
                                    {c.descricao && <span style={{ color: '#94a3b8', marginLeft: 8 }}>{c.descricao}</span>}
                                </div>
                                <button
                                    type="button"
                                    onClick={() => handleRemComp(c.nome)}
                                    style={{ background: 'transparent', border: '1px solid #555', color: '#ef9a9a', borderRadius: 4, padding: '2px 7px', cursor: 'pointer', fontSize: '0.72rem' }}
                                >
                                    Remover
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};
