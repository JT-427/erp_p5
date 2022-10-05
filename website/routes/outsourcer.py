from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..modules import OutsourcerC
from ..modules.decorator import check_authority

outsourcer = Blueprint('outsourcer', __name__)

@outsourcer.route('/', methods=['GET'])
@login_required
@check_authority
def index():
    outsourcers = OutsourcerC()
    outsourcers = outsourcers.get_outsourcers()
    return render_template('outsourcer/index.html', outsourcers=outsourcers, user=current_user)