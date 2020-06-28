import os
from flask import Flask
import redis

# Установим значение режима отладки
DEBUG_MODE = str(
    os.environ.get('DEBUG_MODE', False)
).lower() not in ['0', 'false']

# Установим значение хоста и порта для клиента Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация клиента Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
)


@app.route('/')
def index():
    # Возьмём из Redis текущее значение счётчика
    count = redis_client.get('count')
    # Если значение получено - преобразуем его к числовому типу. Иначе зададим первоначальное значение 0
    count = int(count.decode()) if count is not None else 0
    # Увеличим значение на 1
    count += 1
    # Сохраним значение в Redis
    redis_client.set('count', count)
    # Вернём результат
    return f'Количество просмотров: {count}'


if __name__ == '__main__':
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0',
        port=5000,
    )
