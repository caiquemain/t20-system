import React from 'react';
import '../Ficha.css';
import { validarTodosRequisitos } from '../utils/validators';

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
    listaPoderesGerais = [], dadosDeuses = {},
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao,
    subclasseEmEdicao, setSubclasseEmEdicao,
    devocaoEmEdicao, setDevocaoEmEdicao,
    abrirSeletor
}) => {

    if (!isOpen) return null;

    // --- FUNÇÃO CENTRAL DE BLOQUEIO ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();

        // 1. Perícias fixas da ficha
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => {
                if (info.treino > 0) blocked.add(nome);
            });
        }

        // 2. Poder Concedido (Gratuito)
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

        // 5. Poderes de Classe (Slots)
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
        // Se for Poder Concedido, só mostra se for do meu deus
        if (p.categoria === 'Poder Concedido') {
            return poderesDoMeuDeus.includes(p.nome);
        }
        // Se for Origem, esconde (já tem aba própria)
        if (p.categoria === 'Origem') return false;

        return true;
    });

    // Lista unificada para os Slots de Nível
    const nomesPoderesDisponiveis = Array.from(new Set([
        ...poderesDaClasse.map((p: any) => p.nome),
        ...poderesGeraisFiltrados.map((p: any) => p.nome)
    ])).sort();

    const slotsPoderes = Math.max(0, nivelAtual - 1);

    // --- DETECÇÕES ESPECIAIS ---

    // 1. Subclasse (Ex: Arcanista)
    // Cast explícito para evitar erro TS
    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];

    // 2. Devoção (Ex: Poder Gratuito)
    const infoDeus = dadosDeuses[deusAtual];

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content">
                <button className="btn-close-panel" onClick={onClose}>X</button>
                <h2>⚙️ Configuração de Personagem</h2>
                <hr />

                {/* --- SEÇÃO: SUBCLASSE (AZUL) --- */}
                {opcoesSubclasse.length > 0 && habilidadeComSubclasse && (
                    <div style={{ marginBottom: 20, padding: 15, background: '#253b50', borderRadius: 6, border: '1px solid #64b5f6' }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>
                            {habilidadeComSubclasse.nome}
                        </h3>
                        <p style={{ color: '#ccc', fontSize: '0.9rem', marginBottom: 10 }}>
                            Escolha seu caminho:
                        </p>
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

                {/* --- SEÇÃO: DEVOÇÃO (AMARELO) --- */}
                {deusAtual && infoDeus && (
                    <div className="origem-box" style={{ borderColor: '#ffd700', background: '#2a2a20', marginBottom: 20 }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#ffd700' }}>
                            Devoção: {deusAtual}
                        </h3>
                        <p style={{ color: '#ddd', fontSize: '0.85em', fontStyle: 'italic', marginBottom: 10 }}>
                            "{infoDeus.crencas}"
                        </p>
                        <div style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label>Poder Concedido (Gratuito):</label>
                            <input
                                value={devocaoEmEdicao}
                                readOnly
                                className="input-dark"
                                placeholder="Selecione..."
                                style={{ flex: 1 }}
                            />
                            <button onClick={() => abrirSeletor(
                                'poder',
                                `Poderes de ${deusAtual}`,
                                infoDeus.poderes, // Lista APENAS do deus
                                undefined,
                                (val) => setDevocaoEmEdicao(val),
                                [] // Sem blacklist no gratuito (ou adicione se quiser evitar pegar o mesmo que já tem em slot de nivel, mas raro)
                            )} className="btn-action" style={{ background: '#ffd700', color: 'black' }}>
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
                    {habilidadesEmEdicao.map((hab, idx) => (
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
                                                            const n = [...habilidadesEmEdicao]; n[idx].escolhas_aplicadas = { ...hab.escolhas_aplicadas, [keyEffect]: v }; setHabilidadesEmEdicao(n);
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
                    ))}
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
                    <span style={{ fontSize: '0.7rem', marginLeft: 10, color: '#aaa' }}>(Classe + Gerais + Concedidos)</span>
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
                                        onClick={() => abrirSeletor(
                                            'poder',
                                            `Poder de Nível ${i + 2}`,
                                            nomesPoderesDisponiveis, // LISTA FILTRADA
                                            undefined,
                                            (novoPoder) => {
                                                const novosPoderes = [...classPowersEmEdicao];
                                                while (novosPoderes.length <= i) novosPoderes.push("");
                                                novosPoderes[i] = novoPoder;
                                                setClassPowersEmEdicao(novosPoderes);
                                            },
                                            blocked
                                        )}
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