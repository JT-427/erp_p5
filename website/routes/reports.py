from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy.sql import func
import datetime as dt
import calendar

from .. import db
from ..modules.decorator import check_authority
from ..modules import ReportsC
from ..modules.database.flask_sqlalchemy_model import MiscellaneousExpenditure

reports = Blueprint('reports', __name__)

@reports.route("/monthly_terminated_projects", methods=['GET'])
@login_required
@check_authority
def monthly_terminated_projects():
    reports_c = ReportsC()
    if 'year' in request.args and 'month' in request.args:
        year = int(request.args['year'])
        month = int(request.args['month'])
    else:
        today_ = dt.date.today()
        year = today_.year
        month = today_.month
    this_report = reports_c.monthly_terminated_projects(year, month)

    me = db.session.query(
        func.sum(MiscellaneousExpenditure.price)
    ).filter(
        MiscellaneousExpenditure.project_id == None,
        MiscellaneousExpenditure.date >= dt.date(year, month, 1),
        MiscellaneousExpenditure.date <= dt.date(year, month, calendar.monthrange(year, month)[1])
    ).first()[0]
    net_income = sum([(report['income'] if report['income'] else 0) - (report['cost'] if report['cost'] else 0) for report in this_report])
    return render_template('reports/monthly_terminated_projects.html', reports=this_report, net_income=net_income, me=me, user=current_user)