from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import ProjectC

project_outsourced_put_args = reqparse.RequestParser()
project_outsourced_put_args.add_argument("sn", type=str, required=False)
project_outsourced_put_args.add_argument("outsourcer_id", type=str, required=True)
project_outsourced_put_args.add_argument("description", type=str, required=True)
project_outsourced_put_args.add_argument("price", type=str, required=True)
project_outsourced_put_args.add_argument("date", type=str, required=True)
project_outsourced_put_args.add_argument("notes", type=str, required=False)

project_outsourced_delete_args = reqparse.RequestParser()
project_outsourced_delete_args.add_argument("sn", type=str, required=True)

get_resource_fields = {
    "sn": fields.String,
    "project_id": fields.String,
    "outsourcer_id": fields.String,
    "outsourcer_name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "notes": fields.String
}

class PrejectOutsourcedAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, project_id):
        project = ProjectC(project_id)
        result = project.get_outsourced()
        return result, 200
    
    def put(self, project_id):
        args = project_outsourced_put_args.parse_args()

        project = ProjectC(project_id)
        project.modify_outsourced(**args)
        
        return '', 201
    def delete(self, project_id):
        args = project_outsourced_delete_args.parse_args()

        project = ProjectC(project_id)
        project.delete_outsourced(**args)
        return '', 204
