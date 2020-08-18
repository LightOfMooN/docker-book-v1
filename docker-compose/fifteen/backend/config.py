import os
import redis
from flask import Flask

DEBUG_MODE = str(os.environ.get('DEBUG_MODE')).lower() in {'true', '1', 'yes'}
REDIS_HOST = os.environ.get('REDIS_HOST', 'cache')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

app = Flask(__name__)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
)


def run():
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=DEBUG_MODE,
    )
