from flask_restful import Resource, reqparse

from ..modules import MatarialC

matarial_using_put_args = reqparse.RequestParser()
matarial_using_put_args.add_argument("sn", type=str)
matarial_using_put_args.add_argument("using_date", type=str, required=True)
matarial_using_put_args.add_argument("quantity", type=float, required=True)
matarial_using_put_args.add_argument("project_id", type=str, required=True)
matarial_using_put_args.add_argument("storehouse_id", type=str, required=True)
matarial_using_put_args.add_argument("employee_id", type=str, required=True)


matarial_using_delete_args = reqparse.RequestParser()
matarial_using_delete_args.add_argument("sn", type=str, required=True)

class MatarialUsingAPI(Resource):
    def get(self, matarial_id):
        matarial = MatarialC(matarial_id)
        records = matarial.get_using_record()
        return records, 200

    def put(self, matarial_id):
        args = matarial_using_put_args.parse_args()
        
        matarial = MatarialC(matarial_id)
        matarial.modify_using_record(**args)
        return '', 201
    
    def delete(self, matarial_id):
        args = matarial_using_delete_args.parse_args()

        matarial = MatarialC(matarial_id)
        status = matarial.remove_using_rocord(**args)
        return '', 204
