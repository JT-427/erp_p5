from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import EmployeeC

put_args = reqparse.RequestParser()
put_args.add_argument("sn", type=int)
put_args.add_argument("date", type=str, required=True)
put_args.add_argument("type", type=str, required=True)
put_args.add_argument("amount", type=str, required=True)
put_args.add_argument("notes", type=str)

delete_args = reqparse.RequestParser()
delete_args.add_argument("sn", type=str, required=True)

class EmployeePaymentAPI(Resource):
    def put(self, employee_id):
        args = put_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.modify_payment_record(**args)
        return '', 201
    
    def delete(self, employee_id):
        args = delete_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.delete_payment_record(**args)
        return '', 204