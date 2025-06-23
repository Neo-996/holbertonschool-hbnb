from flask_restx import Api
from flask import Blueprint
from app.api.v1.amenities import api as amenities_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='HBnB API', description='HBnB Application API')

api.add_namespace(amenities_ns, path='/api/v1/amenities')
