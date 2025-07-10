#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    ),
    'password': fields.String(
        required=True,
        min_length=8,
        description='Password (at least 8 characters)'
    )
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Invalid input or email exists')
    def post(self):
        """Create a new user (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
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
        """List all users (public)"""
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
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        current_id = current_user.get('id')

        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            raise NotFound('User not found')

        if not is_admin and current_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not is_admin:
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400

        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)

            if 'password' in user_data:
                updated_user.set_password(user_data['password'])
                updated_user.save()

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            raise BadRequest(str(e))
        
