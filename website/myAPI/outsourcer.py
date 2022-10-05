from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import OutsourcerC

post_fields = reqparse.RequestParser()
post_fields.add_argument("outsourcer_name", type=str, required=True)
post_fields.add_argument("outsourcer_title", type=str, required=True)
post_fields.add_argument("address", type=str, required=False)
post_fields.add_argument("tax_id_num", type=str, required=False)
post_fields.add_argument("contact_person", type=str, required=False)
post_fields.add_argument("contact_number", type=str, required=False)
post_fields.add_argument("fax", type=str, required=False)
post_fields.add_argument("email", type=str, required=False)
post_fields.add_argument("invoice_date", type=str, required=False)
post_fields.add_argument("drawdown_date", type=str, required=False)
post_fields.add_argument("payment_method", type=str, required=False)
post_fields.add_argument("notes", type=str, required=False)

put_fields = post_fields.copy()

get_resource_fields = {
    "outsourcer_id": fields.String,
    "outsourcer_name": fields.String,
    "outsourcer_title": fields.String,
    "address": fields.String,
    "tax_id_num": fields.String,
    "contact_person": fields.String,
    "contact_number": fields.String,
    "fax": fields.String,
    "email": fields.String,
    "invoice_date": fields.String,
    "drawdown_date": fields.String,
    "payment_method": fields.String,
    "notes": fields.String
}

class OutsourcerAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, outsourcer_id):
        outsourcer = OutsourcerC(outsourcer_id)
        return outsourcer.get_outsourcers()[0], 200
    def put(self, outsourcer_id):
        args = put_fields.parse_args()
        
        outsourcer = OutsourcerC(outsourcer_id)
        outsourcer.modify(**args)
        return '', 201
    def delete(self, outsourcer_id):
        outsourcer = OutsourcerC(outsourcer_id)
        outsourcer.delete()
        return '', 204

class OutsourcerListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        outsourcer = OutsourcerC()
        return outsourcer.get_outsourcers(), 200
    def post(self):
        args = post_fields.parse_args()

        outsourcer = OutsourcerC()
        id = outsourcer.create(**args)
        return id, 201