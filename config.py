import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Handle Render's postgres:// URL (SQLAlchemy needs postgresql://)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH') or 'pbkdf2:sha256:600000$default$hash'  # Will be set on first run
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

