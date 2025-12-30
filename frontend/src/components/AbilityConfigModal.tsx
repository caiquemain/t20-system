import React, { useState, useEffect } from 'react';
import '../Ficha.css';

interface AbilityConfigModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: () => void;

    ficha: any;
    origemNome: string;
    qtdEscolhasOrigem: number;
    listaBeneficiosOrigem?: string[];

    classeAtual: string;
    nivelAtual: number;
    dadosHabilidadesClasse: any;

    // Dados para Filtros
    listaPoderesGerais: any[];
    dadosDeuses: any;
    dadosMagias: any;

    // Estados de Edição
    origemBeneficiosEmEdicao: string[];
    setOrigemBeneficiosEmEdicao: (vals: string[]) => void;

    habilidadesEmEdicao: any[];
    setHabilidadesEmEdicao: (vals: any[]) => void;

    classPowersEmEdicao?: string[];
    setClassPowersEmEdicao: React.Dispatch<React.SetStateAction<string[]>>;

    // Subclasse e Devoção
    subclasseEmEdicao: string;
    setSubclasseEmEdicao: (val: string) => void;
    devocaoEmEdicao: string;
    setDevocaoEmEdicao: (val: string) => void;

    abrirSeletor: (
        tipo: string,
        titulo: string,
        listaRestrita?: string[],
        categoriaFixa?: string,
        onConfirm?: (val: string) => void,
        itensBloqueados?: string[]
    ) => void;
}

export const AbilityConfigModal: React.FC<AbilityConfigModalProps> = ({
    isOpen, onClose, onSave,
    ficha, origemNome, qtdEscolhasOrigem, listaBeneficiosOrigem = [],
    classeAtual, nivelAtual, dadosHabilidadesClasse,
    listaPoderesGerais = [], dadosDeuses = {}, dadosMagias = {},
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao,
    subclasseEmEdicao, setSubclasseEmEdicao,
    devocaoEmEdicao, setDevocaoEmEdicao,
    abrirSeletor
}) => {

    const [modosSlot2, setModosSlot2] = useState<Record<number, 'pericia' | 'poder'>>({});

    // --- LOGS DE DEBUG NO CONSOLE (MANTIDOS) ---
    useEffect(() => {
        if (isOpen) {
            console.group("🔍 DEBUG: AbilityConfigModal ABERTO");
            console.log("1. Habilidades Recebidas:", habilidadesEmEdicao);
            const magiasQtd = dadosMagias ? Object.keys(dadosMagias).length : 0;
            console.log(`2. Total de Magias no Banco: ${magiasQtd}`);
            console.groupEnd();
        }
    }, [isOpen, habilidadesEmEdicao, dadosMagias]);

    if (!isOpen) return null;

    // --- PREPARAÇÃO DE DADOS ---
    // Filtra magias de 1º círculo para o Qareen
    const magiasCirculo1 = Object.values(dadosMagias || {})
        // @ts-ignore
        .filter((m: any) => m.circulo === 1 || m.circulo === '1')
        // @ts-ignore
        .map((m: any) => m.nome)
        .sort();

    // --- FUNÇÃO CENTRAL DE BLOQUEIO (Evita duplicatas) ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();
        // Bloqueia perícias já treinadas
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => {
                if (info.treino > 0) blocked.add(nome);
            });
        }
        // Bloqueia devoção atual
        if (devocaoEmEdicao && devocaoEmEdicao !== ignorarValor) blocked.add(devocaoEmEdicao);
        // Bloqueia origens já escolhidas
        origemBeneficiosEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });
        // Bloqueia escolhas raciais
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) {
                Object.values(hab.escolhas_aplicadas).forEach((val: any) => {
                    if (val && val !== ignorarValor) blocked.add(val);
                });
            }
        });
        // Bloqueia poderes de classe
        classPowersEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });
        return Array.from(blocked);
    };

    // --- DADOS ---
    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});
    const habilidadesAutomaticas = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);
    const poderesDaClasse = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo.includes("Poder de"));

    const deusAtual = ficha.cabecalho.deus;
    const poderesDoMeuDeus = (deusAtual && dadosDeuses[deusAtual]) ? dadosDeuses[deusAtual].poderes : [];
    const poderesGeraisFiltrados = listaPoderesGerais.filter((p: any) => {
        if (p.categoria === 'Poder Concedido') return poderesDoMeuDeus.includes(p.nome);
        if (p.categoria === 'Origem') return false;
        return true;
    });
    const nomesPoderesDisponiveis = Array.from(new Set([
        ...poderesDaClasse.map((p: any) => p.nome),
        ...poderesGeraisFiltrados.map((p: any) => p.nome)
    ])).sort();
    const slotsPoderes = Math.max(0, nivelAtual - 1);

    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];
    const infoDeus = dadosDeuses[deusAtual];

    const updateRacialChoice = (index: number, key: string, value: string) => {
        console.log(`📝 Update Racial [${index}]: ${key} = ${value}`);
        const novos = [...habilidadesEmEdicao];
        if (!novos[index].escolhas_aplicadas) novos[index].escolhas_aplicadas = {};
        novos[index].escolhas_aplicadas = { ...novos[index].escolhas_aplicadas, [key]: value };
        setHabilidadesEmEdicao(novos);
    };

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content">
                <button className="btn-close-panel" onClick={onClose}>X</button>
                <h2>⚙️ Configuração de Personagem</h2>
                <hr />

                {/* --- SEÇÃO: SUBCLASSE --- */}
                {opcoesSubclasse.length > 0 && habilidadeComSubclasse && (
                    <div style={{ marginBottom: 20, padding: 15, background: '#253b50', borderRadius: 6, border: '1px solid #64b5f6' }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>{habilidadeComSubclasse.nome}</h3>
                        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                            {opcoesSubclasse.map(opcao => (
                                <button key={opcao} onClick={() => setSubclasseEmEdicao(opcao)}
                                    className={`btn-action ${subclasseEmEdicao === opcao ? 'selected' : ''}`}
                                    style={{ flex: 1, background: subclasseEmEdicao === opcao ? '#4caf50' : '#333', border: subclasseEmEdicao === opcao ? '1px solid #fff' : '1px solid #555', color: 'white' }}>
                                    {opcao}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* --- SEÇÃO: DEVOÇÃO --- */}
                {deusAtual && infoDeus && (
                    <div className="origem-box" style={{ borderColor: '#ffd700', background: '#2a2a20', marginBottom: 20 }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#ffd700' }}>Devoção: {deusAtual}</h3>
                        <div style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label>Poder Concedido:</label>
                            <input value={devocaoEmEdicao} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                            <button onClick={() => abrirSeletor('poder', `Poderes de ${deusAtual}`, infoDeus.poderes, undefined, (val) => setDevocaoEmEdicao(val), [])}
                                className="btn-action" style={{ background: '#ffd700', color: 'black' }}>Selecionar</button>
                        </div>
                    </div>
                )}

                {/* --- SEÇÃO: ORIGEM (Restaurada) --- */}
                {(() => {
                    // Verifica se alguma habilidade racial proíbe origem (ex: Golem)
                    const bloqueioOrigem = habilidadesEmEdicao.find(h => h.efeitos && h.efeitos.sem_origem);

                    if (bloqueioOrigem) {
                        return (
                            <>
                                <h3 className="section-subtitle">Benefícios de Origem</h3>
                                <div className="origem-box" style={{ border: '1px dashed #d32f2f', background: 'rgba(211, 47, 47, 0.1)' }}>
                                    <p style={{ color: '#ff8a80', margin: 0, display: 'flex', alignItems: 'center', gap: 10 }}>
                                        🚫 <strong>Origem Bloqueada:</strong> {bloqueioOrigem.nome}
                                    </p>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', marginTop: 5 }}>
                                        Esta raça não recebe benefícios de origem.
                                    </p>
                                </div>
                            </>
                        );
                    }

                    // Se não tiver bloqueio, mostra os seletores
                    return (
                        <>
                            <h3 className="section-subtitle">Benefícios de Origem ({origemNome})</h3>
                            <div className="origem-box">
                                <p style={{ color: '#aaa', fontSize: '0.9rem', marginBottom: 10 }}>Escolha {qtdEscolhasOrigem} benefícios.</p>
                                {[...Array(qtdEscolhasOrigem)].map((_, i) => {
                                    const valorAtual = origemBeneficiosEmEdicao[i] || '';
                                    const blocked = getBlacklistGlobal(valorAtual);

                                    // Filtra a lista de benefícios permitidos pela Origem
                                    const opcoes = listaBeneficiosOrigem.filter(opt => !blocked.includes(opt) || opt === valorAtual);

                                    return (
                                        <div key={i} style={{ marginBottom: 10, display: 'flex', gap: 10 }}>
                                            <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                            <button onClick={() => abrirSeletor('ambos', `Origem #${i + 1}`, opcoes, undefined, (val) => {
                                                const n = [...origemBeneficiosEmEdicao];
                                                n[i] = val;
                                                setOrigemBeneficiosEmEdicao(n);
                                            }, blocked)} className="btn-action">Selecionar</button>
                                        </div>
                                    );
                                })}
                            </div>
                        </>
                    );
                })()}

                {/* --- SEÇÃO: RACIAIS --- */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Habilidades Raciais</h3>
                <div className="habilidades-list-wrapper">
                    {habilidadesEmEdicao.map((hab, idx) => {

                        // --- CASO 1: HUMANO (VERSÁTIL) ---
                        if (hab.nome === "Versátil") {
                            const p1 = hab.escolhas_aplicadas?.pericia_1 || "";
                            const p2 = hab.escolhas_aplicadas?.pericia_2 || "";
                            const pg = hab.escolhas_aplicadas?.poder_geral || "";
                            const modoAtual = pg ? 'poder' : (modosSlot2[idx] || 'pericia');

                            const toggleModo = (novoModo: 'pericia' | 'poder') => {
                                setModosSlot2(prev => ({ ...prev, [idx]: novoModo }));
                                const novos = [...habilidadesEmEdicao];
                                const novasEscolhas = { ...novos[idx].escolhas_aplicadas };
                                if (novoModo === 'pericia') { delete novasEscolhas.poder_geral; novasEscolhas.pericia_2 = ""; }
                                else { delete novasEscolhas.pericia_2; novasEscolhas.poder_geral = ""; }
                                novos[idx].escolhas_aplicadas = novasEscolhas;
                                setHabilidadesEmEdicao(novos);
                            };

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Humano)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', fontStyle: 'italic' }}>Escolha 2 Perícias <strong>OU</strong> 1 Perícia e 1 Poder Geral.</p>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 15, marginTop: 10 }}>
                                        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                            <label style={{ width: 90, fontSize: '0.85rem', color: '#81c784' }}>Perícia Fixa:</label>
                                            <input value={p1} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione uma perícia..." />
                                            <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Versátil: Perícia Fixa', [], undefined, (v) => updateRacialChoice(idx, 'pericia_1', v), getBlacklistGlobal(p1))}>Escolher</button>
                                        </div>
                                        <div style={{ padding: 10, border: '1px dashed #555', borderRadius: 4, background: 'rgba(255,255,255,0.02)' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                                                <label style={{ fontSize: '0.85rem', color: '#ffd700' }}>Segundo Slot:</label>
                                                <div style={{ display: 'flex', gap: 5 }}>
                                                    <button onClick={() => toggleModo('pericia')} style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'pericia' ? '#00bcd4' : '#333', color: modoAtual === 'pericia' ? '#000' : '#888', border: '1px solid #555', borderRadius: 3 }}>Perícia</button>
                                                    <button onClick={() => toggleModo('poder')} style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'poder' ? '#9c27b0' : '#333', color: modoAtual === 'poder' ? '#fff' : '#888', border: '1px solid #555', borderRadius: 3 }}>Poder Geral</button>
                                                </div>
                                            </div>
                                            {modoAtual === 'pericia' ? (
                                                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                                    <input value={p2} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione a 2ª perícia..." />
                                                    <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Versátil: 2ª Perícia', [], undefined, (v) => updateRacialChoice(idx, 'pericia_2', v), getBlacklistGlobal(p2))}>Escolher</button>
                                                </div>
                                            ) : (
                                                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                                    <input value={pg} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione um poder..." />
                                                    <button className="btn-action" style={{ background: '#9c27b0' }} onClick={() => abrirSeletor('poder', 'Versátil: Poder Geral', [], undefined, (v) => updateRacialChoice(idx, 'poder_geral', v), getBlacklistGlobal(pg))}>Escolher</button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 2: QAREEN (TATUAGEM MÍSTICA) ---
                        if (hab.nome.normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes("Tatuagem")) {
                            const escolhaObj = hab.escolhas_aplicadas || {};
                            const magiaAtual = escolhaObj.magia_escolhida || escolhaObj.magia_escolha || "";

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Qareen)</span>
                                        <span style={{ color: '#e040fb', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', fontStyle: 'italic' }}>
                                        Você aprende uma magia de 1º círculo (Arcana ou Divina).
                                    </p>

                                    <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 10 }}>
                                        <label style={{ fontSize: '0.85rem', color: '#ce93d8' }}>Magia:</label>
                                        <input value={magiaAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione a magia..." />
                                        <button
                                            className="btn-action"
                                            style={{ background: '#9c27b0', color: 'white' }}
                                            onClick={() => abrirSeletor(
                                                'poder', // Modo 'poder' para listar lista simples
                                                'Tatuagem Mística: Escolha uma Magia',
                                                magiasCirculo1,
                                                undefined,
                                                (v) => updateRacialChoice(idx, 'magia_escolhida', v),
                                                [magiaAtual]
                                            )}
                                        >
                                            Escolher Magia
                                        </button>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 3: QAREEN (RESISTÊNCIA) ---
                        const keyRd = Object.keys(hab.efeitos).find(k => k === 'resistencia_rd_escolha');
                        if (keyRd) {
                            const valorAtual = hab.escolhas_aplicadas?.[keyRd] || "";
                            const listaElementos = ["Ácido", "Eletricidade", "Fogo", "Frio", "Luz", "Trevas"];
                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Qareen)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc' }}>Escolha sua ascendência para receber Resistência 10.</p>
                                    <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 10 }}>
                                        <label style={{ width: 90, fontSize: '0.85rem', color: '#ff5722' }}>Elemento:</label>
                                        <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                        <button className="btn-action" style={{ background: '#ff5722' }} onClick={() => abrirSeletor('ambos', 'Ascendência Qareen', listaElementos, undefined, (val) => updateRacialChoice(idx, keyRd, val))}>Escolher</button>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 4: LEFOU (DEFORMIDADE) ---
                        if (hab.nome === "Deformidade") {
                            const p1 = hab.escolhas_aplicadas?.pericia_1 || "";
                            const p2 = hab.escolhas_aplicadas?.pericia_2 || "";
                            const pTormenta = hab.escolhas_aplicadas?.poder_tormenta || "";
                            const modoAtual = pTormenta ? 'poder' : (modosSlot2[idx] || 'pericia');

                            const toggleModo = (novoModo: 'pericia' | 'poder') => {
                                setModosSlot2(prev => ({ ...prev, [idx]: novoModo }));
                                const novos = [...habilidadesEmEdicao];
                                const novasEscolhas = { ...novos[idx].escolhas_aplicadas };
                                if (novoModo === 'pericia') { delete novasEscolhas.poder_tormenta; novasEscolhas.pericia_2 = ""; }
                                else { delete novasEscolhas.pericia_2; novasEscolhas.poder_tormenta = ""; }
                                novos[idx].escolhas_aplicadas = novasEscolhas;
                                setHabilidadesEmEdicao(novos);
                            };

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Lefou)</span>
                                        <span style={{ color: '#d32f2f', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 15, marginTop: 10 }}>
                                        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                            <label style={{ width: 90, fontSize: '0.85rem', color: '#81c784' }}>Perícia (+2):</label>
                                            <input value={p1} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                            <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Deformidade: Bônus em Perícia', [], undefined, (v) => updateRacialChoice(idx, 'pericia_1', v), getBlacklistGlobal(p1))}>Escolher</button>
                                        </div>
                                        {/* Slot 2 */}
                                        <div style={{ padding: 10, border: '1px dashed #555', borderRadius: 4, background: 'rgba(255,0,0,0.05)' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                                                <label style={{ fontSize: '0.85rem', color: '#ff5252' }}>Segundo Slot:</label>
                                                <div style={{ display: 'flex', gap: 5 }}>
                                                    <button onClick={() => toggleModo('pericia')} style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'pericia' ? '#00bcd4' : '#333', color: modoAtual === 'pericia' ? '#000' : '#888', border: '1px solid #555', borderRadius: 3 }}>Perícia (+2)</button>
                                                    <button onClick={() => toggleModo('poder')} style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'poder' ? '#d32f2f' : '#333', color: modoAtual === 'poder' ? '#fff' : '#888', border: '1px solid #555', borderRadius: 3 }}>Poder da Tormenta</button>
                                                </div>
                                            </div>
                                            {modoAtual === 'pericia' ? (
                                                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                                    <input value={p2} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                                    <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Deformidade: Bônus em Perícia', [], undefined, (v) => updateRacialChoice(idx, 'pericia_2', v), getBlacklistGlobal(p2))}>Escolher</button>
                                                </div>
                                            ) : (
                                                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                                    <input value={pTormenta} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione um Poder..." />
                                                    <button className="btn-action" style={{ background: '#d32f2f', color: 'white' }} onClick={() => abrirSeletor('poder', 'Deformidade: Poder da Tormenta', [], 'Tormenta', (v) => updateRacialChoice(idx, 'poder_tormenta', v), getBlacklistGlobal(pTormenta))}>Escolher</button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 5: GENÉRICO (SEREIA, GOLEM, SÍLFIDE...) ---
                        return (
                            <div key={idx} className="habilidade-item" style={{ marginBottom: 10, paddingBottom: 10, borderBottom: '1px solid #333' }}>
                                <div className="hab-header">
                                    <span><strong>{hab.nome}</strong></span>
                                    {hab.precisaEscolha && <span style={{ color: '#ffeb3b', fontSize: '0.8rem' }}>CONFIGURAR</span>}
                                </div>
                                {hab.precisaEscolha && (
                                    <div className="hab-config" style={{ marginTop: 10 }}>
                                        {Object.entries(hab.efeitos).map(([keyEffect, _]) => {
                                            if (keyEffect.endsWith('_escolha') && !keyEffect.includes('magia_adicional') && !keyEffect.includes('imunidade_dano')) {
                                                const valorAtual = hab.escolhas_aplicadas?.[keyEffect] || '';
                                                const blocked = getBlacklistGlobal(valorAtual);
                                                let tipoSeletor = 'pericia'; let label = 'Perícia';

                                                if (keyEffect.includes('pericia_ou_poder')) { tipoSeletor = 'ambos'; label = 'Perícia ou Poder'; }
                                                else if (keyEffect.includes('poder')) { tipoSeletor = 'poder'; label = 'Poder'; if (keyEffect.includes('tormenta')) label = 'Poder da Tormenta'; }

                                                return (
                                                    <div key={keyEffect} style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 5 }}>
                                                        <label style={{ fontSize: '0.8rem', color: '#aaa' }}>{label}:</label>
                                                        <div style={{ display: 'flex', gap: 10 }}>
                                                            <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecionar..." />
                                                            <button onClick={() => abrirSeletor(tipoSeletor, `Escolha para ${hab.nome}`, [], keyEffect.includes('tormenta') ? 'Tormenta' : undefined, (v) => {
                                                                updateRacialChoice(idx, keyEffect, v);
                                                            }, blocked)} className="btn-action" style={{ background: '#2196f3', border: 'none', color: 'white' }}>Escolher</button>
                                                        </div>
                                                    </div>
                                                );
                                            }
                                            return null;
                                        })}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* --- SEÇÃO: CLASSE AUTOMÁTICA --- */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Habilidades de Classe (Fixas)</h3>
                <div className="lista-automatica">
                    {habilidadesAutomaticas.map((hab: any) => (
                        <div key={hab.nome} className="item-auto" style={{ marginBottom: 10, paddingBottom: 10, borderBottom: '1px dashed #444' }}>
                            <span className="item-nome" style={{ fontWeight: 'bold', color: '#81c784' }}>{hab.nome}</span>
                            <span className="item-nivel" style={{ float: 'right', fontSize: '0.8rem', color: '#666' }}>Nível {hab.nivel}</span>
                            <p className="item-desc" style={{ margin: '5px 0', color: '#ccc', fontSize: '0.9rem' }}>{hab.descricao}</p>
                        </div>
                    ))}
                    {habilidadesAutomaticas.length === 0 && <p className="text-muted">Nenhuma habilidade automática neste nível.</p>}
                </div>

                {/* --- SEÇÃO: PODERES DE CLASSE + GERAIS (SLOTS) --- */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>
                    Poderes ({classPowersEmEdicao.length}/{slotsPoderes})
                </h3>

                {slotsPoderes > 0 ? (
                    <div className="powers-slots-container">
                        {[...Array(slotsPoderes)].map((_, i) => {
                            const valorAtual = classPowersEmEdicao[i] || "";
                            const blocked = getBlacklistGlobal(valorAtual);
                            return (
                                <div key={i} className="power-slot-row" style={{ marginBottom: 10, display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <div style={{ width: '25px', color: '#666', fontSize: '0.8rem', textAlign: 'right' }}>{i + 2}º</div>
                                    <input value={valorAtual} readOnly className="input-dark" placeholder="Selecionar Poder..." style={{ flex: 1 }} />
                                    <button onClick={() => abrirSeletor('poder', `Poder de Nível ${i + 2}`, nomesPoderesDisponiveis, undefined, (v) => {
                                        const novosPoderes = [...classPowersEmEdicao];
                                        while (novosPoderes.length <= i) novosPoderes.push("");
                                        novosPoderes[i] = v;
                                        setClassPowersEmEdicao(novosPoderes);
                                    }, blocked)} className="btn-action" style={{ background: valorAtual ? '#4caf50' : '#2196f3', border: 'none', color: 'white' }}>{valorAtual ? 'Trocar' : 'Escolher'}</button>
                                </div>
                            );
                        })}
                    </div>
                ) : <p className="text-muted">Disponível no nível 2.</p>}

                <button className="btn-apply-changes" onClick={onSave} style={{ marginTop: 30 }}>✅ Salvar Todas as Alterações</button>
            </div>
        </div>
    );
};