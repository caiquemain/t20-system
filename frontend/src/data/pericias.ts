/**
 * Dados básicos de perícias para exibição no frontend
 * Este arquivo é necessário para o componente SkillList.tsx
 * 
 * Observação: Os dados completos vêm da API, mas este arquivo
 * fornece valores padrão para atributos e propriedades visuais
 */

export interface DadoPericia {
  atributo: string;
  treino_apenas?: boolean;
  penalidade_armadura?: boolean;
}

export const DADOS_PERICIAS_FRONTEND: Record<string, DadoPericia> = {
  // Perícias Básicas
  'Acrobacia': { atributo: 'des', penalidade_armadura: true },
  'Atletismo': { atributo: 'for', penalidade_armadura: true },
  'Cavalgar': { atributo: 'des', penalidade_armadura: true },
  'Conhecimento (Arcano)': { atributo: 'int' },
  'Conhecimento (História)': { atributo: 'int' },
  'Conhecimento (Mundo)': { atributo: 'int' },
  'Conhecimento (Natureza)': { atributo: 'int' },
  'Conhecimento (Religião)': { atributo: 'int' },
  'Cura': { atributo: 'sab' },
  'Diplomacia': { atributo: 'car' },
  'Enganação': { atributo: 'car' },
  'Furtividade': { atributo: 'des', penalidade_armadura: true },
  'Guerra': { atributo: 'int' },
  'Iniciativa': { atributo: 'des' },
  'Intimidação': { atributo: 'car' },
  'Intuição': { atributo: 'sab' },
  'Investigação': { atributo: 'int' },
  'Luta': { atributo: 'for' },
  'Notação': { atributo: 'sab' },
  'Ofício': { atributo: 'int' },
  'Percepção': { atributo: 'sab' },
  'Pontaria': { atributo: 'des' },
  'Reflexos': { atributo: 'des', penalidade_armadura: true },
  'Reconhecimento': { atributo: 'sab' },
  'Relacionamento': { atributo: 'car' },
  'Sobrevivência': { atributo: 'sab' },
  'Vontade': { atributo: 'sab' },
};

export default DADOS_PERICIAS_FRONTEND;
