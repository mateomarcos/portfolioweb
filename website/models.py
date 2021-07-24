from datetime import timezone
from sqlalchemy.sql.schema import ForeignKey
from . import db #importar del paquete actual el objeto db
from flask_login import UserMixin
from sqlalchemy import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #asi se establece una RELACION!, user se escribe en minuscula porque sql lo va referenciar en minuscula


class User(db.Model, UserMixin): #UserMixin permite usar el modulo flask_login
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True) #unique indica que solo 1 usuario puede tener el mismo mail
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')#al hacer referencias en Relationship si se pone el nombre de la clase, relacion uno a muchos!

    role = db.Column(db.Integer, default = 0) #0 usuario, 1 admin

class Project(db.Model):
    id = db.Column(db.Integer, primary_ley = True)
    name = db.Column(db.String(150), unique = True)
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    description = db.Column(db.String(150))
    link = db.Column(db.String(150))
    