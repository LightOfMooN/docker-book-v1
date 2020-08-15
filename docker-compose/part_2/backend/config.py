# Импортируем библиотеку фреймворка Flask
from flask import Flask
# Импортируем библиотеку для работы с Redis
import redis

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация клиента Redis
redis_client = redis.Redis(
    host='cache',
    port=6379,
)


# Функция запуска веб-сервера приложения
def run():
    app.run(
        host='0.0.0.0',
        port=5000,
    )
