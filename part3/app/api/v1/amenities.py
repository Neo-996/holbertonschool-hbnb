#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, min_length=1, max_length=128, description='Amenity name (1-128 chars)')
})


@api.route('/')
class AmenityListResource(Resource):
    @api.response(200, 'Success')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities (public)"""
        return facade.get_all_amenities()

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created')
    @api.response(400, 'Validation error')
    @api.response(403, 'Admin privileges required')
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity, 201
        except ValueError as e:
            raise BadRequest(str(e))


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The Amenity ID')
class AmenityResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            raise NotFound('Amenity not found')
        return amenity

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated')
    @api.response(400, 'Validation error')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            raise NotFound('Amenity not found')

        try:
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity
        except ValueError as e:
            raise BadRequest(str(e))

