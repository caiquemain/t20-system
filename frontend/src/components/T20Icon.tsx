import React from 'react';
import {
    AlertTriangle,
    ArrowLeft,
    ArrowRight,
    Award,
    Backpack,
    BookMarked,
    BookOpen,
    Check,
    Coins,
    Compass,
    Crosshair,
    Crown,
    Dices,
    Dna,
    Droplets,
    Eye,
    Feather,
    FileDown,
    FileText,
    Filter,
    Flame,
    FlaskConical,
    Footprints,
    Heart,
    History,
    Home,
    Info,
    List,
    Lock,
    Moon,
    Mountain,
    Package,
    Pencil,
    Plus,
    RefreshCw,
    Ruler,
    Save,
    ScrollText,
    Search,
    Send,
    Settings,
    Shield,
    ShieldAlert,
    ShieldBan,
    ShieldCheck,
    ShieldHalf,
    Skull,
    Snowflake,
    Sparkles,
    Star,
    Sun,
    Swords,
    Target,
    Trash2,
    TrendingUp,
    User,
    Wand2,
    Waves,
    Weight,
    Wrench,
    X,
    Zap,
    type LucideIcon,
} from 'lucide-react';

export type IconName =
    // Status & Vitalidade
    | 'hp'
    | 'pm'
    | 'defesa'
    | 'deslocamento'
    | 'escalada'
    | 'natacao'
    | 'voo'
    | 'tamanho'
    | 'xp'
    | 'nivel'
    | 'descanso'
    // Combate & Equipamentos
    | 'espada'
    | 'ataque'
    | 'dano'
    | 'critico'
    | 'arco'
    | 'armadura'
    | 'escudo'
    | 'mochila'
    | 'moedas'
    | 'peso'
    | 'item'
    | 'ferramenta'
    | 'pocao'
    // Magia & Grimório
    | 'magia'
    | 'grimorio'
    | 'pergaminho'
    | 'energia'
    | 'fogo'
    | 'gelo'
    | 'raio'
    | 'acido'
    | 'trevas'
    | 'luz'
    // Personagem & Ficha
    | 'usuario'
    | 'raca'
    | 'classe'
    | 'origem'
    | 'deus'
    | 'pericia'
    | 'habilidade'
    | 'poder'
    | 'dado'
    | 'historico'
    | 'efeito'
    // Sentidos & Proteções
    | 'visao'
    | 'imunidade'
    | 'resistencia'
    | 'vulnerabilidade'
    | 'veneno'
    | 'monstro'
    | 'bestiario'
    // Ações de UI
    | 'pdf'
    | 'roll20'
    | 'salvar'
    | 'editar'
    | 'excluir'
    | 'adicionar'
    | 'fechar'
    | 'buscar'
    | 'filtro'
    | 'voltar'
    | 'avancar'
    | 'check'
    | 'alerta'
    | 'info'
    | 'cadeado'
    | 'refresh'
    | 'config'
    | 'lista'
    | 'nota'
    | 'home';

const ICON_MAP: Record<IconName, LucideIcon> = {
    hp: Heart,
    pm: Sparkles,
    defesa: Shield,
    deslocamento: Footprints,
    escalada: Mountain,
    natacao: Waves,
    voo: Feather,
    tamanho: Ruler,
    xp: TrendingUp,
    nivel: Award,
    descanso: Moon,

    espada: Swords,
    ataque: Swords,
    dano: Flame,
    critico: Crosshair,
    arco: Target,
    armadura: Shield,
    escudo: ShieldCheck,
    mochila: Backpack,
    moedas: Coins,
    peso: Weight,
    item: Package,
    ferramenta: Wrench,
    pocao: FlaskConical,

    magia: Wand2,
    grimorio: BookOpen,
    pergaminho: ScrollText,
    energia: Zap,
    fogo: Flame,
    gelo: Snowflake,
    raio: Zap,
    acido: Droplets,
    trevas: Moon,
    luz: Sun,

    usuario: User,
    raca: Dna,
    classe: ShieldHalf,
    origem: Compass,
    deus: Crown,
    pericia: BookMarked,
    habilidade: Star,
    poder: Zap,
    dado: Dices,
    historico: History,
    efeito: Sparkles,

    visao: Eye,
    imunidade: ShieldBan,
    resistencia: ShieldAlert,
    vulnerabilidade: AlertTriangle,
    veneno: Skull,
    monstro: Skull,
    bestiario: Skull,

    pdf: FileDown,
    roll20: Send,
    salvar: Save,
    editar: Pencil,
    excluir: Trash2,
    adicionar: Plus,
    fechar: X,
    buscar: Search,
    filtro: Filter,
    voltar: ArrowLeft,
    avancar: ArrowRight,
    check: Check,
    alerta: AlertTriangle,
    info: Info,
    cadeado: Lock,
    refresh: RefreshCw,
    config: Settings,
    lista: List,
    nota: FileText,
    home: Home,
};

export interface T20IconProps {
    name: IconName;
    size?: number;
    color?: string;
    strokeWidth?: number;
    className?: string;
    style?: React.CSSProperties;
    title?: string;
}

export const T20Icon: React.FC<T20IconProps> = ({
    name,
    size = 16,
    color = 'currentColor',
    strokeWidth = 2,
    className,
    style,
    title,
}) => {
    const Component = ICON_MAP[name];
    return (
        <Component
            size={size}
            color={color}
            strokeWidth={strokeWidth}
            className={className}
            aria-hidden={title ? undefined : true}
            style={{
                display: 'inline-block',
                verticalAlign: 'middle',
                flexShrink: 0,
                ...style,
            }}
        >
            {title ? <title>{title}</title> : null}
        </Component>
    );
};

export interface EfeitoVisual {
    icon: IconName;
    color: string;
    bg: string;
}

/** Resolve ícone e paleta visual para uma string de `status.efeitos_ativos`. */
export function getEfeitoVisual(efeito: string): EfeitoVisual {
    const lower = efeito.toLowerCase();
    if (lower.includes('imune')) {
        return { icon: 'imunidade', color: '#4caf50', bg: 'rgba(76, 175, 80, 0.1)' };
    }
    if (lower.includes('visão') || lower.includes('sentido') || lower.includes('faro')) {
        return { icon: 'visao', color: '#00bcd4', bg: 'rgba(0, 188, 212, 0.1)' };
    }
    if (lower.includes('escalada')) {
        return { icon: 'escalada', color: '#8bc34a', bg: 'rgba(139, 195, 74, 0.1)' };
    }
    if (lower.includes('tamanho')) {
        return { icon: 'tamanho', color: '#ffeb3b', bg: 'rgba(255, 235, 59, 0.1)' };
    }
    if (lower.includes('tipo de criatura')) {
        return { icon: 'raca', color: '#ce93d8', bg: 'rgba(206, 147, 216, 0.1)' };
    }
    if (lower.includes('ataque com:')) {
        return { icon: 'ataque', color: '#ff7043', bg: 'rgba(255, 112, 67, 0.1)' };
    }
    if (lower.includes('dano')) {
        return { icon: 'dano', color: '#ef5350', bg: 'rgba(239, 83, 80, 0.1)' };
    }
    if (lower.includes('resistências') || lower.includes('rd ')) {
        return { icon: 'resistencia', color: '#ffb74d', bg: 'rgba(255, 183, 77, 0.1)' };
    }
    return { icon: 'efeito', color: '#2196f3', bg: 'rgba(33, 150, 243, 0.1)' };
}
