import React, { useState } from 'react';
import type { Personagem } from '../../types';
import { rolarDuendeSonhosMalucos } from '../../services/api';

interface Props {
    ficha: Personagem;
    onUpdate: (dados: Partial<Personagem>) => void;
    onClose: () => void;
}

export const DuendeHelperModal: React.FC<Props> = ({ ficha, onUpdate, onClose }) => {
    const [resultado, setResultado] = useState<any>(null);
    const [carregando, setCarregando] = useState(false);

    const handleRolar = async () => {
        setCarregando(true);
        try {
            const res = await rolarDuendeSonhosMalucos();
            setResultado(res.data);
        } finally {
            setCarregando(false);
        }
    };

    const handleAplicar = () => {
        if (!resultado) return;
        const novasHabs = (ficha.habilidades || []).map(h => {
            if (h.nome === 'Natureza') {
                return { ...h, escolhas_aplicadas: { ...(h.escolhas_aplicadas || {}), escolha: resultado.natureza } };
            }
            if (h.nome === 'Tamanho') {
                return { ...h, escolhas_aplicadas: { ...(h.escolhas_aplicadas || {}), escolha: resultado.tamanho } };
            }
            if (h.nome === 'Dons') {
                return { ...h, escolhas_aplicadas: { ...(h.escolhas_aplicadas || {}), escolha: resultado.dons } };
            }
            if (h.nome === 'Presentes de Magia e Caos') {
                return { ...h, escolhas_aplicadas: { ...(h.escolhas_aplicadas || {}), escolha: resultado.presentes } };
            }
            return h;
        });
        const conds = Array.from(new Set([...(ficha.condicoes_ativas || []), 'sonhos_malucos']));
        onUpdate({ habilidades: novasHabs, condicoes_ativas: conds });
        onClose();
    };

    return (
        <div
            onClick={onClose}
            style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: 16 }}
        >
            <div
                onClick={e => e.stopPropagation()}
                style={{ background: '#181820', border: '1px solid #ffd700', borderRadius: 8, maxWidth: 520, width: '100%', padding: 20, color: '#eee' }}
            >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <h3 style={{ margin: 0, color: '#ffd700' }}>✨ Duende — Sonhos Malucos</h3>
                    <button type="button" onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#aaa', fontSize: '1.1rem', cursor: 'pointer' }}>✕</button>
                </div>
                <p style={{ fontSize: '0.82rem', color: '#b0bec5', marginTop: 0 }}>
                    Rola automaticamente Natureza (1d3), Tamanho (1d4), Dons (2d6) e 3 Presentes de Magia e Caos (3d12) conforme <em>Heróis de Arton</em> (p. 9), concedendo <strong>+2 PM</strong>!
                </p>

                <button
                    type="button"
                    onClick={handleRolar}
                    disabled={carregando}
                    style={{ width: '100%', background: 'rgba(156,39,176,0.25)', border: '1px solid #ce93d8', color: '#f3e5f5', padding: '10px 14px', borderRadius: 6, fontWeight: 'bold', cursor: 'pointer', marginBottom: 14 }}
                >
                    {carregando ? 'Rolando...' : '🎲 Rolar Sonhos Malucos'}
                </button>

                {resultado && (
                    <div style={{ background: '#121218', border: '1px solid #333', borderRadius: 6, padding: 12, fontSize: '0.84rem', marginBottom: 14 }}>
                        <div><strong style={{ color: '#ffd700' }}>Natureza:</strong> {resultado.natureza}</div>
                        <div><strong style={{ color: '#ffd700' }}>Tamanho:</strong> {resultado.tamanho}</div>
                        <div><strong style={{ color: '#ffd700' }}>Dons:</strong> {(resultado.dons || []).join(', ')}</div>
                        <div><strong style={{ color: '#ffd700' }}>Presentes:</strong> {(resultado.presentes || []).join(', ')}</div>
                        <div style={{ marginTop: 6, color: '#81c784' }}><strong>Bônus:</strong> +2 PM (Sonhos Malucos)</div>
                    </div>
                )}

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
                    <button type="button" onClick={onClose} style={{ background: 'transparent', border: '1px solid #555', color: '#ccc', borderRadius: 4, padding: '6px 12px', cursor: 'pointer' }}>
                        Fechar
                    </button>
                    {resultado && (
                        <button type="button" onClick={handleAplicar} style={{ background: '#ffd700', color: '#111', border: 'none', borderRadius: 4, padding: '6px 14px', fontWeight: 'bold', cursor: 'pointer' }}>
                            Aplicar na Ficha
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};
