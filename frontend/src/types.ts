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

// Index signature para permitir acesso dinâmico (ex: atributos['forca'])
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
// Interface unificada para o campo 'calculo' que vem do backend
export interface DetalhesCalculo {
    inicial: number;
    nivel: number;
    outros: number;
    // Opcionais pois dependem se é PV ou PM
    con?: number;
    atributo?: number;
}

export interface DetalhesPV {
    inicial: number;
    nivel: number;
    con: number;
    outros: number;
}

export interface DetalhesPM {
    inicial: number;
    nivel: number;
    atributo: number;
    outros: number;
}

export interface DetalhesDeslocamento {
    base: number;
    armadura: number;
    outros: number;
}
// ----------------------------------------------------

export interface StatusBarra {
    atual: number;
    maximo: number;
    temporario: number;

    // Novo padrão do backend
    calculo?: DetalhesCalculo;

    // Campos antigos para retrocompatibilidade
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

// RD agora é string simples no novo sistema (ex: "Fogo 10")
// Mantemos a interface antiga comentada caso precise reverter
// export interface RD { tipo: string; valor: number; fonte?: string; }

export interface Defesa {
    total: number;
    detalhes: ModificadorDetalhes;
}

export interface Status {
    pv: StatusBarra;
    pm: StatusBarra;
    defesa: Defesa;

    // CORREÇÃO: RD agora é uma lista de strings
    rd: string[];

    deslocamento: number;
    detalhes_deslocamento?: DetalhesDeslocamento;
}

export interface PericiaInfo {
    treino: number;      // 0 = destreinado, 1 = treinado, 2 = expert
    bonus_nivel: number;
    atributo_valor: number;
    outros: number;
    total: number;
    atributo_override?: string;
}

export interface Ataque {
    nome: string;
    bonus_ataque: number;
    dano: string;
    critico: string;
    tipo: string;
    alcance: string;
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

export interface Habilidade {
    nome: string;
    tipo: string;
    descricao?: string;
    fonte?: string;
    escolhas_aplicadas?: Record<string, any>;

    // Propriedades opcionais de UI
    precisaEscolha?: boolean;
    efeitos?: any;
}

// --- INTERFACE PRINCIPAL ---
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