from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv



load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"

#creation of the Flash app object
def create_app():
    app = Flask(__name__)

    if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
        print("Loading config.development and environment variables from .env file.")
        app.config['SECRET_KEY'] = 'secret-key-goes-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    else:
   # production 
        print("Loading config.production.")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
                                                    dbuser=os.environ['DBUSER'],
                                                    dbpass=os.environ['DBPASS'],
                                                    dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
                                                    dbname=os.environ['DBNAME']
                                                )
        app.config['SECRET_KEY'] = 'secret-key-goes-here'

    db.init_app(app)

    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    