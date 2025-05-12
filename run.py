# Script de lancement de l'application
# run.py
from app import create_app, db
from app.models import User
from insert_users import insert_users

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()
        # Vérifier si la table User est vide
        if User.query.count() == 0:
            print("Aucun utilisateur trouvé. Insertion des utilisateurs initiaux...")
            insert_users()
        else:
            print("Utilisateurs déjà présents dans la base de données.")
    app.run(debug=True, use_reloader=True, reloader_type='stat')