from flask_restful import Resource, reqparse, marshal_with, fields

from ..modules import MatarialSupplierC

post_args = reqparse.RequestParser()
post_args.add_argument("matarial_supplier_name", type=str, required=True)
post_args.add_argument("contact_person", type=str)
post_args.add_argument("contact_number", type=str)
post_args.add_argument("email", type=str)
post_args.add_argument("notes", type=str)
post_args.add_argument("cooperating", type=bool)

put_args = post_args.copy()

get_resource_fields = {
    "matarial_supplier_id": fields.String,
    "matarial_supplier_name": fields.String,
    "contact_person": fields.String,
    "contact_number": fields.String,
    "email": fields.String,
    "notes": fields.String,
    "cooperating": fields.Boolean,
}

class MatarialSupplierAPI(Resource):
    def put(self, matarial_supplier_id):
        args = put_args.parse_args()

        supplier = MatarialSupplierC(matarial_supplier_id)
        supplier.modify(**args)
        return '', 201

    def delete(self, matarial_supplier_id):
        supplier = MatarialSupplierC(matarial_supplier_id)
        supplier.delete()
        return '', 204


class MatarialSupplierListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        supplier = MatarialSupplierC()
        suppliers = supplier.get_suppliers()
        return suppliers, 200

    def post(self):
        args = post_args.parse_args()

        supplier = MatarialSupplierC()
        supplier.create(**args)
        return '', 201