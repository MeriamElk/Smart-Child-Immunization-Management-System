import os
from datetime import timedelta

class Config:
    # Configuration de base
    SECRET_KEY = os.getenv('SECRET_KEY', 'votre_cle_secrete_par_defaut')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'votre_cle_jwt_par_defaut')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///vaccination.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration des emails
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Configuration de l'application
    APP_NAME = 'VacciTrack'
    DEBUG = False
    TESTING = False
    
    # Configuration des sessions
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration des uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configuration des sauvegardes
    BACKUP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    BACKUP_RETENTION_DAYS = 30

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vaccination_dev.db'
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vaccination_test.db'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    # Configuration spécifique à la production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 