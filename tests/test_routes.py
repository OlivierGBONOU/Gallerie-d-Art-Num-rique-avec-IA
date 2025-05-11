# tests/test_routes.py
from flask import url_for
from app.models import User, Artwork, Emotion
from app import db

def test_index_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(title="Test Art", description="Description", image_path="test.png", emotion_target="Joie", user=user)
        db.session.add_all([user, artwork])
        db.session.commit()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test Art" in response.data

def test_artwork_page(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        artwork = Artwork(title="Test Art", description="Description", image_path="test.png", emotion_target="Joie", user=user)
        db.session.add_all([user, artwork])
        db.session.commit()
    response = client.get(url_for('main.artwork', artwork_id=1))
    assert response.status_code == 200
    assert b"Test Art" in response.data
    assert b"Joie" in response.data

def test_login(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
    response = client.post('/login', data={'username': 'testuser', 'password': 'hashed'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Bienvenue sur Gallerium" in response.data