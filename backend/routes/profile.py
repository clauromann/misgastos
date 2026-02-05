from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from ..database.models import db, User, Gasto, Ingreso, Ahorro, Hucha, CategoriaGasto, SubcategoriaGasto

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_username':
            new_username = request.form.get('username').strip()
            if new_username and new_username != current_user.username:
                if User.query.filter_by(username=new_username).first():
                    flash('Ese nombre ya está en uso', 'danger')
                else:
                    current_user.username = new_username
                    db.session.commit()
                    flash('Nombre actualizado', 'success')
        
        elif action == 'update_password':
            if current_user.check_password(request.form.get('old_password')):
                current_user.set_password(request.form.get('new_password'))
                db.session.commit()
                flash('Contraseña actualizada', 'success')
            else:
                flash('La contraseña actual es incorrecta', 'danger')
                
        return redirect(url_for('profile.view_profile'))

    return render_template('auth/profile.html')

@profile_bp.route('/profile/delete', methods=['GET'])
@login_required
def delete_account():
    user = current_user
    uid = user.id
    
    # 1. Borramos todos sus datos asociados
    Gasto.query.filter_by(user_id=uid).delete()
    Ingreso.query.filter_by(user_id=uid).delete()
    Ahorro.query.filter_by(user_id=uid).delete()
    Hucha.query.filter_by(user_id=uid).delete()
    SubcategoriaGasto.query.filter_by(user_id=uid).delete()
    CategoriaGasto.query.filter_by(user_id=uid).delete()
    
    # 2. Borramos el usuario y cerramos sesión
    db.session.delete(user)
    db.session.commit()
    logout_user()
    
    flash('Tu cuenta y todos tus datos han sido eliminados.', 'success')
    return redirect(url_for('main.index'))