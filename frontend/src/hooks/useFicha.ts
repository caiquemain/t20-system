import { useState, useEffect } from 'react';
import {
    fetchRacas, fetchClasses, fetchOrigens, fetchPericias, fetchPoderes,
    fetchDadosClasses, fetchDadosOrigens, fetchDadosRacas, fetchDadosHabilidadesClasse,
    fetchDadosMagias, fetchDadosHabilidades, // <--- Importante para carregar regras de habilidades (Versátil)
    fetchPersonagem, updatePersonagem
} from '../services/api';
import type { Personagem, Habilidade } from '../types';

// Modelo de Ficha Vazia para inicialização
const FICHA_VAZIA: Personagem = {
    _id: '',
    usuario_id: 'guest',
    cabecalho: { nome: '', jogador: '', raca: '', origem: '', nivel_total: 1, xp: { atual: 0, proximo_nivel: 1000 } },
    classes: [{ nome: 'Guerreiro', nivel: 1, primaria: true }],
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
    const [ficha, setFicha] = useState<Personagem | null>(null);
    const [loading, setLoading] = useState(true)
    // --- DADOS ESTÁTICOS (Listas) ---
    const [listaRacas, setListaRacas] = useState<string[]>([]);
    const [listaClasses, setListaClasses] = useState<string[]>([]);
    const [listaOrigens, setListaOrigens] = useState<string[]>([]);
    const [listaTodasPericias, setListaTodasPericias] = useState<string[]>([]);
    const [listaPoderes, setListaPoderes] = useState<any[]>([]);

    // --- DADOS DE REGRAS (Objetos Completos) ---
    const [dadosClasses, setDadosClasses] = useState<any>({});
    const [dadosOrigens, setDadosOrigens] = useState<any>({});
    const [dadosRacas, setDadosRacas] = useState<any>({});
    const [dadosHabilidadesClasse, setDadosHabilidadesClasse] = useState<any>({});
    const [dadosMagias, setDadosMagias] = useState<any>({});
    const [dadosHabilidades, setDadosHabilidades] = useState<any>({}); // <--- Novo: Regras gerais de habilidades

    // --- ESTADOS DE EDIÇÃO (Modal) ---
    const [showHabilidadesPanel, setShowHabilidadesPanel] = useState(false);
    const [habilidadesEmEdicao, setHabilidadesEmEdicao] = useState<any[]>([]);
    const [origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao] = useState<string[]>([]);
    const [classPowersEmEdicao, setClassPowersEmEdicao] = useState<string[]>([]);

    // Estado de Subclasse (ex: Caminho do Arcanista)
    const [subclasseEmEdicao, setSubclasseEmEdicao] = useState<string>("");

    // CARREGAMENTO INICIAL
    useEffect(() => {
        const carregarDados = async () => {
            try {
                console.log("🔄 [useFicha] Carregando dados...");

                const results = await Promise.all([
                    fetchRacas(), fetchClasses(), fetchOrigens(), fetchPericias(), fetchPoderes(),
                    fetchDadosClasses(), fetchDadosOrigens(), fetchDadosRacas(),
                    fetchDadosHabilidadesClasse(),
                    fetchDadosMagias().catch(() => ({ data: {} })),
                    fetchDadosHabilidades().catch(() => ({ data: {} })) // <--- Carrega habilidades gerais
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
                setDadosHabilidades(results[10].data); // Salva no estado

                if (id && id !== 'novo') {
                    const fichaRes = await fetchPersonagem(id);
                    setFicha(fichaRes.data);
                } else {
                    setFicha(FICHA_VAZIA);
                }

                console.log("✅ [useFicha] Dados carregados com sucesso.");
            } catch (error) {
                console.error("❌ Erro ao carregar dados:", error);
            } finally {
                setLoading(false);
            }
        };
        carregarDados();
    }, [id]);

    // --- UPDATE INTELIGENTE ---
    const updateFicha = async (novosDados: Partial<Personagem>) => {
        if (!ficha) return;

        // 1. Atualização Otimista (UI rápida)
        const fichaOtimista = { ...ficha, ...novosDados };
        setFicha(fichaOtimista);

        if (id && id !== 'novo') {
            try {
                // 2. Envia para o Backend processar as regras
                const response = await updatePersonagem(id, fichaOtimista);

                // 3. Atualiza estado com o retorno do Backend (Cálculos de PV, PM, Defesa atualizados)
                setFicha(response.data);
            } catch (e) {
                console.error("Erro ao salvar ficha:", e);
            }
        }
    };

    // Handler para Atributos Base
    const handleAtributoBaseChange = (key: string, valorStr: string) => {
        if (!ficha) return;
        const valor = parseInt(valorStr);
        if (isNaN(valor)) return;
        const novosAtributosBase = { ...ficha.atributos_base, [key]: valor };
        updateFicha({ atributos_base: novosAtributosBase });
    };

    // PREPARAÇÃO DO MODAL DE CONFIGURAÇÃO
    const montarHabilidadesParaPanel = () => {
        if (!ficha) return;

        const habsRaciais = ficha.habilidades
            .filter(h => h.tipo && h.tipo.toLowerCase().includes('raça'))
            .map(h => {
                // CORREÇÃO: Busca a definição original da regra para saber se tem escolhas
                // 1. Tenta achar pelo nome exato no banco de habilidades gerais
                let definicaoOriginal = dadosHabilidades[h.nome];

                // 2. Se falhar, tenta buscar em dadosRacas (caso a chave seja diferente do nome)
                if (!definicaoOriginal) {
                    // Tenta encontrar a habilidade iterando
                    const found = Object.values(dadosHabilidades).find((d: any) => d.nome === h.nome);
                    if (found) definicaoOriginal = found;
                }

                const efeitosRegra = definicaoOriginal?.efeitos || {};

                // Verifica se a regra exige escolhas (chaves terminando em _escolha)
                const temEscolhaNaRegra = Object.keys(efeitosRegra).some(k => k.endsWith('_escolha'));

                // Fallback para nomes conhecidos se o backend não retornou efeitos completos
                const nomesConhecidos = ['Versátil', 'Herança', 'Tatuagem', 'Perícia', 'Poder'];
                const ehConhecido = nomesConhecidos.some(n => h.nome.includes(n));

                return {
                    ...h,
                    precisaEscolha: temEscolhaNaRegra || ehConhecido,
                    // Passa os efeitos da REGRA para o componente saber QUAIS botões desenhar
                    // Mescla com as escolhas JÁ FEITAS (h.escolhas_aplicadas) para preencher os valores
                    efeitos: { ...efeitosRegra, ...h.escolhas_aplicadas }
                };
            });

        setHabilidadesEmEdicao(habsRaciais);

        setOrigemBeneficiosEmEdicao(ficha.escolhas_origem || []);

        const poderesAtuais = ficha.habilidades
            .filter(h => h.tipo.includes('Poder de'))
            .map(h => h.nome);

        setClassPowersEmEdicao(poderesAtuais);

        // Carrega subclasse atual
        const classeAtual = ficha.classes[0];
        setSubclasseEmEdicao(classeAtual.subclasse || "");

        setShowHabilidadesPanel(true);
    };

    // SALVAR DO MODAL
    const handleSaveEscolhas = async () => {
        if (!ficha) return;

        const fichaComOrigem = { ...ficha, escolhas_origem: origemBeneficiosEmEdicao };

        // Salva Subclasse
        const novasClasses = [...ficha.classes];
        if (novasClasses.length > 0) {
            novasClasses[0] = { ...novasClasses[0], subclasse: subclasseEmEdicao };
        }
        fichaComOrigem.classes = novasClasses;

        // Remove poderes antigos de classe para substituir pelos novos
        // (Mas mantém habilidades fixas e de origem)
        const habilidadesBase = ficha.habilidades.filter(h =>
            !h.tipo.includes('Poder de')
        );

        // Reconstrói os objetos de Poderes de Classe com dados completos
        const novosPoderesObj: Habilidade[] = classPowersEmEdicao.map(nomePoder => {
            // Tenta achar nos dados de classe
            let dados = Object.values(dadosHabilidadesClasse).find((d: any) => d.nome === nomePoder) as any;

            // Se não achar, tenta nos poderes gerais (listaPoderes é apenas nomes/categorias, precisamos dos dados completos)
            // A lista completa de poderes gerais está em dadosHabilidades (que carregamos agora)
            if (!dados) {
                dados = Object.values(dadosHabilidades).find((d: any) => d.nome === nomePoder);
            }

            if (dados) {
                return {
                    nome: dados.nome,
                    tipo: dados.tipo, // Mantém o tipo original (ex: Poder Geral (Combate))
                    descricao: dados.descricao,
                    fonte: dados.classe || "Poder Geral"
                };
            }
            // Fallback extremo
            return { nome: nomePoder, tipo: 'Poder de Classe', descricao: 'Poder selecionado.', fonte: 'Classe' };
        });

        // Atualiza as escolhas internas das habilidades raciais
        const habilidadesFinais = habilidadesBase.map(h => {
            const editada = habilidadesEmEdicao.find(he => he.nome === h.nome);
            if (editada) {
                // Salva apenas o que foi escolhido (escolhas_aplicadas)
                return { ...h, escolhas_aplicadas: editada.escolhas_aplicadas };
            }
            return h;
        });

        habilidadesFinais.push(...novosPoderesObj);

        await updateFicha({
            ...fichaComOrigem,
            habilidades: habilidadesFinais
        });

        setShowHabilidadesPanel(false);
    };

    return {
        ficha, loading,
        // Dados
        listaRacas, listaClasses, listaOrigens, listaTodasPericias, listaPoderes,
        dadosClasses, dadosOrigens, dadosRacas, dadosHabilidadesClasse, dadosMagias, dadosHabilidades,
        // UI States
        showHabilidadesPanel, setShowHabilidadesPanel,
        habilidadesEmEdicao, setHabilidadesEmEdicao,
        origemBeneficiosEmEdicao, setOrigemBeneficiosEmEdicao,
        classPowersEmEdicao, setClassPowersEmEdicao,
        subclasseEmEdicao, setSubclasseEmEdicao, // Exporta estados de subclasse
        // Ações
        updateFicha,
        handleAtributoBaseChange,
        montarHabilidadesParaPanel,
        handleSaveEscolhas
    };
};