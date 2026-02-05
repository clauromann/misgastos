import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-por-defecto-muy-debil'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False