#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade
from werkzeug.exceptions import NotFound, BadRequest

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "place_id": fields.String(required=True, description="ID of the reviewed place"),
    "rating": fields.Integer(required=True, min=1, max=5, description="Rating (1-5 stars)"),
    "comment": fields.String(required=True, min_length=10, max_length=1024, description="Review text")
})

@api.route("/")
class ReviewListResource(Resource):
    @api.response(200, "Success")
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews (public)"""
        return facade.get_all_reviews()

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, "Created")
    @api.response(400, "Validation Error")
    def post(self):
        """Create a new review (auth user only, cannot review own place)"""
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        is_admin = current_user.get("is_admin", False)

        data = api.payload
        place = facade.get_place(data["place_id"])
        if not place:
            raise NotFound("Place not found")

        if not is_admin:
            if place["owner_id"] == user_id:
                raise BadRequest("You cannot review your own place")
            if facade.user_reviewed_place(user_id, data["place_id"]):
                raise BadRequest("You have already reviewed this place")

        data["user_id"] = user_id
        review = facade.create_review(data)
        return review, 201


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

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, "Updated")
    @api.response(403, "Unauthorized")
    def put(self, review_id):
        """Update a review (owner or admin only)"""
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        is_admin = current_user.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            raise NotFound("Review not found")

        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        updated_review = facade.update_review(review_id, api.payload)
        return updated_review, 200

    @jwt_required()
    @api.response(200, "Deleted")
    @api.response(403, "Unauthorized")
    def delete(self, review_id):
        """Delete a review (owner or admin only)"""
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        is_admin = current_user.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            raise NotFound("Review not found")

        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted"}, 200

