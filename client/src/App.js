import React from 'react';
import Main from './pages/Main.js';
import AdminInterface from './pages/AdminInterface.js';
import SelectFrames from './pages/SelectFrames.js';
import SchoolInterface from './pages/SchoolInterace.js';
import GroupInterface from './pages/GroupInterface.js';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';

import './App.css';

function App() {
  return (
    <Router>
               <div className="App">
        <Routes>
                    <Route exact path='/' element={< Main />}></Route>
                    <Route exact path='/admin' element={< AdminInterface />}></Route>
                    <Route exact path='/selectframes' element={< SelectFrames />}></Route>
                    <Route exact path='/school' element={< SchoolInterface />}></Route>
                    <Route exact path='/group-page' element={< GroupInterface />}></Route>
                     
              </Routes>
              
    </div>
    </Router>
  );    
}

export default App;
