from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager  # You were missing this import
from app.services.facade import facade as ServiceFacade
from config import DevelopmentConfig

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Attach facade for service access
    app.facade = ServiceFacade

    # Register API v1 blueprint
    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp)

    return app
