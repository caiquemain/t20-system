import type { Personagem } from '../types';
import { API_URL, IS_LOCAL_STORAGE } from '../services/api';

async function baixarFichaFormato(
  ficha: Personagem,
  formato: 'pdf' | 'odg' | 'odt' | 'xlsx',
  idDaUrl?: string,
): Promise<void> {
  const label = formato.toUpperCase();
  try {
    let response: Response;
    if (IS_LOCAL_STORAGE) {
      response = await fetch(`${API_URL}/personagens/exportar/${formato}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ficha),
      });
    } else {
      const id = idDaUrl || ficha._id;
      if (!id) {
        throw new Error("Ficha sem ID. Salve a ficha primeiro.");
      }
      response = await fetch(`${API_URL}/personagens/${id}/${formato}`, {
        method: 'GET',
      });
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    const prefix = formato === 'xlsx' ? 'ficha-auditoria' : 'ficha';
    link.download = `${prefix}-${ficha.cabecalho.nome || 'personagem'}.${formato}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(`Erro ao gerar ${label}:`, error);
    alert(`Erro ao gerar o ${label}: ` + (error as Error).message);
  }
}

export async function gerarPDF(ficha: Personagem, idDaUrl?: string): Promise<void> {
  return baixarFichaFormato(ficha, 'pdf', idDaUrl);
}

export async function gerarODG(ficha: Personagem, idDaUrl?: string): Promise<void> {
  return baixarFichaFormato(ficha, 'odg', idDaUrl);
}

export async function gerarODT(ficha: Personagem, idDaUrl?: string): Promise<void> {
  return baixarFichaFormato(ficha, 'odt', idDaUrl);
}

export async function gerarXLSX(ficha: Personagem, idDaUrl?: string): Promise<void> {
  return baixarFichaFormato(ficha, 'xlsx', idDaUrl);
}
