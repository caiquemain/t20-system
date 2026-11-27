import React, { useEffect, useState } from 'react';
import type { Personagem } from '../../types';
import { fetchDadosTreinador } from '../../services/api';

interface Props {
    ficha: Personagem;
    onUpdate: (dados: Partial<Personagem>) => void;
}

export const MelhorAmigoPanel: React.FC<Props> = ({ ficha, onUpdate }) => {
    const [catalogo, setCatalogo] = useState<any>(null);

    const ehTreinador = (ficha.classes || []).some(
        c => (c.nome || '').toLowerCase() === 'treinador'
    );

    useEffect(() => {
        if (!ehTreinador) return;
        fetchDadosTreinador()
            .then(res => setCatalogo(res.data))
            .catch(() => {});
    }, [ehTreinador]);

    if (!ehTreinador) return null;

    const amigos = (ficha as any).melhores_amigos || [];
    const amigo = amigos[0] || { nome: 'Melhor Amigo', tipo: 'Animal', tamanho: 'Médio', truques: [] };
    const calc = (ficha.combate as any)?.treinador_calc;

    const salvarAmigo = (patch: Record<string, any>) => {
        const atualizado = { ...amigo, ...patch };
        const lista = amigos.length > 0 ? [atualizado, ...amigos.slice(1)] : [atualizado];
        onUpdate({ melhores_amigos: lista } as any);
    };

    const tipos = catalogo?.tipos_melhor_amigo ? Object.keys(catalogo.tipos_melhor_amigo) : ['Animal', 'Construto', 'Espírito', 'Monstro', 'Morto-Vivo'];
    const truquesDisponiveis = catalogo?.truques ? Object.keys(catalogo.truques) : [];
    const truquesAtuais: string[] = amigo.truques || [];

    const toggleTruque = (truque: string) => {
        const existe = truquesAtuais.includes(truque);
        salvarAmigo({
            truques: existe ? truquesAtuais.filter(t => t !== truque) : [...truquesAtuais, truque],
        });
    };

    return (
        <div className="section-card" style={{ marginBottom: 16 }}>
            <h3 className="section-title" style={{ marginBottom: 10 }}>
                🐾 Melhor Amigo (Treinador)
            </h3>

            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 12 }}>
                <input
                    type="text"
                    value={amigo.nome || ''}
                    onChange={e => salvarAmigo({ nome: e.target.value })}
                    placeholder="Nome do Melhor Amigo"
                    style={{ flex: '1 1 180px', background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                />
                <select
                    value={amigo.tipo || 'Animal'}
                    onChange={e => salvarAmigo({ tipo: e.target.value })}
                    style={{ background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                >
                    {tipos.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <select
                    value={amigo.tamanho || 'Médio'}
                    onChange={e => salvarAmigo({ tamanho: e.target.value })}
                    style={{ background: '#141418', border: '1px solid #333', color: '#eee', borderRadius: 4, padding: '6px 10px', fontSize: '0.85rem' }}
                >
                    {['Minúsculo', 'Pequeno', 'Médio', 'Grande'].map(sz => (
                        <option key={sz} value={sz}>{sz}</option>
                    ))}
                </select>
            </div>

            {calc && (
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', padding: '8px 12px', background: 'rgba(255,215,0,0.06)', borderRadius: 6, marginBottom: 12, fontSize: '0.82rem' }}>
                    {calc.pv_max !== undefined && <span><strong style={{ color: '#ef9a9a' }}>PV:</strong> {calc.pv_max}</span>}
                    {calc.defesa !== undefined && <span><strong style={{ color: '#90caf9' }}>Defesa:</strong> {calc.defesa}</span>}
                    {calc.deslocamento !== undefined && <span><strong style={{ color: '#a5d6a7' }}>Desl.:</strong> {calc.deslocamento}m</span>}
                    {calc.ataque_bonus !== undefined && <span><strong style={{ color: '#ffcc80' }}>Ataque:</strong> +{calc.ataque_bonus}</span>}
                    {calc.dano_natural && <span><strong style={{ color: '#ffcc80' }}>Dano:</strong> {calc.dano_natural}</span>}
                </div>
            )}

            {truquesDisponiveis.length > 0 && (
                <div>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: 6, textTransform: 'uppercase' }}>
                        Truques ({truquesAtuais.length})
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                        {truquesDisponiveis.map(tr => {
                            const ativo = truquesAtuais.includes(tr);
                            return (
                                <button
                                    key={tr}
                                    type="button"
                                    onClick={() => toggleTruque(tr)}
                                    title={catalogo?.truques?.[tr]?.descricao || tr}
                                    style={{
                                        padding: '4px 9px',
                                        borderRadius: 4,
                                        fontSize: '0.76rem',
                                        cursor: 'pointer',
                                        background: ativo ? 'rgba(255,215,0,0.16)' : 'rgba(255,255,255,0.04)',
                                        border: ativo ? '1px solid #ffd700' : '1px solid #333',
                                        color: ativo ? '#ffd700' : '#ccc',
                                    }}
                                >
                                    {ativo ? '✓ ' : '+ '}{tr}
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};
