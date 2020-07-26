# Импортируем встроенные библиотеки для работы с JSON и псевдослучайными значениями
import json
import random

# Импортируем объекты приложения и клиента Redis, а также функцию запуска веб-сервера
from config import app, redis_client, run


# Регистрируем функцию, обрабатывающую запрос по пути /api/new_game
@app.route('/api/new_game')
def new_game():
    # Сфромируем список из 15 значений (от 1 до 15)
    values = [i+1 for i in list(range(15))]
    # Перемешаем значения списка в случайном порядке
    random.shuffle(values)
    # Добавим в конец списка значение, содержащее пустую строку
    values.append('')
    # Сформируем JSON-объект с данными о текущей игре
    game_state = json.dumps({
        'values': values,
        'move_count': 0,
        'win': False,
    })
    # Сохраним информацию в Redis
    redis_client.set('game_state', game_state)
    # Вернём инфомрацию в ответ на запрос
    return game_state


# Регистрируем функцию, обрабатывающую запрос по пути /api/game_info
@app.route('/api/game_info')
def game_info():
    # Получим из Redis информацию о текущей игре
    info = redis_client.get('game_state') or None
    # Если информация получена, декодируем её и вернём в ответе на запрос,
    # Иначе, вернём пустой объект
    return info.decode() if info else {}


# При выполнении текущего файла запустим веб-сервер
if __name__ == '__main__':
    run()
