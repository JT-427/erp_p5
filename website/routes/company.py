from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..modules import CompanyC
from ..modules.decorator import check_authority

company = Blueprint('company', __name__)

@company.route("/", methods=['GET'])
@login_required
@check_authority
def index():
    companies = CompanyC().get_all_company()
    return render_template('company/index.html', companies=companies, user=current_user)