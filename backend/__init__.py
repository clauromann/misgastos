from flask import Flask, app
import os
from dotenv import load_dotenv
from .database.models import db # Importamos db y modelos

load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates', 
                static_folder='../frontend/static')
    
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///misgastos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    db.init_app(app)

    with app.app_context():
        db.create_all() # Esto crea el archivo .db automáticamente

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.ahorros import ahorros_bp
    app.register_blueprint(ahorros_bp)

    from .routes.ingresos import ingresos_bp
    app.register_blueprint(ingresos_bp)

    from .routes.gastos import gastos_bp
    app.register_blueprint(gastos_bp)

    return app