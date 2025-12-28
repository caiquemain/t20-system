import { useState, useEffect, useCallback, useRef } from 'react';
import {
    fetchRacas, fetchClasses, fetchOrigens, fetchPericias, fetchPoderes,
    fetchDadosClasses, fetchDadosOrigens, fetchDadosRacas, fetchDadosHabilidadesClasse,
    fetchDadosMagias, fetchDadosHabilidades,
    fetchDeuses, fetchDadosDeuses, fetchDadosPoderesConcedidos,
    fetchPersonagem, updatePersonagem
} from '../services/api';
import type { Personagem, Habilidade } from '../types';

// Valor padrão
const FICHA_VAZIA: Personagem = {
    _id: '',
    usuario_id: 'guest',
    cabecalho: { nome: '', jogador: '', raca: '', origem: '', deus: '', nivel_total: 1, xp: { atual: 0, proximo_nivel: 1000 } },
    classes: [{ nome: 'Guerreiro', nivel: 1, primaria: true, subclasse: '' }],
    descricao: { tamanho: 'Médio', idiomas: [], aparencia: '', historia: '', anotacoes: '' },
    atributos_base: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 },
    atributos: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 },
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

    // --- DADOS ESTÁTICOS ---
    const [listaRacas, setListaRacas] = useState<string[]>([]);
    const [listaClasses, setListaClasses] = useState<string[]>([]);
    const [listaOrigens, setListaOrigens] = useState<string[]>([]);
    const [listaTodasPericias, setListaTodasPericias] = useState<string[]>([]);
    const [listaPoderes, setListaPoderes] = useState<any[]>([]);
    const [listaDeuses, setListaDeuses] = useState<string[]>([]);

    // --- DADOS DE REGRAS ---
    const [dadosClasses, setDadosClasses] = useState<any>({});
    const [dadosOrigens, setDadosOrigens] = useState<any>({});
    const [dadosRacas, setDadosRacas] = useState<any>({});
    const [dadosHabilidadesClasse, setDadosHabilidadesClasse] = useState<any>({});
    const [dadosMagias, setDadosMagias] = useState<any>({});
    const [dadosHabilidades, setDadosHabilidades] = useState<any>({});
    const [dadosDeuses, setDadosDeuses] = useState<any>({});
    const [dadosPoderesConcedidos, setDadosPoderesConcedidos] = useState<any>({});

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

    // --- CARREGAMENTO INICIAL ---
    useEffect(() => {
        const carregarDados = async () => {
            try {
                console.log("🔄 [useFicha] Carregando sistema...");
                setLoading(true);

                const results = await Promise.all([
                    fetchRacas(), fetchClasses(), fetchOrigens(), fetchPericias(), fetchPoderes(),
                    fetchDadosClasses(), fetchDadosOrigens(), fetchDadosRacas(),
                    fetchDadosHabilidadesClasse(),
                    fetchDadosMagias().catch(() => ({ data: {} })),
                    fetchDadosHabilidades().catch(() => ({ data: {} })),
                    fetchDeuses().catch(() => ({ data: [] })),
                    fetchDadosDeuses().catch(() => ({ data: {} })),
                    fetchDadosPoderesConcedidos().catch(() => ({ data: {} }))
                ]);

                setListaRacas(results[0].data);
                setListaClasses(results[1].data);
                setListaOrigens(results[2].data);
                setListaTodasPericias(results[3].data);
                setListaPoderes(results[4].data);

                setDadosClasses(results[5].data);
                setDadosOrigens(results[6].data);
                setDadosRacas(results[7].data);
                setDadosHabilidadesClasse(results[8].data);
                setDadosMagias(results[9].data);
                setDadosHabilidades(results[10].data);

                setListaDeuses(results[11].data);
                setDadosDeuses(results[12].data);
                setDadosPoderesConcedidos(results[13].data);

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
                    }
                } else {
                    console.log("📝 Iniciando ficha nova.");
                    setFicha(FICHA_VAZIA);
                }

                console.log("✅ [useFicha] Sistema pronto.");
            } catch (error) {
                console.error("❌ Erro fatal:", error);
            } finally {
                setLoading(false);
            }
        };
        carregarDados();
    }, [id]);

    // --- SALVAMENTO AUTOMÁTICO ---
    const salvarAutomaticamente = useCallback((dados: Personagem) => {
        if (!dados._id) return;
        if (id === 'novo') return;

        if (saveTimeoutRef.current) {
            clearTimeout(saveTimeoutRef.current);
        }

        setSalvando(true);

        saveTimeoutRef.current = setTimeout(async () => {
            try {
                const targetId = id || dados._id;
                if (targetId) {
                    // CORREÇÃO: Atualiza o estado local com a resposta do servidor (que contém os cálculos oficiais)
                    const response = await updatePersonagem(targetId, dados);
                    if (response.data) {
                        setFicha(prev => {
                            if (!prev) return response.data;
                            // Mescla suave para não perder edições feitas durante o request (race condition raro)
                            return { ...prev, ...response.data };
                        });
                        console.log("💾 Ficha sincronizada com sucesso.");
                    }
                }
            } catch (e) {
                console.error("Erro no autosave:", e);
            } finally {
                setSalvando(false);
            }
        }, 1500); // 1.5s delay
    }, [id]);

    // --- FUNÇÃO DE ATUALIZAÇÃO ---
    const updateFicha = useCallback(async (novosDados: Partial<Personagem>) => {
        setFicha((prev) => {
            if (!prev) return null;
            const novaFicha = { ...prev, ...novosDados };
            fichaRef.current = novaFicha;

            // Dispara salvamento
            salvarAutomaticamente(novaFicha);

            return novaFicha;
        });
    }, [salvarAutomaticamente]);

    // Limpa o timer ao desmontar
    useEffect(() => {
        return () => {
            if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
        };
    }, []);

    // --- HELPERS ---

    // CORREÇÃO AQUI: Atualiza também o Total (otimista) para a UI não piscar
    const handleAtributoBaseChange = (key: string, valorStr: string) => {
        if (!ficha) return;
        const novoValorBase = parseInt(valorStr) || 0;

        // 1. Calcula a diferença
        const valorAntigoBase = ficha.atributos_base[key as keyof typeof ficha.atributos_base] || 0;
        const delta = novoValorBase - valorAntigoBase;

        // 2. Atualiza a Base
        const novosAtributosBase = { ...ficha.atributos_base, [key]: novoValorBase };

        // 3. Atualiza o Total (Otimista)
        // Isso faz o cálculo visual na tela (base + outros) bater imediatamente
        const valorAntigoTotal = ficha.atributos[key as keyof typeof ficha.atributos] || 0;
        const novosAtributosTotal = { ...ficha.atributos, [key]: valorAntigoTotal + delta };

        updateFicha({
            atributos_base: novosAtributosBase,
            atributos: novosAtributosTotal
        });
    };

    const montarHabilidadesParaPanel = () => {
        if (!ficha) return;

        // 1. Raciais
        const habsRaciais = ficha.habilidades
            .filter(h => h.tipo && h.tipo.toLowerCase().includes('raça'))
            .map(h => {
                let def = dadosHabilidades[h.nome];
                if (!def) def = Object.values(dadosHabilidades).find((d: any) => d.nome === h.nome);

                const efeitos = def?.efeitos || {};
                const precisa = Object.keys(efeitos).some(k => k.endsWith('_escolha')) ||
                    ['Versátil', 'Herança', 'Tatuagem', 'Perícia'].some(n => h.nome.includes(n));

                return {
                    ...h,
                    precisaEscolha: precisa,
                    efeitos: { ...efeitos, ...h.escolhas_aplicadas }
                };
            });
        setHabilidadesEmEdicao(habsRaciais);

        // 2. Origem
        setOrigemBeneficiosEmEdicao(ficha.escolhas_origem || []);

        // 3. Classe
        const poderesAtuais = ficha.habilidades
            .filter(h => h.tipo.includes('Poder de'))
            .map(h => h.nome);
        setClassPowersEmEdicao(poderesAtuais);

        // 4. Subclasse
        setSubclasseEmEdicao(ficha.classes[0]?.subclasse || "");

        // 5. Devoção
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

    const handleSaveEscolhas = async () => {
        if (!ficha) return;

        const novaFicha = { ...ficha };

        // 1. Origem
        novaFicha.escolhas_origem = origemBeneficiosEmEdicao;

        // 2. Subclasse
        if (novaFicha.classes.length > 0) {
            novaFicha.classes[0] = { ...novaFicha.classes[0], subclasse: subclasseEmEdicao };
        }

        // 3. Habilidades
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

        await updateFicha({
            ...novaFicha,
            habilidades: habilidadesFinais
        });

        setShowHabilidadesPanel(false);
    };

    return {
        ficha, loading, salvando,

        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes, listaDeuses,
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias, dadosHabilidades,
        dadosDeuses, dadosPoderesConcedidos,

        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,
        subclasseEmEdicao, setSubclasseEmEdicao,
        devocaoEmEdicao, setDevocaoEmEdicao,

        updateFicha,
        handleAtributoBaseChange,
        montarHabilidadesParaPanel,
        handleSaveEscolhas
    };
};