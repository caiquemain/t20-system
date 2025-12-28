import React, { useState } from 'react';
import type { Personagem } from '../types';
import { DADOS_PERICIAS_FRONTEND } from '../data/pericias';

interface SkillListProps {
    ficha: Personagem;
    dadosClasses: any;
    updateFicha: (dados: Partial<Personagem>) => void;
    listaTodasPericias: string[];
}

export const SkillList: React.FC<SkillListProps> = ({ ficha, dadosClasses, updateFicha, listaTodasPericias }) => {

    // --- LÓGICA DE DADOS ---
    const classePrincipal = ficha.classes[0]?.nome;
    const dadosClasse = dadosClasses[classePrincipal] || {};

    const periciasFixas = dadosClasse.pericias_iniciais || dadosClasse.pericias_fixas || [];
    const periciasEscolhaLista = dadosClasse.pericias_lista || [];
    const qtdEscolhasClasse = dadosClasse.pericias_escolha || 0;

    const intAttr = ficha.atributos.inteligencia || 0;
    const intMod = intAttr;
    const qtdTotalEscolhas = qtdEscolhasClasse + (intMod > 0 ? intMod : 0);

    const periciasOrigem = ficha.escolhas_origem || [];
    const periciasTreinadas = ficha.pericias || {};

    const periciasCompradas = Object.keys(periciasTreinadas).filter(p =>
        periciasTreinadas[p].treino > 0 &&
        !periciasFixas.includes(p) &&
        !periciasOrigem.includes(p)
    );

    const totalGastos = periciasCompradas.length;

    const gastosForaDaClasse = periciasCompradas.filter(p => {
        const ehDaClasse = periciasEscolhaLista.includes(p) || p.startsWith("Ofício");
        return !ehDaClasse;
    }).length;

    const slotsInteligenciaRestantes = Math.max(0, intMod - gastosForaDaClasse);
    const slotsTotaisRestantes = Math.max(0, qtdTotalEscolhas - totalGastos);

    // --- AÇÕES ---
    const togglePericia = (pericia: string) => {
        if (periciasFixas.includes(pericia)) return;

        const novaLista = { ...periciasTreinadas };
        const estaTreinada = novaLista[pericia]?.treino > 0;

        if (estaTreinada) {
            novaLista[pericia] = { ...novaLista[pericia], treino: 0, total: 0 };
        } else {
            if (totalGastos >= qtdTotalEscolhas) return;

            const ehDaClasse = periciasEscolhaLista.includes(pericia) || pericia.startsWith("Ofício");

            if (!ehDaClasse && slotsInteligenciaRestantes <= 0) {
                return;
            }

            novaLista[pericia] = {
                treino: 1,
                bonus_nivel: Math.floor((ficha.cabecalho.nivel_total || 1) / 2),
                atributo_valor: 0,
                outros: 0,
                total: 0
            };
        }
        updateFicha({ pericias: novaLista });
    };

    const renderSkillRow = (nomeExibicao: string, chavePericia: string, index: number) => {
        const info = periciasTreinadas[chavePericia] || { treino: 0, bonus_nivel: 0, atributo_valor: 0, outros: 0, total: 0 };

        const chaveBase = chavePericia.startsWith("Ofício") ? "Ofício" : chavePericia;
        const meta = DADOS_PERICIAS_FRONTEND[chaveBase] || { atributo: "???", treino_apenas: false, penalidade_armadura: false };

        const isFixa = periciasFixas.includes(chavePericia);
        const isOrigem = periciasOrigem.includes(chavePericia);
        const isTreinada = info.treino > 0;

        const ehDaClasse = periciasEscolhaLista.includes(chavePericia) || chavePericia.startsWith("Ofício");
        const podeComprar = slotsTotaisRestantes > 0 && (ehDaClasse || slotsInteligenciaRestantes > 0);

        const isInteractable = isTreinada || (!isFixa && !isOrigem && podeComprar);
        const isDisabled = !isInteractable;

        const nivel = Math.max(1, ficha.cabecalho.nivel_total || 1);
        const metadeNivel = Math.floor(nivel / 2);
        const attrVal = info.atributo_valor;
        const treinoVal = isTreinada ? (nivel >= 15 ? 6 : (nivel >= 7 ? 4 : 2)) : 0;
        const outrosVal = info.outros;
        const totalVal = info.total;

        const penalidadeEstimada = totalVal - (metadeNivel + attrVal + treinoVal + outrosVal);
        const temPenalidade = meta.penalidade_armadura && penalidadeEstimada < 0;

        const rowBg = index % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent';

        return (
            <div key={chavePericia} className={`skill-row-grid ${isDisabled && !isFixa && !isOrigem ? 'disabled' : ''}`} style={{ background: rowBg }}>

                {/* CHECKBOX */}
                <div className="col-check" onClick={() => !isFixa && !isOrigem && togglePericia(chavePericia)}>
                    <div className={`checkbox-box ${isTreinada ? 'checked' : ''} ${isFixa || isOrigem ? 'locked' : ''}`}>
                        {isTreinada && "✔"}
                    </div>
                </div>

                {/* NOME (Sem title nativo para não atrapalhar) */}
                <div className="col-name" onClick={() => !isFixa && !isOrigem && togglePericia(chavePericia)}>
                    <span className={`name-text ${isTreinada ? 'trained-text' : ''}`}>
                        {nomeExibicao}
                        {isTreinada && !isFixa && !isOrigem && !ehDaClasse && (
                            <span title="Custo Inteligência" style={{ color: '#00bcd4', fontSize: '0.7em', marginLeft: 5 }}>🧠</span>
                        )}
                    </span>
                    <div className="icons-container">
                        {meta.treino_apenas && <span title="Somente Treinada" className="icon-badge star">✴️</span>}
                        {meta.penalidade_armadura && <span title="Penalidade de Armadura" className="icon-badge shield">🛡️</span>}
                        {isFixa && <span className="text-badge class">(C)</span>}
                        {isOrigem && <span className="text-badge origin">(O)</span>}
                    </div>
                </div>

                {/* TOTAL (Aqui está o Tooltip Customizado) */}
                <div className="col-total tooltip-container">
                    <div className="total-box">{totalVal >= 0 ? `+${totalVal}` : totalVal}</div>

                    {/* O HTML DO TOOLTIP ESTÁ AQUI */}
                    <div className="pericia-tooltip">
                        <div className="tooltip-row">
                            <span>1/2 do Nível</span>
                            <span>+{metadeNivel}</span>
                        </div>
                        <div className="tooltip-row">
                            <span>Atributo ({meta.atributo})</span>
                            <span>{attrVal >= 0 ? `+${attrVal}` : attrVal}</span>
                        </div>
                        <div className="tooltip-row">
                            <span>Treino</span>
                            <span>+{treinoVal}</span>
                        </div>
                        <div className="tooltip-row">
                            <span>Outros</span>
                            <span>{outrosVal >= 0 ? `+${outrosVal}` : outrosVal}</span>
                        </div>

                        {temPenalidade && (
                            <div className="tooltip-row" style={{ color: '#ef5350' }}>
                                <span>Penalidade</span>
                                <span>{penalidadeEstimada}</span>
                            </div>
                        )}

                        <div className="tooltip-total">
                            <span>Total</span>
                            <span>{totalVal >= 0 ? `+${totalVal}` : totalVal}</span>
                        </div>
                    </div>
                </div>

                <div className="col-equal">=</div>

                {/* FÓRMULA SIMPLES */}
                <div className="col-formula">
                    <span className="val-item" title="1/2 Nível">+{metadeNivel}</span>
                    <span className="plus">+</span>
                    <div className="val-item attr-item" title={`Atributo ${meta.atributo}`}>
                        <span>{attrVal >= 0 ? `+${attrVal}` : attrVal}</span>
                        <small>{meta.atributo}</small>
                    </div>
                    <span className="plus">+</span>
                    <span className="val-item" title="Treino">+{treinoVal}</span>
                    <span className="plus">+</span>
                    <span className="val-item" title="Outros">+{outrosVal}</span>
                </div>
            </div>
        );
    };

    const [novoOficio, setNovoOficio] = useState("");
    const adicionarOficio = () => {
        if (!novoOficio) return;
        const nomeCompleto = `Ofício (${novoOficio})`;
        if (!periciasTreinadas[nomeCompleto]) {
            if (slotsTotaisRestantes > 0) {
                const novaLista = { ...periciasTreinadas };
                novaLista[nomeCompleto] = { treino: 1, bonus_nivel: 0, atributo_valor: 0, outros: 0, total: 0 };
                updateFicha({ pericias: novaLista });
            }
            setNovoOficio("");
        }
    };

    const listaExibicao = [...listaTodasPericias];
    Object.keys(periciasTreinadas).forEach(p => {
        if (p.startsWith("Ofício") && !listaExibicao.includes(p)) {
            listaExibicao.push(p);
        }
    });
    listaExibicao.sort();

    return (
        // REMOVIDO: overflow: hidden (Isso cortava o tooltip)
        <div className="section-card" style={{ padding: 0 }}>
            <div className="section-header" style={{ padding: '8px 12px', background: '#222', borderBottom: '1px solid #444', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ margin: 0, fontSize: '1rem', color: '#fff' }}>PERÍCIAS</h3>
                <div style={{ fontSize: '0.8rem', color: '#aaa', display: 'flex', gap: '15px' }}>
                    <span>
                        Classe: <strong style={{ color: '#ffd700' }}>{qtdTotalEscolhas - intMod}</strong>
                    </span>
                    <span>
                        Inteligência: <strong style={{ color: '#00bcd4' }}>{slotsInteligenciaRestantes}</strong>/<strong style={{ color: '#00bcd4' }}>{intMod}</strong>
                    </span>
                    <span>
                        Restante: <strong style={{ color: slotsTotaisRestantes > 0 ? '#4caf50' : '#f44336' }}>{slotsTotaisRestantes}</strong>
                    </span>
                </div>
            </div>

            <div className="skill-header-grid">
                <div className="h-check"></div>
                <div className="h-name">PERÍCIA</div>
                <div className="h-total">TOTAL</div>
                <div className="h-equal"></div>
                <div className="h-formula">
                    <span style={{ width: 25 }}>1/2</span>
                    <span style={{ width: 10 }}></span>
                    <span style={{ width: 25 }}>ATR</span>
                    <span style={{ width: 10 }}></span>
                    <span style={{ width: 25 }}>TR</span>
                    <span style={{ width: 10 }}></span>
                    <span style={{ width: 25 }}>OUT</span>
                </div>
            </div>

            <div className="skills-container" style={{ padding: '0 5px' }}>
                {listaExibicao.map((pericia, index) => renderSkillRow(pericia, pericia, index))}
            </div>

            <div className="add-skill-row" style={{ padding: '8px 12px', borderTop: '1px solid #333' }}>
                <input
                    type="text"
                    placeholder="Novo Ofício..."
                    value={novoOficio}
                    onChange={(e) => setNovoOficio(e.target.value)}
                />
                <button onClick={adicionarOficio}>+</button>
            </div>

            <style>{`
                .skill-row-grid, .skill-header-grid {
                    display: grid;
                    grid-template-columns: 22px 1fr 35px 10px 135px;
                    align-items: center;
                    padding: 4px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.05);
                }

                .skill-header-grid {
                    font-size: 0.6rem; color: #888; font-weight: bold;
                    border-bottom: 1px solid #444; padding: 5px 10px;
                    text-transform: uppercase; letter-spacing: 0.5px;
                }

                .col-check { display: flex; justify-content: center; cursor: pointer; }
                .checkbox-box {
                    width: 12px; height: 12px; border: 1px solid #555; border-radius: 2px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 9px; color: #000; background: #222;
                }
                .checkbox-box.checked { background: #ffd700; border-color: #ffd700; }
                .checkbox-box.locked { background: #4caf50; border-color: #4caf50; color: #fff; }

                .col-name { 
                    display: flex; align-items: center; padding-left: 5px; cursor: pointer; 
                    white-space: nowrap; overflow: hidden;
                }
                .name-text { 
                    font-size: 0.85rem; color: #ccc; 
                    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; 
                }
                .name-text.trained-text { color: #fff; font-weight: 600; }
                
                .icons-container { margin-left: 4px; display: flex; gap: 2px; flex-shrink: 0; }
                .icon-badge { font-size: 0.65rem; }
                .text-badge { font-size: 0.5rem; padding: 0 3px; border-radius: 2px; color:#000; font-weight:bold; }
                .text-badge.class { background: #4caf50; }
                .text-badge.origin { background: #2196f3; }

                /* AREA DE HOVER PARA O TOOLTIP */
                .col-total { 
                    display: flex; 
                    justify-content: center; 
                    position: relative; /* Necessário para posicionar o tooltip */
                    cursor: help;
                }
                .total-box {
                    width: 30px; height: 22px; border: 1px solid #444; background: #1a1a1a;
                    display: flex; align-items: center; justify-content: center;
                    font-weight: bold; font-size: 0.9rem; color: #fff; border-radius: 3px;
                }

                /* ESTILO DO TOOLTIP */
                .pericia-tooltip {
                    visibility: hidden;
                    opacity: 0;
                    position: absolute;
                    bottom: 100%;
                    left: 50%;
                    /* Centraliza e joga para cima */
                    transform: translateX(-50%) translateY(0px);
                    width: 180px;
                    background-color: #1a1a1a;
                    border: 1px solid #ffd700; /* Borda Dourada para destaque */
                    border-radius: 6px;
                    padding: 10px;
                    z-index: 9999; /* Z-Index bem alto */
                    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9);
                    transition: opacity 0.2s, transform 0.2s;
                    pointer-events: none;
                }

                /* TRIGGER DO HOVER */
                .col-total:hover .pericia-tooltip {
                    visibility: visible;
                    opacity: 1;
                    /* Pequena animação subindo */
                    transform: translateX(-50%) translateY(-10px);
                }

                .tooltip-row {
                    display: flex; justify-content: space-between;
                    font-size: 0.75rem; color: #ccc;
                    margin-bottom: 3px; border-bottom: 1px dashed #333;
                }
                .tooltip-total {
                    border-top: 1px solid #fca311; margin-top: 5px;
                    padding-top: 2px; font-weight: bold; color: #fca311;
                    display: flex; justify-content: space-between;
                }

                .col-equal { text-align: center; color: #555; font-weight: bold; font-size: 0.8rem; }

                .col-formula {
                    display: flex; justify-content: space-around; 
                    color: #666; font-family: monospace; font-size: 0.75rem;
                }
                .val-item { width: 25px; text-align: center; color: #999; display: inline-block; }
                .plus { width: 8px; text-align: center; color: #444; display: inline-block; }
                .val-item.attr-item { display: flex; flex-direction: column; align-items: center; line-height: 0.8; }
                .attr-item span { color: #eee; }
                .attr-item small { font-size: 0.5rem; color: #555; margin-top: 1px; }

                .add-skill-row { display: flex; gap: 5px; }
                .add-skill-row input { flex: 1; padding: 4px 8px; background: #111; border: 1px solid #444; color: #fff; border-radius: 3px; font-size: 0.8rem; }
                .add-skill-row button { padding: 0 10px; background: #333; color: #fff; border: 1px solid #444; border-radius: 3px; cursor: pointer; }
            `}</style>
        </div>
    );
};