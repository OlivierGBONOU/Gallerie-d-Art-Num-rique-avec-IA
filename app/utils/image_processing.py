# app/utils/image_processing.py
from PIL import Image
import os
from flask import current_app

def validate_image(file_stream):
    """Valide si le fichier est une image prise en charge (JPEG, PNG)."""
    try:
        img = Image.open(file_stream)
        if img.format not in ['JPEG', 'PNG']:
            return False
        return True
    except Exception:
        return False

def resize_image(file_path, max_size=(800, 800)):
    """Redimensionne l'image pour ne pas dépasser max_size tout en préservant les proportions."""
    try:
        img = Image.open(file_path)
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(file_path, optimize=True, quality=85)
        return True
    except Exception as e:
        current_app.logger.error(f"Erreur lors du redimensionnement de l'image : {e}")
        return False

def process_uploaded_image(file, filename):
    """Traite une image téléchargée : validation et redimensionnement."""
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not validate_image(file):
        raise ValueError("Format d'image non pris en charge. Utilisez JPEG ou PNG.")
    file.save(upload_folder)
    if not resize_image(upload_folder):
        raise ValueError("Erreur lors du traitement de l'image.")
    return upload_folder