#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade
from werkzeug.exceptions import NotFound, BadRequest

api = Namespace("places", description="Place operations")

# Improved model with validation
place_model = api.model("Place", {
    "title": fields.String(
        required=True,
        min_length=1,
        max_length=128,
        description="Place title (1-128 chars)"
    ),
    "description": fields.String(
        required=True,
        min_length=10,
        max_length=1024,
        description="Detailed description (10-1024 chars)"
    ),
    "price_per_night": fields.Float(
        required=True,
        min=0,
        description="Price per night (non-negative)"
    ),
    "latitude": fields.Float(
        required=True,
        min=-90,
        max=90,
        description="Latitude (-90 to 90)"
    ),
    "longitude": fields.Float(
        required=True,
        min=-180,
        max=180,
        description="Longitude (-180 to 180)"
    ),
    "max_guests": fields.Integer(
        required=True,
        min=1,
        description="Maximum guests (at least 1)"
    ),
    "owner_id": fields.String(
        required=True,
        description="ID of the owner/user"
    ),
    "amenities": fields.List(
        fields.String,
        description="List of amenity IDs"
    )
})

@api.route("/")
class PlaceListResource(Resource):
    @api.response(200, "Success")
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @api.expect(place_model, validate=True)
    @api.response(201, "Created")
    @api.response(400, "Validation Error")
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        try:
            place_data = api.payload
            # Override owner_id with authenticated user ID
            place_data["owner_id"] = current_user["id"]
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            raise BadRequest(str(e))

@api.route("/<string:place_id>")
@api.param("place_id", "The Place ID")
class PlaceResource(Resource):
    @api.response(200, "Success")
    @api.response(404, "Not Found")
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get place details"""
        place = facade.get_place(place_id)
        if not place:
            raise NotFound("Place not found")
        return place

    @api.expect(place_model, validate=True)
    @api.response(200, "Updated")
    @api.response(400, "Validation Error")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Not Found")
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update place information (only if owned by user)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            raise NotFound("Place not found")

        if place.owner_id != current_user["id"]:
            return {"error": "Unauthorized action"}, 403

        try:
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            return updated_place
        except ValueError as e:
            raise BadRequest(str(e))
