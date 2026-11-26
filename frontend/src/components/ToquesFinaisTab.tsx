import React from 'react';
import type { Personagem } from '../types';

interface ToquesFinaisTabProps {
    ficha: Personagem;
    onUpdate: (data: Partial<Personagem>, forceSave?: boolean) => void;
}

const ALINHAMENTOS: { codigo: string; nome: string; resumo: string }[] = [
    { codigo: '', nome: 'Não definido', resumo: 'Opcional — guia de conduta sem efeito em regras.' },
    { codigo: 'LB', nome: 'Leal e Bondoso (LB)', resumo: 'Respeita a lei, cumpre promessas e protege os necessitados.' },
    { codigo: 'NB', nome: 'Neutro e Bondoso (NB)', resumo: 'Ajuda o próximo acima de ordens ou leis rígidas.' },
    { codigo: 'CB', nome: 'Caótico e Bondoso (CB)', resumo: 'Espírito livre que promove o bem seguindo seus próprios instintos.' },
    { codigo: 'LN', nome: 'Leal e Neutro (LN)', resumo: 'Metódico e disciplinado; obedece a leis e códigos acima de tudo.' },
    { codigo: 'N', nome: 'Neutro (N)', resumo: 'Age por bom senso ou busca equilíbrio entre extremos.' },
    { codigo: 'CN', nome: 'Caótico e Neutro (CN)', resumo: 'Valoriza a própria liberdade; imprevisível e avesso a autoridade.' },
    { codigo: 'LM', nome: 'Leal e Maligno (LM)', resumo: 'Usa ordem, tradições e códigos de forma cruel e metódica.' },
    { codigo: 'NM', nome: 'Neutro e Maligno (NM)', resumo: 'Egoísta e oportunista; coloca a si mesmo acima de tudo.' },
    { codigo: 'CM', nome: 'Caótico e Maligno (CM)', resumo: 'Brutal, violento e imprevisível; rejeita qualquer regra.' },
];

const MULT_LONGEVIDADE: Record<string, number> = {
    'Anão': 2, 'Qareen': 2,
    'Dahllan': 5, 'Elfo': 5, 'Golem': 5, 'Osteon': 5, 'Sílfide': 5,
};

export const TABELA_TAMANHO_TOOLTIP: Record<string, string> = {
    'Minúsculo': 'Minúsculo — Espaço/Alcance: 1,5m | Furtividade +5 / Manobras –5 | Armas reduzidas (–1 passo de dano)',
    'Pequeno': 'Pequeno — Espaço/Alcance: 1,5m | Furtividade +2 / Manobras –2 | Armas médias',
    'Médio': 'Médio — Espaço/Alcance: 1,5m | Furtividade 0 / Manobras 0 | Armas médias',
    'Grande': 'Grande — Espaço/Alcance: 3m | Furtividade –2 / Manobras +2 | Armas aumentadas (+1 passo de dano)',
    'Enorme': 'Enorme — Espaço/Alcance: 4,5m | Furtividade –5 / Manobras +5 | Armas aumentadas (+1 passo de dano)',
    'Colossal': 'Colossal — Espaço/Alcance: 9m | Furtividade –10 / Manobras +10 | Armas gigantes (+2 passos de dano)',
};

export const ToquesFinaisTab: React.FC<ToquesFinaisTabProps> = ({ ficha, onUpdate }) => {
    const desc = ficha.descricao || ({} as Personagem['descricao']);
    const raca = ficha.cabecalho.raca || '';
    const mult = MULT_LONGEVIDADE[raca] || 1;
    const maduroIdade = 45 * mult;
    const velhoIdade = 70 * mult;
    const faixaAtual = desc.faixa_etaria || 'Adulto';

    const alinhamentoAtual = ALINHAMENTOS.find(a => a.codigo === (desc.alinhamento || '')) || ALINHAMENTOS[0];

    const atualizarDesc = (campo: string, valor: any, recalcular = false) => {
        onUpdate({
            descricao: {
                ...desc,
                [campo]: valor,
            }
        }, recalcular);
    };

    return (
        <div className="section-card" style={{ padding: 20 }}>
            <h3 className="section-title" style={{ marginTop: 0, marginBottom: 16 }}>
                Toques Finais — Identidade, Envelhecimento & Descrição
            </h3>

            {/* Linha 1: Idade, Faixa Etária e Alinhamento */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginBottom: 20 }}>
                <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid #333', borderRadius: 8, padding: 12 }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: 6 }}>
                        Idade (anos) {mult > 1 && <span style={{ color: '#ffd700' }}>• Raça Longeva (×{mult})</span>}
                    </label>
                    <input
                        type="number"
                        min={1}
                        className="input-dark"
                        style={{ width: '100%' }}
                        value={desc.idade ?? ''}
                        placeholder={`Ex: ${20 * mult}`}
                        onChange={e => {
                            const raw = e.target.value;
                            atualizarDesc('idade', raw === '' ? null : parseInt(raw, 10), true);
                        }}
                    />
                    <div style={{ fontSize: '0.72rem', color: '#888', marginTop: 6 }}>
                        Maduro: {maduroIdade}+ • Velho: {velhoIdade}+
                        {mult === 5 ? ' • Sem limite máximo' : ''}
                    </div>
                </div>

                <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid #333', borderRadius: 8, padding: 12 }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: 6 }}>
                        Faixa Etária (Envelhecimento)
                    </label>
                    <select
                        className="input-dark"
                        style={{ width: '100%' }}
                        value={faixaAtual}
                        onChange={e => {
                            onUpdate({
                                descricao: {
                                    ...desc,
                                    idade: null,
                                    faixa_etaria: e.target.value,
                                }
                            }, true);
                        }}
                    >
                        <option value="Adulto">Adulto (sem modificadores)</option>
                        <option value="Maduro">Maduro (For/Des/Con –1, Int/Sab/Car +1)</option>
                        <option value="Velho">Velho (For/Des/Con –3, Int/Sab/Car +2)</option>
                    </select>
                    <div style={{ fontSize: '0.72rem', color: faixaAtual === 'Adulto' ? '#888' : '#ffb74d', marginTop: 6 }}>
                        {faixaAtual === 'Adulto' && 'Sem penalidades ou bônus de idade.'}
                        {faixaAtual === 'Maduro' && 'Aplicado: For –1, Des –1, Con –1, Int +1, Sab +1, Car +1'}
                        {faixaAtual === 'Velho' && 'Aplicado (cumulativo): For –3, Des –3, Con –3, Int +2, Sab +2, Car +2'}
                    </div>
                </div>

                <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid #333', borderRadius: 8, padding: 12 }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: '#aaa', marginBottom: 6 }}>
                        Alinhamento
                    </label>
                    <select
                        className="input-dark"
                        style={{ width: '100%' }}
                        value={desc.alinhamento || ''}
                        onChange={e => atualizarDesc('alinhamento', e.target.value)}
                    >
                        {ALINHAMENTOS.map(a => (
                            <option key={a.codigo} value={a.codigo}>{a.nome}</option>
                        ))}
                    </select>
                    <div style={{ fontSize: '0.72rem', color: '#888', marginTop: 6 }}>
                        {alinhamentoAtual.resumo}
                    </div>
                </div>
            </div>

            {/* Linha 2: Textareas de Aparência, Personalidade, História e Anotações */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 16 }}>
                <div>
                    <label style={{ display: 'block', fontSize: '0.82rem', color: '#ccc', marginBottom: 6 }}>Aparência</label>
                    <textarea
                        className="input-dark"
                        rows={4}
                        style={{ width: '100%', resize: 'vertical' }}
                        placeholder="Traços físicos, vestimentas, cicatrizes, acessórios..."
                        value={desc.aparencia || ''}
                        onChange={e => atualizarDesc('aparencia', e.target.value)}
                    />
                </div>
                <div>
                    <label style={{ display: 'block', fontSize: '0.82rem', color: '#ccc', marginBottom: 6 }}>Personalidade</label>
                    <textarea
                        className="input-dark"
                        rows={4}
                        style={{ width: '100%', resize: 'vertical' }}
                        placeholder="Temperamento, ideais, defeitos, maneirismos..."
                        value={desc.personalidade || ''}
                        onChange={e => atualizarDesc('personalidade', e.target.value)}
                    />
                </div>
                <div>
                    <label style={{ display: 'block', fontSize: '0.82rem', color: '#ccc', marginBottom: 6 }}>História</label>
                    <textarea
                        className="input-dark"
                        rows={5}
                        style={{ width: '100%', resize: 'vertical' }}
                        placeholder="Passado do personagem, motivações, aliados e inimigos..."
                        value={desc.historia || ''}
                        onChange={e => atualizarDesc('historia', e.target.value)}
                    />
                </div>
                <div>
                    <label style={{ display: 'block', fontSize: '0.82rem', color: '#ccc', marginBottom: 6 }}>Anotações de Campanha</label>
                    <textarea
                        className="input-dark"
                        rows={5}
                        style={{ width: '100%', resize: 'vertical' }}
                        placeholder="Pistas, contatos, missões, tesouros..."
                        value={desc.anotacoes || ''}
                        onChange={e => atualizarDesc('anotacoes', e.target.value)}
                    />
                </div>
            </div>
        </div>
    );
};
