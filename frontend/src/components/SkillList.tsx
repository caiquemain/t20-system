import React from 'react';
// CORREÇÃO AQUI: Adicionado 'type'
import type { Personagem, PericiaInfo } from '../types';
import '../Ficha.css';

interface SkillListProps {
    ficha: Personagem;
    dadosClasses: any;
    updateFicha: (dados: Partial<Personagem>) => void;
    listaTodasPericias: string[];
}

export const SkillList: React.FC<SkillListProps> = ({ ficha, dadosClasses, updateFicha, listaTodasPericias }) => {

    // --- CÁLCULOS DE REGRAS DE PERÍCIA ---
    const dadosClasseAtual = ficha.classes[0] ? dadosClasses[ficha.classes[0].nome] : null;
    const qtdBaseClasse = dadosClasseAtual?.qtd_escolhas || 0;
    const bonusInteligencia = Math.max(0, ficha.atributos.inteligencia);
    const limiteTotalEscolhas = qtdBaseClasse + bonusInteligencia;

    let countFixasClasse = 0;
    let countOrigem = 0;
    let countRacaPoder = 0;
    let gastosTotalManual = 0;
    let gastosForaDaClasse = 0;

    // Identifica quais perícias foram ganhas por habilidades (Raça/Poderes) para não cobrar do limite de Int/Classe
    const periciasDeHabilidades = new Set<string>();
    ficha.habilidades.forEach(hab => {
        if (hab.escolhas_aplicadas) {
            Object.entries(hab.escolhas_aplicadas).forEach(([key, v]) => {
                if (!key.includes('bonus') && listaTodasPericias.includes(String(v))) {
                    periciasDeHabilidades.add(String(v));
                }
            });
        }
    });

    // Faz a contagem dos gastos
    Object.entries(ficha.pericias).forEach(([nome, info]) => {
        if (info.treino > 0) {
            const isFixa = dadosClasseAtual?.pericias_fixas.includes(nome);
            const isOrigem = ficha.escolhas_origem?.includes(nome);
            const isHabilidadeChoice = periciasDeHabilidades.has(nome);
            const isOpcaoClasse = dadosClasseAtual?.pericias_lista.includes(nome);

            if (isFixa) countFixasClasse++;
            else if (isOrigem) countOrigem++;
            else if (isHabilidadeChoice) countRacaPoder++;
            else {
                gastosTotalManual++;
                // Se comprei manualmente e NÃO está na lista da classe, conta como gasto de Inteligência
                if (!isOpcaoClasse) gastosForaDaClasse++;
            }
        }
    });

    const slotsRestantesTotal = limiteTotalEscolhas - gastosTotalManual;
    const slotsRestantesInteligencia = bonusInteligencia - gastosForaDaClasse;
    const totalTreinadas = countFixasClasse + countOrigem + countRacaPoder + gastosTotalManual;

    // Helper para mapear sigla do atributo
    const attrMap: Record<string, string> = { 'for': 'forca', 'des': 'destreza', 'con': 'constituicao', 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma' };

    return (
        <div className="section-card">
            <h3 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                Perícias
                <div className="pericias-header-info">
                    <span style={{ fontSize: '0.8rem', color: slotsRestantesTotal < 0 ? '#ef5350' : '#66bb6a', cursor: 'help' }}>
                        (Livres: {slotsRestantesTotal})
                    </span>
                    <div className="info-tooltip">
                        <div className="info-row"><strong>Total Treinadas:</strong> <span>{totalTreinadas}</span></div>
                        <div className="info-row"><span>Classe (Fixas):</span> <span>{countFixasClasse}</span></div>
                        <div className="info-row"><span>Classe (Escolhas):</span> <span>{qtdBaseClasse}</span></div>
                        <div className="info-row"><span>Inteligência:</span> <span>{bonusInteligencia}</span></div>
                        <div className="info-row"><span>Origem:</span> <span>{countOrigem}</span></div>
                        <div className="info-row"><span>Raça/Poderes:</span> <span>{countRacaPoder}</span></div>
                        <div className="info-row" style={{ borderTop: '1px solid #444', marginTop: 4, paddingTop: 4 }}>
                            <strong>Gastos Manuais:</strong> <span>{gastosTotalManual} / {limiteTotalEscolhas}</span>
                        </div>
                        <div className="info-row" style={{ color: slotsRestantesInteligencia < 0 ? '#ef5350' : '#aaa', fontSize: '0.7rem' }}>
                            *Extra Classe (INT): {gastosForaDaClasse} / {bonusInteligencia}
                        </div>
                    </div>
                </div>
            </h3>

            <div className="pericias-wrapper">
                {(Object.entries(ficha.pericias) as [string, PericiaInfo][]).sort((a, b) => a[0].localeCompare(b[0])).map(([nome, info]) => {
                    const isTreinada = info.treino > 0;
                    const metadeNivel = Math.floor(ficha.cabecalho.nivel_total / 2);
                    // @ts-ignore
                    const modAtributo = ficha.atributos[attrMap[info.atributo_chave]];

                    // Regra de Bônus de Treino (2, 4 ou 6)
                    let bonusTreino = 0;
                    if (isTreinada) {
                        if (ficha.cabecalho.nivel_total >= 15) bonusTreino = 6;
                        else if (ficha.cabecalho.nivel_total >= 7) bonusTreino = 4;
                        else bonusTreino = 2;
                    }

                    const isFixaClasse = dadosClasseAtual?.pericias_fixas.includes(nome);
                    const isOpcaoClasse = dadosClasseAtual?.pericias_lista.includes(nome);
                    const isOrigem = ficha.escolhas_origem?.includes(nome);
                    const isHabilidadeChoice = periciasDeHabilidades.has(nome);

                    // Lógica de Desabilitar Checkbox
                    let disabled = false;
                    if (isFixaClasse || isOrigem || isHabilidadeChoice) {
                        disabled = true; // Já ganho por fonte externa, não pode destreinar
                    } else if (!isTreinada) {
                        // Se não sou treinado e quero treinar:
                        if (slotsRestantesTotal <= 0) {
                            disabled = true; // Sem pontos totais
                        } else if (!isOpcaoClasse && slotsRestantesInteligencia <= 0) {
                            disabled = true; // Sem inteligência para pegar fora da classe
                        }
                    }

                    return (
                        <div key={nome} className={`pericia-card ${isTreinada ? 'treinado' : ''} ${disabled && !isTreinada ? 'disabled-card' : ''}`}>
                            <label className="p-check-label">
                                <input
                                    type="checkbox"
                                    className="p-checkbox"
                                    checked={isTreinada}
                                    disabled={disabled}
                                    onChange={() => {
                                        const novasPericias = { ...ficha.pericias };
                                        // Toggle treino (0 ou 1) - Backend recalcula o total
                                        novasPericias[nome].treino = isTreinada ? 0 : 1;
                                        updateFicha({ pericias: novasPericias });
                                    }}
                                />
                                <div className="p-info-col">
                                    <div className="p-nome-row">
                                        <span className="p-nome">{nome}</span>
                                        <span className="p-attr">({info.atributo_chave.toUpperCase().substring(0, 3)})</span>
                                    </div>
                                    <div className="source-badges">
                                        {isFixaClasse && <span className="badge-source bg-classe-fixa">CLASSE</span>}
                                        {isOrigem && <span className="badge-source bg-origem">ORIGEM</span>}
                                        {isHabilidadeChoice && <span className="badge-source bg-raca">RAÇA/PODER</span>}

                                        {!isFixaClasse && !isOrigem && !isHabilidadeChoice && isTreinada && (
                                            isOpcaoClasse
                                                ? <span className="badge-source bg-classe-escolha">CLASSE</span>
                                                : <span className="badge-source" style={{ border: '1px solid #9c27b0', color: '#9c27b0' }}>INTELIGÊNCIA</span>
                                        )}
                                    </div>
                                </div>
                            </label>

                            <span className="p-valor">{info.total >= 0 ? `+${info.total}` : info.total}</span>

                            {/* TOOLTIP DETALHADO AO PASSAR O MOUSE */}
                            <div className="pericia-tooltip">
                                <div className="tooltip-row"><span>1/2 Nível:</span> <span>{isTreinada ? metadeNivel : 0}</span></div>
                                <div className="tooltip-row"><span>Atributo:</span> <span>{modAtributo}</span></div>
                                <div className="tooltip-row"><span>Treino:</span> <span>{bonusTreino}</span></div>
                                {info.outros !== 0 && <div className="tooltip-row"><span>Racial/Outros:</span> <span>{info.outros}</span></div>}
                                <div className="tooltip-row tooltip-total"><span>Total:</span> <span>{info.total}</span></div>

                                {isHabilidadeChoice && <div style={{ color: '#d32f2f', fontSize: '0.7rem', marginTop: 5 }}>Treinada por Habilidade Racial</div>}
                                {!isOpcaoClasse && !isTreinada && slotsRestantesInteligencia <= 0 && (
                                    <div style={{ color: '#f44336', fontSize: '0.7rem', marginTop: 5 }}>Requer Inteligência</div>
                                )}
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    );
};