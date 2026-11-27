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
export const fetchAmeacas = () => api.get('/ameacas/?limite=500');
export const fetchAmeaca = (id: string) => api.get(`/ameacas/${id}`);

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

export default api;
