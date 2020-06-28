# Импортируем библиотеку фреймворка Flask
from flask import Flask
# Импортируем библиотеку для работы с Redis
import redis

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация клиента Redis
redis_client = redis.Redis(
    host='redis',
    port=6379,
)


# Регистрируем функцию, обрабатывающую запрос по корневому пути
@app.route('/')
def index():
    # Возьмём из Redis текущее значение счётчика
    count = redis_client.get('count')
    # Если значение получено - преобразуем его к числовому типу.
    # Иначе зададим первоначальное значение: 0
    count = int(count.decode()) if count is not None else 0
    # Увеличим значение на 1
    count += 1
    # Сохраним значение в Redis
    redis_client.set('count', count)
    # Вернём результат
    return f'Количество просмотров: {count}'


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
