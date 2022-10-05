from flask_restful import Resource, reqparse
from flask import request

from ..modules import MatarialC

matarial_buying_put_args = reqparse.RequestParser()
matarial_buying_put_args.add_argument("sn", type=str)
matarial_buying_put_args.add_argument("buying_date", type=str, required=True)
matarial_buying_put_args.add_argument("matarial_supplier_id", type=str, required=True)
matarial_buying_put_args.add_argument("storehouse_id", type=str, required=True)
matarial_buying_put_args.add_argument("quantity", type=float, required=True)
matarial_buying_put_args.add_argument("price", type=float, required=True)

matarial_buying_delete_args = reqparse.RequestParser()
matarial_buying_delete_args.add_argument("sn", type=str, required=True)

class MatarialBuyingAPI(Resource):
    def get(self, matarial_id):
        args = request.args
        
        matarial = MatarialC(matarial_id)
        records = matarial.get_buying_record(sn=args['sn'])
        return records, 200

    def put(self, matarial_id):
        args = matarial_buying_put_args.parse_args()

        matarial = MatarialC(matarial_id)
        matarial.modify_buying_record(**args)
        return '', 201
    
    def delete(self, matarial_id):
        args = matarial_buying_delete_args.parse_args()

        matarial = MatarialC(matarial_id)
        status = matarial.remove_buying_rocord(**args)
        if status:
            return '', 204
        else:
            return '已開始使用，無法刪除', 409
        
