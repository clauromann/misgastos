from flask import Blueprint, render_template, request, redirect, url_for
from ..database.models import db, Ingreso, Gasto, Ahorro
from datetime import datetime
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Si el usuario ya inició sesión, lo mandamos directo al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    # Si no, ve la Landing Page de Vidda
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required # <--- Esto protege la ruta: si no estás logueado, te manda al login
def dashboard():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual_nombre = meses[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_actual_nombre)

    # --- FILTRADO POR USUARIO (Importante para la privacidad) ---
    uid = current_user.id

    # 1. Datos del mes seleccionado
    ing_mes = db.session.query(db.func.sum(Ingreso.cantidad)).filter(
        Ingreso.mes == mes_seleccionado, Ingreso.user_id == uid
    ).scalar() or 0
    
    gas_mes = db.session.query(db.func.sum(Gasto.cantidad)).filter(
        Gasto.mes == mes_seleccionado, Gasto.user_id == uid
    ).scalar() or 0
    
    disponible_mes = float(ing_mes) - float(gas_mes)

    # 2. Datos Anuales
    total_ing_año = db.session.query(db.func.sum(Ingreso.cantidad)).filter(Ingreso.user_id == uid).scalar() or 0
    total_gas_año = db.session.query(db.func.sum(Gasto.cantidad)).filter(Gasto.user_id == uid).scalar() or 0
    balance_año = float(total_ing_año) - float(total_gas_año)
    total_ahorros = db.session.query(db.func.sum(Ahorro.cantidad)).filter(Ahorro.user_id == uid).scalar() or 0

    # 3. Evolución mensual
    lineas = {"ingresos": [], "gastos": [], "ahorros": []}
    for m in meses:
        i = db.session.query(db.func.sum(Ingreso.cantidad)).filter(Ingreso.mes == m, Ingreso.user_id == uid).scalar() or 0
        g = db.session.query(db.func.sum(Gasto.cantidad)).filter(Gasto.mes == m, Gasto.user_id == uid).scalar() or 0
        a = db.session.query(db.func.sum(Ahorro.cantidad)).filter(Ahorro.mes == m, Ahorro.user_id == uid).scalar() or 0
        lineas["ingresos"].append(float(i))
        lineas["gastos"].append(float(g))
        lineas["ahorros"].append(float(a))

    # 4. Distribución de gastos
    gastos_anuales_cat = db.session.query(
        Gasto.categoria, db.func.sum(Gasto.cantidad)
    ).filter(Gasto.user_id == uid).group_by(Gasto.categoria).all()
    
    labels_pie = [c[0] for c in gastos_anuales_cat]
    values_pie = [float(c[1]) for c in gastos_anuales_cat]

    return render_template('home.html', 
                           meses=meses,
                           mes_sel=mes_seleccionado,
                           ing_mes=float(ing_mes),
                           gas_mes=float(gas_mes),
                           disponible_mes=disponible_mes,
                           balance_año=balance_año,
                           total_ahorros=total_ahorros,
                           lineas=lineas,
                           labels_pie=labels_pie,
                           values_pie=values_pie)