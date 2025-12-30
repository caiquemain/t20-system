import React, { useState, useMemo } from 'react';

interface GrimorioModalProps {
    isOpen: boolean;
    onClose: () => void;
    dadosMagias: any; // Dicionário completo das magias
    magiasConhecidas: any[]; // Lista das magias que o personagem já tem
    onLearn: (magias: any[]) => void; // Função para salvar
}

export const GrimorioModal: React.FC<GrimorioModalProps> = ({
    isOpen,
    onClose,
    dadosMagias,
    magiasConhecidas = [],
    onLearn
}) => {
    // --- HOOKS (Sempre no topo, incondicionalmente) ---
    const [filtroTexto, setFiltroTexto] = useState("");
    const [filtroCirculo, setFiltroCirculo] = useState<number>(1);
    const [selecionadas, setSelecionadas] = useState<any[]>([]);

    // Converte o Dicionário em Lista e Ordena
    const listaTodas = useMemo(() => {
        return Object.values(dadosMagias || {}).sort((a: any, b: any) => a.nome.localeCompare(b.nome));
    }, [dadosMagias]);

    // --- LÓGICA (Executa mesmo com modal fechado para manter consistência) ---

    // Filtra conforme busca e círculo
    const magiasFiltradas = listaTodas.filter((m: any) => {
        const matchTexto = m.nome.toLowerCase().includes(filtroTexto.toLowerCase());
        const matchCirculo = m.circulo === filtroCirculo;
        return matchTexto && matchCirculo;
    });

    // Verifica se a magia já está na ficha
    const isAprendida = (nomeMagia: string) => {
        return magiasConhecidas.some((m: any) => m.nome === nomeMagia);
    };

    // Verifica se a magia está na lista de seleção atual
    const isSelecionada = (nomeMagia: string) => {
        return selecionadas.some((m: any) => m.nome === nomeMagia);
    };

    const toggleSelecao = (magia: any) => {
        if (isAprendida(magia.nome)) return;

        if (isSelecionada(magia.nome)) {
            setSelecionadas(prev => prev.filter(m => m.nome !== magia.nome));
        } else {
            setSelecionadas(prev => [...prev, magia]);
        }
    };

    const handleConfirmar = () => {
        onLearn(selecionadas);
        setSelecionadas([]);
        onClose();
    };

    // --- RENDERIZAÇÃO CONDICIONAL (Sempre por último) ---
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.85)', zIndex: 1000,
            display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
            <div className="modal-content" style={{
                background: '#1e1e1e', width: '90%', maxWidth: '800px', height: '85vh',
                borderRadius: '8px', display: 'flex', flexDirection: 'column',
                boxShadow: '0 0 20px rgba(0,0,0,0.5)', border: '1px solid #333'
            }}>

                {/* --- HEADER --- */}
                <div style={{ padding: '15px 20px', borderBottom: '1px solid #333', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#252525' }}>
                    <h2 style={{ margin: 0, color: '#e0e0e0', fontSize: '1.2rem' }}>📖 Grimório Arcano</h2>
                    <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#888', fontSize: '1.2rem', cursor: 'pointer' }}>✕</button>
                </div>

                {/* --- FILTROS --- */}
                <div style={{ padding: '15px 20px', background: '#2a2a2a', display: 'flex', gap: '15px', flexWrap: 'wrap', alignItems: 'center' }}>
                    <input
                        type="text"
                        placeholder="Buscar magia..."
                        value={filtroTexto}
                        onChange={e => setFiltroTexto(e.target.value)}
                        style={{
                            padding: '8px 12px', borderRadius: '4px', border: '1px solid #444',
                            background: '#1a1a1a', color: '#fff', flex: 1, minWidth: '200px'
                        }}
                    />

                    <div style={{ display: 'flex', gap: '5px' }}>
                        {[1, 2, 3, 4, 5].map(c => (
                            <button
                                key={c}
                                onClick={() => setFiltroCirculo(c)}
                                style={{
                                    padding: '6px 14px', borderRadius: '4px', border: '1px solid #444', cursor: 'pointer',
                                    background: filtroCirculo === c ? '#9c27b0' : '#333',
                                    color: filtroCirculo === c ? '#fff' : '#aaa',
                                    fontWeight: 'bold'
                                }}
                            >
                                {c}º
                            </button>
                        ))}
                    </div>
                </div>

                {/* --- LISTA DE MAGIAS --- */}
                <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '15px', alignContent: 'start' }}>
                    {magiasFiltradas.length === 0 ? (
                        <p style={{ color: '#666', gridColumn: '1/-1', textAlign: 'center', marginTop: 20 }}>Nenhuma magia encontrada neste círculo.</p>
                    ) : (
                        magiasFiltradas.map((magia: any) => {
                            const jaTem = isAprendida(magia.nome);
                            const selecionada = isSelecionada(magia.nome);

                            return (
                                <div
                                    key={magia.nome}
                                    onClick={() => toggleSelecao(magia)}
                                    style={{
                                        border: jaTem ? '1px solid #444' : (selecionada ? '1px solid #9c27b0' : '1px solid #333'),
                                        background: jaTem ? '#1a1a1a' : (selecionada ? 'rgba(156, 39, 176, 0.1)' : '#252525'),
                                        borderRadius: '6px', padding: '12px',
                                        opacity: jaTem ? 0.6 : 1,
                                        cursor: jaTem ? 'default' : 'pointer',
                                        position: 'relative', transition: 'all 0.2s'
                                    }}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '5px' }}>
                                        <h4 style={{ margin: 0, color: jaTem ? '#888' : (selecionada ? '#e040fb' : '#e0e0e0'), fontSize: '1rem' }}>
                                            {magia.nome}
                                        </h4>
                                        <span style={{ fontSize: '0.75rem', background: '#333', padding: '2px 6px', borderRadius: '4px', color: '#ccc' }}>
                                            {magia.escola || "Universal"}
                                        </span>
                                    </div>

                                    <div style={{ fontSize: '0.8rem', color: '#aaa', marginBottom: '8px', display: 'flex', gap: '10px' }}>
                                        <span>⚡ {magia.custo_pm} PM</span>
                                        <span>⏱ {magia.execucao}</span>
                                        <span>🎯 {magia.alcance}</span>
                                    </div>

                                    <p style={{ fontSize: '0.8rem', color: '#777', margin: 0, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                        {magia.descricao}
                                    </p>

                                    {/* STATUS BADGE */}
                                    {jaTem && (
                                        <div style={{ position: 'absolute', top: 10, right: 10, background: '#4caf50', color: 'black', fontSize: '0.7rem', fontWeight: 'bold', padding: '2px 6px', borderRadius: '4px' }}>
                                            APRENDIDA
                                        </div>
                                    )}
                                    {selecionada && (
                                        <div style={{ position: 'absolute', bottom: 10, right: 10, background: '#9c27b0', color: 'white', fontSize: '1.2rem', lineHeight: '10px', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                            ✓
                                        </div>
                                    )}
                                </div>
                            );
                        })
                    )}
                </div>

                {/* --- FOOTER --- */}
                <div style={{ padding: '15px 20px', borderTop: '1px solid #333', background: '#252525', display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '15px' }}>
                    <div style={{ color: '#aaa', fontSize: '0.9rem' }}>
                        {selecionadas.length} magias selecionadas
                    </div>
                    <button
                        onClick={onClose}
                        style={{ padding: '10px 20px', background: 'transparent', border: '1px solid #555', color: '#ccc', borderRadius: '4px', cursor: 'pointer' }}
                    >
                        Cancelar
                    </button>
                    <button
                        onClick={handleConfirmar}
                        disabled={selecionadas.length === 0}
                        style={{
                            padding: '10px 25px', borderRadius: '4px', border: 'none', cursor: 'pointer', fontWeight: 'bold',
                            background: selecionadas.length > 0 ? '#9c27b0' : '#444',
                            color: selecionadas.length > 0 ? '#fff' : '#888'
                        }}
                    >
                        Aprender Magias
                    </button>
                </div>

            </div>
        </div>
    );
};