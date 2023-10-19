import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing.js';
import Idea from './pages/Idea.js';
import About from './pages/About.js';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/about" element={<About />} />
          <Route path="/idea" element={<Idea />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
