import React from 'react';
import type { Personagem } from '../types';
import '../Ficha.css';

interface StatusBarsProps {
    ficha: Personagem;
    onUpdate?: (data: Partial<Personagem>) => void;
    overrideDeslocamento?: number;
    isFlying?: boolean;
    isAquatic?: boolean;
}

export const StatusBars: React.FC<StatusBarsProps> = ({
    ficha,
    onUpdate,
    overrideDeslocamento,
    isFlying,
    isAquatic
}) => {
    const { pv, pm, defesa, deslocamento, detalhes_deslocamento, rd } = ficha.status;
    const detalhesDefesa = defesa.detalhes;

    // --- LÓGICA DE ÍCONES E TEXTOS (DINÂMICO) ---
    // Prioridade: Voo > Natação > Normal
    let iconeDeslocamento = '🦵';
    let labelDeslocamento = 'Deslocamento';

    if (isFlying) {
        iconeDeslocamento = '🪽';
        labelDeslocamento = 'Voo Ativo';
    } else if (isAquatic) {
        iconeDeslocamento = '🧜‍♀️';
        labelDeslocamento = 'Natação';
    }

    // Se tiver override (Voo ou Natação vindo da Ficha), usa ele. Senão, usa o da ficha.
    const valorDeslocamento = overrideDeslocamento || deslocamento;

    // Cálculos de Porcentagem das Barras
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));

    // Helpers para compatibilidade
    const calcPV = pv.calculo || pv.detalhes_pv;
    const calcPM = pm.calculo || pm.detalhes_pm;

    // --- DETECTAR GOLEM E ELEMENTO ---
    // CORREÇÃO: Aceita ambos os nomes possíveis da habilidade
    const habGolem = ficha.habilidades.find(h => h.nome === "Espírito Elemental" || h.nome === "Fonte Elemental");

    // @ts-ignore (Ignora erro de tipagem se não tiver atualizado types.ts)
    const elementoGolem = habGolem?.escolhas_aplicadas?.["elemento_escolha"];

    // --- FUNÇÃO DE DESCANSO ---
    const handleDescansar = () => {
        if (onUpdate) {
            if (window.confirm("Deseja realizar um Descanso Completo? Isso recuperará todo seu PV e PM.")) {
                onUpdate({
                    status: {
                        ...ficha.status,
                        pv: { ...pv, atual: pv.maximo },
                        pm: { ...pm, atual: pm.maximo }
                    }
                });
            }
        }
    };

    return (
        <div className="section-card" style={{ marginTop: '25px' }}>

            {/* CABEÇALHO COM BOTÃO DE DESCANSAR */}
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                <h3 className="section-title" style={{ margin: 0 }}>Status Vitais</h3>

                {onUpdate && (
                    <button
                        onClick={handleDescansar}
                        style={{
                            background: 'transparent',
                            border: '1px solid #4caf50',
                            color: '#4caf50',
                            borderRadius: '4px',
                            padding: '4px 10px',
                            fontSize: '0.75rem',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '5px',
                            transition: 'all 0.2s'
                        }}
                        onMouseOver={(e) => e.currentTarget.style.background = 'rgba(76, 175, 80, 0.1)'}
                        onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
                        title="Recuperar PV e PM totalmente"
                    >
                        💤 Descansar
                    </button>
                )}
            </div>

            {/* --- BARRA DE VIDA (PV) --- */}
            <div className="bar-container tooltip-container">
                <div className="bar-header">
                    <span>PV</span>
                    <span>{pv.atual}/{pv.maximo}</span>
                </div>
                <div className="bar-track">
                    <div className="bar-fill pv-fill" style={{ width: `${pvPerc}%` }}></div>
                </div>

                {/* Tooltip PV */}
                {calcPV && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Inicial:</span> <span>{calcPV.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{calcPV.nivel}</span></div>
                        <div className="tooltip-row"><span>Con:</span> <span>{calcPV.con}</span></div>
                        {calcPV.habilidades !== 0 && <div className="tooltip-row"><span>Habilidades:</span> <span>{calcPV.habilidades}</span></div>}
                        {calcPV.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{calcPV.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{pv.maximo}</span></div>
                    </div>
                )}
            </div>

            {/* --- BARRA DE MANA (PM) --- */}
            <div className="bar-container tooltip-container">
                <div className="bar-header">
                    <span>PM</span>
                    <span>{pm.atual}/{pm.maximo}</span>
                </div>
                <div className="bar-track">
                    <div className="bar-fill pm-fill" style={{ width: `${pmPerc}%` }}></div>
                </div>

                {/* Tooltip PM */}
                {calcPM && (
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Inicial:</span> <span>{calcPM.inicial}</span></div>
                        <div className="tooltip-row"><span>Por Nível:</span> <span>{calcPM.nivel}</span></div>
                        <div className="tooltip-row"><span>Atributo:</span> <span>{calcPM.atributo}</span></div>
                        {calcPM.habilidades !== 0 && <div className="tooltip-row"><span>Habilidades:</span> <span>{calcPM.habilidades}</span></div>}
                        {calcPM.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{calcPM.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{pm.maximo}</span></div>
                    </div>
                )}
            </div>

            {/* --- STATUS SECUNDÁRIOS --- */}
            <div className="stats-row-container">
                {/* DEFESA */}
                <div className="stat-box tooltip-container">
                    <span className="stat-value">🛡️ {defesa.total}</span>
                    <span className="stat-label">Defesa</span>
                    <div className="attr-tooltip">
                        <div className="tooltip-row"><span>Base:</span> <span>10</span></div>
                        <div className="tooltip-row"><span>Des/Atributo:</span> <span>{detalhesDefesa.des_mod}</span></div>
                        {detalhesDefesa.armadura > 0 && <div className="tooltip-row"><span>Armadura:</span> <span>{detalhesDefesa.armadura}</span></div>}
                        {detalhesDefesa.escudo > 0 && <div className="tooltip-row"><span>Escudo:</span> <span>{detalhesDefesa.escudo}</span></div>}
                        {detalhesDefesa.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{detalhesDefesa.outros}</span></div>}
                        <div className="tooltip-total"><span>Total:</span> <span>{defesa.total}</span></div>
                    </div>
                </div>

                {/* DESLOCAMENTO */}
                <div className="stat-box tooltip-container">
                    <span className="stat-value" style={{
                        color: (isFlying || isAquatic) ? '#42a5f5' : 'inherit',
                        transition: 'color 0.3s'
                    }}>
                        {iconeDeslocamento} {valorDeslocamento}m
                    </span>
                    <span className="stat-label">{labelDeslocamento}</span>

                    {detalhes_deslocamento && (
                        <div className="attr-tooltip">
                            <div className="tooltip-row"><span>Base:</span> <span>{detalhes_deslocamento.base}m</span></div>

                            {/* Linhas Condicionais no Tooltip */}
                            {isFlying && <div className="tooltip-row" style={{ color: '#42a5f5' }}><span>Voo:</span> <span>12m</span></div>}
                            {isAquatic && !isFlying && <div className="tooltip-row" style={{ color: '#42a5f5' }}><span>Natação:</span> <span>12m</span></div>}

                            {detalhes_deslocamento.armadura !== 0 && <div className="tooltip-row"><span>Armadura:</span> <span>{detalhes_deslocamento.armadura}m</span></div>}
                            {detalhes_deslocamento.outros !== 0 && <div className="tooltip-row"><span>Outros:</span> <span>{detalhes_deslocamento.outros}m</span></div>}
                            <div className="tooltip-total"><span>Total:</span> <span>{valorDeslocamento}m</span></div>
                        </div>
                    )}
                </div>
            </div>

            {/* --- REDUÇÃO DE DANO (RD) & IMUNIDADES --- */}
            {(rd && rd.length > 0 || elementoGolem) && (
                <div className="rd-section" style={{ marginTop: '15px', paddingTop: '10px', borderTop: '1px solid #333' }}>
                    <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px', display: 'block', marginBottom: '8px' }}>
                        Resistências / Imunidades
                    </span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>

                        {/* Tag Especial do Golem */}
                        {elementoGolem && (() => {
                            // Cores para a tag de status
                            const cores: Record<string, string> = {
                                "Ácido": "#8bc34a",
                                "Eletricidade": "#ffee58",
                                "Fogo": "#ff5252",
                                "Frio": "#4fc3f7"
                            };
                            const cor = cores[elementoGolem] || "#a5d6a7";

                            return (
                                <span title={`Dano de ${elementoGolem} cura metade do dano causado.`} style={{
                                    background: `${cor}33`, // 20% opacidade
                                    color: cor,
                                    border: `1px solid ${cor}`,
                                    padding: '3px 10px',
                                    borderRadius: '4px',
                                    fontSize: '0.8rem',
                                    fontWeight: 'bold',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '5px'
                                }}>
                                    🔋 Absorve: {elementoGolem}
                                </span>
                            );
                        })()}

                        {/* RDs Padrão */}
                        {rd.map((item: string, idx: number) => (
                            <span key={idx} style={{
                                background: '#3e2723',
                                color: '#ffccbc',
                                border: '1px solid #5d4037',
                                padding: '3px 10px',
                                borderRadius: '4px',
                                fontSize: '0.8rem',
                                fontWeight: 'bold',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '5px'
                            }}>
                                🛡️ {item}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};