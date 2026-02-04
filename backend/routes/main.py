from flask import Blueprint, render_template, request
from ..database.models import db, Ingreso, Gasto, Ahorro
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual_nombre = meses[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_actual_nombre)

    # 1. Datos del mes seleccionado (Para la caja de arriba)
    ing_mes = db.session.query(db.func.sum(Ingreso.cantidad)).filter(Ingreso.mes == mes_seleccionado).scalar() or 0
    gas_mes = db.session.query(db.func.sum(Gasto.cantidad)).filter(Gasto.mes == mes_seleccionado).scalar() or 0
    disponible_mes = float(ing_mes) - float(gas_mes)

    # 2. Datos Anuales (Para las tarjetas burdeos)
    total_ing_año = db.session.query(db.func.sum(Ingreso.cantidad)).scalar() or 0
    total_gas_año = db.session.query(db.func.sum(Gasto.cantidad)).scalar() or 0
    balance_año = float(total_ing_año) - float(total_gas_año)
    total_ahorros = db.session.query(db.func.sum(Ahorro.cantidad)).scalar() or 0

    # 3. Evolución mensual (Gráfico de líneas)
    lineas = {"ingresos": [], "gastos": [], "ahorros": []}
    for m in meses:
        i = db.session.query(db.func.sum(Ingreso.cantidad)).filter(Ingreso.mes == m).scalar() or 0
        g = db.session.query(db.func.sum(Gasto.cantidad)).filter(Gasto.mes == m).scalar() or 0
        a = db.session.query(db.func.sum(Ahorro.cantidad)).filter(Ahorro.mes == m).scalar() or 0
        lineas["ingresos"].append(float(i))
        lineas["gastos"].append(float(g))
        lineas["ahorros"].append(float(a))

    # 4. Distribución de gastos
    gastos_anuales_cat = db.session.query(
        Gasto.categoria, db.func.sum(Gasto.cantidad)
    ).group_by(Gasto.categoria).all()
    
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
