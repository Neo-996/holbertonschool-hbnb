#!/usr/bin/python3

from flask import request
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
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.place_repo.get_all()

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = request.json
        place = facade.create_place(data)
        return place, 201


@api.route("/<string:place_id>")
@api.param("place_id", "The Place ID")
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve a place by ID"""
        place = facade.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a place by ID"""
        data = request.json
        updated = facade.update_place(place_id, data)
        if not updated:
            raise NotFound("Place not found")
        return updated
