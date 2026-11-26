import type { Personagem } from '../types';

async function baixarFichaFormato(
  ficha: Personagem,
  formato: 'pdf' | 'odg',
  idDaUrl?: string,
): Promise<void> {
  const label = formato.toUpperCase();
  try {
    const id = idDaUrl || ficha._id;

    if (!id) {
      throw new Error("Ficha sem ID. Salve a ficha primeiro.");
    }

    const response = await fetch(`http://localhost:8000/personagens/${id}/${formato}`, {
      method: 'GET',
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ficha-${ficha.cabecalho.nome || 'personagem'}.${formato}`;
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
