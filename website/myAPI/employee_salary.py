from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import EmployeeC

put_args = reqparse.RequestParser()
put_args.add_argument("sn", type=str, default=None, required=False)
put_args.add_argument("salary", type=float, required=True)
put_args.add_argument("unit", type=str, required=True)
put_args.add_argument("start_date", type=str, required=True)

delete_args = reqparse.RequestParser()
delete_args.add_argument("sn", type=str, required=True)

get_resource_fields = {
    "sn": fields.String,
    "employee_id": fields.String,
    "salary": fields.String,
    "unit": fields.String,
    "start_date": fields.String,
    "end_date": fields.String
}
class EmployeeSalaryAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id):
        employee = EmployeeC(employee_id)
        record = employee.get_salary_record()
        return record, 200
    
    def put(self, employee_id):
        args = put_args.parse_args()
        
        employee = EmployeeC(employee_id)
        employee.modify_salary_record(**args)
        return '', 201
    
    def delete(self, employee_id):
        args = delete_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.delete_salary_record(**args)
        return '', 204