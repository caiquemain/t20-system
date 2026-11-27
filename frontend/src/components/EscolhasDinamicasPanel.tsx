import React, { useState } from 'react';
import { T20Icon } from './T20Icon';
import { EntitySelectorModal, type EntityItem } from './EntitySelectorModal';

interface OpcaoEscolha {
    valor: string;
    rotulo: string;
    bonus?: string;
    descricao?: string;
    tooltip?: string;
    fonte?: string;
}

interface GatilhoEscolha {
    chave: string;
    rotulo: string;
    opcoes?: Array<string | OpcaoEscolha>;
    tipo_dinamico?: string;
    depende_de?: { chave: string; contem?: string; igual?: string };
}

interface EscolhasDinamicasPanelProps {
    ficha: any;
    habilidades: any[];
    dadosEscolhas: any;
    dadosHabilidadesClasse: Record<string, any>;
    dadosMagias: Record<string, any>;
    listaPoderes: any[];
    onChangeEscolha: (habNome: string, chave: string, valor: string) => void;
    titulo?: string;
}

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

function normalizarOpcoes(lista: Array<string | OpcaoEscolha>): OpcaoEscolha[] {
    return lista.map(it =>
        typeof it === 'string'
            ? { valor: it, rotulo: it }
            : { valor: it.valor, rotulo: it.rotulo, bonus: it.bonus, descricao: it.descricao, tooltip: it.tooltip, fonte: it.fonte }
    );
}

/**
 * Painel genérico guiado por `/dados/escolhas` (PODERES_COM_ESCOLHA).
 * Renderiza automaticamente seletores filtrados conforme as regras oficiais do livro
 * para habilidades raciais, origens regionais e poderes com escolha secundária.
 * Seletores com listas ricas (ex.: Duplo Feérico, Magias, Poderes) abrem o modal
 * 2 colunas (EntitySelectorModal) com busca e painel lateral de descrição completa.
 */
export const EscolhasDinamicasPanel: React.FC<EscolhasDinamicasPanelProps> = ({
    ficha,
    habilidades,
    dadosEscolhas,
    dadosHabilidadesClasse,
    dadosMagias,
    listaPoderes,
    onChangeEscolha,
    titulo = 'Escolhas de Raça & Origem',
}) => {
    const [modalAtivo, setModalAtivo] = useState<{
        habNome: string;
        chave: string;
        titulo: string;
        valorAtual: string;
        opcoes: OpcaoEscolha[];
    } | null>(null);

    const mapaPoderes: Record<string, GatilhoEscolha[]> = dadosEscolhas?.PODERES_COM_ESCOLHA || {};
    const classeAtual = ficha?.classes?.[0]?.nome || '';

    const habilidadesConfiguraveis = (habilidades || []).filter(
        h => h && h.nome && Array.isArray(mapaPoderes[h.nome]) && mapaPoderes[h.nome].length > 0
    );

    if (habilidadesConfiguraveis.length === 0) return null;

    const buscarDescricaoHabClasse = (it: any): string => {
        if (it?.descricao) return String(it.descricao);
        if (it?.chave_catalogo && dadosHabilidadesClasse?.[it.chave_catalogo]?.descricao) {
            return String(dadosHabilidadesClasse[it.chave_catalogo].descricao);
        }
        const match = Object.values(dadosHabilidadesClasse || {}).find(
            (h: any) => h?.nome === it?.nome && (!it?.classe || h?.classe === it?.classe)
        );
        return match?.descricao ? String(match.descricao) : '';
    };

    const resolverOpcoes = (g: GatilhoEscolha): OpcaoEscolha[] => {
        if (Array.isArray(g.opcoes) && g.opcoes.length > 0) {
            return normalizarOpcoes(g.opcoes);
        }

        const td = g.tipo_dinamico;
        if (td === 'habilidade_classe_nv1_outra') {
            const lista = Array.isArray(dadosEscolhas?.HABILIDADES_CLASSE_NV1)
                ? dadosEscolhas.HABILIDADES_CLASSE_NV1
                : [];
            return lista
                .filter((it: any) => !classeAtual || it.classe !== classeAtual)
                .map((it: any) => {
                    const desc = buscarDescricaoHabClasse(it);
                    const sub = `Habilidade de 1º Nível (${it.classe})`;
                    return {
                        valor: it.valor,
                        rotulo: it.rotulo,
                        bonus: it.classe,
                        descricao: desc || sub,
                        tooltip: `${it.rotulo} — ${sub}\n${desc ? `Descrição: ${desc}` : ''}`,
                        fonte: it.fonte || 'T20 JdA',
                    };
                });
        }

        if (td === 'magia_1_qualquer' || td === 'magia_1_arcana' || td === 'magia_1_adivinhacao') {
            return Object.values(dadosMagias || {})
                .filter((m: any) => {
                    if (Number(m?.circulo) !== 1) return false;
                    if (td === 'magia_1_arcana' && m?.tipo !== 'Arcana' && m?.tipo !== 'Universal') return false;
                    if (td === 'magia_1_adivinhacao' && (m?.escola || '').toLowerCase() !== 'adivinhação') return false;
                    return true;
                })
                .map((m: any) => {
                    const meta = [m.tipo, m.escola, m.execucao, m.alcance, m.duracao].filter(Boolean).join(' • ');
                    const desc = m.descricao || '';
                    return {
                        valor: m.nome,
                        rotulo: `${m.nome} (${m.escola})`,
                        bonus: `${m.tipo || 'Magia'} • ${m.escola || ''}`,
                        descricao: desc,
                        tooltip: `${m.nome} — ${meta}\n${m.resistencia ? `Resistência: ${m.resistencia}\n` : ''}${desc ? `Descrição: ${desc}` : ''}`,
                        fonte: m.fonte || 'T20 JdA',
                    };
                })
                .sort((a, b) => a.rotulo.localeCompare(b.rotulo));
        }

        if (td === 'poder_classe_atual') {
            return Object.values(dadosHabilidadesClasse || {})
                .filter((h: any) => h?.classe === classeAtual && String(h?.tipo || '').includes('Poder de'))
                .map((h: any) => ({
                    valor: h.nome,
                    rotulo: h.nome,
                    bonus: `Poder de ${classeAtual}`,
                    descricao: h.descricao || '',
                    tooltip: `${h.nome} — Poder de ${classeAtual}\n${h.descricao ? `Descrição: ${h.descricao}` : ''}`,
                    fonte: h.fonte || 'T20 JdA',
                }))
                .sort((a, b) => a.rotulo.localeCompare(b.rotulo));
        }

        if (td === 'poder_tormenta') {
            return (listaPoderes || [])
                .filter((p: any) => p?.categoria === 'Tormenta')
                .map((p: any) => ({
                    valor: p.nome,
                    rotulo: p.nome,
                    bonus: 'Poder da Tormenta',
                    descricao: p.descricao || '',
                    tooltip: `${p.nome} — Poder da Tormenta\n${p.descricao ? `Descrição: ${p.descricao}` : ''}`,
                    fonte: p.fonte || 'T20 JdA',
                }))
                .sort((a, b) => a.rotulo.localeCompare(b.rotulo));
        }

        if (td === 'poder_combate_ou_tormenta') {
            return (listaPoderes || [])
                .filter((p: any) => p?.categoria === 'Combate' || p?.categoria === 'Tormenta')
                .map((p: any) => ({
                    valor: p.nome,
                    rotulo: `${p.nome} (${p.categoria})`,
                    bonus: `Poder de ${p.categoria}`,
                    descricao: p.descricao || '',
                    tooltip: `${p.nome} — Poder de ${p.categoria}\n${p.descricao ? `Descrição: ${p.descricao}` : ''}`,
                    fonte: p.fonte || 'T20 JdA',
                }))
                .sort((a, b) => a.rotulo.localeCompare(b.rotulo));
        }

        if (td === 'poder_geral_sem_concedido_tormenta') {
            return (listaPoderes || [])
                .filter((p: any) => p?.is_general && p?.categoria !== 'Tormenta' && p?.categoria !== 'Poder Concedido')
                .map((p: any) => ({
                    valor: p.nome,
                    rotulo: `${p.nome} (${p.categoria})`,
                    bonus: `Poder Geral • ${p.categoria}`,
                    descricao: p.descricao || '',
                    tooltip: `${p.nome} — Poder Geral (${p.categoria})\n${p.descricao ? `Descrição: ${p.descricao}` : ''}`,
                    fonte: p.fonte || 'T20 JdA',
                }))
                .sort((a, b) => a.rotulo.localeCompare(b.rotulo));
        }

        return [];
    };

    return (
        <div
            style={{
                background: '#1a1d2e',
                border: '1px solid #32385a',
                borderRadius: 10,
                padding: 16,
                fontFamily: FONT_BODY,
                textTransform: 'none',
            }}
        >
            <h4
                style={{
                    margin: '0 0 12px',
                    color: '#ffd700',
                    fontSize: '0.95rem',
                    fontFamily: 'Tormenta, serif',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 7,
                }}
            >
                <T20Icon name="efeito" size={16} color="#ffd700" /> {titulo}
            </h4>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {habilidadesConfiguraveis.map(hab => {
                    const gatilhos = mapaPoderes[hab.nome] || [];
                    const esc = hab.escolhas_aplicadas || {};
                    return (
                        <div
                            key={hab.nome}
                            style={{
                                background: '#121524',
                                border: '1px solid #2b3152',
                                borderRadius: 8,
                                padding: 12,
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 10,
                            }}
                        >
                            <div>
                                <div style={{ color: '#f8fafc', fontWeight: 700, fontSize: '0.9rem' }}>
                                    {hab.nome}
                                </div>
                                {hab.descricao && (
                                    <div style={{ color: '#94a3b8', fontSize: '0.76rem', marginTop: 3, lineHeight: 1.4 }}>
                                        {hab.descricao}
                                    </div>
                                )}
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 10 }}>
                                {gatilhos.map(g => {
                                    if (g.depende_de) {
                                        const depVal = String(esc[g.depende_de.chave] || '');
                                        if (g.depende_de.contem && !depVal.toLowerCase().includes(g.depende_de.contem.toLowerCase())) {
                                            return null;
                                        }
                                        if (g.depende_de.igual && depVal !== g.depende_de.igual) {
                                            return null;
                                        }
                                    }
                                    const opcoes = resolverOpcoes(g);
                                    const valorAtual = String(esc[g.chave] || '');
                                    const usarModal = Boolean(g.tipo_dinamico) || opcoes.length > 8;
                                    const opcaoAtual = opcoes.find(op => op.valor === valorAtual);

                                    if (usarModal) {
                                        return (
                                            <div key={g.chave} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                                                <label style={{ fontSize: '0.74rem', color: '#a5b4fc', fontWeight: 600 }}>
                                                    {g.rotulo}
                                                </label>
                                                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                                                    <input
                                                        readOnly
                                                        value={opcaoAtual ? opcaoAtual.rotulo : valorAtual}
                                                        placeholder="Clique em Selecionar para ver detalhes..."
                                                        onClick={() => setModalAtivo({
                                                            habNome: hab.nome,
                                                            chave: g.chave,
                                                            titulo: `${hab.nome} — ${g.rotulo}`,
                                                            valorAtual,
                                                            opcoes,
                                                        })}
                                                        style={{
                                                            flex: 1,
                                                            padding: '8px 10px',
                                                            background: '#1c2036',
                                                            border: valorAtual ? '1px solid #ffd700' : '1px solid #3a4066',
                                                            borderRadius: 6,
                                                            color: valorAtual ? '#fff' : '#94a3b8',
                                                            fontSize: '0.84rem',
                                                            cursor: 'pointer',
                                                        }}
                                                    />
                                                    <button
                                                        type="button"
                                                        onClick={() => setModalAtivo({
                                                            habNome: hab.nome,
                                                            chave: g.chave,
                                                            titulo: `${hab.nome} — ${g.rotulo}`,
                                                            valorAtual,
                                                            opcoes,
                                                        })}
                                                        style={{
                                                            background: '#ffd700',
                                                            color: '#111',
                                                            border: 'none',
                                                            borderRadius: 6,
                                                            padding: '8px 14px',
                                                            fontWeight: 700,
                                                            fontSize: '0.8rem',
                                                            cursor: 'pointer',
                                                            whiteSpace: 'nowrap',
                                                        }}
                                                    >
                                                        Selecionar
                                                    </button>
                                                </div>
                                                {opcaoAtual?.descricao && (
                                                    <div style={{ fontSize: '0.74rem', color: '#cbd5e1', lineHeight: 1.4, marginTop: 2 }}>
                                                        {opcaoAtual.descricao}
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    }

                                    return (
                                        <div key={g.chave} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                                            <label style={{ fontSize: '0.74rem', color: '#a5b4fc', fontWeight: 600 }}>
                                                {g.rotulo}
                                            </label>
                                            <select
                                                value={valorAtual}
                                                onChange={e => onChangeEscolha(hab.nome, g.chave, e.target.value)}
                                                style={{
                                                    padding: '8px 10px',
                                                    background: '#1c2036',
                                                    border: valorAtual ? '1px solid #ffd700' : '1px solid #3a4066',
                                                    borderRadius: 6,
                                                    color: valorAtual ? '#fff' : '#94a3b8',
                                                    fontSize: '0.84rem',
                                                }}
                                            >
                                                <option value="">Selecione...</option>
                                                {opcoes.map(op => (
                                                    <option key={op.valor} value={op.valor}>
                                                        {op.rotulo}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    );
                })}
            </div>

            {modalAtivo && (
                <EntitySelectorModal
                    aberto={true}
                    titulo={modalAtivo.titulo}
                    iconeTitulo="efeito"
                    selecionado={modalAtivo.opcoes.find(o => o.valor === modalAtivo.valorAtual)?.rotulo || modalAtivo.valorAtual}
                    permitirVazio={true}
                    labelVazio="Limpar escolha"
                    itens={modalAtivo.opcoes.map((op): EntityItem => ({
                        nome: op.rotulo,
                        icone: 'efeito',
                        bonus: op.bonus,
                        descricao: op.descricao,
                        tooltip: op.tooltip || `${op.rotulo}\n${op.descricao ? `Descrição: ${op.descricao}` : ''}`,
                        fonte: op.fonte || 'T20 JdA',
                    }))}
                    onConfirm={(rotuloSelecionado) => {
                        if (!rotuloSelecionado) {
                            onChangeEscolha(modalAtivo.habNome, modalAtivo.chave, '');
                        } else {
                            const encontrado = modalAtivo.opcoes.find(o => o.rotulo === rotuloSelecionado);
                            onChangeEscolha(modalAtivo.habNome, modalAtivo.chave, encontrado ? encontrado.valor : rotuloSelecionado);
                        }
                        setModalAtivo(null);
                    }}
                    onFechar={() => setModalAtivo(null)}
                />
            )}
        </div>
    );
};
