import type { Personagem } from '../types';

export interface WizardStepProps {
    ficha: Personagem;
    updateFicha: (novosDados: Partial<Personagem>, salvarAgora?: boolean) => void;
    
    // Listas simples
    listaRacas: string[];
    listaClasses: string[];
    listaOrigens: string[];
    listaTodasPericias: string[];
    listaPoderes: any[];
    listaDeuses: string[];
    
    // Dados de regras
    dadosRacas: any;
    dadosClasses: any;
    dadosOrigens: any;
    dadosHabilidadesClasse: any;
    dadosMagias: any;
    dadosHabilidades: any;
    dadosDeuses: any;
    dadosPoderesConcedidos: any;
    dadosHabilidadesRaciais: any;
    
    // Funções de regra de negócio
    handleAtributoBaseChange: (key: string, valorStr: string) => void;
    montarHabilidadesParaPanel: () => void;
    handleSaveEscolhas: () => Promise<void>;
}