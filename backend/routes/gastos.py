from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Gasto, CategoriaGasto, SubcategoriaGasto
from datetime import datetime
from flask_login import login_required, current_user #

gastos_bp = Blueprint('gastos', __name__)

@gastos_bp.route('/gastos')
@login_required #
def lista_gastos():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = request.args.get('mes', meses_es[datetime.now().month - 1])
    uid = current_user.id #
    
    # Obtener gastos del mes del usuario
    gastos_mes = Gasto.query.filter_by(mes=mes_actual, user_id=uid).order_by(Gasto.fecha.desc()).all()
    total_mes = sum(g.cantidad for g in gastos_mes)

    # 1. Lógica de Evolución Semanal
    data_sem = [0, 0, 0, 0, 0]
    for g in gastos_mes:
        indice = min(max(g.semana - 1, 0), 4) 
        data_sem[indice] += float(g.cantidad)

    # 2. Datos para gráfico de Reparto filtrado por usuario
    stats_cat_raw = db.session.query(
        Gasto.categoria, 
        db.func.sum(Gasto.cantidad)
    ).filter(Gasto.mes == mes_actual, Gasto.user_id == uid).group_by(Gasto.categoria).all()

    labels_cat = [c[0] for c in stats_cat_raw]
    values_cat = [float(c[1]) for c in stats_cat_raw]

    # 3. Datos para gráficos Mini (Subcategorías del usuario)
    stats_sub = {}
    for cat_nombre in labels_cat:
        gastos_sub_raw = db.session.query(
            Gasto.subcategoria, 
            db.func.sum(Gasto.cantidad)
        ).filter(
            Gasto.mes == mes_actual, 
            Gasto.categoria == cat_nombre,
            Gasto.user_id == uid
        ).group_by(Gasto.subcategoria).all()
        
        stats_sub[cat_nombre] = {
            "subcategorias": {s[0]: float(s[1]) for s in gastos_sub_raw}
        }

    return render_template('gastos.html', 
                           gastos=gastos_mes, 
                           total_mes=total_mes,
                           mes_actual=mes_actual,
                           meses=meses_es,
                           categorias=CategoriaGasto.query.filter_by(user_id=uid).all(), #
                           data_sem=data_sem,
                           labels_cat=labels_cat,
                           values_cat=values_cat,
                           stats_sub=stats_sub)

@gastos_bp.route('/nuevo_gasto', methods=['POST'])
@login_required
def nuevo_gasto():
    concepto = request.form.get('concepto')
    cantidad = float(request.form.get('cantidad', 0))
    fecha_str = request.form.get('fecha')
    categoria = request.form.get('categoria')
    subcategoria = request.form.get('subcategoria')
    
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_nombre = meses_es[fecha.month - 1]
    semana_manual = int(request.form.get('semana'))

    nuevo = Gasto(
        concepto=concepto, 
        cantidad=cantidad, 
        fecha=fecha, 
        mes=mes_nombre, 
        categoria=categoria, 
        semana=semana_manual,
        subcategoria=subcategoria,
        user_id=current_user.id # Vinculamos al usuario actual
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('gastos.lista_gastos', mes=mes_nombre))

@gastos_bp.route('/eliminar_gasto/<int:id>', methods=['DELETE'])
@login_required
def eliminar_gasto(id):
    # Solo puede eliminar sus propios gastos
    gasto = Gasto.query.filter_by(id=id, user_id=current_user.id).first()
    if gasto:
        db.session.delete(gasto)
        db.session.commit()
        return '', 204
    return jsonify({"error": "No encontrado"}), 404

@gastos_bp.route('/api/subcategorias/<int:categoria_id>')
@login_required
def get_subcategorias(categoria_id):
    # Solo subcategorías del usuario
    subs = SubcategoriaGasto.query.filter_by(categoria_id=categoria_id, user_id=current_user.id).all()
    return jsonify([{"id": s.id, "nombre": s.nombre} for s in subs])

@gastos_bp.route('/gastos/nueva_categoria', methods=['POST'])
@login_required
def nueva_categoria():
    nombre = request.form.get('nombre')
    if nombre:
        nueva = CategoriaGasto(nombre=nombre, user_id=current_user.id)
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('gastos.lista_gastos'))

@gastos_bp.route('/gastos/nueva_subcategoria', methods=['POST'])
@login_required
def nueva_subcategoria():
    nombre = request.form.get('nombre_sub')
    cat_id = request.form.get('categoria_padre_id')
    if nombre and cat_id:
        nueva = SubcategoriaGasto(nombre=nombre, categoria_id=cat_id, user_id=current_user.id)
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('gastos.lista_gastos'))

@gastos_bp.route('/gastos/eliminar_categoria/<int:id>', methods=['DELETE'])
@login_required
def eliminar_categoria(id):
    # Buscamos la categoría asegurándonos de que sea del usuario logueado
    categoria = CategoriaGasto.query.filter_by(id=id, user_id=current_user.id).first()
    
    if categoria:
        try:
            # Al tener cascade="all, delete-orphan" en el modelo, 
            # SQLAlchemy borrará automáticamente las subcategorías.
            # Pero los Gastos no se borran solos porque no tienen relación directa con el ID de categoría.
            # Limpiamos los gastos que usen este nombre de categoría para evitar errores de integridad.
            Gasto.query.filter_by(categoria=categoria.nombre, user_id=current_user.id).delete()
            
            db.session.delete(categoria)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Categoría no encontrada"}), 404

@gastos_bp.route('/gastos/eliminar_subcategoria/<int:id>', methods=['DELETE'])
@login_required
def eliminar_subcategoria(id):
    # Verificamos que la subcategoría pertenezca al usuario
    sub = SubcategoriaGasto.query.filter_by(id=id, user_id=current_user.id).first()
    
    if sub:
        try:
            db.session.delete(sub)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Subcategoría no encontrada"}), 404