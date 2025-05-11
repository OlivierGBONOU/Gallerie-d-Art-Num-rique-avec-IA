# tests/test_models.py
from app.models import User, Artwork, Emotion, Vote, Comment, Report
from app import db

def test_user_model(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        assert User.query.count() == 1
        assert User.query.first().username == "testuser"

def test_artwork_model(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(title="Test Art", description="Description", image_path="test.png", emotion_target="Joie", user=user)
        db.session.add_all([user, artwork])
        db.session.commit()
        assert Artwork.query.count() == 1
        assert Artwork.query.first().title == "Test Art"

def test_emotion_model(app):
    with app.app_context():
        assert Emotion.query.count() == 1  # Émotion ajoutée dans conftest.py
        assert Emotion.query.first().name == "Joie"