# import statements
from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from .code2vec import code2vec, interactive_predict
from gensim.models import KeyedVectors as word2vec

#load_dotenv()
db = SQLAlchemy()
DB_NAME = "database.db"

# initialize and set values for global variables
#code2vec model
model, config = code2vec.c2v()
predictor = interactive_predict.InteractivePredictor(config, model)

#load word2vec model using target name vectors
vectors_text_path_target = 'website/code2vec/models/java14_model/targets.txt'
target_model = word2vec.load_word2vec_format(vectors_text_path_target, binary=False)

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
    app.register_blueprint(auth, url_prefix = '/')

    # stuff for login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)



    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # end of init
    return app


#function that creates the database
def create_database(app: Flask):
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
        check = User.query.filter_by(username='cleanFreak2023').first()
        if not check:
            #create dummy users
            jonna = User(
                username = "cleanFreak2023",
                password = generate_password_hash("Gruiscool1", method='sha256'),
                highscore = 1000,
                current_score=0
            )

            nicole = User(
                username = 'Minions',
                password = generate_password_hash('Gruiscool2',method='sha256'),
                highscore = 0,
                current_score=0
            )

            # commit dummy users to the database
            db.session.add_all([jonna, nicole])
            db.session.commit()


#function to empty the database
def drop_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
    print('Database has been dropped!')

