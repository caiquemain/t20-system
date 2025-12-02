import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

interface Personagem {
  _id: string;
  cabecalho: {
    nome: string;
    raca: string;
    classe: string;
    nivel_total: number;
  };
  atributos: {
    forca: number;
    destreza: number;
    constituicao: number;
    inteligencia: number;
    sabedoria: number;
    carisma: number;
  };
  status: {
    pv: { atual: number; maximo: number };
    pm: { atual: number; maximo: number };
    defesa: { total: number };
  };
  inventario: {
    carga_total: number;
    carga_maxima: number;
  }
}

function App() {
  const [personagens, setPersonagens] = useState<Personagem[]>([]);
  const [opcoesRacas, setOpcoesRacas] = useState<string[]>([]);
  const [opcoesClasses, setOpcoesClasses] = useState<string[]>([]);

  const [form, setForm] = useState({
    nome: '',
    raca: '',
    classe: '',
    forca: 0, destreza: 0, constituicao: 0,
    inteligencia: 0, sabedoria: 0, carisma: 0
  });

  const API_URL = 'http://localhost:8000';

  useEffect(() => {
    const carregarDados = async () => {
      try {
        const [resPersonagens, resRacas, resClasses] = await Promise.all([
          axios.get(`${API_URL}/personagens/`),
          axios.get(`${API_URL}/racas`),
          axios.get(`${API_URL}/classes`)
        ]);

        setPersonagens(resPersonagens.data);
        setOpcoesRacas(resRacas.data);
        setOpcoesClasses(resClasses.data);

        setForm(prev => ({
          ...prev,
          raca: resRacas.data[0] || 'Humano',
          classe: resClasses.data[0] || 'Guerreiro'
        }));

      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      }
    };

    carregarDados();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      usuario_id: "user_front",
      cabecalho: {
        nome: form.nome,
        jogador: "Você",
        raca: form.raca,
        origem: "Aventureiro",
        divindade: "Nenhuma",
        nivel_total: 1
      },
      classes: [{ nome: form.classe, nivel: 1, primaria: true }],
      atributos: {
        forca: Number(form.forca),
        destreza: Number(form.destreza),
        constituicao: Number(form.constituicao),
        inteligencia: Number(form.inteligencia),
        sabedoria: Number(form.sabedoria),
        carisma: Number(form.carisma)
      },
      status: { pv: { atual: 0, maximo: 0 }, pm: { atual: 0, maximo: 0 } },
      inventario: { dinheiro: { tl: 0, tp: 0, to: 0 }, equipamentos: [] }
    };

    try {
      await axios.post(`${API_URL}/personagens/`, payload);
      const res = await axios.get(`${API_URL}/personagens/`);
      setPersonagens(res.data);
      alert("Personagem criado com sucesso!");
    } catch (error) {
      console.error("Erro ao criar:", error);
      alert("Erro ao criar personagem.");
    }
  };

  const handleDelete = async (id: string, nome: string) => {
    if (confirm(`Tem certeza que deseja apagar a ficha de ${nome}?`)) {
      try {
        await axios.delete(`${API_URL}/personagens/${id}`);
        // Atualiza a lista localmente filtrando o removido
        setPersonagens(prev => prev.filter(p => p._id !== id));
      } catch (error) {
        console.error("Erro ao deletar:", error);
        alert("Erro ao deletar ficha.");
      }
    }
  };

  const handleDeleteAll = async () => {
    if (confirm("ATENÇÃO: Isso apagará TODAS as fichas do sistema. Deseja continuar?")) {
      try {
        await axios.delete(`${API_URL}/personagens/`);
        setPersonagens([]);
        alert("Todas as fichas foram apagadas.");
      } catch (error) {
        console.error("Erro ao limpar tudo:", error);
      }
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <div className="container">
      <h1 style={{ textAlign: 'center' }}>⚔️ Tormenta 20 - Criador de Fichas</h1>

      <div className="card-form">
        <h3>Novo Personagem</h3>
        <form onSubmit={handleSubmit} className="form-grid">

          <div style={{ gridColumn: '1 / -1' }}>
            <label>Nome do Personagem:</label>
            <input name="nome" value={form.nome} onChange={handleInput} placeholder="Ex: Valeros" required />
          </div>

          <div>
            <label>Raça:</label>
            <select name="raca" value={form.raca} onChange={handleInput}>
              {opcoesRacas.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>

          <div>
            <label>Classe (Nível 1):</label>
            <select name="classe" value={form.classe} onChange={handleInput}>
              {opcoesClasses.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          {['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'].map(attr => (
            <div key={attr}>
              <label style={{ textTransform: 'capitalize' }}>{attr}:</label>
              <input type="number" name={attr} value={form[attr as keyof typeof form]} onChange={handleInput} />
            </div>
          ))}

          <div style={{ gridColumn: '1 / -1', marginTop: '10px' }}>
            <button type="submit" className="btn-primary">
              Criar Ficha & Calcular Regras
            </button>
          </div>
        </form>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3>Fichas Salvas ({personagens.length})</h3>
        {personagens.length > 0 && (
          <button onClick={handleDeleteAll} className="btn-danger-small">
            🗑️ Limpar Tudo
          </button>
        )}
      </div>

      <div className="char-grid">
        {personagens.map((p) => (
          <div key={p._id} className="char-card">
            <div className="char-header">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <h2>{p.cabecalho.nome}</h2>
                <button
                  onClick={() => handleDelete(p._id, p.cabecalho.nome)}
                  className="btn-delete-card"
                  title="Apagar ficha"
                >
                  ✕
                </button>
              </div>
              <div className="char-subtitle">
                {p.cabecalho.raca} {p.cabecalho.classe} (Nvl {p.cabecalho.nivel_total})
              </div>
            </div>

            <div className="stats-row">
              <div className="stat-badge pv">❤️ PV: {p.status.pv.maximo}</div>
              <div className="stat-badge pm">💙 PM: {p.status.pm.maximo}</div>
              <div className="stat-badge def">🛡️ Def: {p.status.defesa.total}</div>
            </div>

            <div className="attributes-box">
              <strong>Atributos:</strong><br />
              FOR {p.atributos.forca} | DES {p.atributos.destreza} | CON {p.atributos.constituicao}<br />
              INT {p.atributos.inteligencia} | SAB {p.atributos.sabedoria} | CAR {p.atributos.carisma}
            </div>

            <div className="char-footer">
              🎒 Espaços: {p.inventario.carga_total} / {p.inventario.carga_maxima}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;