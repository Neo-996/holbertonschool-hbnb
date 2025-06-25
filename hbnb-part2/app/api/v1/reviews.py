#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werkzeug.exceptions import NotFound, BadRequest

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "user_id": fields.String(
        required=True,
        description="ID of the reviewing user"
    ),
    "place_id": fields.String(
        required=True,
        description="ID of the reviewed place"
    ),
    "rating": fields.Integer(
        required=True,
        min=1,
        max=5,
        description="Rating (1-5 stars)"
    ),
    "comment": fields.String(
        required=True,
        min_length=10,
        max_length=1024,
        description="Detailed review (10-1024 chars)"
    )
})

@api.route("/")
class ReviewListResource(Resource):
    @api.response(200, "Success")
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.response(201, "Created")
    @api.response(400, "Validation Error")
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            raise BadRequest(str(e))

@api.route("/<string:review_id>")
@api.param("review_id", "The Review ID")
class ReviewResource(Resource):
    @api.response(200, "Success")
    @api.response(404, "Not Found")
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review details"""
        review = facade.get_review(review_id)
        if not review:
            raise NotFound("Review not found")
        return review

    @api.expect(review_model, validate=True)
    @api.response(200, "Updated")
    @api.response(400, "Validation Error")
    @api.response(404, "Not Found")
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        try:
            review_data = api.payload
            updated = facade.update_review(review_id, review_data)
            if not updated:
                raise NotFound("Review not found")
            return updated
        except ValueError as e:
            raise BadRequest(str(e))

    @api.response(200, "Deleted")
    @api.response(404, "Not Found")
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            raise NotFound("Review not found")
        return {"message": "Review deleted successfully"}, 200
