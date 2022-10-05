from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import datetime as dt

from ..modules import EmployeeC
from ..modules.decorator import check_authority

employee = Blueprint('employee', __name__)

@employee.route("/", methods=['GET'])
@login_required
@check_authority
def index():
    if 'mode' in request.args and request.args['mode']=='all':
        date = ''
        mode = 'all'
    else:
        date = dt.date.today()
        mode = 'default'
    employee = EmployeeC()
    employees = employee.get_all_employee(date)
    return render_template('employee/index.html', employees=employees, mode=mode, user=current_user)

@employee.route("/salary-record/<employee_id>", methods=['GET'])
@login_required
@check_authority
def salary(employee_id):
    employee = EmployeeC(employee_id)
    records = employee.get_salary_record()
    return render_template('employee/salary.html', employee=employee, records=records, user=current_user)

@employee.route("/dispatch-record/<employee_id>", methods=['GET'])
@login_required
@check_authority
def dispatch(employee_id):
    employee = EmployeeC(employee_id)
    records = employee.get_dispatches()
    return render_template('employee/dispatch.html', employee=employee, records=records, user=current_user)

@employee.route("/hired-record/<employee_id>", methods=['GET'])
@login_required
@check_authority
def hired(employee_id):
    employee = EmployeeC(employee_id)
    records = employee.get_hired_record()
    return render_template('employee/hired.html', employee=employee, records=records, user=current_user)

@employee.route("/payment-record/<employee_id>", methods=['GET'])
@login_required
# @check_authority
def payment(employee_id):
    employee = EmployeeC(employee_id)
    records = employee.get_payment_record()
    return render_template('employee/payment.html', employee=employee, records=records, user=current_user)