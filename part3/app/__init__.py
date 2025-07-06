from flask import Flask
from app.services.facade import facade as ServiceFacade

def create_app():
    app = Flask(__name__)
    app.facade = ServiceFacade
    
    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    
    return app
