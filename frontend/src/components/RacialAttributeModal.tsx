import React from 'react';
import '../Ficha.css';

interface RacialAttributeModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    racaNome: string;
    qtdEscolhas: number;
    escolhasAtuais: string[];
    onToggle: (key: string) => void;
    atributos: Record<string, number>; // Apenas para pegar as chaves (forca, destreza...)
    infoRacaAtual: { attrs: Record<string, number> };
}

const MAPA_ATTR_KEY: Record<string, string> = {
    'forca': 'for', 'destreza': 'des', 'constituicao': 'con',
    'inteligencia': 'int', 'sabedoria': 'sab', 'carisma': 'car'
};

export const RacialAttributeModal: React.FC<RacialAttributeModalProps> = ({
    isOpen, onClose, onConfirm,
    racaNome, qtdEscolhas, escolhasAtuais, onToggle,
    atributos, infoRacaAtual
}) => {
    if (!isOpen) return null;

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content" style={{ maxWidth: '500px' }}>
                <div className="modal-header">
                    <h3>🧬 Bônus Racial: {racaNome}</h3>
                    <button className="btn-close-panel" onClick={onClose}>X</button>
                </div>
                <hr />

                <p style={{ color: '#ccc', margin: '15px 0' }}>
                    Escolha <strong>{qtdEscolhas}</strong> atributos diferentes para receber +1.
                </p>

                <div className="racial-selector-grid">
                    {Object.keys(atributos).map((key) => {
                        const label = key.charAt(0).toUpperCase() + key.slice(1);
                        const shortKey = MAPA_ATTR_KEY[key];

                        // Verifica se já tem bônus fixo (impedindo seleção)
                        const valorFixo = infoRacaAtual.attrs?.[shortKey] || 0;
                        const isSelected = escolhasAtuais.includes(key);

                        // Desabilita se tiver fixo OU se atingiu limite (e não é este o selecionado)
                        const isDisabled = valorFixo !== 0 || (!isSelected && escolhasAtuais.length >= qtdEscolhas);

                        return (
                            <div
                                key={key}
                                className={`racial-option ${isSelected ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}`}
                                onClick={() => !isDisabled && onToggle(key)}
                            >
                                <div>
                                    <span style={{ fontWeight: 'bold' }}>{label}</span>
                                    {valorFixo !== 0 && (
                                        <span style={{ fontSize: '0.7rem', display: 'block', color: valorFixo > 0 ? '#66bb6a' : '#ef5350' }}>
                                            Fixo: {valorFixo > 0 ? `+${valorFixo}` : valorFixo}
                                        </span>
                                    )}
                                </div>
                                <div className="check-circle">{isSelected && "✓"}</div>
                            </div>
                        );
                    })}
                </div>

                <div style={{ marginTop: 20, textAlign: 'right', borderTop: '1px solid #333', paddingTop: 15 }}>
                    <button
                        className="btn-apply-changes"
                        onClick={onConfirm}
                        disabled={escolhasAtuais.length !== qtdEscolhas}
                        style={{ width: 'auto' }}
                    >
                        Confirmar Escolhas
                    </button>
                </div>
            </div>
        </div>
    );
};