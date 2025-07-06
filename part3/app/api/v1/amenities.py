#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(
        required=True,
        min_length=1,
        max_length=128,
        description='Name of the amenity (1-128 chars)'
    )
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Create a new amenity"""
        data = api.payload
        try:
            new_amenity = facade.create_amenity(data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """List all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': a.id,
            'name': a.name
        } for a in amenities], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get a specific amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity"""
        data = api.payload
        try:
            updated = facade.update_amenity(amenity_id, data)
            if not updated:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity updated'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
