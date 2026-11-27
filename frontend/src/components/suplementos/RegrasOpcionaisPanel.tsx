import React, { useEffect, useMemo, useState } from 'react';
import type { ComplicacaoPersonagem, Personagem } from '../../types';
import { fetchDadosRegrasOpcionais } from '../../services/api';
import { EntitySelectorModal, type EntityItem } from '../EntitySelectorModal';

interface Props {
    ficha: Personagem;
    onUpdate: (dados: Partial<Personagem>) => void;
}

interface ComplicacaoCatalogoItem {
    nome: string;
    categoria: string;
    descricao: string;
    classe?: string;
}

export const RegrasOpcionaisPanel: React.FC<Props> = ({ ficha, onUpdate }) => {
    const [catalogo, setCatalogo] = useState<any>(null);
    const [modalCompAberto, setModalCompAberto] = useState(false);

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

    // Unifica as 73 complicações oficiais (32 gerais + 22 de classe + 19 de idade)
    const todasComplicacoes = useMemo<Record<string, ComplicacaoCatalogoItem>>(() => {
        const mapa: Record<string, ComplicacaoCatalogoItem> = {};
        if (!catalogo) return mapa;
        const addDict = (dict: any, categoriaPadrao: string) => {
            if (!dict || typeof dict !== 'object') return;
            Object.entries(dict).forEach(([chave, val]: [string, any]) => {
                const nome = val?.nome || chave;
                const cat = val?.classe
                    ? `Restrição de Classe (${val.classe})`
                    : categoriaPadrao;
                mapa[nome] = {
                    nome,
                    categoria: cat,
                    descricao: val?.descricao || '',
                    classe: val?.classe,
                };
            });
        };
        addDict(catalogo.complicacoes, 'Geral');
        addDict(catalogo.complicacoes_gerais, 'Complicação Geral');
        addDict(catalogo.complicacoes_classe, 'Restrição de Classe');
        addDict(catalogo.complicacoes_idade, 'Complicação de Idade');
        return mapa;
    }, [catalogo]);

    const itensModalComplicacoes = useMemo<EntityItem[]>(() => {
        const jaTem = new Set(complicacoes.map(c => c.nome));
        return Object.values(todasComplicacoes)
            .filter(c => !jaTem.has(c.nome))
            .sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'))
            .map((c): EntityItem => ({
                nome: c.nome,
                icone: 'alerta',
                bonus: c.categoria,
                descricao: c.descricao,
                tooltip: `${c.nome} — ${c.categoria}\nDescrição: ${c.descricao}\nBenefício: Concede +1 Poder Geral adicional (Heróis de Arton, Cap. 4).`,
                fonte: 'Heróis de Arton',
            }));
    }, [todasComplicacoes, complicacoes]);

    const handleAddComp = (nomeAlvo: string) => {
        const info = todasComplicacoes[nomeAlvo];
        if (!info) return;
        const nova: ComplicacaoPersonagem = {
            nome: info.nome,
            descricao: info.descricao || '',
            poder_bonus: '',
            fonte: 'Heróis de Arton',
        };
        onUpdate({ complicacoes: [...complicacoes, nova] });
        setModalCompAberto(false);
    };

    const handleRemComp = (nome: string) => {
        onUpdate({ complicacoes: complicacoes.filter(c => c.nome !== nome) });
    };

    const papeis = catalogo?.papeis_grupo ? Object.keys(catalogo.papeis_grupo) : [];
    const objetivos = catalogo?.objetivos_heroicos ? Object.keys(catalogo.objetivos_heroicos) : [];
    const totalComplicacoesCatalogo = Object.keys(todasComplicacoes).length;

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
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>
                        Complicações ({complicacoes.length}) — cada complicação concede +1 Poder Geral
                    </div>
                    <button
                        type="button"
                        onClick={() => setModalCompAberto(true)}
                        disabled={itensModalComplicacoes.length === 0}
                        style={{
                            background: '#ffd700',
                            color: '#111',
                            border: 'none',
                            borderRadius: 6,
                            padding: '7px 14px',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            fontSize: '0.82rem',
                        }}
                    >
                        + Escolher Complicação ({totalComplicacoesCatalogo})
                    </button>
                </div>

                {complicacoes.length > 0 && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        {complicacoes.map(c => (
                            <div
                                key={c.nome}
                                style={{
                                    background: '#16161c',
                                    border: '1px solid rgba(255, 183, 77, 0.35)',
                                    borderRadius: 6,
                                    padding: '8px 12px',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'flex-start',
                                    gap: 10,
                                }}
                            >
                                <div>
                                    <div style={{ fontWeight: 'bold', color: '#ffb74d', fontSize: '0.88rem' }}>
                                        {c.nome}
                                    </div>
                                    <div style={{ fontSize: '0.78rem', color: '#cbd5e1', marginTop: 3, lineHeight: 1.4 }}>
                                        {c.descricao || todasComplicacoes[c.nome]?.descricao}
                                    </div>
                                </div>
                                <button
                                    type="button"
                                    onClick={() => handleRemComp(c.nome)}
                                    style={{
                                        background: '#3a2222',
                                        color: '#ff8a80',
                                        border: '1px solid #663333',
                                        borderRadius: 4,
                                        padding: '4px 9px',
                                        cursor: 'pointer',
                                        fontSize: '0.76rem',
                                        whiteSpace: 'nowrap',
                                    }}
                                >
                                    Remover
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <EntitySelectorModal
                aberto={modalCompAberto}
                titulo={`Escolher Complicação (${totalComplicacoesCatalogo})`}
                iconeTitulo="alerta"
                itens={itensModalComplicacoes}
                onConfirm={handleAddComp}
                onFechar={() => setModalCompAberto(false)}
            />
        </div>
    );
};
