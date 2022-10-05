import json
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from ..modules.decorator import check_authority

from ..modules import MatarialC, StorehouseC

matarial = Blueprint('matarial', __name__)

@matarial.route("/", methods=['GET'])
@login_required
@check_authority
def index():
    args = {}
    if 'storehouse_id' in request.args:
        args['storehouse_id'] = request.args['storehouse_id']
    
    matarial_c = MatarialC()
    matarials = matarial_c.get_matarials(**args)
    storehouse = StorehouseC(args['storehouse_id'])
    storehouse = storehouse.get_storehouse()
    return render_template('matarial/index.html', matarials=matarials, storehouse=storehouse, user=current_user)


@matarial.route("/buying", methods=['GET'])
@login_required
@check_authority
def buying():
    matarial_id = request.args['matarial_id']
    storehouse_id = request.args['storehouse_id']

    matarial = MatarialC(matarial_id)
    records = matarial.get_buying_record(storehouse_id=storehouse_id)
    storehouse = StorehouseC(storehouse_id)
    storehouse = storehouse.get_storehouse()
    return render_template('matarial/buying.html', matarial=matarial.get_info(storehouse_id), storehouse=storehouse, records=records, user=current_user)

@matarial.route("/using", methods=['GET'])
@login_required
@check_authority
def using():
    matarial_id = request.args['matarial_id']
    storehouse_id = request.args['storehouse_id']

    matarial = MatarialC(matarial_id)
    records = matarial.get_using_record(storehouse_id=storehouse_id)
    storehouse = StorehouseC(storehouse_id)
    storehouse = storehouse.get_storehouse()
    return render_template('matarial/using.html', matarial=matarial.get_info(storehouse_id), storehouse=storehouse, records=records, user=current_user)

@matarial.route("/transfer", methods=['GET'])
@login_required
@check_authority
def transfer():
    matarial_id = request.args['matarial_id']
    matarial = MatarialC(matarial_id)
    records = matarial.get_transfer_record()
    return render_template('matarial/transfer.html', matarial=matarial.get_info(), records=records, user=current_user)