// Regras de compra de atributos do Tormenta 20 (Jogo do Ano)
// Centralizadas aqui para uso na Ficha e no Wizard

export const PONTOS_INICIAIS = 10;
export const MIN_ATTR = -1;
export const MAX_ATTR = 4;

// Custo em pontos para cada valor de atributo base
export const TABELA_CUSTO: Record<string, number> = {
    "-1": -1,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 4,
    "4": 7
};

// Mapeia nome completo do atributo -> chave curta usada nos dados de raça
export const MAPA_ATTR_KEY: Record<string, string> = {
    forca: 'for',
    destreza: 'des',
    constituicao: 'con',
    inteligencia: 'int',
    sabedoria: 'sab',
    carisma: 'car'
};
