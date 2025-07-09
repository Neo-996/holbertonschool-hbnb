from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import config

# Import your API namespaces here
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
# Import other namespaces as needed (places, reviews, etc.)

bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize bcrypt with the app
    bcrypt.init_app(app)

    # Initialize Flask-Restx API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register other namespaces here

    return app

