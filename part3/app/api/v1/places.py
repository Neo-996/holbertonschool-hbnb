#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title": fields.String(required=True, min_length=1, max_length=128, description="Place title"),
    "description": fields.String(required=True, min_length=10, max_length=1024, description="Place description"),
    "price_per_night": fields.Float(required=True, min=0, description="Nightly price"),
    "latitude": fields.Float(required=True, min=-90, max=90, description="Latitude"),
    "longitude": fields.Float(required=True, min=-180, max=180, description="Longitude"),
    "max_guests": fields.Integer(required=True, min=1, description="Maximum number of guests"),
    "amenities": fields.List(fields.String, description="List of amenity IDs")
})


@api.route("/")
class PlaceListResource(Resource):
    @api.response(200, "Success")
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places (public)"""
        return facade.get_all_places()

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, "Created")
    @api.response(400, "Validation Error")
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place (authenticated users only)"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data["owner_id"] = current_user.get("id")

        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            raise BadRequest(str(e))


@api.route("/<string:place_id>")
@api.param("place_id", "The Place ID")
class PlaceResource(Resource):
    @api.response(200, "Success")
    @api.response(404, "Place not found")
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get place details (public)"""
        place = facade.get_place(place_id)
        if not place:
            raise NotFound("Place not found")
        return place

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, "Updated")
    @api.response(400, "Validation error")
    @api.response(403, "Unauthorized")
    @api.response(404, "Place not found")
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a place (owner or admin only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            raise NotFound("Place not found")

        is_admin = current_user.get("is_admin", False)
        user_id = current_user.get("id")

        if not is_admin and place.get("owner_id") != user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            return updated_place
        except ValueError as e:
            raise BadRequest(str(e))

