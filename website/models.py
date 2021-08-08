from . import db  # the "." is the folder "website" called from the "__init__.py" file
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):  # In here we are creating the values for the "Notes"
    id = db.Column(db.Integer, primary_key=True)  # with the same ID for the unique user_id
    data = db.Column(db.String(10000))  # and no more than 10,000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # we also add the date when we create the note.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # A "foreignkey" is a key that takes the user id from another database. Is a column that it is in your database refering to another column in another database. In this case we are referencing the user from the other database in the table "user" looking for the "is"  "user.id" and the "user" should be in lower case when using the "foreignkey"


class User(db.Model, UserMixin):  # We are telling the database to create with this model storing this values
    id = db.Column(db.Integer, primary_key=True)  # In here the ID will be get from an integer column making the ID unique. This is needed because there will not be repeated values
    email = db.Column(db.String(150), unique=True)  # We are telling the app that the email should be unique. This avoids having 2 users with the same email address. Also we are telling the app that the email should  be no more than 150 characters long.
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')  # In here we are taking the ID from the note table and storing it in the database "User" referencing to the database "Note". In this case the "Note" it should be the first character in upper case. This relationship is one "user" to many "notes"