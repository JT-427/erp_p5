from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

import datetime as dt

from ..modules import StorehouseC
from ..modules.decorator import check_authority

storehouse = Blueprint('storehouse', __name__)

@storehouse.route('/', methods=['GET'])
@login_required
@check_authority
def index():
    if 'mode' in request.args and request.args['mode']=='all':
        date = ''
        mode = 'all'
    else:
        date = dt.date.today()
        mode = 'default'
    storehouses = StorehouseC().get_all_storehouse(date)
    return render_template(
        'storehouse/index.html', 
        storehouses=storehouses, 
        mode=mode, 
        admin='admin' in [role.role_name for role in current_user.user_roles.all()], 
        user=current_user
    )