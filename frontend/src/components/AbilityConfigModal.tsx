import React, { useEffect } from 'react';
import '../Ficha.css';
import { RacialAbilityRow } from './RacialAbilityRow'; // Importação limpa

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
    listaPoderesGerais: any[];
    dadosDeuses: any;
    dadosMagias: any;
    dadosOrigens?: any;
    dadosHabilidadesRaciais?: any;
    dadosEscolhas?: any;
    origemBeneficiosEmEdicao: string[];
    setOrigemBeneficiosEmEdicao: (vals: string[]) => void;
    habilidadesEmEdicao: any[];
    setHabilidadesEmEdicao: (vals: any[]) => void;
    classPowersEmEdicao?: string[];
    setClassPowersEmEdicao: React.Dispatch<React.SetStateAction<string[]>>;
    subclasseEmEdicao: string;
    setSubclasseEmEdicao: (val: string) => void;
    devocaoEmEdicao: string;
    setDevocaoEmEdicao: (val: string) => void;
    poderesEscolhasEmEdicao: Record<string, Record<string, any>>;
    linhagemEmEdicao: string;
    setLinhagemEmEdicao: (v: string) => void;
    tipoDanoEmEdicao: string;
    setTipoDanoEmEdicao: (v: string) => void;
    setPoderesEscolhasEmEdicao: React.Dispatch<React.SetStateAction<Record<string, Record<string, any>>>>;
    abrirSeletor: (tipo: string, titulo: string, listaRestrita?: string[], categoriaFixa?: string, onConfirm?: (val: string) => void, itensBloqueados?: string[]) => void;
}

export const AbilityConfigModal: React.FC<AbilityConfigModalProps> = ({
    isOpen, onClose, onSave, ficha, origemNome, qtdEscolhasOrigem, listaBeneficiosOrigem = [],
    classeAtual, nivelAtual, dadosHabilidadesClasse, listaPoderesGerais = [], dadosDeuses = {},
    dadosMagias = {}, dadosOrigens = {}, dadosHabilidadesRaciais = {}, dadosEscolhas = {},
    origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao, habilidadesEmEdicao, setHabilidadesEmEdicao,
    classPowersEmEdicao = [], setClassPowersEmEdicao, subclasseEmEdicao, setSubclasseEmEdicao,
    devocaoEmEdicao, setDevocaoEmEdicao, abrirSeletor,
    poderesEscolhasEmEdicao = {}, setPoderesEscolhasEmEdicao,
    linhagemEmEdicao, setLinhagemEmEdicao, tipoDanoEmEdicao, setTipoDanoEmEdicao
}) => {
    useEffect(() => {
        if (isOpen && habilidadesEmEdicao.length === 0 && ficha && ficha.habilidades) {
            console.log("⚠️ Lista vazia detectada! Tentando popular automaticamente...");
            const raciaisEncontradas = ficha.habilidades.filter((h: any) => {
                const nome = h.nome;
                const ehRacialPeloDict = dadosHabilidadesRaciais && (dadosHabilidadesRaciais[nome] || Object.values(dadosHabilidadesRaciais).find((d: any) => d.nome === nome));
                const ehRacialPeloTipo = h.tipo && (h.tipo.includes("Racial") || h.tipo.includes("Raça"));
                return ehRacialPeloDict || ehRacialPeloTipo;
            });
            if (raciaisEncontradas.length > 0) setHabilidadesEmEdicao(raciaisEncontradas);
        }
    }, [isOpen, habilidadesEmEdicao, ficha, dadosHabilidadesRaciais]);

    if (!isOpen) return null;

    // Helper para lista de perícias
    const listaNomesPericias = ficha && ficha.pericias ? Object.keys(ficha.pericias) : [];

    const getNomeHabilidade = (id: string) => {
        if (!id) return "";
        let nome = id;
        if (dadosHabilidadesRaciais && dadosHabilidadesRaciais[id]) nome = dadosHabilidadesRaciais[id].nome;
        return nome.replace(/_/g, " ");
    };

    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();
        if (ficha?.pericias) Object.entries(ficha.pericias).forEach(([nome, info]: any) => { if (info.treino > 0) blocked.add(nome); });
        if (devocaoEmEdicao && devocaoEmEdicao !== ignorarValor) blocked.add(devocaoEmEdicao);
        origemBeneficiosEmEdicao.forEach(val => { if (val && val !== ignorarValor) blocked.add(val); });
        habilidadesEmEdicao.forEach(hab => {
            if (hab.escolhas_aplicadas) Object.values(hab.escolhas_aplicadas).forEach((val: any) => {
                if (Array.isArray(val)) val.forEach(v => { if (v && v !== ignorarValor) blocked.add(v); });
                else if (val && val !== ignorarValor) blocked.add(val);
            });
        });
        classPowersEmEdicao.forEach(val => { if (val && val !== ignorarValor) blocked.add(val); });
        return Array.from(blocked);
    };

    const updateRacialChoice = (ref: number | string, key: string, value: any) => {
        const novos = [...habilidadesEmEdicao];
        let idx = typeof ref === 'number' ? ref : novos.findIndex(h => h.nome === ref);
        if (idx === -1 || !novos[idx]) {
            console.error('[MODAL][RACIAL] alvo não encontrado:', { ref, key, value });
            return;
        }
        console.log('[MODAL][RACIAL] gravando:', { alvo: novos[idx].nome, key, value });
        novos[idx] = {
            ...novos[idx],
            escolhas_aplicadas: { ...(novos[idx].escolhas_aplicadas || {}), [key]: value }
        };
        setHabilidadesEmEdicao(novos);
    };

    // [LOTE 1-UI] Atualiza escolha secundária de um poder (escola/atributo/familiar)
    const updatePoderEscolha = (poderNome: string, chave: string, valor: any) => {
        if (!setPoderesEscolhasEmEdicao) return;
        setPoderesEscolhasEmEdicao(prev => ({
            ...prev,
            [poderNome]: { ...(prev[poderNome] || {}), [chave]: valor }
        }));
    };

    const infoDeus = dadosDeuses[ficha.cabecalho.deus];
    const poderesDoDeus = infoDeus ? infoDeus.poderes : [];

    const nomesPoderesDisponiveis = listaPoderesGerais.filter((p: any) => {
        if (p.is_general) return true;
        const t = (p.tipo || p.categoria || "").toString();
        if (p.is_general === undefined) {
            const grupos = ["Combate", "Destino", "Magia", "Tormenta"];
            const ehPermitido = grupos.some(g => t.includes(g));
            const ehProibido = t.includes("Classe") || t.includes("Origem") || t.includes("Racial") || t.includes("Raça") || t.includes("Concedido");
            if (ehPermitido && !ehProibido) return true;
        }
        const isConcedido = t.includes("Concedido") || p.categoria === "Poder Concedido";
        if (isConcedido && poderesDoDeus.includes(p.nome)) return true;
        return false;
    }).map(p => p.nome).sort();

    // [LOTE 1-UI] Poderes da classe atual entram na lista de seleção
    const nomesPoderesClasse = Object.values(dadosHabilidadesClasse || {})
        .filter((h: any) => h.classe === classeAtual && (h.tipo || "").includes("Poder de") && (h.nivel ?? 2) <= nivelAtual)
        .map((h: any) => h.nome);

    const listaCompletaHabilidadesClasse = Object.values(dadosHabilidadesClasse || {});
    const habilidadesAutomaticas = listaCompletaHabilidadesClasse.filter((h: any) => h.classe === classeAtual && h.tipo === "Habilidade de Classe" && h.nivel <= nivelAtual);
    const slotsPoderes = Math.max(0, nivelAtual - 1);
    const nomesPoderesDisponiveisFinais = Array.from(new Set([...nomesPoderesDisponiveis, ...nomesPoderesClasse])).sort();
    const habilidadeComSubclasse: any = habilidadesAutomaticas.find((h: any) => h.efeitos && h.efeitos.escolha_subclasse);
    const opcoesSubclasse: string[] = habilidadeComSubclasse ? habilidadeComSubclasse.efeitos.escolha_subclasse : [];

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content">
                <button className="btn-close-panel" onClick={onClose}>X</button>
                <h2>⚙️ Configuração de Personagem</h2>
                <hr />
                {/* 1. SUBCLASSE */}
                {opcoesSubclasse.length > 0 && habilidadeComSubclasse && (
                    <div style={{ marginBottom: 20, padding: 15, background: '#253b50', borderRadius: 6, border: '1px solid #64b5f6' }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>{habilidadeComSubclasse.nome}</h3>
                        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                            {opcoesSubclasse.map(opcao => (
                                <div key={opcao} style={{ flex: 1, minWidth: 180 }}>
                                    <button onClick={() => setSubclasseEmEdicao(opcao)} className={`btn-action ${subclasseEmEdicao === opcao ? 'selected' : ''}`} style={{ width: '100%', background: subclasseEmEdicao === opcao ? '#4caf50' : '#333', border: subclasseEmEdicao === opcao ? '1px solid #fff' : '1px solid #555', color: 'white' }}>
                                        {subclasseEmEdicao === opcao ? '✅ ' : ''}{opcao}
                                    </button>
                                    {(dadosEscolhas?.CAMINHOS_ARCANISTA_INFO || {})[opcao] && (
                                        <p style={{ margin: '6px 2px 0', fontSize: '0.72rem', color: subclasseEmEdicao === opcao ? '#a5d6a7' : '#90a4ae', lineHeight: 1.35 }}>
                                            {(dadosEscolhas?.CAMINHOS_ARCANISTA_INFO || {})[opcao]}
                                        </p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {/* 1b. LINHAGEM (FEITICEIRO) */}
             {subclasseEmEdicao === "Feiticeiro" && (
                 <div style={{ marginBottom: 20, padding: 15, background: '#3b2530', borderRadius: 6, border: '1px solid #ce93d8' }}>
                     <h3 className="section-subtitle" style={{ marginTop: 0, color: '#ce93d8' }}>Linhagem Sobrenatural</h3>
                     <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                         {["Dracônica", "Feérica", "Rubra"].map(l => (
                             <button key={l} onClick={() => setLinhagemEmEdicao(l)} className={`btn-action ${linhagemEmEdicao === l ? 'selected' : ''}`} style={{ flex: 1, background: linhagemEmEdicao === l ? '#4caf50' : '#333', border: linhagemEmEdicao === l ? '1px solid #fff' : '1px solid #555', color: 'white' }}>{l}</button>
                         ))}
                     </div>
                     {linhagemEmEdicao === "Dracônica" && (
                         <div style={{ marginTop: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                             <label style={{ fontSize: '0.8rem', color: '#aaa' }}>Tipo de dano:</label>
                             <select className="input-dark" value={tipoDanoEmEdicao} onChange={e => setTipoDanoEmEdicao(e.target.value)} style={{ flex: 1 }}>
                                 <option value="">Selecionar...</option>
                                 {["ácido", "eletricidade", "fogo", "frio"].map(t => <option key={t} value={t}>{t}</option>)}
                             </select>
                         </div>
                     )}
                 </div>
             )}
             {/* 2. DEVOÇÃO */}
                {ficha.cabecalho.deus && infoDeus && (
                    <div className="origem-box" style={{ borderColor: '#ffd700', background: '#2a2a20', marginBottom: 20 }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#ffd700' }}>Devoção: {ficha.cabecalho.deus}</h3>
                        <div style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label>Poder Concedido:</label>
                            <input value={devocaoEmEdicao} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                            <button onClick={() => abrirSeletor('poder', `Poderes de ${ficha.cabecalho.deus}`, infoDeus.poderes, undefined, (val) => setDevocaoEmEdicao(val), getBlacklistGlobal(devocaoEmEdicao))} className="btn-action" style={{ background: '#ffd700', color: 'black' }}>Selecionar</button>
                        </div>
                    </div>
                )}
                {/* 3. ORIGEM */}
                {(() => {
                    const bloqueioOrigem = habilidadesEmEdicao.find(h => h.efeitos && h.efeitos.sem_origem);
                    if (bloqueioOrigem) return <div className="origem-box" style={{ border: '1px dashed #d32f2f', background: 'rgba(211, 47, 47, 0.1)', marginBottom: 20 }}><p style={{ color: '#ff8a80', margin: 0 }}>🚫 <strong>Origem Bloqueada:</strong> {bloqueioOrigem.nome}</p></div>;
                    return (
                        <div className="origem-box">
                            <h3 className="section-subtitle">Benefícios de Origem ({origemNome})</h3>
                            {[...Array(qtdEscolhasOrigem)].map((_, i) => {
                                const valorAtual = origemBeneficiosEmEdicao[i] || '';
                                return (
                                    <div key={i} style={{ marginBottom: 10, display: 'flex', gap: 10 }}>
                                        <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                                        <button onClick={() => abrirSeletor('ambos', `Origem #${i + 1}`, listaBeneficiosOrigem, undefined, (val) => {
                                            const n = [...origemBeneficiosEmEdicao]; n[i] = val; setOrigemBeneficiosEmEdicao(n);
                                        }, getBlacklistGlobal(valorAtual))} className="btn-action">Selecionar</button>
                                    </div>
                                );
                            })}
                        </div>
                    );
                })()}
                {/* 4. HABILIDADES RACIAIS */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Habilidades Raciais</h3>
                <div className="habilidades-list-wrapper">
                    {habilidadesEmEdicao.map((hab, idx) => (
                        <RacialAbilityRow
                            key={idx} index={idx} hab={hab}
                            dadosHabilidadesRaciais={dadosHabilidadesRaciais}
                            listaPoderesGerais={listaPoderesGerais}
                            dadosMagias={dadosMagias} dadosOrigens={dadosOrigens}
                            abrirSeletor={abrirSeletor}
                            updateRacialChoice={updateRacialChoice}
                            getBlacklistGlobal={getBlacklistGlobal}
                            getNomeHabilidade={getNomeHabilidade}
                            poderesDoDeus={poderesDoDeus}
                            listaPericias={listaNomesPericias}
                        />
                    ))}
                </div>
                {/* 5. CLASSE (Fixas) */}
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
                {/* 6. PODERES (Slots) */}
                <h3 className="section-subtitle" style={{ marginTop: 20 }}>Poderes ({classPowersEmEdicao.length}/{slotsPoderes})</h3>
                {slotsPoderes > 0 ? (
                    <div className="powers-slots-container">
                        {[...Array(slotsPoderes)].map((_, i) => {
                            const valorAtual = classPowersEmEdicao[i] || "";
                            return (
                                <div key={i} style={{ marginBottom: 10 }}>
                                    <div className="power-slot-row" style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                                        <div style={{ width: '25px', color: '#666', fontSize: '0.8rem', textAlign: 'right' }}>{i + 2}º</div>
                                        <input value={valorAtual} readOnly className="input-dark" placeholder="Selecionar Poder..." style={{ flex: 1 }} />
                                        <button onClick={() => abrirSeletor('poder', `Poder de Nível ${i + 2}`, nomesPoderesDisponiveisFinais, undefined, (v) => {
                                            const novosPoderes = [...classPowersEmEdicao];
                                            while (novosPoderes.length <= i) novosPoderes.push("");
                                            novosPoderes[i] = v;
                                            setClassPowersEmEdicao(novosPoderes);
                                        }, getBlacklistGlobal(valorAtual))} className="btn-action" style={{ background: valorAtual ? '#4caf50' : '#2196f3', border: 'none', color: 'white' }}>{valorAtual ? 'Trocar' : 'Escolher'}</button>
                                    </div>
                                    {/* [LOTE 1-UI] Seletores secundários (escola/atributo/familiar) */}
                                    {(((dadosEscolhas?.PODERES_COM_ESCOLHA || {})[valorAtual] || []) || []).map((g: any) => {
                                        const valorEscolha = ((poderesEscolhasEmEdicao || {})[valorAtual] || {})[g.chave] || "";
                                        return (
                                            <div key={g.chave} style={{ display: 'flex', gap: 10, alignItems: 'center', width: '100%', marginTop: 6, marginLeft: 35 }}>
                                                <label style={{ fontSize: '0.8rem', color: '#aaa', minWidth: 110 }}>{g.rotulo}:</label>
                                                <select className="input-dark" value={valorEscolha} onChange={e => updatePoderEscolha(valorAtual, g.chave, e.target.value)} style={{ flex: 1 }}>
                                                    <option value="">Selecionar...</option>
                                                    {g.opcoes.map((o: any) => {
                                                        const val = typeof o === 'string' ? o : o.valor;
                                                        const rot = typeof o === 'string' ? o : o.rotulo;
                                                        return <option key={val} value={val}>{rot}</option>;
                                                    })}
                                                </select>
                                            </div>
                                        );
                                    })}
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
