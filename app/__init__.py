# Initialisation de l'application (Flask app factory)
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

# Liste des émotions par défaut
DEFAULT_EMOTIONS = [
    "Joie",
    "Tristesse",
    "Colère",
    "Peur",
    "Surprise",
    "Dégoût"
]

def init_emotions():
    """Initialise la table Emotion avec les émotions par défaut si elles n'existent pas."""
    from .models import Emotion  # Importer ici pour éviter les importations circulaires
    with db.session.no_autoflush:
        for emotion_name in DEFAULT_EMOTIONS:
            if not Emotion.query.filter_by(name=emotion_name).first():
                emotion = Emotion(name=emotion_name)
                db.session.add(emotion)
        db.session.commit()
    print("Émotions initialisées :", [e.name for e in Emotion.query.all()])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',  # Remplacez par votre serveur SMTP
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='gbonourichard44@gmail.com',  # Remplacez par votre email
        MAIL_PASSWORD='Oliviertyui2004',  # Mot de passe d'application
        MAIL_DEFAULT_SENDER='gbonourichard44@gmail.com'
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()
        init_emotions()

    from .routes import main, auth, user, admin, interactions
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(interactions.bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))