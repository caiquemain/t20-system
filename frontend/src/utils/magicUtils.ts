// frontend/src/utils/magicUtils.ts

// Cores das Escolas (Inspirado em convenções de RPG)
export const SCHOOL_COLORS: Record<string, string> = {
    'Abjuração': '#4fc3f7',   // Azul Claro (Proteção)
    'Adivinhação': '#26c6da', // Ciano (Visão)
    'Convocação': '#ffb74d',  // Laranja (Invocação)
    'Encantamento': '#f06292',// Rosa (Mente)
    'Evocação': '#e57373',    // Vermelho Claro (Fogo/Dano)
    'Ilusão': '#ba68c8',      // Roxo (Mistério)
    'Necromancia': '#81c784', // Verde (Vida/Morte)
    'Transmutação': '#fff176',// Amarelo (Mudança)
    'default': '#9e9e9e'      // Cinza
};

// Cores dos Círculos (Raridade/Poder)
export const CIRCLE_COLORS: Record<number, string> = {
    1: '#ffffff', // Comum (Branco)
    2: '#66bb6a', // Incomum (Verde)
    3: '#42a5f5', // Raro (Azul)
    4: '#ab47bc', // Épico (Roxo)
    5: '#ffca28'  // Lendário (Dourado)
};

export const getSchoolColor = (escola?: string) => {
    if (!escola) return SCHOOL_COLORS['default'];
    // Busca parcial (ex: "Evocação" encontra a chave)
    const key = Object.keys(SCHOOL_COLORS).find(k => escola.includes(k));
    return key ? SCHOOL_COLORS[key] : SCHOOL_COLORS['default'];
};

export const getCircleColor = (circulo: number) => {
    return CIRCLE_COLORS[circulo] || '#ffffff';
};

export const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#ff5252'; // Padrão/Universal agora é Vermelho
    const t = tipo.toLowerCase();
    if (t.includes('arcana')) return '#d236d2'; // Roxo/Magenta
    if (t.includes('divina')) return '#ffc107'; // Dourado/Amarelo
    return '#ff5252'; // Vermelho (Universal)
};
// 🆕 LOTE R5 — Tabela 4-1 + reduções (espelho de app/src/regras/custo_magia.py)
export const CUSTO_POR_CIRCULO: Record<number, number> = { 1: 1, 2: 3, 3: 6, 4: 10, 5: 15 };

export function obterAtributoChaveMagiaView(ficha: any): { chave: string; sigla: string; valor: number } {
    for (const c of ficha?.classes || []) {
        const nome = (c?.nome || '').trim();
        const sub = (c?.subclasse || '').trim();
        if (nome === 'Arcanista') {
            const chave = sub === 'Feiticeiro' ? 'carisma' : 'inteligencia';
            return { chave, sigla: chave === 'carisma' ? 'CAR' : 'INT', valor: Number(ficha?.atributos?.[chave] || 0) };
        }
        if (nome === 'Bardo' || nome === 'Feiticeiro') {
            return { chave: 'carisma', sigla: 'CAR', valor: Number(ficha?.atributos?.carisma || 0) };
        }
        if (nome === 'Clérigo' || nome === 'Druida') {
            return { chave: 'sabedoria', sigla: 'SAB', valor: Number(ficha?.atributos?.sabedoria || 0) };
        }
        if (nome === 'Mago' || nome === 'Bruxo') {
            return { chave: 'inteligencia', sigla: 'INT', valor: Number(ficha?.atributos?.inteligencia || 0) };
        }
    }
    return { chave: 'inteligencia', sigla: 'INT', valor: Number(ficha?.atributos?.inteligencia || 0) };
}

export function calcularLimitePmMagiaView(ficha: any, comoRitual = false) {
    const nivel = Math.max(1, Number(ficha?.cabecalho?.nivel_total || 1));
    const habs: any[] = ficha?.habilidades || [];
    const temMagiaIlimitada = habs.some(
        h => h?.efeitos?.limite_pm_soma_atributo_chave || (h?.nome || '') === 'Magia Ilimitada'
    );
    const temCelebrarRitual = habs.some(
        h => h?.efeitos?.celebrar_ritual_dobra_limite_pm || (h?.nome || '') === 'Celebrar Ritual'
    );

    const partes: string[] = [`Nível ${nivel}`];
    let limiteBase = nivel;

    if (temMagiaIlimitada) {
        const attr = obterAtributoChaveMagiaView(ficha);
        if (attr.valor > 0) {
            limiteBase += attr.valor;
            partes.push(`+${attr.valor} ${attr.sigla} (Magia Ilimitada)`);
        }
    }

    const limiteBackend = Number(ficha?.combate?.limite_pm_magia || 0);
    if (limiteBackend > limiteBase) {
        limiteBase = limiteBackend;
    }

    const limiteRitual = temCelebrarRitual ? limiteBase * 2 : null;
    const limite = comoRitual && limiteRitual ? limiteRitual : limiteBase;
    if (comoRitual && limiteRitual) {
        partes.push('×2 (Celebrar Ritual)');
    }

    return {
        limite,
        limiteBase,
        limiteRitual,
        temMagiaIlimitada,
        temCelebrarRitual,
        detalhe: partes.join(' '),
    };
}

export function calcularCustoMagiaView(magia: any, ficha: any) {
    const circ = parseInt(String(magia?.circulo), 10) || 1;
    const base = CUSTO_POR_CIRCULO[circ] ?? 1;
    const fontes: { label: string; valor: number }[] = [{ label: `Custo do ${circ}º círculo (Tabela 4-1)`, valor: base }];
    let total = base;
    const nomeMagiaLow = (magia?.nome || '').trim().toLowerCase();
    const tipoMagiaLow = (magia?.tipo || '').trim().toLowerCase();
    const escolaMagia = (magia?.escola || '').trim();

    for (const hab of ficha?.habilidades || []) {
        const ef: any = { ...(hab.efeitos || {}), ...(hab.escolhas_aplicadas || {}) };
        const mult = ef.reducao_custo_magia_global;
        if (typeof mult === 'number' && mult > 0 && mult < 1) {
            const antes = total;
            total = Math.floor(total * mult);
            fontes.push({ label: `${hab.nome} (×${mult})`, valor: total - antes });
        }
        const rc = ef.reducao_custo_magia;
        if (rc && Array.isArray(rc.nomes) && rc.nomes.includes(magia?.nome)) {
            const v = parseInt(rc.valor, 10) || 1;
            total -= v;
            fontes.push({ label: `${hab.nome} (−${v} PM)`, valor: -v });
        }
        if (ef.foco_em_magia || (hab.nome || '') === 'Foco em Magia') {
            const alvoFoco = (ef.magia || ef.magia_escolhida || ef.foco_magia || '').trim().toLowerCase();
            if (alvoFoco && alvoFoco === nomeMagiaLow) {
                total -= 1;
                fontes.push({ label: 'Foco em Magia (−1 PM)', valor: -1 });
            }
        }
    }

    // Mestre em Escola (custo_por_escola negativo)
    const redEscola = Number(ficha?.combate?.custo_por_escola?.[escolaMagia] || 0);
    if (redEscola < 0) {
        total += redEscola;
        fontes.push({ label: `Mestre em Escola (${escolaMagia})`, valor: redEscola });
    }

    // Itens mágicos / esotéricos equipados
    const equipados = new Set<string>(
        (ficha?.inventario?.equipamentos || [])
            .filter((it: any) => it?.equipado)
            .map((it: any) => (it?.nome || '').trim().toLowerCase())
    );
    const ehArcana = tipoMagiaLow.includes('arcan') || tipoMagiaLow.includes('universal');
    const ehDivina = tipoMagiaLow.includes('divin') || tipoMagiaLow.includes('universal');
    if (equipados.has('cajado do poder') && ehArcana) {
        total -= 1;
        fontes.push({ label: 'Cajado do poder (−1 PM)', valor: -1 });
    }
    if (equipados.has('símbolo abençoado') && ehDivina && (ficha?.cabecalho?.deus || '').trim()) {
        total -= 1;
        fontes.push({ label: 'Símbolo abençoado (−1 PM)', valor: -1 });
    }
    if (equipados.has('medalhão de prata') && (magia?.alcance || '').trim().toLowerCase() === 'pessoal') {
        total -= 1;
        fontes.push({ label: 'Medalhão de prata (−1 PM)', valor: -1 });
    }

    // Condição Alquebrado (+1 PM)
    const conds: string[] = (ficha?.condicoes_ativas || []).map((c: string) => (c || '').toLowerCase());
    if (conds.includes('alquebrado')) {
        total += 1;
        fontes.push({ label: 'Condição: Alquebrado (+1 PM)', valor: 1 });
    }

    total = Math.max(1, total); // mínimo 1 PM (0 só para Truque)
    return { total, base, fontes };
}
