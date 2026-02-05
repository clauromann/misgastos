from flask import Flask
from .database.models import db
import os
from .routes.gastos import inicializar_categorias
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/static', 
                template_folder='../frontend/templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///misgastos.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate=Migrate(app, db)

    with app.app_context():
        from .routes.main import main_bp
        from .routes.ingresos import ingresos_bp
        from .routes.gastos import gastos_bp  # Asegúrate de que esto no esté comentado
        from .routes.ahorros import ahorros_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(ingresos_bp)
        app.register_blueprint(gastos_bp)  # Registro vital para que funcione el menú
        app.register_blueprint(ahorros_bp)

        if not os.path.exists('sqlite:///misgastos.db'):
            db.create_all()
        inicializar_categorias()  # Asegúrate de que esta función esté definida en gastos.py

    return app