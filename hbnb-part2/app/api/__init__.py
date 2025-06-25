from flask import Flask
from flask_restx import Api
from app.services.facade import facade as ServiceFacade
from app.persistence.repository import Repository

# Import namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

def create_app():
    """Application factory with in-memory repository"""
    app = Flask(__name__)
    
    # Initialize persistence and business layers (REQUIRED in Project Setup)
    repository = Repository()
    app.facade = ServiceFacade
    
    # Configure API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register namespaces (REQUIRED in all endpoint tasks)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
