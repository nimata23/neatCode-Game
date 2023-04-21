# imports
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin

# leaderboard data class
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(30), db.ForeignKey('user.id'))
    second = db.Column(db.String(30),db.ForeignKey('user.id'))
    third = db.Column(db.String(30),db.ForeignKey('user.id'))

# user data class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    highscore = db.Column(db.Integer)
    current_score = db.Column(db.Integer)
