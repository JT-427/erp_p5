from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import EmployeeC

put_args = reqparse.RequestParser()
put_args.add_argument("sn", type=int, required=False)
put_args.add_argument("hired_date", type=str, required=True)
put_args.add_argument("resigned_date", type=str, required=True)

delete_args = reqparse.RequestParser()
delete_args.add_argument("sn", type=str, required=True)


get_resource_fields = {
    "sn": fields.String,
    "employee_id": fields.String,
    "hired_date": fields.String,
    "resigned_date": fields.String
}
class EmployeeHiredAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id):
        employee = EmployeeC(employee_id)
        records = employee.get_hired_record()
        return records, 200
    
    def put(self, employee_id):
        args = put_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.modify_hired_record(**args)
        return '', 201
    
    def delete(self, employee_id):
        args = delete_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.delete_hired_record(**args)
        return '', 204