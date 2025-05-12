# Gallerium - README

Gallerium est une plateforme web développée avec Flask, conçue pour permettre aux utilisateurs de partager, découvrir et interagir avec des œuvres d'art numériques tout en explorant les émotions qu'elles suscitent. Ce document présente une description complète des fonctionnalités, de l'architecture, des dépendances, de l'installation et des instructions pour contribuer au projet.

## Table des matières

- [Gallerium - README](#gallerium---readme)
  - [Table des matières](#table-des-matières)
  - [Présentation du projet](#présentation-du-projet)
  - [Fonctionnalités principales](#fonctionnalités-principales)
    - [Pour tous les utilisateurs](#pour-tous-les-utilisateurs)
    - [Pour les utilisateurs connectés](#pour-les-utilisateurs-connectés)
    - [Pour les administrateurs](#pour-les-administrateurs)
  - [Architecture du projet](#architecture-du-projet)
  - [Dépendances](#dépendances)
  - [Installation et configuration](#installation-et-configuration)
    - [Prérequis](#prérequis)
    - [Étapes d'installation](#étapes-dinstallation)
    - [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
    - [Lancement de l'application](#lancement-de-lapplication)
  - [Tests](#tests)
  - [Contribuer](#contribuer)
    - [Bonnes pratiques](#bonnes-pratiques)
  - [Licence](#licence)

## Présentation du projet

Gallerium est une plateforme sociale dédiée à l'art numérique, où les utilisateurs peuvent partager leurs créations, voter pour les émotions associées aux œuvres, commenter, et interagir avec une communauté d'artistes. L'application intègre des fonctionnalités d'analyse émotionnelle basée sur le NLP (Natural Language Processing) pour détecter les émotions dans les descriptions des œuvres, ainsi que des outils de modération pour garantir un environnement sûr et respectueux. Elle utilise une interface moderne avec Bootstrap et Chart.js pour une expérience utilisateur fluide et visuellement attrayante.

Le projet est conçu pour être modulaire, avec une séparation claire entre les routes, les modèles, les formulaires, et les utilitaires. Il inclut également des tests unitaires pour assurer la robustesse du code.

## Fonctionnalités principales

### Pour tous les utilisateurs

- **Exploration des œuvres** :
  - Parcourir une liste paginée d'œuvres récentes sur la page d'accueil (`/`) avec un affichage en grille responsive.
  - Accéder à une page dédiée pour chaque œuvre (`/artwork/<id>`) avec des détails tels que le titre, la description, l'image, l'émotion cible, l'émotion détectée, et un compteur de likes.
  - Visualiser un nuage de mots généré à partir des commentaires associés à une œuvre (si disponible).
  - Consulter un graphique de répartition des votes émotionnels pour chaque œuvre.

- **Recherche avancée** :
  - Rechercher des œuvres par mot-clé (titre ou description) via un formulaire sur la page d'accueil.
  - Filtrer les œuvres par émotion cible (ex. Joie, Tristesse).
  - Trier les résultats par date (ascendant/descendant) ou par nombre de likes.

- **Navigation intuitive** :
  - Interface utilisateur moderne avec une barre de navigation responsive.
  - Pagination pour naviguer facilement entre les pages d'œuvres.
  - Messages flash pour informer des actions réussies ou des erreurs (ex. "Œuvre ajoutée avec succès").

### Pour les utilisateurs connectés

- **Authentification** :
  - Inscription avec validation des champs (nom d'utilisateur unique, email valide, mot de passe confirmé) (`/register`).
  - Connexion sécurisée avec hachage des mots de passe (`/login`).
  - Déconnexion (`/logout`).

- **Gestion du profil** :
  - Visualiser son profil avec avatar, bio, email, et liste des œuvres publiées (`/profile`).
  - Modifier le profil, y compris le nom d'utilisateur, l'email, la bio, et l'avatar (images JPEG/PNG uniquement) (`/edit_profile`).

- **Gestion des œuvres** :
  - Ajouter une œuvre avec un titre, une description, une image (JPEG/PNG, max 16MB), et une émotion cible (`/upload`).
  - Modifier une œuvre existante (titre, description, image facultative, émotion cible) (`/edit/<id>`).
  - Supprimer une œuvre avec confirmation via une boîte de dialogue (`/delete/<id>`).
  - Analyse automatique de l'émotion dans la description de l'œuvre grâce à un modèle NLP (j-hartmann/emotion-english-distilroberta-base).

- **Interactions avec les œuvres** :
  - Aimer (liker) ou retirer son like sur une œuvre (`/like/<id>`).
  - Voter pour une émotion associée à une œuvre (une seule fois par utilisateur) (`/vote/<id>`).
  - Ajouter un commentaire sur une œuvre (`/comment/<id>`).
  - Signaler une œuvre ou un commentaire inapproprié avec une raison spécifiée (`/report/<id>` ou `/report_comment/<id>`).

### Pour les administrateurs

- **Tableau de bord d'administration** (`/admin/dashboard`) :
  - Lister tous les utilisateurs, œuvres et commentaires.
  - Bloquer un utilisateur (sauf les autres administrateurs).
  - Supprimer une œuvre ou un commentaire.
  - Accéder à la page de modération.

- **Modération** (`/admin/moderation`) :
  - Consulter les signalements non résolus (œuvres ou commentaires) avec les raisons et les utilisateurs concernés.
  - Supprimer le contenu signalé ou marquer le signalement comme résolu.
  - Ignorer un signalement sans supprimer le contenu.

- **Notifications** (`/admin/notifications`) :
  - Recevoir des notifications pour chaque nouveau signalement (œuvre ou commentaire).
  - Marquer les notifications comme lues.
  - Recevoir des emails automatiques pour chaque signalement (configurable via Mailtrap ou un autre serveur SMTP).

- **Commandes CLI** :
  - Initialiser les émotions par défaut dans la base de données (`flask emotion init`).
  - Insérer des utilisateurs prédéfinis pour les tests ou la démo (`flask user init`).

## Architecture du projet

L'application suit une architecture modulaire avec une séparation claire des responsabilités :

- **Configuration** :
  - `config.py` : Définit les paramètres globaux (clé secrète, URI de la base de données, configuration email, etc.).
  - `instance/config.py` : Contient les configurations sensibles (non versionnées).

- **Application principale** :
  - `app/__init__.py` : Initialise l'application Flask, les extensions (SQLAlchemy, Flask-Login, Flask-Mail, etc.), et enregistre les blueprints.
  - `run.py` : Point d'entrée pour lancer l'application, crée les tables et initialise les données (émotions, utilisateurs).

- **Modèles** (`app/models.py`) :
  - Définit les entités de la base de données : `User`, `Artwork`, `Emotion`, `Vote`, `Comment`, `Report`, `Notification`, `Like`.
  - Relations entre les entités (ex. un utilisateur peut avoir plusieurs œuvres, une œuvre peut avoir plusieurs commentaires).

- **Formulaires** (`app/forms.py`) :
  - Formulaires Flask-WTF pour la connexion, l'inscription, l'ajout/modification d'œuvres, et la gestion du profil.
  - Validations des champs (ex. email valide, extensions de fichiers autorisées).

- **Routes** (`app/routes/`) :
  - `main.py` : Routes publiques pour la page d'accueil, la recherche, et les pages d'œuvres.
  - `auth.py` : Routes pour l'authentification (connexion, inscription, déconnexion).
  - `user.py` : Routes pour la gestion du profil et des œuvres.
  - `interactions.py` : Routes pour les interactions (likes, votes, commentaires, signalements).
  - `admin.py` : Routes pour l'administration et la modération.

- **Utilitaires** (`app/utils/`) :
  - `emotion_analysis.py` : Analyse des émotions dans les descriptions via un modèle NLP.
  - `image_processing.py` : Validation et redimensionnement des images téléchargées.
  - `security.py` : Nettoyage des entrées utilisateur et gestion des mots de passe.
  - `wordcloud_generator.py` : Génération de nuages de mots à partir des commentaires.
  - `decorators.py` : Décorateur pour restreindre l'accès aux administrateurs.

- **Templates** (`app/templates/`) :
  - Templates HTML avec Jinja2 pour l'interface utilisateur, basés sur Bootstrap 5.
  - Inclut des formulaires, des grilles d'œuvres, des graphiques (Chart.js), et des notifications.

- **Statique** (`app/static/`) :
  - `js/ajax.js` : Gestion des interactions asynchrones (likes, commentaires).
  - `js/charts.js` : Création de graphiques pour l'engagement (likes, commentaires).
  - `css/style.css` : Styles personnalisés pour l'interface.

- **Tests** (`tests/`) :
  - Tests unitaires pour les modèles (`test_models.py`) et les routes (`test_routes.py`).
  - Configuration des fixtures pour une base de données en mémoire (`conftest.py`).

- **Scripts utilitaires** :
  - `insert_users.py` : Script pour insérer des utilisateurs prédéfinis dans la base de données.

## Dépendances

Les dépendances sont listées dans `requirements.txt` :

```
flask
flask-sqlalchemy
flask-login
flask-wtf
flask-mail
flask-migrate
psycopg2-binary
email-validator
Pillow
transformers
werkzeug
torch
spacy
python-dotenv
wordcloud
matplotlib
pytest
pytest-flask
```

Ces dépendances incluent :
- **Flask et extensions** : Framework web, ORM, authentification, formulaires, emails, migrations.
- **Bibliothèques d'image et NLP** : Traitement des images (Pillow), analyse émotionnelle (transformers, torch), génération de nuages de mots (wordcloud).
- **Tests** : Framework de test (pytest) et intégration Flask (pytest-flask).
- **Utilitaires** : Validation des emails, gestion des variables d'environnement.

## Installation et configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- SQLite (par défaut) ou PostgreSQL (optionnel)
- Compte Mailtrap (ou autre serveur SMTP) pour les emails
- Git (pour cloner le dépôt)

### Étapes d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/gallerium.git
   cd gallerium
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement** :
   Créer un fichier `.env` dans le répertoire racine avec les variables suivantes :
   ```
   SECRET_KEY=votre_clé_secrète
   DATABASE_URL=sqlite:///gallerium.db  # Ou URL PostgreSQL
   MAIL_SERVER=smtp.mailtrap.io
   MAIL_PORT=2525
   MAIL_USE_TLS=True
   MAIL_USERNAME=votre_utilisateur_mailtrap
   MAIL_PASSWORD=votre_mot_de_passe_mailtrap
   MAIL_DEFAULT_SENDER=votre_email@example.com
   ```

5. **Initialiser la base de données** :
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Insérer les données initiales** :
   ```bash
   flask emotion init
   flask user init
   ```

### Configuration des variables d'environnement

- `SECRET_KEY` : Clé secrète pour la sécurité des sessions.
- `DATABASE_URL` : URI de la base de données (SQLite par défaut, PostgreSQL en production).
- `MAIL_*` : Configuration du serveur SMTP pour les notifications par email.
- Assurez-vous que les variables sensibles ne sont pas versionnées (utilisez `.gitignore` pour le fichier `.env`).

### Lancement de l'application

1. **Activer l'environnement virtuel** (si ce n'est pas déjà fait) :
   ```bash
   source venv/bin/activate
   ```

2. **Lancer l'application** :
   ```bash
   python run.py
   ```

3. **Accéder à l'application** :
   Ouvrez un navigateur et allez à `http://127.0.0.1:5000`.

## Tests

Le projet inclut des tests unitaires pour les modèles et les routes.

1. **Lancer les tests** :
   ```bash
   pytest
   ```

2. **Détails des tests** :
   - `test_models.py` : Vérifie la création des utilisateurs, œuvres, et émotions.
   - `test_routes.py` : Teste l'accès aux pages (index, artwork, profile, etc.) et les actions comme la suppression d'œuvres.
   - Les tests utilisent une base de données SQLite en mémoire pour éviter de modifier la base de production.

## Contribuer

Nous accueillons les contributions ! Pour contribuer :

1. **Forker le dépôt** et créer une branche pour votre fonctionnalité :
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. **Écrire du code propre** avec des tests associés.
3. **Exécuter les tests** pour s'assurer que tout fonctionne :
   ```bash
   pytest
   ```

4. **Soumettre une pull request** avec une description claire des changements.

### Bonnes pratiques

- Suivez les conventions de codage PEP 8.
- Ajoutez des tests pour chaque nouvelle fonctionnalité.
- Documentez les nouvelles fonctionnalités dans ce README.
- Évitez de modifier les fichiers sensibles (ex. `instance/config.py`) dans les commits.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.