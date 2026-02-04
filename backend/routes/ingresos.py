from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Ingreso  
from datetime import datetime

ingresos_bp = Blueprint('ingresos', __name__)

@ingresos_bp.route('/ingresos', methods=['GET', 'POST'])
@ingresos_bp.route('/ingresos', methods=['GET', 'POST'])
def gestionar_ingresos():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    mes_hoy = meses_es[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_hoy)

    if request.method == 'POST':
        fecha_str = request.form.get('fecha') # Ejemplo: "2026-02-15"
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        # --- EL ARREGLO ESTÁ AQUÍ ---
        # Extraemos el nombre del mes real de la fecha elegida
        mes_real = meses_es[fecha_dt.month - 1] 
        
        nuevo_ingreso = Ingreso(
            cantidad=float(request.form.get('cantidad')),
            concepto=request.form.get('concepto'),
            categoria=request.form.get('categoria'),
            fecha=fecha_dt,
            semana=int(request.form.get('semana')),
            mes=mes_real  # <--- Ahora guardamos el mes de la fecha, no del filtro
        )
        db.session.add(nuevo_ingreso)
        db.session.commit()
        
        # Redirigimos al usuario al mes donde acaba de guardar el dinero
        return redirect(url_for('ingresos.gestionar_ingresos', mes=mes_real))

    # 1. Obtener ingresos
    ingresos = Ingreso.query.filter_by(mes=mes_seleccionado).order_by(Ingreso.fecha.desc()).all()
    
    # 2. Calcular total del mes
    total_mes = sum(i.cantidad for i in ingresos)

    # 3. Gráfico de Categorías (Donut)
    stats_cat = db.session.query(Ingreso.categoria, db.func.sum(Ingreso.cantidad))\
        .filter_by(mes=mes_seleccionado)\
        .group_by(Ingreso.categoria).all()
    labels_cat = [s[0] for s in stats_cat]
    values_cat = [float(s[1]) for s in stats_cat]

    # 4. Gráfico de Semanas (Líneas) - AQUÍ ESTABA EL ERROR
    stats_sem = db.session.query(Ingreso.semana, db.func.sum(Ingreso.cantidad))\
        .filter_by(mes=mes_seleccionado)\
        .group_by(Ingreso.semana).all()
    
    dict_sem = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for s in stats_sem:
        dict_sem[s[0]] = float(s[1])
    
    datos_semanales = list(dict_sem.values()) # Convertimos a lista [sem1, sem2...]

    # 5. Renderizar con TODAS las variables necesarias
    return render_template('ingresos.html', 
                           ingresos=ingresos, 
                           total_mes=total_mes,
                           mes_actual=mes_seleccionado, 
                           meses=meses_es,
                           labels_cat=labels_cat,
                           values_cat=values_cat,
                           datos_semanales=datos_semanales) # <--- Variable enviada

@ingresos_bp.route('/eliminar_ingreso/<int:id>', methods=['DELETE'])
def eliminar_ingreso(id):
    try:
        ingreso = db.session.get(Ingreso, id)
        if ingreso:
            db.session.delete(ingreso)
            db.session.commit()
            return '', 204
        return jsonify({"error": "No encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500