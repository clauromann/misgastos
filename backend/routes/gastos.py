from flask import Blueprint, render_template, request, redirect, url_for
from ..database.models import db, Gasto
from datetime import datetime

gastos_bp = Blueprint('gastos', __name__)

@gastos_bp.route('/gastos', methods=['GET', 'POST'])
def gestionar_gastos():
    # Estas son las categorías de tu Excel
    categorias = ["Ocio", "Personal", "Suscripciones", "Vacaciones", "Otros"]
    
    if request.method == 'POST':
        nuevo_gasto = Gasto(
            categoria=request.form.get('categoria'),
            concepto=request.form.get('concepto'),
            cantidad=float(request.form.get('cantidad')),
            fecha=datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        )
        db.session.add(nuevo_gasto)
        db.session.commit()
        return redirect(url_for('gastos.gestionar_gastos'))

    # Traemos los gastos ordenados por fecha (el más reciente primero)
    todos_gastos = Gasto.query.order_by(Gasto.fecha.desc()).all()
    return render_template('gastos.html', gastos=todos_gastos, categorias=categorias)