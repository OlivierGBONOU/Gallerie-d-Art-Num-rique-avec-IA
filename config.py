# Fichier de configuration (dev, prod, DB, clés API)
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_cle_secrete_tres_securisee'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gallerium.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 Mo max pour les uploads