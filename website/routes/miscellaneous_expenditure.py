from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..modules import MiscellaneousExpenditureC
from ..modules.decorator import check_authority

miscellaneousExpenditure = Blueprint('miscellaneousExpenditure', __name__)

@miscellaneousExpenditure.route('/', methods=['GET'])
@login_required
@check_authority
def index():
    me = MiscellaneousExpenditureC()
    records = me.get_records()
    return render_template(
        'miscellaneous_expenditure/index.html', 
        records=records, 
        admin='admin' in [role.role_name for role in current_user.user_roles.all()], 
        user=current_user
    )