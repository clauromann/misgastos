from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..database.models import db, User
from werkzeug.security import check_password_hash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == 'POST':
        action = request.form.get('action')
        
        # --- CAMBIAR NOMBRE DE USUARIO ---
        if action == 'update_username':
            new_username = request.form.get('username').strip()
            if new_username and new_username != current_user.username:
                # Verificar que el nombre no esté pillado
                exists = User.query.filter_by(username=new_username).first()
                if exists:
                    flash('Ese nombre de usuario ya existe.', 'danger')
                else:
                    current_user.username = new_username
                    db.session.commit()
                    flash('¡Nombre de usuario actualizado!', 'success')
        
        # --- CAMBIAR CONTRASEÑA ---
        elif action == 'update_password':
            old_pass = request.form.get('old_password')
            new_pass = request.form.get('new_password')
            
            if current_user.check_password(old_pass):
                current_user.set_password(new_pass)
                db.session.commit()
                flash('Contraseña cambiada correctamente.', 'success')
            else:
                flash('La contraseña actual no es correcta.', 'danger')
                
        return redirect(url_for('profile.view_profile'))

    return render_template('auth/profile.html')