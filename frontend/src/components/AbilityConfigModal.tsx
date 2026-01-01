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
    dadosOrigens?: any; // Novo: Recebe dados das origens para listar os poderes

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
    listaPoderesGerais = [], dadosDeuses = {}, dadosMagias = {}, dadosOrigens = {},
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao,
    subclasseEmEdicao, setSubclasseEmEdicao,
    devocaoEmEdicao, setDevocaoEmEdicao,
    abrirSeletor
}) => {

    // --- 1. HOOKS (Sempre no topo) ---
    const [modosSlot2, setModosSlot2] = useState<Record<number, 'pericia' | 'poder'>>({});

    // Logs de Debug
    useEffect(() => {
        if (isOpen) {
            console.group("🔍 DEBUG: AbilityConfigModal ABERTO");
            console.log("1. Habilidades Recebidas:", habilidadesEmEdicao);
            console.log("2. Origens Disponíveis:", Object.keys(dadosOrigens).length);
            console.groupEnd();
        }
    }, [isOpen, habilidadesEmEdicao, dadosMagias, dadosOrigens]);

    if (!isOpen) return null;

    // --- FUNÇÃO CENTRAL DE BLOQUEIO (Evita duplicatas) ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => {
                if (info.treino > 0) blocked.add(nome);
            });
        }
        if (devocaoEmEdicao && devocaoEmEdicao !== ignorarValor) blocked.add(devocaoEmEdicao);
        origemBeneficiosEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) {
                Object.values(hab.escolhas_aplicadas).forEach((val: any) => {
                    if (val && val !== ignorarValor) blocked.add(val);
                });
            }
        });
        classPowersEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });
        return Array.from(blocked);
    };

    // --- DADOS E FILTROS ---
    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});
    const habilidadesAutomaticas = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);
    const poderesDaClasse = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo.includes("Poder de"));

    const deusAtual = ficha.cabecalho.deus;
    const poderesDoMeuDeus = (deusAtual && dadosDeuses[deusAtual]) ? dadosDeuses[deusAtual].poderes : [];

    // --- FILTRO PRINCIPAL DE PODERES GERAIS ---
    // Remove Poderes Concedidos (que não sejam do meu deus), Origens e Raciais
    const poderesGeraisFiltrados = listaPoderesGerais.filter((p: any) => {
        const t = (p.tipo || p.categoria || "").toString();

        // Se for Poder Concedido, só mostra se for do meu Deus
        if (t.includes('Concedido')) return poderesDoMeuDeus.includes(p.nome);

        // Remove Origens da lista de compra de nível (pois geralmente se compra Poder Geral)
        if (t.includes('Origem')) return false;

        // Remove Habilidades Raciais
        if (t.includes('Raça') || t.includes('Racial')) return false;

        return true;
    });

    // Lista unificada para os slots de nível (combina classe + gerais filtrados)
    const nomesPoderesDisponiveis = Array.from(new Set([
        ...poderesDaClasse.map((p: any) => p.nome),
        ...poderesGeraisFiltrados.map((p: any) => p.nome)
    ])).sort();

    const slotsPoderes = Math.max(0, nivelAtual - 1);

    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];
    const infoDeus = dadosDeuses[deusAtual];

    const updateRacialChoice = (index: number, key: string, value: string) => {
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

                {/* --- SEÇÃO: ORIGEM --- */}
                {(() => {
                    const bloqueioOrigem = habilidadesEmEdicao.find(h => h.efeitos && h.efeitos.sem_origem);
                    if (bloqueioOrigem) {
                        return (
                            <>
                                <h3 className="section-subtitle">Benefícios de Origem</h3>
                                <div className="origem-box" style={{ border: '1px dashed #d32f2f', background: 'rgba(211, 47, 47, 0.1)' }}>
                                    <p style={{ color: '#ff8a80', margin: 0, display: 'flex', alignItems: 'center', gap: 10 }}>
                                        🚫 <strong>Origem Bloqueada:</strong> {bloqueioOrigem.nome}
                                    </p>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', marginTop: 5 }}>Esta raça não recebe benefícios de origem.</p>
                                </div>
                            </>
                        );
                    }
                    return (
                        <>
                            <h3 className="section-subtitle">Benefícios de Origem ({origemNome})</h3>
                            <div className="origem-box">
                                <p style={{ color: '#aaa', fontSize: '0.9rem', marginBottom: 10 }}>Escolha {qtdEscolhasOrigem} benefícios.</p>
                                {[...Array(qtdEscolhasOrigem)].map((_, i) => {
                                    const valorAtual = origemBeneficiosEmEdicao[i] || '';
                                    const blocked = getBlacklistGlobal(valorAtual);
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
                                                    <button
                                                        className="btn-action"
                                                        style={{ background: '#9c27b0' }}
                                                        onClick={() => abrirSeletor(
                                                            'poder',
                                                            'Versátil: Poder Geral',
                                                            poderesGeraisFiltrados.map((p: any) => p.nome),
                                                            undefined,
                                                            (v) => updateRacialChoice(idx, 'poder_geral', v),
                                                            getBlacklistGlobal(pg)
                                                        )}
                                                    >
                                                        Escolher
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 2: AMBIÇÃO HERDADA (MEIO-ELFO) [CORRIGIDO] ---
                        const efeitosAmbicao = hab.efeitos || {};
                        const escolhasAmbicao = hab.escolhas_aplicadas || {};

                        if (efeitosAmbicao.poder_geral_ou_origem) {
                            const qtd = efeitosAmbicao.poder_geral_ou_origem;
                            const slots = Array.from({ length: qtd });

                            // LÓGICA ROBUSTA: Junta Poderes Gerais + TODOS Poderes de Origem disponíveis nos dados
                            const nomesGerais = listaPoderesGerais.filter(p => {
                                const t = (p.tipo || p.categoria || "").toString();
                                const allow = ["Geral", "Combate", "Destino", "Magia", "Tormenta"];
                                const deny = ["Racial", "Concedido", "Classe", "Deus", "Origem"]; // Exclui origem aqui para evitar duplicatas, adicionamos explicitamente abaixo
                                return allow.some(k => t.includes(k)) && !deny.some(k => t.includes(k));
                            }).map(p => p.nome);

                            // Extrai TODOS os benefícios de origem conhecidos pelo sistema
                            const nomesOrigem = dadosOrigens
                                ? Object.values(dadosOrigens).flatMap((o: any) => o.beneficios_lista || [])
                                // @ts-ignore
                                : [];

                            // Unifica e remove duplicatas
                            const listaCombinada = Array.from(new Set([...nomesGerais, ...nomesOrigem])).sort();

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Meio-Elfo)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', marginBottom: 10 }}>
                                        Escolha {qtd} Poder(es) Geral(is) ou de Origem.
                                    </p>

                                    {slots.map((_, i) => {
                                        const chaveSalva = `poder_ambicao_${i}`;
                                        const valorAtual = escolhasAmbicao[chaveSalva] || "";

                                        return (
                                            <div key={i} style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                                                <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                                <button
                                                    className="btn-action"
                                                    onClick={() => abrirSeletor(
                                                        'poder',
                                                        `Ambição Herdada #${i + 1}`,
                                                        listaCombinada, // <--- Lista Completa
                                                        undefined,
                                                        (val) => {
                                                            const novos = [...habilidadesEmEdicao];
                                                            if (!novos[idx].escolhas_aplicadas) novos[idx].escolhas_aplicadas = {};
                                                            novos[idx].escolhas_aplicadas[chaveSalva] = val;
                                                            setHabilidadesEmEdicao(novos);
                                                        },
                                                        getBlacklistGlobal(valorAtual)
                                                    )}
                                                >
                                                    Escolher
                                                </button>
                                            </div>
                                        );
                                    })}
                                </div>
                            );
                        }

                        // --- CASO 3: MAGIAS ADICIONAIS ---
                        const configMagia = hab.efeitos?.magia_adicional_escolha;
                        if (configMagia) {
                            const quantidade = configMagia.quantidade || 1;
                            const listaFixa = configMagia.lista || [];
                            const circulo = configMagia.circulo || 1;

                            let opcoesMagias = listaFixa;
                            if (opcoesMagias.length === 0 && dadosMagias) {
                                opcoesMagias = Object.values(dadosMagias)
                                    // @ts-ignore
                                    .filter((m: any) => String(m.circulo) === String(circulo))
                                    // @ts-ignore
                                    .map((m: any) => m.nome)
                                    .sort();
                            }

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong></span>
                                        <span style={{ color: '#e040fb', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', fontStyle: 'italic' }}>
                                        {listaFixa.length > 0
                                            ? `Escolha ${quantidade} magia(s) da lista permitida.`
                                            : `Escolha ${quantidade} magia(s) de ${circulo}º círculo.`}
                                    </p>

                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 10 }}>
                                        {[...Array(quantidade)].map((_, i) => {
                                            const keyStore = quantidade > 1 ? `magia_${i}` : `magia_escolhida`;
                                            const magiaAtual = hab.escolhas_aplicadas?.[keyStore] || "";

                                            return (
                                                <div key={i} style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                                    <label style={{ fontSize: '0.85rem', color: '#ce93d8', minWidth: 60 }}>Magia {quantidade > 1 ? i + 1 : ''}:</label>
                                                    <input value={magiaAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione a magia..." />
                                                    <button
                                                        className="btn-action"
                                                        style={{ background: '#9c27b0', color: 'white' }}
                                                        onClick={() => abrirSeletor(
                                                            'poder',
                                                            `Escolha a Magia ${quantidade > 1 ? i + 1 : ''}`,
                                                            opcoesMagias,
                                                            undefined,
                                                            (v) => updateRacialChoice(idx, keyStore, v),
                                                            [magiaAtual]
                                                        )}
                                                    >
                                                        Escolher
                                                    </button>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 4: QAREEN (RESISTÊNCIA) ---
                        const keyRd = hab.efeitos && Object.keys(hab.efeitos).find(k => k === 'resistencia_rd_escolha');
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

                        // --- CASO GOLEM (ESPÍRITO/FONTE ELEMENTAL) ---
                        if (hab.nome === "Fonte Elemental" || hab.nome === "Espírito Elemental") {
                            const keyElem = "elemento_escolha";
                            const valorAtual = hab.escolhas_aplicadas?.[keyElem] || "";
                            const opcoesElementos = [
                                { nome: "Ácido", cor: "#8bc34a", icon: "🧪", border: "#33691e" },
                                { nome: "Eletricidade", cor: "#ffeb3b", icon: "⚡", border: "#f57f17", text: "#000" },
                                { nome: "Fogo", cor: "#ff5252", icon: "🔥", border: "#b71c1c" },
                                { nome: "Frio", cor: "#4fc3f7", icon: "❄️", border: "#01579b" }
                            ];

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Golem)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', marginBottom: 10 }}>
                                        Escolha sua fonte elemental. Você absorve dano deste tipo (cura PV em vez de sofrer dano).
                                    </p>
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                                        {opcoesElementos.map((elem) => {
                                            const isSelected = valorAtual === elem.nome;
                                            return (
                                                <button
                                                    key={elem.nome}
                                                    onClick={() => updateRacialChoice(idx, keyElem, elem.nome)}
                                                    style={{
                                                        background: isSelected ? elem.cor : 'transparent',
                                                        color: isSelected ? (elem.text || '#fff') : '#ccc',
                                                        border: `1px solid ${isSelected ? elem.border : '#555'}`,
                                                        borderRadius: '6px',
                                                        padding: '10px',
                                                        cursor: 'pointer',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        gap: '8px',
                                                        fontWeight: isSelected ? 'bold' : 'normal',
                                                        transition: 'all 0.2s'
                                                    }}
                                                >
                                                    <span style={{ fontSize: '1.2rem' }}>{elem.icon}</span>
                                                    <span>{elem.nome}</span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO OSTEON (MEMÓRIA PÓSTUMA) ---
                        if (hab.nome === "Memória Póstuma") {
                            const keyEscolha = "habilidade_racial_escolha";
                            const valorAtual = hab.escolhas_aplicadas?.[keyEscolha] || hab.escolhas_aplicadas?.["poder_escolha"] || "";

                            const raciaisDisponiveis = listaPoderesGerais
                                .filter((p: any) => {
                                    const t = (p.tipo || p.categoria || "").toString();
                                    return t.includes("Raça") || t.includes("Racial");
                                })
                                .map((p: any) => p.nome);

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Osteon)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', marginBottom: 10 }}>
                                        Você pode escolher 1 Poder Geral OU 1 Habilidade de outra Raça.
                                    </p>

                                    <div style={{ display: 'flex', gap: 10, flexDirection: 'column' }}>
                                        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                            <span style={{ color: '#fff' }}>Atual: <strong>{valorAtual || "Nenhum"}</strong></span>
                                        </div>

                                        <div style={{ display: 'flex', gap: 10 }}>
                                            <button
                                                className="btn-action"
                                                onClick={() => abrirSeletor(
                                                    'geral',
                                                    'Memória Póstuma (Poder)',
                                                    poderesGeraisFiltrados.map((p: any) => p.nome),
                                                    undefined,
                                                    (val) => {
                                                        updateRacialChoice(idx, "habilidade_racial_escolha", "");
                                                        updateRacialChoice(idx, "poder_escolha", val);
                                                    }
                                                )}
                                            >
                                                Escolher Poder Geral
                                            </button>

                                            <button
                                                className="btn-action"
                                                style={{ background: '#7b1fa2' }}
                                                onClick={() => abrirSeletor(
                                                    'poder',
                                                    'Memória Póstuma (Racial)',
                                                    raciaisDisponiveis,
                                                    undefined,
                                                    (val) => {
                                                        updateRacialChoice(idx, "poder_escolha", "");
                                                        updateRacialChoice(idx, "habilidade_racial_escolha", val);
                                                    }
                                                )}
                                            >
                                                Escolher Habilidade Racial
                                            </button>
                                        </div>
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

                        // --- CASO 5: GENÉRICO PADRÃO ---
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