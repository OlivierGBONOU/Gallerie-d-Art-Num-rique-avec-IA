# README - Gallerium

## Introduction

Gallerium est une plateforme web interactive conçue pour permettre aux utilisateurs de partager, découvrir et interagir avec des œuvres d'art numériques. Construite avec le framework **Flask** en Python, cette application offre une expérience utilisateur riche, intégrant des fonctionnalités telles que l'upload d'œuvres, l'analyse des émotions, les interactions sociales (likes, commentaires, votes), ainsi qu'un panneau d'administration robuste pour la modération. Ce README fournit une description détaillée et complète du projet, de son architecture, de ses fonctionnalités, et des instructions pour son utilisation et son développement.

---

## Fonctionnalités Principales

Gallerium propose une gamme complète de fonctionnalités pour les utilisateurs et les administrateurs, décrites ci-dessous :

### 1. **Gestion des Utilisateurs**
- **Inscription et Connexion** : Les utilisateurs peuvent créer un compte avec un nom d'utilisateur, un email et un mot de passe, ou se connecter à un compte existant. Les mots de passe sont hachés de manière sécurisée avec `pbkdf2:sha256`.
- **Profil Utilisateur** : Chaque utilisateur dispose d'une page de profil où il peut voir ses informations (nom d'utilisateur, email, bio, avatar) et ses œuvres publiées. Les utilisateurs peuvent modifier leur profil, y compris leur avatar et leur bio.
- **Authentification Sécurisée** : Utilisation de `Flask-Login` pour gérer les sessions utilisateur et de `Flask-WTF` pour la protection CSRF.

### 2. **Gestion des Œuvres**
- **Upload d'Œuvres** : Les utilisateurs authentifiés peuvent télécharger des œuvres d'art (images au format JPEG ou PNG) accompagnées d'un titre, d'une description et d'une émotion cible (parmi une liste prédéfinie : Joie, Tristesse, Colère, Peur, Surprise, Dégoût).
- **Édition et Suppression** : Les utilisateurs peuvent modifier ou supprimer leurs propres œuvres via une interface dédiée.
- **Analyse des Émotions** : Lors de l'upload ou de la modification d'une œuvre, une analyse automatique des émotions est effectuée sur la description grâce à un modèle NLP pré-entraîné (`j-hartmann/emotion-english-distilroberta-base`).
- **Traitement des Images** : Les images téléchargées sont validées (JPEG/PNG uniquement) et redimensionnées pour optimiser l'espace de stockage (taille maximale : 800x800 pixels).

### 3. **Interactions Sociales**
- **Likes** : Les utilisateurs authentifiés peuvent liker ou retirer leur like sur une œuvre. Le nombre total de likes est affiché.
- **Votes Émotionnels** : Les utilisateurs peuvent voter pour associer une émotion à une œuvre, ce qui permet de comparer l'émotion cible (définie par l'auteur) avec les perceptions des autres utilisateurs.
- **Commentaires** : Les utilisateurs peuvent ajouter des commentaires sur les œuvres. Un nuage de mots (wordcloud) est généré à partir des commentaires pour visualiser les termes les plus fréquents.
- **Signalements** : Les utilisateurs peuvent signaler une œuvre ou un commentaire inapproprié, avec une raison obligatoire. Les signalements sont envoyés aux administrateurs via des notifications et des emails.

### 4. **Recherche et Navigation**
- **Page d'Accueil** : Affiche une liste paginée des œuvres récentes (8 par page), avec un aperçu de l'image, du titre et de l'auteur.
- **Recherche Avancée** : Les utilisateurs peuvent rechercher des œuvres par mot-clé (titre ou description), filtrer par émotion cible, et trier par date (croissant/décroissant) ou nombre de likes.
- **Pagination** : La navigation entre les pages est intuitive, avec des liens pour les pages précédentes/suivantes.

### 5. **Administration**
- **Tableau de Bord Admin** : Accessible uniquement aux utilisateurs marqués comme administrateurs (`is_admin=True`), il affiche un aperçu des utilisateurs, œuvres et commentaires, avec des actions rapides (bloquer un utilisateur, supprimer une œuvre ou un commentaire).
- **Modération des Signalements** : Les administrateurs peuvent consulter les signalements non résolus, supprimer le contenu signalé (œuvre ou commentaire) ou marquer le signalement comme résolu.
- **Notifications Admin** : Les signalements génèrent des notifications pour les administrateurs, visibles dans une interface dédiée. Les notifications peuvent être marquées comme lues.
- **Envoi d'Emails** : Lorsqu'un signalement est soumis, un email est envoyé à chaque administrateur via un serveur SMTP (Mailtrap par défaut pour les tests).

### 6. **Fonctionnalités Techniques**
- **Base de Données** : Utilisation de **SQLAlchemy** avec une base SQLite par défaut (configurable via `SQLALCHEMY_DATABASE_URI`). Les modèles incluent `User`, `Artwork`, `Emotion`, `Vote`, `Comment`, `Report`, `Notification`, et `Like`.
- **Sécurité** : 
  - Protection CSRF via `Flask-WTF`.
  - Sanitisation des entrées utilisateur pour éviter les injections XSS/SQL.
  - Validation des fichiers uploadés pour garantir leur format et leur intégrité.
- **Logging** : Les erreurs sont enregistrées dans un fichier `error.log` (rotation des fichiers pour limiter la taille).
- **Tests Unitaires** : Tests pour les modèles et les routes principales, utilisant **Pytest** avec une base de données en mémoire.
- **CLI Personnalisée** : Commandes CLI pour initialiser les émotions (`flask emotion init`) et les utilisateurs (commentées dans le code).

---

## Architecture du Projet

Le projet suit une structure modulaire et organisée, typique d'une application Flask. Voici une vue d'ensemble des dossiers et fichiers principaux :

### Structure des Dossiers

```
gallerium/
├── app/
│   ├── routes/
│   │   ├── admin.py        # Routes pour l'administration
│   │   ├── auth.py         # Routes pour l'authentification
│   │   ├── interactions.py # Routes pour les interactions (likes, votes, commentaires, signalements)
│   │   ├── main.py         # Routes principales (accueil, recherche, page d'œuvre)
│   │   ├── user.py         # Routes pour la gestion du profil et des œuvres
│   │   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   ├── images/
│   │   ├── uploads/        # Dossier pour les images téléchargées
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── moderation.html
│   │   ├── artwork.html
│   │   ├── base.html
│   │   ├── edit.html
│   │   ├── edit_profile.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── notifications.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   ├── upload.html
│   ├── utils/
│   │   ├── decorators.py       # Décorateurs personnalisés (ex. admin_required)
│   │   ├── emotion_analysis.py  # Analyse des émotions via NLP
│   │   ├── image_processing.py  # Traitement des images
│   │   ├── security.py         # Fonctions de sécurité
│   │   ├── wordcloud_generator.py # Génération de nuages de mots
│   ├── __init__.py             # Initialisation de l'application Flask
│   ├── forms.py                # Formulaires Flask-WTF
│   ├── models.py               # Modèles SQLAlchemy
├── instance/
│   ├── config.py               # Configuration privée (non versionnée)
├── tests/
│   ├── conftest.py             # Configuration des tests Pytest
│   ├── test_models.py          # Tests des modèles
│   ├── test_routes.py          # Tests des routes
│   ├── __init__.py
├── .gitignore
├── config.py                   # Configuration principale
├── README.md
├── requirements.txt            # Dépendances Python
├── run.py                      # Script de lancement
```

### Fichiers Clés

1. **config.py** : Contient la classe `Config` avec les paramètres de l'application (clé secrète, URI de la base de données, configuration email, dossier d'upload, etc.).
2. **run.py** : Script principal pour lancer l'application. Crée les tables de la base de données si elles n'existent pas.
3. **app/__init__.py** : Initialise l'application Flask, configure les extensions (`SQLAlchemy`, `Flask-Login`, `Flask-WTF`, `Flask-Mail`, `Flask-Migrate`), et enregistre les blueprints.
4. **app/models.py** : Définit les modèles SQLAlchemy pour la gestion des données (utilisateurs, œuvres, émotions, etc.).
5. **app/forms.py** : Définit les formulaires Flask-WTF pour l'inscription, la connexion, l'upload d'œuvres, etc.
6. **app/utils/** : Contient des modules utilitaires pour l'analyse des émotions, le traitement des images, la sécurité, et la génération de nuages de mots.
7. **app/templates/** : Contient les templates HTML Jinja2 pour l'interface utilisateur, avec un design responsive basé sur Bootstrap 5.
8. **app/static/** : Contient les fichiers statiques (CSS, images, uploads).
9. **tests/** : Contient les tests unitaires pour valider les modèles et les routes.

---

## Prérequis

Pour exécuter ou développer Gallerium, assurez-vous d'avoir les outils suivants installés :

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Virtualenv** (recommandé pour isoler les dépendances)
- **SQLite** (inclus avec Python, utilisé par défaut)
- Un serveur SMTP pour les emails (Mailtrap recommandé pour les tests)

### Dépendances

Les dépendances sont listées dans `requirements.txt`. Les principales incluent :

- `Flask` : Framework web
- `Flask-SQLAlchemy` : ORM pour la base de données
- `Flask-Login` : Gestion des sessions utilisateur
- `Flask-WTF` : Gestion des formulaires et CSRF
- `Flask-Mail` : Envoi d'emails
- `Flask-Migrate` : Gestion des migrations de base de données
- `transformers` : Analyse NLP des émotions
- `Pillow` : Traitement des images
- `wordcloud` : Génération de nuages de mots
- `pytest` : Tests unitaires

Installez-les avec :

```bash
pip install -r requirements.txt
```

---

## Installation et Configuration

### 1. Cloner le Répertoire

```bash
git clone <url-du-répertoire>
cd gallerium
```

### 2. Créer un Environnement Virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les Variables d'Environnement

Créez un fichier `.env` à la racine du projet pour définir les variables sensibles :

```env
SECRET_KEY=votre_clé_secrète
DATABASE_URL=sqlite:///gallerium.db
MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=votre_username_mailtrap
MAIL_PASSWORD=votre_password_mailtrap
MAIL_DEFAULT_SENDER=votre_email@example.com
```

Chargez ces variables avec `python-dotenv` (inclus dans `requirements.txt`).

### 5. Initialiser la Base de Données

Exécutez le script principal pour créer les tables :

```bash
python run.py
```

Vous pouvez également utiliser Flask-Migrate pour gérer les migrations :

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Initialiser les Émotions (Optionnel)

Pour ajouter les émotions par défaut à la base de données, décommentez et exécutez la commande CLI dans `app/__init__.py` :

```bash
flask emotion init
```

### 7. Lancer l'Application

```bash
python run.py
```

L'application sera accessible à `http://127.0.0.1:5000`.

---

## Utilisation

### Interface Utilisateur

1. **Accueil** : Parcourez les œuvres récentes ou utilisez la barre de recherche pour filtrer par mot-clé, émotion ou tri.
2. **Inscription/Connexion** : Créez un compte ou connectez-vous pour accéder aux fonctionnalités d'upload et d'interaction.
3. **Profil** : Consultez vos œuvres, modifiez votre profil, ou ajoutez une nouvelle œuvre.
4. **Œuvres** : Consultez une œuvre, votez pour une émotion, ajoutez un commentaire, ou signalez un contenu inapproprié.
5. **Administration** : Si vous êtes administrateur, accédez au tableau de bord pour gérer les utilisateurs, œuvres, commentaires, et signalements.

### Interface Admin

- **Tableau de Bord** : Vue d'ensemble des utilisateurs, œuvres et commentaires avec options de suppression/bannissement.
- **Modération** : Traitez les signalements en supprimant le contenu ou en les marquant comme résolus.
- **Notifications** : Consultez et gérez les notifications des signalements.

---

## Tests

Les tests unitaires sont situés dans le dossier `tests/`. Pour les exécuter :

```bash
pytest
```

Les tests couvrent :
- La création des modèles (`User`, `Artwork`, `Emotion`).
- Les routes principales (accueil, page d'œuvre, profil, édition/suppression d'œuvre, édition de profil).

Les tests utilisent une base de données SQLite en mémoire et désactivent le CSRF pour simplifier les requêtes.

---

## Sécurité

Gallerium intègre plusieurs mesures de sécurité :
- **Hachage des Mots de Passe** : Utilisation de `pbkdf2:sha256`.
- **Protection CSRF** : Via `Flask-WTF`.
- **Sanitisation des Entrées** : Pour éviter les injections XSS/SQL.
- **Validation des Fichiers** : Seuls les fichiers JPEG/PNG sont acceptés, avec redimensionnement pour limiter l'utilisation des ressources.
- **Autorisations** : Les routes sensibles (édition, suppression, administration) vérifient l'authentification et les permissions.

---

## Limitations et Améliorations Futures

### Limitations
- **Analyse des Émotions** : Le modèle NLP est limité aux émotions prédéfinies et peut manquer de précision pour des textes complexes.
- **Base de Données** : SQLite est utilisé par défaut, ce qui peut poser des problèmes de performance pour un grand nombre d'utilisateurs.
- **Emails** : La configuration Mailtrap est destinée aux tests ; un serveur SMTP de production est nécessaire pour une utilisation réelle.
- **Tests** : Les tests unitaires couvrent les fonctionnalités principales, mais des tests d'intégration et de charge seraient utiles.

### Améliorations Possibles
- Ajouter une analyse des émotions basée sur les images (par exemple, avec un modèle de vision par ordinateur).
- Implémenter un système de messagerie privée entre utilisateurs.
- Ajouter des statistiques avancées (par exemple, graphiques des émotions les plus votées).
- Migrer vers une base de données plus robuste comme PostgreSQL.
- Intégrer un système de notifications en temps réel avec WebSockets.
- Améliorer l'interface utilisateur avec des animations et des filtres interactifs.

---

## Contribution

Pour contribuer au projet :
1. Forkez le répertoire.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3. Committez vos changements (`git commit -m "Ajout de nouvelle fonctionnalité"`).
4. Poussez votre branche (`git push origin feature/nouvelle-fonctionnalite`).
5. Créez une Pull Request avec une description claire des modifications.

Assurez-vous de respecter les conventions de code (PEP 8) et d'ajouter des tests pour les nouvelles fonctionnalités.

---

## Crédits

- **Framework** : Flask, Bootstrap 5
- **Bibliothèques** : Transformers (Hugging Face), Pillow, WordCloud
- **Icônes** : Font Awesome, Bootstrap Icons
- **Développeur** : [Votre Nom]

---

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.