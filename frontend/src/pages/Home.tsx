import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchPersonagens, createPersonagem, deletePersonagem } from '../services/api';
import '../Ficha.css';

const Home = () => {
    const navigate = useNavigate();
    const [personagens, setPersonagens] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const carregarPersonagens = async () => {
        try {
            const res = await fetchPersonagens();
            setPersonagens(res.data);
        } catch (error) {
            console.error("Erro ao listar personagens", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        carregarPersonagens();
    }, []);

    // Criação rápida (método antigo)
    const handleNovoPersonagem = async () => {
        const novaFicha = {
            cabecalho: { nome: "Novo Aventureiro", raca: "Humano", origem: "Acólito", nivel_total: 1 },
            classes: [{ nome: "Guerreiro", nivel: 1 }],
            atributos_base: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 }
        };
        try {
            // @ts-ignore
            const res = await createPersonagem(novaFicha);
            navigate(`/ficha/${res.data._id}`);
        } catch (error) {
            console.error("Erro ao criar", error);
            alert("Erro ao criar personagem.");
        }
    };

    const handleDeletar = async (e: React.MouseEvent, id: string) => {
        e.stopPropagation();
        if (confirm("Tem certeza que deseja apagar esta ficha?")) {
            await deletePersonagem(id);
            carregarPersonagens();
        }
    };

    return (
        <div className="ficha-container" style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '40px' }}>
            {/* Header com criação rápida */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
                <h1 style={{ color: '#ffd700', margin: 0 }}>Grimório T20</h1>
                <button className="btn-action" onClick={handleNovoPersonagem} style={{ fontSize: '1rem', padding: '10px 20px' }}>
                    + Novo Personagem (Rápido)
                </button>
            </div>

            {/* Card de destaque do Wizard */}
            <div
                onClick={() => navigate('/wizard')}
                style={{
                    background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
                    border: '2px solid #ffd700',
                    borderRadius: '12px',
                    padding: '25px',
                    marginBottom: '30px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '20px',
                    transition: 'all 0.3s ease',
                    boxShadow: '0 4px 20px rgba(255, 215, 0, 0.2)'
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-3px)';
                    e.currentTarget.style.boxShadow = '0 8px 30px rgba(255, 215, 0, 0.4)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 4px 20px rgba(255, 215, 0, 0.2)';
                }}
            >
                <div style={{
                    fontSize: '3rem',
                    background: 'rgba(255, 215, 0, 0.1)',
                    borderRadius: '12px',
                    width: '70px',
                    height: '70px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                }}>
                    🧙‍♂️
                </div>
                <div style={{ flex: 1 }}>
                    <h2 style={{ color: '#ffd700', margin: '0 0 5px 0', fontSize: '1.4rem' }}>
                        Criar Novo Personagem
                    </h2>
                    <p style={{ color: '#aaa', margin: 0, fontSize: '0.95rem' }}>
                        Wizard passo a passo guiado, com transparência total dos bônus
                    </p>
                </div>
                <div style={{ color: '#ffd700', fontSize: '2rem' }}>→</div>
            </div>

            {/* Lista de personagens */}
            <h2 style={{ color: '#ccc', marginBottom: '15px', fontSize: '1.1rem', borderBottom: '1px solid #333', paddingBottom: '10px' }}>
                📚 Meus Personagens
            </h2>

            {loading ? (
                <div className="loading-screen">Carregando fichas...</div>
            ) : (
                <div className="char-list" style={{ display: 'grid', gap: '15px' }}>
                    {personagens.map((p) => {
                        const classeDisplay = p.classes && p.classes.length > 0
                            ? `${p.classes[0].nome} ${p.classes[0].nivel}`
                            : 'Nível 1';

                        return (
                            <div
                                key={p._id}
                                onClick={() => navigate(`/ficha/${p._id}`)}
                                style={{
                                    background: '#252525',
                                    padding: '20px',
                                    borderRadius: '8px',
                                    border: '1px solid #333',
                                    cursor: 'pointer',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    transition: 'transform 0.2s'
                                }}
                                onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.01)'}
                                onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                            >
                                <div>
                                    <h3 style={{ margin: '0 0 5px 0', color: '#e0e0e0' }}>
                                        {p.cabecalho?.nome || "Sem Nome"}
                                    </h3>
                                    <span style={{ color: '#888', fontSize: '0.9rem' }}>
                                        {p.cabecalho?.raca} • {classeDisplay}
                                    </span>
                                </div>
                                <div style={{ display: 'flex', gap: '10px' }}>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            navigate(`/wizard/${p._id}`);
                                        }}
                                        title="Editar no Wizard"
                                        style={{
                                            background: 'transparent',
                                            border: '1px solid #ffd700',
                                            color: '#ffd700',
                                            padding: '5px 10px',
                                            borderRadius: '4px',
                                            cursor: 'pointer',
                                            fontSize: '0.85rem'
                                        }}
                                    >
                                        🧙‍♂️
                                    </button>
                                    <button
                                        onClick={(e) => handleDeletar(e, p._id)}
                                        style={{
                                            background: 'transparent',
                                            border: '1px solid #d32f2f',
                                            color: '#d32f2f',
                                            padding: '5px 10px',
                                            borderRadius: '4px',
                                            cursor: 'pointer'
                                        }}
                                    >
                                        Excluir
                                    </button>
                                </div>
                            </div>
                        );
                    })}

                    {personagens.length === 0 && (
                        <p style={{ textAlign: 'center', color: '#666', marginTop: 20 }}>
                            Nenhum personagem encontrado. Crie o primeiro usando o Wizard acima!
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Home;