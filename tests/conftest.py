# tests/conftest.py
import pytest
from app import create_app, db
from app.models import User, Artwork, Emotion

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Base de données en mémoire
        'WTF_CSRF_ENABLED': False  # Désactiver CSRF pour simplifier les tests
    })
    with app.app_context():
        db.create_all()
        # Ajouter une émotion pour les tests
        emotion = Emotion(name="Joie")
        db.session.add(emotion)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_request_context()