import json
import random
from config import app, redis_client, run, db, DB_ACTIVE
from models import Results


@app.route('/')
def main():
    return 'API-сервер работает'


@app.route('/api/new_game')
def new_game():
    values = [i + 1 for i in list(range(15))]
    random.shuffle(values)
    values.append('')
    game_state = json.dumps({
        'values': values,
        'move_count': 0,
        'win': False,
    })
    redis_client.set('game_state', game_state)
    return game_state


@app.route('/api/game_info')
def game_info():
    info = redis_client.get('game_state') or None
    return info.decode() if info else {}


@app.route('/api/move/<int(min=0, max=15):index>')
def move(index: int):
    game_state = json.loads(
        redis_client.get('game_state').decode()
    )
    moved = False
    if not game_state['win']:
        values = game_state['values']
        empty_index = values.index('')
        movable_indexes = {empty_index - 4, empty_index + 4}
        if (empty_index + 1) % 4:
            movable_indexes.add(empty_index + 1)
        if (empty_index - 1) % 4 != 3:
            movable_indexes.add(empty_index - 1)
        if index in movable_indexes:
            values[empty_index] = values[index]
            values[index] = ''
            game_state['values'] = values
            moved = True
            game_state['move_count'] += 1
            if values[-1] == '':
                last_value = values[0]
                win = True
                for value in values[1:-1]:
                    if value < last_value:
                        win = False
                        break
                    last_value = value
                game_state['win'] = win
                if win and DB_ACTIVE:
                    result = Results(move_count=game_state['move_count'])
                    db.session.add(result)
                    db.session.commit()
    game_state = json.dumps(game_state)
    if moved:
        redis_client.set('game_state', game_state)
    return game_state


@app.route('/api/last_results/<int(min=1):number>')
def last_results(number):
    results = []
    if DB_ACTIVE:
        for r in Results.query.order_by(Results.id.desc()).limit(number).all():
            results.append(r.move_count)
    return json.dumps(results)


if __name__ == '__main__':
    run()
