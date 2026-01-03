import React, { useState, useEffect } from 'react';

interface RacialRowProps {
    hab: any;
    index: number;
    dadosHabilidadesRaciais: any;
    listaPoderesGerais: any[];
    dadosMagias: any;
    dadosOrigens: any;
    abrirSeletor: (tipo: string, titulo: string, listaRestrita?: string[], categoriaFixa?: string, onConfirm?: (val: string) => void, itensBloqueados?: string[]) => void;
    updateRacialChoice: (idx: number, key: string, val: any) => void;
    getBlacklistGlobal: (ignorar?: string) => string[];
    getNomeHabilidade: (id: string) => string;
    poderesDoDeus: string[];
    listaPericias: string[];
}

export const RacialAbilityRow: React.FC<RacialRowProps> = ({
    hab, index, dadosHabilidadesRaciais, listaPoderesGerais, dadosMagias, dadosOrigens,
    abrirSeletor, updateRacialChoice, getBlacklistGlobal, getNomeHabilidade, poderesDoDeus,
    listaPericias
}) => {
    const [modoEscolha, setModoEscolha] = useState<'pericia' | 'poder' | 'racial'>('pericia');

    // --- 1. PREPARAÇÃO DOS DADOS ---
    let defOriginal = null;
    if (dadosHabilidadesRaciais) {
        if (dadosHabilidadesRaciais[hab.nome]) {
            defOriginal = dadosHabilidadesRaciais[hab.nome];
        } else {
            defOriginal = Object.values(dadosHabilidadesRaciais).find((d: any) => d.nome === hab.nome);
        }
    }
    const efeitos = { ...(defOriginal?.efeitos || {}), ...(hab.efeitos || {}) };

    // --- 2. HELPERS DE FILTROS ---
    const getPoderesGeraisValidos = () => {
        return listaPoderesGerais.filter(p => {
            const t = (p.tipo || p.categoria || "").toString();
            if (p.is_general) return true;

            const grupos = ["Combate", "Destino", "Magia", "Tormenta"];
            const ehPermitido = grupos.some(g => t.includes(g));
            const ehProibido = t.includes("Classe") || t.includes("Origem") || t.includes("Racial") || t.includes("Raça") || t.includes("Concedido");
            const isConcedido = t.includes("Concedido") || p.categoria === "Poder Concedido";
            if (isConcedido && poderesDoDeus.includes(p.nome)) return true;

            return ehPermitido && !ehProibido;
        }).map(p => p.nome).sort();
    };

    const getListaPoderesTormenta = () => {
        return listaPoderesGerais.filter(p => {
            const t = (p.tipo || p.categoria || "").toString();
            return t.includes("Tormenta");
        }).map(p => p.nome).sort();
    };

    const getListaPoderesEOrigens = () => {
        const nomesGerais = listaPoderesGerais.filter(p => {
            const t = (p.tipo || p.categoria || "").toString();
            return !t.includes("Racial") && !t.includes("Raça") && !t.includes("Concedido");
        }).map(p => p.nome);

        const nomesOrigem = dadosOrigens ? Object.values(dadosOrigens)
            .flatMap((o: any) => o.beneficios_lista || [])
            .filter((beneficio: string) => !listaPericias.includes(beneficio))
            : [];

        return Array.from(new Set([...nomesGerais, ...(nomesOrigem as string[])])).sort();
    };

    const getListaRaciais = () => {
        return dadosHabilidadesRaciais ? Object.values(dadosHabilidadesRaciais)
            .filter((h: any) => !h.nome.includes("Osteon") && !h.nome.includes("Memória Póstuma"))
            .map((h: any) => h.nome).sort() : [];
    };

    // --- 3. AUTO-DETECÇÃO DE ABA ---
    useEffect(() => {
        if (efeitos.pericia_ou_poder_ou_raca_escolha) {
            const val = hab.escolhas_aplicadas?.memoria_postuma;
            if (val) {
                const ehPoder = listaPoderesGerais.some((p: any) => p.nome === val);
                if (ehPoder) { setModoEscolha('poder'); return; }

                const ehRacial = dadosHabilidadesRaciais && (dadosHabilidadesRaciais[val] || Object.values(dadosHabilidadesRaciais).some((d: any) => d.nome === val));
                if (ehRacial) { setModoEscolha('racial'); return; }

                setModoEscolha('pericia');
            }
        }
        if (hab.nome === "Versátil") {
            const salvoPoder = hab.escolhas_aplicadas?.poder_geral;
            if (salvoPoder) setModoEscolha('poder');
            else if (hab.escolhas_aplicadas?.pericia_2) setModoEscolha('pericia');
        }
    }, [hab.escolhas_aplicadas, listaPoderesGerais, dadosHabilidadesRaciais, efeitos.escolha_memoria_postuma, hab.nome]);


    // ========================================================================
    // RENDERIZAÇÃO
    // ========================================================================

    const renderizadores: React.ReactNode[] = [];

    // --- A. MEIO-ELFO (Ambição Herdada) ---
    if (efeitos.poder_geral_ou_origem) {
        const qtd = efeitos.poder_geral_ou_origem || 1;
        const slots = Array.from({ length: qtd });
        const lista = getListaPoderesEOrigens();

        renderizadores.push(
            <div key="ambicao" className="sub-section" style={{ marginTop: 10 }}>
                {slots.map((_, i) => {
                    const chaveSalva = `poder_ambicao_${i}`;
                    const valorAtual = hab.escolhas_aplicadas?.[chaveSalva] || "";
                    return (
                        <div key={i} style={{ marginBottom: 10, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label style={{ fontSize: '0.85rem', color: '#ffcc80', width: 70 }}>Ambição:</label>
                            <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Poder ou Origem..." />
                            <button className="btn-action" onClick={() => abrirSeletor('poder', `Ambição #${i + 1}`, lista, undefined, (v: string) => updateRacialChoice(index, chaveSalva, v), getBlacklistGlobal(valorAtual))}>Escolher</button>
                        </div>
                    );
                })}
            </div>
        );
    }

    // --- B. BÔNUS EM PERÍCIAS (EX: LEFOU / DEFORMIDADE) - DESIGN VERSÁTIL ---
    if (efeitos.pericia_bonus_escolha) {
        let qtd = 0;
        if (typeof efeitos.pericia_bonus_escolha === 'number') {
            qtd = efeitos.pericia_bonus_escolha;
        } else {
            qtd = parseInt(efeitos.pericia_bonus_escolha);
        }

        if (!isNaN(qtd) && qtd > 0) {
            const permiteTroca = efeitos.troca_poder_tormenta === true;
            const maxTrocas = 1;

            // Conta quantas trocas já foram feitas
            let slotsComoPoder = 0;
            for (let k = 0; k < qtd; k++) {
                // Se tiver valor de poder salvo, ou se o modo estiver setado explicitamente
                if (hab.escolhas_aplicadas?.[`poder_tormenta_${k}`] || hab.escolhas_aplicadas?.[`modo_slot_${k}`] === 'poder') {
                    slotsComoPoder++;
                }
            }

            renderizadores.push(
                <div key="pericia_bonus" className="sub-section" style={{ marginTop: 10 }}>
                    {Array.from({ length: qtd }).map((_, i) => {
                        const chavePericia = `pericia_bonus_${i}`;
                        const chavePoder = `poder_tormenta_${i}`;
                        const chaveModo = `modo_slot_${i}`;

                        const valorPericia = hab.escolhas_aplicadas?.[chavePericia] || "";
                        const valorPoder = hab.escolhas_aplicadas?.[chavePoder] || "";

                        // Define o modo atual deste slot
                        const isPowerMode = !!valorPoder || hab.escolhas_aplicadas?.[chaveModo] === 'poder';

                        // Pode trocar se: O modo já é poder, OU ainda temos slots livres para troca
                        const canSwitchToPower = isPowerMode || (slotsComoPoder < maxTrocas);

                        // Função para alternar modo
                        const switchMode = (m: 'pericia' | 'poder') => {
                            if (m === 'poder' && !canSwitchToPower) return; // Bloqueia

                            // Atualiza o modo
                            updateRacialChoice(index, chaveModo, m);

                            // Limpa o valor do outro modo para não ficar lixo no banco
                            if (m === 'pericia') updateRacialChoice(index, chavePoder, "");
                            else updateRacialChoice(index, chavePericia, "");
                        };

                        return (
                            <div key={i} className="sub-section" style={{ marginTop: 8, padding: 8, border: '1px dashed #555', borderRadius: 4, background: 'rgba(0,0,0,0.2)' }}>
                                {/* LINHA 1: Label e Botões de Troca */}
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                                    <label style={{ fontSize: '0.85rem', color: isPowerMode ? '#ff5252' : '#81c784' }}>
                                        {isPowerMode ? `Slot ${i + 1}: Poder da Tormenta` : `Slot ${i + 1}: Perícia (+2)`}
                                    </label>

                                    {permiteTroca && (
                                        <div style={{ display: 'flex', gap: 5 }}>
                                            <button
                                                onClick={() => switchMode('pericia')}
                                                style={{
                                                    fontSize: '0.7rem',
                                                    padding: '3px 8px',
                                                    background: !isPowerMode ? '#00bcd4' : '#333',
                                                    color: !isPowerMode ? '#000' : '#888',
                                                    border: '1px solid #444',
                                                    cursor: 'pointer'
                                                }}
                                            >
                                                Perícia
                                            </button>
                                            <button
                                                onClick={() => switchMode('poder')}
                                                disabled={!canSwitchToPower}
                                                title={!canSwitchToPower ? "Máximo de trocas atingido" : ""}
                                                style={{
                                                    fontSize: '0.7rem',
                                                    padding: '3px 8px',
                                                    background: isPowerMode ? '#d32f2f' : '#333',
                                                    color: isPowerMode ? '#fff' : (canSwitchToPower ? '#888' : '#444'),
                                                    border: '1px solid #444',
                                                    cursor: canSwitchToPower ? 'pointer' : 'not-allowed',
                                                    opacity: canSwitchToPower ? 1 : 0.5
                                                }}
                                            >
                                                Poder
                                            </button>
                                        </div>
                                    )}
                                </div>

                                {/* LINHA 2: Input e Botão Escolher */}
                                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                                    <input
                                        value={isPowerMode ? valorPoder : valorPericia}
                                        readOnly
                                        className="input-dark"
                                        style={{ flex: 1, borderColor: isPowerMode ? '#d32f2f' : '#444' }}
                                        placeholder={isPowerMode ? "Selecione Poder..." : "Selecione Perícia..."}
                                    />
                                    {isPowerMode ? (
                                        <button
                                            className="btn-action"
                                            style={{ background: '#d32f2f' }}
                                            onClick={() => abrirSeletor(
                                                'poder',
                                                'Escolha: Poder da Tormenta',
                                                getListaPoderesTormenta(),
                                                undefined,
                                                (v) => updateRacialChoice(index, chavePoder, v),
                                                getBlacklistGlobal(valorPoder)
                                            )}
                                        >
                                            Escolher
                                        </button>
                                    ) : (
                                        <button
                                            className="btn-action"
                                            onClick={() => abrirSeletor(
                                                'pericia',
                                                'Escolha: Perícia (+2)',
                                                [],
                                                undefined,
                                                (v) => updateRacialChoice(index, chavePericia, v),
                                                getBlacklistGlobal(valorPericia)
                                            )}
                                        >
                                            Escolher
                                        </button>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            );
        }
    }

    // --- C. OSTEON (Memória Póstuma) ---
    if (efeitos.pericia_ou_poder_ou_raca_escolha) {
        const keyStore = 'memoria_postuma';
        const valorAtual = hab.escolhas_aplicadas?.[keyStore] || "";
        const listaRaciais = getListaRaciais();
        const listaGerais = getPoderesGeraisValidos();

        const mudarAbaOsteon = (novaAba: 'pericia' | 'poder' | 'racial') => setModoEscolha(novaAba);

        renderizadores.push(
            <div key="triplo" className="sub-section" style={{ marginTop: 10, padding: 10, border: '1px dashed #666', borderRadius: 4, background: 'rgba(0,0,0,0.2)' }}>
                <div style={{ display: 'flex', gap: 5, marginBottom: 10, justifyContent: 'center' }}>
                    <button onClick={() => mudarAbaOsteon('pericia')} className={`btn-tab ${modoEscolha === 'pericia' ? 'active' : ''}`} style={{ flex: 1, padding: 5, background: modoEscolha === 'pericia' ? '#00bcd4' : '#333', color: modoEscolha === 'pericia' ? 'black' : '#888' }}>Perícia</button>
                    <button onClick={() => mudarAbaOsteon('poder')} className={`btn-tab ${modoEscolha === 'poder' ? 'active' : ''}`} style={{ flex: 1, padding: 5, background: modoEscolha === 'poder' ? '#9c27b0' : '#333', color: modoEscolha === 'poder' ? 'white' : '#888' }}>Poder</button>
                    <button onClick={() => mudarAbaOsteon('racial')} className={`btn-tab ${modoEscolha === 'racial' ? 'active' : ''}`} style={{ flex: 1, padding: 5, background: modoEscolha === 'racial' ? '#ff9800' : '#333', color: modoEscolha === 'racial' ? 'black' : '#888' }}>Racial</button>
                </div>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                    <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder={`Selecione ${modoEscolha}...`} />
                    {modoEscolha === 'pericia' && <button className="btn-action" onClick={() => abrirSeletor('pericia', `Escolha: Perícia`, [], undefined, (v) => updateRacialChoice(index, keyStore, v), getBlacklistGlobal(valorAtual))}>Escolher</button>}
                    {modoEscolha === 'poder' && <button className="btn-action" style={{ background: '#9c27b0' }} onClick={() => abrirSeletor('poder', `Escolha: Poder`, listaGerais, undefined, (v) => updateRacialChoice(index, keyStore, v), getBlacklistGlobal(valorAtual))}>Escolher</button>}
                    {modoEscolha === 'racial' && <button className="btn-action" style={{ background: '#ff9800', color: 'black' }} onClick={() => abrirSeletor('poder', `Escolha: Racial`, listaRaciais, undefined, (v) => updateRacialChoice(index, keyStore, v), getBlacklistGlobal(valorAtual))}>Escolher</button>}
                </div>
            </div>
        );
    }

    // --- D. HUMANO / VERSÁTIL ---
    if (efeitos.pericia_ou_poder_escolha) {
        const isPower = modoEscolha === 'poder';
        const keyStore = isPower ? 'poder_geral' : 'pericia_2';
        const valorAtual = hab.escolhas_aplicadas?.[keyStore] || "";

        const switchMode = (m: 'pericia' | 'poder') => {
            setModoEscolha(m);
            if (m === 'pericia') updateRacialChoice(index, 'poder_geral', "");
            else updateRacialChoice(index, 'pericia_2', "");
        };

        renderizadores.push(
            <div key="duplo" className="sub-section" style={{ marginTop: 10, padding: 10, border: '1px dashed #555', borderRadius: 4 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                    <label style={{ fontSize: '0.85rem', color: '#ffd700' }}>Slot Flexível:</label>
                    <div style={{ display: 'flex', gap: 5 }}>
                        <button onClick={() => switchMode('pericia')} style={{ fontSize: '0.7rem', padding: '3px 8px', background: !isPower ? '#00bcd4' : '#333', color: !isPower ? '#000' : '#888' }}>Perícia</button>
                        <button onClick={() => switchMode('poder')} style={{ fontSize: '0.7rem', padding: '3px 8px', background: isPower ? '#9c27b0' : '#333', color: isPower ? '#fff' : '#888' }}>Poder</button>
                    </div>
                </div>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                    <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder={isPower ? "Poder Geral..." : "Perícia..."} />
                    {isPower ? (
                        <button className="btn-action" style={{ background: '#9c27b0' }} onClick={() => abrirSeletor('poder', 'Escolha: Poder Geral', getPoderesGeraisValidos(), undefined, (v) => updateRacialChoice(index, 'poder_geral', v), getBlacklistGlobal(valorAtual))}>Escolher</button>
                    ) : (
                        <button className="btn-action" onClick={() => abrirSeletor('pericia', 'Escolha: Perícia', [], undefined, (v) => updateRacialChoice(index, 'pericia_2', v), getBlacklistGlobal(valorAtual))}>Escolher</button>
                    )}
                </div>
            </div>
        );
    }

    // --- E. PERÍCIA SIMPLES ---
    if (efeitos.pericia_escolha) {
        const qtd = efeitos.pericia_escolha;
        const chaveBase = hab.nome === "Versátil" ? "pericia_1" : "pericia_escolha";

        renderizadores.push(
            <div key="pericia_simples" className="sub-section" style={{ marginTop: 10 }}>
                {Array.from({ length: qtd }).map((_, i) => {
                    const valorAtual = hab.escolhas_aplicadas?.[chaveBase] || "";
                    return (
                        <div key={i} style={{ marginBottom: 5, display: 'flex', gap: 10, alignItems: 'center' }}>
                            <label style={{ fontSize: '0.85rem', color: '#81c784', width: 70 }}>Perícia:</label>
                            <input value={valorAtual} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                            <button className="btn-action" onClick={() => abrirSeletor('pericia', `Escolha: Perícia`, [], undefined, (v) => updateRacialChoice(index, chaveBase, v), getBlacklistGlobal(valorAtual))}>Escolher</button>
                        </div>
                    )
                })}
            </div>
        );
    }

    // --- F. ATRIBUTOS ---
    if (efeitos.atributo_bonus_escolha) {
        const qtd = efeitos.atributo_bonus_escolha;
        const currentSelections = hab.escolhas_aplicadas?.atributo_bonus || [];
        const MapaAttrInv: Record<string, string> = { 'forca': 'for', 'destreza': 'des', 'constituicao': 'con', 'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car' };

        renderizadores.push(
            <div key="atributos" className="sub-section" style={{ marginTop: 10 }}>
                {Array.from({ length: qtd }).map((_, i) => (
                    <div key={i} className="selector-row" style={{ marginBottom: 5 }}>
                        <select value={currentSelections[i] || ""} onChange={(e) => {
                            const newSel = [...currentSelections]; newSel[i] = e.target.value; updateRacialChoice(index, 'atributo_bonus', newSel);
                        }} className="input-dark" style={{ width: '100%' }}>
                            <option value="">Selecione Atributo...</option>
                            {['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'].map(a => <option key={a} value={MapaAttrInv[a]} disabled={currentSelections.includes(MapaAttrInv[a]) && currentSelections[i] !== MapaAttrInv[a]}>{a.toUpperCase()}</option>)}
                        </select>
                    </div>
                ))}
            </div>
        );
    }

    // --- G. MAGIAS ---
    const configMagia = efeitos.magia_adicional_escolha;
    if (configMagia) {
        const quantidade = configMagia.quantidade || 1;
        const circulo = configMagia.circulo || 1;
        let opcoesMagias: string[] = [];
        if (dadosMagias) {
            opcoesMagias = Object.values(dadosMagias)
                // @ts-ignore
                .filter((m: any) => String(m.circulo) === String(circulo))
                // @ts-ignore
                .map((m: any) => m.nome).sort();
        }

        renderizadores.push(
            <div key="magia" className="sub-section" style={{ marginTop: 10 }}>
                <p style={{ fontSize: '0.8rem', color: '#ccc' }}>Magias ({circulo}º Círculo):</p>
                {Array.from({ length: quantidade }).map((_, i) => (
                    <div key={i} style={{ marginBottom: 5, display: 'flex', gap: 10 }}>
                        <input value={hab.escolhas_aplicadas?.[`magia_${i}`] || ""} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Magia..." />
                        <button className="btn-action" style={{ background: '#9c27b0' }} onClick={() => abrirSeletor('poder', `Magia`, opcoesMagias, undefined, (v: string) => updateRacialChoice(index, `magia_${i}`, v), [])}>Escolher</button>
                    </div>
                ))}
            </div>
        );
    }

    // --- H. LISTA RESTRITA ---
    let listaOpcoesIDs: string[] = [];
    const chaveLista = 'poder_escolha';
    if (defOriginal && defOriginal.efeitos && Array.isArray(defOriginal.efeitos[chaveLista])) {
        listaOpcoesIDs = defOriginal.efeitos[chaveLista];
    } else if (listaOpcoesIDs.length === 0 && efeitos[chaveLista] && Array.isArray(efeitos[chaveLista])) {
        listaOpcoesIDs = efeitos[chaveLista];
    }

    if (listaOpcoesIDs.length > 0 && !efeitos.pericia_ou_poder_escolha && !efeitos.pericia_ou_poder_ou_raca_escolha) {
        const qtd = efeitos.qtd_escolhas || 1;
        const rawEscolha = hab.escolhas_aplicadas?.[chaveLista] || efeitos[chaveLista];
        let escolhasAtuais: string[] = [];
        if (Array.isArray(rawEscolha)) {
            const ehAPropriaLista = rawEscolha.length === listaOpcoesIDs.length && rawEscolha.every((v: any, i: any) => v === listaOpcoesIDs[i]);
            if (!ehAPropriaLista) escolhasAtuais = rawEscolha;
        } else if (typeof rawEscolha === 'string') escolhasAtuais = [rawEscolha];

        renderizadores.push(
            <div key="restrita" className="sub-section" style={{ marginTop: 10 }}>
                {Array.from({ length: qtd }).map((_, i) => {
                    const valAtual = escolhasAtuais[i] || "";
                    const nomeExibicao = getNomeHabilidade(valAtual) || valAtual;
                    return (
                        <div key={i} style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 5 }}>
                            <input value={nomeExibicao} readOnly className="input-dark" style={{ flex: 1 }} placeholder="Selecione..." />
                            <button onClick={() => abrirSeletor('ambos', `Escolha`, listaOpcoesIDs, undefined, (val: string) => {
                                let newSel = [...escolhasAtuais];
                                while (newSel.length < qtd) newSel.push("");
                                newSel[i] = val;
                                const valorFinal = qtd === 1 ? newSel[0] : newSel.filter(x => x);
                                updateRacialChoice(index, chaveLista, valorFinal);
                            }, qtd > 1 ? escolhasAtuais : [])} className="btn-action">Escolher</button>
                        </div>
                    );
                })}
            </div>
        );
    }

    // --- I. FALLBACK GENÉRICO ---
    if (renderizadores.length === 0 && hab.precisaEscolha) {
        renderizadores.push(
            <div key="fallback" className="sub-section" style={{ marginTop: 10 }}>
                {Object.entries(hab.efeitos).map(([key, _]) => {
                    if (key.endsWith('_escolha') && !key.includes('magia') && !key.includes('imunidade')) {
                        const val = hab.escolhas_aplicadas?.[key] || '';
                        return <div key={key} style={{ marginTop: 8 }}><button onClick={() => abrirSeletor('pericia', `Escolha`, [], undefined, (v) => updateRacialChoice(index, key, v), getBlacklistGlobal(val))} className="btn-action">Escolher</button> {val}</div>
                    }
                    return null;
                })}
            </div>
        );
    }

    if (renderizadores.length > 0) {
        return (
            <div className="habilidade-item" style={{ marginBottom: 15, paddingBottom: 15, borderBottom: '1px solid #333' }}>
                <div className="hab-header" style={{ marginBottom: 10 }}>
                    <span><strong>{hab.nome}</strong></span>
                    <span style={{ color: '#00e676', fontSize: '0.8rem', marginLeft: 10 }}>CONFIGURAR</span>
                </div>
                {efeitos.descricao_extra && <p style={{ fontSize: '0.8rem', color: '#ffcc80', marginBottom: 10 }}>{efeitos.descricao_extra}</p>}
                {renderizadores}
            </div>
        );
    }

    return null;
};