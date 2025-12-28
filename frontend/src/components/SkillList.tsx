import React, { useState } from 'react';
import type { Personagem } from '../types';
// Garanta que o caminho do arquivo de dados esteja correto
import { DADOS_PERICIAS_FRONTEND } from '../data/pericias';

interface SkillListProps {
    ficha: Personagem;
    dadosClasses: any;
    updateFicha: (dados: Partial<Personagem>) => void;
    listaTodasPericias: string[];
}

export const SkillList: React.FC<SkillListProps> = ({ ficha, dadosClasses, updateFicha, listaTodasPericias }) => {

    // --- 1. DADOS BASE ---
    const classePrincipal = ficha.classes[0]?.nome;
    const dadosClasse = dadosClasses[classePrincipal] || {};

    const periciasFixas = dadosClasse.pericias_iniciais || dadosClasse.pericias_fixas || [];
    const periciasEscolhaLista = dadosClasse.pericias_lista || [];
    const qtdEscolhasClasse = dadosClasse.pericias_escolha || 0;

    // Inteligência (Valor bruto ou modificador, dependendo de como seu backend retorna. 
    // Assumindo que ficha.atributos.inteligencia já é o modificador final +0, +2 etc)
    const intMod = Math.max(0, ficha.atributos.inteligencia || 0);

    const qtdTotalEscolhas = qtdEscolhasClasse + intMod;
    const periciasOrigem = ficha.escolhas_origem || [];
    const periciasTreinadas = ficha.pericias || {};

    // --- 2. CONTAGEM INTELIGENTE ---

    // Lista de todas as perícias que o jogador marcou manualmente (exclui fixas e origem)
    const periciasCompradas = Object.keys(periciasTreinadas).filter(p =>
        periciasTreinadas[p].treino > 0 &&
        !periciasFixas.includes(p) &&
        !periciasOrigem.includes(p)
    );

    const totalGastos = periciasCompradas.length;

    // Quantas dessas compradas NÃO pertencem à classe? (Gastam slots de INT)
    // Consideramos Ofícios como "da classe" para simplificar, ou regra geral.
    const gastosForaDaClasse = periciasCompradas.filter(p => {
        const ehDaClasse = periciasEscolhaLista.includes(p) || p.startsWith("Ofício");
        return !ehDaClasse;
    }).length;

    const slotsInteligenciaRestantes = Math.max(0, intMod - gastosForaDaClasse);
    const slotsTotaisRestantes = Math.max(0, qtdTotalEscolhas - totalGastos);

    // --- 3. LÓGICA DE TOGGLE ---
    const togglePericia = (pericia: string) => {
        // Bloqueia destreino de fixas
        if (periciasFixas.includes(pericia)) return;

        const novaLista = { ...periciasTreinadas };
        const estaTreinada = novaLista[pericia]?.treino > 0;

        if (estaTreinada) {
            // Destreinar (sempre permitido)
            novaLista[pericia] = { ...novaLista[pericia], treino: 0, total: 0 };
        } else {
            // Tentar Treinar

            // 1. Tem espaço total?
            if (totalGastos >= qtdTotalEscolhas) return;

            // 2. É da classe?
            const ehDaClasse = periciasEscolhaLista.includes(pericia) || pericia.startsWith("Ofício");

            // 3. Regra de Inteligência:
            // Se NÃO for da classe, preciso ter slot de inteligência sobrando.
            if (!ehDaClasse && slotsInteligenciaRestantes <= 0) {
                // Feedback visual ou sonoro poderia vir aqui
                console.log("Sem slots de inteligência para perícia fora da classe.");
                return;
            }

            // Aplica o treino
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

        // Verifica Disponibilidade
        const ehDaClasse = periciasEscolhaLista.includes(chavePericia) || chavePericia.startsWith("Ofício");

        // Pode clicar se:
        // 1. Já está treinada (para destreinar)
        // 2. É Fixa/Origem (mas a função toggle bloqueia a mudança, aqui só habilita o visual)
        // 3. Tem vaga total E (É da classe OU Tem vaga de Inteligência)
        const podeComprar = slotsTotaisRestantes > 0 && (ehDaClasse || slotsInteligenciaRestantes > 0);

        const isInteractable = isTreinada || (!isFixa && !isOrigem && podeComprar);
        const isDisabled = !isInteractable; // Visualmente desabilitado

        // Cálculos visuais
        const nivel = Math.max(1, ficha.cabecalho.nivel_total || 1);
        const metadeNivel = Math.floor(nivel / 2);
        const attrVal = info.atributo_valor;
        const treinoVal = isTreinada ? (nivel >= 15 ? 6 : (nivel >= 7 ? 4 : 2)) : 0;
        const outrosVal = info.outros;
        const totalVal = info.total;

        const rowBg = index % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent';

        return (
            <div key={chavePericia} className={`skill-row-grid ${isDisabled && !isFixa && !isOrigem ? 'disabled' : ''}`} style={{ background: rowBg }}>

                <div className="col-check" onClick={() => !isFixa && !isOrigem && togglePericia(chavePericia)}>
                    <div className={`checkbox-box ${isTreinada ? 'checked' : ''} ${isFixa || isOrigem ? 'locked' : ''}`}>
                        {isTreinada && "✔"}
                    </div>
                </div>

                <div className="col-name" onClick={() => !isFixa && !isOrigem && togglePericia(chavePericia)} title={nomeExibicao}>
                    <span className={`name-text ${isTreinada ? 'trained-text' : ''}`}>
                        {nomeExibicao}
                        {/* Indicador visual se foi comprada via INT */}
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

                <div className="col-total">
                    <div className="total-box">{totalVal >= 0 ? `+${totalVal}` : totalVal}</div>
                </div>

                <div className="col-equal">=</div>

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

    // --- OFÍCIOS ---
    const [novoOficio, setNovoOficio] = useState("");
    const adicionarOficio = () => {
        if (!novoOficio) return;
        const nomeCompleto = `Ofício (${novoOficio})`;
        if (!periciasTreinadas[nomeCompleto]) {
            // Ofícios contam como perícia de classe, então só checa slots totais
            if (slotsTotaisRestantes > 0) {
                const novaLista = { ...periciasTreinadas };
                novaLista[nomeCompleto] = { treino: 1, bonus_nivel: 0, atributo_valor: 0, outros: 0, total: 0 };
                updateFicha({ pericias: novaLista });
            } else {
                // Pode adicionar destreinado se quiser, mas aqui vamos assumir que quer treinar
                const novaLista = { ...periciasTreinadas };
                novaLista[nomeCompleto] = { treino: 0, bonus_nivel: 0, atributo_valor: 0, outros: 0, total: 0 };
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
        <div className="section-card" style={{ padding: 0, overflow: 'hidden' }}>
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
                        Total Restante: <strong style={{ color: slotsTotaisRestantes > 0 ? '#4caf50' : '#f44336' }}>{slotsTotaisRestantes}</strong>
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
                /* Mantendo o estilo Grid que ajustamos anteriormente */
                .skill-row-grid, .skill-header-grid {
                    display: grid;
                    grid-template-columns: 22px 1fr 35px 10px 135px; /* Compactado para dar espaço ao nome */
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

                .col-total { display: flex; justify-content: center; }
                .total-box {
                    width: 30px; height: 22px; border: 1px solid #444; background: #1a1a1a;
                    display: flex; align-items: center; justify-content: center;
                    font-weight: bold; font-size: 0.9rem; color: #fff; border-radius: 3px;
                }

                .col-equal { text-align: center; color: #555; font-weight: bold; font-size: 0.8rem; }

                .col-formula, .h-formula {
                    display: flex; justify-content: space-around; 
                    color: #666; font-family: monospace; font-size: 0.75rem;
                }
                
                .val-item { width: 25px; text-align: center; color: #999; display: inline-block; }
                .plus { width: 8px; text-align: center; color: #444; display: inline-block; }
                .h-formula span { text-align: center; display: inline-block; }

                .val-item.attr-item {
                    display: flex; flex-direction: column; align-items: center; line-height: 0.8;
                }
                .attr-item span { color: #eee; }
                .attr-item small { font-size: 0.5rem; color: #555; margin-top: 1px; }

                .skill-row-grid.disabled { opacity: 0.3; pointer-events: none; }

                .add-skill-row { display: flex; gap: 5px; }
                .add-skill-row input {
                    flex: 1; padding: 4px 8px; background: #111; border: 1px solid #444; 
                    color: #fff; border-radius: 3px; font-size: 0.8rem;
                }
                .add-skill-row button {
                    padding: 0 10px; background: #333; color: #fff; border: 1px solid #444; 
                    border-radius: 3px; cursor: pointer; font-size: 1.1rem; line-height: 1;
                }
                .add-skill-row button:hover { background: #444; border-color: #555; }
            `}</style>
        </div>
    );
};