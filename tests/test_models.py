# tests/test_models.py
from app import db
from app.models import User, Artwork, Emotion
from datetime import datetime

def test_user_creation(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed", bio = "testuser", avatar = "test", is_admin = 1)
        db.session.add(user)
        db.session.commit()
        assert User.query.count() == 1
        assert User.query.first().username == "testuser"

def test_artwork_creation(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(
            title="Test Art",
            description="Description",
            image_path="test.png",
            emotion_target="Joie",
            user=user,
            created_at=datetime.utcnow()  # Ajouter created_at
        )
        db.session.add_all([user, artwork])
        db.session.commit()
        assert Artwork.query.count() == 1
        assert Artwork.query.first().title == "Test Art"
        assert Artwork.query.first().created_at is not None

def test_emotion_creation(app):
    with app.app_context():
        emotion = Emotion(name="Joie")
        db.session.add(emotion)
        db.session.commit()
        assert Emotion.query.count() == 1
        assert Emotion.query.first().name == "Joie"