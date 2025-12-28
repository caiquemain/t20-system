import React from 'react';

interface PowerListItemProps {
    item: any;
    isBlocked?: boolean;
    blockReason?: string[];
    onClick: () => void;
}

export const PowerListItem: React.FC<PowerListItemProps> = ({ item, isBlocked, blockReason, onClick }) => {

    // Tratamento de classes para os Badges
    let badgeClass = "power-badge"; // Classe base
    if (item.tagClass) badgeClass += ` ${item.tagClass}`;

    return (
        <button
            className={`power-list-item ${isBlocked ? 'blocked' : ''}`}
            onClick={!isBlocked ? onClick : undefined}
            disabled={isBlocked}
        // IMPORTANTE: Removemos o atributo 'title' aqui para não aparecer a tooltip preta do navegador
        >
            <div className="power-header">
                <span className="power-name">{item.nome}</span>

                {/* Badge de Categoria (Arcana/Divina/Geral) */}
                {item.categoria && (
                    <span className={badgeClass}>
                        {item.categoria}
                    </span>
                )}
            </div>

            <p className="power-desc">
                {item.descricao}
            </p>

            {/* Mensagem de Bloqueio (Requisitos) */}
            {isBlocked && blockReason && blockReason.length > 0 && (
                <div className="power-block-reason">
                    🛑 {blockReason.join(', ')}
                </div>
            )}
        </button>
    );
};