from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import ProjectC

project_details_put_args = reqparse.RequestParser()
project_details_put_args.add_argument("sn", type=int, help="series number of details")
project_details_put_args.add_argument("description", type=str, help="description of details is required", required=True)
project_details_put_args.add_argument("unit", type=str, help="unit of details is required", required=True)
project_details_put_args.add_argument("quantity", type=float, help="quantity of details is required", required=True)
project_details_put_args.add_argument("unit_price", type=float, help="unit_price of details is required", required=True)
project_details_put_args.add_argument("price", type=float, help="price of details is required", required=True)
project_details_put_args.add_argument("date", type=str, help="date of details is required")

project_details_delete_args = reqparse.RequestParser()
project_details_delete_args.add_argument("sn", type=int, help="series number of details", required=True)

get_resource_fields = {
    "sn": fields.String,
    "project_id": fields.String,
    "description": fields.String,
    "unit": fields.String,
    "quantity": fields.Float,
    "unit_price": fields.Float,
    "price": fields.Float,
    "date": fields.String
}

class ProjectDetailsAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, project_id):
        project = ProjectC(project_id)
        project_details = project.get_details()
        return project_details, 200
    
    def put(self, project_id):
        args = project_details_put_args.parse_args()
        project = ProjectC(project_id)
        project.modify_details(**args)
        return '', 201
    
    def delete(self, project_id):
        args = project_details_delete_args.parse_args()
        project = ProjectC(project_id)
        project.delete_detail(**args)
        return '', 204