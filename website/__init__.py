# import statements
from venv import create
from flask import flask
from flask_aqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
from werkzeung.security import generate_password_hash

load_dotenv()
db = SQLAlchemy()
DB_NAME = "database.db"

# creates the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    db.init_app(app)

    #creates the databases
    from .models import User

    create_database(app)
    dummy_populate(app)

    # register blueprints for other pages (views and authentication)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')

    # stuff for login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user.loader
    def load_user(id):
        return User.query.get(int(id))
    
    # end of init
    return app


#function that creates the database
def create_database(app: FLask):
    #use app context in order to initialize properly
    with app.app_context():
        db.create_all()

        #debugging message
        print('Created Database')


#function to populate database with dummy values
def dummy_populate(app):
    with app.app_context():
        #check if there are users
        from .models import User
        check = User.query.filter_by(username='nimata23').first()
        if not check:
            #add dummy data here


#function to empty the database
def drop_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
    print('Database has been dropped!')