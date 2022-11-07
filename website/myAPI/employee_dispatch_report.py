from flask_restful import Resource, reqparse
from flask_login import current_user
from ..modules import EmployeeC

put_args = reqparse.RequestParser()
put_args.add_argument("date", type=str, required=True)
put_args.add_argument("projects", type=dict, required=True)
put_args.add_argument("working_days", type=float, required=True)

class EmployeeDispatchReportAPI(Resource):
    def put(self):
        args = put_args.parse_args()

        employee_id = current_user.employee_id
        employee = EmployeeC(employee_id)
        employee.report_dispatches(**args)