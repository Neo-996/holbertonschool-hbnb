"""API version 1 package initialization."""
from flask_restx import Api
from flask import Blueprint

# Initialize blueprint
bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(bp, 
          version='1.0', 
          title='HBnB API',
          description='HBNB API version 1.0')

# Import and register namespaces
from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns
from .amenities import api as amenities_ns

api.add_namespace(users_ns)
api.add_namespace(places_ns)
api.add_namespace(reviews_ns)
api.add_namespace(amenities_ns)
