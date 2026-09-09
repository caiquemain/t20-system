import { PONTOS_INICIAIS, MIN_ATTR, MAX_ATTR, TABELA_CUSTO, MAPA_ATTR_KEY } from '../../../utils/atributosRules';
import type { WizardStepProps } from '../../../types/wizard';

const MAPA_ATTR: Record<string, string> = {
    forca: 'Força', destreza: 'Destreza', constituicao: 'Constituição',
    inteligencia: 'Inteligência', sabedoria: 'Sabedoria', carisma: 'Carisma'
};

export function StepAtributos({ ficha, updateFicha, dadosRacas }: WizardStepProps) {
    const racaNome = ficha.cabecalho.raca;
    const infoRaca = dadosRacas?.[racaNome] || { attrs: {}, escolhas: 0 };
    const qtdEscolhas = infoRaca.escolhas || 0;
    const escolhasAtuais: string[] = ficha.escolhas_atributos_raciais || [];

    const pontosGastos = Object.values(ficha.atributos_base as Record<string, number>)
        .reduce((acc, v) => acc + (TABELA_CUSTO[String(v)] ?? 0), 0);
    const pontosRestantes = PONTOS_INICIAIS - pontosGastos;

    const changeBase = (key: string, delta: number) => {
        const atual = ficha.atributos_base[key] ?? 0;
        const novo = atual + delta;

        if (delta > 0) {
            if (atual >= MAX_ATTR) return;
            const custoDelta = (TABELA_CUSTO[String(novo)] ?? 0) - (TABELA_CUSTO[String(atual)] ?? 0);
            if (custoDelta > pontosRestantes) return;
        } else {
            if (atual <= MIN_ATTR) return;
        }

        updateFicha({
            atributos_base: { ...ficha.atributos_base, [key]: novo },
            atributos: { ...ficha.atributos, [key]: (ficha.atributos[key] ?? 0) + delta }
        });
    };

    const toggleEscolhaRacial = (key: string) => {
        const shortKey = MAPA_ATTR_KEY[key];
        const racialFixo = infoRaca.attrs?.[shortKey] || 0;
        if (racialFixo !== 0) return;

        let novasEscolhas: string[];
        let delta: number;
        if (escolhasAtuais.includes(key)) {
            novasEscolhas = escolhasAtuais.filter(k => k !== key);
            delta = -1;
        } else {
            if (escolhasAtuais.length >= qtdEscolhas) return;
            novasEscolhas = [...escolhasAtuais, key];
            delta = +1;
        }
        updateFicha({
            escolhas_atributos_raciais: novasEscolhas,
            atributos: { ...ficha.atributos, [key]: (ficha.atributos[key] ?? 0) + delta }
        }, true);
    };

    return (
        <div>
            <h2 style={{ color: '#ffd700', marginBottom: '20px' }}>💪 Passo 2: Atributos</h2>
            <p style={{ color: '#aaa', marginBottom: '20px' }}>
                Compre seus atributos com pontos (mín. {MIN_ATTR}, máx. +{MAX_ATTR}). Bônus raciais são gratuitos.
            </p>

            <div style={{
                display: 'inline-flex', alignItems: 'center', gap: 12,
                background: pontosRestantes < 0 ? 'rgba(211,47,47,0.15)' : '#1a1a1a',
                border: `1px solid ${pontosRestantes < 0 ? '#d32f2f' : '#444'}`,
                borderRadius: 8, padding: '10px 20px', marginBottom: 24
            }}>
                <span style={{ color: '#888' }}>Pontos de Atributo:</span>
                <span style={{ color: pontosRestantes < 0 ? '#ff5252' : '#4caf50', fontSize: '1.3rem', fontWeight: 'bold' }}>
                    {pontosRestantes} / {PONTOS_INICIAIS}
                </span>
            </div>

            {qtdEscolhas > 0 && racaNome && (
                <div style={{
                    background: 'rgba(255,215,0,0.08)', border: '1px solid #5a4a1a',
                    borderRadius: 8, padding: '10px 16px', marginBottom: 24, color: '#ffd700', fontSize: '0.9rem'
                }}>
                    🧬 {racaNome} permite <strong>{qtdEscolhas} escolha(s) de +1</strong> em atributos sem bônus fixo.
                    Clique no botão "🧬" dos cards abaixo. ({escolhasAtuais.length}/{qtdEscolhas} usadas)
                </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 16 }}>
                {Object.entries(MAPA_ATTR).map(([key, label]) => {
                    const base = ficha.atributos_base[key] ?? 0;
                    const total = ficha.atributos[key] ?? 0;
                    const shortKey = MAPA_ATTR_KEY[key];
                    const racialFixo = infoRaca.attrs?.[shortKey] || 0;
                    const isEscolhido = escolhasAtuais.includes(key);
                    const racialTotal = racialFixo + (isEscolhido ? 1 : 0);
                    const outros = total - base - racialTotal;
                    const podeEscolher = qtdEscolhas > 0 && racialFixo === 0;
                    const escolhasCheias = escolhasAtuais.length >= qtdEscolhas;

                    const custoProx = (TABELA_CUSTO[String(base + 1)] ?? 0) - (TABELA_CUSTO[String(base)] ?? 0);
                    const podeAumentar = base < MAX_ATTR && custoProx <= pontosRestantes;
                    const podeDiminuir = base > MIN_ATTR;

                    return (
                        <div key={key} style={{ background: '#1a1a1a', border: '1px solid #444', borderRadius: 10, padding: 18 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                                <strong style={{ color: '#fff' }}>{label}</strong>
                                <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: total > 0 ? '#ffd700' : total < 0 ? '#ff5252' : '#ccc' }}>
                                    {total > 0 ? `+${total}` : total}
                                </span>
                            </div>

                            <div style={{ fontSize: '0.75rem', color: '#888', marginBottom: 12, minHeight: 16 }}>
                                Base {base}
                                {racialFixo !== 0 && <span style={{ color: '#4caf50' }}> • Raça {racialFixo > 0 ? `+${racialFixo}` : racialFixo}</span>}
                                {isEscolhido && <span style={{ color: '#4caf50' }}> • Escolha +1</span>}
                                {outros !== 0 && <span style={{ color: '#2196f3' }}> • Outros {outros > 0 ? `+${outros}` : outros}</span>}
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <button
                                    onClick={() => changeBase(key, -1)}
                                    disabled={!podeDiminuir}
                                    style={{ width: 38, height: 38, background: podeDiminuir ? '#444' : '#2a2a2a', color: podeDiminuir ? '#fff' : '#555', border: 'none', borderRadius: 6, fontSize: '1.1rem', cursor: podeDiminuir ? 'pointer' : 'not-allowed' }}
                                >−</button>
                                <span style={{ flex: 1, textAlign: 'center', color: '#ccc' }}>Base: {base}</span>
                                <button
                                    onClick={() => changeBase(key, +1)}
                                    disabled={!podeAumentar}
                                    style={{ width: 38, height: 38, background: podeAumentar ? '#444' : '#2a2a2a', color: podeAumentar ? '#fff' : '#555', border: 'none', borderRadius: 6, fontSize: '1.1rem', cursor: podeAumentar ? 'pointer' : 'not-allowed' }}
                                >+</button>
                            </div>

                            {podeEscolher && (
                                <button
                                    onClick={() => toggleEscolhaRacial(key)}
                                    disabled={!isEscolhido && escolhasCheias}
                                    style={{
                                        marginTop: 10, width: '100%', padding: '6px 0',
                                        background: isEscolhido ? 'rgba(76,175,80,0.2)' : 'transparent',
                                        border: `1px solid ${isEscolhido ? '#4caf50' : '#555'}`,
                                        color: isEscolhido ? '#4caf50' : '#888',
                                        borderRadius: 6, cursor: (!isEscolhido && escolhasCheias) ? 'not-allowed' : 'pointer',
                                        fontSize: '0.8rem'
                                    }}
                                >
                                    {isEscolhido ? '✓ +1 racial escolhido' : '🧬 Escolher +1 racial'}
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}