import React, { useMemo, useState } from 'react';
import type { Magia } from '../types';
import { getSchoolColor, getCircleColor, getTypeColor, calcularCustoMagiaView } from '../utils/magicUtils';
import {
    rolarExpressao,
    extrairFormulaDeTexto,
    parseCustoAprimoramento,
    type ResultadoExpressao,
} from '../utils/diceRoller';
import { T20Icon } from './T20Icon';

interface SpellDetailsModalProps {
    magia: Magia | null;
    onClose: () => void;
    onRemove: () => void;
    ficha?: any;
    hideRemove?: boolean;
}

export const SpellDetailsModal: React.FC<SpellDetailsModalProps> = ({ magia, onClose, onRemove, ficha, hideRemove }) => {
    const [aprimoramentosQtd, setAprimoramentosQtd] = useState<Record<number, number>>({});
    const [truqueAtivo, setTruqueAtivo] = useState(false);
    const [ultimoRoll, setUltimoRoll] = useState<{
        resultado: ResultadoExpressao;
        rotulo: string;
        custoPm: number;
    } | null>(null);

    const custoBaseView = useMemo(() => (magia ? calcularCustoMagiaView(magia, ficha) : { total: 0, fontes: [] }), [magia, ficha]);

    if (!magia) return null;

    const typeColor = getTypeColor(magia.tipo);
    const schoolColor = getSchoolColor(magia.escola);
    const circleColor = getCircleColor(magia.circulo);
    const cdMagia = ficha?.combate?.cd_magias ?? 10;
    const nivelTotal = Math.max(1, Number(ficha?.cabecalho?.nivel_total || 1));
    const bonusDanoMagias = Number(ficha?.combate?.bonus_dano_magias || 0);

    // Soma de PM dos aprimoramentos selecionados
    const pmAprimoramentos = truqueAtivo
        ? 0
        : (magia.aprimoramentos || []).reduce((acc, ap, idx) => {
            const qtd = aprimoramentosQtd[idx] || 0;
            if (!qtd) return acc;
            const parsed = parseCustoAprimoramento(ap.custo);
            return acc + parsed.pm * qtd;
        }, 0);

    const custoTotalPm = truqueAtivo ? 0 : custoBaseView.total + pmAprimoramentos;
    const acimaLimitePm = !truqueAtivo && custoTotalPm > nivelTotal;

    // Fórmula de rolagem: usa rolagem estruturada do motor ou fallback da descrição
    const formulaBase = magia.rolagem?.formula || extrairFormulaDeTexto(magia.descricao);
    const tipoRolagem = magia.rolagem?.tipo || (/cura|recupera/i.test(magia.descricao) ? 'cura' : 'dano');
    const tipoDano = magia.rolagem?.tipo_dano || '';
    const formulaFinal = formulaBase
        ? (tipoRolagem === 'dano' && bonusDanoMagias > 0 ? `${formulaBase}+${bonusDanoMagias}` : formulaBase)
        : null;

    const handleToggleAprimoramento = (idx: number, ehTruque: boolean, delta: number) => {
        if (ehTruque) {
            const prox = !truqueAtivo;
            setTruqueAtivo(prox);
            if (prox) setAprimoramentosQtd({});
            return;
        }
        setTruqueAtivo(false);
        setAprimoramentosQtd(prev => {
            const atual = prev[idx] || 0;
            const prox = Math.max(0, atual + delta);
            const next = { ...prev };
            if (prox === 0) delete next[idx];
            else next[idx] = prox;
            return next;
        });
    };

    const handleRolarMagia = () => {
        if (!formulaFinal) return;
        const res = rolarExpressao(formulaFinal);
        if (!res) return;
        const rotulo =
            tipoRolagem === 'cura'
                ? 'Cura (PV)'
                : tipoRolagem === 'pv_temp'
                    ? 'PV Temporários'
                    : `Dano${tipoDano ? ` (${tipoDano})` : ''}`;
        setUltimoRoll({ resultado: res, rotulo, custoPm: custoTotalPm });
    };

    return (
        <div className="modal-overlay" style={{ zIndex: 3000 }}>
            <div className="modal-content" style={{ maxWidth: '540px', borderTop: `4px solid ${typeColor}` }}>

                <div className="modal-header">
                    <h3 style={{ fontSize: '1.4rem', color: '#fff', margin: 0 }}>
                        {magia.nome}
                    </h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="modal-body">
                    {/* Tags Coloridas */}
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
                        <span style={{ background: `${typeColor}15`, color: typeColor, border: `1px solid ${typeColor}60`, padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                            {magia.tipo || 'Universal'}
                        </span>

                        <span style={{
                            background: `${schoolColor}15`, color: schoolColor, border: `1px solid ${schoolColor}50`,
                            padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase'
                        }}>
                            {magia.escola}
                        </span>

                        <span style={{
                            color: circleColor, border: `1px solid ${circleColor}80`,
                            padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold'
                        }}>
                            {magia.circulo}º Círculo
                        </span>

                        <span className="badge-pm">{custoTotalPm} PM</span>

                        {magia.resistencia && (
                            <span style={{ background: 'rgba(255, 183, 77, 0.12)', color: '#ffb74d', border: '1px solid rgba(255, 183, 77, 0.4)', padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                                CD {cdMagia}
                            </span>
                        )}
                    </div>

                    {/* Painel de Rolagem Rápida da Magia */}
                    {formulaFinal && (
                        <div style={{ background: '#16161e', border: `1px solid ${typeColor}55`, borderRadius: '8px', padding: '12px', marginBottom: '14px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                                <div>
                                    <div style={{ fontSize: '0.72rem', color: '#999', textTransform: 'uppercase' }}>
                                        Rolagem da Magia ({tipoRolagem === 'cura' ? 'Cura' : tipoRolagem === 'pv_temp' ? 'PV Temp.' : tipoDano || 'Dano'})
                                    </div>
                                    <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#ffcc80' }}>
                                        {formulaFinal}
                                        {magia.resistencia ? ` • ${magia.resistencia} (CD ${cdMagia})` : ''}
                                    </div>
                                </div>
                                <button
                                    onClick={handleRolarMagia}
                                    style={{
                                        background: '#7b1fa2',
                                        color: '#fff',
                                        border: 'none',
                                        borderRadius: '6px',
                                        padding: '8px 14px',
                                        cursor: 'pointer',
                                        fontWeight: 'bold',
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        gap: '6px',
                                    }}
                                >
                                    <T20Icon name="dado" size={15} /> Rolar ({formulaFinal})
                                </button>
                            </div>

                            {ultimoRoll && (
                                <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #2d2d3a', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                                    <div style={{ fontSize: '0.82rem', color: '#ccc' }}>
                                        <strong>{ultimoRoll.rotulo}:</strong>{' '}
                                        {ultimoRoll.resultado.detalhes.map((d, i) => (
                                            <span key={i} style={{ marginRight: '6px', color: '#b39ddb' }}>
                                                {d.dado}[{d.rolagens.join(', ')}]
                                            </span>
                                        ))}
                                        {ultimoRoll.resultado.bonus !== 0 && (
                                            <span style={{ color: '#81c784' }}>
                                                {ultimoRoll.resultado.bonus > 0 ? `+${ultimoRoll.resultado.bonus}` : ultimoRoll.resultado.bonus}
                                            </span>
                                        )}
                                        <span style={{ marginLeft: '8px', color: '#888', fontSize: '0.75rem' }}>
                                            ({ultimoRoll.custoPm} PM)
                                        </span>
                                    </div>
                                    <div style={{ fontSize: '1.35rem', fontWeight: 'bold', color: '#ffd54f' }}>
                                        = {ultimoRoll.resultado.total}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Breakdown de Custo em PM */}
                    <div style={{ marginBottom: '14px', background: '#151515', border: '1px solid #333', borderRadius: '4px', padding: '6px 10px', fontSize: '0.72rem', color: '#aaa' }}>
                        {!truqueAtivo && custoBaseView.fontes.map((f: any, i: number) => (
                            <div key={i} style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <span>{f.label}</span>
                                <span style={{ color: f.valor < 0 ? '#81c784' : '#ccc' }}>{f.valor >= 0 ? `+${f.valor}` : f.valor} PM</span>
                            </div>
                        ))}
                        {!truqueAtivo && pmAprimoramentos > 0 && (
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <span>Aprimoramentos selecionados</span>
                                <span style={{ color: '#ce93d8' }}>+{pmAprimoramentos} PM</span>
                            </div>
                        )}
                        {truqueAtivo && (
                            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#80deea' }}>
                                <span>Truque ativo (versão simples)</span>
                                <span>0 PM</span>
                            </div>
                        )}
                        <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #444', marginTop: '4px', paddingTop: '4px', color: acimaLimitePm ? '#ff8a80' : '#ce93d8', fontWeight: 'bold' }}>
                            <span>Total {acimaLimitePm ? `(acima do limite de ${nivelTotal} PM!)` : ''}</span>
                            <span>{custoTotalPm} PM</span>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', background: '#1a1a1a', padding: '15px', borderRadius: '8px', marginBottom: '16px', border: '1px solid #333' }}>
                        <DetailInfo label="Execução" value={magia.execucao} />
                        <DetailInfo label="Alcance" value={magia.alcance} />
                        <DetailInfo label="Alvo/Área" value={magia.alvo || magia.alvo_area || '-'} />
                        <DetailInfo label="Duração" value={magia.duracao} />
                        <DetailInfo label="Resistência" value={magia.resistencia ? `${magia.resistencia} (CD ${cdMagia})` : '-'} />
                    </div>

                    <div style={{ background: '#111', padding: '15px', borderRadius: '6px', color: '#ddd', lineHeight: '1.6', fontSize: '0.95rem', whiteSpace: 'pre-wrap', borderLeft: `2px solid ${typeColor}80` }}>
                        {magia.descricao}
                    </div>

                    {magia.aprimoramentos && magia.aprimoramentos.length > 0 && (
                        <div style={{ marginTop: '20px' }}>
                            <h4 style={{ color: '#aaa', fontSize: '0.85rem', textTransform: 'uppercase', borderBottom: '1px solid #333', paddingBottom: '5px', marginBottom: '10px' }}>
                                Aprimoramentos (clique para somar PM)
                            </h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {magia.aprimoramentos.map((ap, idx) => {
                                    const parsed = parseCustoAprimoramento(ap.custo);
                                    const cumulativo = /^aumenta/i.test((ap.descricao || '').trim());
                                    const qtd = parsed.ehTruque ? (truqueAtivo ? 1 : 0) : (aprimoramentosQtd[idx] || 0);
                                    const ativo = qtd > 0;
                                    return (
                                        <div
                                            key={idx}
                                            style={{
                                                display: 'flex',
                                                gap: '10px',
                                                background: ativo ? 'rgba(156, 39, 176, 0.14)' : '#1a1a1a',
                                                padding: '8px',
                                                borderRadius: '4px',
                                                border: ativo ? '1px solid rgba(206, 147, 216, 0.6)' : '1px solid #2a2a2a',
                                                flexWrap: 'wrap',
                                                alignItems: 'flex-start',
                                            }}
                                        >
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', minWidth: '88px' }}>
                                                {cumulativo && !parsed.ehTruque ? (
                                                    <>
                                                        <button
                                                            type="button"
                                                            onClick={() => handleToggleAprimoramento(idx, false, -1)}
                                                            disabled={qtd === 0}
                                                            style={{ width: 22, height: 22, background: '#2a2a2a', color: '#fff', border: '1px solid #444', borderRadius: 3, cursor: qtd ? 'pointer' : 'not-allowed' }}
                                                        >-</button>
                                                        <span style={{ color: '#ce93d8', fontWeight: 'bold', fontSize: '0.8rem', minWidth: 16, textAlign: 'center' }}>{qtd}</span>
                                                        <button
                                                            type="button"
                                                            onClick={() => handleToggleAprimoramento(idx, false, 1)}
                                                            style={{ width: 22, height: 22, background: '#2a2a2a', color: '#fff', border: '1px solid #444', borderRadius: 3, cursor: 'pointer' }}
                                                        >+</button>
                                                    </>
                                                ) : (
                                                    <input
                                                        type="checkbox"
                                                        checked={ativo}
                                                        onChange={() => handleToggleAprimoramento(idx, parsed.ehTruque, ativo ? -1 : 1)}
                                                        style={{ cursor: 'pointer' }}
                                                    />
                                                )}
                                                <span style={{ color: parsed.ehTruque ? '#80deea' : '#ce93d8', fontWeight: 'bold', fontSize: '0.82rem', whiteSpace: 'nowrap' }}>
                                                    {parsed.ehTruque ? 'Truque · 0 PM' : ap.custo}
                                                </span>
                                            </div>
                                            <div style={{ color: '#ccc', fontSize: '0.88rem', lineHeight: '1.4', flex: 1 }}>{ap.descricao}</div>
                                            {parsed.ehTruque && (
                                                <div style={{ color: '#80deea', fontSize: '0.7rem', minWidth: '100%', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                                    <T20Icon name="info" size={12} /> Truque: custo 0 PM — não combina com outros aprimoramentos
                                                </div>
                                            )}
                                            {/Requer \dº círculo/.test(ap.descricao) && (magia.fonte_origem || '').startsWith('Racial') && (
                                                <div style={{ color: '#ff8a80', fontSize: '0.7rem', minWidth: '100%', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                                    <T20Icon name="cadeado" size={12} /> Pré-requisito de círculo: magias raciais não podem cumpri-lo
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                </div>

                <div className="modal-footer" style={{ justifyContent: 'space-between' }}>
                    {!hideRemove && (
                        <button className="btn-delete" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }} onClick={() => { if (window.confirm(`Tem certeza que deseja esquecer a magia "${magia.nome}"?`)) { onRemove(); onClose(); } }}>
                            <T20Icon name="excluir" size={14} /> Esquecer Magia
                        </button>
                    )}
                    <button className="btn-cancel" onClick={onClose}>Fechar</button>
                </div>
            </div>
            <style>{`
                .badge-pm { background: rgba(156, 39, 176, 0.15); color: #ce93d8; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; border: 1px solid rgba(156, 39, 176, 0.4); }
                .btn-delete { background: rgba(255, 82, 82, 0.1); color: #ff5252; border: 1px solid #ff5252; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
                .btn-delete:hover { background: #ff5252; color: white; }
            `}</style>
        </div>
    );
};

const DetailInfo = ({ label, value }: { label: string, value: string }) => (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase', marginBottom: '3px', fontWeight: '600' }}>{label}</span>
        <span style={{ fontSize: '0.9rem', color: '#fff', fontWeight: '500' }}>{value}</span>
    </div>
);