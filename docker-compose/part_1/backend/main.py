import datetime
import json
import random

import pytz
from flask import Flask
import redis

import config as c

app = Flask(__name__)

redis_client = redis.Redis(
    host=c.REDIS_HOST,
    port=c.REDIS_PORT,
)


@app.route('/api/new_game')
def new_game():
    values = [i+1 for i in list(range(15))]
    random.shuffle(values)
    values.append('')
    game_state = json.dumps({
        'values': values,
        'start_time': datetime.datetime.now(tz=pytz.UTC).isoformat(),
        'finish_time': None,
    })
    redis_client.set('game_state', game_state)
    return game_state


@app.route('/api/game_info')
def game_info():
    info = redis_client.get('game_state') or None
    return info.decode() if info else json.dumps(info)


if __name__ == '__main__':
    app.run(
        debug=c.DEBUG_MODE,
        host='0.0.0.0',
        port=5000,
    )
