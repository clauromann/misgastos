from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Ahorro, Hucha
from datetime import datetime

ahorros_bp = Blueprint('ahorros', __name__)

@ahorros_bp.route('/ahorros', methods=['GET', 'POST'])
def lista_ahorros():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # 1. Determinar el mes actual o el seleccionado
    mes_hoy = meses_es[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_hoy)

    if request.method == 'POST':
        # CASO CREAR HUCHA
        if 'nombre_hucha' in request.form:
            nombre = request.form.get('nombre_hucha').strip()
            if nombre:
                nueva_hucha = Hucha(nombre=nombre)
                db.session.add(nueva_hucha)
                db.session.commit()
            return redirect(url_for('ahorros.lista_ahorros', mes=mes_seleccionado))

        # CASO REGISTRAR AHORRO
        else:
            fecha_str = request.form.get('fecha')
            fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
            mes_registro = meses_es[fecha_dt.month - 1]
            
            nuevo_ahorro = Ahorro(
                concepto=request.form.get('concepto'),
                cantidad=float(request.form.get('cantidad')),
                categoria=request.form.get('categoria'),
                fecha=fecha_dt,
                mes=mes_registro
            )
            db.session.add(nuevo_ahorro)
            db.session.commit()
            # Redirigimos al mes donde el usuario ha metido el dato
            return redirect(url_for('ahorros.lista_ahorros', mes=mes_registro))

    # --- LÓGICA DE VISUALIZACIÓN ---

    # 2. Obtener huchas y calcular total SOLO del mes seleccionado
    huchas_db = Hucha.query.all()
    totales_huchas = []
    for h in huchas_db:
        # AQUÍ ESTÁ EL CAMBIO: Filtramos la suma por mes=mes_seleccionado
        total_mes = db.session.query(db.func.sum(Ahorro.cantidad))\
            .filter(Ahorro.categoria == h.nombre)\
            .filter(Ahorro.mes == mes_seleccionado)\
            .scalar() or 0
        
        totales_huchas.append({
            'id': h.id,
            'nombre': h.nombre,
            'total': total_mes
        })

    # 3. Historial del mes seleccionado
    ahorros_mes = Ahorro.query.filter_by(mes=mes_seleccionado).order_by(Ahorro.fecha.desc()).all()

    return render_template('ahorros.html', 
                           ahorros=ahorros_mes, 
                           huchas=totales_huchas, 
                           mes_actual=mes_seleccionado, 
                           meses=meses_es,
                           hoy=datetime.now().strftime('%Y-%m-%d'))

@ahorros_bp.route('/eliminar_hucha/<int:id>', methods=['DELETE'])
def eliminar_hucha(id):
    hucha = db.session.get(Hucha, id)
    if hucha:
        # Al borrar la hucha, borramos sus registros para no dejar basura
        Ahorro.query.filter_by(categoria=hucha.nombre).delete()
        db.session.delete(hucha)
        db.session.commit()
        return '', 204
    return '', 404

@ahorros_bp.route('/eliminar_ahorro/<int:id>', methods=['DELETE'])
def eliminar_ahorro(id):
    a = db.session.get(Ahorro, id)
    if a:
        db.session.delete(a)
        db.session.commit()
        return '', 204
    return '', 404