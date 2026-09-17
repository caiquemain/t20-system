import type { Personagem } from '../types';

export async function gerarPDF(ficha: Personagem, idDaUrl?: string): Promise<void> {
  try {
    // Pega o ID da URL (useParams) ou do objeto ficha
    const id = idDaUrl || ficha.id;
    
    if (!id) {
      throw new Error("Ficha sem ID. Salve a ficha primeiro.");
    }
    
    console.log('📄 Gerando PDF para ficha ID:', id);
    
    // Chama o endpoint do backend
    const response = await fetch(`http://localhost:8000/personagens/${id}/pdf`, {
      method: 'GET',
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro ${response.status}: ${errorText}`);
    }
    
    // Faz download do blob
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ficha-${ficha.cabecalho.nome || 'personagem'}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    console.log('✅ PDF baixado com sucesso!');
  } catch (error) {
    console.error(" Erro ao gerar PDF:", error);
    alert("Erro ao gerar o PDF: " + (error as Error).message);
  }
}
