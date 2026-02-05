import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from .database.models import db, User


def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/static', 
                template_folder='../frontend/templates')
    
    # Cargamos toda la configuración desde config.py (incluyendo DATABASE_URL y SECRET_KEY)
    app.config.from_object(Config)

    # Inicializamos la base de datos y las migraciones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración del sistema de Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Indica a dónde redirigir si no hay sesión
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Esta función permite a Flask-Login recuperar el objeto usuario por su ID
        return User.query.get(int(user_id))

    # Importamos y registramos los Blueprints
    from .routes.main import main_bp
    from .routes.ingresos import ingresos_bp
    from .routes.gastos import gastos_bp
    from .routes.ahorros import ahorros_bp
    from .routes.auth import auth_bp  
    from .routes.profile import profile_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(ingresos_bp)
    app.register_blueprint(gastos_bp)
    app.register_blueprint(ahorros_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    
    return app