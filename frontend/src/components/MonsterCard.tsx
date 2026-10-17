import React from 'react';
import type { Ameaca } from '../types';

interface MonsterCardProps {
    ameaca: Ameaca;
}

export const MonsterCard: React.FC<MonsterCardProps> = ({ ameaca }) => {
    const enviarParaRoll20 = () => {
        if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
            chrome.runtime.sendMessage({ type: 'AMEACA_PARA_ROLL20', ameaca }, (response: any) => {
                if (response && response.ok) {
                    alert(`✅ ${ameaca.nome} enviado para o Roll20 com sucesso!`);
                } else {
                    alert(`❌ Erro ao enviar. Verifique se uma ficha do Roll20 está aberta.`);
                }
            });
        } else {
            alert('⚠️ Extensão T20 Bridge não detectada neste navegador.');
        }
    };

    return (
        <div className="char-card">
            <div className="char-header">
                <div>
                    <h2>{ameaca.nome}</h2>
                    <div className="char-subtitle">
                        {ameaca.tipo} {ameaca.subtipo ? `(${ameaca.subtipo})` : ''} • {ameaca.tamanho}
                    </div>
                </div>
                <div style={{ background: 'var(--accent-color)', color: 'white', padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold', fontSize: '0.85rem' }}>
                    ND {ameaca.nd}
                </div>
            </div>

            <div className="stats-row">
                <div className="stat-badge pv">PV: {ameaca.pontos_de_vida}</div>
                <div className="stat-badge def">Defesa: {ameaca.defesa}</div>
            </div>

            <div className="attributes-box">
                <strong>FOR</strong> {ameaca.atributos.forca ?? '—'} • <strong>DES</strong> {ameaca.atributos.destreza ?? '—'} • <strong>CON</strong> {ameaca.atributos.constituicao ?? '—'}<br />
                <strong>INT</strong> {ameaca.atributos.inteligencia ?? '—'} • <strong>SAB</strong> {ameaca.atributos.sabedoria ?? '—'} • <strong>CAR</strong> {ameaca.atributos.carisma ?? '—'}
            </div>

            <div className="char-footer" style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                <button 
                    onClick={enviarParaRoll20}
                    style={{ flex: 1, padding: '10px', background: '#9c27b0', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
                >
                    📤 Enviar pro Roll20
                </button>
            </div>
        </div>
    );
};
