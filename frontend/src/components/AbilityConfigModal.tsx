import React, { useState } from 'react';
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
    dadosMagias: any; // <--- NOVO: Recebe o dicionário de magias

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
    listaPoderesGerais = [], dadosDeuses = {}, dadosMagias = {}, // Default vazio
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao,
    subclasseEmEdicao, setSubclasseEmEdicao,
    devocaoEmEdicao, setDevocaoEmEdicao,
    abrirSeletor
}) => {

    // Estado local para controlar a UI de alternância do Versátil (Humano)
    const [modosSlot2, setModosSlot2] = useState<Record<number, 'pericia' | 'poder'>>({});

    if (!isOpen) return null;

    // --- PREPARAÇÃO DE DADOS ---

    // Lista de Magias de 1º Círculo (Arcanas e Divinas) para Tatuagem Mística
    const magiasCirculo1 = Object.values(dadosMagias)
        .filter((m: any) => m.circulo === 1)
        .map((m: any) => m.nome)
        .sort();

    // --- FUNÇÃO CENTRAL DE BLOQUEIO ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();

        // 1. Perícias fixas da ficha
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => {
                if (info.treino > 0) blocked.add(nome);
            });
        }

        // 2. Poder Concedido
        if (devocaoEmEdicao && devocaoEmEdicao !== ignorarValor) {
            blocked.add(devocaoEmEdicao);
        }

        // 3. Origem
        origemBeneficiosEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });

        // 4. Raciais
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) {
                Object.values(hab.escolhas_aplicadas).forEach((val: any) => {
                    if (val && val !== ignorarValor) blocked.add(val);
                });
            }
        });

        // 5. Poderes de Classe
        classPowersEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });

        return Array.from(blocked);
    };

    // --- DADOS ---
    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});

    // Habilidades Automáticas e Poderes de Classe
    const habilidadesAutomaticas = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);

    const poderesDaClasse = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo.includes("Poder de"));

    // --- FILTRO INTELIGENTE DE PODERES GERAIS ---
    const deusAtual = ficha.cabecalho.deus;
    const poderesDoMeuDeus = (deusAtual && dadosDeuses[deusAtual]) ? dadosDeuses[deusAtual].poderes : [];

    const poderesGeraisFiltrados = listaPoderesGerais.filter((p: any) => {
        if (p.categoria === 'Poder Concedido') {
            return poderesDoMeuDeus.includes(p.nome);
        }
        if (p.categoria === 'Origem') return false;
        return true;
    });

    const nomesPoderesDisponiveis = Array.from(new Set([
        ...poderesDaClasse.map((p: any) => p.nome),
        ...poderesGeraisFiltrados.map((p: any) => p.nome)
    ])).sort();

    const slotsPoderes = Math.max(0, nivelAtual - 1);

    // --- DETECÇÕES ESPECIAIS ---
    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];

    const infoDeus = dadosDeuses[deusAtual];

    // Helper para atualizar escolhas raciais
    const updateRacialChoice = (index: number, key: string, value: string) => {
        const novos = [...habilidadesEmEdicao];
        novos[index].escolhas_aplicadas = {
            ...novos[index].escolhas_aplicadas,
            [key]: value
        };
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
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>
                            {habilidadeComSubclasse.nome}
                        </h3>
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
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#ffd700' }}>
                            Devoção: {deusAtual}
                        </h3>
                        <div style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label>Poder Concedido:</label>
                            <input value={devocaoEmEdicao} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                            <button onClick={() => abrirSeletor('poder', `Poderes de ${deusAtual}`, infoDeus.poderes, undefined, (val) => setDevocaoEmEdicao(val), [])}
                                className="btn-action" style={{ background: '#ffd700', color: 'black' }}>
                                Selecionar
                            </button>
                        </div>
                    </div>
                )}

                {/* --- SEÇÃO: ORIGEM --- */}
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
                                    const n = [...origemBeneficiosEmEdicao]; n[i] = val; setOrigemBeneficiosEmEdicao(n);
                                }, blocked)} className="btn-action">Selecionar</button>
                            </div>
                        );
                    })}
                </div>

                {/* --- SEÇÃO: RACIAIS --- */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Habilidades Raciais</h3>
                <div className="habilidades-list-wrapper">
                    {habilidadesEmEdicao.map((hab, idx) => {

                        // --- CASO 1: HUMANO (VERSÁTIL) ---
                        if (hab.nome === "Versátil") {
                            const p1 = hab.escolhas_aplicadas?.pericia_1 || "";

                            // Define valores do segundo slot
                            const p2 = hab.escolhas_aplicadas?.pericia_2 || "";
                            const pg = hab.escolhas_aplicadas?.poder_geral || "";

                            // Determina modo atual (se já tem poder salvo, é 'poder', senão é o que tá no state ou 'pericia')
                            const modoAtual = pg ? 'poder' : (modosSlot2[idx] || 'pericia');

                            // Função para alternar o modo e limpar o valor antigo
                            const toggleModo = (novoModo: 'pericia' | 'poder') => {
                                setModosSlot2(prev => ({ ...prev, [idx]: novoModo }));

                                // Limpa o valor da escolha anterior no objeto
                                const novos = [...habilidadesEmEdicao];
                                const novasEscolhas = { ...novos[idx].escolhas_aplicadas };

                                if (novoModo === 'pericia') {
                                    delete novasEscolhas.poder_geral;
                                    novasEscolhas.pericia_2 = "";
                                } else {
                                    delete novasEscolhas.pericia_2;
                                    novasEscolhas.poder_geral = "";
                                }

                                novos[idx].escolhas_aplicadas = novasEscolhas;
                                setHabilidadesEmEdicao(novos);
                            };

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Humano)</span>
                                        <span style={{ color: '#ffeb3b', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc', fontStyle: 'italic' }}>
                                        Escolha 2 Perícias <strong>OU</strong> 1 Perícia e 1 Poder Geral.
                                    </p>

                                    <div style={{ display: 'flex', flexDirection: 'column', gap: 15, marginTop: 10 }}>
                                        {/* SLOT 1: PERÍCIA FIXA */}
                                        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                            <label style={{ width: 90, fontSize: '0.85rem', color: '#81c784' }}>Perícia Fixa:</label>
                                            <input value={p1} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione uma perícia..." />
                                            <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Versátil: Perícia Fixa', [], undefined, (v) => updateRacialChoice(idx, 'pericia_1', v), getBlacklistGlobal(p1))}>Escolher</button>
                                        </div>

                                        {/* SLOT 2: FLEXÍVEL */}
                                        <div style={{ padding: 10, border: '1px dashed #555', borderRadius: 4, background: 'rgba(255,255,255,0.02)' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                                                <label style={{ fontSize: '0.85rem', color: '#ffd700' }}>Segundo Slot:</label>
                                                <div style={{ display: 'flex', gap: 5 }}>
                                                    <button onClick={() => toggleModo('pericia')}
                                                        style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'pericia' ? '#00bcd4' : '#333', color: modoAtual === 'pericia' ? '#000' : '#888', border: '1px solid #555', borderRadius: 3 }}>
                                                        Perícia
                                                    </button>
                                                    <button onClick={() => toggleModo('poder')}
                                                        style={{ fontSize: '0.7rem', padding: '3px 8px', cursor: 'pointer', background: modoAtual === 'poder' ? '#9c27b0' : '#333', color: modoAtual === 'poder' ? '#fff' : '#888', border: '1px solid #555', borderRadius: 3 }}>
                                                        Poder Geral
                                                    </button>
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
                        if (hab.nome.includes("Tatuagem")) {
                            const magiaEscolhida = hab.escolhas_aplicadas?.magia_escolha || "";

                            return (
                                <div key={idx} className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                                    <div className="hab-header" style={{ marginBottom: 10 }}>
                                        <span><strong>{hab.nome}</strong> (Qareen)</span>
                                        <span style={{ color: '#e040fb', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                                    </div>
                                    <p style={{ fontSize: '0.8rem', color: '#ccc' }}>
                                        Você aprende uma magia de 1º círculo (Arcana ou Divina).
                                    </p>

                                    <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 10 }}>
                                        <label style={{ width: 90, fontSize: '0.85rem', color: '#e040fb' }}>Magia:</label>
                                        <input value={magiaEscolhida} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione uma magia..." />
                                        <button
                                            className="btn-action"
                                            style={{ background: '#e040fb', color: 'white' }}
                                            onClick={() => abrirSeletor(
                                                'ambos', // Usa 'ambos' para passar lista genérica
                                                'Escolha sua Tatuagem Mística',
                                                magiasCirculo1, // Passa a lista filtrada de magias
                                                undefined,
                                                (val) => updateRacialChoice(idx, 'magia_escolha', val)
                                            )}
                                        >
                                            Escolher
                                        </button>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 3: QAREEN (RESISTÊNCIA ELEMENTAL) ---
                        // Verifica se existe o efeito de escolha de RD
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
                                    <p style={{ fontSize: '0.8rem', color: '#ccc' }}>
                                        Escolha sua ascendência para receber Resistência 10.
                                    </p>

                                    <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 10 }}>
                                        <label style={{ width: 90, fontSize: '0.85rem', color: '#ff5722' }}>Elemento:</label>
                                        <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                        <button
                                            className="btn-action"
                                            style={{ background: '#ff5722' }}
                                            onClick={() => abrirSeletor(
                                                'ambos',
                                                'Ascendência Qareen',
                                                listaElementos,
                                                undefined,
                                                (val) => updateRacialChoice(idx, keyRd, val)
                                            )}
                                        >
                                            Escolher
                                        </button>
                                    </div>
                                </div>
                            );
                        }

                        // --- CASO 4: GENÉRICO (OUTRAS RAÇAS) ---
                        return (
                            <div key={idx} className="habilidade-item" style={{ marginBottom: 10, paddingBottom: 10, borderBottom: '1px solid #333' }}>
                                <div className="hab-header">
                                    <span><strong>{hab.nome}</strong></span>
                                    {hab.precisaEscolha && <span style={{ color: '#ffeb3b', fontSize: '0.8rem' }}>CONFIGURAR</span>}
                                </div>
                                {hab.precisaEscolha && (
                                    <div className="hab-config" style={{ marginTop: 10 }}>
                                        {Object.entries(hab.efeitos).map(([keyEffect, _]) => {
                                            if (keyEffect.endsWith('_escolha')) {
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
                                    <button
                                        onClick={() => abrirSeletor('poder', `Poder de Nível ${i + 2}`, nomesPoderesDisponiveis, undefined, (v) => {
                                            const novosPoderes = [...classPowersEmEdicao];
                                            while (novosPoderes.length <= i) novosPoderes.push("");
                                            novosPoderes[i] = v;
                                            setClassPowersEmEdicao(novosPoderes);
                                        }, blocked)}
                                        className="btn-action"
                                        style={{ background: valorAtual ? '#4caf50' : '#2196f3', border: 'none', color: 'white' }}
                                    >
                                        {valorAtual ? 'Trocar' : 'Escolher'}
                                    </button>
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