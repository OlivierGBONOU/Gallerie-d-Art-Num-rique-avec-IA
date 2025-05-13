# Modèles SQLAlchemy (Users, Artworks, Comments...)
# app/models.py
from flask_login import UserMixin
from datetime import datetime
from . import db

DEFAULT_EMOTIONS = [
    "Joie",
    "Tristesse",
    "Colère",
    "Peur",
    "Surprise",
    "Dégoût"
]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(128), nullable=False)
    emotion_target = db.Column(db.String(64), nullable=False)
    emotion_detected = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref=db.backref('artworks', lazy=True))
    comments = db.relationship('Comment', backref='artwork', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='artwork', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='artwork', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='artwork', lazy=True, cascade='all, delete-orphan')

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    emotion_id = db.Column(db.Integer, db.ForeignKey('emotion.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text, nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    resolved = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('reports', lazy=True))
    comment = db.relationship('Comment', backref=db.backref('reports', lazy=True))
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Admin destinataire
    message = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='notifications')
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='likes')