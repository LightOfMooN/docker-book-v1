import os

DEBUG_MODE = bool(os.environ.get('DEBUG_MODE', False))

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
