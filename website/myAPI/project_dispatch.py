from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import ProjectC

project_dispatch_put_args = reqparse.RequestParser()
project_dispatch_put_args.add_argument("employee_id", type=str, help="employee_id of dispatchment is required", required=True)
project_dispatch_put_args.add_argument("date", type=str, help="date of dispatchment is required", required=True)
project_dispatch_put_args.add_argument("assigned", type=bool, help="assigned of dispatchment is required", required=True)


get_resource_fields = {
    "employee_id": fields.String,
    "name": fields.String,
    "assigned": fields.Boolean
}

class ProjectDispatchAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, project_id):
        args = request.args
        project = ProjectC(project_id)
        result = project.get_dispatches_by_date(args['date'])
        return result, 200
    
    def put(self, project_id):
        args = project_dispatch_put_args.parse_args()
        project = ProjectC(project_id)
        project.dispatch(**args)
        
        return 201