from flask import Blueprint, render_template, request
from ..database.models import db, Ingreso, Gasto, Ahorro
from ..utils import obtener_datos_anuales
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual_nombre = meses[datetime.now().month - 1]
    mes_seleccionado = request.args.get('mes', mes_actual_nombre)
    mes_num = meses.index(mes_seleccionado) + 1

    # --- DATOS DEL MES ---
    ing_mes = db.session.query(db.func.sum(Ingreso.cantidad)).filter(Ingreso.mes == mes_seleccionado).scalar() or 0
    gas_mes = db.session.query(db.func.sum(Gasto.cantidad)).filter(db.func.extract('month', Gasto.fecha) == mes_num).scalar() or 0

    # --- BALANCE AÑO (Acumulado Real) ---
    total_ing_año = db.session.query(db.func.sum(Ingreso.cantidad)).scalar() or 0
    total_gas_año = db.session.query(db.func.sum(Gasto.cantidad)).scalar() or 0
    balance_año = total_ing_año - total_gas_año

    # --- RESUMEN CATEGORÍAS DEL MES ---
    gastos_por_cat = db.session.query(
        Gasto.categoria, db.func.sum(Gasto.cantidad)
    ).filter(db.func.extract('month', Gasto.fecha) == mes_num).group_by(Gasto.categoria).all()
    # Preparamos los datos para el gráfico de tarta
    nombres_cat = [c[0] for c in gastos_por_cat]
    totales_cat = [c[1] for c in gastos_por_cat]

    # --- OTROS ---
    total_ahorros = db.session.query(db.func.sum(Ahorro.cantidad)).scalar() or 0
    datos_anuales = obtener_datos_anuales()

    return render_template('home.html', 
                           mes=mes_seleccionado, 
                           ingresos=ing_mes, 
                           gastos=gas_mes, 
                           balance=ing_mes - gas_mes,
                           balance_anual=balance_año,
                           ahorros=total_ahorros,
                           datos_anuales=datos_anuales,
                           categorias=gastos_por_cat,
                           labels_cat=nombres_cat,
                           values_cat=totales_cat)