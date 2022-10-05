from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request

from ..modules import MiscellaneousExpenditureC

miscellaneous_expenditure_put_args = reqparse.RequestParser()
miscellaneous_expenditure_put_args.add_argument("sn", type=str)
miscellaneous_expenditure_put_args.add_argument("date", type=str, required=True)
miscellaneous_expenditure_put_args.add_argument("employee_id", type=str, required=True)
miscellaneous_expenditure_put_args.add_argument("project_id", type=str, required=True)
miscellaneous_expenditure_put_args.add_argument("description", type=str, required=True)
miscellaneous_expenditure_put_args.add_argument("classification", type=str, required=True)
miscellaneous_expenditure_put_args.add_argument("price", type=float, required=True)

miscellaneous_expenditure_delete_args = reqparse.RequestParser()
miscellaneous_expenditure_delete_args.add_argument("sn", type=str, required=True)

class MiscellaneousExpenditureAPI(Resource):
    def get(self):
        args = request.args
        sn = args['sn'] if 'sn' in args else None
        miscellaneous_expenditure = MiscellaneousExpenditureC()
        records = miscellaneous_expenditure.get_records(sn=sn)
        return records, 200
    def put(self):
        args = miscellaneous_expenditure_put_args.parse_args()
        miscellaneous_expenditure = MiscellaneousExpenditureC()
        miscellaneous_expenditure.modify(**args)
        return '', 201
    def delete(self):
        args = miscellaneous_expenditure_delete_args.parse_args()

        miscellaneous_expenditure = MiscellaneousExpenditureC() 
        miscellaneous_expenditure.delete(**args)
        return '', 204
