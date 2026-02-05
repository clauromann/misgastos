from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..database.models import db, User, CategoriaGasto
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Comprobar si el usuario ya existe
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('El nombre de usuario ya está pillado. Prueba otro.', 'danger')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario
        new_user = User(username=username)
        new_user.set_password(password) # Esto usa el hash que configuramos en models

        db.session.add(new_user)
        db.session.commit()

        # --- OPCIONAL: Crear categorías por defecto para el nuevo usuario ---
        categorias_iniciales = ['Comida', 'Transporte', 'Ocio', 'Hogar', 'Salud']
        for cat_nombre in categorias_iniciales:
            nueva_cat = CategoriaGasto(nombre=cat_nombre, user_id=new_user.id)
            db.session.add(nueva_cat)
        db.session.commit()

        flash('¡Cuenta creada con éxito! Ya puedes entrar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index')) # Cambia 'main.index' por tu ruta principal
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))