import { useState, useEffect, useCallback, useRef } from 'react';
import {
    // Listas Simples (para Selects)
    fetchRacas, fetchClasses, fetchOrigens, fetchPericias, fetchPoderes, fetchDeuses,
    // Dados Completos (Regras)
    fetchDadosClasses, fetchDadosOrigens, fetchDadosRacas, fetchDadosHabilidadesClasse,
    fetchDadosMagias, fetchDadosHabilidades, fetchDadosDeuses, fetchDadosPoderesConcedidos,
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
                    // Listas simples
                    fetchRacas(),
                    fetchClasses(),
                    fetchOrigens(),
                    fetchPericias(),
                    fetchPoderes(),
                    // Dados detalhados
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
                    fetchDeuses().catch(() => ({ data: [] })),
                    fetchDadosDeuses().catch(() => ({ data: {} })),
                    fetchDadosPoderesConcedidos().catch(() => ({ data: {} }))
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
                // Atualiza o estado com a resposta (útil para pegar cálculos do backend)
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
    // Agora aceita 'salvarAgora' (boolean) para forçar update imediato
    const updateFicha = useCallback((novosDados: Partial<Personagem>, salvarAgora: boolean = false) => {
        setFicha((prev) => {
            if (!prev) return null;
            const novaFicha = { ...prev, ...novosDados };
            fichaRef.current = novaFicha;

            // Cancela timer anterior
            if (saveTimeoutRef.current) {
                clearTimeout(saveTimeoutRef.current);
            }

            if (salvarAgora) {
                // Salva imediatamente
                executarSalvamentoReal(novaFicha);
            } else {
                // Agenda Debounce (1.5s)
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

        // Calcula a diferença para atualizar o total corretamente
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

    // B. Prepara dados para o MODAL (Com a lógica para Qareen e Magias)
    const montarHabilidadesParaPanel = () => {
        if (!ficha) return;

        // --- FILTRO DE RACIAIS ---
        const habsRaciais = ficha.habilidades
            // Filtra por tipo 'Raça', 'Poder Racial' ou se o nome é uma habilidade racial conhecida
            .filter(h => {
                const tipo = h.tipo ? h.tipo.toLowerCase() : '';
                return tipo.includes('raça') || tipo.includes('racial');
            })
            .map(h => {
                // Tenta achar a definição nos dados carregados
                let def = dadosHabilidades[h.nome];

                // Se não achar direto, tenta busca case-insensitive nos valores
                if (!def) {
                    def = Object.values(dadosHabilidades).find((d: any) =>
                        d.nome && d.nome.toLowerCase() === h.nome.toLowerCase()
                    );
                }

                // Efeitos acumulados (da definição + escolhas já feitas)
                const efeitos = def?.efeitos || {};

                // GATILHOS: Palavras-chave que indicam que essa habilidade precisa de configuração
                const gatilhosDeEscolha = [
                    'Versátil',    // Humanos
                    'Herança',     // Aggelus/Sulfure
                    'Tatuagem',    // Qareen (Magia)
                    'Mística',     // Variação
                    'Deformidade', // Lefou
                    'Perícia',     // Várias raças
                    'Adaptável',
                    'Arma',
                    'Elemento'
                ];

                // Verifica se precisa de escolha pelo JSON de efeitos OU pelo nome
                const precisa =
                    Object.keys(efeitos).some(k => k.endsWith('_escolha')) ||
                    gatilhosDeEscolha.some(n => h.nome.includes(n));

                return {
                    ...h,
                    precisaEscolha: precisa,
                    efeitos: { ...efeitos, ...h.escolhas_aplicadas }
                };
            });

        setHabilidadesEmEdicao(habsRaciais);

        // --- ORIGEM ---
        setOrigemBeneficiosEmEdicao(ficha.escolhas_origem || []);

        // --- CLASSE (Poderes) ---
        const poderesAtuais = ficha.habilidades
            .filter(h => h.tipo.includes('Poder de'))
            .map(h => h.nome);
        setClassPowersEmEdicao(poderesAtuais);

        // --- SUBCLASSE ---
        setSubclasseEmEdicao(ficha.classes[0]?.subclasse || "");

        // --- DEVOÇÃO ---
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

        // 1. Aplica Origem
        novaFicha.escolhas_origem = origemBeneficiosEmEdicao;

        // 2. Aplica Subclasse
        if (novaFicha.classes.length > 0) {
            novaFicha.classes[0] = { ...novaFicha.classes[0], subclasse: subclasseEmEdicao };
        }

        // 3. Reconstrói Habilidades
        // Remove poderes antigos e habilidades de classe para readicionar limpo
        // (Isso evita duplicação de poderes se o usuário trocar e destrocar)
        let habilidadesFinais = novaFicha.habilidades.filter(h =>
            !h.tipo.includes('Poder de') &&
            !h.tipo.includes('Poder Concedido') &&
            h.tipo !== 'Classe'
        );

        // Atualiza as escolhas nas habilidades que sobraram (Raciais/Gerais)
        habilidadesFinais = habilidadesFinais.map(h => {
            const editada = habilidadesEmEdicao.find(he => he.nome === h.nome);
            // Se foi editada no modal, preserva as escolhas aplicadas
            return editada ? { ...h, escolhas_aplicadas: editada.escolhas_aplicadas } : h;
        });

        // Adiciona novos Poderes de Classe selecionados
        const novosPoderesClasse: Habilidade[] = classPowersEmEdicao.map(nome => {
            // Tenta achar nos dados de classe, senão nos gerais
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

        // Adiciona Poder Concedido (Devoção)
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

        // Força salvamento imediato ao fechar o modal (true)
        updateFicha({
            ...novaFicha,
            habilidades: habilidadesFinais
        }, true);

        setShowHabilidadesPanel(false);
    };

    return {
        // --- ESTADOS ---
        ficha,
        setFicha,
        loading,
        salvando,
        error,

        // --- LISTAS ---
        listaRacas,
        listaClasses,
        listaOrigens,
        listaTodasPericias,
        listaPoderes,
        listaDeuses,

        // --- DADOS DE REGRAS ---
        dadosClasses,
        dadosOrigens,
        dadosRacas,
        dadosHabilidadesClasse,
        dadosMagias,
        dadosHabilidades,
        dadosDeuses,
        dadosPoderesConcedidos,

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
        // (autoSalvar removido pois updateFicha agora gerencia isso internamente)
    };
};