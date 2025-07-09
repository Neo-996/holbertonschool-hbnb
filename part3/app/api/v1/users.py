#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werkzeug.exceptions import NotFound, BadRequest
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Model for user creation (with password)
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
    ),
    'password': fields.String(
        required=True,
        min_length=8,
        description='Password (at least 8 characters)'
    )
})

# Model for updating user (no email or password)
user_update_model = api.model('UserUpdate', {
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
            if facade.get_user_by_email(user_data['email']):
                return {'error': 'Email already registered'}, 400

            # Create user and hash password
            new_user = facade.create_user(user_data)
            new_user.set_password(user_data['password'])
            new_user.save()

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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information (only own, no email or password)"""
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            user_data = api.payload
            # Email and password cannot be updated here, no need to check since model excludes them

            user = facade.get_user(user_id)
            if not user:
                raise NotFound('User not found')

            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']

            facade.save_user(user)

            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200
        except ValueError as e:
            raise BadRequest(str(e))

