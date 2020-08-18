from config import app, run


@app.route('/')
def main():
    return 'API-сервер работает'


if __name__ == '__main__':
    run()
