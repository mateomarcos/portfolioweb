from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
views = Blueprint('views',__name__, static_folder='static',template_folder='templates')


@views.route("/portfolio", methods=['GET','POST'])
def portfolio():
    if request.method=="POST" and current_user.role == "admin":
        project = request.form.get('portfolio')
        #crear un nuevo proyecto
        
    return render_template('portfolio.html', user=current_user)

@views.route("/", methods=['GET','POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash('No puedes agregar una nota vacia!', category = 'error')
        else:
            flash('Nueva nota agregada!', category='success')
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html', user=current_user)

@views.route("/delete-note", methods = ['POST'])
def delete_note():
    data =json.loads(request.data)
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})