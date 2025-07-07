import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    DEBUG = False

    # Optional but useful JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour (in seconds)
    JWT_TOKEN_LOCATION = ['headers']  # Default, but explicit
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

