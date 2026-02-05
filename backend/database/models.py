from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relaciones para borrar en cascada si se borra el usuario
    ingresos = db.relationship('Ingreso', backref='usuario', lazy=True, cascade="all, delete-orphan")
    gastos = db.relationship('Gasto', backref='usuario', lazy=True, cascade="all, delete-orphan")
    huchas = db.relationship('Hucha', backref='usuario', lazy=True, cascade="all, delete-orphan")
    categorias_propias = db.relationship('CategoriaGasto', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    semana = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class CategoriaGasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subcategorias = db.relationship('SubcategoriaGasto', backref='categoria', lazy=True, cascade="all, delete-orphan")

class SubcategoriaGasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_gasto.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(100))
    categoria = db.Column(db.String(50), nullable=False)
    subcategoria = db.Column(db.String(50), nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Hucha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Ahorro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False) # Aquí irá el nombre de la hucha
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    mes = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)