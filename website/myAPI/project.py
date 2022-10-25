from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import ProjectC

project_list_get_args = reqparse.RequestParser()
project_list_get_args.add_argument("date")

project_post_args = reqparse.RequestParser()
project_post_args.add_argument("project_name", type=str, help="project_name of the project is required", required=True)
project_post_args.add_argument("address", type=str, help="address of the project is required", required=True)
project_post_args.add_argument("customer_id", type=str, help="customer_id of the project is required", required=True)
project_post_args.add_argument("invoice", type=bool, help="invoice of the project is required", required=True)
project_post_args.add_argument("singing_date", type=str, help="singing_date of the project is required", required=True)
project_post_args.add_argument("start_date", type=str)
project_post_args.add_argument("finish_date", type=str)
project_post_args.add_argument("company_id", type=str, required=True)
project_post_args.add_argument("referrer", type=str)
project_post_args.add_argument("commision", type=float)

project_put_args = project_post_args.copy()

get_resource_fields = {
    "project_id": fields.String,
    "project_name": fields.String,
    "address": fields.String,
    "invoice": fields.Boolean,
    "singing_date": fields.String,
    "start_date": fields.String,
    "finish_date": fields.String,
    "customer_id": fields.String,
    "account_receivable": fields.Float,
    "referrer": fields.String,
    "company_id": fields.String,
    "commision": fields.Float,
    "customer_name": fields.String,
    "company_name": fields.String
}
class ProjectAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, project_id) -> tuple:
        project = ProjectC(project_id)
        result = project.get_info()
        if result:
            return result, 200
        else:
            return '', 204
    
    def put(self, project_id):
        args = project_put_args.parse_args()

        project = ProjectC(project_id)
        project.modify(**args)
        return '', 201
    
    def patch(self, project_id):
        args = request.json
        project = ProjectC(project_id)
        project.modify(**args)
        return '', 201

    def delete(self, project_id):
        project = ProjectC(project_id)
        project.delete()
        return '', 204


class ProjectListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self) -> tuple:
        args = request.args
        project = ProjectC()
        date = args['date'] if 'date' in args else ''
        projects = project.get_all_project(date)
        return projects, 200

    def post(self):
        args = project_post_args.parse_args()
        project = ProjectC()
        project.create(**args)
        return '', 201
