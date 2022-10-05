from flask_restful import Resource, reqparse
from flask import request

from ..modules import MatarialC

matarial_transfer_put_args = reqparse.RequestParser()
matarial_transfer_put_args.add_argument("storehouse_id_from", type=str, required=True)
matarial_transfer_put_args.add_argument("storehouse_id_to", type=str, required=True)
matarial_transfer_put_args.add_argument("quantity", type=float, required=True)


class MatarialTransferAPI(Resource):
    def get(self, matarial_id):
        args = request.args
        
        matarial = MatarialC(matarial_id)
        records = matarial.get_matarials(sn=args['sn'])
        return records, 200

    def put(self, matarial_id):
        args = matarial_transfer_put_args.parse_args()

        matarial = MatarialC(matarial_id)
        matarial.modify_transfer_record(**args)
        return '', 201
        
