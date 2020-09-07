import os
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DEBUG_MODE = str(os.environ.get('DEBUG_MODE')).lower() in {'true', '1', 'yes'}
REDIS_HOST = os.environ.get('REDIS_HOST', 'cache')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'fifteen')
DB_USER = os.environ.get('DB_USER', 'fifteen')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_ACTIVE = DB_HOST and DB_PORT

app = Flask(__name__)

if DB_ACTIVE:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db = SQLAlchemy(app)

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
