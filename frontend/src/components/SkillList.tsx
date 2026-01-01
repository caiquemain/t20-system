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

    const classePrincipal = ficha.classes[0]?.nome;
    const dadosClasse = dadosClasses[classePrincipal] || {};

    const periciasFixas = dadosClasse.pericias_iniciais || dadosClasse.pericias_fixas || [];
    const periciasObrigatoriasSelecao = dadosClasse.pericias_fixas_selecao || [];
    const periciasDaClassePossiveis = dadosClasse.pericias_lista || [];
    const qtdEscolhasClasse = dadosClasse.pericias_escolha || 0;

    const intAttr = ficha.atributos.inteligencia || 0;
    const qtdEscolhasInteligencia = Math.max(0, intAttr);

    const periciasOrigem = ficha.escolhas_origem || [];
    const periciasTreinadas = ficha.pericias || {};

    const periciasCompradas = Object.keys(periciasTreinadas).filter(p =>
        periciasTreinadas[p].treino > 0 &&
        !periciasFixas.includes(p) &&
        !periciasOrigem.includes(p)
    );

    let gastosDeClasse = 0;
    const compradasParaProcessar = [...periciasCompradas];

    for (let i = compradasParaProcessar.length - 1; i >= 0; i--) {
        const p = compradasParaProcessar[i];
        const ehDaClasse = periciasDaClassePossiveis.includes(p) || p.startsWith("Ofício");

        if (ehDaClasse && gastosDeClasse < qtdEscolhasClasse) {
            gastosDeClasse++;
            compradasParaProcessar.splice(i, 1);
        }
    }

    const gastosDeInteligencia = compradasParaProcessar.length;
    const slotsClasseRestantes = Math.max(0, qtdEscolhasClasse - gastosDeClasse);
    const slotsInteligenciaRestantes = Math.max(0, qtdEscolhasInteligencia - gastosDeInteligencia);

    const cumpriuRequisitoObrigatorio = periciasObrigatoriasSelecao.length === 0 ||
        periciasObrigatoriasSelecao.some((p: string) => periciasTreinadas[p]?.treino > 0);

    const isTravadoPelaObrigatoria = !cumpriuRequisitoObrigatorio && slotsClasseRestantes === 1;

    // --- AÇÕES ---
    const alternarAtributo = (pericia: string, info: any) => {
        const possiveis = (info as any).atributos_possiveis || [];
        if (possiveis.length <= 1) return;

        const atual = (info as any).atributo_selecionado || possiveis[0];
        const idxAtual = possiveis.indexOf(atual);
        const proximoIdx = (idxAtual + 1) % possiveis.length;
        const novoAttr = possiveis[proximoIdx];

        updateFicha({
            pericias: {
                ...periciasTreinadas,
                [pericia]: {
                    ...periciasTreinadas[pericia],
                    atributo_selecionado: novoAttr
                }
            }
        });
    };

    const togglePericia = (pericia: string) => {
        if (periciasFixas.includes(pericia) || periciasOrigem.includes(pericia)) return;

        const novaLista = { ...periciasTreinadas };
        const estaTreinada = novaLista[pericia]?.treino > 0;

        if (estaTreinada) {
            novaLista[pericia] = { ...novaLista[pericia], treino: 0, total: 0 };
        } else {
            const ehDaClasse = periciasDaClassePossiveis.includes(pericia) || pericia.startsWith("Ofício");
            const ehObrigatoria = periciasObrigatoriasSelecao.includes(pericia);

            if (isTravadoPelaObrigatoria && ehDaClasse && !ehObrigatoria) return;

            let podeComprar = false;
            if (ehDaClasse) {
                if (slotsClasseRestantes > 0) podeComprar = true;
                else if (slotsInteligenciaRestantes > 0) podeComprar = true;
            } else {
                if (slotsInteligenciaRestantes > 0) podeComprar = true;
            }

            if (!podeComprar) return;

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
        const bonusAuto = (info as any).bonus_automatico || 0;
        const fontesBonus = (info as any).fontes_bonus || [];

        const atributosPossiveis = (info as any).atributos_possiveis || [];
        const atributoAtual = (info as any).atributo_selecionado || DADOS_PERICIAS_FRONTEND[chavePericia.startsWith("Ofício") ? "Ofício" : chavePericia]?.atributo || "???";
        const podeTrocarAtributo = atributosPossiveis.length > 1;

        const chaveBase = chavePericia.startsWith("Ofício") ? "Ofício" : chavePericia;
        const meta = DADOS_PERICIAS_FRONTEND[chaveBase] || { atributo: "???", treino_apenas: false, penalidade_armadura: false };

        const isFixa = periciasFixas.includes(chavePericia);
        const isOrigem = periciasOrigem.includes(chavePericia);
        const isTreinada = info.treino > 0;

        const ehDaClasse = periciasDaClassePossiveis.includes(chavePericia) || chavePericia.startsWith("Ofício");
        const ehObrigatoria = periciasObrigatoriasSelecao.includes(chavePericia);

        const temSlotClasse = slotsClasseRestantes > 0;
        const temSlotInt = slotsInteligenciaRestantes > 0;

        let podeHabilitar = ehDaClasse ? (temSlotClasse || temSlotInt) : temSlotInt;
        if (isTravadoPelaObrigatoria && ehDaClasse && !ehObrigatoria) podeHabilitar = false;

        const isInteractable = (!isFixa && !isOrigem) && (isTreinada || podeHabilitar);
        const isDisabled = !isInteractable;
        const isObrigatoriaHighlight = ehObrigatoria;

        const nivel = Math.max(1, ficha.cabecalho.nivel_total || 1);
        const metadeNivel = Math.floor(nivel / 2);
        const attrVal = info.atributo_valor;
        const treinoVal = isTreinada ? (nivel >= 15 ? 6 : (nivel >= 7 ? 4 : 2)) : 0;

        // SOMA VISUAL DO CAMPO "OUTROS"
        const outrosExibicao = info.outros + bonusAuto;
        const totalVal = info.total;

        let rowBg = index % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent';
        if (isObrigatoriaHighlight && !cumpriuRequisitoObrigatorio) {
            rowBg = 'rgba(255, 193, 7, 0.1)';
        }

        return (
            <div key={chavePericia} className={`skill-row-grid ${isDisabled && !isFixa && !isOrigem ? 'disabled' : ''}`} style={{ background: rowBg }}>
                <div className="col-check" onClick={() => isInteractable && togglePericia(chavePericia)}>
                    <div className={`checkbox-box ${isTreinada ? 'checked' : ''} ${isFixa || isOrigem ? 'locked' : ''} ${isDisabled ? 'disabled-box' : ''}`}>
                        {isTreinada && "✔"}
                    </div>
                </div>
                <div className="col-name" onClick={() => isInteractable && togglePericia(chavePericia)}>
                    <span className={`name-text ${isTreinada ? 'trained-text' : ''} ${isDisabled ? 'disabled-text' : ''}`}>
                        {nomeExibicao}
                        {isObrigatoriaHighlight && <span style={{ color: '#ffc107', fontSize: '0.7em', marginLeft: 5 }}>★</span>}
                    </span>
                    <div className="icons-container">
                        {meta.treino_apenas && <span title="Somente Treinada" className="icon-badge star">✴️</span>}
                        {meta.penalidade_armadura && <span title="Penalidade de Armadura" className="icon-badge shield">🛡️</span>}
                        {isFixa && <span className="text-badge class">(C)</span>}
                        {isOrigem && <span className="text-badge origin">(O)</span>}
                    </div>
                </div>

                <div className="col-total tooltip-container">
                    <div className="total-box">{totalVal >= 0 ? `+${totalVal}` : totalVal}</div>

                    {/* TOOLTIP MELHORADO */}
                    <div className="pericia-tooltip">
                        <div className="tooltip-row"><span>1/2 do Nível</span><span>+{metadeNivel}</span></div>
                        <div className="tooltip-row">
                            <span>Atributo ({atributoAtual.toUpperCase()})</span>
                            <span>{attrVal >= 0 ? `+${attrVal}` : attrVal}</span>
                        </div>
                        <div className="tooltip-row"><span>Treino</span><span>+{treinoVal}</span></div>

                        {/* SEÇÃO DE OUTROS DETALHADA */}
                        <div style={{ marginTop: 5, borderTop: '1px dashed #444', paddingTop: 3 }}>
                            <div className="tooltip-row" style={{ color: outrosExibicao !== 0 ? '#4fc3f7' : '#ccc', fontWeight: 'bold' }}>
                                <span>Outros (Total)</span>
                                <span>{outrosExibicao >= 0 ? `+${outrosExibicao}` : outrosExibicao}</span>
                            </div>
                            {/* Detalhes */}
                            {info.outros !== 0 && (
                                <div className="tooltip-row source-row"><span>↳ Base (Manual)</span><span>{info.outros >= 0 ? `+${info.outros}` : info.outros}</span></div>
                            )}
                            {fontesBonus.map((fonte: string, idx: number) => (
                                <div key={idx} className="tooltip-row source-row">
                                    <span>↳ {fonte}</span>
                                </div>
                            ))}
                        </div>

                        <div className="tooltip-total"><span>Total</span><span>{totalVal >= 0 ? `+${totalVal}` : totalVal}</span></div>
                    </div>
                </div>

                <div className="col-equal">=</div>

                <div className="col-formula">
                    <span className="val-item">+{metadeNivel}</span><span className="plus">+</span>

                    {/* BOTÃO LIMPO (SÓ A SIGLA) */}
                    <div className="val-item attr-item"
                        onClick={(e) => {
                            if (podeTrocarAtributo) {
                                e.stopPropagation();
                                alternarAtributo(chavePericia, info);
                            }
                        }}
                        style={{
                            cursor: podeTrocarAtributo ? 'pointer' : 'default',
                            color: podeTrocarAtributo ? '#64b5f6' : '#999',
                            borderBottom: podeTrocarAtributo ? '1px dotted #64b5f6' : 'none',
                            fontWeight: podeTrocarAtributo ? 'bold' : 'normal'
                        }}
                        title={podeTrocarAtributo ? `Clique para alternar (Opções: ${atributosPossiveis.join(', ').toUpperCase()})` : ''}
                    >
                        <span>{atributoAtual.toUpperCase()}</span>
                    </div>

                    <span className="plus">+</span>
                    <span className="val-item">+{treinoVal}</span><span className="plus">+</span>

                    <span className="val-item" style={{ color: bonusAuto !== 0 ? '#4fc3f7' : '#999', fontWeight: bonusAuto !== 0 ? 'bold' : 'normal' }}>
                        {outrosExibicao >= 0 ? `+${outrosExibicao}` : outrosExibicao}
                    </span>
                </div>
            </div>
        );
    };

    const [novoOficio, setNovoOficio] = useState("");
    const adicionarOficio = () => {
        if (!novoOficio) return;
        const nomeCompleto = `Ofício (${novoOficio})`;
        if (!periciasTreinadas[nomeCompleto]) {
            togglePericia(nomeCompleto);
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
        <div className="section-card" style={{ padding: 0 }}>
            <div className="section-header" style={{ padding: '8px 12px', background: '#222', borderBottom: '1px solid #444', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ margin: 0, fontSize: '1rem', color: '#fff' }}>PERÍCIAS</h3>
                <div style={{ fontSize: '0.8rem', color: '#aaa', display: 'flex', gap: '15px' }}>
                    <span>Classe: <strong style={{ color: slotsClasseRestantes > 0 ? '#4caf50' : '#888' }}>{slotsClasseRestantes}</strong> / {qtdEscolhasClasse}</span>
                    <span>Inteligência: <strong style={{ color: slotsInteligenciaRestantes > 0 ? '#00bcd4' : '#888' }}>{slotsInteligenciaRestantes}</strong> / {qtdEscolhasInteligencia}</span>
                </div>
            </div>

            {!cumpriuRequisitoObrigatorio && periciasObrigatoriasSelecao.length > 0 && (
                <div style={{ background: 'rgba(255, 193, 7, 0.15)', borderBottom: '1px solid #ffc107', padding: '10px', textAlign: 'center' }}>
                    <p style={{ color: '#ffc107', margin: '0 0 8px 0', fontSize: '0.85rem', fontWeight: 'bold' }}>⚠️ Requisito de Classe: Escolha Luta ou Pontaria</p>
                    {isTravadoPelaObrigatoria && <p style={{ color: '#ff5252', fontSize: '0.75rem', marginTop: 4 }}>(Último slot reservado para obrigatória!)</p>}
                    <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 8 }}>
                        {periciasObrigatoriasSelecao.map((p: string) => (
                            <button key={p} onClick={() => togglePericia(p)} disabled={slotsClasseRestantes <= 0 && slotsInteligenciaRestantes <= 0}
                                style={{ background: '#ffc107', color: '#000', border: 'none', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold', fontSize: '0.8rem', opacity: (slotsClasseRestantes <= 0 && slotsInteligenciaRestantes <= 0) ? 0.5 : 1 }}>
                                {p}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* CABEÇALHO ALINHADO */}
            <div className="skill-header-grid">
                <div className="h-check"></div>
                <div className="h-name">PERÍCIA</div>
                <div className="h-total">TOTAL</div>
                <div className="h-equal"></div>
                {/* Mesma estrutura de flexbox e larguras da linha (col-formula) */}
                <div className="h-formula" style={{ display: 'flex', justifyContent: 'space-around', width: '100%' }}>
                    <span style={{ width: 25, textAlign: 'center' }}>1/2</span>
                    <span style={{ width: 8 }}></span>
                    <span style={{ width: 25, textAlign: 'center' }}>ATR</span>
                    <span style={{ width: 8 }}></span>
                    <span style={{ width: 25, textAlign: 'center' }}>TR</span>
                    <span style={{ width: 8 }}></span>
                    <span style={{ width: 25, textAlign: 'center' }}>OUT</span>
                </div>
            </div>

            <div className="skills-container" style={{ padding: '0 5px' }}>
                {listaExibicao.map((pericia, index) => renderSkillRow(pericia, pericia, index))}
            </div>

            <div className="add-skill-row" style={{ padding: '8px 12px', borderTop: '1px solid #333' }}>
                <input type="text" placeholder="Novo Ofício..." value={novoOficio} onChange={(e) => setNovoOficio(e.target.value)} />
                <button onClick={adicionarOficio}>+</button>
            </div>
            <style>{`
                .skill-row-grid, .skill-header-grid { display: grid; grid-template-columns: 22px 1fr 35px 10px 135px; align-items: center; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
                .skill-header-grid { font-size: 0.6rem; color: #888; font-weight: bold; border-bottom: 1px solid #444; padding: 5px 10px; text-transform: uppercase; letter-spacing: 0.5px; }
                
                .col-check { display: flex; justify-content: center; cursor: pointer; }
                .checkbox-box { width: 12px; height: 12px; border: 1px solid #555; border-radius: 2px; display: flex; align-items: center; justify-content: center; font-size: 9px; color: #000; background: #222; }
                .checkbox-box.checked { background: #ffd700; border-color: #ffd700; }
                .checkbox-box.locked { background: #4caf50; border-color: #4caf50; color: #fff; }
                .checkbox-box.disabled-box { background: #111; border-color: #333; opacity: 0.5; }

                .col-name { display: flex; align-items: center; padding-left: 5px; cursor: pointer; white-space: nowrap; overflow: hidden; }
                .name-text { font-size: 0.85rem; color: #ccc; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
                .name-text.trained-text { color: #fff; font-weight: 600; }
                .name-text.disabled-text { color: #555; }
                
                .icons-container { margin-left: 4px; display: flex; gap: 2px; flex-shrink: 0; }
                .icon-badge { font-size: 0.65rem; }
                .text-badge { font-size: 0.5rem; padding: 0 3px; border-radius: 2px; color:#000; font-weight:bold; }
                .text-badge.class { background: #4caf50; }
                .text-badge.origin { background: #2196f3; }

                .col-total { display: flex; justify-content: center; position: relative; cursor: help; }
                .total-box { width: 30px; height: 22px; border: 1px solid #444; background: #1a1a1a; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; color: #fff; border-radius: 3px; }

                .pericia-tooltip { visibility: hidden; opacity: 0; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%) translateY(0px); width: 220px; background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 6px; padding: 10px; z-index: 9999; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.9); transition: opacity 0.2s, transform 0.2s; pointer-events: none; }
                .col-total:hover .pericia-tooltip { visibility: visible; opacity: 1; transform: translateX(-50%) translateY(-10px); }
                .tooltip-row { display: flex; justify-content: space-between; font-size: 0.75rem; color: #ccc; margin-bottom: 3px; border-bottom: 1px dashed #333; }
                .tooltip-row.source-row { font-size: 0.7rem; color: #888; border-bottom: none; margin-bottom: 1px; padding-left: 5px; }
                .tooltip-total { border-top: 1px solid #fca311; margin-top: 5px; padding-top: 2px; font-weight: bold; color: #fca311; display: flex; justify-content: space-between; }

                .col-equal { text-align: center; color: #555; font-weight: bold; font-size: 0.8rem; }
                .col-formula { display: flex; justify-content: space-around; color: #666; font-family: monospace; font-size: 0.75rem; }
                .val-item { width: 25px; text-align: center; color: #999; display: inline-block; }
                .plus { width: 8px; text-align: center; color: #444; display: inline-block; }
                .val-item.attr-item { display: flex; flex-direction: column; align-items: center; justify-content: center; }

                .add-skill-row { display: flex; gap: 5px; }
                .add-skill-row input { flex: 1; padding: 4px 8px; background: #111; border: 1px solid #444; color: #fff; border-radius: 3px; font-size: 0.8rem; }
                .add-skill-row button { padding: 0 10px; background: #333; color: #fff; border: 1px solid #444; border-radius: 3px; cursor: pointer; }
            `}</style>
        </div>
    );
};