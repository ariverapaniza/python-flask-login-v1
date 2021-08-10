# This will make the folder "website" as a Python package. 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # We have to add this in order to trigger the SQLAlchemy
from os import path  # This is for the operating system import the path to the database
from flask_login import LoginManager  # We have to import this in order to trigger the LoginManager

db = SQLAlchemy()  # This will create the "Object" instance triggering the SQLAlchemy
DB_NAME = "database.db"  # This will create the "Database" file


def create_app():
    app = Flask(__name__)  # This will initialize the Flask app
    app.config['SECRET_KEY'] = 'mySecretKey'  # we have to create a pass. In production we do not share this key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # in this line we are telling the app that our database is located in this address. 
    db.init_app(app)  # and in here we are telling the app to start the sqlalchemy in flask

    from .views import views  # in here we are telling the code to import the "blueprint" views.py
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  # and with this we are telling the code to register the views blueprint. The / means that there are not prefix. 
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note  #  This will import the "models.py" calling the "User" and "Note"

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # We are going to be redirected to this page if we are not logged in
    login_manager.init_app(app)  # this will know which app is going to be used for the login login_manager

    @login_manager.user_loader  # This will tell flask to load the user
    def load_user(id):
        return User.query.get(int(id))  # This will tell flask to load the user

    return app


def create_database(app):  # This will check if the database already exists and create it if it doesnt
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')