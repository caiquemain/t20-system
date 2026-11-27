import React, { useState } from 'react';
import { T20Icon } from './T20Icon';
import { PortalTooltip, type TooltipLinha } from './PortalTooltip';
import { rolarAtaqueD20, rolarExpressao, type ResultadoD20, type ResultadoExpressao } from '../utils/diceRoller';
import type { SpellRollConfig } from './SpellDetailsModal';

interface StatCalcView {
    base: number;
    total: number;
    fontes?: { fonte: string; valor: number }[];
}

interface AtaqueView {
    nome: string; bonus_ataque: string; dano: string; critico: string;
    tipo: string; alcance: string; teste: string; especial?: string;
    cd_fontes?: string[];
    dano_fontes?: string[];
}

interface AttackListProps {
    ataques: AtaqueView[];
    cdMagiasCalc?: StatCalcView;
    fluxoDeMana?: boolean;
    focoVital?: boolean;
    spellConfigs?: Record<string, SpellRollConfig>;
    onOpenSpell?: (nomeMagia: string) => void;
    onAplicarCura?: (valor: number, tipo: 'cura' | 'pv_temp', nomeMagia: string) => void;
}

interface RollAtaqueState {
    nome: string;
    ehMagia: boolean;
    modo: 'dano' | 'cura' | 'pv_temp';
    cdTexto?: string;
    custoPm?: number;
    ataque?: ResultadoD20;
    dano: ResultadoExpressao | null;
    tipoDano: string;
    aplicado?: boolean;
}

// Classificação visual dos efeitos (mesmo idioma de cores do sistema)
const ehPenalidade = (t: string) => /-\d/.test(t) || /não proficiente|penalidade|desbalanceada/i.test(t);
const ehBuff = (t: string) => /\+\d/.test(t) || /conta como/i.test(t);

export const AttackList: React.FC<AttackListProps> = ({ ataques, cdMagiasCalc, fluxoDeMana, focoVital, spellConfigs, onOpenSpell, onAplicarCura }) => {
    const [ultimoRoll, setUltimoRoll] = useState<RollAtaqueState | null>(null);

    const handleRolarAtaque = (a: AtaqueView) => {
        const ehCura = a.tipo === 'Cura' || a.bonus_ataque === 'Cura';
        const ehPvTemp = a.tipo === 'PV Temp' || a.bonus_ataque === 'PV Temp';
        const modo: 'dano' | 'cura' | 'pv_temp' = ehCura ? 'cura' : ehPvTemp ? 'pv_temp' : 'dano';
        const ehMagia = ehCura || ehPvTemp || /^CD\s+\d+|^Auto$/i.test((a.bonus_ataque || '').trim());
        const cfg = spellConfigs?.[a.nome];
        const danoFormula = (ehMagia && cfg?.formulaEfetiva) ? cfg.formulaEfetiva : a.dano;
        const danoRes = rolarExpressao(danoFormula);
        if (ehMagia) {
            setUltimoRoll({
                nome: a.nome,
                ehMagia: true,
                modo,
                cdTexto: ehCura
                    ? 'Cura de PV'
                    : ehPvTemp
                        ? 'PV Temporários'
                        : a.bonus_ataque === 'Auto'
                            ? 'Acerto Automático'
                            : `${a.teste} ${a.bonus_ataque}`,
                custoPm: cfg?.custoTotalPm,
                dano: danoRes,
                tipoDano: a.tipo,
                aplicado: false,
            });
        } else {
            setUltimoRoll({
                nome: a.nome,
                ehMagia: false,
                modo: 'dano',
                ataque: rolarAtaqueD20(a.bonus_ataque),
                dano: danoRes,
                tipoDano: a.tipo,
            });
        }
    };

    const montarLinhasCdOuAtaque = (a: AtaqueView, ehMagia: boolean): TooltipLinha[] => {
        if (ehMagia) {
            if ((a.bonus_ataque || '').trim().toLowerCase() === 'auto') {
                return [{ texto: 'Acerto automático (sem teste de resistência).', cor: '#ce93d8' }];
            }
            if (a.cd_fontes && a.cd_fontes.length > 0) {
                return a.cd_fontes.map((f, idx) => ({
                    texto: f,
                    cor: idx === a.cd_fontes!.length - 1 ? '#ffd700' : f.includes('-') ? '#ff8a80' : '#ce93d8',
                    negrito: idx === a.cd_fontes!.length - 1,
                    separador: idx === a.cd_fontes!.length - 1 && a.cd_fontes!.length > 1,
                }));
            }
            if (cdMagiasCalc) {
                const linhas: TooltipLinha[] = [{ texto: `Base: ${cdMagiasCalc.base}`, cor: '#ccc' }];
                for (const b of cdMagiasCalc.fontes || []) {
                    linhas.push({
                        texto: `${b.fonte}: ${b.valor >= 0 ? `+${b.valor}` : b.valor}`,
                        cor: b.valor < 0 ? '#ff8a80' : '#ce93d8',
                    });
                }
                linhas.push({ texto: `Total: ${a.bonus_ataque}`, cor: '#ffd700', negrito: true, separador: true });
                return linhas;
            }
            return [{ texto: `Teste de resistência: ${a.teste} (${a.bonus_ataque})`, cor: '#ce93d8' }];
        }

        // Arma / Ataque físico
        const linhas: TooltipLinha[] = [{ texto: `Perícia usada: ${a.teste || 'Luta'}`, cor: '#80deea' }];
        if (a.especial) {
            for (const parte of a.especial.split('; ')) {
                if (/ataque|não proficiente|avariado/i.test(parte)) {
                    linhas.push({
                        texto: parte,
                        cor: ehPenalidade(parte) ? '#ff8a80' : '#81c784',
                        negrito: true,
                    });
                }
            }
        }
        linhas.push({ texto: `Bônus exibido: ${a.bonus_ataque}`, cor: '#ffd700', negrito: true, separador: true });
        return linhas;
    };

    const montarLinhasDano = (a: AtaqueView, ehMagia: boolean, cfg?: SpellRollConfig): TooltipLinha[] => {
        const danoExibido = cfg?.formulaEfetiva || a.dano;
        const linhas: TooltipLinha[] = [];

        if (a.dano_fontes && a.dano_fontes.length > 0) {
            const semTotal = a.dano_fontes.filter(f => !f.startsWith('Total:'));
            for (const f of semTotal) {
                linhas.push({
                    texto: f,
                    cor: f.startsWith('Base') || f.startsWith('Dado base') ? '#ffcc80' : '#81c784',
                });
            }
        } else {
            linhas.push({
                texto: `${ehMagia ? 'Base da magia' : 'Dado base'} (${a.nome}): ${a.dano}`,
                cor: '#ffcc80',
            });
        }

        if (ehMagia && cfg && cfg.formulaEfetiva && cfg.formulaEfetiva !== a.dano) {
            linhas.push({
                texto: `Aprimoramentos aplicados (${cfg.custoTotalPm} PM): ${cfg.formulaEfetiva}`,
                cor: '#ce93d8',
                negrito: true,
            });
        }

        linhas.push({
            texto: `Total: ${danoExibido} (${a.tipo})`,
            cor: '#ffd700',
            negrito: true,
            separador: true,
        });
        return linhas;
    };

    return (
        <div className="section-card" style={{ marginTop: 25 }}>
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <h3 className="section-title" style={{ margin: 0, display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                    <T20Icon name="ataque" size={18} /> Ataques
                </h3>
                <div style={{ display: 'flex', gap: 6 }}>
                    {fluxoDeMana && (
                        <span style={{ fontSize: '0.7rem', color: '#80deea', background: 'rgba(0,188,212,0.1)', border: '1px solid rgba(0,188,212,0.4)', padding: '2px 8px', borderRadius: 4, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                            <T20Icon name="natacao" size={12} /> Fluxo de Mana
                        </span>
                    )}
                    {focoVital && (
                        <span style={{ fontSize: '0.7rem', color: '#ef9a9a', background: 'rgba(244,67,54,0.1)', border: '1px solid rgba(244,67,54,0.4)', padding: '2px 8px', borderRadius: 4, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                            <T20Icon name="hp" size={12} /> Foco Vital
                        </span>
                    )}
                </div>
            </div>

            {ultimoRoll && (
                <div style={{
                    background: '#16161e',
                    border: '1px solid #ffd70066',
                    borderRadius: 6,
                    padding: '8px 12px',
                    marginBottom: 12,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: 10,
                    fontSize: '0.85rem',
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                        <strong style={{ color: '#ffd54f' }}>{ultimoRoll.nome}</strong>
                        {ultimoRoll.ehMagia ? (
                            <span style={{ color: '#ce93d8', fontWeight: 'bold' }}>
                                {ultimoRoll.cdTexto}
                                {ultimoRoll.custoPm !== undefined ? ` • ${ultimoRoll.custoPm} PM` : ''}
                            </span>
                        ) : ultimoRoll.ataque && (
                            <span>
                                Ataque:{' '}
                                <strong style={{
                                    color: ultimoRoll.ataque.criticoNatural === 'sucesso'
                                        ? '#81c784'
                                        : ultimoRoll.ataque.criticoNatural === 'falha'
                                            ? '#ff5252'
                                            : '#fff',
                                }}>
                                    {ultimoRoll.ataque.total}
                                </strong>{' '}
                                <span style={{ color: '#888', fontSize: '0.75rem' }}>
                                    (d20[{ultimoRoll.ataque.d20}] {ultimoRoll.ataque.bonus >= 0 ? `+${ultimoRoll.ataque.bonus}` : ultimoRoll.ataque.bonus})
                                </span>
                            </span>
                        )}
                        {ultimoRoll.dano && (
                            <span>
                                {ultimoRoll.modo === 'cura'
                                    ? '💚 Cura: '
                                    : ultimoRoll.modo === 'pv_temp'
                                        ? '🛡️ PV Temporários: '
                                        : `Dano (${ultimoRoll.tipoDano}): `}
                                <strong style={{ color: ultimoRoll.modo === 'cura' ? '#81c784' : ultimoRoll.modo === 'pv_temp' ? '#64b5f6' : '#ffcc80' }}>
                                    {ultimoRoll.dano.total}
                                </strong>{' '}
                                <span style={{ color: '#888', fontSize: '0.75rem' }}>
                                    ({ultimoRoll.dano.detalhes.map(d => `${d.dado}[${d.rolagens.join(',')}]`).join(' + ')}
                                    {ultimoRoll.dano.bonus !== 0 ? (ultimoRoll.dano.bonus > 0 ? `+${ultimoRoll.dano.bonus}` : ultimoRoll.dano.bonus) : ''})
                                </span>
                            </span>
                        )}
                        {ultimoRoll.dano && (ultimoRoll.modo === 'cura' || ultimoRoll.modo === 'pv_temp') && onAplicarCura && (
                            <button
                                type="button"
                                disabled={ultimoRoll.aplicado}
                                onClick={() => {
                                    if (!ultimoRoll.dano) return;
                                    onAplicarCura(ultimoRoll.dano.total, ultimoRoll.modo as 'cura' | 'pv_temp', ultimoRoll.nome);
                                    setUltimoRoll(prev => prev ? { ...prev, aplicado: true } : null);
                                }}
                                style={{
                                    background: ultimoRoll.aplicado
                                        ? '#2a332a'
                                        : ultimoRoll.modo === 'cura'
                                            ? '#2e7d32'
                                            : '#1565c0',
                                    color: '#fff',
                                    border: 'none',
                                    borderRadius: 4,
                                    padding: '4px 10px',
                                    fontSize: '0.75rem',
                                    fontWeight: 'bold',
                                    cursor: ultimoRoll.aplicado ? 'default' : 'pointer',
                                }}
                            >
                                {ultimoRoll.aplicado
                                    ? '✓ Aplicado ao PV'
                                    : ultimoRoll.modo === 'cura'
                                        ? `+ Aplicar +${ultimoRoll.dano.total} PV`
                                        : `+ Aplicar ${ultimoRoll.dano.total} PV Temp`}
                            </button>
                        )}
                    </div>
                    <button
                        onClick={() => setUltimoRoll(null)}
                        style={{ background: 'transparent', border: 'none', color: '#888', cursor: 'pointer', fontSize: '1rem' }}
                        title="Fechar resultado"
                    >
                        &times;
                    </button>
                </div>
            )}

            {(!ataques || ataques.length === 0) ? (
                <p style={{ color: '#666', textAlign: 'center', fontSize: '0.85rem' }}>Nenhum ataque ou poder ofensivo.</p>
            ) : (
                <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                    <thead>
                        <tr style={{ color: '#888', textTransform: 'uppercase', fontSize: '0.7rem' }}>
                            {['Arma / Magia', 'Bônus / CD', 'Dano / Cura', 'Crít.', 'Tipo', 'Alcance', 'Teste', ''].map(h => (
                                <th key={h} style={{ textAlign: 'left', padding: '6px 8px', borderBottom: '1px solid #333', whiteSpace: 'nowrap' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {ataques.map((a, i) => {
                            const ehMagia = strEhMagia(a.especial);
                            const ehCura = a.tipo === 'Cura' || a.bonus_ataque === 'Cura';
                            const ehPvTemp = a.tipo === 'PV Temp' || a.bonus_ataque === 'PV Temp';
                            const cfg = ehMagia ? spellConfigs?.[a.nome] : undefined;
                            const danoExibido = cfg?.formulaEfetiva || a.dano;
                            const linhasEspecial: TooltipLinha[] = a.especial
                                ? a.especial.split('; ').map(t => ({
                                    texto: t,
                                    cor: ehPenalidade(t) ? '#ff8a80' : ehBuff(t) ? '#80deea' : '#ccc',
                                    negrito: ehPenalidade(t) || ehBuff(t),
                                }))
                                : [];

                            return (
                                <tr key={i} style={{ borderBottom: '1px solid #252525' }}>
                                    <td style={{ padding: '8px', minWidth: 190 }}>
                                        <PortalTooltip titulo={a.nome} linhas={linhasEspecial}>
                                            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '4px 6px' }}>
                                                <strong
                                                    onClick={() => ehMagia && onOpenSpell && onOpenSpell(a.nome)}
                                                    title={ehMagia && onOpenSpell ? 'Clique para abrir aprimoramentos da magia' : undefined}
                                                    style={{
                                                        color: ehCura ? '#81c784' : ehPvTemp ? '#64b5f6' : ehMagia ? '#ce93d8' : '#e0e0e0',
                                                        cursor: ehMagia && onOpenSpell ? 'pointer' : 'default',
                                                        lineHeight: 1.25,
                                                    }}
                                                >
                                                    {a.nome}
                                                </strong>
                                                {(cfg || a.especial) && (
                                                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, whiteSpace: 'nowrap', flexShrink: 0 }}>
                                                        {cfg && (
                                                            <span style={{ fontSize: '0.7rem', color: '#ce93d8', background: 'rgba(156,39,176,0.18)', border: '1px solid rgba(206,147,216,0.45)', borderRadius: 4, padding: '1px 6px', whiteSpace: 'nowrap', lineHeight: 1.25 }}>
                                                                {cfg.custoTotalPm} PM
                                                            </span>
                                                        )}
                                                        {a.especial && (
                                                            <span style={{ display: 'inline-flex', alignItems: 'center' }}>
                                                                <T20Icon
                                                                    name={ehPenalidade(a.especial) ? 'alerta' : ehCura ? 'hp' : ehMagia ? 'grimorio' : 'efeito'}
                                                                    size={13}
                                                                    color={ehPenalidade(a.especial) ? '#ffb74d' : ehCura ? '#81c784' : ehPvTemp ? '#64b5f6' : ehMagia ? '#ce93d8' : '#80deea'}
                                                                />
                                                            </span>
                                                        )}
                                                    </span>
                                                )}
                                            </div>
                                        </PortalTooltip>
                                    </td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: ehMagia ? '#ce93d8' : '#ccc', fontWeight: ehMagia ? 'bold' : 'normal' }}>
                                        <PortalTooltip
                                            titulo={ehCura ? `Magia de Cura — ${a.nome}` : ehPvTemp ? `PV Temporários — ${a.nome}` : ehMagia ? `Auditoria da CD — ${a.nome}` : `Auditoria de Ataque — ${a.nome}`}
                                            linhas={montarLinhasCdOuAtaque(a, ehMagia)}
                                        >
                                            {ehCura ? (
                                                <span style={{ fontSize: '0.72rem', background: 'rgba(76,175,80,0.18)', border: '1px solid rgba(129,199,132,0.5)', color: '#81c784', borderRadius: 4, padding: '2px 7px', fontWeight: 'bold' }}>
                                                    💚 CURA
                                                </span>
                                            ) : ehPvTemp ? (
                                                <span style={{ fontSize: '0.72rem', background: 'rgba(33,150,243,0.18)', border: '1px solid rgba(100,181,246,0.5)', color: '#64b5f6', borderRadius: 4, padding: '2px 7px', fontWeight: 'bold' }}>
                                                    🛡️ PV TEMP
                                                </span>
                                            ) : (
                                                <span style={{ borderBottom: '1px dotted rgba(206,147,216,0.55)' }}>
                                                    {a.bonus_ataque}
                                                </span>
                                            )}
                                        </PortalTooltip>
                                    </td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: ehCura ? '#81c784' : ehPvTemp ? '#64b5f6' : '#ffcc80', fontWeight: 'bold' }}>
                                        <PortalTooltip
                                            titulo={`${ehCura ? 'Auditoria de Cura' : ehPvTemp ? 'Auditoria de PV Temp' : 'Auditoria de Dano'} — ${a.nome}`}
                                            linhas={montarLinhasDano(a, ehMagia, cfg)}
                                        >
                                            <span style={{ borderBottom: `1px dotted ${ehCura ? 'rgba(129,199,132,0.55)' : ehPvTemp ? 'rgba(100,181,246,0.55)' : 'rgba(255,204,128,0.55)'}` }}>
                                                {danoExibido}
                                            </span>
                                        </PortalTooltip>
                                    </td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: '#ccc' }}>{a.critico}</td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: ehCura ? '#81c784' : ehPvTemp ? '#64b5f6' : '#ccc' }}>{a.tipo}</td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: '#ccc' }}>{a.alcance}</td>
                                    <td style={{ padding: '8px', whiteSpace: 'nowrap', color: '#ccc' }}>{a.teste}</td>
                                    <td style={{ padding: '8px', textAlign: 'right', whiteSpace: 'nowrap' }}>
                                        <button
                                            type="button"
                                            onClick={() => handleRolarAtaque(a)}
                                            title={`Rolar ${a.nome} (${danoExibido})`}
                                            style={{
                                                background: ehCura
                                                    ? 'rgba(76, 175, 80, 0.2)'
                                                    : ehPvTemp
                                                        ? 'rgba(33, 150, 243, 0.2)'
                                                        : ehMagia
                                                            ? 'rgba(156, 39, 176, 0.2)'
                                                            : 'rgba(255, 193, 7, 0.12)',
                                                color: ehCura ? '#81c784' : ehPvTemp ? '#64b5f6' : ehMagia ? '#ce93d8' : '#ffd54f',
                                                border: `1px solid ${ehCura ? 'rgba(129, 199, 132, 0.5)' : ehPvTemp ? 'rgba(100, 181, 246, 0.5)' : ehMagia ? 'rgba(206, 147, 216, 0.45)' : 'rgba(255, 213, 79, 0.35)'}`,
                                                borderRadius: 4,
                                                padding: '3px 8px',
                                                cursor: 'pointer',
                                                fontSize: '0.75rem',
                                                display: 'inline-flex',
                                                alignItems: 'center',
                                                gap: 4,
                                                whiteSpace: 'nowrap',
                                            }}
                                        >
                                            <T20Icon name="dado" size={12} /> {ehCura ? 'Curar' : 'Rolar'}
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                </div>
            )}
        </div>
    );
};

function strEhMagia(especial?: string): boolean {
    return Boolean(especial && especial.startsWith('Magia •'));
}
