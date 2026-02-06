from backend import create_app
from backend.database.models import db # Importamos la base de datos
import os
import psycopg2

app = create_app()

# Configuración de la base de datos (la dejamos como la tenías)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///misgastos.db')

if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

if __name__ == "__main__":
    # --- ESTO ES LO QUE CREA LAS TABLAS ---
    with app.app_context():
        db.create_all() 
    # --------------------------------------
    app.run(debug=True)