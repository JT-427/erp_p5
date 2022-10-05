from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from flask import flash

def check_authority(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user._get_current_object().check_authority(func.__module__, func.__name__):
            # flash('Good Job')
            return func(*args, **kwargs)
        else:
            flash('沒有權限')
            return redirect(url_for('auth.login'))
    return inner