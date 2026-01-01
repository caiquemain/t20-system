import type { Personagem } from '../types';

interface ValidationResult {
    ok: boolean;
    msg: string;
}

export const verificarRequisito = (
    ficha: Personagem,
    req: string,
    poderesEscolhidos: string[] = [],
    subclasseEmEdicao: string = ""
): ValidationResult => {
    const reqLower = req.toLowerCase().trim();

    // 1. Validação de Caminho/Subclasse (Arcanista, etc)
    if (reqLower.includes('caminho') || reqLower.includes('subclasse')) {
        const partes = reqLower.split(/[:=]/); // Divide por : ou =
        const conteudo = partes[1] ? partes[1].trim() : "";
        const opcoes = conteudo.split(' ou ').map(op => op.trim());

        // Verifica na ficha salva OU na edição atual
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
        const mapaAtributos: Record<string, string> = {
            'for': 'forca', 'des': 'destreza', 'con': 'constituicao',
            'int': 'inteligencia', 'sab': 'sabedoria', 'car': 'carisma'
        };
        const sigla = matchAttr[1].substring(0, 3);
        const attrKey = mapaAtributos[sigla];
        const valorMin = parseInt(matchAttr[2]);
        // @ts-ignore
        const valorAtual = ficha.atributos[attrKey] || 0;

        return {
            ok: valorAtual >= valorMin,
            msg: `Requer ${sigla.toUpperCase()} ${valorMin} (Atual: ${valorAtual})`
        };
    }

    // 3. Perícias (Ex: "Treinado em Luta")
    if (reqLower.includes('treinado em')) {
        const periciaNome = req.replace(/treinado em /i, '').trim();
        const periciaKey = Object.keys(ficha.pericias).find(k => k.toLowerCase() === periciaNome.toLowerCase());
        const isTreinado = periciaKey ? ficha.pericias[periciaKey].treino > 0 : false;

        return {
            ok: isTreinado,
            msg: `Requer treino em ${periciaNome}`
        };
    }

    // 4. Nível (Ex: "Nível 5", "6º nível de guerreiro")
    const matchNivel = reqLower.match(/(?:nível|nivel)\s?(\d+)/);
    if (matchNivel) {
        const nivelReq = parseInt(matchNivel[1]);
        const nivelChar = ficha.cabecalho.nivel_total;
        return {
            ok: nivelChar >= nivelReq,
            msg: `Requer Nível ${nivelReq} (Atual: ${nivelChar})`
        };
    }

    // --- [NOVO] 5. Proficiências (Ex: "Proficiência com escudos", "Armaduras Pesadas") ---
    // Verifica se o texto do requisito contém alguma das proficiências que o personagem JÁ TEM.
    // Ex: Se char tem "Escudos" e requisito é "Proficiência com escudos", reqLower.includes("escudos") dá true.
    if (ficha.proficiencias && ficha.proficiencias.length > 0) {
        const temProficiencia = ficha.proficiencias.some(prof => reqLower.includes(prof.toLowerCase()));

        // Só valida como "ok" se o requisito realmente parecer ser sobre proficiência/equipamento
        const keywordsProf = ['proficiência', 'proficiencia', 'escudos', 'armas', 'armaduras'];
        if (temProficiencia && keywordsProf.some(k => reqLower.includes(k))) {
            return { ok: true, msg: 'Ok' };
        }
    }

    // 6. Outros Poderes (Ex: "Foco Vital")
    // Verifica na ficha ou na lista de pré-seleção
    const temNaFicha = ficha.habilidades.some(h => h.nome.toLowerCase() === reqLower);
    const temNaSelecao = poderesEscolhidos.map(p => p.toLowerCase()).includes(reqLower);

    if (temNaFicha || temNaSelecao) return { ok: true, msg: 'Ok' };

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