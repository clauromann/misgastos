from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(20), nullable=False) # Enero, Febrero...
    semana = db.Column(db.Integer, nullable=False) # 1, 2, 3, 4, 5
    concepto = db.Column(db.String(50))           # Salario, Paga...
    cantidad = db.Column(db.Float, default=0.0)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    categoria = db.Column(db.String(50))          # Ocio, Personal, Otros...
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float, nullable=False)

class Ahorro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)