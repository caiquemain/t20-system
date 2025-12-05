import type { Personagem } from '../types';

interface ValidationResult {
    ok: boolean;
    msg: string;
}

export const verificarRequisito = (ficha: Personagem, req: string, poderesEscolhidos: string[] = []): ValidationResult => {
    const reqLower = req.toLowerCase().trim();

    // LOG DE DEBUG (Filtra para não spammar demais, foca nos atributos/perícias)
    const isDebug = reqLower.includes('des') || reqLower.includes('luta') || reqLower.includes('treinado');
    if (isDebug) {
        console.groupCollapsed(`🕵️‍♂️ Validando Requisito: "${req}"`);
    }

    // 1. Atributos (ex: "For 1", "Destreza 3")
    // Regex ajustada para ser mais flexível com espaços e dois pontos
    const matchAttr = reqLower.match(/^(for|des|con|int|sab|car)\w*\s?:?\s?(\d+)$/);

    if (matchAttr) {
        const mapaAtributos: Record<string, string> = {
            'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
        };

        const sigla = matchAttr[1].substring(0, 3); // Pega 'des' de 'destreza'
        const attrKey = mapaAtributos[sigla];
        const valorMin = parseInt(matchAttr[2]);

        // @ts-ignore
        const valorAtual = ficha.atributos[attrKey] || 0;

        if (isDebug) {
            console.log(`Atributo detectado: ${attrKey}`);
            console.log(`Mínimo: ${valorMin} | Atual na Ficha: ${valorAtual}`);
            console.log(`Resultado: ${valorAtual >= valorMin ? 'APROVADO' : 'REPROVADO'}`);
        }

        if (isDebug) console.groupEnd();

        return {
            ok: valorAtual >= valorMin,
            msg: `Requer ${sigla.toUpperCase()} ${valorMin} (Atual: ${valorAtual})`
        };
    }

    // 2. Perícias (ex: "Treinado em Luta")
    if (reqLower.includes('treinado em')) {
        const periciaNome = req.replace(/treinado em /i, '').trim();

        // Busca a chave exata no objeto de perícias
        const periciaKey = Object.keys(ficha.pericias).find(k => k.toLowerCase() === periciaNome.toLowerCase());
        const dadosPericia = periciaKey ? ficha.pericias[periciaKey] : null;
        const isTreinado = dadosPericia ? dadosPericia.treino > 0 : false;

        if (isDebug) {
            console.log(`Perícia detectada: "${periciaNome}"`);
            console.log(`Encontrada na ficha? ${periciaKey ? 'Sim' : 'Não'}`);
            console.log(`Dados da perícia:`, dadosPericia);
            console.log(`Está treinado? ${isTreinado}`);
        }

        if (isDebug) console.groupEnd();

        return {
            ok: isTreinado,
            msg: `Requer treino em ${periciaNome}`
        };
    }

    // 3. Nível
    const matchNivel = reqLower.match(/(?:nível|nivel)\s?(\d+)/);
    if (matchNivel) {
        const nivelReq = parseInt(matchNivel[1]);
        const nivelChar = ficha.cabecalho.nivel_total;

        if (isDebug) console.groupEnd();
        return {
            ok: nivelChar >= nivelReq,
            msg: `Requer Nível ${nivelReq} (Atual: ${nivelChar})`
        };
    }

    // 4. Outros Poderes
    const temNaFicha = ficha.habilidades.some(h => h.nome.toLowerCase() === reqLower);
    const temNaSelecao = poderesEscolhidos.map(p => p.toLowerCase()).includes(reqLower);

    if (isDebug) console.groupEnd();

    if (temNaFicha || temNaSelecao) {
        return { ok: true, msg: 'Ok' };
    }

    return { ok: false, msg: `Requer habilidade: ${req}` };
};

export const validarTodosRequisitos = (ficha: Personagem, requisitos: string[] = [], poderesEscolhidos: string[] = []) => {
    if (!requisitos || requisitos.length === 0) return { apto: true, erros: [] };

    const analises = requisitos.map(r => verificarRequisito(ficha, r, poderesEscolhidos));
    const erros = analises.filter(a => !a.ok).map(a => a.msg);

    return { apto: erros.length === 0, erros };
};