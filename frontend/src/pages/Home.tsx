import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api'; // Usando o serviço centralizado
import type { Personagem } from '../types';
import './Home.css';

// Objeto padrão para criar um novo personagem
const NOVO_PERSONAGEM_TEMPLATE: Partial<Personagem> = {
    usuario_id: "guest",
    cabecalho: {
        nome: "Novo Aventureiro",
        jogador: "",
        raca: "Humano",
        origem: "Amnésico",
        nivel_total: 1,
        xp: { atual: 0, proximo_nivel: 1000 }
    },
    classes: [{ nome: "Guerreiro", nivel: 1, primaria: true }],
    atributos_base: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 },
    atributos: { forca: 0, destreza: 0, constituicao: 0, inteligencia: 0, sabedoria: 0, carisma: 0 },
    status: {
        pv: { atual: 20, maximo: 20, temporario: 0 },
        pm: { atual: 3, maximo: 3, temporario: 0 },
        defesa: { total: 10, detalhes: { base: 10, des_mod: 0, armadura: 0, escudo: 0, outros: 0 } },
        rd: [],
        deslocamento: 9
    },
    pericias: {},
    proficiencias: [],
    habilidades: [],
    inventario: { dinheiro: { tl: 0, tp: 0, to: 0 }, equipamentos: [], carga_total: 0, carga_maxima: 10 },
    combate: { ataques: [], magias: [], cd_magias: 10, bba: 0, iniciativa: 0 }
};

function Home() {
    const navigate = useNavigate();
    const [personagens, setPersonagens] = useState<Personagem[]>([]);
    const [loading, setLoading] = useState(true);

    // Carregar lista ao montar
    useEffect(() => {
        carregarPersonagens();
    }, []);

    const carregarPersonagens = async () => {
        try {
            setLoading(true);
            const response = await api.get('/personagens/');
            setPersonagens(response.data);
        } catch (error) {
            console.error("Erro ao carregar personagens:", error);
            alert("Não foi possível carregar a lista de personagens.");
        } finally {
            setLoading(false);
        }
    };

    const handleCriarNovo = async () => {
        try {
            const response = await api.post('/personagens/', NOVO_PERSONAGEM_TEMPLATE);
            const novoId = response.data._id;
            navigate(`/ficha/${novoId}`);
        } catch (error) {
            console.error("Erro ao criar personagem:", error);
            alert("Erro ao criar novo personagem.");
        }
    };

    const handleExcluir = async (e: React.MouseEvent, id?: string) => {
        e.stopPropagation(); // Evita abrir a ficha ao clicar no botão de excluir
        if (!id) return;

        if (window.confirm("Tem certeza que deseja excluir este personagem? Esta ação é irreversível.")) {
            try {
                await api.delete(`/personagens/${id}`);
                // Atualiza a lista localmente
                setPersonagens(prev => prev.filter(p => p._id !== id));
            } catch (error) {
                console.error("Erro ao excluir:", error);
                alert("Erro ao excluir personagem.");
            }
        }
    };

    if (loading) {
        return (
            <div className="home-container loading-state">
                <div className="spinner"></div>
                <h2>Carregando Grimório...</h2>
            </div>
        );
    }

    return (
        <div className="home-container">
            <header className="home-header">
                <div className="logo-area">
                    <h1>Grimório T20</h1>
                    <p>Gerenciador de Fichas de Tormenta 20</p>
                </div>
                <button className="btn-new-char" onClick={handleCriarNovo}>
                    + Novo Personagem
                </button>
            </header>

            <main className="char-grid-area">
                {personagens.length === 0 ? (
                    <div className="empty-state">
                        <h3>Nenhum personagem encontrado.</h3>
                        <p>Crie sua primeira ficha para começar a aventura!</p>
                        <button className="btn-new-char large" onClick={handleCriarNovo}>
                            Criar Ficha Agora
                        </button>
                    </div>
                ) : (
                    <div className="char-grid">
                        {personagens.map((char) => (
                            <div
                                key={char._id}
                                className="char-card"
                                onClick={() => navigate(`/ficha/${char._id}`)}
                            >
                                <div className="char-card-header">
                                    <h3 className="char-name">{char.cabecalho.nome || "Sem Nome"}</h3>
                                    <span className="char-level">Nível {char.cabecalho.nivel_total}</span>
                                </div>

                                <div className="char-info">
                                    <div className="info-pill race">{char.cabecalho.raca || "Raça?"}</div>
                                    <div className="info-pill class">
                                        {char.classes.map(c => c.nome).join(' / ') || "Classe?"}
                                    </div>
                                </div>

                                <div className="char-stats-preview">
                                    <div className="stat-mini">
                                        <span className="label">PV</span>
                                        <span className="value">{char.status.pv.atual}/{char.status.pv.maximo}</span>
                                    </div>
                                    <div className="stat-mini">
                                        <span className="label">PM</span>
                                        <span className="value">{char.status.pm.atual}/{char.status.pm.maximo}</span>
                                    </div>
                                </div>

                                <div className="char-actions">
                                    <button className="btn-open">Abrir Ficha</button>
                                    <button
                                        className="btn-delete"
                                        onClick={(e) => handleExcluir(e, char._id)}
                                        title="Excluir Personagem"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

export default Home;