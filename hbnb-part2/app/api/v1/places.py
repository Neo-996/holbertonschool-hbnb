#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werkzeug.exceptions import NotFound

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "price_per_night": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "max_guests": fields.Integer(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String)
})


@api.route("/")
class PlaceListResource(Resource):
    @api.response(200, "List of places retrieved successfully")
    @api.marshal_list_with(place_model)
    def get(self):
        return facade.get_all_places()

    @api.expect(place_model, validate=True)
    @api.response(201, "Place created successfully")
    @api.marshal_with(place_model, code=201)
    def post(self):
        place_data = api.payload
        new_place = facade.create_place(place_data)
        return new_place, 201


@api.route("/<string:place_id>")
@api.param("place_id", "The Place ID")
class PlaceResource(Resource):
    @api.response(200, "Place retrieved successfully")
    @api.response(404, "Place not found")
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            raise NotFound("Place not found")
        return place

    @api.expect(place_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.marshal_with(place_model)
    def put(self, place_id):
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            raise NotFound("Place not found")
        return updated_place
