from flask_restful import Resource, reqparse, marshal_with, fields
from flask import request
from ..modules import MatarialC

matarial_post_args = reqparse.RequestParser()
matarial_post_args.add_argument("matarial_name", type=str, help="matarial_name of matarial is required", required=True)
matarial_post_args.add_argument("unit", type=str, help="unit of matarial is required", required=True)
matarial_post_args.add_argument("notes", type=str, help="notes of matarial is required")

matarial_put_args = matarial_post_args.copy()
get_resource_fields = {
    "matarial_id": fields.String,
    "matarial_name": fields.String,
    "notes": fields.String,
    "unit": fields.String,
    "storehouse_id": fields.String,
    "remaining": fields.String
}

class MatarialAPI(Resource):
    def put(self, matarial_id):
        args = matarial_put_args.parse_args()

        matarial = MatarialC(matarial_id)
        matarial.modify(**args)
        return '', 201

    def patch(self, matarial_id):
        matarial = MatarialC(matarial_id)
        if 'storehouse_id' in request.json and 'remaining' in request.json and request.json['remaining'] != '':
            matarial.modify_remaining(**request.json)
            return '', 201
        else:
            return '', 401

    def delete(self, matarial_id):
        matarial = MatarialC(matarial_id)
        matarial.delete()
        return '', 204


class MatarialListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        matarials = MatarialC()
        matarials = matarials.get_matarials()
        return matarials, 200

    def post(self):
        args = matarial_post_args.parse_args()

        matarial = MatarialC()
        matarial.create(**args)
        return '', 201