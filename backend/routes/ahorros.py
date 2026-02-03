from flask import Blueprint, render_template, request, redirect, url_for
from ..database.models import db, Ahorro

ahorros_bp = Blueprint('ahorros', __name__)

@ahorros_bp.route('/ahorros', methods=['GET', 'POST'])
def lista_ahorros():
    if request.method == 'POST':
        concepto = request.form.get('concepto')
        cantidad = request.form.get('cantidad')
        
        nuevo_ahorro = Ahorro(concepto=concepto, cantidad=float(cantidad))
        db.session.add(nuevo_ahorro)
        db.session.commit()
        return redirect(url_for('ahorros.lista_ahorros'))

    todos_los_ahorros = Ahorro.query.order_by(Ahorro.fecha.desc()).all()
    total = sum(a.cantidad for a in todos_los_ahorros)
    return render_template('ahorros.html', ahorros=todos_los_ahorros, total=total)