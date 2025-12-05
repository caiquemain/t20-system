// src/services/api.ts
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Funções de ajuda para buscar dados
export const fetchRacas = () => api.get('/racas');
export const fetchClasses = () => api.get('/classes');
export const fetchOrigens = () => api.get('/origens');
export const fetchPericias = () => api.get('/pericias');
export const fetchPoderes = () => api.get('/poderes');
export const fetchDadosHabilidades = () => api.get('/dados/habilidades');

export const fetchDadosClasses = () => api.get('/dados/classes');
export const fetchDadosOrigens = () => api.get('/dados/origens');
export const fetchDadosRacas = () => api.get('/dados/racas');
export const fetchDadosHabilidadesClasse = () => api.get('/dados/habilidades-classe');
export const fetchDadosMagias = () => api.get('/dados/magias');

export const fetchPersonagem = (id: string) => api.get(`/personagens/${id}`);
export const updatePersonagem = (id: string, data: any) => api.put(`/personagens/${id}`, data);