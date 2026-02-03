from flask import Blueprint, render_template, request, redirect, url_for
from ..database.models import db, Ingreso
from datetime import datetime

ingresos_bp = Blueprint('ingresos', __name__)

@ingresos_bp.route('/ingresos', methods=['GET', 'POST'])
def gestionar_ingresos():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if request.method == 'POST':
        nuevo_ingreso = Ingreso(
            mes=request.form.get('mes'),
            semana=int(request.form.get('semana')),
            concepto=request.form.get('concepto'),
            cantidad=float(request.form.get('cantidad'))
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()
        return redirect(url_for('ingresos.gestionar_ingresos'))

    # Obtenemos el mes actual para filtrar por defecto (opcional)
    todos_ingresos = Ingreso.query.order_by(Ingreso.id.desc()).all()
    return render_template('ingresos.html', ingresos=todos_ingresos, meses=meses)