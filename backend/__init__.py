import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv # Recuerda instalarlo: pip install python-dotenv
from .database.models import db, User

# Cargamos las variables del archivo .env (donde pegarás tu DATABASE_URL de Supabase)
load_dotenv()

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend/static', 
                template_folder='../frontend/templates')
    
    # 1. CONFIGURACIÓN DE LA BASE DE DATOS
    # Intentamos obtener la URL de Supabase desde el entorno
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Truco técnico: Render y Google Cloud a veces pasan 'postgres://'
        # pero SQLAlchemy necesita 'postgresql://' para funcionar.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Si no hay .env o no hay URL, usamos la base de datos local para no romper nada
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///misgastos.db'

    # Configuración de seguridad básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'desarrollo_seguro_vidda_2024')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. INICIALIZACIÓN DE COMPONENTES
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración del sistema de Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 3. REGISTRO DE BLUEPRINTS (Rutas)
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