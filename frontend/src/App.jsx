import React from 'react';
import './App.css';
import Registration from '../pages/signup';
import Navbar from '../components/navbar';

function App() {
  return (
    <>
      <Navbar />
      <div className="flex justify-center items-center h-screen">
        <Registration />
      </div>
    </>
  );
}

export default App;
