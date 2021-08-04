# This will make the folder "website" as a Python package. 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)  # This will initialize the Flask app
    app.config['SECRET_KEY'] = 'mySecretKey'  # we have to create a pass. In production we do not share this key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views  # in here we are telling the code to import the "blueprint" views.py
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  # and with this we are telling the code to register the views blueprint. The / means that there are not prefix. 
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')