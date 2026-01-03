import { useState, useEffect, useCallback, useRef } from 'react';
import {
    // Listas Simples (para Selects)
    fetchRacas, fetchClasses, fetchOrigens, fetchPericias, fetchPoderes, fetchDeuses,
    // Dados Completos (Regras)
    fetchDadosClasses, fetchDadosOrigens, fetchDadosRacas, fetchDadosHabilidadesClasse,
    fetchDadosMagias, fetchDadosHabilidades, fetchDadosDeuses, fetchDadosPoderesConcedidos,
    // [NOVO] Dados de Habilidades Raciais (Sub-escolhas)
    fetchDadosHabilidadesRaciais,
    // Ações de Personagem
    fetchPersonagem, updatePersonagem, createPersonagem
} from '../services/api';
import type { Personagem, Habilidade } from '../types';

// Valor padrão para inicialização (Ficha Vazia)
const FICHA_VAZIA: Personagem = {
    _id: '',
    usuario_id: 'guest',
    cabecalho: { nome: '', jogador: '', raca: '', origem: '', deus: '', nivel_total: 1, xp: { atual: 0, proximo_nivel: 1000 } },
    classes: [{ nome: 'Guerreiro', nivel: 1, primaria: true, subclasse: '' }],
    descricao: { tamanho: 'Médio', idiomas: [], aparencia: '', historia: '', anotacoes: '' },
    atributos_base: { forca: 10, destreza: 10, constituicao: 10, inteligencia: 10, sabedoria: 10, carisma: 10 },
    atributos: { forca: 10, destreza: 10, constituicao: 10, inteligencia: 10, sabedoria: 10, carisma: 10 },
    modificadores_raciais: {}, modificadores_envelhecimento: {}, modificadores_outros: {},
    escolhas_atributos_raciais: [],
    escolhas_origem: [],
    status: {
        pv: { atual: 0, maximo: 0, temporario: 0 },
        pm: { atual: 0, maximo: 0, temporario: 0 },
        defesa: { total: 10, detalhes: { base: 10, des_mod: 0, armadura: 0, escudo: 0, outros: 0 } },
        rd: [], deslocamento: 9
    },
    pericias: {}, proficiencias: [], combate: { ataques: [], magias: [], cd_magias: 0, bba: 0, iniciativa: 0 },
    habilidades: [],
    inventario: { dinheiro: { tl: 0, tp: 0, to: 0 }, equipamentos: [], carga_total: 0, carga_maxima: 0 }
};

export const useFicha = (id: string | undefined) => {
    // --- ESTADOS PRINCIPAIS ---
    const [ficha, setFicha] = useState<Personagem | null>(null);
    const [loading, setLoading] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // --- DADOS ESTÁTICOS (Listas para Dropdowns) ---
    const [listaRacas, setListaRacas] = useState<string[]>([]);
    const [listaClasses, setListaClasses] = useState<string[]>([]);
    const [listaOrigens, setListaOrigens] = useState<string[]>([]);
    const [listaTodasPericias, setListaTodasPericias] = useState<string[]>([]);
    const [listaPoderes, setListaPoderes] = useState<any[]>([]);
    const [listaDeuses, setListaDeuses] = useState<string[]>([]);

    // --- DADOS DE REGRAS (Infos detalhadas para lógica) ---
    const [dadosClasses, setDadosClasses] = useState<any>({});
    const [dadosOrigens, setDadosOrigens] = useState<any>({});
    const [dadosRacas, setDadosRacas] = useState<any>({});
    const [dadosHabilidadesClasse, setDadosHabilidadesClasse] = useState<any>({});
    const [dadosMagias, setDadosMagias] = useState<any>({});
    const [dadosHabilidades, setDadosHabilidades] = useState<any>({});
    const [dadosDeuses, setDadosDeuses] = useState<any>({});
    const [dadosPoderesConcedidos, setDadosPoderesConcedidos] = useState<any>({});
    // [NOVO] Estado para Habilidades Raciais (Duende, Osteon, etc)
    const [dadosHabilidadesRaciais, setDadosHabilidadesRaciais] = useState<any>({});

    // --- ESTADOS DE EDIÇÃO (MODAL) ---
    const [showHabilidadesPanel, setShowHabilidadesPanel] = useState(false);
    const [habilidadesEmEdicao, setHabilidadesEmEdicao] = useState<any[]>([]);
    const [origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao] = useState<string[]>([]);
    const [classPowersEmEdicao, setClassPowersEmEdicao] = useState<string[]>([]);
    const [subclasseEmEdicao, setSubclasseEmEdicao] = useState<string>("");
    const [devocaoEmEdicao, setDevocaoEmEdicao] = useState<string>("");

    // Refs para controle
    const fichaRef = useRef<Personagem | null>(null);
    const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    // --- 1. CARREGAMENTO INICIAL ---
    useEffect(() => {
        const carregarDados = async () => {
            try {
                console.log("🔄 [useFicha] Carregando sistema T20...");
                setLoading(true);

                // Carrega tudo em paralelo
                const results = await Promise.all([
                    // Listas simples (Indices 0-4)
                    fetchRacas(),
                    fetchClasses(),
                    fetchOrigens(),
                    fetchPericias(),
                    fetchPoderes(),
                    // Dados detalhados (Indices 5-10)
                    fetchDadosClasses(),
                    fetchDadosOrigens(),
                    fetchDadosRacas(),
                    fetchDadosHabilidadesClasse(),
                    fetchDadosMagias().catch((err) => {
                        console.warn("Aviso: Falha ao carregar Magias", err);
                        return { data: {} };
                    }),
                    fetchDadosHabilidades().catch((err) => {
                        console.warn("Aviso: Falha ao carregar Habilidades Gerais", err);
                        return { data: {} };
                    }),
                    // Dados extras (Indices 11-13)
                    fetchDeuses().catch(() => ({ data: [] })),
                    fetchDadosDeuses().catch(() => ({ data: {} })),
                    fetchDadosPoderesConcedidos().catch(() => ({ data: {} })),
                    // [NOVO] (Indice 14)
                    fetchDadosHabilidadesRaciais().catch((err) => {
                        console.warn("Aviso: Falha ao carregar Habilidades Raciais", err);
                        return { data: {} };
                    })
                ]);

                // Define as Listas
                setListaRacas(results[0].data);
                setListaClasses(results[1].data);
                setListaOrigens(results[2].data);
                setListaTodasPericias(results[3].data);
                setListaPoderes(results[4].data);

                // Define os Dados de Regras
                setDadosClasses(results[5].data);
                setDadosOrigens(results[6].data);
                setDadosRacas(results[7].data);
                setDadosHabilidadesClasse(results[8].data);
                setDadosMagias(results[9].data);
                setDadosHabilidades(results[10].data);

                setListaDeuses(results[11].data);
                setDadosDeuses(results[12].data);
                setDadosPoderesConcedidos(results[13].data);
                // [NOVO]
                setDadosHabilidadesRaciais(results[14].data);

                // Carrega ou Cria Ficha
                const idValido = id && id !== 'novo' && id !== 'null' && id !== 'undefined';

                if (idValido) {
                    console.log(`📡 Buscando ficha ID: ${id}`);
                    try {
                        const fichaRes = await fetchPersonagem(id);
                        setFicha(fichaRes.data);
                        fichaRef.current = fichaRes.data;
                    } catch (err) {
                        console.error("❌ Erro ao buscar ficha, iniciando vazia.", err);
                        setFicha(FICHA_VAZIA);
                        setError("Ficha não encontrada. Criando nova.");
                    }
                } else {
                    console.log("📝 Iniciando ficha nova.");
                    setFicha(FICHA_VAZIA);
                }

                console.log("✅ [useFicha] Sistema carregado.");
            } catch (error) {
                console.error("❌ Erro fatal ao carregar useFicha:", error);
                setError("Falha ao conectar com o servidor.");
            } finally {
                setLoading(false);
            }
        };
        carregarDados();
    }, [id]);

    // --- 2. LÓGICA DE SALVAMENTO (CENTRALIZADA) ---
    const executarSalvamentoReal = useCallback(async (dadosParaSalvar: Personagem) => {
        setSalvando(true);
        try {
            let response;
            // Se tem ID real, atualiza (PUT)
            if (dadosParaSalvar._id && dadosParaSalvar._id !== 'novo') {
                response = await updatePersonagem(dadosParaSalvar._id, dadosParaSalvar);
            }
            // Se é novo e usuário já digitou algo relevante (nome), cria (POST)
            else if (id === 'novo' && dadosParaSalvar.cabecalho.nome.length > 2) {
                response = await createPersonagem(dadosParaSalvar);
            }

            if (response && response.data) {
                setFicha(prev => {
                    if (!prev) return response.data;
                    return { ...prev, ...response.data };
                });
                console.log("💾 Ficha salva com sucesso.");
            }
        } catch (e) {
            console.error("❌ Erro ao salvar ficha:", e);
            setError("Erro ao salvar alterações.");
        } finally {
            setSalvando(false);
        }
    }, [id]);

    // --- 3. ATUALIZAÇÃO DE ESTADO (Wrapper Público) ---
    const updateFicha = useCallback((novosDados: Partial<Personagem>, salvarAgora: boolean = false) => {
        setFicha((prev) => {
            if (!prev) return null;
            const novaFicha = { ...prev, ...novosDados };
            fichaRef.current = novaFicha;

            if (saveTimeoutRef.current) {
                clearTimeout(saveTimeoutRef.current);
            }

            if (salvarAgora) {
                executarSalvamentoReal(novaFicha);
            } else {
                saveTimeoutRef.current = setTimeout(() => {
                    executarSalvamentoReal(novaFicha);
                }, 1500);
            }

            return novaFicha;
        });
    }, [executarSalvamentoReal]);

    // Limpeza de Timers ao desmontar
    useEffect(() => {
        return () => {
            if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
        };
    }, []);

    // --- 4. FUNÇÕES DE REGRA DE NEGÓCIO ---

    // A. Atualiza Atributos Base
    const handleAtributoBaseChange = (key: string, valorStr: string) => {
        if (!ficha) return;
        const novoValorBase = parseInt(valorStr) || 0;
        const valorAntigoBase = ficha.atributos_base[key as keyof typeof ficha.atributos_base] || 0;
        const delta = novoValorBase - valorAntigoBase;

        const novosAtributosBase = { ...ficha.atributos_base, [key]: novoValorBase };
        const valorAntigoTotal = ficha.atributos[key as keyof typeof ficha.atributos] || 0;
        const novosAtributosTotal = { ...ficha.atributos, [key]: valorAntigoTotal + delta };

        updateFicha({
            atributos_base: novosAtributosBase,
            atributos: novosAtributosTotal
        });
    };

    // B. Prepara dados para o MODAL (Com a lógica para Qareen, Magias e DUENDE)
    const montarHabilidadesParaPanel = () => {
        if (!ficha) return;

        const habsParaConfigurar = ficha.habilidades
            .map(h => {
                // 1. Busca dados completos
                let def = dadosHabilidades[h.nome];

                if (!def && dadosHabilidadesRaciais) {
                    def = Object.values(dadosHabilidadesRaciais).find((d: any) =>
                        d.nome === h.nome || h.nome === d.nome
                    );
                    if (!def && dadosHabilidadesRaciais[h.nome]) {
                        def = dadosHabilidadesRaciais[h.nome];
                    }
                }

                if (!def) {
                    def = Object.values(dadosHabilidades).find((d: any) =>
                        d.nome && d.nome.toLowerCase() === h.nome.toLowerCase()
                    );
                }

                const efeitos = def?.efeitos || h.efeitos || {};
                const escolhasFeitas = h.escolhas_aplicadas || {};

                // 2. Verifica se TEM algo para configurar
                const temGatilhoDeEscolha = Object.keys(efeitos).some(k => k.endsWith('_escolha'));

                // Gatilhos de nome (Pais)
                const gatilhosDeEscolha = [
                    'Versátil', 'Herança', 'Tatuagem', 'Mística', 'Deformidade', 'Perícia',
                    'Adaptável', 'Arma', 'Elemento',
                    'Natureza', 'Tamanho', 'Presentes', 'Limitações', 'Dons', 'Memória'
                ];

                // 3. LISTA NEGRA: Remove tudo que sabemos que é passivo ou resultado
                // Adicionei aqui todas as que apareceram no seu print
                const ignorar = [
                    // Passivas gerais
                    "Mineral", "Vegetal", "Minúsculo", "Pequeno", "Médio", "Grande",
                    "Afinidade Elemental",
                    // Passivas do Duende (Presentes/Tabus)
                    "Voo", "Invisibilidade (Poder)", "Enfeitiçar (Poder)",
                    "Encantar Objetos", "Língua da Natureza", "Maldição",
                    "Mais Lá do que Aqui", "Metamorfose Animal", "Sonhos Proféticos",
                    "Velocidade do Pensamento", "Visão Feérica", "Tabu"
                ];

                // Se estiver na lista negra, só passa se TIVER uma escolha explícita (ex: Natureza Animal tem escolha de atributo)
                if (ignorar.some(nome => h.nome.includes(nome)) && !temGatilhoDeEscolha) {
                    return null;
                }

                // Verifica gatilhos de nome (com cuidado extra para não pegar falsos positivos como 'Língua da Natureza')
                const matchNome = gatilhosDeEscolha.some(n => h.nome.includes(n));

                return {
                    ...h,
                    efeitos: { ...efeitos, ...escolhasFeitas },
                    precisaEscolha: temGatilhoDeEscolha || matchNome
                };
            })
            // 4. O FILTRO FINAL
            // Removemos '|| h.tipo === "Racial"' para não deixar passar lixo.
            // Agora só passa se realmente tiver flag de escolha.
            .filter(h => h && h.precisaEscolha);

        setHabilidadesEmEdicao(habsParaConfigurar);

        // ... Resto da função (Origem, etc) ...
        setOrigemBeneficiosEmEdicao(ficha.escolhas_origem || []);

        const poderesAtuais = ficha.habilidades
            .filter(h => h.tipo.includes('Poder de'))
            .map(h => h.nome);
        setClassPowersEmEdicao(poderesAtuais);

        setSubclasseEmEdicao(ficha.classes[0]?.subclasse || "");

        const deus = ficha.cabecalho.deus;
        const infoDeus = dadosDeuses[deus];
        if (deus && infoDeus) {
            const poder = ficha.habilidades.find(h => infoDeus.poderes.includes(h.nome));
            setDevocaoEmEdicao(poder ? poder.nome : "");
        } else {
            setDevocaoEmEdicao("");
        }

        setShowHabilidadesPanel(true);
    };

    // C. Salva as escolhas do MODAL
    const handleSaveEscolhas = async () => {
        if (!ficha) return;

        const novaFicha = { ...ficha };
        novaFicha.escolhas_origem = origemBeneficiosEmEdicao;

        if (novaFicha.classes.length > 0) {
            novaFicha.classes[0] = { ...novaFicha.classes[0], subclasse: subclasseEmEdicao };
        }

        let habilidadesFinais = novaFicha.habilidades.filter(h =>
            !h.tipo.includes('Poder de') &&
            !h.tipo.includes('Poder Concedido') &&
            h.tipo !== 'Classe'
        );

        habilidadesFinais = habilidadesFinais.map(h => {
            const editada = habilidadesEmEdicao.find(he => he.nome === h.nome);
            return editada ? { ...h, escolhas_aplicadas: editada.escolhas_aplicadas } : h;
        });

        const novosPoderesClasse: Habilidade[] = classPowersEmEdicao.map(nome => {
            let d = Object.values(dadosHabilidadesClasse).find((x: any) => x.nome === nome) as any;
            if (!d) d = Object.values(dadosHabilidades).find((x: any) => x.nome === nome);

            return {
                nome: nome,
                tipo: d?.tipo || 'Poder de Classe',
                descricao: d?.descricao || 'Poder selecionado',
                fonte: d?.classe || 'Classe'
            };
        });
        habilidadesFinais.push(...novosPoderesClasse);

        if (novaFicha.cabecalho.deus && devocaoEmEdicao) {
            const dPoder = dadosPoderesConcedidos[devocaoEmEdicao];
            if (dPoder) {
                habilidadesFinais.push({
                    nome: dPoder.nome,
                    tipo: "Poder Concedido",
                    descricao: dPoder.descricao,
                    fonte: `Devoção: ${novaFicha.cabecalho.deus}`
                });
            }
        }

        updateFicha({
            ...novaFicha,
            habilidades: habilidadesFinais
        }, true);

        setShowHabilidadesPanel(false);
    };

    return {
        // --- ESTADOS ---
        ficha, setFicha, loading, salvando, error,

        // --- LISTAS ---
        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes, listaDeuses,

        // --- DADOS DE REGRAS ---
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias,
        dadosHabilidades, dadosDeuses, dadosPoderesConcedidos,
        // [NOVO] Retorna para ser usado no AbilityConfigModal
        dadosHabilidadesRaciais,

        // --- CONTROLES DE UI ---
        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,
        subclasseEmEdicao, setSubclasseEmEdicao,
        devocaoEmEdicao, setDevocaoEmEdicao,

        // --- MÉTODOS ---
        updateFicha,
        handleAtributoBaseChange,
        montarHabilidadesParaPanel,
        handleSaveEscolhas,
    };
};