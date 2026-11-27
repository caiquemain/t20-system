import type { Personagem } from '../types';

interface ValidationResult {
    ok: boolean;
    msg: string;
}

const CLASSES_COM_HABILIDADE_MAGIAS = new Set([
    'arcanista', 'bardo', 'clérigo', 'clerigo', 'druida', 'frade', 'ermitão', 'ermitao', 'bruxo', 'mago', 'feiticeiro',
]);

const CLASSES_MAGIAS_DIVINAS = new Set([
    'clérigo', 'clerigo', 'druida', 'frade', 'ermitão', 'ermitao',
]);

function temHabilidadeMagias(ficha: Personagem): boolean {
    const porClasse = (ficha.classes || []).some(c =>
        CLASSES_COM_HABILIDADE_MAGIAS.has((c.nome || '').trim().toLowerCase())
    );
    const porHabilidade = (ficha.habilidades || []).some(h => {
        const n = (h.nome || '').trim().toLowerCase();
        return n === 'magias' || n.startsWith('magias (');
    });
    return porClasse || porHabilidade;
}

function obterCirculoMaximo(ficha: Personagem): number {
    const direto = Number((ficha.combate as { circulo_maximo?: number } | undefined)?.circulo_maximo || 0);
    if (direto > 0) return direto;
    return temHabilidadeMagias(ficha) ? 1 : 0;
}

function podeLancarMagias(ficha: Personagem): boolean {
    return (
        temHabilidadeMagias(ficha)
        || obterCirculoMaximo(ficha) >= 1
        || ((ficha.combate?.magias?.length || 0) > 0)
    );
}

function podeLancarMagiasDivinas(ficha: Personagem): boolean {
    const porClasse = (ficha.classes || []).some(c =>
        CLASSES_MAGIAS_DIVINAS.has((c.nome || '').trim().toLowerCase())
    );
    const linhagemAbencoada = (ficha.habilidades || []).some(h => (h.nome || '').trim().toLowerCase() === 'linhagem abençoada');
    const temMagiaDivina = (ficha.combate?.magias || []).some(m => (m.tipo || '').toLowerCase() === 'divina');
    return porClasse || linhagemAbencoada || temMagiaDivina;
}

export const verificarRequisito = (
    ficha: Personagem,
    req: string,
    poderesEscolhidos: string[] = [],
    subclasseEmEdicao: string = ""
): ValidationResult => {
    const reqLower = req.toLowerCase().trim();

    // 0a. Requisitos de Raça (Ex: "Raça: Duende, Eiradaan, Sílfide", "Raça: Várias", "Não humano")
    if (reqLower.startsWith('raça:') || reqLower.startsWith('raca:')) {
        const bruto = req.split(':').slice(1).join(':').trim();
        const opcoes = bruto.split(/,|\s+ou\s+/i).map(s => s.trim().toLowerCase()).filter(Boolean);
        if (opcoes.includes('várias') || opcoes.includes('varias') || opcoes.includes('qualquer')) {
            return { ok: true, msg: 'Ok' };
        }
        const racaAtual = (ficha.cabecalho?.raca || '').trim().toLowerCase();
        const okRaca = Boolean(racaAtual) && opcoes.some(op => {
            if (racaAtual === op) return true;
            // Ex.: "Suraggel" casa com "Suraggel (Aggelus)" e "Suraggel (Sulfure)"; "Moreau do Lobo" casa com "Moreau"
            if (racaAtual.startsWith(op) || op.startsWith(racaAtual)) return true;
            if (op === 'sereia/tritão' && (racaAtual.includes('sereia') || racaAtual.includes('tritão') || racaAtual.includes('tritao'))) return true;
            return false;
        });
        return {
            ok: okRaca,
            msg: `Requer Raça: ${bruto} (Atual: ${ficha.cabecalho?.raca || 'Nenhuma'})`,
        };
    }

    if (reqLower === 'não humano' || reqLower === 'nao humano') {
        const racaAtual = (ficha.cabecalho?.raca || '').trim().toLowerCase();
        return {
            ok: Boolean(racaAtual) && racaAtual !== 'humano',
            msg: 'Requer raça não humana',
        };
    }

    // 0b. Requisitos de Magia ("Lançar magias", "Lançar magias divinas", "Habilidade Magias", "Lançar magias de Xº círculo")
    if (reqLower === 'lançar magias divinas' || reqLower === 'lancar magias divinas') {
        return {
            ok: podeLancarMagiasDivinas(ficha),
            msg: 'Requer: Lançar magias divinas',
        };
    }

    if (reqLower === 'possuir um familiar') {
        const temFam = (ficha.habilidades || []).some(h => (h.nome || '').toLowerCase().includes('familiar'))
            || poderesEscolhidos.some(p => p.toLowerCase().includes('familiar'));
        return { ok: temFam, msg: 'Requer: Possuir um familiar' };
    }

    const matchCirculo = reqLower.match(/lançar magias de (\d+)[º°o]?\s*c[íi]rculo|lancar magias de (\d+)[º°o]?\s*c[íi]rculo/);
    if (matchCirculo) {
        const circReq = parseInt(matchCirculo[1] || matchCirculo[2], 10);
        const circAtual = obterCirculoMaximo(ficha);
        return {
            ok: circAtual >= circReq,
            msg: `Requer lançar magias de ${circReq}º círculo (Atual: ${circAtual > 0 ? `${circAtual}º` : 'nenhum'})`,
        };
    }

    if (reqLower === 'habilidade magias' || reqLower.includes('habilidade de classe magias')) {
        return {
            ok: temHabilidadeMagias(ficha),
            msg: 'Requer: Habilidade Magias',
        };
    }

    if (
        reqLower === 'lançar magias'
        || reqLower === 'lancar magias'
        || reqLower === 'capacidade de lançar magias'
        || reqLower === 'capacidade de lancar magias'
    ) {
        return {
            ok: podeLancarMagias(ficha),
            msg: 'Requer: Lançar magias',
        };
    }

    // 1. Validação de Caminho/Subclasse (Arcanista, etc)
    if (reqLower.includes('caminho') || reqLower.includes('subclasse')) {
        const partes = reqLower.split(/[:=]/);
        const conteudo = partes[1] ? partes[1].trim() : "";
        const opcoes = conteudo.split(' ou ').map(op => op.trim());

        const temNaFicha = ficha.classes.some(c =>
            c.subclasse && opcoes.includes(c.subclasse.toLowerCase())
        );
        const temNaEdicao = opcoes.includes(subclasseEmEdicao.toLowerCase());

        return {
            ok: temNaFicha || temNaEdicao,
            msg: `Requer Caminho: ${req.split(':')[1]?.trim() || conteudo}`
        };
    }

    // 2. Atributos (Ex: "For 1", "Destreza 3")
    const matchAttr = reqLower.match(/^(for|des|con|int|sab|car)\w*\s?:?\s?(\d+)$/);
    if (matchAttr) {
        const mapaAtributos: Record<string, keyof Personagem['atributos']> = {
            'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
        };
        const sigla = matchAttr[1].substring(0, 3);
        const attrKey = mapaAtributos[sigla];
        const valorMin = parseInt(matchAttr[2], 10);
        const valorAtual = Number(ficha.atributos?.[attrKey] ?? 0);

        return {
            ok: valorAtual >= valorMin,
            msg: `Requer ${sigla.toUpperCase()} ${valorMin} (Atual: ${valorAtual})`
        };
    }

    // 3. Perícias (Ex: "Treinado em Luta", "Treinado em Misticismo ou Religião", "Treinado em Ofício (Escriba)")
    if (reqLower.includes('treinado em')) {
        const bruto = req.replace(/treinado em /i, '').trim();
        const opcoes = bruto.split(/\s+ou\s+/i).map(s => s.trim()).filter(Boolean);
        const periciasKeys = Object.keys(ficha.pericias || {});

        const isTreinado = opcoes.some(op => {
            const opLow = op.toLowerCase();
            const keyExata = periciasKeys.find(k => k.toLowerCase() === opLow);
            if (keyExata && (ficha.pericias[keyExata]?.treino || 0) > 0) return true;
            // Se pedir "Ofício (X)" e o personagem tiver "Ofício" genérico treinado, também libera se não houver chave específica
            if (opLow.startsWith('ofício') || opLow.startsWith('oficio')) {
                const keyOficio = periciasKeys.find(k => k.toLowerCase() === 'ofício' || k.toLowerCase() === 'oficio');
                if (keyOficio && (ficha.pericias[keyOficio]?.treino || 0) > 0) return true;
            }
            return false;
        });

        return {
            ok: isTreinado,
            msg: `Requer treino em ${bruto}`
        };
    }

    // 4. Nível (Ex: "Nível 5", "6º nível", "5º nível de arcanista")
    const matchNivel =
        reqLower.match(/^(\d+)[º°o]?\s*(?:nível|nivel)(?:\s+de\s+(.+))?$/)
        || reqLower.match(/^(?:nível|nivel)\s*(\d+)(?:\s+de\s+(.+))?$/);
    if (matchNivel) {
        const nivelReq = parseInt(matchNivel[1], 10);
        const classeReq = (matchNivel[2] || '').trim();
        let nivelAtual = Number(ficha.cabecalho?.nivel_total || 1);
        if (classeReq) {
            const cls = (ficha.classes || []).find(c => (c.nome || '').toLowerCase() === classeReq);
            nivelAtual = cls ? Number(cls.nivel || 0) : 0;
        }
        return {
            ok: nivelAtual >= nivelReq,
            msg: classeReq
                ? `Requer ${nivelReq}º nível de ${classeReq} (Atual: ${nivelAtual})`
                : `Requer Nível ${nivelReq} (Atual: ${nivelAtual})`
        };
    }

    // 5. Proficiências (Ex: "Proficiência com escudos", "Armaduras Pesadas")
    const keywordsProf = ['proficiência', 'proficiencia', 'escudos', 'armas', 'armaduras'];
    if (keywordsProf.some(k => reqLower.includes(k))) {
        const statusProfs: unknown = ficha.status?.proficiencias;
        const statusProfsList: string[] = Array.isArray(statusProfs)
            ? statusProfs.map(String)
            : typeof statusProfs === 'string'
                ? statusProfs.split(/[,;]/).map(s => s.trim()).filter(Boolean)
                : [];
        const listaProfs: string[] = [
            ...(Array.isArray(ficha.proficiencias) ? ficha.proficiencias : []),
            ...statusProfsList,
        ];
        const temProficiencia = listaProfs.some(prof => reqLower.includes(prof.toLowerCase()));
        if (temProficiencia) {
            return { ok: true, msg: 'Ok' };
        }
    }

    // 6. Outros Poderes / Habilidades (suporta "Poder A ou Poder B")
    const opcoesPoder = reqLower.split(/\s+ou\s+/).map(s => s.trim()).filter(Boolean);
    const habsLow = (ficha.habilidades || []).map(h => (h.nome || '').toLowerCase());
    const selLow = poderesEscolhidos.map(p => p.toLowerCase());
    const temPoder = opcoesPoder.some(op => habsLow.includes(op) || selLow.includes(op));

    if (temPoder) return { ok: true, msg: 'Ok' };

    return { ok: false, msg: `Requer: ${req}` };
};

export const validarTodosRequisitos = (
    ficha: Personagem,
    requisitos: string[] = [],
    poderesEscolhidos: string[] = [],
    subclasseEmEdicao: string = ""
) => {
    if (!requisitos || requisitos.length === 0) return { apto: true, erros: [] };

    const analises = requisitos.map(r => verificarRequisito(ficha, r, poderesEscolhidos, subclasseEmEdicao));
    const erros = analises.filter(a => !a.ok).map(a => a.msg);

    return { apto: erros.length === 0, erros };
};