import React from 'react';
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

    origemBeneficiosEmEdicao: string[];
    setOrigemBeneficiosEmEdicao: (vals: string[]) => void;

    habilidadesEmEdicao: any[];
    setHabilidadesEmEdicao: (vals: any[]) => void;

    classPowersEmEdicao?: string[];
    setClassPowersEmEdicao: React.Dispatch<React.SetStateAction<string[]>>;

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
    ficha, origemNome, qtdEscolhasOrigem,
    listaBeneficiosOrigem = [],
    classeAtual, nivelAtual, dadosHabilidadesClasse,
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
    habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [],
    setClassPowersEmEdicao,
    abrirSeletor
}) => {

    if (!isOpen) return null;

    // --- FUNÇÃO CENTRAL DE BLOQUEIO ---
    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();

        // 1. Perícias já treinadas na ficha base
        if (ficha && ficha.pericias) {
            Object.entries(ficha.pericias).forEach(([nome, info]: any) => {
                if (info.treino > 0) blocked.add(nome);
            });
        }

        // 2. Escolhas de Origem
        origemBeneficiosEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });

        // 3. Escolhas Raciais
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) {
                Object.values(hab.escolhas_aplicadas).forEach((val: any) => {
                    if (val && val !== ignorarValor) blocked.add(val);
                });
            }
        });

        // 4. Poderes de Classe
        classPowersEmEdicao.forEach(val => {
            if (val && val !== ignorarValor) blocked.add(val);
        });

        return Array.from(blocked);
    };

    // --- DADOS ---
    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});

    // 1. Habilidades da Classe Atual
    const habilidadesDaClasse = listaCompletaHabilidadesClasse.filter((h: any) => h.classe === classeAtual);

    // 2. Automáticas
    const habilidadesAutomaticas = habilidadesDaClasse.filter((h: any) => h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);

    // 3. Poderes Disponíveis (Classe + Gerais)
    const poderesDaClasse = habilidadesDaClasse.filter((h: any) => h.tipo.includes("Poder de"));

    const poderesGerais = listaCompletaHabilidadesClasse.filter((h: any) => {
        const tipo = h.tipo || "";
        return tipo.includes("Geral") ||
            tipo.includes("Combate") ||
            tipo.includes("Destino") ||
            tipo.includes("Magia") ||
            tipo.includes("Tormenta") ||
            tipo.includes("Concedido");
    });

    const todosPoderesPossiveis = [...poderesDaClasse, ...poderesGerais];

    // CORREÇÃO AQUI: Adicionado tipagem ': any' para item, a e b
    const poderesDisponiveis = Array.from(
        new Map(todosPoderesPossiveis.map((item: any) => [item.nome, item])).values()
    ).sort((a: any, b: any) => a.nome.localeCompare(b.nome));

    const slotsPoderes = Math.max(0, nivelAtual - 1);
    const safeBeneficios = Array.isArray(listaBeneficiosOrigem) ? listaBeneficiosOrigem : [];

    // --- VALIDAÇÃO DE REQUISITOS ---
    const verificarRequisito = (req: string): { ok: boolean, msg: string } => {
        const reqLower = req.toLowerCase();

        const matchAttr = reqLower.match(/(for|des|con|int|sab|car)\s?(\d+)/);
        if (matchAttr) {
            const attrMapInverso: Record<string, string> = { 'for': 'forca', 'des': 'destreza', 'con': 'constituicao', 'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma' };
            const attrKey = attrMapInverso[matchAttr[1]];
            const valorMin = parseInt(matchAttr[2]);
            const valorAtual = ficha.atributos[attrKey] || 0;
            return { ok: valorAtual >= valorMin, msg: `Requer ${matchAttr[1].toUpperCase()} ${valorMin}` };
        }
        if (reqLower.includes('treinado em')) {
            const periciaNome = req.replace(/treinado em /i, '').trim();
            const isTreinado = getBlacklistGlobal().includes(periciaNome);
            return { ok: isTreinado, msg: `Requer treino em ${periciaNome}` };
        }
        const matchNivel = reqLower.match(/(?:nível|nivel)\s?(\d+)/);
        if (matchNivel) {
            const nivelReq = parseInt(matchNivel[1]);
            const nivelChar = ficha.classes[0]?.nivel || 1;
            return { ok: nivelChar >= nivelReq, msg: `Requer Nível ${nivelReq}` };
        }

        const temPoder = getBlacklistGlobal().includes(req);
        if (temPoder) return { ok: true, msg: 'Ok' };

        return { ok: false, msg: `Requer: ${req}` };
    };

    const validarTodosRequisitos = (requisitos?: string[]) => {
        if (!requisitos || requisitos.length === 0) return { apto: true, erros: [] };
        const analises = requisitos.map(verificarRequisito);
        const erros = analises.filter(a => !a.ok).map(a => a.msg);
        return { apto: erros.length === 0, erros };
    };

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content">
                <button className="btn-close-panel" onClick={onClose}>X</button>
                <h2>⚙️ Configuração de Personagem</h2>
                <hr />

                {/* SEÇÃO 1: ORIGEM */}
                <h3 className="section-subtitle">Benefícios de Origem ({origemNome})</h3>
                {safeBeneficios.length === 0 ? (
                    <div className="alert-box error">⚠ Origem não carregada.</div>
                ) : (
                    <div className="origem-box">
                        <p style={{ color: '#aaa', fontSize: '0.9rem', marginBottom: 10 }}>
                            Escolha {qtdEscolhasOrigem} benefícios.
                        </p>
                        {[...Array(qtdEscolhasOrigem)].map((_, i) => {
                            const valorAtual = origemBeneficiosEmEdicao[i] || '';
                            const bloqueados = getBlacklistGlobal(valorAtual);
                            const opcoesDisponiveis = safeBeneficios.filter(opt => !bloqueados.includes(opt));

                            return (
                                <div key={i} style={{ marginBottom: '10px', display: 'flex', gap: 10 }}>
                                    <input value={valorAtual} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                                    <button onClick={() => abrirSeletor(
                                        'ambos',
                                        `Origem #${i + 1}`,
                                        opcoesDisponiveis,
                                        undefined,
                                        (val) => {
                                            const novo = [...origemBeneficiosEmEdicao];
                                            novo[i] = val;
                                            setOrigemBeneficiosEmEdicao(novo);
                                        },
                                        bloqueados
                                    )} className="btn-action">Selecionar</button>
                                </div>
                            );
                        })}
                    </div>
                )}

                {/* SEÇÃO 2: HABILIDADES DE RAÇA */}
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
                                            const bloqueados = getBlacklistGlobal(valorAtual);

                                            let tipoSeletor = 'pericia';
                                            let label = 'Perícia';

                                            if (keyEffect.includes('pericia_ou_poder')) {
                                                tipoSeletor = 'ambos';
                                                label = 'Perícia ou Poder';
                                            } else if (keyEffect.includes('poder')) {
                                                tipoSeletor = 'poder';
                                                label = 'Poder';
                                                if (keyEffect.includes('tormenta')) { label = 'Poder da Tormenta'; }
                                            }

                                            return (
                                                <div key={keyEffect} style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 5 }}>
                                                    <label style={{ fontSize: '0.8rem', color: '#aaa' }}>{label}:</label>
                                                    <div style={{ display: 'flex', gap: 10 }}>
                                                        <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecionar..." />
                                                        <button onClick={() => abrirSeletor(
                                                            tipoSeletor,
                                                            `Escolha para ${hab.nome}`,
                                                            [],
                                                            keyEffect.includes('tormenta') ? 'Tormenta' : undefined,
                                                            (novoVal) => {
                                                                const novoHab = [...habilidadesEmEdicao];
                                                                novoHab[idx].escolhas_aplicadas = {
                                                                    ...hab.escolhas_aplicadas,
                                                                    [keyEffect]: novoVal
                                                                };
                                                                setHabilidadesEmEdicao(novoHab);
                                                            },
                                                            bloqueados
                                                        )} className="btn-action" style={{ background: '#2196f3', border: 'none', color: 'white' }}>Escolher</button>
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

                {/* SEÇÃO 3: CLASSE AUTOMÁTICA */}
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

                {/* SEÇÃO 4: PODERES DE CLASSE + GERAIS */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>
                    Poderes ({classPowersEmEdicao.length}/{slotsPoderes})
                    <span style={{ fontSize: '0.7rem', marginLeft: 10, color: '#aaa' }}>(Classe + Gerais)</span>
                </h3>

                {slotsPoderes > 0 ? (
                    <div className="powers-grid">
                        {poderesDisponiveis.map((poder: any) => {
                            const isSelected = classPowersEmEdicao.includes(poder.nome);
                            const { apto, erros } = validarTodosRequisitos(poder.requisitos);
                            const jaTem = getBlacklistGlobal('').includes(poder.nome) && !isSelected;
                            const bloqueado = (!apto || jaTem) && !isSelected;

                            // Estilo para diferenciar Geral de Classe
                            const isGeral = !poder.tipo.includes("Poder de");
                            const borderColor = isGeral ? '#7e57c2' : '#4caf50';

                            return (
                                <div
                                    key={poder.nome}
                                    className={`power-card ${isSelected ? 'selected' : ''} ${bloqueado ? 'blocked' : ''}`}
                                    style={!bloqueado && !isSelected ? { borderLeft: `4px solid ${borderColor}` } : {}}
                                    onClick={() => {
                                        if (bloqueado) return;
                                        if (isSelected) setClassPowersEmEdicao(prev => prev.filter(p => p !== poder.nome));
                                        else if (classPowersEmEdicao.length < slotsPoderes) setClassPowersEmEdicao(prev => [...prev, poder.nome]);
                                    }}
                                    title={bloqueado ? (jaTem ? "Já possui esta habilidade" : erros.join(', ')) : poder.descricao}
                                >
                                    <div className="power-header">
                                        <span className="power-name">{poder.nome}</span>
                                        {bloqueado && "🔒"}
                                        {isSelected && "✅"}
                                    </div>
                                    <div style={{ fontSize: '0.65rem', color: '#aaa', marginBottom: 4 }}>
                                        {poder.tipo}
                                    </div>
                                    {poder.requisitos && <div className="power-reqs" style={{ fontSize: '0.7rem', color: '#ffb74d' }}>Req: {poder.requisitos.join(', ')}</div>}
                                </div>
                            )
                        })}
                    </div>
                ) : <p className="text-muted">Disponível no nível 2.</p>}

                <button className="btn-apply-changes" onClick={onSave} style={{ marginTop: 30 }}>✅ Salvar</button>
            </div>
        </div>
    );
};