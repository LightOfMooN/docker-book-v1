from flask_migrate import Migrate
from config import db, app


class Results(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    move_count = db.Column(db.Integer)


migrate = Migrate(app, db)
