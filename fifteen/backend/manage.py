from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# export FLASK_APP=manage.py
# flask db init
# flask db migrate
if __name__ == '__main__':
    manager.run()
