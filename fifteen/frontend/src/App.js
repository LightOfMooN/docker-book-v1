import React, { useEffect, useState } from 'react';
import './App.css';


function Board({gameState, moveHandler}) {
  const {values} = gameState;
  const emptyIndex = values.indexOf('');
  const movableIndexes = new Set();
  if (!gameState['finish_time']) {
    [-4, 4].forEach(
      i => movableIndexes.add(emptyIndex + i)
    );
    if ((emptyIndex + 1) % 4) {
      movableIndexes.add(emptyIndex + 1);
    }
    if ((emptyIndex - 1) % 4 !== 3) {
      movableIndexes.add(emptyIndex - 1);
    }
  }
  return (
    <div className='board'>
      {
        values.map(
          (i, index) =>
            <div className={movableIndexes.has(index) ? 'cell movable' : 'cell'}
                 onClick={movableIndexes.has(index) ? () => moveHandler(index) : null}
                 key={i}>{i}
            </div>
        )
      }
    </div>
  );
}

function App() {
  const [gameState, setGameState] = useState();
  const [finishTime, setFinishTime] = useState(new Date());
  const [timerId, setTimerId] = useState(0);
  const [lastResults, setLastResults] = useState([]);

  useEffect(
    () => {
      fetch('/api/game_info')
        .then(response => response.json())
        .then(result => {
          setGameState(result);
          if (result['finish_time']) {
            setFinishTime(new Date(result['finish_time']));
          } else if (result['start_time']) {
            runTimer();
          }
        });
      updateLastResults();
    },
    []
  );

  const runTimer = () => {
    setFinishTime(new Date());
    if (!timerId) {
      setTimerId(
        setInterval(
          () => {
            setFinishTime(new Date());
          },
          1000
        )
      );
    }
  };

  const updateLastResults = () => {
    fetch('/api/last_results/5')
      .then(response => response.json())
      .then(results => {
        const items = results.map(result => {
          return {
            finishTime: new Date(result['finish_time']).toLocaleString(),
            elapsedTime: result['elapsed_time']
          }
        });
        setLastResults(items);
      });
  };

  const newGame = () => {
    fetch('/api/new_game')
      .then(response => response.json())
      .then(result => {
          runTimer();
          setGameState(result);
        }
      );
  };

  const move = (index) => {
    fetch(`/api/move/${index}`)
      .then(response => response.json())
      .then(result => {
        setGameState(result);
        if (result['finish_time']) {
          clearInterval(timerId);
          setTimerId(0);
          setFinishTime(new Date(result['finish_time']));
          updateLastResults();
        }
      });
  };

  return (
    <div className='game'>
      {
        gameState &&
        <>
          <h1>{
            gameState['finish_time']
              ? 'Вы победили за '
              : null
          }
            {Math.floor((finishTime - new Date(gameState['start_time'])) / 1000)} с.
          </h1>
          <Board gameState={gameState}
                 moveHandler={move}/>
        </>
      }
      <div className={'new-game'}
           onClick={newGame}>Новая игра
      </div>
      {
        lastResults ?
          <div className={'results'}>
            <h2>Последние результаты</h2>
            {
              lastResults.map(
                (result, index) => <div key={index}>
                  Победа {result.finishTime} за <span>{result.elapsedTime}</span> с.
                </div>
              )
            }
          </div>
          : null
      }
    </div>
  );
}

export default App;
