# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
from flask.cli import AppGroup
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurer le logging
    if not app.debug:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Créer le dossier logs s'il n'existe pas
        handler = RotatingFileHandler(os.path.join(log_dir, 'error.log'), maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(handler)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main, auth, user, interactions, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(interactions.bp)
    app.register_blueprint(admin.bp)

    # Commande CLI pour initialiser les émotions
    emotion_cli = AppGroup('emotion', help='Commands for managing emotions')
    
    @emotion_cli.command('init')
    def init_emotions_command():
        """Initialize the emotions in the database."""
        emotions = ['Joie', 'Tristesse', 'Colère', 'Peur', 'Surprise', 'Dégoût']
        with app.app_context():
            for emotion_name in emotions:
                from app.models import Emotion
                if not Emotion.query.filter_by(name=emotion_name).first():
                    emotion = Emotion(name=emotion_name)
                    db.session.add(emotion)
            db.session.commit()
            print("Émotions initialisées :", emotions)

    app.cli.add_command(emotion_cli)

    return app