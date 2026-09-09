import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

import Home from './pages/Home';
import Ficha from './pages/Ficha';
import Wizard from './pages/Wizard';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/ficha/:id" element={<Ficha />} />
                <Route path="/wizard" element={<Wizard />} />
                <Route path="/wizard/:id" element={<Wizard />} />
            </Routes>
        </Router>
    );
}

export default App;