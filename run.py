# Script de lancement de l'application
# run.py
from app import create_app, db
from app.models import User, Emotion
from insert_users import insert_users

app = create_app()

def init_emotions():
    """Initialise les émotions si la table Emotion est vide."""
    from app.models import Emotion, DEFAULT_EMOTIONS
    try:
        for emotion_name in DEFAULT_EMOTIONS:
            if not Emotion.query.filter_by(name=emotion_name).first():
                emotion = Emotion(name=emotion_name)
                db.session.add(emotion)
                print(f"Émotion '{emotion_name}' ajoutée.")
        db.session.commit()
        print("Initialisation des émotions terminée.")
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'initialisation des émotions : {e}")

if __name__ == "__main__":
    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()
        # Vérifier si la table Emotion est vide
        if Emotion.query.count() == 0:
            print("Aucune émotion trouvée. Initialisation des émotions...")
            init_emotions()
        else:
            print("Émotions déjà présentes dans la base de données.")
        if User.query.count() == 0:
            print("Aucun utilisateur trouvé. Insertion des utilisateurs initiaux...")
            insert_users()
        else:
            print("Utilisateurs déjà présents dans la base de données.")
    app.run(debug=True, use_reloader=True, reloader_type='stat')