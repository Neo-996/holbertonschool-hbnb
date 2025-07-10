import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    DEBUG = False

    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour (seconds)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # SQLAlchemy general settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable to avoid overhead

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # SQLite for dev

class ProductionConfig(Config):
    DEBUG = False
    # Add your production DB URI here, e.g.:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

