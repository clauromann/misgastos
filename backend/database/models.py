from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    semana = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    
class CategoriaGasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    subcategorias = db.relationship('SubcategoriaGasto', backref='categoria', lazy=True, cascade="all, delete-orphan")

class SubcategoriaGasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_gasto.id'), nullable=False)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(100))
    categoria = db.Column(db.String(50), nullable=False)
    subcategoria = db.Column(db.String(50), nullable=False)
    mes = db.Column(db.String(20), nullable=False)

class Hucha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class Ahorro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False) # Aquí irá el nombre de la hucha
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    mes = db.Column(db.String(20), nullable=False)