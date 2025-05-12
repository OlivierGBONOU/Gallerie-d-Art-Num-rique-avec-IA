# tests/test_routes.py
from flask import url_for
from app import db
from app.models import User, Artwork, Emotion
from datetime import datetime
import html
from flask_login import login_user

def test_index_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(
            title="Test Art",
            description="Description",
            image_path="test.png",
            emotion_target="Joie",
            user=user,
            created_at=datetime.utcnow()
        )
        db.session.add_all([user, artwork])
        db.session.commit()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test Art" in response.data

def test_artwork_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(
            title="Test Art",
            description="Description",
            image_path="test.png",
            emotion_target="Joie",
            user=user,
            created_at=datetime.utcnow()
        )
        db.session.add_all([user, artwork])
        db.session.commit()
    response = client.get(url_for('main.artwork', artwork_id=1))
    assert response.status_code == 200
    assert b"Test Art" in response.data
    assert b"Joie" in response.data

def test_profile_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        with client:
            login_user(user)  # Utiliser login_user pour simuler l'authentification
            response = client.get('/profile')
            assert response.status_code == 200
            assert b"Profil de testuser" in response.data

def test_edit_artwork_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(
            title="Test Art",
            description="Description",
            image_path="test.png",
            emotion_target="Joie",
            user=user,
            created_at=datetime.utcnow()
        )
        db.session.add_all([user, artwork])
        db.session.commit()
        with client:
            login_user(user)
            response = client.get(f'/edit/{artwork.id}')
            assert response.status_code == 200
            assert b"Test Art" in response.data

def test_delete_artwork(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(
            title="Test Art",
            description="Description",
            image_path="test.png",
            emotion_target="Joie",
            user=user,
            created_at=datetime.utcnow()
        )
        db.session.add_all([user, artwork])
        db.session.commit()
        with client:
            login_user(user)
            response = client.post(f'/delete/{artwork.id}', follow_redirects=True)
            assert response.status_code == 200
            assert Artwork.query.count() == 0
            assert "Œuvre supprimée." in response.data.decode('utf-8')  # Décoder et vérifier le texte

def test_edit_profile_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        with client:
            login_user(user)
            response = client.get('/edit_profile')
            assert response.status_code == 200
            assert b"Modifier le profil" in response.data