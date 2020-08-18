import React, { useEffect, useState } from 'react';
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

  const newGame = () => callApi('/api/new_game');

  const move = (index) => callApi(`/api/move/${index}`);

  return (
    <div className='game'>
      {
        gameState && Object.keys(gameState).length !== 0 &&
        <>
          <div className='move-count'>
            Ходов: <b>{gameState['move_count']}</b>
          </div>
          <Board gameState={gameState}
                 moveHandler={move}/>
          {gameState['win'] && <h1>Вы победили!</h1>}
        </>
      }
      <div className='new-game'
           onClick={newGame}>Новая игра
      </div>
    </div>
  );
}

function Board({gameState, moveHandler}) {
  const {values} = gameState;
  const movables = new Set();
  if (!gameState['win']) {
    const emptyIndex = values.indexOf('');
    movables.add(emptyIndex - 4);
    movables.add(emptyIndex + 4);
    if ((emptyIndex + 1) % 4) {
      movables.add(emptyIndex + 1);
    }
    if ((emptyIndex - 1) % 4 !== 3) {
      movables.add(emptyIndex - 1);
    }
  }
  return (
    <div className='board'>
      {
        values.map(
          (i, idx) =>
            <div className={movables.has(idx) && 'movable'}
                 onClick={movables.has(idx) ? () => moveHandler(idx) : null}
                 key={i}>
              {i}
            </div>
        )
      }
    </div>
  );
}

export default App;