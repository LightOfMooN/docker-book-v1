# Импортируем встроенную библиотеку для работы с операционной системой
import os

# Импортируем библиотеку фреймворка Flask
from flask import Flask
# Импортируем библиотеку для работы с Redis
import redis

# Переменная, содержащая значение активности режима отладки (Да/Нет)
DEBUG_MODE = bool(os.environ.get('DEBUG_MODE', False))

# Переменные хоста и порта Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация клиента Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
)


# Функция запуска веб-сервера приложения
def run():
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0',
        port=5000,
    )
