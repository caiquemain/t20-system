import React from 'react';
import { SpellList } from './SpellList'; // Reutiliza o componente detalhado
import type { Magia } from '../types';

interface FullGrimorioModalProps {
    isOpen: boolean;
    onClose: () => void;
    magias: Magia[];
    onRemove: (nome: string) => void;
    pmAtual: number;
    pmMaximo: number;
}

export const FullGrimorioModal: React.FC<FullGrimorioModalProps> = ({
    isOpen, onClose, magias, onRemove, pmAtual, pmMaximo
}) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" style={{ zIndex: 2000 }}>
            <div className="modal-content large" style={{ maxHeight: '85vh', display: 'flex', flexDirection: 'column' }}>
                <div className="modal-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <h3>📖 Grimório Completo</h3>
                        <span style={{ fontSize: '0.9rem', color: '#aaa', background: '#111', padding: '2px 8px', borderRadius: '4px', border: '1px solid #333' }}>
                            PM: <strong style={{ color: '#ce93d8' }}>{pmAtual}</strong> / {pmMaximo}
                        </span>
                    </div>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="modal-body" style={{ overflowY: 'auto', paddingRight: '5px' }}>
                    <SpellList magias={magias} onRemove={onRemove} />
                </div>

                <div className="modal-footer">
                    <button className="btn-cancel" onClick={onClose}>Fechar</button>
                </div>
            </div>
        </div>
    );
};