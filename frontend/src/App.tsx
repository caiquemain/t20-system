import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

import Home from './pages/Home';
import Ficha from './pages/Ficha';
import Wizard from './pages/Wizard';
import Bestiario from './pages/Bestiario';
import AmeacaDetail from './pages/AmeacaDetail';
import Grimorio from './pages/Grimorio';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/ficha/:id" element={<Ficha />} />
                <Route path="/wizard" element={<Wizard />} />
                <Route path="/wizard/:id" element={<Wizard />} />
                
                <Route path="/bestiario" element={<Bestiario />} />
                <Route path="/ameaca/:id" element={<AmeacaDetail />} />

                <Route path="/grimorio" element={<Grimorio />} />

                <Route path="/ficha" element={<Navigate to="/" replace />} />
                <Route path="/ficha/" element={<Navigate to="/" replace />} />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </Router>
    );
}

export default App;
