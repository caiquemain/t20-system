import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../Ficha.css';
import { useFicha } from '../hooks/useFicha';

// Componentes Modulares
import { PowerSelectorModal } from '../components/PowerSelectorModal';
import { AbilityConfigModal } from '../components/AbilityConfigModal';
import { GrimorioModal } from '../components/GrimorioModal';
import { AttributeCard } from '../components/AttributeCard';
import { SkillList } from '../components/SkillList';
import { StatusBars } from '../components/StatusBars';
import { RacialAttributeModal } from '../components/RacialAttributeModal';

// Tipos
import type { Magia } from '../types';

// --- REGRAS DE SISTEMA (T20 Jogo do Ano) ---
const PONTOS_INICIAIS = 10;

const MAPA_ATTR_KEY: Record<string, string> = {
    'forca': 'for', 'destreza': 'des', 'constituicao': 'con',
    'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car'
};

const TABELA_CUSTO: Record<string, number> = {
    "-1": -1, "0": 0, "1": 1, "2": 2, "3": 4, "4": 7
};

// Metadados de Raças (Fallback para UI)
const RACAS_METADATA: Record<string, { attrs: Record<string, number>, escolhas: number }> = {
    "Anão": { attrs: { con: 2, sab: 1, des: -1 }, escolhas: 0 },
    "Dahllan": { attrs: { sab: 2, des: 1, int: -1 }, escolhas: 0 },
    "Elfo": { attrs: { int: 2, des: 1, con: -1 }, escolhas: 0 },
    "Goblin": { attrs: { des: 2, int: 1, car: -1 }, escolhas: 0 },
    "Humano": { attrs: {}, escolhas: 3 },
    "Lefou": { attrs: { car: -1 }, escolhas: 3 },
    "Minotauro": { attrs: { for: 2, con: 1, sab: -1 }, escolhas: 0 },
    "Qareen": { attrs: { car: 2, int: 1, sab: -1 }, escolhas: 0 },
    "Golem": { attrs: { for: 2, con: 1, car: -1 }, escolhas: 0 },
    "Hynne": { attrs: { des: 2, car: 1, for: -1 }, escolhas: 0 },
    "Kliren": { attrs: { int: 2, car: 1, for: -1 }, escolhas: 0 },
    "Medusa": { attrs: { des: 2, car: 1, sab: -1 }, escolhas: 0 },
    "Meio-Elfo": { attrs: { int: 1 }, escolhas: 2 },
    "Osteon": { attrs: { con: -1 }, escolhas: 3 },
    "Sereia/Tritão": { attrs: {}, escolhas: 3 },
    "Sílfide": { attrs: { car: 2, des: 1, for: -2 }, escolhas: 0 },
    "Suraggel (Aggelus)": { attrs: { sab: 2, car: 1 }, escolhas: 0 },
    "Suraggel (Sulfure)": { attrs: { des: 2, int: 1 }, escolhas: 0 },
    "Trog": { attrs: { con: 2, for: 1, int: -1 }, escolhas: 0 }
};

function Ficha() {
    const { id } = useParams();
    const navigate = useNavigate();

    const {
        ficha, loading,
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias,
        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes,

        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,

        updateFicha,
        handleAtributoBaseChange,
        montarHabilidadesParaPanel,
        handleSaveEscolhas
    } = useFicha(id);

    // Estados Locais
    const [escolhasRaciais, setEscolhasRaciais] = useState<string[]>([]);
    const [showRacialModal, setShowRacialModal] = useState(false);
    const [showGrimorio, setShowGrimorio] = useState(false);

    const [selectorModalOpen, setSelectorModalOpen] = useState(false);
    const [selectorConfig, setSelectorConfig] = useState<any>({});

    // Sincronização Inicial do Estado Racial
    useEffect(() => {
        if (ficha) {
            setEscolhasRaciais(ficha.escolhas_atributos_raciais || []);
        }
    }, [ficha?.cabecalho.raca, ficha?.escolhas_atributos_raciais]);

    const handleSalvarAtributosRaciais = () => {
        updateFicha({ escolhas_atributos_raciais: escolhasRaciais });
        setShowRacialModal(false);
    };

    // --- CORREÇÃO: Função auxiliar robusta para abrir seletores ---
    const abrirSeletor = (
        tipo: string,
        titulo: string,
        listaRestrita: string[] = [],
        categoriaFixa: string | undefined = undefined,
        onConfirm?: (val: string) => void,
        itensBloqueados: string[] = [] // Recebe a Blacklist
    ) => {
        // Define o modo corretamente
        let tipoModo = 'ambos';
        if (tipo === 'pericia') tipoModo = 'pericia';
        else if (tipo === 'poder') tipoModo = 'poder';
        else if (tipo === 'ambos') tipoModo = 'ambos';

        setSelectorConfig({
            tipo: tipoModo,
            titulo,
            listaRestrita,
            categoriaFixa,
            itensBloqueados, // Salva no estado para passar pro modal
            callback: (val: string) => {
                if (onConfirm) onConfirm(val);
                setSelectorModalOpen(false);
            }
        });
        setSelectorModalOpen(true);
    };

    if (loading || !ficha) return <div className="loading-screen">Carregando grimório...</div>;

    // --- CÁLCULOS ---
    const calcularPontosGastos = () => {
        let gastos = 0;
        Object.values(ficha.atributos_base).forEach(val => gastos += TABELA_CUSTO[String(val)] || 0);
        return gastos;
    };
    const pontosRestantes = PONTOS_INICIAIS - calcularPontosGastos();

    const racaNome = ficha.cabecalho.raca;
    const infoRacaAtual = dadosRacas?.[racaNome] || RACAS_METADATA[racaNome] || { attrs: {}, escolhas: 0 };
    const qtdEscolhasRacial = infoRacaAtual.escolhas || 0;

    const toggleRacialChoice = (attrKey: string) => {
        const shortKey = MAPA_ATTR_KEY[attrKey];
        const valorFixo = infoRacaAtual.attrs?.[shortKey] || 0;
        if (valorFixo !== 0) return;

        if (escolhasRaciais.includes(attrKey)) {
            setEscolhasRaciais(prev => prev.filter(k => k !== attrKey));
        } else {
            if (escolhasRaciais.length < qtdEscolhasRacial) {
                setEscolhasRaciais(prev => [...prev, attrKey]);
            }
        }
    };

    // --- MAGIAS ---
    const handleAprenderMagias = (novas: Magia[]) => {
        if (!ficha) return;
        const listaAtual = ficha.combate.magias || [];
        const novasFiltradas = novas.filter(n => !listaAtual.some(a => a.nome === n.nome));
        updateFicha({ combate: { ...ficha.combate, magias: [...listaAtual, ...novasFiltradas] } });
    };

    const removerMagia = (nomeMagia: string) => {
        if (!ficha) return;
        const novaLista = ficha.combate.magias.filter(m => m.nome !== nomeMagia);
        updateFicha({ combate: { ...ficha.combate, magias: novaLista } });
    };

    const origemNome = ficha.cabecalho.origem;
    const infoOrigem = dadosOrigens ? dadosOrigens[origemNome] : null;

    return (
        <div className="ficha-container">

            {/* MODAL CONFIG (HABILIDADES) */}
            <AbilityConfigModal
                isOpen={showHabilidadesPanel}
                onClose={() => setShowHabilidadesPanel(false)}
                onSave={handleSaveEscolhas}
                ficha={ficha}
                origemNome={origemNome}
                qtdEscolhasOrigem={infoOrigem?.qtd_escolhas || 2}
                listaBeneficiosOrigem={infoOrigem?.beneficios_lista || []}
                classeAtual={ficha.classes[0]?.nome}
                nivelAtual={ficha.classes[0]?.nivel || 1}
                dadosHabilidadesClasse={dadosHabilidadesClasse}
                origemBeneficiosEmEdicao={origemBeneficiosEmEdicao}
                setOrigemBeneficiosEmEdicao={setOrigemBeneficiosEmEdicao}
                habilidadesEmEdicao={habilidadesEmEdicao}
                setHabilidadesEmEdicao={setHabilidadesEmEdicao}
                classPowersEmEdicao={classPowersEmEdicao}
                setClassPowersEmEdicao={setClassPowersEmEdicao}
                abrirSeletor={abrirSeletor}
            />

            {/* MODAL GRIMÓRIO */}
            <GrimorioModal
                isOpen={showGrimorio}
                onClose={() => setShowGrimorio(false)}
                onLearn={handleAprenderMagias}
                dadosMagias={dadosMagias}
                magiasConhecidas={ficha.combate.magias || []}
            />

            {/* MODAL DE SELEÇÃO GENÉRICO */}
            <PowerSelectorModal
                isOpen={selectorModalOpen}
                onClose={() => setSelectorModalOpen(false)}
                onSelect={selectorConfig.callback}

                // --- NOVA PROP ---
                ficha={ficha}
                // ----------------

                listaPoderes={listaPoderes}
                listaPericias={listaTodasPericias}
                tipoEscolha={selectorConfig.tipo}
                titulo={selectorConfig.titulo}
                listaRestrita={selectorConfig.listaRestrita}
                categoriaFixa={selectorConfig.categoriaFixa}
                itensBloqueados={selectorConfig.itensBloqueados}
            />

            {/* MODAL ATRIBUTOS RACIAIS */}
            <RacialAttributeModal
                isOpen={showRacialModal}
                onClose={() => setShowRacialModal(false)}
                onConfirm={handleSalvarAtributosRaciais}
                racaNome={racaNome}
                qtdEscolhas={qtdEscolhasRacial}
                escolhasAtuais={escolhasRaciais}
                onToggle={toggleRacialChoice}
                atributos={ficha.atributos}
                infoRacaAtual={infoRacaAtual}
            />

            {/* HEADER */}
            <header className="ficha-header">
                <button className="btn-back" onClick={() => navigate('/')}>← Voltar</button>
                <div className="header-inputs">
                    <input className="input-nome" value={ficha.cabecalho.nome} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, nome: e.target.value } })} />
                    <div className="header-sub">
                        <select className="select-header" value={ficha.cabecalho.raca} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, raca: e.target.value } })}>{listaRacas.map(r => <option key={r} value={r}>{r}</option>)}</select>
                        <span>•</span>
                        <select className="select-header" value={ficha.cabecalho.origem} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, origem: e.target.value }, escolhas_origem: [] })}>{listaOrigens.map(o => <option key={o} value={o}>{o}</option>)}</select>
                        <span>•</span>
                        <select className="select-header" value={ficha.classes[0]?.nome} onChange={e => {
                            const novasClasses = [...ficha.classes];
                            novasClasses[0] = { ...novasClasses[0], nome: e.target.value };
                            updateFicha({ classes: novasClasses });
                        }}>
                            {listaClasses.map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                        <input className="input-nivel" type="number" value={ficha.classes[0]?.nivel} onChange={e => { const nc = [...ficha.classes]; nc[0].nivel = parseInt(e.target.value); updateFicha({ classes: nc }); }} />
                    </div>
                </div>
            </header>

            <div className="ficha-grid">
                {/* COLUNA 1 */}
                <div className="col-stats">
                    <div className="section-card">
                        <h3 className="section-title">Atributos</h3>
                        <div className="points-panel">
                            <span className="points-label">Pontos</span>
                            <span className={`points-value ${pontosRestantes < 0 ? 'error' : ''}`}>{pontosRestantes} / {PONTOS_INICIAIS}</span>
                        </div>

                        {qtdEscolhasRacial > 0 && (
                            <button
                                className={`btn-config-racial ${escolhasRaciais.length < qtdEscolhasRacial ? 'pendente' : ''}`}
                                onClick={() => setShowRacialModal(true)}
                            >
                                <span>🧬 Atributos Raciais ({racaNome})</span>
                                <span>{escolhasRaciais.length}/{qtdEscolhasRacial}</span>
                            </button>
                        )}

                        <div className="atributos-grid">
                            {Object.entries(ficha.atributos).map(([key, valTotalBackend]) => {
                                // @ts-ignore
                                const valBase = ficha.atributos_base[key];
                                const shortKey = MAPA_ATTR_KEY[key];

                                const racialFixo = infoRacaAtual.attrs?.[shortKey] || 0;
                                const isEscolhido = escolhasRaciais.includes(key);
                                const racialTotal = racialFixo + (isEscolhido ? 1 : 0);
                                const canChooseRacial = qtdEscolhasRacial > 0 && racialFixo === 0;
                                const isRacialDisabled = escolhasRaciais.length >= qtdEscolhasRacial;

                                const outrosMods = (valTotalBackend - valBase - racialTotal);
                                const valorTotalExibicao = valBase + racialTotal + outrosMods;

                                return (
                                    <AttributeCard
                                        key={key}
                                        attrKey={key}
                                        valBase={valBase}
                                        valTotal={valorTotalExibicao}
                                        racialFixo={racialFixo}
                                        isRacialChosen={isEscolhido}
                                        canChooseRacial={canChooseRacial}
                                        isRacialDisabled={isRacialDisabled}
                                        onBaseChange={(k, delta) => handleAtributoBaseChange(k, String(valBase + delta))}
                                        onToggleRacial={toggleRacialChoice}
                                    />
                                );
                            })}
                        </div>
                    </div>

                    <StatusBars ficha={ficha} />
                </div>

                {/* COLUNA 2 */}
                <div className="col-inventory">
                    <div className="section-card">
                        <h3 className="section-title">Equipamento</h3>
                        <p style={{ color: '#777', textAlign: 'center' }}>Carga: {ficha.inventario.carga_total} / {ficha.inventario.carga_maxima}</p>
                    </div>

                    <div className="section-card" style={{ marginTop: '25px' }}>
                        <h3 className="section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            Habilidades
                            <button className="btn-toggle-racial" style={{ width: 'auto', padding: '4px 10px', fontSize: '0.8rem', margin: 0 }} onClick={montarHabilidadesParaPanel}>⚙️ Configurar</button>
                        </h3>
                        <div style={{ maxHeight: '500px', overflowY: 'auto', paddingRight: '5px' }}>
                            {ficha.habilidades.map((hab, i) => (
                                <div key={i} className="habilidade-row">
                                    <strong>{hab.nome}</strong> <span style={{ fontSize: '0.75em', color: '#888', float: 'right' }}>({hab.tipo})</span>
                                    <p style={{ fontSize: '0.85em', color: '#ccc', margin: '4px 0' }}>{hab.descricao}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* COLUNA 3 */}
                <div className="col-skills">
                    <SkillList
                        ficha={ficha}
                        dadosClasses={dadosClasses}
                        updateFicha={updateFicha}
                        listaTodasPericias={listaTodasPericias}
                    />
                </div>
            </div>

            {/* GRIMÓRIO */}
            <div className="section-card full-width" style={{ marginTop: 20 }}>
                <h3 className="section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    Grimório
                    <button className="btn-toggle-racial" style={{ width: 'auto', padding: '6px 12px', margin: 0 }} onClick={() => setShowGrimorio(true)}>+ Adicionar Magias</button>
                </h3>

                {ficha.combate.magias && ficha.combate.magias.length > 0 ? (
                    <div className="magias-list-sheet">
                        {ficha.combate.magias.map((magia, idx) => (
                            <div key={idx} className="mini-spell-card">
                                <div className="mini-spell-header">
                                    <span className="circle-badge">{magia.circulo}º</span>
                                    <span className="spell-name">{magia.nome}</span>
                                    <button className="btn-remove-mini" onClick={() => removerMagia(magia.nome)} title="Remover">×</button>
                                </div>
                                <div className="mini-spell-info">
                                    <span>{magia.execucao}</span> • <span>{magia.alcance}</span> • <span style={{ color: '#42a5f5' }}>{magia.custo_pm} PM</span>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p style={{ color: '#777', textAlign: 'center', padding: 20, fontStyle: 'italic' }}>Nenhuma magia aprendida.</p>
                )}
            </div>
        </div>
    );
}

export default Ficha;