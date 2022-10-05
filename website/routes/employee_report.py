from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import datetime as dt

from ..modules import EmployeeC
from ..modules.decorator import check_authority

employeeReport = Blueprint('employee_report', __name__)

@employeeReport.route("/", methods=['GET'])
@login_required
# @check_authority
def index():
    return render_template('employee_report/index.html', user=current_user)

@employeeReport.route("/records", methods=['GET'])
@login_required
# @check_authority
def records():
    employee = EmployeeC(current_user.employee_id)
    records = employee.get_dispatches()
    return render_template('employee_report/records.html', records=records, user=current_user)