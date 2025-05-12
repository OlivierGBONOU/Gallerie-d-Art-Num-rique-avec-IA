# Fonctions utilitaires de sécurité# app/utils/security.py
import re
from flask import request, abort
from werkzeug.security import generate_password_hash, check_password_hash

def sanitize_input(text):
    """Nettoie les entrées utilisateur pour éviter les injections XSS ou SQL."""
    if not text:
        return text
    # Supprimer les balises HTML et scripts
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Supprimer les caractères dangereux
    clean_text = re.sub(r'[\;\|\`]', '', clean_text)
    return clean_text

def verify_csrf_token():
    """Vérifie le jeton CSRF pour les requêtes POST."""
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != request.session.get('csrf_token'):
            abort(403, description="Jeton CSRF invalide.")
    return True

def hash_password(password):
    """Hache un mot de passe."""
    return generate_password_hash(password, method='pbkdf2:sha256')

def check_password(hashed_password, password):
    """Vérifie un mot de passe contre son hachage."""
    return check_password_hash(hashed_password, password)