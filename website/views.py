from flask import Blueprint, Flask, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)    # Blueprint method means that is telling the app that inside the app we have multiple routes


@views.route('/', methods=['GET', 'POST'])  # This is the route that will lead you to the home page 
@login_required  # And we have to login
def home():  # and after we have log in we can go back to the home page with this "defined function"
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)  # This is the route that will redirect or load into our Home Page in this case "home.html"

    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})