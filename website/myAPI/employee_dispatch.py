from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import EmployeeC

put_args = reqparse.RequestParser()
put_args.add_argument("working_days", type=float, required=True)
put_args.add_argument("projects", type=dict, required=True)

get_resource_fields = {
    "date": fields.String,
    "project_id": fields.String,
    "project_name": fields.String,
    "working_days": fields.Float,
    "accounts_payable": fields.Float
}

class EmployeeDispatchByDateAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id, date):
        date = date if date else None

        employee = EmployeeC(employee_id)
        records = employee.get_dispatches_by_date(date=date)
        return records, 200
    
    def put(self, employee_id, date):
        args = put_args.parse_args()
        args['date'] = date

        employee = EmployeeC(employee_id)
        employee.modify_dispatches(**args)
        return '', 201
    
    def delete(self, employee_id, date):
        employee = EmployeeC(employee_id)
        employee.delete_dispatches(date)
        return '', 204

class EmployeeDispatchByMonthAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, employee_id, year, month):
        employee = EmployeeC(employee_id)
        records = employee.get_dispatches(year=year, month=month)
        return records, 200