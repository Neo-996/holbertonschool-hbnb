#!/usr/bin/python3
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('protected', description='Protected route example')

@api.route('/')
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()  # Returns dict with id and is_admin
        return {'message': f'Hello, user {current_user["id"]}'}, 200
