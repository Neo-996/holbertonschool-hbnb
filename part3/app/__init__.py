from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

# Import your API namespaces here
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
# Import other namespaces as needed (places, reviews, etc.)

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

    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    # Register other namespaces here (places, reviews, etc.)

    return app

