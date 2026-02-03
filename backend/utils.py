from .database.models import Ingreso, Gasto, db
from sqlalchemy import func
from datetime import datetime

def obtener_resumen_mes(nombre_mes):
    # Sumar ingresos de este mes
    total_ingresos = db.session.query(func.sum(Ingreso.cantidad)).filter(Ingreso.mes == nombre_mes).scalar() or 0.0
    
    # Sumar gastos de este mes (basado en la fecha)
    # Nota: Simplificamos buscando gastos del mes actual del año en curso
    mes_num = datetime.now().month 
    total_gastos = db.session.query(func.sum(Gasto.cantidad)).filter(func.extract('month', Gasto.fecha) == mes_num).scalar() or 0.0
    
    return {
        'ingresos': round(total_ingresos, 2),
        'gastos': round(total_gastos, 2),
        'balance': round(total_ingresos - total_gastos, 2)
    }

def obtener_datos_anuales():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    datos_grafico = {"labels": meses, "ingresos": [], "gastos": []}
    
    for i, nombre_mes in enumerate(meses):
        # Ingresos del mes
        ing = db.session.query(func.sum(Ingreso.cantidad)).filter(Ingreso.mes == nombre_mes).scalar() or 0
        # Gastos del mes (i+1 porque Enero es mes 1)
        gas = db.session.query(func.sum(Gasto.cantidad)).filter(func.extract('month', Gasto.fecha) == i+1).scalar() or 0
        
        datos_grafico["ingresos"].append(ing)
        datos_grafico["gastos"].append(gas)
        
    return datos_grafico