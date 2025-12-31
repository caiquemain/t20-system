import React from 'react';
import type { Magia } from '../types';
import { getSchoolColor, getCircleColor, getTypeColor } from '../utils/magicUtils'; // <--- IMPORT

interface SpellDetailsModalProps {
    magia: Magia | null;
    onClose: () => void;
    onRemove: () => void;
}

export const SpellDetailsModal: React.FC<SpellDetailsModalProps> = ({ magia, onClose, onRemove }) => {
    if (!magia) return null;

    const typeColor = getTypeColor(magia.tipo);
    const schoolColor = getSchoolColor(magia.escola); // Cor da Escola
    const circleColor = getCircleColor(magia.circulo); // Cor do Círculo

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
                    {/* Tags Coloridas */}
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
                        <span style={{ background: `${typeColor}15`, color: typeColor, border: `1px solid ${typeColor}60`, padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                            {magia.tipo || 'Universal'}
                        </span>

                        {/* ESCOLA */}
                        <span style={{
                            background: `${schoolColor}15`, color: schoolColor, border: `1px solid ${schoolColor}50`,
                            padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase'
                        }}>
                            {magia.escola}
                        </span>

                        {/* CÍRCULO */}
                        <span style={{
                            color: circleColor, border: `1px solid ${circleColor}80`,
                            padding: '4px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold'
                        }}>
                            {magia.circulo}º Círculo
                        </span>

                        <span className="badge-pm">{magia.custo_pm} PM</span>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', background: '#1a1a1a', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #333' }}>
                        <DetailInfo label="Execução" value={magia.execucao} />
                        <DetailInfo label="Alcance" value={magia.alcance} />
                        <DetailInfo label="Alvo/Área" value={magia.alvo || magia.alvo_area || '-'} />
                        <DetailInfo label="Duração" value={magia.duracao} />
                        <DetailInfo label="Resistência" value={magia.resistencia || '-'} />
                    </div>

                    <div style={{ background: '#111', padding: '15px', borderRadius: '6px', color: '#ddd', lineHeight: '1.6', fontSize: '0.95rem', whiteSpace: 'pre-wrap', borderLeft: `2px solid ${typeColor}80` }}>
                        {magia.descricao}
                    </div>

                    {magia.aprimoramentos && magia.aprimoramentos.length > 0 && (
                        <div style={{ marginTop: '20px' }}>
                            <h4 style={{ color: '#aaa', fontSize: '0.85rem', textTransform: 'uppercase', borderBottom: '1px solid #333', paddingBottom: '5px', marginBottom: '10px' }}>Aprimoramentos</h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                {magia.aprimoramentos.map((ap, idx) => (
                                    <div key={idx} style={{ display: 'flex', gap: '10px', background: '#1a1a1a', padding: '8px', borderRadius: '4px', border: '1px solid #2a2a2a' }}>
                                        <div style={{ color: '#ce93d8', fontWeight: 'bold', fontSize: '0.85rem', whiteSpace: 'nowrap', minWidth: '50px' }}>{ap.custo}</div>
                                        <div style={{ color: '#ccc', fontSize: '0.9rem', lineHeight: '1.4' }}>{ap.descricao}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                <div className="modal-footer" style={{ justifyContent: 'space-between' }}>
                    <button className="btn-delete" onClick={() => { if (window.confirm(`Tem certeza que deseja esquecer a magia "${magia.nome}"?`)) { onRemove(); onClose(); } }}>🗑️ Esquecer Magia</button>
                    <button className="btn-cancel" onClick={onClose}>Fechar</button>
                </div>
            </div>
            <style>{`
                .badge-pm { background: rgba(156, 39, 176, 0.15); color: #ce93d8; padding: 4px 10px; borderRadius: 4px; fontSize: 0.8rem; fontWeight: bold; border: 1px solid rgba(156, 39, 176, 0.4); }
                .btn-delete { background: rgba(255, 82, 82, 0.1); color: #ff5252; border: 1px solid #ff5252; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
                .btn-delete:hover { background: #ff5252; color: white; }
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