from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class GameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
