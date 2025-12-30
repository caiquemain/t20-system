import React from 'react';
import type { Magia } from '../types';

interface SpellDetailsModalProps {
    magia: Magia | null;
    onClose: () => void;
    onRemove: () => void; // <--- Nova propriedade para deletar
}

// Função auxiliar de cor (Universal agora é Vermelho)
const getTypeColor = (tipo?: string) => {
    if (!tipo) return '#ff5252'; // Padrão/Universal agora é Vermelho
    const t = tipo.toLowerCase();

    if (t.includes('arcana')) return '#d236d2'; // Roxo/Magenta
    if (t.includes('divina')) return '#ffc107'; // Dourado/Amarelo

    return '#ff5252'; // Vermelho (Universal)
};

export const SpellDetailsModal: React.FC<SpellDetailsModalProps> = ({ magia, onClose, onRemove }) => {
    if (!magia) return null;

    const typeColor = getTypeColor(magia.tipo);

    return (
        <div className="modal-overlay" style={{ zIndex: 3000 }}>
            <div className="modal-content" style={{ maxWidth: '500px', borderTop: `4px solid ${typeColor}` }}>

                <div className="modal-header">
                    <h3 style={{ fontSize: '1.4rem', color: '#fff', margin: 0 }}>
                        {magia.nome}
                    </h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="modal-body">
                    {/* Tags */}
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
                        <span style={{
                            background: `${typeColor}15`, color: typeColor, border: `1px solid ${typeColor}60`,
                            padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase'
                        }}>
                            {magia.tipo || 'Universal'}
                        </span>
                        <span className="badge-info">{magia.escola}</span>
                        <span className="badge-info">{magia.circulo}º Círculo</span>
                        <span className="badge-pm">{magia.custo_pm} PM</span>
                    </div>

                    {/* Grid de Stats */}
                    <div style={{
                        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px',
                        background: '#1a1a1a', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #333'
                    }}>
                        <DetailInfo label="Execução" value={magia.execucao} />
                        <DetailInfo label="Alcance" value={magia.alcance} />
                        <DetailInfo label="Alvo/Área" value={magia.alvo || magia.alvo_area || '-'} />
                        <DetailInfo label="Duração" value={magia.duracao} />
                        <DetailInfo label="Resistência" value={magia.resistencia || '-'} />
                    </div>

                    {/* Descrição */}
                    <div style={{
                        background: '#111', padding: '15px', borderRadius: '6px', color: '#ddd',
                        lineHeight: '1.6', fontSize: '0.95rem', whiteSpace: 'pre-wrap', borderLeft: `2px solid ${typeColor}80`
                    }}>
                        {magia.descricao}
                    </div>
                </div>

                {/* Rodapé com Botão DELETAR */}
                <div className="modal-footer" style={{ justifyContent: 'space-between' }}>
                    <button
                        className="btn-delete"
                        onClick={() => {
                            if (window.confirm(`Tem certeza que deseja esquecer a magia "${magia.nome}"?`)) {
                                onRemove();
                                onClose();
                            }
                        }}
                    >
                        🗑️ Esquecer Magia
                    </button>
                    <button className="btn-cancel" onClick={onClose}>
                        Fechar
                    </button>
                </div>
            </div>

            <style>{`
                .badge-info { background: #333; color: #ccc; padding: 4px 10px; borderRadius: 4px; fontSize: 0.8rem; textTransform: uppercase; fontWeight: bold; border: 1px solid #444; }
                .badge-pm { background: rgba(156, 39, 176, 0.15); color: #ce93d8; padding: 4px 10px; borderRadius: 4px; fontSize: 0.8rem; fontWeight: bold; border: 1px solid rgba(156, 39, 176, 0.4); }
                
                .btn-delete {
                    background: rgba(255, 82, 82, 0.1);
                    color: #ff5252;
                    border: 1px solid #ff5252;
                    padding: 8px 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    transition: all 0.2s;
                }
                .btn-delete:hover {
                    background: #ff5252;
                    color: white;
                }
            `}</style>
        </div>
    );
};

const DetailInfo = ({ label, value }: { label: string, value: string }) => (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span style={{ fontSize: '0.75rem', color: '#888', textTransform: 'uppercase', marginBottom: '3px', fontWeight: '600' }}>{label}</span>
        <span style={{ fontSize: '0.9rem', color: '#fff', fontWeight: '500' }}>{value}</span>
    </div>
);