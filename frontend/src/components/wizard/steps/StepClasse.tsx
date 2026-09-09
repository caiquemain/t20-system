import { useState } from 'react';
import { SelectionModal } from '../SelectionModal';
import type { WizardStepProps } from '../../../types/wizard';

export function StepClasse({ ficha, updateFicha, listaClasses, dadosClasses }: WizardStepProps) {
    const [modalAberto, setModalAberto] = useState(false);
    const classeNome = ficha.classes[0]?.nome || '';
    const nivel = ficha.classes[0]?.nivel || 1;
    const dados = dadosClasses[classeNome];

    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px' }}>⚔️ Passo 3: Classe</h2>
            <p style={{ color: '#aaa', marginBottom: '30px' }}>
                Escolha sua classe e o nível inicial do personagem.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 700 }}>
                <div
                    onClick={() => setModalAberto(true)}
                    style={{ background: '#1a1a1a', border: '1px solid #444', borderRadius: 10, padding: '16px 20px', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                >
                    <div>
                        <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: 4 }}>CLASSE</div>
                        <div style={{ fontSize: '1.1rem', color: '#fff' }}>{classeNome || 'Escolher classe...'}</div>
                    </div>
                    <span style={{ color: '#ffd700', fontSize: '1.2rem' }}>▸</span>
                </div>

                <div style={{ maxWidth: 200 }}>
                    <label style={{ display: 'block', marginBottom: 8, color: '#ccc' }}>Nível Inicial</label>
                    <input
                        type="number" min={1} max={20} value={nivel}
                        onChange={e => {
                            const nc = [...ficha.classes];
                            nc[0] = { ...nc[0], nivel: parseInt(e.target.value) || 1 };
                            updateFicha({ classes: nc }, true);
                        }}
                        style={{ width: '100%', padding: 12, background: '#1a1a1a', border: '1px solid #555', borderRadius: 8, color: '#fff', fontSize: '1rem' }}
                    />
                </div>
            </div>

            {dados && (
                <div style={{ marginTop: 30, background: '#1a1a1a', border: '1px solid #333', borderRadius: 10, padding: 20, maxWidth: 700 }}>
                    <h3 style={{ color: '#ffd700', marginTop: 0 }}>{classeNome}</h3>
                    {dados.descricao && <p style={{ color: '#bbb', fontSize: '0.9rem', lineHeight: 1.5 }}>{dados.descricao}</p>}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 12, marginTop: 16 }}>
                        <div style={{ background: '#252525', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                            <div style={{ color: '#888', fontSize: '0.75rem' }}>PV INICIAL</div>
                            <div style={{ color: '#4caf50', fontSize: '1.3rem', fontWeight: 'bold' }}>{dados.pv_inicial}</div>
                        </div>
                        <div style={{ background: '#252525', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                            <div style={{ color: '#888', fontSize: '0.75rem' }}>PV / NÍVEL</div>
                            <div style={{ color: '#4caf50', fontSize: '1.3rem', fontWeight: 'bold' }}>+{dados.pv_nivel}</div>
                        </div>
                        <div style={{ background: '#252525', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                            <div style={{ color: '#888', fontSize: '0.75rem' }}>PM INICIAL</div>
                            <div style={{ color: '#2196f3', fontSize: '1.3rem', fontWeight: 'bold' }}>{dados.pm_inicial}</div>
                        </div>
                        <div style={{ background: '#252525', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                            <div style={{ color: '#888', fontSize: '0.75rem' }}>PM / NÍVEL</div>
                            <div style={{ color: '#2196f3', fontSize: '1.3rem', fontWeight: 'bold' }}>+{dados.pm_nivel}</div>
                        </div>
                        <div style={{ background: '#252525', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                            <div style={{ color: '#888', fontSize: '0.75rem' }}>ATRIBUTO PM</div>
                            <div style={{ color: '#ffd700', fontSize: '1.3rem', fontWeight: 'bold', textTransform: 'uppercase' }}>{dados.pm_atributo}</div>
                        </div>
                    </div>
                </div>
            )}

            <SelectionModal
                isOpen={modalAberto}
                onClose={() => setModalAberto(false)}
                title="Escolha sua Classe"
                icon="⚔️"
                selected={classeNome}
                items={listaClasses.map(c => ({
                    nome: c,
                    descricao: dadosClasses[c]?.descricao,
                    tags: [`PV ${dadosClasses[c]?.pv_inicial}`, `PM ${dadosClasses[c]?.pm_inicial}`]
                }))}
                onSelect={nome => {
                    const nc = [...ficha.classes];
                    nc[0] = { ...nc[0], nome: nome, subclasse: undefined };
                    updateFicha({ classes: nc, pericias: {} }, true);
                }}
            />
        </div>
    );
}