import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Importações das Páginas (Default Exports)
import Home from './pages/Home';
import Ficha from './pages/Ficha';

function App() {
  return (
    <Router>
      <Routes>
        {/* Rota Principal: Lista de Personagens */}
        <Route path="/" element={<Home />} />
        
        {/* Rota da Ficha: Edição */}
        <Route path="/ficha/:id" element={<Ficha />} />
      </Routes>
    </Router>
  );
}

export default App;