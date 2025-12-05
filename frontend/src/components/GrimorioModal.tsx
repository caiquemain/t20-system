import React, { useState, useMemo } from 'react';
import '../Ficha.css';
import type { Magia } from '../types';

interface GrimorioModalProps {
    isOpen: boolean;
    onClose: () => void;
    onLearn: (novasMagias: Magia[]) => void;
    dadosMagias: Record<string, any>;
    magiasConhecidas: Magia[];
}

export const GrimorioModal: React.FC<GrimorioModalProps> = ({
    isOpen, onClose, onLearn, dadosMagias, magiasConhecidas
}) => {
    const [filtroTexto, setFiltroTexto] = useState('');
    const [filtroCirculo, setFiltroCirculo] = useState<number | 'Todos'>('Todos');
    const [filtroTipo, setFiltroTipo] = useState<string>('Todos');
    const [selecionadas, setSelecionadas] = useState<string[]>([]);
    const [expandedMagia, setExpandedMagia] = useState<string | null>(null);

    // Helper para extrair custo (Placeholder)
    const parseCusto = (_texto: string) => 1;

    if (!isOpen) return null;

    const listaMagias = useMemo(() => {
        return Object.values(dadosMagias || {});
    }, [dadosMagias]);

    const magiasFiltradas = listaMagias.filter((m: any) => {
        const matchTexto = m.nome.toLowerCase().includes(filtroTexto.toLowerCase());
        const matchCirculo = filtroCirculo === 'Todos' || m.circulo === filtroCirculo;
        const matchTipo = filtroTipo === 'Todos' || m.tipo === filtroTipo || m.tipo === 'Universal';
        return matchTexto && matchCirculo && matchTipo;
    });

    const toggleSelecao = (nome: string) => {
        if (selecionadas.includes(nome)) {
            setSelecionadas(prev => prev.filter(n => n !== nome));
        } else {
            setSelecionadas(prev => [...prev, nome]);
        }
    };

    const handleSalvar = () => {
        const novasObjetos: Magia[] = selecionadas.map(nome => {
            const dados = dadosMagias[nome];
            return {
                nome: dados.nome,
                circulo: dados.circulo,
                escola: dados.escola,
                custo_pm: parseCusto(dados.execucao) || 1,
                execucao: dados.execucao,
                alcance: dados.alcance,
                duracao: dados.duracao,
                resistencia: dados.resistencia || '-',
                descricao: dados.descricao
            };
        });
        onLearn(novasObjetos);
        setSelecionadas([]);
        onClose();
    };

    return (
        <div className="habilidades-panel-overlay">
            <div className="habilidades-panel-content grimorio-content">
                <div className="modal-header">
                    <h3>📖 Grimório Arcano & Divino</h3>
                    <button onClick={onClose} className="btn-close-panel">X</button>
                </div>

                <div className="grimorio-filters">
                    <input
                        type="text"
                        placeholder="Buscar magia..."
                        className="modal-search-input"
                        value={filtroTexto}
                        onChange={e => setFiltroTexto(e.target.value)}
                    />
                    <select
                        className="modal-category-select"
                        value={filtroCirculo}
                        onChange={e => setFiltroCirculo(e.target.value === 'Todos' ? 'Todos' : parseInt(e.target.value))}
                    >
                        <option value="Todos">Todos os Círculos</option>
                        <option value={1}>1º Círculo</option>
                        <option value={2}>2º Círculo</option>
                        <option value={3}>3º Círculo</option>
                        <option value={4}>4º Círculo</option>
                        <option value={5}>5º Círculo</option>
                    </select>
                    <select
                        className="modal-category-select"
                        value={filtroTipo}
                        onChange={e => setFiltroTipo(e.target.value)}
                    >
                        <option value="Todos">Arcana & Divina</option>
                        <option value="Arcana">Arcana</option>
                        <option value="Divina">Divina</option>
                        <option value="Universal">Universal</option>
                    </select>
                </div>

                <div className="grimorio-grid">
                    {magiasFiltradas.map((magia: any) => {
                        const jaConhecida = magiasConhecidas.some(m => m.nome === magia.nome);
                        const isSelected = selecionadas.includes(magia.nome);
                        const isExpanded = expandedMagia === magia.nome;

                        return (
                            <div
                                key={magia.nome}
                                className={`spell-card ${isSelected ? 'selected' : ''} ${jaConhecida ? 'known' : ''}`}
                                onClick={() => !jaConhecida && toggleSelecao(magia.nome)}
                            >
                                <div className="spell-header">
                                    <div className="spell-title-row">
                                        <span className="spell-circle">{magia.circulo}º</span>
                                        <span className="spell-name">{magia.nome}</span>
                                        {jaConhecida && <span className="tag-known">Aprendida</span>}
                                        {isSelected && <span className="check-icon">✅</span>}
                                    </div>
                                    <div className="spell-meta">
                                        <span className="spell-school">{magia.escola}</span>
                                        <span className="spell-type">{magia.tipo}</span>
                                    </div>
                                </div>

                                <button
                                    className="btn-details"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        setExpandedMagia(isExpanded ? null : magia.nome);
                                    }}
                                >
                                    {isExpanded ? 'Ocultar Detalhes' : 'Ver Detalhes'}
                                </button>

                                {isExpanded && (
                                    <div className="spell-details">
                                        <p><strong>Execução:</strong> {magia.execucao}</p>
                                        <p><strong>Alcance:</strong> {magia.alcance}</p>
                                        <p><strong>Duração:</strong> {magia.duracao}</p>
                                        <p><strong>Resistência:</strong> {magia.resistencia || '-'}</p>
                                        <p className="spell-desc">{magia.descricao}</p>
                                        {magia.aprimoramentos && (
                                            <div className="spell-upgrades">
                                                <strong>Aprimoramentos:</strong>
                                                <ul>
                                                    {magia.aprimoramentos.map((ap: any, idx: number) => (
                                                        <li key={idx}>
                                                            <span className="pm-cost">{ap.custo}:</span> {ap.descricao}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                <div className="modal-footer">
                    <span>{selecionadas.length} magia(s) selecionada(s)</span>
                    <button
                        className="btn-apply-changes"
                        onClick={handleSalvar}
                        disabled={selecionadas.length === 0}
                    >
                        Aprender Selecionadas
                    </button>
                </div>
            </div>
        </div>
    );
};