from datetime import timedelta
from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..modules.database.flask_sqlalchemy_model import Users

auth = Blueprint('auth', __name__)

@auth.route("/", methods=['GET', 'POST'])
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user = current_user
        if user.is_authenticated:
            roles = [role.role_name for role in user.user_roles.all()]
            if 'admin' in roles:
                return redirect(url_for('project.index'))
            elif '一般員工' in roles:
                return redirect(url_for('employee_report.index'))
            elif '管理庫存' in roles:
                return redirect(url_for('storehouse.index'))
            elif '管理雜支' in roles:
                return redirect(url_for('miscellaneous_expenditure.index'))
            else:
                # 其他權限
                return redirect(url_for('auth.logout'))
        else:
            return render_template('auth/login.html')
    elif request.method == 'POST':
        args = request.json
        account = args['account']
        password = args['password']
        user = Users.query.filter_by(user_id=account).first()
        if user:
            if user.password:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True, duration=timedelta(days=7))
                    roles = [role.role_name for role in user.user_roles.all()]
                    
                    if 'admin' in roles:
                        return '/project', 308
                    elif 'general employee' in roles:
                        return '/employeeReport', 308
                    else:
                        # 其他權限
                        return '/', 401
                else:
                    return '密碼錯誤', 403
            else:
                return '/sign-up', 308
        else:
            return '/sign-up', 308

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/sign_up.html')
    elif request.method == 'POST':
        args = request.json
        account = args['account']
        password = args['password']
        user = db.session.query(
            Users
        ).filter(
            Users.user_id == account
        ).first()
        if user and not user.password:
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
            return '/login', 308
        else:
            return '沒有權限', 401