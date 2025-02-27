from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required, current_user

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and any(current_user.role == role for role in roles):
                return func(*args, **kwargs)
            flash("You do not have the required permissions.", "danger")
            return redirect(url_for('login'))
        return wrapper
    return decorator