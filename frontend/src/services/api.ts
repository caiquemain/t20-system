import axios from 'axios';
import type { Personagem } from '../types';

const API_URL = 'http://localhost:8000';

// CORREÇÃO: Adicionado 'export' aqui para permitir 'import { api }'
export const api = axios.create({
    baseURL: API_URL,
});

// --- DADOS ESTÁTICOS ---
export const fetchRacas = () => api.get('/racas');
export const fetchClasses = () => api.get('/classes');
export const fetchOrigens = () => api.get('/origens');
export const fetchPericias = () => api.get('/pericias');
export const fetchPoderes = () => api.get('/poderes');

// Detalhes Completos
export const fetchDadosRacas = () => api.get('/dados/racas');
export const fetchDadosClasses = () => api.get('/dados/classes');
export const fetchDadosOrigens = () => api.get('/dados/origens');
export const fetchDadosHabilidades = () => api.get('/dados/habilidades');
export const fetchDadosHabilidadesClasse = () => api.get('/dados/habilidades-classe');
export const fetchDadosMagias = () => api.get('/dados/magias');

// --- DEUSES E PODERES ---
export const fetchDeuses = () => api.get('/deuses');
export const fetchDadosDeuses = () => api.get('/dados/deuses');
export const fetchDadosPoderesConcedidos = () => api.get('/dados/poderes-concedidos');

// --- PERSONAGEM ---
export const fetchPersonagens = () => api.get('/personagens/');
export const fetchPersonagem = (id: string) => api.get(`/personagens/${id}`);
export const createPersonagem = (data: Personagem) => api.post('/personagens/', data);
export const updatePersonagem = (id: string, data: Partial<Personagem>) => api.put(`/personagens/${id}`, data);
export const deletePersonagem = (id: string) => api.delete(`/personagens/${id}`);

export default api;