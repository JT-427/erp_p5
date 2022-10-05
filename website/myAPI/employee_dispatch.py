from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import EmployeeC

delete_args = reqparse.RequestParser()
delete_args.add_argument("date", type=str, required=True)

put_args = delete_args.copy()
put_args.add_argument("working_days", type=float, required=True)
put_args.add_argument("projects", type=dict, required=True)

get_resource_fields = {
    "date": fields.String,
    "project_id": fields.String,
    "project_name": fields.String,
    "assigned": fields.Boolean,
    "working_days": fields.Float
}

class EmployeeDispatchAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id):
        date = request.args['date'] if 'date' in request.args else None

        employee = EmployeeC(employee_id)
        records = employee.get_dispatches(date=date)
        return records, 200
    
    def put(self, employee_id):
        args = put_args.parse_args()
        
        employee = EmployeeC(employee_id)
        employee.modify_dispatches(**args)
        return '', 201
    
    def delete(self, employee_id):
        args = delete_args.parse_args()

        employee = EmployeeC(employee_id)
        employee.delete_dispatches(**args)
        return '', 204