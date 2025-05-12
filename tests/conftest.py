# tests/conftest.py
import pytest
from app import create_app, db
from flask import Flask
import logging
import warnings  # Ajouter l'import

# Désactiver le logging pendant les tests
logging.getLogger().setLevel(logging.CRITICAL)

# Ignorer les avertissements LegacyAPIWarning
warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_sqlalchemy")

@pytest.fixture
def app(monkeypatch):
    def mock_emotion_classifier(*args, **kwargs):
        class MockPipeline:
            def __call__(self, text):
                return [{"label": "joy", "score": 0.9}]
        return MockPipeline()
    
    monkeypatch.setattr("app.utils.emotion_analysis.pipeline", mock_emotion_classifier)

    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'DEBUG': True,
        'MAIL_SUPPRESS_SEND': True,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()