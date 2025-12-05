import React from 'react';
import '../Ficha.css';

interface PowerListItemProps {
    item: any; // Objeto processado do seletor
    isBlocked: boolean;
    blockReason?: string[];
    onClick: () => void;
}

export const PowerListItem: React.FC<PowerListItemProps> = ({ item, isBlocked, blockReason, onClick }) => {

    // Tooltip content
    const tooltipText = isBlocked
        ? `BLOQUEADO:\n• ${blockReason?.join('\n• ')}`
        : item.descricao;

    return (
        <div
            className={`modal-list-item ${isBlocked ? 'blocked-item' : ''}`}
            onClick={() => !isBlocked && onClick()}
            title={tooltipText} // Tooltip nativo simples (ou pode usar o CSS customizado)
        >
            {/* Se estiver bloqueado, mostra um overlay visual ou ícone */}
            <div className="item-header">
                <div className="item-title-wrapper">
                    {isBlocked && <span className="lock-icon">🔒</span>}
                    <span className="item-name">{item.nome}</span>
                </div>
                <span className={`item-tag ${item.tagClass}`}>
                    {item.categoria}
                </span>
            </div>

            <div className="item-desc-container">
                {isBlocked ? (
                    <p className="item-req-error">
                        {blockReason?.[0]} {blockReason!.length > 1 && `(+${blockReason!.length - 1})`}
                    </p>
                ) : (
                    <p className="item-desc-small">{item.descricao}</p>
                )}
            </div>

            {/* Requisitos (sempre visíveis, mas destacados se falhar) */}
            {item.requisitos && item.requisitos.length > 0 && (
                <div className="item-reqs-list">
                    <small>Req: {item.requisitos.join(', ')}</small>
                </div>
            )}
        </div>
    );
};