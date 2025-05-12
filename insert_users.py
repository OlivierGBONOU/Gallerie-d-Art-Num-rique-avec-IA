from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Liste des utilisateurs à insérer
users = [
    {
        "username": "olivier_richard",
        "email": "gbonourichard44@gmail.com",
        "password": "oliviertyui2004",
        "bio": "Adminstrateur de Gallerium. Passionné d'art comptemporain.",
        "avatar": "uploads/avatar0.jpg",
        "is_admin": True
    },
    {
        "username": "julie_peintre",
        "email": "julie.peintre@example.com",
        "password": "password123",
        "bio": "Passionnée de peinture impressionniste, j'aime capturer la lumière.",
        "avatar": "uploads/avatar1.jpg",
        "is_admin": False
    },
    {
        "username": "marc_artiste",
        "email": "marc.artiste@example.com",
        "password": "password123",
        "bio": "Sculpteur amateur, inspiré par la nature et les formes organiques.",
        "avatar": "uploads/avatar2.jpg",
        "is_admin": False
    },
    {
        "username": "sophie_dessin",
        "email": "sophie.dessin@example.com",
        "password": "password123",
        "bio": "Dessinatrice de portraits, toujours à la recherche d'émotions.",
        "avatar": "uploads/avatar3.jpg",
        "is_admin": False
    },
    {
        "username": "luc_photographe",
        "email": "luc.photographe@example.com",
        "password": "password123",
        "bio": "Photographe de rue, capturant la vie quotidienne.",
        "avatar": "uploads/avatar4.jpg",
        "is_admin": False
    },
    {
        "username": "emma_create",
        "email": "emma.create@example.com",
        "password": "password123",
        "bio": "Artiste numérique, j'explore les univers fantastiques.",
        "avatar": "uploads/avatar5.jpg",
        "is_admin": False
    },
    {
        "username": "paul_peinture",
        "email": "paul.peinture@example.com",
        "password": "password123",
        "bio": "Peintre abstrait, mes œuvres expriment le chaos intérieur.",
        "avatar": "uploads/avatar6.jpg",
        "is_admin": False
    },
    {
        "username": "clara_vision",
        "email": "clara.vision@example.com",
        "password": "password123",
        "bio": "Aquarelliste, j'aime les paysages doux et apaisants.",
        "avatar": "uploads/avatar7.jpg",
        "is_admin": False
    },
    {
        "username": "nico_sculpt",
        "email": "nico.sculpt@example.com",
        "password": "password123",
        "bio": "Sculpteur sur bois, inspiré par les traditions anciennes.",
        "avatar": "uploads/avatar8.jpg",
        "is_admin": False
    },
    {
        "username": "lea_graphiste",
        "email": "lea.graphiste@example.com",
        "password": "password123",
        "bio": "Graphiste et illustratrice, fan de couleurs vives.",
        "avatar": "uploads/avatar9.jpg",
        "is_admin": False
    },
    {
        "username": "theo_art",
        "email": "theo.art@example.com",
        "password": "password123",
        "bio": "Artiste multidisciplinaire, je mélange peinture et collage.",
        "avatar": "uploads/avatar10.jpg",
        "is_admin": False
    }
]

# Insérer les utilisateurs dans la base de données
def insert_users():
    try:
        for user_data in users:
            # Vérifier si l'utilisateur ou l'email existe déjà
            if User.query.filter_by(username=user_data["username"]).first():
                print(f"Utilisateur {user_data['username']} existe déjà.")
                continue
            if User.query.filter_by(email=user_data["email"]).first():
                print(f"Email {user_data['email']} existe déjà.")
                continue

            # Hacher le mot de passe
            user_data["password_hash"] = generate_password_hash(user_data["password"])
            del user_data["password"]  # Supprimer le mot de passe en clair

            # Créer et ajouter l'utilisateur
            user = User(**user_data)
            db.session.add(user)
            print(f"Utilisateur {user_data['username']} ajouté.")

        # Valider les changements
        db.session.commit()
        print("Tous les utilisateurs ont été insérés avec succès.")

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'insertion des utilisateurs : {e}")