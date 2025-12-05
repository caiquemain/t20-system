import React from 'react';
import '../Ficha.css';

// Tabela de Custo para tooltip/dicas (Regra JdA)
const TABELA_CUSTO: Record<string, number> = {
    "-1": -1, "0": 0, "1": 1, "2": 2, "3": 4, "4": 7
};

interface AttributeCardProps {
    attrKey: string;      // ex: 'forca'
    valBase: number;      // Valor comprado
    valTotal: number;     // Valor final (Base + Racial + Outros)

    // Dados Raciais
    racialFixo: number;        // ex: +2 (Anão/Con) ou 0
    isRacialChosen: boolean;   // Se o checkbox está marcado (Humano)
    canChooseRacial: boolean;  // Se deve exibir o checkbox
    isRacialDisabled: boolean; // Se o checkbox deve estar travado (limite atingido)

    // Ações
    onBaseChange: (key: string, delta: number) => void;
    onToggleRacial: (key: string) => void;
}

export const AttributeCard: React.FC<AttributeCardProps> = ({
    attrKey, valBase, valTotal,
    racialFixo, isRacialChosen, canChooseRacial, isRacialDisabled,
    onBaseChange, onToggleRacial
}) => {

    // Labels
    const label = attrKey.substring(0, 3).toUpperCase();

    // Cálculos
    const racialTotal = racialFixo + (isRacialChosen ? 1 : 0);
    const outrosMods = valTotal - valBase - racialTotal;
    const custoProximo = TABELA_CUSTO[String(valBase + 1)];

    return (
        <div className="attr-box tooltip-container">
            {/* TOOLTIP DETALHADO (HOVER) */}
            <div className="attr-tooltip">
                <div className="tooltip-row">
                    <span>Base (Compra):</span> <span>{valBase}</span>
                </div>
                <div className="tooltip-row">
                    <span>Racial:</span>
                    <span>{racialTotal > 0 ? `+${racialTotal}` : racialTotal}</span>
                </div>
                {outrosMods !== 0 && (
                    <div className="tooltip-row">
                        <span>Outros (Item/Nível):</span>
                        <span>{outrosMods > 0 ? `+${outrosMods}` : outrosMods}</span>
                    </div>
                )}
                <div className="tooltip-row tooltip-total">
                    <span>Total:</span> <span>{valTotal}</span>
                </div>
            </div>

            {/* CABEÇALHO */}
            <div className="attr-header-row">
                <span className="attr-label">{label}</span>
            </div>

            {/* VALOR TOTAL (GRANDE) */}
            <div className="attr-total-container">
                <span className="attr-main-value">
                    {valTotal >= 0 ? `+${valTotal}` : valTotal}
                </span>
            </div>

            {/* CONTROLES DE BASE */}
            <div className="attr-controls-wrapper">
                <button
                    className="btn-attr"
                    onClick={() => onBaseChange(attrKey, -1)}
                    disabled={valBase <= -1} // Regra: Mínimo -1
                    title="Reduzir Base"
                >
                    -
                </button>

                <div className="attr-base-display">
                    <span className="attr-base-label">BASE</span>
                    <span className="attr-base-val">{valBase}</span>
                </div>

                <button
                    className="btn-attr"
                    onClick={() => onBaseChange(attrKey, 1)}
                    disabled={valBase >= 4} // Regra: Máximo 4 na compra inicial
                    title={valBase < 4 ? `Custo para +${valBase + 1}: ${custoProximo} pts` : "Máximo atingido"}
                >
                    +
                </button>
            </div>

            {/* ÁREA RACIAL (Checkbox ou Badge) */}
            <div style={{ minHeight: '24px', marginTop: '6px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>

                {/* CASO 1: Checkbox de Escolha (Humano, Lefou, etc) */}
                {canChooseRacial && (
                    <label style={{
                        fontSize: '0.7rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 4,
                        cursor: (!isRacialDisabled || isRacialChosen) ? 'pointer' : 'not-allowed',
                        color: isRacialChosen ? '#64b5f6' : '#666',
                        fontWeight: isRacialChosen ? 'bold' : 'normal'
                    }}>
                        <input
                            type="checkbox"
                            checked={isRacialChosen}
                            onChange={() => onToggleRacial(attrKey)}
                            disabled={isRacialDisabled && !isRacialChosen}
                            style={{ width: 12, height: 12, accentColor: '#2196f3', cursor: 'inherit' }}
                        />
                        +1 Racial
                    </label>
                )}

                {/* CASO 2: Badge Fixo (Anão, Elfo, etc) */}
                {!canChooseRacial && racialFixo !== 0 && (
                    <span className={`mod-badge ${racialFixo < 0 ? 'negativo' : ''}`} style={{
                        color: racialFixo < 0 ? '#ef5350' : '#61dafb',
                        borderColor: racialFixo < 0 ? '#ef5350' : '#3b5f70'
                    }}>
                        {racialFixo > 0 ? `+${racialFixo}` : racialFixo} Raça
                    </span>
                )}

            </div>
        </div>
    );
};