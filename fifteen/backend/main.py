import datetime
import json
import random

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

import config as c

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{c.DB_USER}:{c.DB_PASSWORD}@{c.DB_HOST}:{c.DB_PORT}/{c.DB_NAME}'

db = SQLAlchemy(app)

redis_client = redis.Redis(
    host=c.REDIS_HOST,
    port=c.REDIS_PORT,
)


class Results(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    finish_time = db.Column(db.DateTime)
    elapsed_time = db.Column(db.Integer, index=True)


def get_disorders(values):
    count = 0
    for index in range(len(values) - 1):
        value = values[index]
        for i in values[index + 1:]:
            if i < value:
                count += 1
    return count


@app.route('/api/new_game')
def new_game():
    values = [i+1 for i in list(range(15))]
    random.shuffle(values)
    while get_disorders(values) % 2:
        random.shuffle(values)
    values.append('')
    game_state = json.dumps({
        'values': values,
        'start_time': datetime.datetime.now(tz=pytz.UTC).isoformat(),
        'finish_time': None,
    })
    redis_client.set('game_state', game_state)
    return game_state


@app.route('/api/move/<int(min=0, max=15):index>')
def move(index: int):
    game_state = json.loads(
        redis_client.get('game_state').decode()
    )
    moved = False
    # Обработаем перемещение только если игра не закончена
    if not game_state['finish_time']:
        values = game_state['values']
        empty_index = values.index('')
        # Сформируем набор перемещаемых индексов
        movable_indexes = {
            empty_index - 4,
            empty_index + 4,
        }
        if (empty_index + 1) % 4:
            movable_indexes.add(empty_index + 1)
        if (empty_index - 1) % 4 != 3:
            movable_indexes.add(empty_index - 1)
        # Поменяем значения местами, если это возможно
        if index in movable_indexes:
            values[empty_index] = values[index]
            values[index] = ''
            game_state['values'] = values
            moved = True
            # Проверим на факт победы
            if values[-1] == '':
                last_value = values[0]
                win = True
                for value in values[1:-1]:
                    if value < last_value:
                        win = False
                        break
                    last_value = value
                if win:
                    finish_time = datetime.datetime.now(tz=pytz.UTC)
                    game_state['finish_time'] = finish_time.isoformat()
                    result = Results(
                        finish_time=finish_time,
                        elapsed_time=(
                            finish_time - datetime.datetime.fromisoformat(
                                game_state['start_time']
                            )
                        ).seconds
                    )
                    db.session.add(result)
                    db.session.commit()
    game_state = json.dumps(game_state)
    if moved:
        redis_client.set('game_state', game_state)
    return game_state


@app.route('/api/game_info')
def game_info():
    info = redis_client.get('game_state') or None
    return info.decode() if info else json.dumps(info)


@app.route('/api/last_results/<int:number>')
def last_results(number):
    return json.dumps([
        {
            'finish_time': r.finish_time.isoformat(),
            'elapsed_time': r.elapsed_time,
        } for r in Results.query.order_by(Results.id.desc()).limit(number).all()
    ])


if __name__ == '__main__':
    app.run(
        debug=c.DEBUG_MODE,
        host='0.0.0.0',
        port=5000,
    )
