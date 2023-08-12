import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Update the import

import Button from '@mui/material/Button';
import Login from './components/Login';

import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        
        {/* Define your routes */}
        <Routes> {/* Use Routes instead of Switch */}
          <Route path="/" element={<Login />} /> {/* Default route */}
          {/* Define other routes here */}
          {/* <Route path="/dashboard" element={<Dashboard />} /> */}
          {/* <Route path="/profile" element={<UserProfile />} /> */}
          {/* ... */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;



