import React, { useState, useEffect } from 'react';
import './App.css';


function App() {
  const [gameState, setGameState] = useState();

  const callApi = (url) => {
    fetch(url)
      .then(response => response.json())
      .then(result => {
          setGameState(result);
        }
      );
  };

  useEffect(
    () => callApi('/api/game_info'),
    []
  );

  return <>
    {
      gameState && gameState['values']
    }
  </>;
}

export default App;
