#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werkzeug.exceptions import NotFound, BadRequest

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'email': fields.String(
        required=True,
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        description='Valid email address'
    ),
    'first_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        description='First name (1-50 chars)'
    ),
    'last_name': fields.String(
        required=True,
        min_length=1,
        max_length=50,
        description='Last name (1-50 chars)'
    )
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Invalid input or email exists')
    def post(self):
        """Create a new user"""
        try:
            user_data = api.payload
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
                
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            raise BadRequest(str(e))

    @api.response(200, 'Success')
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/<string:user_id>')
@api.param('user_id', 'The User ID')
class UserResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details"""
        user = facade.get_user(user_id)
        if not user:
            raise NotFound('User not found')
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        try:
            user_data = api.payload
            user = facade.update_user(user_id, user_data)
            if not user:
                raise NotFound('User not found')
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200
        except ValueError as e:
            raise BadRequest(str(e))
