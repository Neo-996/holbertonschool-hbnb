from flask import Flask
from app.services.facade import facade as ServiceFacade
from config import DevelopmentConfig  # Default config class

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configuration
    app.facade = ServiceFacade

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app
