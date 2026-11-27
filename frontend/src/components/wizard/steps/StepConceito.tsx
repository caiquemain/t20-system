import { useState } from 'react';
import { SelectionModal } from '../SelectionModal';
import { T20Icon } from '../../T20Icon';
import { formatarTooltipDeus } from '../../../utils/deusTooltip';
import {
    SUPLEMENTOS_OFICIAIS,
    TODOS_SUPLEMENTOS_IDS,
    entidadePermitidaPorSuplementos,
} from '../../../utils/suplementos';
import type { WizardStepProps } from '../../../types/wizard';

type ModalAberto = 'raca' | 'origem' | 'deus' | null;

export function StepConceito({ ficha, updateFicha, listaRacas, listaOrigens, listaDeuses, dadosRacas, dadosOrigens, dadosDeuses }: WizardStepProps) {
    const [modal, setModal] = useState<ModalAberto>(null);

    const suplementosAtivos = (ficha.suplementos_ativos && ficha.suplementos_ativos.length > 0)
        ? ficha.suplementos_ativos
        : TODOS_SUPLEMENTOS_IDS;

    const toggleSuplemento = (id: string) => {
        if (id === 'T20 JdA') return;
        const existe = suplementosAtivos.includes(id);
        const novos = existe
            ? suplementosAtivos.filter(s => s !== id)
            : [...suplementosAtivos, id];
        updateFicha({ suplementos_ativos: novos }, true);
    };

    const getDeusesPermitidos = () => {
        const raca = ficha.cabecalho.raca;
        const classe = ficha.classes[0]?.nome;
        const base = (raca === 'Humano' || classe === 'Clérigo')
            ? listaDeuses
            : listaDeuses.filter(nomeDeus => {
                const dados = dadosDeuses[nomeDeus];
                if (!dados) return false;
                const permitidos = dados.devotos || [];
                if (permitidos.includes("Todos") || permitidos.includes("Quaisquer") || permitidos.includes(raca) || permitidos.includes(classe)) return true;
                if (nomeDeus === "Thwor" && ["Goblin", "Hobgoblin", "Bugbear", "Orc", "Ogro"].includes(raca)) return true;
                return false;
            });
        return base.filter(d => entidadePermitidaPorSuplementos(dadosDeuses[d]?.fonte, suplementosAtivos));
    };

    const ehGolem = (ficha.cabecalho.raca || '').toLowerCase() === 'golem';

    const CardSelecao = ({ rotulo, valor, placeholder, onOpen, cor, desabilitado }: any) => (
        <div
            onClick={() => !desabilitado && onOpen()}
            style={{
                background: '#1a1a1a', border: `1px solid ${valor ? '#444' : '#5a4a1a'}`,
                borderRadius: 10, padding: '16px 20px',
                cursor: desabilitado ? 'not-allowed' : 'pointer',
                opacity: desabilitado ? 0.55 : 1,
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}
        >
            <div>
                <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: 4 }}>{rotulo}</div>
                <div style={{ fontSize: '1.1rem', color: valor ? cor || '#fff' : '#666' }}>
                    {valor || placeholder}
                </div>
            </div>
            {!desabilitado && <span style={{ color: '#ffd700', fontSize: '1.2rem' }}>▸</span>}
        </div>
    );

    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px', display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                <T20Icon name="nota" size={22} /> Passo 1: Conceito do Personagem
            </h2>
            <p style={{ color: '#aaa', marginBottom: '22px' }}>
                Defina a identidade básica do seu herói. Clique nos cards para abrir a seleção.
            </p>

            {/* Toggle de Livros / Suplementos Ativos na Ficha */}
            <div style={{
                maxWidth: 700,
                marginBottom: 20,
                padding: '12px 14px',
                background: 'rgba(22, 24, 41, 0.7)',
                border: '1px solid #32385a',
                borderRadius: 10,
                fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
                textTransform: 'none',
            }}>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: 8, fontWeight: 600, letterSpacing: '0.03em' }}>
                    LIVROS PERMITIDOS NA FICHA
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {SUPLEMENTOS_OFICIAIS.map(sup => {
                        const ativo = suplementosAtivos.includes(sup.id);
                        return (
                            <button
                                key={sup.id}
                                type="button"
                                disabled={sup.basico}
                                onClick={() => toggleSuplemento(sup.id)}
                                style={{
                                    fontSize: '0.76rem',
                                    padding: '4px 10px',
                                    borderRadius: 999,
                                    cursor: sup.basico ? 'default' : 'pointer',
                                    border: `1px solid ${ativo ? sup.cor : '#334155'}`,
                                    background: ativo ? `${sup.cor}38` : 'transparent',
                                    color: ativo ? '#f8fafc' : '#64748b',
                                    fontWeight: ativo ? 700 : 500,
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: 5,
                                    opacity: sup.basico ? 0.9 : 1,
                                }}
                            >
                                {ativo && <T20Icon name="check" size={11} color="#ffd700" />}
                                {sup.sigla}
                            </button>
                        );
                    })}
                </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: 700 }}>
                <div>
                    <label style={{ display: 'block', marginBottom: 8, color: '#ccc' }}>Nome do Personagem</label>
                    <input
                        type="text"
                        value={ficha.cabecalho.nome}
                        onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, nome: e.target.value } })}
                        placeholder="Ex: Thorin, Elara, Zephyr..."
                        style={{ width: '100%', padding: 12, background: '#1a1a1a', border: '1px solid #555', borderRadius: 8, color: '#fff', fontSize: '1rem' }}
                    />
                </div>

                <CardSelecao rotulo="RAÇA" valor={ficha.cabecalho.raca} placeholder="Escolher raça..." onOpen={() => setModal('raca')} />
                <CardSelecao
                    rotulo="ORIGEM"
                    valor={ehGolem ? 'Sem origem (Golem)' : ficha.cabecalho.origem}
                    placeholder="Escolher origem..."
                    onOpen={() => setModal('origem')}
                    desabilitado={ehGolem}
                />
                <CardSelecao
                    rotulo="DIVINDADE (OPCIONAL)"
                    valor={ficha.cabecalho.deus}
                    placeholder="Sem devoção"
                    onOpen={() => setModal('deus')}
                    cor="#ffd700"
                />
            </div>

            <SelectionModal
                isOpen={modal === 'raca'}
                onClose={() => setModal(null)}
                title="Escolha sua Raça"
                icon="raca"
                selected={ficha.cabecalho.raca}
                items={listaRacas
                    .filter(r => entidadePermitidaPorSuplementos(dadosRacas[r]?.fonte, suplementosAtivos))
                    .map(r => ({
                        nome: r,
                        descricao: dadosRacas[r]?.descricao,
                        fonte: dadosRacas[r]?.fonte || 'T20 JdA',
                        tags: Object.entries(dadosRacas[r]?.attrs || {}).map(([k, v]: any) => `${k} ${v > 0 ? '+' + v : v}`),
                    }))}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, raca: nome }, escolhas_atributos_raciais: [] }, true)}
            />
            <SelectionModal
                isOpen={modal === 'origem'}
                onClose={() => setModal(null)}
                title="Escolha sua Origem"
                icon="origem"
                selected={ficha.cabecalho.origem}
                items={listaOrigens
                    .filter(o => entidadePermitidaPorSuplementos(dadosOrigens[o]?.fonte, suplementosAtivos))
                    .map(o => ({
                        nome: o,
                        descricao: dadosOrigens[o]?.descricao,
                        fonte: dadosOrigens[o]?.fonte || 'T20 JdA',
                    }))}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, origem: nome }, escolhas_origem: [] }, true)}
            />
            <SelectionModal
                isOpen={modal === 'deus'}
                onClose={() => setModal(null)}
                title="Escolha sua Divindade"
                icon="deus"
                selected={ficha.cabecalho.deus}
                items={[
                    { nome: '', descricao: 'Remover devoção' },
                    ...getDeusesPermitidos().map(d => {
                        const info = dadosDeuses[d];
                        const tags: string[] = [];
                        if (info?.titulo) tags.push(info.titulo);
                        if (info?.energia) tags.push(`Energia: ${info.energia}`);
                        tags.push(`Arma: ${info?.arma || 'Nenhuma'}`);
                        return {
                            nome: d,
                            tags,
                            descricao: info?.crencas || info?.descricao,
                            tooltip: formatarTooltipDeus(d, info),
                            fonte: info?.fonte || 'T20 JdA',
                        };
                    })
                ]}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, deus: nome } }, true)}
            />
        </div>
    );
}