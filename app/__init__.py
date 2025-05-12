import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
from flask.cli import AppGroup
from dotenv import load_dotenv
from config import Config

# Charger les variables d'environnement
load_dotenv()

# Initialiser les extensions sans les lier à une application spécifique
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()

def create_app():
    # Créer l'instance de l'application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurer le logging
    if not app.debug:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = RotatingFileHandler(
            os.path.join(log_dir, 'error.log'),
            maxBytes=10000,
            backupCount=1
        )
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(handler)

    # Initialiser les extensions avec l'application
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Configurer Flask-Login
    login_manager.login_view = 'auth.login'

    # Définir le loader d'utilisateur
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ajouter un context_processor pour les notifications non lues
    @app.context_processor
    def inject_unread_count():
        from flask_login import current_user
        from app.models import Notification
        unread_count = 0
        if current_user.is_authenticated:
            unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return dict(unread_count=unread_count)

    # Enregistrer les blueprints
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
        """Initialise les émotions dans la base de données."""
        from app.models import Emotion
        emotions = ['Joie', 'Tristesse', 'Colère', 'Peur', 'Surprise', 'Dégoût']
        with app.app_context():
            for emotion_name in emotions:
                if not Emotion.query.filter_by(name=emotion_name).first():
                    emotion = Emotion(name=emotion_name)
                    db.session.add(emotion)
            db.session.commit()
            app.logger.info(f"Émotions initialisées : {emotions}")
            print(f"Émotions initialisées : {emotions}")

    app.cli.add_command(emotion_cli)

    return app