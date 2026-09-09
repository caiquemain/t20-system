import { useState } from 'react';
import { SelectionModal } from '../SelectionModal';
import type { WizardStepProps } from '../../../types/wizard';

type ModalAberto = 'raca' | 'origem' | 'deus' | null;

export function StepConceito({ ficha, updateFicha, listaRacas, listaOrigens, listaDeuses, dadosRacas, dadosOrigens, dadosDeuses }: WizardStepProps) {
    const [modal, setModal] = useState<ModalAberto>(null);

    const getDeusesPermitidos = () => {
        const raca = ficha.cabecalho.raca;
        const classe = ficha.classes[0]?.nome;
        if (raca === 'Humano' || classe === 'Clérigo') return listaDeuses;
        return listaDeuses.filter(nomeDeus => {
            const dados = dadosDeuses[nomeDeus];
            if (!dados) return false;
            const permitidos = dados.devotos || [];
            if (permitidos.includes("Todos") || permitidos.includes("Quaisquer") || permitidos.includes(raca) || permitidos.includes(classe)) return true;
            if (nomeDeus === "Thwor" && ["Goblin", "Hobgoblin", "Bugbear", "Orc", "Ogro"].includes(raca)) return true;
            return false;
        });
    };

    const CardSelecao = ({ rotulo, valor, placeholder, onOpen, cor }: any) => (
        <div
            onClick={onOpen}
            style={{
                background: '#1a1a1a', border: `1px solid ${valor ? '#444' : '#5a4a1a'}`,
                borderRadius: 10, padding: '16px 20px', cursor: 'pointer',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}
        >
            <div>
                <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: 4 }}>{rotulo}</div>
                <div style={{ fontSize: '1.1rem', color: valor ? cor || '#fff' : '#666' }}>
                    {valor || placeholder}
                </div>
            </div>
            <span style={{ color: '#ffd700', fontSize: '1.2rem' }}>▸</span>
        </div>
    );

    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px' }}>📝 Passo 1: Conceito do Personagem</h2>
            <p style={{ color: '#aaa', marginBottom: '30px' }}>
                Defina a identidade básica do seu herói. Clique nos cards para abrir a seleção.
            </p>

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
                <CardSelecao rotulo="ORIGEM" valor={ficha.cabecalho.origem} placeholder="Escolher origem..." onOpen={() => setModal('origem')} />
                <CardSelecao rotulo="DIVINDADE (OPCIONAL)" valor={ficha.cabecalho.deus} placeholder="Sem devoção" onOpen={() => setModal('deus')} cor="#ffd700" />
            </div>

            <SelectionModal
                isOpen={modal === 'raca'}
                onClose={() => setModal(null)}
                title="Escolha sua Raça"
                icon="🧬"
                selected={ficha.cabecalho.raca}
                items={listaRacas.map(r => ({
                    nome: r,
                    descricao: dadosRacas[r]?.descricao,
                    tags: Object.entries(dadosRacas[r]?.attrs || {}).map(([k, v]: any) => `${k} ${v > 0 ? '+' + v : v}`)
                }))}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, raca: nome }, escolhas_atributos_raciais: [] }, true)}
            />
            <SelectionModal
                isOpen={modal === 'origem'}
                onClose={() => setModal(null)}
                title="Escolha sua Origem"
                icon="🏕️"
                selected={ficha.cabecalho.origem}
                items={listaOrigens.map(o => ({ nome: o, descricao: dadosOrigens[o]?.descricao }))}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, origem: nome }, escolhas_origem: [] }, true)}
            />
            <SelectionModal
                isOpen={modal === 'deus'}
                onClose={() => setModal(null)}
                title="Escolha sua Divindade"
                icon="⛪"
                selected={ficha.cabecalho.deus}
                items={[{ nome: '', descricao: 'Remover devoção' }, ...getDeusesPermitidos().map(d => ({ nome: d, descricao: dadosDeuses[d]?.descricao }))]}
                onSelect={nome => updateFicha({ cabecalho: { ...ficha.cabecalho, deus: nome } }, true)}
            />
        </div>
    );
}