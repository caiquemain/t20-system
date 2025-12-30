import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../Ficha.css';
import { useFicha } from '../hooks/useFicha';

// Componentes Modulares
import { PowerSelectorModal } from '../components/PowerSelectorModal';
import { AbilityConfigModal } from '../components/AbilityConfigModal';
import { GrimorioModal } from '../components/GrimorioModal';         // Modal de Adicionar (Estudar)
import { FullGrimorioModal } from '../components/FullGrimorioModal'; // Modal de Gerenciar (Visual Detalhado)
import { SpellDetailsModal } from '../components/SpellDetailsModal'; // Modal de Visualização Rápida (Clique Único)
import { SpellSummary } from '../components/SpellSummary';           // Resumo Compacto na Ficha
import { AttributeCard } from '../components/AttributeCard';
import { SkillList } from '../components/SkillList';
import { StatusBars } from '../components/StatusBars';
import { RacialAttributeModal } from '../components/RacialAttributeModal';

// Tipos
import type { Magia } from '../types';

const PONTOS_INICIAIS = 10;
const MAPA_ATTR_KEY: Record<string, string> = { 'forca': 'for', 'destreza': 'des', 'constituicao': 'con', 'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car' };
const TABELA_CUSTO: Record<string, number> = { "-1": -1, "0": 0, "1": 1, "2": 2, "3": 4, "4": 7 };
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

const extrairPoderesDaClasse = (dadosHabilidadesClasse: any, nomeClasse: string) => {
    return Object.values(dadosHabilidadesClasse || {})
        // @ts-ignore
        .filter((h: any) => h.classe === nomeClasse && h.tipo && h.tipo.includes("Poder de"))
        .map((h: any) => ({
            nome: h.nome,
            tipo: h.tipo,
            categoria: h.classe,
            descricao: h.descricao,
            requisitos: h.requisitos || []
        }));
};

function Ficha() {
    const { id } = useParams();
    const navigate = useNavigate();

    const {
        ficha, loading,
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias,
        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes,
        listaDeuses, dadosDeuses,
        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,
        subclasseEmEdicao, setSubclasseEmEdicao,
        devocaoEmEdicao, setDevocaoEmEdicao,
        updateFicha, handleAtributoBaseChange, montarHabilidadesParaPanel, handleSaveEscolhas
    } = useFicha(id);

    const [escolhasRaciais, setEscolhasRaciais] = useState<string[]>([]);
    const [showRacialModal, setShowRacialModal] = useState(false);

    // --- ESTADOS DO GRIMÓRIO ---
    const [showGrimorio, setShowGrimorio] = useState(false);         // Modal de Adicionar Magias
    const [showFullGrimorio, setShowFullGrimorio] = useState(false); // Modal de Gerenciar (Lista Completa)
    const [viewSpell, setViewSpell] = useState<Magia | null>(null);  // Modal de Detalhes (Visualização Rápida)

    const [selectorModalOpen, setSelectorModalOpen] = useState(false);
    const [selectorConfig, setSelectorConfig] = useState<any>({});

    useEffect(() => {
        if (ficha) {
            setEscolhasRaciais(ficha.escolhas_atributos_raciais || []);
        }
    }, [ficha?.cabecalho.raca, ficha?.escolhas_atributos_raciais]);

    const handleSalvarAtributosRaciais = () => {
        updateFicha({ escolhas_atributos_raciais: escolhasRaciais });
        setShowRacialModal(false);
    };

    const abrirSeletor = (tipo: string, titulo: string, listaRestrita: string[] = [], categoriaFixa: string | undefined = undefined, onConfirm?: (val: string) => void, itensBloqueados: string[] = []) => {
        setSelectorConfig({ tipo: tipo === 'ambos' ? 'ambos' : tipo, titulo, listaRestrita, categoriaFixa, itensBloqueados, callback: (val: string) => { if (onConfirm) onConfirm(val); setSelectorModalOpen(false); } });
        setSelectorModalOpen(true);
    };

    // --- LOGS DE DEBUG ---
    console.groupCollapsed("🔍 DEBUG: Ficha Render");
    console.log("Loading:", loading);
    console.log("Ficha:", ficha);
    console.log("Magias Disponíveis (DB):", dadosMagias ? Object.keys(dadosMagias).length : 0);
    console.groupEnd();

    if (loading || !ficha) return <div className="loading-screen">Carregando grimório...</div>;

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
        if (escolhasRaciais.includes(attrKey)) setEscolhasRaciais(prev => prev.filter(k => k !== attrKey));
        else if (escolhasRaciais.length < qtdEscolhasRacial) setEscolhasRaciais(prev => [...prev, attrKey]);
    };

    const poderesDaClasse = ficha ? extrairPoderesDaClasse(dadosHabilidadesClasse, ficha.classes[0].nome) : [];
    const poderesMistos = [...listaPoderes, ...poderesDaClasse];

    const getDeusesPermitidos = () => {
        if (!ficha) return [];
        const raca = ficha.cabecalho.raca;
        const classe = ficha.classes[0]?.nome;
        if (raca === 'Humano' || classe === 'Clérigo') return listaDeuses;
        return listaDeuses.filter(nomeDeus => {
            const dados = dadosDeuses[nomeDeus];
            if (!dados) return false;
            const permitidos = dados.devotos || [];
            if (permitidos.includes("Todos") || permitidos.includes("Quaisquer") || permitidos.includes(raca) || permitidos.includes(classe)) return true;
            if (nomeDeus === "Thwor" && ["Goblin", "Hobgoblin", "Bugbear", "Orc", "Ogro"].includes(raca)) return true;
            return false;
        });
    };
    const deusesDisponiveis = getDeusesPermitidos();

    const handleAprenderMagiaUnica = (novaMagia: Magia) => {
        if (!ficha) return;
        const listaAtual = ficha.combate.magias || [];
        if (!listaAtual.some(m => m.nome === novaMagia.nome)) {
            const novaLista = [...listaAtual, novaMagia];
            updateFicha({ combate: { ...ficha.combate, magias: novaLista } }, true);
        }
    };

    const handleRemoverMagia = (nome: string) => {
        const novasMagias = ficha.combate.magias.filter((m: any) => m.nome !== nome);
        updateFicha({ combate: { ...ficha.combate, magias: novasMagias } }, true);
    };

    const origemNome = ficha.cabecalho.origem;
    // --- LÓGICA DE BUSCA DE ORIGEM (CORRIGE BUG DE ACENTO) ---
    const getDadosOrigem = (nome: string) => {
        if (!dadosOrigens) return null;
        if (dadosOrigens[nome]) return dadosOrigens[nome];

        // Busca insensível a acentos (Ex: "Acólito" encontra "Acolito")
        const nomeNormalizado = nome.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        const chaveEncontrada = Object.keys(dadosOrigens).find(k =>
            k.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() === nomeNormalizado
        );

        return chaveEncontrada ? dadosOrigens[chaveEncontrada] : null;
    };
    const infoOrigem = getDadosOrigem(origemNome);

    const origemBloqueada = ficha.habilidades.some((h: any) => h.efeitos?.sem_origem || h.escolhas_aplicadas?.sem_origem);

    return (
        <div className="ficha-container">
            {/* --- MODAIS DE CONFIGURAÇÃO --- */}

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
                listaPoderesGerais={listaPoderes}
                dadosDeuses={dadosDeuses}
                dadosMagias={dadosMagias}
                origemBeneficiosEmEdicao={origemBeneficiosEmEdicao}
                setOrigemBeneficiosEmEdicao={setOrigemBeneficiosEmEdicao}
                habilidadesEmEdicao={habilidadesEmEdicao}
                setHabilidadesEmEdicao={setHabilidadesEmEdicao}
                classPowersEmEdicao={classPowersEmEdicao}
                setClassPowersEmEdicao={setClassPowersEmEdicao}
                subclasseEmEdicao={subclasseEmEdicao}
                setSubclasseEmEdicao={setSubclasseEmEdicao}
                devocaoEmEdicao={devocaoEmEdicao}
                setDevocaoEmEdicao={setDevocaoEmEdicao}
                abrirSeletor={abrirSeletor}
            />

            {/* MODAL 1: ADICIONAR MAGIAS (ESTUDO) */}
            <GrimorioModal
                isOpen={showGrimorio}
                onClose={() => setShowGrimorio(false)}
                onAddMagia={handleAprenderMagiaUnica}
                dadosMagias={dadosMagias}
                magiasConhecidas={ficha.combate.magias || []}
                pmAtual={ficha.status.pm.atual}
                pmMaximo={ficha.status.pm.maximo}
            />

            {/* MODAL 2: GERENCIAR GRIMÓRIO (DETALHADO + REMOVER) */}
            <FullGrimorioModal
                isOpen={showFullGrimorio}
                onClose={() => setShowFullGrimorio(false)}
                magias={ficha.combate.magias}
                onRemove={handleRemoverMagia}
                pmAtual={ficha.status.pm.atual}
                pmMaximo={ficha.status.pm.maximo}
            />

            {/* MODAL 3: DETALHES RÁPIDOS (CLIQUE NO RESUMO) */}
            <SpellDetailsModal
                magia={viewSpell}
                onClose={() => setViewSpell(null)}
                // CONECTANDO A REMOÇÃO:
                onRemove={() => {
                    if (viewSpell) {
                        handleRemoverMagia(viewSpell.nome); // Chama a função que já existe na Ficha
                        setViewSpell(null); // Fecha o modal
                    }
                }}
            />

            <PowerSelectorModal
                isOpen={selectorModalOpen}
                onClose={() => setSelectorModalOpen(false)}
                onSelect={selectorConfig.callback}
                ficha={ficha}
                listaPoderes={poderesMistos}
                listaPericias={listaTodasPericias}
                dadosMagias={dadosMagias}
                tipoEscolha={selectorConfig.tipo}
                titulo={selectorConfig.titulo}
                listaRestrita={selectorConfig.listaRestrita}
                categoriaFixa={selectorConfig.categoriaFixa}
                itensBloqueados={selectorConfig.itensBloqueados}
                subclasse={subclasseEmEdicao}
            />

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

            {/* --- HEADER --- */}
            <header className="ficha-header">
                <button className="btn-back" onClick={() => navigate('/')}>← Voltar</button>
                <div className="header-inputs">
                    <input className="input-nome" value={ficha.cabecalho.nome} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, nome: e.target.value } })} />
                    <div className="header-sub">
                        <select className="select-header" value={ficha.cabecalho.raca} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, raca: e.target.value }, escolhas_atributos_raciais: [] }, true)}>
                            {listaRacas.map(r => <option key={r} value={r}>{r}</option>)}
                        </select>
                        <span>•</span>
                        <select className="select-header" value={origemBloqueada ? "" : ficha.cabecalho.origem} disabled={origemBloqueada} style={origemBloqueada ? { opacity: 0.6, cursor: 'not-allowed', color: '#ff5252', border: '1px solid #d32f2f' } : {}} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, origem: e.target.value }, escolhas_origem: [] }, true)}>
                            {origemBloqueada ? <option value="">🚫 Sem Origem</option> : listaOrigens.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>
                        <span>•</span>
                        <select className="select-header" value={ficha.cabecalho.deus || ""} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, deus: e.target.value } }, true)} style={{ color: '#ffd700' }}>
                            <option value="">Sem Devoção</option>
                            {deusesDisponiveis.map(d => <option key={d} value={d}>{d}</option>)}
                        </select>
                        <span>•</span>
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            <select className="select-header" value={ficha.classes[0]?.nome} onChange={e => {
                                const novasClasses = [...ficha.classes];
                                novasClasses[0] = { ...novasClasses[0], nome: e.target.value, subclasse: undefined };
                                updateFicha({ classes: novasClasses, pericias: {} }, true);
                            }}>
                                {listaClasses.map(c => <option key={c} value={c}>{c}</option>)}
                            </select>
                            {ficha.classes[0]?.subclasse && <span className="subclass-badge" title="Caminho / Subclasse">{ficha.classes[0].subclasse}</span>}
                        </div>
                        <label style={{ marginLeft: 10 }}>Nível:</label>
                        <input className="input-nivel" type="number" value={ficha.classes[0]?.nivel} onChange={e => { const nc = [...ficha.classes]; nc[0].nivel = parseInt(e.target.value); updateFicha({ classes: nc }, true); }} />
                    </div>
                </div>
            </header>

            <div className="ficha-grid">
                {/* COLUNA 1: ATRIBUTOS & STATUS */}
                <div className="col-stats">
                    <div className="section-card">
                        <h3 className="section-title">Atributos</h3>
                        <div className="points-panel">
                            <span className="points-label">Pontos</span>
                            <span className={`points-value ${pontosRestantes < 0 ? 'error' : ''}`}>{pontosRestantes} / {PONTOS_INICIAIS}</span>
                        </div>
                        {qtdEscolhasRacial > 0 && (
                            <button className={`btn-config-racial ${escolhasRaciais.length < qtdEscolhasRacial ? 'pendente' : ''}`} onClick={() => setShowRacialModal(true)}>
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

                                return <AttributeCard key={key} attrKey={key} valBase={valBase} valTotal={valorTotalExibicao} racialFixo={racialFixo} isRacialChosen={isEscolhido} canChooseRacial={canChooseRacial} isRacialDisabled={isRacialDisabled} onBaseChange={(k, delta) => handleAtributoBaseChange(k, String(valBase + delta))} onToggleRacial={toggleRacialChoice} />;
                            })}
                        </div>
                    </div>
                    <StatusBars ficha={ficha} />
                    <div className="proficiencias-container" style={{ background: '#1e1e1e', padding: '10px', borderRadius: '6px', marginTop: '15px', border: '1px solid #333' }}>
                        <h4 style={{ margin: '0 0 8px 0', color: '#aaa', fontSize: '0.8rem', textTransform: 'uppercase', borderBottom: '1px solid #333', paddingBottom: '4px' }}>🛠️ Proficiências & Sentidos</h4>
                        {ficha.proficiencias && ficha.proficiencias.length > 0 ? (
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                                {ficha.proficiencias.map((item: string, idx: number) => {
                                    const isSentido = item.includes('Visão') || item.includes('Faro');
                                    const isImunidade = item.includes('Movimento') || item.includes('Imune');
                                    let bg = '#333'; let color = '#ccc'; let border = '#444';
                                    if (isSentido) { bg = 'rgba(63, 81, 181, 0.2)'; border = '#3949ab'; color = '#c5cae9'; }
                                    if (isImunidade) { bg = 'rgba(76, 175, 80, 0.2)'; border = '#2e7d32'; color = '#c8e6c9'; }
                                    return <span key={idx} style={{ background: bg, color: color, border: `1px solid ${border}`, padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '500' }}>{item}</span>;
                                })}
                            </div>
                        ) : <p style={{ color: '#555', fontStyle: 'italic', fontSize: '0.8rem', margin: 0 }}>Nenhuma listada.</p>}
                    </div>
                </div>

                {/* COLUNA 2: EQUIPAMENTO & HABILIDADES */}
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

                {/* COLUNA 3: PERÍCIAS */}
                <div className="col-skills">
                    <SkillList ficha={ficha} dadosClasses={dadosClasses} updateFicha={updateFicha} listaTodasPericias={listaTodasPericias} />
                </div>
            </div>

            {/* --- SEÇÃO GRIMÓRIO (RESUMO) --- */}
            <div className="section-card">
                <div className="section-header">
                    <h3>GRIMÓRIO</h3>
                    <div className="header-actions">
                        <span style={{ fontSize: '0.8rem', color: '#aaa', marginRight: 10 }}>PM: {ficha.status.pm.atual} / {ficha.status.pm.maximo}</span>
                        <button className="btn-small" onClick={() => setShowGrimorio(true)}>+ Adicionar</button>
                    </div>
                </div>
                <div style={{ padding: '15px' }}>
                    {/* Exibe o Resumo Compacto na tela principal */}
                    <SpellSummary
                        magias={ficha.combate.magias}
                        onOpenDetalhes={() => setShowFullGrimorio(true)}
                        onSpellClick={(m) => setViewSpell(m)}
                    />
                </div>
            </div>
        </div>
    );
}

export default Ficha;