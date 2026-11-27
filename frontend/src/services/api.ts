import axios from 'axios';
import type { Personagem } from '../types';

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const IS_LOCAL_STORAGE =
    (import.meta.env.VITE_STORAGE_MODE || '').trim().toLowerCase() === 'local';

const LS_KEY = 't20_personagens_v1';

function lerPersonagensLocal(): Personagem[] {
    try {
        const raw = localStorage.getItem(LS_KEY);
        if (!raw) return [];
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    } catch {
        return [];
    }
}

function salvarPersonagensLocal(lista: Personagem[]): void {
    localStorage.setItem(LS_KEY, JSON.stringify(lista));
}

function gerarIdLocal(): string {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
        return crypto.randomUUID();
    }
    return `local-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

// CORREÇÃO: Adicionado 'export' aqui para permitir 'import { api }'
export const api = axios.create({
    baseURL: API_URL,
});

// --- DADOS ESTÁTICOS ---
export const fetchSuplementos = () => api.get('/dados/suplementos');
export const fetchRacas = (incluirSuplementos = true) =>
    api.get(`/racas?incluir_suplementos=${incluirSuplementos}`);
export const fetchClasses = () => api.get('/classes');
export const fetchOrigens = () => api.get('/origens');
export const fetchPericias = () => api.get('/pericias');
export const fetchPoderes = () => api.get('/poderes');

// Detalhes Completos
export const fetchDadosRacas = (incluirSuplementos = true) =>
    api.get(`/dados/racas?incluir_suplementos=${incluirSuplementos}`);
export const fetchDadosClasses = () => api.get('/dados/classes');
export const fetchDadosOrigens = () => api.get('/dados/origens');
export const fetchDadosHabilidades = () => api.get('/dados/habilidades');
export const fetchDadosHabilidadesClasse = () => api.get('/dados/habilidades-classe');
export const fetchDadosMagias = () => api.get('/dados/magias');

// --- DEUSES E PODERES ---
export const fetchDeuses = () => api.get('/deuses');
export const fetchDadosDeuses = () => api.get('/dados/deuses');
export const fetchDadosEscolhas = () => api.get('/dados/escolhas');
export const fetchDadosPoderesConcedidos = () => api.get('/dados/poderes-concedidos');
export const fetchDadosHabilidadesRaciais = () => api.get('/dados/habilidades-raciais');
export const fetchDadosEquipamentos = () => api.get('/dados/equipamentos');

// --- PERSONAGEM (MongoDB local OU localStorage + motor stateless) ---
export const fetchPersonagens = async () => {
    if (IS_LOCAL_STORAGE) {
        return { data: lerPersonagensLocal() };
    }
    return api.get('/personagens/');
};

export const fetchPersonagem = async (id: string) => {
    if (IS_LOCAL_STORAGE) {
        const lista = lerPersonagensLocal();
        const encontrado = lista.find(p => p._id === id);
        if (!encontrado) {
            throw new Error('Personagem não encontrado no navegador');
        }
        const res = await api.post('/personagens/calcular', encontrado);
        const calculado: Personagem = { ...res.data, _id: id };
        salvarPersonagensLocal(lista.map(p => (p._id === id ? calculado : p)));
        return { data: calculado };
    }
    return api.get(`/personagens/${id}`);
};

export const createPersonagem = async (data: Personagem) => {
    if (IS_LOCAL_STORAGE) {
        const res = await api.post('/personagens/calcular', data);
        const novo: Personagem = { ...res.data, _id: gerarIdLocal() };
        const lista = lerPersonagensLocal();
        salvarPersonagensLocal([...lista, novo]);
        return { data: novo };
    }
    return api.post('/personagens/', data);
};

export const updatePersonagem = async (id: string, data: Partial<Personagem>) => {
    if (IS_LOCAL_STORAGE) {
        const lista = lerPersonagensLocal();
        const atual = lista.find(p => p._id === id) || ({} as Personagem);
        const mesclado = { ...atual, ...data, _id: id };
        const res = await api.post('/personagens/calcular', mesclado);
        const atualizado: Personagem = { ...res.data, _id: id };
        const existe = lista.some(p => p._id === id);
        salvarPersonagensLocal(
            existe ? lista.map(p => (p._id === id ? atualizado : p)) : [...lista, atualizado]
        );
        return { data: atualizado };
    }
    return api.put(`/personagens/${id}`, data);
};

export const deletePersonagem = async (id: string) => {
    if (IS_LOCAL_STORAGE) {
        const lista = lerPersonagensLocal().filter(p => p._id !== id);
        salvarPersonagensLocal(lista);
        return { data: null };
    }
    return api.delete(`/personagens/${id}`);
};

// --- AMEAÇAS (BESTIÁRIO) ---
const LOCAL_AMEACAS_KEY = 't20_ameacas_custom_v1';

const lerAmeacasLocal = (): any[] => {
    try {
        const raw = localStorage.getItem(LOCAL_AMEACAS_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch {
        return [];
    }
};

const salvarAmeacasLocal = (lista: any[]) => {
    localStorage.setItem(LOCAL_AMEACAS_KEY, JSON.stringify(lista));
};

export const fetchAmeacas = async () => {
    const res = await api.get('/ameacas/?limite=500');
    if (IS_LOCAL_STORAGE) {
        const custom = lerAmeacasLocal();
        return { data: [...custom, ...(res.data || [])] };
    }
    return res;
};

export const fetchAmeaca = async (id: string) => {
    if (IS_LOCAL_STORAGE && id.startsWith('custom-')) {
        const found = lerAmeacasLocal().find((a: any) => a._id === id);
        if (found) return { data: found };
    }
    return api.get(`/ameacas/${id}`);
};

export const fetchTabelasConstrutorAmeacas = () => api.get('/ameacas/construtor/tabelas');
export const gerarAmeacaManual = (payload: Record<string, any>) => api.post('/ameacas/construtor/gerar', payload);
export const criarAmeaca = async (ameaca: Record<string, any>) => {
    const res = await api.post('/ameacas/', ameaca);
    if (IS_LOCAL_STORAGE) {
        const criada = res.data;
        const lista = lerAmeacasLocal();
        salvarAmeacasLocal([criada, ...lista.filter((a: any) => a._id !== criada._id)]);
        return { data: criada };
    }
    return res;
};

// --- SUPLEMENTOS & ATIVÁVEIS ---
export const fetchDadosDistincoes = () => api.get('/dados/distincoes');
export const fetchDadosTreinador = () => api.get('/dados/treinador');
export const fetchDadosRegrasOpcionais = () => api.get('/dados/regras-opcionais');
export const rolarDuendeSonhosMalucos = (seed?: number) =>
    api.get(seed !== undefined ? `/dados/duende/sonhos-malucos?seed=${seed}` : '/dados/duende/sonhos-malucos');
export const fetchAtivaveisPersonagem = (id: string) => api.get(`/personagens/${id}/ativaveis`);
export const ativarHabilidadePersonagem = async (id: string, nome: string, pm_extra = 0) => {
    if (IS_LOCAL_STORAGE) {
        const lista = lerPersonagensLocal();
        const atual = lista.find(p => p._id === id);
        if (!atual) throw new Error('Personagem não encontrado no navegador');
        const res = await api.post('/personagens/ativar-stateless', {
            personagem: atual,
            nome,
            pm_extra,
        });
        const atualizado: Personagem = { ...res.data.personagem, _id: id };
        salvarPersonagensLocal(lista.map(p => (p._id === id ? atualizado : p)));
        return { data: { ...res.data, personagem: atualizado } };
    }
    return api.post(`/personagens/${id}/ativar`, { nome, pm_extra });
};

// --- LEVEL-UP & HISTÓRICO (MongoDB ou localStorage) ---
const lsHistKey = (id: string) => `t20_historico_v1_${id}`;

function lerHistoricoLocal(id: string): any[] {
    try {
        const raw = localStorage.getItem(lsHistKey(id));
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
    } catch {
        return [];
    }
}

export const subirNivelPersonagem = async (id: string, fichaAtual: Personagem) => {
    if (IS_LOCAL_STORAGE) {
        const classes = (fichaAtual.classes || []).map((c, idx) =>
            idx === 0 ? { ...c, nivel: (c.nivel || 1) + 1 } : c
        );
        const novoNivel = classes[0]?.nivel || 2;
        const atualizadaResp = await updatePersonagem(id, { ...fichaAtual, classes });
        const novaFicha = atualizadaResp.data;
        const hist = lerHistoricoLocal(id);
        const evento = {
            id: gerarIdLocal(),
            nivel: novoNivel,
            tipo: 'level_up',
            timestamp: new Date().toISOString(),
            resumo: [`Subiu para o nível ${novoNivel} (${classes[0]?.nome || 'Classe'})`],
            snapshot: novaFicha,
        };
        localStorage.setItem(lsHistKey(id), JSON.stringify([evento, ...hist]));
        return { data: novaFicha };
    }
    return api.post(`/personagens/${id}/level-up`, {});
};

export const fetchHistoricoPersonagem = async (id: string) => {
    if (IS_LOCAL_STORAGE) {
        return { data: lerHistoricoLocal(id) };
    }
    return api.get(`/personagens/${id}/historico`);
};

export const restaurarEventoHistorico = async (id: string, eventoId: string) => {
    if (IS_LOCAL_STORAGE) {
        const hist = lerHistoricoLocal(id);
        const alvo = hist.find((e: any) => e.id === eventoId);
        if (!alvo?.snapshot) throw new Error('Snapshot não encontrado no histórico local');
        const restauradaResp = await updatePersonagem(id, alvo.snapshot);
        const eventoRest = {
            id: gerarIdLocal(),
            nivel: alvo.nivel,
            tipo: 'restauracao',
            timestamp: new Date().toISOString(),
            resumo: [`Restaurado para o nível ${alvo.nivel}`],
            snapshot: restauradaResp.data,
        };
        localStorage.setItem(lsHistKey(id), JSON.stringify([eventoRest, ...hist]));
        return { data: restauradaResp.data };
    }
    return api.post(`/personagens/${id}/historico/${eventoId}/restaurar`, {});
};

export default api;
