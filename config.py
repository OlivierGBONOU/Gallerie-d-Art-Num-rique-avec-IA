# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gallerium.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max pour les uploads
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.mailtrap.io'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 2525)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-mailtrap-username'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-mailtrap-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your.email@example.com'