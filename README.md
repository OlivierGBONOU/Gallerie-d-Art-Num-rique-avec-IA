# Gallerium - Plateforme de Partage d'Art

**Gallerium** est une plateforme web développée avec **Flask** permettant aux utilisateurs de partager, découvrir et interagir avec des œuvres d'art numériques. Les utilisateurs peuvent télécharger des images, créer des profils, commenter des œuvres, recevoir des notifications et gérer leurs interactions. Une interface d'administration est également disponible pour modérer le contenu et gérer les utilisateurs.

## Table des matières
- [Gallerium - Plateforme de Partage d'Art](#gallerium---plateforme-de-partage-dart)
  - [Table des matières](#table-des-matières)
  - [Fonctionnalités](#fonctionnalités)
  - [Technologies utilisées](#technologies-utilisées)
  - [Structure du projet](#structure-du-projet)
  - [Prérequis](#prérequis)
  - [Installation](#installation)
  - [Utilisation](#utilisation)
  - [Accès administrateur](#accès-administrateur)
  - [Tests](#tests)
  - [Contribuer](#contribuer)
  - [Licence](#licence)

## Fonctionnalités
- **Authentification** : Inscription, connexion et gestion de profils utilisateurs.
- **Gestion d'œuvres** : Téléchargement, modification et suppression d'images artistiques.
- **Interactions** : Commentaires, likes et notifications pour les interactions entre utilisateurs.
- **Administration** : Tableau de bord pour modérer les contenus et gérer les utilisateurs.
- **Analyse émotionnelle** : Analyse des commentaires pour détecter les émotions (via `emotion_analysis.py`).
- **Nuage de mots** : Génération de nuages de mots à partir des descriptions des œuvres (via `wordcloud_generator.py`).
- **Personnalisation** : Interface utilisateur avec CSS personnalisé et JavaScript pour des interactions dynamiques.

## Technologies utilisées
- **Backend** : Python 3, Flask
- **Base de données** : SQLite (`gallerium.db`)
- **Frontend** : HTML, CSS, JavaScript
- **Tests** : Pytest
- **Autres** : Gestion des dépendances avec `requirements.txt`, configuration via `config.py`

## Structure du projet
```
├── .gitignore                # Fichiers/dossiers ignorés par Git
├── config.py                 # Configuration globale de l'application
├── README.md                 # Documentation du projet
├── requirements.txt          # Dépendances Python
├── run.py                    # Point d'entrée de l'application
├── tree.txt                  # Arborescence du projet
├── instance/
│   ├── config.py             # Configuration spécifique à l'instance
│   ├── gallerium.db          # Base de données SQLite
├── app/
│   ├── __init__.py           # Initialisation de l'application Flask
│   ├── forms.py              # Formulaires WTForms
│   ├── models.py             # Modèles SQLAlchemy
│   ├── routes/               # Routes de l'application
│   │   ├── admin.py          # Routes pour l'administration
│   │   ├── auth.py           # Routes pour l'authentification
│   │   ├── interactions.py   # Routes pour les interactions utilisateur
│   │   ├── main.py           # Routes principales
│   │   ├── user.py           # Routes pour la gestion des profils
│   ├── static/               # Fichiers statiques
│   │   ├── css/style.css     # Styles personnalisés
│   │   ├── images/           # Images statiques
│   │   ├── js/               # Scripts JavaScript
│   │   ├── uploads/          # Images téléchargées par les utilisateurs
│   ├── templates/            # Modèles HTML
│   │   ├── admin/            # Templates pour l'administration
│   │   ├── *.html            # Templates pour les pages principales
│   ├── utils/                # Fonctions utilitaires
│   │   ├── decorators.py     # Décorateurs personnalisés (ex. restriction admin)
│   │   ├── emotion_analysis.py # Analyse émotionnelle des commentaires
│   │   ├── image_processing.py # Traitement des images (à implémenter)
│   │   ├── security.py       # Fonctions de sécurité (à implémenter)
│   │   ├── wordcloud_generator.py # Génération de nuages de mots
├── logs/
│   ├── error.log             # Journal des erreurs
├── tests/
│   ├── conftest.py           # Configuration des tests
│   ├── test_models.py        # Tests des modèles
│   ├── test_routes.py        # Tests des routes
```

## Prérequis
- Python 3.11+
- Git
- Navigateur web moderne

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/OlivierGBONOU/Gallerie-d-Art-Num-rique-avec-IA.git
   cd gallerium
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez la base de données :
   - Assurez-vous que `instance/config.py` contient les configurations nécessaires (ex. `SECRET_KEY`).
   - Initialisez la base de données en exécutant :
     ```python
     from app import db
     db.create_all()
     ```

5. Lancez l'application :
   ```bash
   python run.py
   ```

6. Accédez à l'application via `http://localhost:5000`.

## Utilisation
- **Inscription/Connexion** : Créez un compte ou connectez-vous via `/register` ou `/login`.
- **Téléchargement d'œuvres** : Accédez à `/upload` pour partager vos images.
- **Profil utilisateur** : Consultez et modifiez votre profil via `/profile`.
- **Interactions** : Commentez et likez les œuvres via les pages des œuvres.
- **Administration** : Les administrateurs peuvent accéder au tableau de bord via `/admin/dashboard`.

## Accès administrateur
Les pages réservées aux administrateurs (comme `/admin/dashboard` et `/admin/moderation`) sont protégées par un décorateur défini dans `app/utils/decorators.py` (probablement `@admin_required`). Pour qu'un utilisateur accède à ces pages :
1. L'utilisateur doit être authentifié.
2. L'utilisateur doit avoir un rôle `admin` dans la base de données.
3. Lors de l'inscription ou via une action manuelle dans la base de données, un administrateur doit attribuer le rôle `admin` à l'utilisateur.
4. Une fois connecté, l'administrateur peut accéder aux routes sous `/admin/*` pour gérer les utilisateurs, modérer les contenus et consulter les statistiques.

## Tests
Les tests sont situés dans le dossier `tests/` et utilisent **Pytest**. Pour exécuter les tests :
```bash
pytest
```
- `test_models.py` : Tests des modèles de la base de données.
- `test_routes.py` : Tests des routes de l'application.

## Contribuer
1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Committez vos modifications (`git commit -m "Ajout de nouvelle fonctionnalité"`).
4. Poussez votre branche (`git push origin feature/nouvelle-fonctionnalite`).
5. Ouvrez une Pull Request.

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.