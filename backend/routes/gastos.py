from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..database.models import db, Gasto, CategoriaGasto, SubcategoriaGasto
from datetime import datetime

gastos_bp = Blueprint('gastos', __name__)

@gastos_bp.route('/gastos')
def lista_gastos():
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = request.args.get('mes', meses_es[datetime.now().month - 1])
    
    # Obtener gastos del mes
    gastos_mes = Gasto.query.filter_by(mes=mes_actual).order_by(Gasto.fecha.desc()).all()
    total_mes = sum(g.cantidad for g in gastos_mes)

    # 1. Lógica de Evolución Semanal
    data_sem = [0, 0, 0, 0, 0]
    for g in gastos_mes:
        # Usamos g.semana que es lo que guardamos manualmente
        # Restamos 1 porque las listas en Python empiezan en 0
        indice = min(max(g.semana - 1, 0), 4) 
        data_sem[indice] += float(g.cantidad)

    # 2. Datos para gráfico de Reparto (Categorías Madre)
    stats_cat_raw = db.session.query(
        Gasto.categoria, 
        db.func.sum(Gasto.cantidad)
    ).filter(Gasto.mes == mes_actual).group_by(Gasto.categoria).all()

    labels_cat = [c[0] for c in stats_cat_raw]
    values_cat = [float(c[1]) for c in stats_cat_raw]

    # 3. Datos para gráficos Mini (Subcategorías)
    stats_sub = {}
    for cat_nombre in labels_cat:
        gastos_sub_raw = db.session.query(
            Gasto.subcategoria, 
            db.func.sum(Gasto.cantidad)
        ).filter(
            Gasto.mes == mes_actual, 
            Gasto.categoria == cat_nombre
        ).group_by(Gasto.subcategoria).all()
        
        stats_sub[cat_nombre] = {
            "subcategorias": {s[0]: float(s[1]) for s in gastos_sub_raw}
        }

    return render_template('gastos.html', 
                           gastos=gastos_mes, 
                           total_mes=total_mes,
                           mes_actual=mes_actual,
                           meses=meses_es,
                           categorias=CategoriaGasto.query.all(),
                           data_sem=data_sem,
                           labels_cat=labels_cat,
                           values_cat=values_cat,
                           stats_sub=stats_sub)

@gastos_bp.route('/nuevo_gasto', methods=['POST'])
def nuevo_gasto():
    # Coincide con los names de form_gasto.html
    concepto = request.form.get('concepto')
    cantidad = float(request.form.get('cantidad', 0))
    fecha_str = request.form.get('fecha')
    categoria = request.form.get('categoria') # Aquí llega el NOMBRE de la categoría
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
        subcategoria=subcategoria
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('gastos.lista_gastos', mes=mes_nombre))

@gastos_bp.route('/eliminar_gasto/<int:id>', methods=['DELETE'])
def eliminar_gasto(id):
    gasto = db.session.get(Gasto, id)
    if gasto:
        db.session.delete(gasto)
        db.session.commit()
        return '', 204
    return jsonify({"error": "No encontrado"}), 404

@gastos_bp.route('/api/subcategorias/<int:categoria_id>')
def get_subcategorias(categoria_id):
    subs = SubcategoriaGasto.query.filter_by(categoria_id=categoria_id).all()
    return jsonify([{"id": s.id, "nombre": s.nombre} for s in subs])

# Rutas de administración de categorías
@gastos_bp.route('/gastos/nueva_categoria', methods=['POST'])
def nueva_categoria():
    nombre = request.form.get('nombre')
    if nombre:
        nueva = CategoriaGasto(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('gastos.lista_gastos'))

@gastos_bp.route('/gastos/nueva_subcategoria', methods=['POST'])
def nueva_subcategoria():
    nombre = request.form.get('nombre_sub')
    cat_id = request.form.get('categoria_padre_id')
    if nombre and cat_id:
        nueva = SubcategoriaGasto(nombre=nombre, categoria_id=cat_id)
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('gastos.lista_gastos'))

@gastos_bp.route('/gastos/eliminar_categoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = db.session.get(CategoriaGasto, id)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Categoría no encontrada"}), 404

@gastos_bp.route('/gastos/eliminar_subcategoria/<int:id>', methods=['DELETE'])
def eliminar_subcategoria(id):
    sub = db.session.get(SubcategoriaGasto, id)
    if sub:
        db.session.delete(sub)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Subcategoría no encontrada"}), 404

def inicializar_categorias():
    categorias_excel = {
        "Ocio": ["Restaurantes", "Calle"],
        "Personal": ["Ropa", "Regalos", "Caprichos random", "Gasolina"],
        "Suscripciones": ["Netflix", "Spotify", "Gimnasio"],
        "Vacaciones": ["Transporte", "Estancia", "Comida", "Ocio", "Otros"],
        "Otros": ["Varios"]
    }
    for cat_nombre, subs in categorias_excel.items():
        categoria = CategoriaGasto.query.filter_by(nombre=cat_nombre).first()
        if not categoria:
            categoria = CategoriaGasto(nombre=cat_nombre)
            db.session.add(categoria)
            db.session.commit()
        for sub_nombre in subs:
            if not SubcategoriaGasto.query.filter_by(nombre=sub_nombre, categoria_id=categoria.id).first():
                nueva_sub = SubcategoriaGasto(nombre=sub_nombre, categoria_id=categoria.id)
                db.session.add(nueva_sub)
    db.session.commit()