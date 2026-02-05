from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Ahorro, Hucha
from datetime import datetime
from flask_login import login_required, current_user #

ahorros_bp = Blueprint('ahorros', __name__)

@ahorros_bp.route('/ahorros', methods=['GET', 'POST'])
@login_required #
def lista_ahorros():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    mes_hoy = meses_es[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_hoy)
    uid = current_user.id #

    if request.method == 'POST':
        if 'nombre_hucha' in request.form:
            nombre = request.form.get('nombre_hucha').strip()
            if nombre:
                # Añadimos el user_id al crear la hucha
                nueva_hucha = Hucha(nombre=nombre, user_id=uid)
                db.session.add(nueva_hucha)
                db.session.commit()
            return redirect(url_for('ahorros.lista_ahorros', mes=mes_seleccionado))

        else:
            fecha_str = request.form.get('fecha')
            fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
            mes_registro = meses_es[fecha_dt.month - 1]
            
            # Añadimos el user_id al registrar ahorro
            nuevo_ahorro = Ahorro(
                concepto=request.form.get('concepto'),
                cantidad=float(request.form.get('cantidad')),
                categoria=request.form.get('categoria'),
                fecha=fecha_dt,
                mes=mes_registro,
                user_id=uid
            )
            db.session.add(nuevo_ahorro)
            db.session.commit()
            return redirect(url_for('ahorros.lista_ahorros', mes=mes_registro))

    # Filtramos huchas por usuario
    huchas_db = Hucha.query.filter_by(user_id=uid).all()
    totales_huchas = []
    for h in huchas_db:
        # Filtramos la suma por categoría, mes y USUARIO
        total_mes = db.session.query(db.func.sum(Ahorro.cantidad))\
            .filter(Ahorro.categoria == h.nombre)\
            .filter(Ahorro.mes == mes_seleccionado)\
            .filter(Ahorro.user_id == uid)\
            .scalar() or 0
        
        totales_huchas.append({
            'id': h.id,
            'nombre': h.nombre,
            'total': total_mes
        })

    # Historial filtrado por usuario
    ahorros_mes = Ahorro.query.filter_by(mes=mes_seleccionado, user_id=uid).order_by(Ahorro.fecha.desc()).all()

    return render_template('ahorros.html', 
                           ahorros=ahorros_mes, 
                           huchas=totales_huchas, 
                           mes_actual=mes_seleccionado, 
                           meses=meses_es,
                           hoy=datetime.now().strftime('%Y-%m-%d'))

@ahorros_bp.route('/eliminar_hucha/<int:id>', methods=['DELETE'])
@login_required
def eliminar_hucha(id):
    # Verificamos que la hucha pertenezca al usuario
    hucha = Hucha.query.filter_by(id=id, user_id=current_user.id).first()
    if hucha:
        Ahorro.query.filter_by(categoria=hucha.nombre, user_id=current_user.id).delete()
        db.session.delete(hucha)
        db.session.commit()
        return '', 204
    return '', 404

@ahorros_bp.route('/eliminar_ahorro/<int:id>', methods=['DELETE'])
@login_required
def eliminar_ahorro(id):
    # Verificamos que el ahorro sea del usuario
    a = Ahorro.query.filter_by(id=id, user_id=current_user.id).first()
    if a:
        db.session.delete(a)
        db.session.commit()
        return '', 204
    return '', 404