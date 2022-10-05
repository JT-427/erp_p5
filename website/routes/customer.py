from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..modules import CustomerC
from ..modules.decorator import check_authority

customer = Blueprint('customer', __name__)

@customer.route("/", methods=['GET'])
@login_required
@check_authority
def index():
    customer = CustomerC()
    customers = customer.get_all_customer()
    return render_template('customer/index.html', customers=customers, user=current_user)