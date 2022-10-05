from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from ..modules.decorator import check_authority

from ..modules.matraila_suppler import MatarialSupplierC

matarial_supplier = Blueprint('matarial_supplier', __name__)

@matarial_supplier.route('/', methods=['GET'])
@login_required
@check_authority
def index():
    if 'cooperating' in request.args:
        cooperating = True if request.args['cooperating'] == "true" else False
    else:
        cooperating = True
    supplier = MatarialSupplierC()
    suppliers = supplier.get_suppliers(cooperating)
    return render_template('matarial_supplier/index.html', matarial_suppliers=suppliers, cooperating=cooperating, user=current_user)