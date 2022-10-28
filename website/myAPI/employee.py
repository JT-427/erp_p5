from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import EmployeeC

employee_post_args = reqparse.RequestParser()
employee_post_args.add_argument("name", type=str, help="name of employee is required", required=True)
employee_post_args.add_argument("sex", type=str, help="gender of employee is required", required=True)
employee_post_args.add_argument("birthday", type=str, help="birthday of employee is required", required=True)
employee_post_args.add_argument("telephone", type=str, help="telephone of employee is required")
employee_post_args.add_argument("cellphone", type=str, help="cellphone of employee is required")
employee_post_args.add_argument("address", type=str, help="address of employee is required")
employee_post_args.add_argument("email", type=str, help="email of employee is required")
employee_post_args.add_argument("hired_date", type=str, help="hired_date of employee is required", required=True)
employee_post_args.add_argument("salary", type=str, help="salary of employee is required", required=True)
employee_post_args.add_argument("salary_unit", type=str, help="salary_unit of employee is required", required=True)

employee_put_args = reqparse.RequestParser()
employee_put_args.add_argument("name", type=str, help="name of employee is required", required=True)
employee_put_args.add_argument("sex", type=str, help="gender of employee is required", required=True)
employee_put_args.add_argument("birthday", type=str, help="birthday of employee is required", required=True)
employee_put_args.add_argument("telephone", type=str, help="telephone of employee is required")
employee_put_args.add_argument("cellphone", type=str, help="cellphone of employee is required")
employee_put_args.add_argument("address", type=str, help="address of employee is required")
employee_put_args.add_argument("email", type=str, help="email of employee is required")

get_resource_fields = {
    "employee_id": fields.String,
    "name": fields.String,
    "sex": fields.String,
    "birthday": fields.String,
    "telephone": fields.String,
    "cellphone": fields.String,
    "address": fields.String,
    "email": fields.String,
    "hired_date": fields.String,
    "user_id": fields.Integer,
    "salary": fields.Float,
    "salary_unit": fields.String,
    "salary_start_date": fields.String
}

class EmployeeAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id):
        # 需要訂規格
        employee = EmployeeC(employee_id=employee_id)
        return employee, 200
    def put(self, employee_id):
        employee = EmployeeC(employee_id)
        employee.modify(**employee_put_args.parse_args())
        return '', 201

class EmployeeListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self) -> tuple:
        employees_query = EmployeeC().get_all_employee()
        return employees_query, 200
    
    def post(self):
        employee_ = EmployeeC()
        employee_.create(employee_post_args.parse_args())
        return '', 201
    
