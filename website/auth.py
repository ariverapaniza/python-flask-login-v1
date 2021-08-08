from flask import Blueprint, render_template, request, flash, redirect, url_for  # "flash" is a Flask method to return error messages determined in the "if else" statement. 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash  # This is really important because will transform the password that we used to create the user to a HASH but we can not take that hash and convert it to the password that we input. Then to check if the password is correct we type the password and then it will transform the password to the HASH again and if it match the hash stored then it grants access
from . import db  #  This is to import the db to store the new users into the database
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)     # Blueprint method means that is telling the app that inside the app we have multiple routes


@auth.route('/login', methods=['GET', 'POST'])  # We have to create the routes for the login logout and sign up methods using "defined functions" depending of the action taken by the user. This one is for the LOGIN action.  Notice that this has a prefix, in this case is "/login, /logout, /sign-up" calling different routes and depending of the route we take we will be redirected to an specific page  ## a GET request is to get information and a POST request is modifying or creating information. The GET request is like refreshing the page and the POST request is like submitting information to the server. 
def login():
    if request.method == 'POST':  # THis will request the email and the password
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # So in here we can check if the user is already exists looking for "User (database)"."query (parameter to look for)"."filter_by (look for the email if exist)"."first (first result)"
        if user:
            if check_password_hash(user.password, password):  # if the user exist we check the password with the database and the password entered into the form, if it match access granted!
                flash('Logged in successfully!', category='success')  # THis is a variable that when called in the html it will display the message. The python code in the html is created between 2 curly brackets "{{ example="message" }}" like this.  The "flash" is a flask method to display error messages in the html. the "category" parameter is to get a category for the error messages, it can have any name. 
                login_user(user, remember=True)  # This will remember that the user is logged in until it logs out
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')  # This is to the LOG OUT action
@login_required # We can not access the auth.login if we are logged
def logout():
    logout_user()  # we are going to log out the user
    return redirect(url_for('auth.login'))  # and redirect back to the login page


@auth.route('/sign-up', methods=['GET', 'POST'])  #  and this is for the SIGN UP method
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))  # The SHA256 will be the hashing method to encrypt the password
            db.session.add(new_user)  # The new user will be created into the database and 
            db.session.commit() # this will make the database commit or tell the database to store what we just added. 
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # after we created the user, we should redirect back to the home page

    return render_template("sign_up.html", user=current_user)