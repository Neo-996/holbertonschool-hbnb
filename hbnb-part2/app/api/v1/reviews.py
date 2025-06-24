#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werkzeug.exceptions import NotFound

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "id": fields.String(readonly=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "rating": fields.Integer(required=True, min=1, max=5),
    "comment": fields.String(required=True)
})


@api.route("/")
class ReviewListResource(Resource):
    @api.response(200, "List of reviews retrieved successfully")
    @api.marshal_list_with(review_model)
    def get(self):
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created successfully")
    @api.marshal_with(review_model, code=201)
    def post(self):
        review_data = api.payload
        new_review = facade.create_review(review_data)
        return new_review, 201


@api.route("/<string:review_id>")
@api.param("review_id", "The Review ID")
class ReviewResource(Resource):
    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    @api.marshal_with(review_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            raise NotFound("Review not found")
        return review

    @api.expect(review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.marshal_with(review_model)
    def put(self, review_id):
        review_data = api.payload
        updated = facade.update_review(review_id, review_data)
        if not updated:
            raise NotFound("Review not found")
        return updated

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            raise NotFound("Review not found")
        return {"message": "Review deleted successfully"}, 200
