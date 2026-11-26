import { useMemo, useState } from 'react';
import type { WizardStepProps } from '../../../types/wizard';
import { DADOS_PERICIAS_FRONTEND as DADOS_PERICIAS } from '../../../data/pericias';
import { T20Icon } from '../../T20Icon';

const FONT_BODY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

export function StepPericias({ ficha, updateFicha, dadosClasses }: WizardStepProps) {
    const [busca, setBusca] = useState('');
    const [apenasClasse, setApenasClasse] = useState(false);

    const classeNome = ficha.classes[0]?.nome || '';
    const dadosClasse = dadosClasses[classeNome] || {};
    const periciasFixas: string[] = dadosClasse.pericias_fixas || [];
    const periciasClasseLista: string[] = dadosClasse.pericias_escolha || dadosClasse.pericias_lista || [];
    const qtdClasse = Number(dadosClasse.pericias_qtd || dadosClasse.qtd_pericias || 0);
    const bonusInt = Math.max(0, Number(ficha.atributos?.inteligencia || 0));
    const totalEscolhasSugeridas = qtdClasse + bonusInt;

    const todasPericias = useMemo(() => {
        const chaves = Object.keys(DADOS_PERICIAS);
        return chaves.filter(nome => {
            if (busca.trim() && !nome.toLowerCase().includes(busca.trim().toLowerCase())) return false;
            if (apenasClasse && periciasClasseLista.length > 0 && !periciasClasseLista.includes(nome) && !periciasFixas.includes(nome)) {
                return false;
            }
            return true;
        });
    }, [busca, apenasClasse, periciasClasseLista, periciasFixas]);

    const treinadasAtuais = useMemo(
        () => Object.entries(ficha.pericias || {}).filter(([, p]) => (p?.treino || 0) > 0).map(([k]) => k),
        [ficha.pericias]
    );
    const escolhidasCount = treinadasAtuais.filter(k => !periciasFixas.includes(k)).length;

    const handleTogglePericia = (nome: string) => {
        if (periciasFixas.includes(nome)) return;
        const atual = ficha.pericias?.[nome];
        const novoTreino = (atual?.treino || 0) > 0 ? 0 : 2;
        const novasPericias = {
            ...(ficha.pericias || {}),
            [nome]: {
                ...(atual || { atributo_usado: DADOS_PERICIAS[nome]?.atributo || 'int', outros: 0, total: 0 }),
                treino: novoTreino,
            },
        };
        updateFicha({ pericias: novasPericias }, true);
    };

    return (
        <div style={{ fontFamily: FONT_BODY, textTransform: 'none' }}>
            <h2 style={{ color: '#ffd700', marginBottom: 10, fontFamily: 'Tormenta, serif', display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                <T20Icon name="arco" size={22} /> Passo 4: Perícias
            </h2>
            <p style={{ color: '#94a3b8', marginBottom: 20, fontSize: '0.92rem' }}>
                Selecione as perícias treinadas do seu personagem. Perícias fixas de <strong>{classeNome || 'sua classe'}</strong> já vêm treinadas automaticamente.
            </p>

            {/* Resumo do orçamento de perícias */}
            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 18 }}>
                <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Fixas da Classe</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#81c784' }}>
                        {periciasFixas.length > 0 ? periciasFixas.join(', ') : 'Nenhuma fixa'}
                    </div>
                </div>
                <div style={{ background: '#1a1d2e', border: '1px solid #32385a', borderRadius: 8, padding: '10px 14px' }}>
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Escolhas Treinadas</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, color: escolhidasCount > totalEscolhasSugeridas ? '#ffb74d' : '#ffd700' }}>
                        {escolhidasCount} / {totalEscolhasSugeridas}{' '}
                        <span style={{ fontSize: '0.76rem', color: '#94a3b8', fontWeight: 400 }}>
                            ({qtdClasse} classe + {bonusInt} INT)
                        </span>
                    </div>
                </div>
            </div>

            {/* Filtros */}
            <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16, flexWrap: 'wrap' }}>
                <input
                    type="text"
                    placeholder="Filtrar perícia..."
                    value={busca}
                    onChange={e => setBusca(e.target.value)}
                    style={{ padding: '9px 12px', background: '#1a1a1a', border: '1px solid #444', borderRadius: 6, color: '#fff', minWidth: 220 }}
                />
                {periciasClasseLista.length > 0 && (
                    <label style={{ display: 'inline-flex', alignItems: 'center', gap: 6, color: '#cbd5e1', fontSize: '0.86rem', cursor: 'pointer' }}>
                        <input
                            type="checkbox"
                            checked={apenasClasse}
                            onChange={e => setApenasClasse(e.target.checked)}
                        />
                        Mostrar apenas lista da classe ({classeNome})
                    </label>
                )}
            </div>

            {/* Grade de Perícias */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))', gap: 10 }}>
                {todasPericias.map(nome => {
                    const meta = DADOS_PERICIAS[nome];
                    const info = ficha.pericias?.[nome];
                    const fixa = periciasFixas.includes(nome);
                    const treinada = fixa || (info?.treino || 0) > 0;
                    const daClasse = periciasClasseLista.includes(nome);
                    const total = info?.total ?? 0;

                    return (
                        <button
                            key={nome}
                            type="button"
                            onClick={() => handleTogglePericia(nome)}
                            style={{
                                textAlign: 'left',
                                padding: '10px 12px',
                                borderRadius: 8,
                                border: fixa
                                    ? '1px solid #4caf50'
                                    : treinada
                                        ? '2px solid #ffd700'
                                        : '1px solid #3a3a4a',
                                background: fixa
                                    ? 'rgba(76, 175, 80, 0.14)'
                                    : treinada
                                        ? 'rgba(255, 215, 0, 0.12)'
                                        : '#1b1d28',
                                cursor: fixa ? 'default' : 'pointer',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                gap: 8,
                            }}
                        >
                            <div>
                                <div style={{ color: treinada ? '#fff' : '#cbd5e1', fontWeight: 600, fontSize: '0.92rem' }}>
                                    {nome}
                                </div>
                                <div style={{ display: 'flex', gap: 5, marginTop: 3, flexWrap: 'wrap' }}>
                                    <span style={{ fontSize: '0.68rem', color: '#94a3b8', textTransform: 'uppercase' }}>
                                        {meta?.atributo || 'int'}
                                    </span>
                                    {fixa && <span style={{ fontSize: '0.66rem', color: '#81c784' }}>• Fixa</span>}
                                    {!fixa && daClasse && <span style={{ fontSize: '0.66rem', color: '#7dd3fc' }}>• Classe</span>}
                                    {meta?.treino_apenas && <span style={{ fontSize: '0.66rem', color: '#f59e0b' }}>• Trein.</span>}
                                    {meta?.penalidade_armadura && <span style={{ fontSize: '0.66rem', color: '#f87171' }}>• PA</span>}
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                <span style={{ fontWeight: 700, color: treinada ? '#ffd700' : '#94a3b8', fontSize: '0.95rem' }}>
                                    {total >= 0 ? `+${total}` : total}
                                </span>
                                {treinada && <T20Icon name="check" size={14} color={fixa ? '#81c784' : '#ffd700'} />}
                            </div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}