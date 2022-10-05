from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import ProjectC

labor_fields = {
    # 'project_id': fields.String,
    # 'employee_id': fields.String,
    'name': fields.String,
    'working_days': fields.Float,
    'payment': fields.Float
}
matarial_fields = {
    # 'matarial_id': fields.String,
    'matarial_name': fields.String,
    'quantity': fields.Float,
    'cost': fields.Float
}
outsourced_fields = {
    'outsourcer_name': fields.String,
    'count': fields.Float,
    'payment': fields.Float
}
miscellaneous_expenditure_fields = {
    'total': fields.Float
}
commision_fields = {
    'referrer': fields.String,
    'commision': fields.String
}
get_resource_fields = {
    'labor': fields.Nested(labor_fields),
    'matarial': fields.Nested(matarial_fields),
    'outsourced': fields.Nested(outsourced_fields),
    'miscellaneous_expenditure': fields.Nested(miscellaneous_expenditure_fields),
    'commision': fields.Nested(commision_fields)
}

class ProjectCostAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, project_id):
        project = ProjectC(project_id)
        project_cost = project.get_cost()
        return project_cost, 200
        