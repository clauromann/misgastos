from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Ingreso  
from datetime import datetime
from flask_login import login_required, current_user #

ingresos_bp = Blueprint('ingresos', __name__)

@ingresos_bp.route('/ingresos', methods=['GET', 'POST'])
@login_required #
def gestionar_ingresos():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    mes_hoy = meses_es[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_hoy)
    uid = current_user.id #

    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        mes_real = meses_es[fecha_dt.month - 1] 
        
        nuevo_ingreso = Ingreso(
            cantidad=float(request.form.get('cantidad')),
            concepto=request.form.get('concepto'),
            categoria=request.form.get('categoria'),
            fecha=fecha_dt,
            semana=int(request.form.get('semana')),
            mes=mes_real,
            user_id=uid # Sello del usuario
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()
        return redirect(url_for('ingresos.gestionar_ingresos', mes=mes_real))

    # Ingresos filtrados por usuario
    ingresos = Ingreso.query.filter_by(mes=mes_seleccionado, user_id=uid).order_by(Ingreso.fecha.desc()).all()
    total_mes = sum(i.cantidad for i in ingresos)

    # Gráficos filtrados por usuario
    stats_cat = db.session.query(Ingreso.categoria, db.func.sum(Ingreso.cantidad))\
        .filter_by(mes=mes_seleccionado, user_id=uid)\
        .group_by(Ingreso.categoria).all()
    labels_cat = [s[0] for s in stats_cat]
    values_cat = [float(s[1]) for s in stats_cat]

    stats_sem = db.session.query(Ingreso.semana, db.func.sum(Ingreso.cantidad))\
        .filter_by(mes=mes_seleccionado, user_id=uid)\
        .group_by(Ingreso.semana).all()
    
    dict_sem = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for s in stats_sem:
        dict_sem[s[0]] = float(s[1])
    
    datos_semanales = list(dict_sem.values())

    return render_template('ingresos.html', 
                           ingresos=ingresos, 
                           total_mes=total_mes,
                           mes_actual=mes_seleccionado, 
                           meses=meses_es,
                           labels_cat=labels_cat,
                           values_cat=values_cat,
                           datos_semanales=datos_semanales)

@ingresos_bp.route('/eliminar_ingreso/<int:id>', methods=['DELETE'])
@login_required
def eliminar_ingreso(id):
    try:
        # Verificamos propiedad antes de borrar
        ingreso = Ingreso.query.filter_by(id=id, user_id=current_user.id).first()
        if ingreso:
            db.session.delete(ingreso)
            db.session.commit()
            return '', 204
        return jsonify({"error": "No encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500