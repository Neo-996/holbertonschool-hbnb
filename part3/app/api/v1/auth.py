#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.services.facade import facade
from werkzeug.exceptions import Unauthorized

api = Namespace("auth", description="Authentication")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="Email"),
    "password": fields.String(required=True, description="Password")
})

@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, "Login successful")
    @api.response(401, "Invalid credentials")
    def post(self):
        """User login to receive JWT token"""
        data = request.json
        user = facade.get_user_by_email(data["email"])
        if not user or not user.check_password(data["password"]):
            raise Unauthorized("Invalid email or password")

        token_data = {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin  # included in JWT
        }
        token = create_access_token(identity=token_data)
        return {"access_token": token}, 200

