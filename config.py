import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

class Config:
    """Configuration de base"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_ECHO = True
    
    # ✅ Utiliser les variables d'environnement
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    TESTING = False
    # ✅ DATABASE_URL depuis .env
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://african_legends:passer123@db:5432/heroes_db'
    )

class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    TESTING = False
    # ✅ DATABASE_URL depuis .env
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://african_legends:passer123@db:5432/heroes_db'
    )

class TestingConfig(Config):
    """Configuration test"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}