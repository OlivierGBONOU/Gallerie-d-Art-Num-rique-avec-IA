# app/utils/decorators.py
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Vous devez être administrateur pour accéder à cette page.", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function