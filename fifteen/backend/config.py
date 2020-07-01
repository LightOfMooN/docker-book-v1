import os

DEBUG_MODE = bool(os.environ.get('DEBUG_MODE', False))

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'fifteen')
DB_USER = os.environ.get('DB_USER', 'fifteen')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
