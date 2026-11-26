import { useState } from 'react';
import type { WizardStepProps } from '../../../types/wizard';
import type { Magia } from '../../../types';
import { GrimorioModal } from '../../GrimorioModal';
import { SpellDetailsModal } from '../../SpellDetailsModal';
import { calcularLimitePmMagiaView, getCircleColor } from '../../../utils/magicUtils';
import { T20Icon } from '../../T20Icon';

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

export function StepMagias({ ficha, updateFicha, dadosMagias }: WizardStepProps) {
    const [showGrimorio, setShowGrimorio] = useState(false);
    const [viewSpell, setViewSpell] = useState<Magia | null>(null);

    const magias = ficha.combate?.magias || [];
    const circuloMaximo = Number((ficha.combate as any)?.circulo_maximo || 0);
    const limiteMagias = (ficha.combate as any)?.limite_magias ?? null;
    const cdMagias = ficha.combate?.cd_magias ?? 10;
    const limitePm = calcularLimitePmMagiaView(ficha);

    const handleAddMagia = (magia: Magia) => {
        if (magias.some(m => m.nome === magia.nome)) return;
        updateFicha({
            combate: { ...ficha.combate, magias: [...magias, magia] },
        }, true);
    };

    const handleRemoveMagia = (nome: string) => {
        updateFicha({
            combate: { ...ficha.combate, magias: magias.filter(m => m.nome !== nome) },
        }, true);
    };

    return (
        <div style={{ fontFamily: FONT_BODY, textTransform: 'none' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12, marginBottom: 18 }}>
                <div>
                    <h2 style={{ color: '#ffd700', margin: '0 0 6px', fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                        <T20Icon name="grimorio" size={22} /> Passo 6: Grimório & Magias
                    </h2>
                    <p style={{ color: '#94a3b8', margin: 0, fontSize: '0.92rem' }}>
                        {circuloMaximo > 0
                            ? 'Escolha as magias iniciais do seu conjurador.'
                            : 'Sua classe não conjura magias inicialmente — você pode avançar direto para a Revisão.'}
                    </p>
                </div>
                {circuloMaximo > 0 && (
                    <button
                        type="button"
                        onClick={() => setShowGrimorio(true)}
                        style={{
                            background: '#7b1fa2',
                            color: '#fff',
                            border: 'none',
                            borderRadius: 8,
                            padding: '10px 18px',
                            fontWeight: 700,
                            cursor: 'pointer',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: 6,
                        }}
                    >
                        <T20Icon name="grimorio" size={16} /> + Adicionar Magia
                    </button>
                )}
            </div>

            {circuloMaximo > 0 && (
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 20 }}>
                    <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>Círculo Máximo</div>
                        <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#ce93d8' }}>{circuloMaximo}º Círculo</div>
                    </div>
                    <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>Magias Conhecidas</div>
                        <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#ffd700' }}>
                            {magias.length}{limiteMagias ? ` / ${limiteMagias}` : ''}
                        </div>
                    </div>
                    <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>CD das Magias</div>
                        <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#ffb74d' }}>CD {cdMagias}</div>
                    </div>
                    <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>Limite de PM</div>
                        <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#80deea' }}>{limitePm.limite} PM</div>
                    </div>
                </div>
            )}

            {magias.length === 0 ? (
                <div style={{ background: '#1a1d2e', border: '1px dashed #3a4066', borderRadius: 10, padding: 28, textAlign: 'center', color: '#94a3b8' }}>
                    {circuloMaximo > 0
                        ? 'Nenhuma magia adicionada ainda. Clique em "+ Adicionar Magia" para abrir o Grimório.'
                        : 'Nenhuma magia conhecida.'}
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 10 }}>
                    {magias.map(m => (
                        <div
                            key={m.nome}
                            onClick={() => setViewSpell(m)}
                            style={{
                                background: '#1a1d2e',
                                border: '1px solid #32385a',
                                borderRadius: 8,
                                padding: 12,
                                cursor: 'pointer',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                gap: 8,
                            }}
                        >
                            <div>
                                <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: '0.94rem' }}>{m.nome}</div>
                                <div style={{ fontSize: '0.76rem', color: '#94a3b8', marginTop: 2 }}>
                                    <span style={{ color: getCircleColor(m.circulo), fontWeight: 700 }}>{m.circulo}º</span> • {m.escola} • {m.custo_pm} PM
                                </div>
                            </div>
                            <button
                                type="button"
                                onClick={(e) => { e.stopPropagation(); handleRemoveMagia(m.nome); }}
                                title="Esquecer magia"
                                style={{ background: 'transparent', border: 'none', color: '#f87171', cursor: 'pointer', padding: 4 }}
                            >
                                <T20Icon name="excluir" size={14} />
                            </button>
                        </div>
                    ))}
                </div>
            )}

            <GrimorioModal
                ficha={ficha}
                isOpen={showGrimorio}
                onClose={() => setShowGrimorio(false)}
                onAddMagia={handleAddMagia}
                dadosMagias={dadosMagias}
                magiasConhecidas={magias}
                pmAtual={ficha.status.pm.atual}
                pmMaximo={ficha.status.pm.maximo}
                circuloMaximo={circuloMaximo}
                limiteMagias={limiteMagias}
            />

            <SpellDetailsModal
                ficha={ficha}
                magia={viewSpell}
                onClose={() => setViewSpell(null)}
                onRemove={() => { if (viewSpell) { handleRemoveMagia(viewSpell.nome); setViewSpell(null); } }}
            />
        </div>
    );
}