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

    // NOVO: Recebe a lista de poderes gerais para montar o seletor misto
    listaPoderesGerais: any[];

    origemBeneficiosEmEdicao: string[];
    setOrigemBeneficiosEmEdicao: (vals: string[]) => void;

    habilidadesEmEdicao: any[];
    setHabilidadesEmEdicao: (vals: any[]) => void;

    classPowersEmEdicao?: string[];
    setClassPowersEmEdicao: React.Dispatch<React.SetStateAction<string[]>>;

    subclasseEmEdicao: string;
    setSubclasseEmEdicao: (val: string) => void;

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
    listaPoderesGerais = [], // Padrão vazio
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao,
    subclasseEmEdicao, setSubclasseEmEdicao,
    abrirSeletor
}) => {

    if (!isOpen) return null;

    // --- FUNÇÃO CENTRAL DE BLOQUEIO ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => { if (info.treino > 0) blocked.add(nome); });
        }
        origemBeneficiosEmEdicao.forEach(val => { if (val && val !== ignorarValor) blocked.add(val); });
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) {
                Object.values(hab.escolhas_aplicadas).forEach((val: any) => { if (val && val !== ignorarValor) blocked.add(val); });
            }
        });
        classPowersEmEdicao.forEach(val => { if (val && val !== ignorarValor) blocked.add(val); });
        return Array.from(blocked);
    };

    // --- DADOS ---
    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});

    // 1. Habilidades Automáticas
    const habilidadesAutomaticas = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);

    // 2. Poderes da Classe (Extraídos do objeto de regras da classe)
    const poderesDaClasse = listaCompletaHabilidadesClasse
        .filter((h: any) => h.classe === classeAtual && h.tipo.includes("Poder de"));

    // 3. Poderes Gerais (Vindos da prop)
    // Filtramos apenas para garantir que são poderes mesmo
    const poderesGeraisValidos = listaPoderesGerais.filter((p: any) => p.categoria !== 'Origem');

    // 4. Lista Unificada para o Seletor (Apenas Nomes para a Lista Restrita)
    const nomesPoderesDisponiveis = Array.from(new Set([
        ...poderesDaClasse.map((p: any) => p.nome),
        ...poderesGeraisValidos.map((p: any) => p.nome)
    ])).sort();

    const slotsPoderes = Math.max(0, nivelAtual - 1);

    // Detecção de Subclasse (Arcanista)
    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content">
                <button className="btn-close-panel" onClick={onClose}>X</button>
                <h2>⚙️ Configuração de Personagem</h2>
                <hr />

                {/* SUBCLASSE */}
                {opcoesSubclasse.length > 0 && habilidadeComSubclasse && (
                    <div style={{ marginBottom: 20, padding: 15, background: '#253b50', borderRadius: 6, border: '1px solid #64b5f6' }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>{habilidadeComSubclasse.nome}</h3>
                        <p style={{ color: '#ccc', fontSize: '0.9rem', marginBottom: 10 }}>Escolha seu caminho:</p>
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

                {/* ORIGEM */}
                <h3 className="section-subtitle">Benefícios de Origem ({origemNome})</h3>
                <div className="origem-box">
                    <p style={{ color: '#aaa', fontSize: '0.9rem', marginBottom: 10 }}>Escolha {qtdEscolhasOrigem} benefícios.</p>
                    {[...Array(qtdEscolhasOrigem)].map((_, i) => {
                        const valorAtual = origemBeneficiosEmEdicao[i] || '';
                        const blocked = getBlacklistGlobal(valorAtual);
                        const opcoes = listaBeneficiosOrigem.filter(opt => !blocked.includes(opt) || opt === valorAtual);
                        return (
                            <div key={i} style={{ marginBottom: '10px', display: 'flex', gap: 10 }}>
                                <input value={valorAtual} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                                <button onClick={() => abrirSeletor('ambos', `Origem #${i + 1}`, opcoes, undefined, (val) => {
                                    const novo = [...origemBeneficiosEmEdicao]; novo[i] = val; setOrigemBeneficiosEmEdicao(novo);
                                }, blocked)} className="btn-action">Selecionar</button>
                            </div>
                        );
                    })}
                </div>

                {/* RACIAIS */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Habilidades Raciais</h3>
                <div className="habilidades-list-wrapper">
                    {habilidadesEmEdicao.map((hab, idx) => (
                        <div key={idx} className="habilidade-item" style={{ marginBottom: 10, paddingBottom: 10, borderBottom: '1px solid #333' }}>
                            <div className="hab-header"><span><strong>{hab.nome}</strong></span> {hab.precisaEscolha && <span style={{ color: '#ffeb3b', fontSize: '0.8rem' }}>CONFIGURAR</span>}</div>
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
                                                        <button onClick={() => abrirSeletor(tipoSeletor, `Escolha para ${hab.nome}`, [], keyEffect.includes('tormenta') ? 'Tormenta' : undefined, (novoVal) => {
                                                            const novoHab = [...habilidadesEmEdicao]; novoHab[idx].escolhas_aplicadas = { ...hab.escolhas_aplicadas, [keyEffect]: novoVal }; setHabilidadesEmEdicao(novoHab);
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

                {/* CLASSE AUTOMÁTICA */}
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

                {/* PODERES DE CLASSE + GERAIS (SLOTS) */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Poderes ({classPowersEmEdicao.length}/{slotsPoderes}) <span style={{ fontSize: '0.7rem', marginLeft: 10, color: '#aaa' }}>(Classe + Gerais)</span></h3>
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
                                            nomesPoderesDisponiveis, // AGORA CONTÉM CLASSE + GERAIS
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