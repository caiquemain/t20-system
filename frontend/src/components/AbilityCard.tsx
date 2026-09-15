import React from 'react';
import { DesejosButton } from './DesejosButton';

// Condições situacionais ativáveis direto no card da habilidade
const CONDICOES_TOGGLE: Record<string, { id: string; label: string; icone: string }> = {
    "Reptiliano": { id: "sem_armadura", label: "Sem armadura ou roupas pesadas", icone: "🦎" },
    "Conhecimento das Rochas": { id: "subterraneo", label: "No subterrâneo", icone: "⛰️" },
};
import type { Habilidade } from '../types';

interface AbilityCardProps {
    habilidade: Habilidade;
    pmAtual: number;
    onAtivar: (custo: number, nome: string) => void;
    updateFicha?: (data: any) => void;
    magiasConhecidas?: string[];
    condicoesAtivas?: string[];
}

export const AbilityCard: React.FC<AbilityCardProps> = ({ habilidade, pmAtual, onAtivar, updateFicha, magiasConhecidas = [], condicoesAtivas = [] }) => {
    const ativavel = habilidade.efeitos?.habilidade_ativavel;
    const podePagar = ativavel ? pmAtual >= ativavel.custo : false;

    const getActionColor = (acao?: string) => {
        const a = acao?.toLowerCase() || '';
        if (a.includes('padrão')) return '#d32f2f';
        if (a.includes('movimento')) return '#fbc02d';
        if (a.includes('livre') || a.includes('reac')) return '#388e3c';
        if (a.includes('completa')) return '#7b1fa2';
        return '#666';
    };

    // ✨ Chips de ESCOLHAS REAIS
    const efeitos = habilidade.efeitos || {};
    const escolhas = habilidade.escolhas_aplicadas || {};
    const ROTULOS_ESCOLHA: Record<string, string> = {
        poder_escolha: 'Poder Geral',
        resistencia_rd_escolha: 'Ascendência',
    };

    // Formata rótulo legível: magia_0 -> "Magia 1", magia_1 -> "Magia 2"
    const formatarRotuloEscolha = (chave: string): string => {
        if (ROTULOS_ESCOLHA[chave]) return ROTULOS_ESCOLHA[chave];
        const m = chave.match(/^(.+)_(\d+)$/);
        if (m) {
            const base = m[1].replace(/_/g, ' ');
            const idx = parseInt(m[2], 10) + 1;
            return base.charAt(0).toUpperCase() + base.slice(1) + ' ' + idx;
        }
        return chave.replace(/_/g, ' ');
    };
    const chavesEscolha = Object.keys(escolhas).filter(chave => {
        // Gatilhos de escolha nunca são escolhas reais — EXCETO quando o
        // gatilho é numérico (quantidade) e o valor salvo é string
        // (escolha real), ex.: poder_escolha=1 + "Lobo Solitário"
        if (chave.endsWith('_escolha')) {
            const vEfeito = (efeitos as any)[chave];
            const vEscolha = escolhas[chave];
            // Gatilho pode ser number (quantidade) OU string (nome já escolhido)
            if (!(typeof vEscolha === 'string' && vEscolha)) return false;
        }
        const v = escolhas[chave];
        // Objetos não renderizam (evita [object Object])
        if (v !== null && typeof v === 'object' && !Array.isArray(v)) return false;
        if (Array.isArray(v)) {
            // Arrays de objetos não renderizam
            if (v.some(item => typeof item === 'object')) return false;
            // Array IDÊNTICO ao de efeitos = gatilho vazado (ex.: escolha_subclasse com as 3 opções)
            if (chave in efeitos && JSON.stringify(efeitos[chave]) === JSON.stringify(v)) return false;
        }
        return true;
    });

    return (
        <div style={{ background: '#1e1e1e', borderRadius: '8px', marginBottom: '10px', border: '1px solid #333', overflow: 'hidden' }}>
            <div style={{ padding: '10px 15px', background: '#252525', borderBottom: '1px solid #333', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 'bold', color: '#e0e0e0' }}>{habilidade.nome}</span>
                <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase' }}>{habilidade.tipo}</span>
            </div>
            <div style={{ padding: '15px', color: '#ccc', fontSize: '0.9rem', lineHeight: '1.5' }}>
                {habilidade.descricao}
                {chavesEscolha.length > 0 && (
                    <div style={{ marginTop: '10px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                        {chavesEscolha.map(chave => {
                            const valor = escolhas[chave];
                            const valores = Array.isArray(valor) ? valor : [valor];
                            return valores.map((v: any, i: number) => (
                                <span key={`${chave}-${i}`} style={{
                                    fontSize: '0.75rem', color: '#80deea',
                                    background: 'rgba(0, 188, 212, 0.1)',
                                    padding: '2px 8px', borderRadius: '4px',
                                    border: '1px solid rgba(0, 188, 212, 0.4)'
                                }}>
                                    ✨ {formatarRotuloEscolha(chave)}: <strong>{String(v)}</strong>
                                </span>
                            ));
                        })}
                    </div>
                )}
                {ativavel && (
                    <div style={{ marginTop: '10px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                        {ativavel.alcance && <Badge label="Alcance" value={ativavel.alcance} />}
                        {ativavel.duracao && <Badge label="Duração" value={ativavel.duracao} />}
                        {ativavel.resistencia && <Badge label="Resistência" value={ativavel.resistencia} />}
                    </div>
                )}
                {CONDICOES_TOGGLE[habilidade.nome] && (efeitos as any).bonus_pericia_condicional && updateFicha && (() => {
                    const cfg = CONDICOES_TOGGLE[habilidade.nome];
                    const ativa = condicoesAtivas.includes(cfg.id);
                    const bonusTxt = Object.entries((efeitos as any).bonus_pericia_condicional as Record<string, number>)
                        .map(([p, v]) => `+${v} ${p}`).join(', ');
                    return (
                        <div style={{ marginTop: 10 }}>
                            <button
                                className="btn-action"
                                style={{
                                    background: ativa ? 'rgba(76, 175, 80, 0.15)' : 'transparent',
                                    border: `1px solid ${ativa ? '#4caf50' : '#555'}`,
                                    color: ativa ? '#4caf50' : '#888',
                                    fontWeight: 'bold', fontSize: '0.8rem', padding: '6px 12px',
                                    display: 'block', width: '100%', textAlign: 'left'
                                }}
                                title={ativa ? 'Desativar condição (remove o bônus)' : 'Ativar condição (aplica o bônus)'}
                                onClick={() => {
                                    const novas = ativa
                                        ? condicoesAtivas.filter((c: string) => c !== cfg.id)
                                        : [...condicoesAtivas, cfg.id];
                                    updateFicha({ condicoes_ativas: novas } as any);
                                }}
                            >
                                {cfg.icone} {ativa ? 'ATIVO:' : 'Ativar:'} {cfg.label} ({bonusTxt})
                            </button>
                        </div>
                    );
                })()}
                {habilidade.nome === "Desejos" && updateFicha && (
                    <DesejosButton
                        magiaAtual={escolhas.magia_desejada || ''}
                        magiasConhecidas={magiasConhecidas}
                        reducao={efeitos.reducao_pm_condicional || 1}
                        onEscolher={(nome: string) => {
                            const novasEscolhas = { ...escolhas, magia_desejada: nome || null };
                            const novasHabilidades = (habilidade as any)._ficha_habilidades || [];
                            const habIndex = novasHabilidades.findIndex((h: any) => h.nome === habilidade.nome);
                            if (habIndex >= 0) {
                                const updated = [...novasHabilidades];
                                updated[habIndex] = { ...updated[habIndex], escolhas_aplicadas: novasEscolhas };
                                updateFicha({ habilidades: updated });
                            }
                        }}
                    />
                )}
            </div>
            {ativavel && (
                <div style={{ padding: '10px 15px', background: '#1a1a1a', borderTop: '1px solid #333', display: 'flex', justifyContent: 'flex-end' }}>
                    <button
                        onClick={() => onAtivar(ativavel.custo, habilidade.nome)}
                        disabled={!podePagar}
                        style={{
                            background: podePagar ? 'transparent' : 'rgba(255,255,255,0.05)',
                            border: `1px solid ${podePagar ? getActionColor(ativavel.acao) : '#444'}`,
                            color: podePagar ? getActionColor(ativavel.acao) : '#666',
                            padding: '6px 12px', borderRadius: '4px',
                            cursor: podePagar ? 'pointer' : 'not-allowed',
                            fontWeight: 'bold', fontSize: '0.85rem',
                            display: 'flex', alignItems: 'center', gap: '8px', transition: 'all 0.2s'
                        }}
                        onMouseOver={(e) => { if (podePagar) { e.currentTarget.style.background = getActionColor(ativavel.acao); e.currentTarget.style.color = '#111'; } }}
                        onMouseOut={(e) => { if (podePagar) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = getActionColor(ativavel.acao); } }}
                    >
                        <span>⚡ {ativavel.custo} PM</span>
                        <span style={{ borderLeft: `1px solid ${podePagar ? 'currentColor' : '#444'}`, paddingLeft: '8px', opacity: 0.8 }}>
                            {ativavel.acao || 'Livre'}
                        </span>
                    </button>
                </div>
            )}
        </div>
    );
};

const Badge = ({ label, value }: { label: string, value: string }) => (
    <span style={{ fontSize: '0.75rem', color: '#888', background: '#222', padding: '2px 6px', borderRadius: '4px', border: '1px solid #333' }}>
        <strong>{label}:</strong> {value}
    </span>
);
