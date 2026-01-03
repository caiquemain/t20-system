export type TamanhoEnum = "Minúsculo" | "Pequeno" | "Médio" | "Grande" | "Enorme" | "Colossal";

export interface XP {
    atual: number;
    proximo_nivel: number;
}

export interface Cabecalho {
    nome: string;
    jogador: string;
    raca: string;
    origem: string;
    deus: string;
    divindade?: string;
    nivel_total: number;
    xp: XP;
}

export interface ClasseInfo {
    nome: string;
    nivel: number;
    subclasse?: string;
    primaria: boolean;
}

export interface Descricao {
    idade?: string;
    altura?: string;
    tamanho: TamanhoEnum;
    genero?: string;
    idiomas: string[];
    aparencia?: string;
    historia?: string;
    anotacoes?: string;
}

export interface Atributos {
    [key: string]: number;
    forca: number;
    destreza: number;
    constituicao: number;
    inteligencia: number;
    sabedoria: number;
    carisma: number;
}

// --- INTERFACES DE DETALHES ---
export interface DetalhesCalculo {
    inicial: number;
    nivel: number;
    outros: number;
    con?: number;
    atributo?: number;
    habilidades?: number;
}

export interface DetalhesPV {
    inicial: number;
    nivel: number;
    con: number;
    outros: number;
    habilidades?: number;
}

export interface DetalhesPM {
    inicial: number;
    nivel: number;
    atributo: number;
    outros: number;
    habilidades?: number;
}

export interface DetalhesDeslocamento {
    base: number;
    armadura: number;
    outros: number;
}

export interface StatusBarra {
    atual: number;
    maximo: number;
    temporario: number;
    calculo?: DetalhesCalculo;
    detalhes_pv?: DetalhesPV;
    detalhes_pm?: DetalhesPM;
}

export interface ModificadorDetalhes {
    base: number;
    des_mod: number;
    armadura: number;
    escudo: number;
    outros: number;
}

export interface Defesa {
    total: number;
    detalhes: ModificadorDetalhes;
}

// --- 1. NOVA INTERFACE BUFF ---
export interface Buff {
    origem: string;
    atributo: string;
    valor: number;
    duracao?: string;
}

export interface Status {
    pv: StatusBarra;
    pm: StatusBarra;
    defesa: Defesa;
    rd: string[]; // Lista de strings ("Fogo 10")
    deslocamento: number;
    detalhes_deslocamento?: DetalhesDeslocamento;
    efeitos_ativos?: string[];
    buffs?: Buff[];
    proficiencias: string[];
    imunidades: string[];
    sentidos: string[];
}

export interface PericiaInfo {
    treino: number;
    bonus_nivel: number;
    atributo_valor: number;
    outros: number;
    total: number;
    bonus_automatico?: number;
    atributo_selecionado?: string;
    atributos_possiveis?: string[];
    atributo_override?: string;
    fontes_bonus?: string[];
}

export interface Ataque {
    nome: string;
    bonus_ataque: number;
    dano: string;
    critico: string;
    tipo: string;
    alcance: string;
}

export interface Aprimoramento {
    custo: string;
    descricao: string;
}

export interface Magia {
    nome: string;
    circulo: number;
    escola: string;
    execucao: string;
    tipo?: string;
    alcance: string;
    alvo?: string;
    alvo_area?: string;
    duracao: string;
    resistencia: string;
    custo_pm: number;
    descricao: string;
    fonte?: string; // Adicionado para compatibilidade
    aprimoramentos?: Aprimoramento[];
}

export interface Combate {
    ataques: Ataque[];
    magias: Magia[];
    cd_magias: number;
    bba: number;
    iniciativa: number;
}

export interface Item {
    nome: string;
    qtd: number;
    espaco: number;
    equipado: boolean;
    local: string;
}

export interface Dinheiro {
    tl: number;
    tp: number;
    to: number;
}

export interface Inventario {
    dinheiro: Dinheiro;
    equipamentos: Item[];
    carga_total: number;
    carga_maxima: number;
}

export interface HabilidadeAtivavel {
    custo: number;
    acao?: string;
    alcance?: string;
    duracao?: string;
    resistencia?: string;
    efeito?: string;
    gatilho?: string;
    restricao?: string;
    nome_acumulo?: string;
    reducao_se_acumular?: number;
    // Tipagem para os modificadores matemáticos no JSON
    modificadores?: { atributo: string; valor: number; }[];
}

export interface Habilidade {
    nome: string;
    tipo: string;
    descricao: string;
    fonte?: string;
    nivel?: number;
    requisitos?: string[];
    escolhas_aplicadas?: Record<string, any>;
    precisaEscolha?: boolean;

    // Campos de efeitos
    efeitos?: {
        habilidade_ativavel?: HabilidadeAtivavel;
        [key: string]: any;
    };

    // --- 3. Atalho para modificadores (opcional, mas ajuda o TS) ---
    modificadores?: { atributo: string; valor: number; }[];
}

export interface Personagem {
    _id?: string;
    usuario_id: string;

    cabecalho: Cabecalho;
    classes: ClasseInfo[];
    descricao: Descricao;

    atributos_base: Atributos;
    atributos: Atributos;

    modificadores_raciais: Record<string, number>;
    modificadores_envelhecimento: Record<string, number>;
    modificadores_outros: Record<string, number>;

    escolhas_atributos_raciais: string[];
    escolhas_origem: string[];

    status: Status;
    pericias: Record<string, PericiaInfo>;
    proficiencias: string[];
    combate: Combate;

    habilidades: Habilidade[];
    inventario: Inventario;
}

// --- TIPOS DE DADOS ESTÁTICOS ---
export interface DadosRaca {
    attrs: Record<string, number>;
    escolhas: number;
    tamanho: string;
    habilidades: string[];
}

export interface DadosClasse {
    pv_ini: number;
    pv_niv: number;
    pm_ini: number;
    pm_niv: number;
    pericias_fixas: string[];
    pericias_lista: string[];
    qtd_escolhas: number;
    proficiencias: string[];
    habilidades: string[];
}

export interface DadosOrigem {
    descricao: string;
    itens: string;
    qtd_escolhas: number;
    pericias_fixas: string[];
    beneficios_lista: string[];
}

export interface DadosHabilidade {
    nome: string;
    tipo: string;
    classe?: string;
    nivel?: number;
    descricao: string;
    requisitos?: string[];
    efeitos?: any;
}