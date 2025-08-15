import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    
    # Supabase Configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = False  # Token não expira para simplicidade
    
    # Railway/Production specific
    PORT = int(os.environ.get('PORT', 5001))
    HOST = os.environ.get('HOST', '0.0.0.0')
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    
    # CORS Settings for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://reception-sync-production.up.railway.app').split(',')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:3000']

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}