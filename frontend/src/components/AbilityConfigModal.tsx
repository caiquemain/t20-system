import React, { useEffect } from 'react';
import '../Ficha.css';
import { RacialAbilityRow } from './RacialAbilityRow'; // Importação limpa
import { T20Icon } from './T20Icon';
import { useEscapeKey } from '../hooks/useEscapeKey';
import { EscolhasDinamicasPanel } from './EscolhasDinamicasPanel';

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
    devocaoEmEdicao: string[];
    setDevocaoEmEdicao: React.Dispatch<React.SetStateAction<string[]>>;
    fundamentalistaEmEdicao: boolean;
    setFundamentalistaEmEdicao: (val: boolean) => void;
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
    devocaoEmEdicao = [], setDevocaoEmEdicao, fundamentalistaEmEdicao = false, setFundamentalistaEmEdicao,
    abrirSeletor,
    poderesEscolhasEmEdicao = {}, setPoderesEscolhasEmEdicao,
    linhagemEmEdicao, setLinhagemEmEdicao, tipoDanoEmEdicao, setTipoDanoEmEdicao
}) => {
    useEscapeKey(isOpen, onClose);
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

    const getNomeHabilidade = (id: string) => {
        if (!id) return "";
        let nome = id;
        if (dadosHabilidadesRaciais && dadosHabilidadesRaciais[id]) nome = dadosHabilidadesRaciais[id].nome;
        return nome.replace(/_/g, " ");
    };

    const getBlacklistGlobal = (ignorarValor: string = "") => {
        const blocked = new Set<string>();
        if (ficha?.pericias) Object.entries(ficha.pericias).forEach(([nome, info]: any) => { if (info.treino > 0) blocked.add(nome); });
        (devocaoEmEdicao || []).forEach(val => { if (val && val !== ignorarValor) blocked.add(val); });
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

    // Gravação atômica de múltiplas chaves (evita race condition em switchMode)
    const updateRacialChoiceMulti = (ref: number | string, updates: Record<string, any>) => {
        const novos = [...habilidadesEmEdicao];
        let idx = typeof ref === 'number' ? ref : novos.findIndex(h => h.nome === ref);
        if (idx === -1 || !novos[idx]) {
            console.error('[MODAL][RACIAL] alvo não encontrado:', { ref, updates });
            return;
        }
        console.log('[MODAL][RACIAL] gravando múltiplas chaves:', { alvo: novos[idx].nome, updates });
        novos[idx] = {
            ...novos[idx],
            escolhas_aplicadas: { ...(novos[idx].escolhas_aplicadas || {}), ...updates }
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
                <h2 style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                    <T20Icon name="config" size={22} /> Configuração de Personagem
                </h2>
                <hr />
                {/* 1. SUBCLASSE */}
                {opcoesSubclasse.length > 0 && habilidadeComSubclasse && (
                    <div style={{ marginBottom: 20, padding: 15, background: '#253b50', borderRadius: 6, border: '1px solid #64b5f6' }}>
                        <h3 className="section-subtitle" style={{ marginTop: 0, color: '#64b5f6' }}>{habilidadeComSubclasse.nome}</h3>
                        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                            {opcoesSubclasse.map(opcao => (
                                <div key={opcao} style={{ flex: 1, minWidth: 180 }}>
                                    <button onClick={() => setSubclasseEmEdicao(opcao)} className={`btn-action ${subclasseEmEdicao === opcao ? 'selected' : ''}`} style={{ width: '100%', background: subclasseEmEdicao === opcao ? '#4caf50' : '#333', border: subclasseEmEdicao === opcao ? '1px solid #fff' : '1px solid #555', color: 'white', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                                        {subclasseEmEdicao === opcao && <T20Icon name="check" size={14} />}{opcao}
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
                         {["Dracônica", "Feérica", "Rubra", "Abençoada"].map(l => (
                             <button key={l} onClick={() => setLinhagemEmEdicao(l)} className={`btn-action ${linhagemEmEdicao === l ? 'selected' : ''}`} style={{ flex: 1, minWidth: 100, background: linhagemEmEdicao === l ? '#4caf50' : '#333', border: linhagemEmEdicao === l ? '1px solid #fff' : '1px solid #555', color: 'white' }}>{l}</button>
                         ))}
                     </div>
                     {linhagemEmEdicao === "Abençoada" && (
                         <p style={{ margin: '10px 0 0', fontSize: '0.78rem', color: '#f3d5ff' }}>
                             <strong>Deuses de Arton:</strong> Escolha um deus maior (Básica: +1 magia divina de 1º círculo e 1 poder concedido no 2º nv sem precisar ser devoto; Aprimorada: –1 PM em magias divinas de círculo ≤ Sab e 2º–3º círculos; Superior: +1 Sab e 4º–5º círculos).
                         </p>
                     )}
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
                {ficha.cabecalho.deus && infoDeus && (() => {
                    const classesComDevotoFiel = ['Clérigo', 'Druida', 'Paladino', 'Frade', 'Ermitão'];
                    const temDevotoFiel =
                        classesComDevotoFiel.includes(classeAtual) ||
                        habilidadesAutomaticas.some((h: any) => (h.nome || '').toLowerCase().includes('devoto fiel')) ||
                        (ficha.habilidades || []).some((h: any) => (h.nome || '').toLowerCase().includes('devoto fiel'));
                    const ehPanteao = ['panteão', 'panteao', 'arton', 'bem'].includes((ficha.cabecalho.deus || '').trim().toLowerCase());
                    const qtdSlotsDevocao = ehPanteao
                        ? 0
                        : 1 + (temDevotoFiel ? 1 : 0) + (fundamentalistaEmEdicao ? 1 : 0);
                    const fontesResumo: string[] = ['1 base'];
                    if (temDevotoFiel) fontesResumo.push('+1 Devoto Fiel');
                    if (fundamentalistaEmEdicao) fontesResumo.push('+1 Fundamentalista');

                    return (
                        <div className="origem-box" style={{ borderColor: '#ffd700', background: '#2a2a20', marginBottom: 20 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                                <h3 className="section-subtitle" style={{ margin: 0, color: '#ffd700' }}>
                                    Devoção: {ficha.cabecalho.deus}
                                </h3>
                                {!ehPanteao && (
                                    <span style={{ fontSize: '0.76rem', color: '#fde68a', background: 'rgba(255, 215, 0, 0.14)', border: '1px solid rgba(255, 215, 0, 0.35)', borderRadius: 999, padding: '2px 10px', fontWeight: 600 }}>
                                        {qtdSlotsDevocao} Poder(es) Concedido(s) ({fontesResumo.join(' ')})
                                    </span>
                                )}
                            </div>

                            {!ehPanteao && (
                                <label
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: 8,
                                        marginBottom: 12,
                                        padding: '8px 10px',
                                        borderRadius: 6,
                                        background: fundamentalistaEmEdicao ? 'rgba(245, 158, 11, 0.18)' : 'rgba(0, 0, 0, 0.25)',
                                        border: `1px solid ${fundamentalistaEmEdicao ? '#f59e0b' : '#444'}`,
                                        cursor: 'pointer',
                                        fontSize: '0.8rem',
                                        color: fundamentalistaEmEdicao ? '#fde68a' : '#ccc',
                                    }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={fundamentalistaEmEdicao}
                                        onChange={e => {
                                            const ativo = e.target.checked;
                                            setFundamentalistaEmEdicao(ativo);
                                            if (!ativo) {
                                                const maxNovo = 1 + (temDevotoFiel ? 1 : 0);
                                                setDevocaoEmEdicao(prev => prev.slice(0, maxNovo));
                                            }
                                        }}
                                    />
                                    <span>
                                        <strong>Fundamentalista</strong> <span style={{ color: '#94a3b8' }}>(Deuses de Arton)</span> — Segue as Obrigações &amp; Restrições Fundamentalistas e libera <strong>+1 Poder Concedido</strong>.
                                    </span>
                                </label>
                            )}

                            {Array.from({ length: qtdSlotsDevocao }).map((_, idx) => {
                                const valorSlot = devocaoEmEdicao[idx] || '';
                                return (
                                    <div key={idx} style={{ marginBottom: 8, display: 'flex', gap: 8, alignItems: 'center' }}>
                                        <label style={{ minWidth: 145, fontSize: '0.84rem', color: '#eee' }}>
                                            Poder Concedido #{idx + 1}:
                                        </label>
                                        <input value={valorSlot} readOnly className="input-dark" placeholder="Selecione..." style={{ flex: 1 }} />
                                        <button
                                            type="button"
                                            onClick={() => abrirSeletor(
                                                'poder',
                                                `Poderes de ${ficha.cabecalho.deus} (#${idx + 1})`,
                                                infoDeus.poderes,
                                                undefined,
                                                (val) => {
                                                    setDevocaoEmEdicao(prev => {
                                                        const next = [...prev];
                                                        next[idx] = val;
                                                        return next;
                                                    });
                                                },
                                                getBlacklistGlobal(valorSlot)
                                            )}
                                            className="btn-action"
                                            style={{ background: '#ffd700', color: 'black' }}
                                        >
                                            Selecionar
                                        </button>
                                        {valorSlot && (
                                            <button
                                                type="button"
                                                title="Limpar poder"
                                                onClick={() => setDevocaoEmEdicao(prev => {
                                                    const next = [...prev];
                                                    next[idx] = '';
                                                    return next;
                                                })}
                                                style={{ background: '#3a2222', color: '#ff8a80', border: '1px solid #663333', borderRadius: 4, padding: '6px 9px', cursor: 'pointer' }}
                                            >
                                                ✕
                                            </button>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    );
                })()}
                {/* 3. ORIGEM */}
                {(() => {
                    const bloqueioOrigem = habilidadesEmEdicao.find(h => h.efeitos && h.efeitos.sem_origem);
                    if (bloqueioOrigem) return <div className="origem-box" style={{ border: '1px dashed #d32f2f', background: 'rgba(211, 47, 47, 0.1)', marginBottom: 20 }}><p style={{ color: '#ff8a80', margin: 0, display: 'inline-flex', alignItems: 'center', gap: '6px' }}><T20Icon name="imunidade" size={15} /> <strong>Origem Bloqueada:</strong> {bloqueioOrigem.nome}</p></div>;
                    const infoOrigemAtual = dadosOrigens?.[origemNome];
                    if (infoOrigemAtual?.regional || qtdEscolhasOrigem === 0) {
                        const periciasFixasReg: string[] = infoOrigemAtual?.pericias_fixas || [];
                        return (
                            <div className="origem-box" style={{ borderColor: '#2e7d32', background: 'rgba(46, 125, 50, 0.12)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', marginBottom: 6 }}>
                                    <h3 className="section-subtitle" style={{ margin: 0, color: '#81c784' }}>
                                        Origem Regional: {origemNome} — Benefício Único (Automático)
                                    </h3>
                                    {infoOrigemAtual?.regiao && (
                                        <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 999, background: 'rgba(46,125,50,0.35)', color: '#dcedc8' }}>
                                            {infoOrigemAtual.regiao}
                                        </span>
                                    )}
                                </div>
                                <p style={{ color: '#e2e8f0', fontSize: '0.88rem', margin: '0 0 6px', lineHeight: 1.45 }}>
                                    {infoOrigemAtual?.beneficio_texto || infoOrigemAtual?.descricao}
                                </p>
                                {periciasFixasReg.length > 0 && (
                                    <p style={{ color: '#a5d6a7', fontSize: '0.8rem', margin: '0 0 4px' }}>
                                        <strong>Perícias treinadas automaticamente:</strong> {periciasFixasReg.join(', ')} (se já for treinado pela classe, recebe +1 perícia de classe na aba de Perícias).
                                    </p>
                                )}
                                {infoOrigemAtual?.itens && (
                                    <p style={{ color: '#94a3b8', fontSize: '0.78rem', margin: 0 }}>
                                        <strong>Itens iniciais:</strong> {infoOrigemAtual.itens}
                                    </p>
                                )}
                                {/* Escolha dinâmica da própria Origem Regional (ex.: Duplo Feérico, Futura Lenda, De Outro Mundo, Cosmopolita) */}
                                <div style={{ marginTop: 10 }}>
                                    {(() => {
                                        const habsOrig = (ficha?.habilidades || []).filter(
                                            (h: any) => (h.fonte || '').startsWith('Origem:') || (infoOrigemAtual?.poder_fixo && h.nome === infoOrigemAtual.poder_fixo)
                                        );
                                        if (infoOrigemAtual?.poder_fixo && !habsOrig.some((h: any) => h.nome === infoOrigemAtual.poder_fixo)) {
                                            habsOrig.push({
                                                nome: infoOrigemAtual.poder_fixo,
                                                tipo: 'Origem',
                                                fonte: `Origem: ${origemNome}`,
                                                descricao: infoOrigemAtual.beneficio_texto || '',
                                                escolhas_aplicadas: {},
                                            });
                                        }
                                        return (
                                            <EscolhasDinamicasPanel
                                                titulo={`Configurar ${origemNome}`}
                                                ficha={ficha}
                                                habilidades={habsOrig.map((h: any) => ({
                                                    ...h,
                                                    escolhas_aplicadas: {
                                                        ...(h.escolhas_aplicadas || {}),
                                                        ...((poderesEscolhasEmEdicao || {})[h.nome] || {}),
                                                    },
                                                }))}
                                                dadosEscolhas={dadosEscolhas}
                                                dadosHabilidadesClasse={dadosHabilidadesClasse}
                                                dadosMagias={dadosMagias}
                                                listaPoderes={listaPoderesGerais}
                                                onChangeEscolha={(habNome, chave, valor) => {
                                                    updatePoderEscolha(habNome, chave, valor);
                                                }}
                                            />
                                        );
                                    })()}
                                </div>
                            </div>
                        );
                    }
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
                            updateRacialChoiceMulti={updateRacialChoiceMulti}
                            getBlacklistGlobal={getBlacklistGlobal}
                            getNomeHabilidade={getNomeHabilidade}
                            poderesDoDeus={poderesDoDeus}
                            listaPericias={Object.keys(ficha?.pericias || {})}
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
                                        const opcoesList = Array.isArray(g.opcoes) ? g.opcoes : [];
                                        if (opcoesList.length === 0) return null;
                                        return (
                                            <div key={g.chave} style={{ display: 'flex', gap: 10, alignItems: 'center', width: '100%', marginTop: 6, marginLeft: 35 }}>
                                                <label style={{ fontSize: '0.8rem', color: '#aaa', minWidth: 110 }}>{g.rotulo}:</label>
                                                <select className="input-dark" value={valorEscolha} onChange={e => updatePoderEscolha(valorAtual, g.chave, e.target.value)} style={{ flex: 1 }}>
                                                    <option value="">Selecionar...</option>
                                                    {opcoesList.map((o: any) => {
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

                {/* 7. ESCOLHAS DE RAÇA & OUTRAS HABILIDADES (Suplementos) */}
                <div style={{ marginTop: 20 }}>
                    <EscolhasDinamicasPanel
                        titulo="Escolhas de Raça & Outras Habilidades"
                        ficha={ficha}
                        habilidades={[
                            ...(habilidadesEmEdicao || []),
                            ...((ficha?.habilidades || []).filter(
                                (h: any) =>
                                    !(habilidadesEmEdicao || []).some((e: any) => e.nome === h.nome) &&
                                    !((dadosOrigens?.[origemNome]?.regional || qtdEscolhasOrigem === 0) && (h.fonte || '').startsWith('Origem:'))
                            )),
                        ].map((h: any) => ({
                            ...h,
                            escolhas_aplicadas: {
                                ...(h.escolhas_aplicadas || {}),
                                ...((poderesEscolhasEmEdicao || {})[h.nome] || {}),
                            },
                        }))}
                        dadosEscolhas={dadosEscolhas}
                        dadosHabilidadesClasse={dadosHabilidadesClasse}
                        dadosMagias={dadosMagias}
                        listaPoderes={listaPoderesGerais}
                        onChangeEscolha={(habNome, chave, valor) => {
                            updatePoderEscolha(habNome, chave, valor);
                            const idx = (habilidadesEmEdicao || []).findIndex((h: any) => h.nome === habNome);
                            if (idx !== -1) {
                                updateRacialChoice(idx, chave, valor);
                            }
                        }}
                    />
                </div>

                <button className="btn-apply-changes" onClick={onSave} style={{ marginTop: 30, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                    <T20Icon name="salvar" size={16} /> Salvar Todas as Alterações
                </button>
            </div>
        </div>
    );
};
