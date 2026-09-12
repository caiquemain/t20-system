import { useState, useEffect, useCallback, useRef } from 'react';
import {
    fetchRacas, fetchClasses, fetchOrigens, fetchPericias, fetchPoderes, fetchDeuses,
    fetchDadosClasses, fetchDadosOrigens, fetchDadosRacas, fetchDadosHabilidadesClasse,
    fetchDadosMagias, fetchDadosHabilidades, fetchDadosDeuses, fetchDadosPoderesConcedidos,
    fetchDadosHabilidadesRaciais, fetchDadosEscolhas,
    fetchPersonagem, updatePersonagem, createPersonagem
} from '../services/api';
import type { Personagem, Habilidade } from '../types';

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
        rd: [],
        deslocamento: 9,
        proficiencias: [],
        imunidades: [],
        sentidos: [], vulnerabilidades: [] },
    pericias: {}, proficiencias: [], combate: { ataques: [], magias: [], cd_magias: 0, bba: 0, iniciativa: 0, circulo_maximo: 0, limite_magias: 0 },
    habilidades: [],
    inventario: { dinheiro: { tl: 0, tp: 0, to: 0 }, equipamentos: [], carga_total: 0, carga_maxima: 0 }
};

export const useFicha = (id: string | undefined) => {
    const [ficha, setFicha] = useState<Personagem | null>(null);
    const [loading, setLoading] = useState(true);
    const [salvando, setSalvando] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [listaRacas, setListaRacas] = useState<string[]>([]);
    const [listaClasses, setListaClasses] = useState<string[]>([]);
    const [listaOrigens, setListaOrigens] = useState<string[]>([]);
    const [listaTodasPericias, setListaTodasPericias] = useState<string[]>([]);
    const [listaPoderes, setListaPoderes] = useState<any[]>([]);
    const [listaDeuses, setListaDeuses] = useState<string[]>([]);
    const [dadosClasses, setDadosClasses] = useState<any>({});
    const [dadosOrigens, setDadosOrigens] = useState<any>({});
    const [dadosRacas, setDadosRacas] = useState<any>({});
    const [dadosHabilidadesClasse, setDadosHabilidadesClasse] = useState<any>({});
    const [dadosMagias, setDadosMagias] = useState<any>({});
    const [dadosHabilidades, setDadosHabilidades] = useState<any>({});
    const [dadosDeuses, setDadosDeuses] = useState<any>({});
    const [dadosPoderesConcedidos, setDadosPoderesConcedidos] = useState<any>({});
    const [dadosHabilidadesRaciais, setDadosHabilidadesRaciais] = useState<any>({});
    const [dadosEscolhas, setDadosEscolhas] = useState<any>({});

    const [showHabilidadesPanel, setShowHabilidadesPanel] = useState(false);
    const [habilidadesEmEdicao, setHabilidadesEmEdicao] = useState<any[]>([]);
    const [origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao] = useState<string[]>([]);
    const [classPowersEmEdicao, setClassPowersEmEdicao] = useState<string[]>([]);
    const [subclasseEmEdicao, setSubclasseEmEdicao] = useState<string>("");
    const [devocaoEmEdicao, setDevocaoEmEdicao] = useState<string>("");
    // [LOTE 1-UI] Escolhas secundárias de poderes (escola, atributo, familiar...)
    const [poderesEscolhasEmEdicao, setPoderesEscolhasEmEdicao] = useState<Record<string, Record<string, any>>>({});
    const [linhagemEmEdicao, setLinhagemEmEdicao] = useState<string>("");
    const [tipoDanoEmEdicao, setTipoDanoEmEdicao] = useState<string>("");

    const fichaRef = useRef<Personagem | null>(null);
    const saveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        const carregarDados = async () => {
            try {
                console.log("🔄 [useFicha] Carregando sistema T20...");
                setLoading(true);
                const results = await Promise.all([
                    fetchRacas(), fetchClasses(), fetchOrigens(), fetchPericias(), fetchPoderes(),
                    fetchDadosClasses(), fetchDadosOrigens(), fetchDadosRacas(), fetchDadosHabilidadesClasse(),
                    fetchDadosMagias().catch(() => ({ data: {} })),
                    fetchDadosHabilidades().catch(() => ({ data: {} })),
                    fetchDeuses().catch(() => ({ data: [] })),
                    fetchDadosDeuses().catch(() => ({ data: {} })),
                    fetchDadosPoderesConcedidos().catch(() => ({ data: {} })),
                    fetchDadosHabilidadesRaciais().catch(() => ({ data: {} })),
                fetchDadosEscolhas().catch(() => ({ data: {} }))
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
                setDadosHabilidadesRaciais(results[14].data);
             setDadosEscolhas(results[15]?.data || {});

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

    const executarSalvamentoReal = useCallback(async (dadosParaSalvar: Personagem) => {
        setSalvando(true);
        try {
            let response;
            if (dadosParaSalvar._id && dadosParaSalvar._id !== 'novo') {
                response = await updatePersonagem(dadosParaSalvar._id, dadosParaSalvar);
            } else if (id === 'novo' && dadosParaSalvar.cabecalho.nome.length > 2) {
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

    const updateFicha = useCallback((novosDados: Partial<Personagem>, salvarAgora: boolean = false) => {
        setFicha((prev) => {
            if (!prev) return null;
            const novaFicha = { ...prev, ...novosDados };
            fichaRef.current = novaFicha;
            if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);
            if (salvarAgora) {
                executarSalvamentoReal(novaFicha);
            } else {
                saveTimeoutRef.current = setTimeout(() => executarSalvamentoReal(novaFicha), 1500);
            }
            return novaFicha;
        });
    }, [executarSalvamentoReal]);

    useEffect(() => {
        return () => { if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current); };
    }, []);

    const handleAtributoBaseChange = (key: string, valorStr: string) => {
        if (!ficha) return;
        const novoValorBase = parseInt(valorStr) || 0;
        const valorAntigoBase = ficha.atributos_base[key as keyof typeof ficha.atributos_base] || 0;
        const delta = novoValorBase - valorAntigoBase;
        const novosAtributosBase = { ...ficha.atributos_base, [key]: novoValorBase };
        const valorAntigoTotal = ficha.atributos[key as keyof typeof ficha.atributos] || 0;
        const novosAtributosTotal = { ...ficha.atributos, [key]: valorAntigoTotal + delta };
        updateFicha({ atributos_base: novosAtributosBase, atributos: novosAtributosTotal });
    };

    const montarHabilidadesParaPanel = () => {
        if (!ficha) return;
        const habsParaConfigurar = ficha.habilidades
            .map(h => {
                let def = dadosHabilidades[h.nome];
                if (!def && dadosHabilidadesRaciais) {
                    def = Object.values(dadosHabilidadesRaciais).find((d: any) => d.nome === h.nome || h.nome === d.nome);
                    if (!def && dadosHabilidadesRaciais[h.nome]) def = dadosHabilidadesRaciais[h.nome];
                }
                if (!def) {
                    def = Object.values(dadosHabilidades).find((d: any) => d.nome && d.nome.toLowerCase() === h.nome.toLowerCase());
                }
                const efeitos = def?.efeitos || h.efeitos || {};
                const escolhasFeitas = h.escolhas_aplicadas || {};
                const temGatilhoDeEscolha = Object.keys(efeitos).some(k => k.endsWith('_escolha'));
                const gatilhosDeEscolha = ['Versátil', 'Herança', 'Tatuagem', 'Mística', 'Deformidade', 'Perícia', 'Adaptável', 'Arma', 'Elemento', 'Natureza', 'Tamanho', 'Presentes', 'Limitações', 'Dons', 'Memória'];
                const ignorar = ["Mineral", "Vegetal", "Minúsculo", "Pequeno", "Médio", "Grande", "Afinidade Elemental", "Voo", "Invisibilidade (Poder)", "Enfeitiçar (Poder)", "Encantar Objetos", "Língua da Natureza", "Maldição", "Mais Lá do que Aqui", "Metamorfose Animal", "Sonhos Proféticos", "Velocidade do Pensamento", "Visão Feérica", "Tabu"];
                if (ignorar.some(nome => h.nome.includes(nome)) && !temGatilhoDeEscolha) return null;
                const matchNome = gatilhosDeEscolha.some(n => h.nome.includes(n));
                return { ...h, efeitos: { ...efeitos, ...escolhasFeitas }, precisaEscolha: temGatilhoDeEscolha || matchNome };
            })
            .filter(h => h && h.precisaEscolha);
        setHabilidadesEmEdicao(habsParaConfigurar);
        setOrigemBeneficiosEmEdicao(ficha.escolhas_origem || []);
        const poderesAtuais = ficha.habilidades.filter(h => h.tipo.includes('Poder de')).map(h => h.nome);
        setClassPowersEmEdicao(poderesAtuais);
        // [LOTE 1-UI] Recarrega as escolhas secundárias dos poderes salvos
        const escolhasPoderes: Record<string, Record<string, any>> = {};
        ficha.habilidades
            .filter(h => h.tipo.includes('Poder de') && h.escolhas_aplicadas && Object.keys(h.escolhas_aplicadas).length > 0)
            .forEach(h => { escolhasPoderes[h.nome] = { ...h.escolhas_aplicadas }; });
        setPoderesEscolhasEmEdicao(escolhasPoderes);
        setSubclasseEmEdicao(ficha.classes[0]?.subclasse || "");
        const linhagemHab = ficha.habilidades.find(h => (h.nome || "").startsWith("Linhagem"));
        setLinhagemEmEdicao(linhagemHab ? linhagemHab.nome.replace("Linhagem ", "") : "");
        setTipoDanoEmEdicao(linhagemHab?.escolhas_aplicadas?.tipo_dano || "");
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

    void 0; // mantém helper para uso futuro
    const _sanitizarEscolhasAplicadas = (habilidade: any) => {
        const efeitos = habilidade.efeitos || {};
        const escolhasOriginais = habilidade.escolhas_aplicadas || {};
        const limpas: Record<string, any> = {};

        Object.entries(escolhasOriginais).forEach(([k, v]) => {
            // Remove gatilhos vazados dos efeitos, ex.: pericia_escolha: 1
            if (k in efeitos && v === efeitos[k]) return;

            // Chaves *_escolha só são escolha real quando string não vazia.
            // Ex.: pericia_escolha = "Diplomacia"
            if (k.endsWith('_escolha')) {
                if (typeof v === 'string' && v.trim().length > 0) {
                    limpas[k] = v;
                }
                return;
            }

            // Preserva demais escolhas reais, como pericia_bonus_0, poder_ambicao_0 etc.
            if (v !== undefined && v !== null && v !== '') {
                limpas[k] = v;
            }
        });

        return limpas;
    };

    const handleSaveEscolhas = async () => {
        if (!ficha) return;
        const novaFicha = { ...ficha };
        novaFicha.escolhas_origem = origemBeneficiosEmEdicao;
        if (novaFicha.classes.length > 0) {
            novaFicha.classes[0] = { ...novaFicha.classes[0], subclasse: subclasseEmEdicao };
        }
        let habilidadesFinais = novaFicha.habilidades.filter(h =>
            !h.tipo.includes('Poder de') && !h.tipo.includes('Poder Concedido') && h.tipo !== 'Classe'
        );
        const buscarDef = (nome: string): any => {
            let d = (dadosHabilidades as any)[nome];
            if (!d && dadosHabilidadesRaciais) {
                d = Object.values(dadosHabilidadesRaciais).find((x: any) => x.nome === nome) || (dadosHabilidadesRaciais as any)[nome];
            }
            if (!d) d = Object.values(dadosHabilidadesClasse).find((x: any) => x.nome === nome);
            return d || null;
        };
        habilidadesFinais = habilidadesFinais.map(h => {
            const editada = habilidadesEmEdicao.find(he => he.nome === h.nome);
            const def = buscarDef(h.nome);
            const gatilhos = def?.efeitos || {};
            let escolhas: Record<string, any> = { ...(editada ? editada.escolhas_aplicadas : h.escolhas_aplicadas) || {} };
            Object.keys(escolhas).forEach(k => {
            const v = escolhas[k];
            // PRESERVA escolha real em string (ex.: pericia_escolha='Diplomacia')
            if (typeof v === 'string' && v.length > 0) return;
            const ehGatilho = (k in gatilhos) || k.endsWith('_escolha');
            if (ehGatilho) delete escolhas[k];
        });
            void sanitizarEscolhasAplicadas(h);
            if (gatilhos.escolha_subclasse) escolhas.subclasse = subclasseEmEdicao;
            return { ...h, escolhas_aplicadas: escolhas };
        });
        const novosPoderesClasse: Habilidade[] = classPowersEmEdicao.map(nome => {
            let d = Object.values(dadosHabilidadesClasse).find((x: any) => x.nome === nome) as any;
            if (!d) d = Object.values(dadosHabilidades).find((x: any) => x.nome === nome);
            return {
                nome: nome,
                tipo: d?.tipo || 'Poder de Classe',
                descricao: d?.descricao || 'Poder selecionado',
                fonte: d?.classe || 'Classe',
                efeitos: d?.efeitos || {},
                escolhas_aplicadas: poderesEscolhasEmEdicao[nome] || {}
            };
        });
        // [FEITICEIRO] Upsert da linhagem escolhida
        habilidadesFinais = habilidadesFinais.filter(h => !(h.nome || "").startsWith("Linhagem"));
        if (subclasseEmEdicao === "Feiticeiro" && linhagemEmEdicao) {
            habilidadesFinais.push({
                nome: `Linhagem ${linhagemEmEdicao}`,
                tipo: "Habilidade de Classe",
                descricao: `Linhagem sobrenatural do feiticeiro (${linhagemEmEdicao}).`,
                fonte: "Feiticeiro",
                escolhas_aplicadas: linhagemEmEdicao === "Dracônica" && tipoDanoEmEdicao ? { tipo_dano: tipoDanoEmEdicao } : {}
            } as Habilidade);
        }
        habilidadesFinais.push(...novosPoderesClasse);
        if (novaFicha.cabecalho.deus && devocaoEmEdicao) {
            const dPoder = dadosPoderesConcedidos[devocaoEmEdicao];
            if (dPoder) {
                habilidadesFinais.push({ nome: dPoder.nome, tipo: "Poder Concedido", descricao: dPoder.descricao, fonte: `Devoção: ${novaFicha.cabecalho.deus}` });
            }
        }
        // 🧹 Troca de escolha racial de perícia remove o treino da antiga
        const CHAVES_PERICIA_ESCOLHA = ["pericia_escolha", "pericia_1", "pericia_2", "memoria_postuma", "pericia_bonus_0", "pericia_bonus_1"];
        const periciasPayload = { ...(novaFicha.pericias || {}) };
        habilidadesFinais.forEach((hNova: any) => {
            const hAntiga = (ficha.habilidades || []).find((h: any) => h.nome === hNova.nome);
            if (!hAntiga) return;
            CHAVES_PERICIA_ESCOLHA.forEach((k) => {
                const vAntigo = hAntiga.escolhas_aplicadas?.[k];
                const vNovo = hNova.escolhas_aplicadas?.[k];
                if (typeof vAntigo === "string" && vAntigo && vAntigo !== vNovo && periciasPayload[vAntigo]) {
                    periciasPayload[vAntigo] = { ...periciasPayload[vAntigo], treino: 0 };
                }
            });
        });
        novaFicha.pericias = periciasPayload;
        console.log('[SAVE][RACIAIS] escolhas pós-cleanup:', habilidadesFinais
            .filter((h: any) => h.tipo === 'Racial')
            .map((h: any) => ({ nome: h.nome, escolhas: h.escolhas_aplicadas })));
        updateFicha({ ...novaFicha, habilidades: habilidadesFinais }, true);
        setShowHabilidadesPanel(false);
    };

    return {
        ficha, setFicha, loading, salvando, error,
        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes, listaDeuses,
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias,
        dadosHabilidades, dadosDeuses, dadosPoderesConcedidos, dadosHabilidadesRaciais,
        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,
        subclasseEmEdicao, setSubclasseEmEdicao,
        devocaoEmEdicao, setDevocaoEmEdicao,
        poderesEscolhasEmEdicao, setPoderesEscolhasEmEdicao,
     dadosEscolhas,
        linhagemEmEdicao,
    setLinhagemEmEdicao,
    tipoDanoEmEdicao,
    setTipoDanoEmEdicao,
    updateFicha, handleAtributoBaseChange, montarHabilidadesParaPanel, handleSaveEscolhas,
    };
};
