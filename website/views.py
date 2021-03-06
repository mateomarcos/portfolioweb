from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note,Project
from . import db
import json

views = Blueprint('views',__name__, static_folder='static',template_folder='templates')


@views.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html', user = current_user)


@views.route("/portfolio", methods=['GET','POST'])
def portfolio():
    if request.method=="POST" and current_user.role == 1:
        name = request.form.get("name")
        enlace = request.form.get("enlace")
        description = request.form.get("description")
        new_project = Project(name=name, link=enlace,description=description)
        db.session.add(new_project)
        db.session.commit()
        flash("Proyecto creado correctamente!", category="success")
    projects = Project.query.all()
    return render_template('portfolio.html', user=current_user, projects=projects)

@views.route("/", methods=['GET','POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash('No puedes agregar una nota vacia!', category = 'error')
        else:
            flash('Comentario agregado!', category='success')
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

@views.route("/delete-project", methods = ['POST'])
def delete_project():
    data =json.loads(request.data)
    projectId = data['projectId']
    project = Project.query.get(projectId)
    if project:
        if current_user.role == 1:
            db.session.delete(project)
            db.session.commit()
    return jsonify({})