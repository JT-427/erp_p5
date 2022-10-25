from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import CompanyC

post_args = reqparse.RequestParser()
post_args.add_argument("company_name", type=str, required=True)
post_args.add_argument("address", type=str)
post_args.add_argument("postal_address", type=str)
post_args.add_argument("tax_id_num", type=str)
post_args.add_argument("fax", type=str)
post_args.add_argument("responsible_person", type=str)
post_args.add_argument("contact_person", type=str)
post_args.add_argument("contact_number", type=str)
post_args.add_argument("create_date", type=str, required=True)
post_args.add_argument("end_date", type=str)
post_args.add_argument("notes", type=str)

put_args = post_args.copy()

get_resource_fields = {
    "company_id": fields.String,
    "company_name": fields.String,
    "address": fields.String,
    "postal_address": fields.String,
    "tax_id_num": fields.String,
    "fax": fields.String,
    "responsible_person": fields.String,
    "contact_person": fields.String,
    "contact_number": fields.String,
    "create_date": fields.String,
    "end_date": fields.String,
    "notes": fields.String,
}
class CompanyAPI(Resource):
    # @marshal_with(get_resource_fields)
    # def get(self, company_id):
    #     pass
    def put(self, company_id):
        args = put_args.parse_args()
        company = CompanyC(company_id)
        company.modify(**args)
        return '', 201

    def delete(self, company_id):
        company = CompanyC(company_id)
        company.delete()
        return '', 204

class CompanyListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = request.args
        date = args['date'] if 'date' in args else ''

        company = CompanyC()
        companies = company.get_all_company(date)
        return companies, 200
    def post(self):
        args = post_args.parse_args()
        company = CompanyC()
        company.create(**args)
        return '', 201
