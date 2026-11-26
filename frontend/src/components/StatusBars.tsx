import React, { useState } from 'react';
import type { Personagem } from '../types';
import { T20Icon, type IconName } from './T20Icon';
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
    const [showDescansoMenu, setShowDescansoMenu] = useState(false);
    const { pv, pm, defesa, deslocamento, rd, proficiencias, imunidades, sentidos, vulnerabilidades} = ficha.status;
    const statusAny = ficha.status as any;

    let iconeDeslocamento: IconName = 'deslocamento';
    let labelDeslocamento = 'Deslocamento';
    if (isFlying) { iconeDeslocamento = 'voo'; labelDeslocamento = 'Voo Ativo'; }
    else if (isAquatic) { iconeDeslocamento = 'natacao'; labelDeslocamento = 'Natação'; }

    const deslocamentoNatacao = (ficha.status as any).deslocamento_natacao;
    const valorDeslocamento = overrideDeslocamento !== undefined 
        ? overrideDeslocamento 
        : (isAquatic && deslocamentoNatacao ? deslocamentoNatacao : deslocamento);
    const pvPerc = Math.min(100, Math.max(0, (pv.atual / (pv.maximo || 1)) * 100));
    const pmPerc = Math.min(100, Math.max(0, (pm.atual / (pm.maximo || 1)) * 100));

    const habGolem = ficha.habilidades.find(h => h.nome === "Espírito Elemental" || h.nome === "Fonte Elemental");
    // @ts-ignore
    const elementoGolem = habGolem?.escolhas_aplicadas?.["elemento_escolha"];

    const nivel = Math.max(1, ficha.cabecalho.nivel_total || 1);
    const descansoCalc = ficha.status.descanso_calc || {
        ruim: Math.max(1, Math.floor(nivel / 2)),
        normal: nivel,
        confortavel: nivel * 2,
        luxuosa: nivel * 3,
        bonus_categoria: 0,
        minimo_nivel: false,
    };

    const aplicarDescanso = (quantidade: number | 'completo') => {
        if (!onUpdate) return;
        const novoPv = quantidade === 'completo' ? pv.maximo : Math.min(pv.maximo, pv.atual + quantidade);
        const novoPm = quantidade === 'completo' ? pm.maximo : Math.min(pm.maximo, pm.atual + quantidade);
        onUpdate({
            status: {
                ...ficha.status,
                pv: { ...pv, atual: novoPv, temporario: 0 },
                pm: { ...pm, atual: novoPm, temporario: 0 },
            }
        });
        setShowDescansoMenu(false);
    };

    const getIconeResistencia = (texto: string): IconName => {
        const t = texto.toLowerCase();
        if (t.includes('fogo')) return 'fogo';
        if (t.includes('frio') || t.includes('gelo')) return 'gelo';
        if (t.includes('eletricidade') || t.includes('elétrico')) return 'raio';
        if (t.includes('ácido')) return 'acido';
        if (t.includes('veneno')) return 'veneno';
        if (t.includes('luz')) return 'luz';
        if (t.includes('trevas') || t.includes('sombra')) return 'trevas';
        if (t.includes('mental') || t.includes('psíquico')) return 'magia';
        if (t.includes('corte') || t.includes('perfura') || t.includes('impacto')) return 'espada';
        if (t.includes('magia')) return 'efeito';
        return 'defesa';
    };

    // TOOLTIP GENÉRICO DA PILHA DE MODIFICADORES (funciona p/ PV, PM, Defesa e Deslocamento)
    const renderTooltipPilha = (calc: any, total: number | string, unidade = '') => {
        if (!calc) return null;
        const fontes: any[] = calc.fontes || [];
        if (fontes.length === 0 && !calc.base) return null;
        return (
            <div className="status-custom-tooltip">
                {calc.base !== 0 && (
                    <div className="tooltip-row"><span>Base</span><span>{calc.base}{unidade}</span></div>
                )}
                {fontes.map((f: any, i: number) => (
                    <div key={i} className="tooltip-row">
                        <span>{f.fonte}</span>
                        <span>{f.valor >= 0 ? `+${f.valor}` : f.valor}{unidade}</span>
                    </div>
                ))}
                <div className="tooltip-total"><span>Total</span><span>{total}{unidade}</span></div>
            </div>
        );
    };

    return (
        <div className="section-card" style={{ marginTop: '25px', position: 'relative' }}>
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', position: 'relative' }}>
                <h3 className="section-title" style={{ margin: 0 }}>Status Vitais</h3>
                {onUpdate && (
                    <div style={{ position: 'relative' }}>
                        <button
                            onClick={() => setShowDescansoMenu(prev => !prev)}
                            className="btn-descansar"
                            title="Recuperar PV e PM por condição de descanso (T20 p.106)"
                        >
                            <T20Icon name="descanso" size={14} /> Descansar ▾
                        </button>
                        {showDescansoMenu && (
                            <div style={{
                                position: 'absolute', right: 0, top: '110%', zIndex: 50,
                                background: '#1a1a2e', border: '1px solid #3a3a5a', borderRadius: 8,
                                padding: 8, minWidth: 215, boxShadow: '0 8px 24px rgba(0,0,0,0.7)',
                                display: 'flex', flexDirection: 'column', gap: 4
                            }}>
                                <div style={{ fontSize: '0.72rem', color: '#999', padding: '2px 6px' }}>
                                    Condição de Descanso (zera PV/PM temp.)
                                </div>
                                {[
                                    { label: 'Ruim', val: descansoCalc.ruim, desc: 'Ao relento' },
                                    { label: 'Normal', val: descansoCalc.normal, desc: 'Estalagem comum' },
                                    { label: 'Confortável', val: descansoCalc.confortavel, desc: '2× nível' },
                                    { label: 'Luxuosa', val: descansoCalc.luxuosa, desc: '3× nível' },
                                ].map(opt => (
                                    <button
                                        key={opt.label}
                                        onClick={() => aplicarDescanso(opt.val)}
                                        style={{
                                            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                            background: 'rgba(255,255,255,0.04)', border: '1px solid #333',
                                            color: '#eee', borderRadius: 6, padding: '6px 8px', cursor: 'pointer', fontSize: '0.8rem'
                                        }}
                                        title={opt.desc}
                                    >
                                        <span>{opt.label}</span>
                                        <span style={{ color: '#8bc34a', fontWeight: 'bold' }}>+{opt.val} PV/PM</span>
                                    </button>
                                ))}
                                <button
                                    onClick={() => aplicarDescanso('completo')}
                                    style={{
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                        background: 'rgba(76,175,80,0.15)', border: '1px solid #4caf50',
                                        color: '#a5d6a7', borderRadius: 6, padding: '6px 8px', cursor: 'pointer', fontSize: '0.8rem', marginTop: 2
                                    }}
                                >
                                    <span>Completo (100%)</span>
                                    <span>Máx</span>
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* PV */}
            <div className="bar-container tooltip-anchor">
                <div className="bar-header">
                    <span>PV</span>
                    <span>
                        {pv.atual}/{pv.maximo}
                        {(pv.temporario || 0) > 0 && <span style={{ color: '#4fc3f7', marginLeft: 4 }}>(+{pv.temporario})</span>}
                    </span>
                </div>
                <div className="bar-track"><div className="bar-fill pv-fill" style={{ width: `${pvPerc}%` }}></div></div>
                {renderTooltipPilha(statusAny.pv_calc, pv.maximo)}
            </div>

            {/* PM */}
            <div className="bar-container tooltip-anchor">
                <div className="bar-header">
                    <span>PM</span>
                    <span>
                        {pm.atual}/{pm.maximo}
                        {(pm.temporario || 0) > 0 && <span style={{ color: '#ce93d8', marginLeft: 4 }}>(+{pm.temporario})</span>}
                    </span>
                </div>
                <div className="bar-track"><div className="bar-fill pm-fill" style={{ width: `${pmPerc}%` }}></div></div>
                {renderTooltipPilha(statusAny.pm_calc, pm.maximo)}
            </div>

            {/* DEFESA + DESLOCAMENTO */}
            <div className="stats-row-container">
                <div className="stat-box tooltip-anchor">
                    <span className="stat-value" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <T20Icon name="defesa" size={18} color="#90caf9" /> {defesa.total}
                    </span>
                    <span className="stat-label">Defesa</span>
                    {renderTooltipPilha(statusAny.defesa_calc, defesa.total)}
                </div>
                <div className="stat-box tooltip-anchor">
                    <span className="stat-value" style={{ color: (isFlying || isAquatic) ? '#42a5f5' : 'inherit', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <T20Icon name={iconeDeslocamento} size={18} /> {valorDeslocamento}m
                    </span>
                    <span className="stat-label">{labelDeslocamento}</span>
                    {renderTooltipPilha(statusAny.deslocamento_calc, valorDeslocamento, 'm')}
                </div>
            </div>

            {/* PROFICIÊNCIAS */}
            {proficiencias && proficiencias.length > 0 && (
                <div className="rd-section" style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #333' }}>
                    <span className="status-section-label">Proficiências</span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {proficiencias.map((item: string, idx: number) => (
                            <span key={idx} className="prof-tag">{item}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* RD, IMUNIDADES & SENTIDOS */}
            {((rd && rd.length > 0) || elementoGolem || (imunidades && imunidades.length > 0) || (sentidos && sentidos.length > 0) || (vulnerabilidades && vulnerabilidades.length > 0)) && (
                <div className="rd-section" style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #333' }}>
                    <span className="status-section-label">Resistências & Sentidos</span>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                        {elementoGolem && (
                            <span className="rd-tag" style={{ background: '#1b5e20', color: '#a5d6a7', borderColor: '#2e7d32' }}>
                                <T20Icon name="energia" size={13} /> Absorve: {elementoGolem}
                            </span>
                        )}
                        {rd?.map((item: string, idx: number) => (
                            <span key={`rd-${idx}`} className="rd-tag">
                                <T20Icon name={getIconeResistencia(item)} size={13} />
                                {item}
                            </span>
                        ))}
                        {imunidades?.map((item: string, idx: number) => (
                            <span key={`imun-${idx}`} className="rd-tag" style={{ background: '#4a148c', color: '#e1bee7', borderColor: '#7b1fa2' }}>
                                <T20Icon name="imunidade" size={13} /> {item}
                            </span>
                        ))}
                        {sentidos?.map((item: string, idx: number) => (
                            <span key={`sens-${idx}`} className="rd-tag" style={{ background: '#01579b', color: '#b3e5fc', borderColor: '#0277bd' }}>
                                <T20Icon name="visao" size={13} /> {item}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            <style>{`
                .btn-descansar {
                    background: transparent; border: 1px solid #4caf50; color: #4caf50;
                    border-radius: 4px; padding: 4px 10px; fontSize: 0.75rem; font-weight: bold;
                    cursor: pointer; display: flex; alignItems: center; gap: 5px; transition: all 0.2s;
                }
                .btn-descansar:hover { background: rgba(76, 175, 80, 0.1); }
                .status-section-label {
                    font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.5px;
                    display: block; margin-bottom: 5px; font-weight: bold;
                }
                .tooltip-anchor { position: relative; cursor: help; }
                .status-custom-tooltip {
                    visibility: hidden; opacity: 0; position: absolute; bottom: 100%; left: 50%;
                    transform: translateX(-50%) translateY(5px); width: 240px; background-color: #1a1a1a;
                    border: 1px solid #ffd700; border-radius: 6px; padding: 10px; z-index: 9999;
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9); transition: opacity 0.2s, transform 0.2s;
                    pointer-events: none;
                }
                .tooltip-anchor:hover .status-custom-tooltip {
                    visibility: visible; opacity: 1; transform: translateX(-50%) translateY(-10px);
                }
                .tooltip-row { display: flex; justify-content: space-between; font-size: 0.75rem; color: #ccc; margin-bottom: 3px; border-bottom: 1px dashed #333; }
                .tooltip-total { border-top: 1px solid #fca311; margin-top: 5px; padding-top: 2px; font-weight: bold; color: #fca311; display: flex; justify-content: space-between; }
                .rd-tag {
                    background: #3e2723; color: #ffccbc; border: 1px solid #5d4037;
                    padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;
                    display: flex; align-items: center; gap: 5px;
                }
                .prof-tag {
                    background: #263238; color: #cfd8dc; border: 1px solid #455a64;
                    padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;
                }
            `}</style>
        </div>
    );
};
