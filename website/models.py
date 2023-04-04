# imports
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from . import db

# leaderboard data class
class Leaderboard(db.Model):
    username = db.Column(db.String(30), unique=True)

# user data class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    highscore = db.Column(db.Integer)
    current_score = db.Column(db.Integer)