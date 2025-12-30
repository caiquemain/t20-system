import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchPersonagens, createPersonagem, deletePersonagem } from '../services/api';
import '../Ficha.css'; // Reutilizando estilos ou crie um Home.css

// Definição simplificada para a lista
interface PersonagemResumo {
    _id: string;
    cabecalho: {
        nome: string;
        raca: string;
        classe: string; // ou classes[0].nome se for complexo
        nivel_total: number;
    };
}

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

    const handleNovoPersonagem = async () => {
        // Objeto mínimo para criar ficha (o backend preenche o resto)
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
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
                <h1 style={{ color: '#ffd700', margin: 0 }}>Grimório T20</h1>
                <button className="btn-action" onClick={handleNovoPersonagem} style={{ fontSize: '1rem', padding: '10px 20px' }}>
                    + Novo Personagem
                </button>
            </div>

            {loading ? (
                <div className="loading-screen">Carregando fichas...</div>
            ) : (
                <div className="char-list" style={{ display: 'grid', gap: '15px' }}>
                    {personagens.map((p) => {
                        // Tratamento seguro para exibir classes
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
                        );
                    })}

                    {personagens.length === 0 && (
                        <p style={{ textAlign: 'center', color: '#666', marginTop: 20 }}>
                            Nenhum personagem encontrado. Crie o primeiro!
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Home;