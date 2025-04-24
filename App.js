import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './Home.js';
import MainScreen from '/Users/nicholasfiebig/Desktop/DJ-Group-Project/src/Hard.jsx';
import './App.css';


function App() {

  return ( <div>
    <BrowserRouter>
      <Routes>
          <Route index element = {<Home/>} /> 
          <Route path="/home" element = {<Home/>} />
          <Route path="/hard" element = {<MainScreen/>} />
        </Routes>
  </BrowserRouter>

 
        
  </div>
  );
  }

export default App;
