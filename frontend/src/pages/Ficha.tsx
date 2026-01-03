import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../Ficha.css';
import { useFicha } from '../hooks/useFicha';

// Componentes Modulares
import { PowerSelectorModal } from '../components/PowerSelectorModal';
import { AbilityConfigModal } from '../components/AbilityConfigModal';
import { GrimorioModal } from '../components/GrimorioModal';
import { FullGrimorioModal } from '../components/FullGrimorioModal';
import { SpellDetailsModal } from '../components/SpellDetailsModal';
import { SpellSummary } from '../components/SpellSummary';
import { AttributeCard } from '../components/AttributeCard';
import { SkillList } from '../components/SkillList';
import { StatusBars } from '../components/StatusBars';
import { RacialAttributeModal } from '../components/RacialAttributeModal';
import { AbilityCard } from '../components/AbilityCard';

// Tipos
import type { Magia } from '../types';

const PONTOS_INICIAIS = 10;
const MAPA_ATTR_KEY: Record<string, string> = { 'forca': 'for', 'destreza': 'des', 'constituicao': 'con', 'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car' };
const TABELA_CUSTO: Record<string, number> = { "-1": -1, "0": 0, "1": 1, "2": 2, "3": 4, "4": 7 };

const RACAS_METADATA: Record<string, { attrs: Record<string, number>, escolhas: number }> = {
    "Anão": { attrs: { con: 2, sab: 1, des: -1 }, escolhas: 0 },
    "Dahllan": { attrs: { sab: 2, des: 1, int: -1 }, escolhas: 0 },
    "Duende": { attrs: {}, escolhas: 2 },
    "Eiradaan": { attrs: { sab: 2, car: 1, for: -1 }, escolhas: 0 },
    "Elfo": { attrs: { int: 2, des: 1, con: -1 }, escolhas: 0 },
    "Galokk": { attrs: { for: 1, con: 1, car: -1 }, escolhas: 1 },
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
    // ADICIONADO: Sátiro estava faltando!
    "Sátiro": { attrs: { car: 2, des: 1, sab: -1 }, escolhas: 0 },
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
        listaDeuses, dadosDeuses, dadosHabilidades,
        // [NOVO] Desestruturando o dado novo
        dadosHabilidadesRaciais,

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
    const [activeTab, setActiveTab] = useState<'atributos' | 'efeitos'>('atributos');

    // --- ESTADOS DO GRIMÓRIO ---
    const [showGrimorio, setShowGrimorio] = useState(false);
    const [showFullGrimorio, setShowFullGrimorio] = useState(false);
    const [viewSpell, setViewSpell] = useState<Magia | null>(null);

    // --- ESTADOS DE DESLOCAMENTO ESPECIAL ---
    const [isFlying, setIsFlying] = useState(false);
    const [isAquatic, setIsAquatic] = useState(false);

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

    // --- FUNÇÃO DE ATIVAÇÃO DE HABILIDADE ---
    const handleAtivarHabilidade = (custo: number, nome: string) => {
        if (!ficha) return;

        const habilidade = ficha.habilidades.find(h => h.nome === nome);
        const efeitosRaw = (habilidade?.efeitos as any) || {};
        const efeitosAtivaveis = efeitosRaw.habilidade_ativavel || {};
        const modificadores = efeitosAtivaveis.modificadores || [];

        const statusAny = ficha.status as any;
        const buffsAtuais: any[] = statusAny.buffs || [];
        const jaEstaAtivo = buffsAtuais.some((b: any) => b.origem === nome);

        let novosBuffs = [...buffsAtuais];
        let pmAtual = ficha.status.pm.atual;

        if (jaEstaAtivo) {
            novosBuffs = novosBuffs.filter((b: any) => b.origem !== nome);
            if (nome === "Asas de Borboleta") setIsFlying(false);
            if (nome === "Transformação Anfíbia") setIsAquatic(false);
            console.log(`❌ ${nome} desativado.`);
        } else {
            if (pmAtual < custo) {
                alert("Pontos de Mana insuficientes!");
                return;
            }
            pmAtual -= custo;

            if (modificadores.length > 0) {
                modificadores.forEach((mod: any) => {
                    novosBuffs.push({
                        origem: nome,
                        atributo: mod.atributo,
                        valor: mod.valor,
                        duracao: efeitosAtivaveis.duracao || "Cena"
                    });
                });
            }
            else if (nome === "Asas de Borboleta") setIsFlying(true);
            else if (nome === "Transformação Anfíbia") setIsAquatic(true);

            console.log(`⚡ ${nome} ativado!`);
        }

        updateFicha({
            status: {
                ...ficha.status,
                pm: { ...ficha.status.pm, atual: pmAtual },
                // @ts-ignore
                buffs: novosBuffs
            }
        }, true);
    };

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
    const getDadosOrigem = (nome: string) => {
        if (!dadosOrigens) return null;
        if (dadosOrigens[nome]) return dadosOrigens[nome];
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
                dadosOrigens={dadosOrigens}
                dadosDeuses={dadosDeuses}
                dadosMagias={dadosMagias}
                // [NOVO] Passando os dados de sub-habilidades para o Modal
                dadosHabilidadesRaciais={dadosHabilidadesRaciais}

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

            <GrimorioModal
                isOpen={showGrimorio}
                onClose={() => setShowGrimorio(false)}
                onAddMagia={handleAprenderMagiaUnica}
                dadosMagias={dadosMagias}
                magiasConhecidas={ficha.combate.magias || []}
                pmAtual={ficha.status.pm.atual}
                pmMaximo={ficha.status.pm.maximo}
            />

            <FullGrimorioModal
                isOpen={showFullGrimorio}
                onClose={() => setShowFullGrimorio(false)}
                magias={ficha.combate.magias}
                onRemove={handleRemoverMagia}
                pmAtual={ficha.status.pm.atual}
                pmMaximo={ficha.status.pm.maximo}
            />

            <SpellDetailsModal
                magia={viewSpell}
                onClose={() => setViewSpell(null)}
                onRemove={() => { if (viewSpell) { handleRemoverMagia(viewSpell.nome); setViewSpell(null); } }}
            />

            <PowerSelectorModal
                isOpen={selectorModalOpen}
                onClose={() => setSelectorModalOpen(false)}
                onSelect={selectorConfig.callback}
                ficha={ficha}
                listaPoderes={poderesMistos}
                listaPericias={listaTodasPericias}
                dadosMagias={dadosMagias}
                dadosHabilidades={dadosHabilidades}
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
                    {/* Linha 1: Nome */}
                    <input
                        className="input-nome"
                        placeholder="Nome do Personagem"
                        value={ficha.cabecalho.nome}
                        onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, nome: e.target.value } })}
                    />

                    {/* Linha 2: Dados Principais */}
                    <div className="header-sub">
                        {/* Raça */}
                        <select className="select-header" value={ficha.cabecalho.raca} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, raca: e.target.value }, escolhas_atributos_raciais: [] }, true)}>
                            {listaRacas.map(r => <option key={r} value={r}>{r}</option>)}
                        </select>
                        <span>•</span>
                        {/* Origem */}
                        <select className="select-header" value={origemBloqueada ? "" : ficha.cabecalho.origem} disabled={origemBloqueada} style={origemBloqueada ? { opacity: 0.6, cursor: 'not-allowed', color: '#ff5252', border: '1px solid #d32f2f' } : {}} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, origem: e.target.value }, escolhas_origem: [] }, true)}>
                            {origemBloqueada ? <option value="">🚫 Sem Origem</option> : listaOrigens.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>
                        <span>•</span>
                        {/* Deus */}
                        <select className="select-header" value={ficha.cabecalho.deus || ""} onChange={e => updateFicha({ cabecalho: { ...ficha.cabecalho, deus: e.target.value } }, true)} style={{ color: '#ffd700' }}>
                            <option value="">Sem Devoção</option>
                            {deusesDisponiveis.map(d => <option key={d} value={d}>{d}</option>)}
                        </select>
                        <span>•</span>
                        {/* Classe */}
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
                        {/* Nível */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: 5, marginLeft: 10 }}>
                            <label style={{ fontSize: '0.8rem', color: '#888' }}>NV</label>
                            <input className="input-nivel" type="number" min={1} max={20} value={ficha.classes[0]?.nivel} onChange={e => { const nc = [...ficha.classes]; nc[0].nivel = parseInt(e.target.value); updateFicha({ classes: nc }, true); }} />
                        </div>

                        {/* --- NOVO: TAMANHO E DESLOCAMENTO --- */}
                        <div className="header-divider">|</div>
                        <div className="header-info-tag" title="Tamanho">
                            <span className="tag-label">TAM</span>
                            <span className="tag-value" style={{ color: ficha.descricao.tamanho === 'Médio' ? '#fff' : '#ffeb3b' }}>
                                {ficha.descricao.tamanho || "Médio"}
                            </span>
                        </div>
                        <div className="header-info-tag" title="Deslocamento">
                            <span className="tag-label">DESL</span>
                            <span className="tag-value">{ficha.status.deslocamento}m</span>
                        </div>
                    </div>
                </div>
            </header>

            {/* --- NAVEGAÇÃO INTERNA DA FICHA (TABS) --- */}
            <div className="ficha-tabs" style={{ display: 'flex', gap: 10, padding: '0 20px', marginBottom: 15, borderBottom: '1px solid #333' }}>
                <button
                    className={`tab-btn ${activeTab === 'atributos' ? 'active' : ''}`}
                    onClick={() => setActiveTab('atributos')}
                    style={{ background: 'transparent', border: 'none', color: activeTab === 'atributos' ? '#ffd700' : '#888', borderBottom: activeTab === 'atributos' ? '2px solid #ffd700' : 'none', padding: '10px 20px', cursor: 'pointer', fontWeight: 'bold' }}
                >
                    ATRIBUTOS & PERÍCIAS
                </button>
                <button
                    className={`tab-btn ${activeTab === 'efeitos' ? 'active' : ''}`}
                    onClick={() => setActiveTab('efeitos')}
                    style={{ background: 'transparent', border: 'none', color: activeTab === 'efeitos' ? '#2196f3' : '#888', borderBottom: activeTab === 'efeitos' ? '2px solid #2196f3' : 'none', padding: '10px 20px', cursor: 'pointer', fontWeight: 'bold' }}
                >
                    EFEITOS & CONDIÇÕES
                </button>
            </div>

            {/* --- CONTEÚDO DA ABA PRINCIPAL --- */}
            {activeTab === 'atributos' && (
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

                        {/* --- STATUS BARS --- */}
                        <StatusBars
                            ficha={ficha}
                            onUpdate={(data) => updateFicha(data, true)}
                            isFlying={isFlying}
                            isAquatic={isAquatic}
                            overrideDeslocamento={isFlying ? 12 : (isAquatic ? 12 : undefined)}
                        />
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
                                    <AbilityCard
                                        key={`${hab.nome}-${i}`}
                                        habilidade={hab}
                                        pmAtual={ficha.status.pm.atual}
                                        onAtivar={handleAtivarHabilidade}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* COLUNA 3: PERÍCIAS */}
                    <div className="col-skills">
                        <SkillList ficha={ficha} dadosClasses={dadosClasses} updateFicha={updateFicha} listaTodasPericias={listaTodasPericias} />
                    </div>
                </div>
            )}

            {/* --- CONTEÚDO DA ABA EFEITOS --- */}
            {activeTab === 'efeitos' && (
                <div className="tab-content" style={{ padding: '0 20px 20px 20px' }}>
                    <div className="section-card">
                        <h3 className="section-title" style={{ color: '#2196f3', borderBottomColor: '#2196f3' }}>✨ Efeitos Ativos & Condições</h3>

                        {(!ficha.status.efeitos_ativos || ficha.status.efeitos_ativos.length === 0) ? (
                            <div style={{ padding: 40, textAlign: 'center', color: '#666', border: '1px dashed #444', borderRadius: 8, margin: 20 }}>
                                <p style={{ fontSize: '1.2rem', marginBottom: 10 }}>🧘‍♂️ Nenhum efeito ativo</p>
                                <p style={{ fontSize: '0.9rem' }}>Suas habilidades passivas, magias duradouras ou condições aparecerão aqui.</p>
                            </div>
                        ) : (
                            <div className="effects-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 15, padding: 15 }}>
                                {ficha.status.efeitos_ativos.map((efeito: string, i: number) => {
                                    // Ícones dinâmicos baseados no texto
                                    let icon = '✨';
                                    let color = '#2196f3';
                                    let bg = 'rgba(33, 150, 243, 0.1)';

                                    if (efeito.includes('Imune')) { icon = '🛡️'; color = '#4caf50'; bg = 'rgba(76, 175, 80, 0.1)'; }
                                    else if (efeito.includes('Visão') || efeito.includes('Sentido') || efeito.includes('Faro')) { icon = '👁️'; color = '#00bcd4'; bg = 'rgba(0, 188, 212, 0.1)'; }
                                    else if (efeito.includes('Tamanho')) { icon = '📏'; color = '#ffeb3b'; bg = 'rgba(255, 235, 59, 0.1)'; }

                                    // Separa título e descrição se houver ':'
                                    const [titulo, desc] = efeito.includes(':') ? efeito.split(/:(.+)/) : [efeito, null];
                                    const tituloLimpo = titulo.replace(/^[✨🛡️👁️📏]\s*/, '');

                                    return (
                                        <div key={i} className="effect-card" style={{
                                            background: bg,
                                            border: `1px solid ${color}`,
                                            borderRadius: 8,
                                            padding: '15px',
                                            display: 'flex',
                                            flexDirection: 'column',
                                            gap: 5,
                                            boxShadow: '0 4px 10px rgba(0,0,0,0.2)'
                                        }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 10, borderBottom: `1px solid ${color}44`, paddingBottom: 8, marginBottom: 5 }}>
                                                <span style={{ fontSize: '1.4rem' }}>{icon}</span>
                                                <span style={{ fontWeight: 'bold', fontSize: '1.1rem', color: '#fff' }}>{tituloLimpo}</span>
                                            </div>
                                            {desc && <p style={{ margin: 0, fontSize: '0.9rem', color: '#ddd', lineHeight: '1.4' }}>{desc.trim()}</p>}
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* --- SEÇÃO GRIMÓRIO (SEMPRE VISÍVEL) --- */}
            <div className="section-card" style={{ marginTop: 20 }}>
                <div className="section-header">
                    <h3>GRIMÓRIO</h3>
                    <div className="header-actions">
                        <span style={{ fontSize: '0.8rem', color: '#aaa', marginRight: 10 }}>PM: {ficha.status.pm.atual} / {ficha.status.pm.maximo}</span>
                        <button className="btn-small" onClick={() => setShowGrimorio(true)}>+ Adicionar</button>
                    </div>
                </div>
                <div style={{ padding: '15px' }}>
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