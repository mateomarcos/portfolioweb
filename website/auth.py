from flask import Blueprint, request, flash, redirect, url_for, render_template
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash #forma de hacer una contrase;a segura encriptandola

auth = Blueprint('auth',__name__, static_folder='static',template_folder='templates')

@auth.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')      
        password = request.form.get('password')  

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Sesion iniciada correctamente', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('La contraseña es erronea', category='error')
        else:
            flash('La direccion ingresada no existe', category='error')

    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required #solo podes acceder a esta pagina si estas logueado
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign_up", methods=["POST","GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email='email').first() #chequear si ya existe
        if user:
            flash('Ya existe una cuenta con esta direccion asociada', category='error')
        elif len(email) < 4:
            flash("El email debe tener mas de 3 caracteres", category ="error")    
        elif len(firstName) < 3:
            flash("El nombre debe ser mayor a 2 caracteres", category="error")
        elif password1 != password2:
            flash("Las contraseñas no coinciden", category="error")
            pass
        elif len(password1) < 11:
            flash("La longitud de la contraseña debe ser mayor a 10 caracteres", category="error")
        else:
            new_user = User(email=email, first_name = firstName, password = generate_password_hash(password1, method= 'sha256')) 
            db.session.add(new_user)
            db.session.commit()
            flash("Cuenta creada correctamente!", category="success")   #add user to database
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user = current_user)