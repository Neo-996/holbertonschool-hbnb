from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

# Import API namespaces
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    """Application Factory to initialize Flask app with configuration"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-Restx API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register namespaces with their URL prefixes
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app

