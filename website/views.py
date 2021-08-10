from flask import Blueprint, Flask, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note  # This will import the parameters from models.py regarding the format of the "Note" database.
from . import db
import json

views = Blueprint('views', __name__)    # Blueprint method means that is telling the app that inside the app we have multiple routes


@views.route('/', methods=['GET', 'POST'])  # This is the route that will lead you to the home page. The method is used to let the home page know that we can GET the info and also POST or we can modify the page accordingly to the database.
@login_required  # And we have to login
def home():  # and after we have log in we can go back to the home page with this "defined function"
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # In case the note is valid and longer than 1 character, we can add the note to the database with the "data=note" and the "user_id=current_user.id" which the current user is being pulled from the flask_login module
            db.session.add(new_note)  #  THis will add the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)  # This is the route that will redirect or load into our Home Page in this case "home.html"

    
@views.route('/delete-note', methods=['POST'])  # This is the route that will use to delete the note using the jsonify in the index.js
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})