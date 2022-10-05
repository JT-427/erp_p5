from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import CustomerC

post_args = reqparse.RequestParser()
post_args.add_argument("customer_name", type=str, required=True)
post_args.add_argument("customer_title", type=str, required=True)
post_args.add_argument("address", type=str, required=False)
post_args.add_argument("tax_id_num", type=str, required=False)
post_args.add_argument("contact_person", type=str, required=False)
post_args.add_argument("contact_number", type=str, required=False)
post_args.add_argument("fax", type=str, required=False)
post_args.add_argument("email", type=str, required=False)
post_args.add_argument("invoice_date", type=str, required=False)
post_args.add_argument("drawdown_date", type=str, required=False)
post_args.add_argument("payment_method", type=str, required=False)
post_args.add_argument("notes", type=str, required=False)

put_args = post_args.copy()


get_resource_fields = {
    "customer_id": fields.String,
    "customer_name": fields.String,
    "customer_title": fields.String,
    "address": fields.String,
    "tax_id_num": fields.String,
    "contact_person": fields.String,
    "contact_number": fields.String,
    "fax": fields.String,
    "email": fields.String,
    "invoice_date": fields.String,
    "drawdown_date": fields.String,
    "payment_method": fields.String,
    "notes": fields.String,
}

class CustomerAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, customer_id):
        customer = CustomerC(customer_id=customer_id)
        info = customer.get_customer_info()
        return info, 200
    def put(self, customer_id):
        customer = CustomerC(customer_id)
        customer.modify(**put_args.parse_args())
        return '', 201
    def delete(self, customer_id):
        customer = CustomerC(customer_id)
        customer.delete()
        return '', 204

class CustomerListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        customer = CustomerC()
        customers = customer.get_all_customer()
        return customers, 200
    def post(self):
        customer = CustomerC()
        customer.create(**post_args.parse_args())
        return '', 201