from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields
import datetime as dt

from ..modules import StorehouseC

storehouse_post_args = reqparse.RequestParser()
storehouse_post_args.add_argument("storehouse_name", type=str, help="storehouse_name of storehouse is required", required=True)
storehouse_post_args.add_argument("address", type=str, help="address  storehouse is required", required=True)
storehouse_post_args.add_argument("create_date", type=str, help="create_date  storehouse is required", required=True)
storehouse_post_args.add_argument("quit_date", type=str, help="create_date  storehouse is required")
storehouse_post_args.add_argument("notes", type=str, help="notes of storehouse is required")

storehouse_put_args = storehouse_post_args.copy()

get_resource_fields = {
    'storehouse_id': fields.String,
    'storehouse_name': fields.String,
    'create_date': fields.String,
    'quit_date': fields.String,
    'address': fields.String,
    'notes': fields.String
}

class StorehouseAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self, storehouse_id):
        storehouse = StorehouseC(storehouse_id)
        return storehouse.get_storehouse(), 200

    def put(self, storehouse_id):
        args = storehouse_put_args.parse_args()

        storehouse = StorehouseC(storehouse_id)
        storehouse.modify(**args)
        return '', 201
    def delete(self, storehouse_id):
        storehouse = StorehouseC(storehouse_id)
        storehouse.delete()
        return '', 204

class StorehouseListAPI(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        date = '' if 'mode' in request.args and request.args['mode']=='all' else dt.date.today()
        storehouses = StorehouseC()
        storehouses = storehouses.get_all_storehouse(date)
        return storehouses, 200

    def post(self):
        args = storehouse_post_args.parse_args()

        storehouse = StorehouseC()
        storehouse.create(**args)
        return '', 201