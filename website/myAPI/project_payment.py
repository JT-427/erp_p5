from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import ProjectC

put_args = reqparse.RequestParser()
put_args.add_argument('sn', type=int)
put_args.add_argument('date', type=str, required=True)
put_args.add_argument('amount', type=float, required=True)
put_args.add_argument('notes', type=str, required=True)

delete_args = reqparse.RequestParser()
delete_args.add_argument('sn', type=int, required=True)

resource_fields = {
    'sn':fields.Integer,
    'amount':fields.Float,
    'notes':fields.String
}

class ProjectPaymentAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, project_id):
        project_c = ProjectC(project_id)
        records = project_c.get_payment()
        return records, 200
    
    def put(self, project_id):
        args = put_args.parse_args()

        project_c = ProjectC(project_id)
        project_c.modify_payment(**args)
        return '', 201
    
    def delete(self, project_id):
        args = delete_args.parse_args()

        project_c = ProjectC(project_id)
        project_c.delete_payment(**args)
        return '', 204