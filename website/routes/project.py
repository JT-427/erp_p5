from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
import datetime as dt
import pandas as pd

from ..modules import ProjectC
from ..modules.decorator import check_authority

project = Blueprint('project', __name__)

@project.route("/", methods=['GET'])
@login_required
@check_authority
def index():
    if 'mode' in request.args and request.args['mode']=='all':
        date = ''
        mode = 'all'
    else:
        date = dt.date.today()
        mode = 'default'
    project = ProjectC()
    projects = project.get_all_project(date)
    return render_template(
        'project/index.html', 
        projects=projects, 
        mode=mode, 
        admin='admin' in [role.role_name for role in current_user.user_roles.all()], 
        user=current_user
    )


@project.route("/details/<project_id>", methods=['GET', 'POST'])
@login_required
@check_authority
def details(project_id):
    project_ = ProjectC(project_id)
    if request.method == "POST":
        file = request.files['import_file']
        file = pd.read_csv(
            file, 
            dtype={
                '項目': str,
                '單位': str,
                '數量': float,
                '單價': float
            }
        )
        file.columns = ['description', 'unit', 'quantity', 'unit_price']
        file['price'] = file['quantity'] * file['unit_price']
        for i in file.to_dict('index').values():
            project_.modify_details(**i)
        return redirect(url_for('project.details', project_id=project_id))
    info = project_.get_info()
    details_ = project_.get_details()
    total_ = sum([i.price for i in details_])
    discount_ = (total_*1.05 if info.invoice else total_) - info['account_receivable']

    payment_records = project_.get_payment()
    total_payment = sum([i.amount for i in payment_records])
        
    return render_template(
        'project/details.html', 
        project=info, 
        details=details_, 
        total=total_, 
        discount=discount_,
        payment_records=payment_records,
        total_payment=total_payment,
        admin='admin' in [role.role_name for role in current_user.user_roles.all()], 
        user=current_user
    )

@project.route("/dispatches/<project_id>", methods=['GET'])
@login_required
@check_authority
def dispatches(project_id):
    project_ = ProjectC(project_id)
    dispatches_ = project_.get_all_dispatches()
    return render_template('project/dispatches.html', project=project_.get_info(), dispatches=dispatches_, user=current_user)

@project.route("/outsourced/<project_id>", methods=['GET'])
@login_required
@check_authority
def outsourced(project_id):
    project_ = ProjectC(project_id)
    records = project_.get_outsourced()
    return render_template(
        'project/outsourced.html', 
        project=project_.get_info(), 
        records=records, 
        # admin='admin' in [role.role_name for role in current_user.user_roles.all()], 
        user=current_user
    )