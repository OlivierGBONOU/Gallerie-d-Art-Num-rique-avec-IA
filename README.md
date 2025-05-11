# Documentation projet
## 🎯 **Projet Gallerium – Cahier des Charges Explicité**

**Gallerium** est une plateforme web collaborative destinée à l’exposition d’œuvres d’art numériques. Elle utilise l’intelligence artificielle pour analyser les émotions transmises par les œuvres et permet aux visiteurs d’interagir en exprimant leurs ressentis. L’objectif est de créer une expérience artistique collective basée sur les émotions.

---

## 1. 🎯 **Objectifs du Projet**

Le projet a plusieurs objectifs principaux :

1. **Pour les artistes** :

   * Proposer un espace personnel pour publier leurs créations numériques.
   * Obtenir une **analyse émotionnelle automatique** de leur œuvre, générée par IA à partir de la description textuelle.

2. **Pour les visiteurs** :

   * Explorer les œuvres, interagir avec elles en exprimant leurs émotions (via un système de votes).
   * Commenter les œuvres librement pour enrichir les retours artistiques.

3. **Pour la communauté** :

   * Afficher des visualisations collectives des émotions perçues (graphiques, nuages de mots).
   * Encourager une lecture participative et émotionnelle de l’art.

---

## 2. 🔧 **Fonctionnalités Attendues**

### 2.1. 👤 **Fonctionnalités Utilisateur (Frontend + Backend)**

* **Inscription / Connexion / Déconnexion**

  * Authentification sécurisée via **Flask-Login**.

* **Gestion de profil**

  * Création de profil avec photo/avatar, bio, et affichage de la galerie personnelle.

* **Ajout d’œuvres**

  * Upload d’images (formats `.jpg` ou `.png`, max 5 Mo).
  * Champs obligatoires : titre, description, mots-clés.
  * L’artiste choisit une **émotion cible** associée à l’œuvre (ex : joie, colère, tristesse...).

* **Visualisation des œuvres**

  * Page de consultation des œuvres avec :

    * Image,
    * Informations (titre, auteur, description, émotion cible),
    * Réactions émotionnelles des visiteurs (sous forme de votes),
    * Commentaires des visiteurs.

* **Interactions**

  * Les visiteurs peuvent :

    * Voter pour une émotion ressentie.
    * Laisser des commentaires.
    * Voir la perception globale via un graphique.

---

### 2.2. 🧠 **Fonctionnalités d’Analyse IA**

* Utilisation de **modèles NLP** (type spaCy ou Hugging Face Transformers) pour :

  * Analyser la **description textuelle** des œuvres.
  * Identifier les **émotions dominantes** et les **mots-clés** pertinents.

* Résultats de l’analyse :

  * Un **histogramme des émotions** (via **Chart.js**) basé sur les réactions et l’analyse IA.
  * Un **nuage de mots** issu des commentaires des visiteurs.

---

### 2.3. 🔐 **Fonctionnalités d’Administration**

* Tableau de bord pour les administrateurs avec :

  * Modération des commentaires et œuvres signalées.
  * Suppression ou blocage de comptes.
  * Gestion des signalements (contenus inappropriés, abus, etc.).

---

## 3. 🏗️ **Architecture Technique**

### Backend

* **Flask** : gestion du serveur, des routes et sessions.
* **SQLAlchemy** : gestion de la base de données avec ORM.
* **Flask-Login** : authentification.
* **Flask-WTF** : formulaires sécurisés.
* **Pillow** ou **Cloudinary** : pour la gestion et le redimensionnement d’images.
* **Modèle NLP** : spaCy, ou un modèle de type BERT pour détecter les émotions.

### Frontend

* **HTML/CSS (Jinja2)** : templates dynamiques.
* **JavaScript** :

  * **Chart.js** : graphiques interactifs.
  * **D3.js** : visualisations avancées (optionnel).
* **AJAX** : interactions sans rechargement (votes, commentaires...).

### Base de Données (PostgreSQL)

* **Tables principales** :

  * `Users` : informations sur les comptes.
  * `Artworks` : métadonnées et fichiers des œuvres.
  * `Emotions` : émotions associées aux œuvres.
  * `Comments` : commentaires des utilisateurs.
  * `Votes` : votes émotionnels sur les œuvres.

---

## 4. 🎨 **Design & Expérience Utilisateur (UX)**

* **Interface épurée, claire, moderne**, responsive pour tous supports.
* Navigation fluide entre les galeries, les profils, et les œuvres.
* Recherche d’œuvres par **mot-clé** ou **émotion perçue**.
* Interaction simple et intuitive (voter, commenter, explorer).
* Visualisation claire des données d’analyse (graphiques, nuages de mots).

---

## 5. ⚠️ **Contraintes & Sécurité**

* Taille maximale des images : **5 Mo**.
* Système de **modération** humaine pour les œuvres et commentaires.
* Sécurité Web :

  * **Protection CSRF** avec Flask-WTF,
  * **Prévention XSS et SQL Injection** via ORM et validation stricte.
* Respect du **RGPD** :

  * Fonction de **suppression de compte**.
  * Possibilité d’anonymiser ses données.
  * Politique de confidentialité claire.

---

## 📁 Structure de Dossiers – Projet Gallerium

```
gallerium/
│
├── app/                           # Dossier principal de l'application Flask
│   ├── __init__.py               # Initialisation de l'application (Flask app factory)
│   ├── models.py                 # Modèles SQLAlchemy (Users, Artworks, Comments...)
│   ├── forms.py                  # Formulaires Flask-WTF
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Routes publiques (accueil, galerie, vue d’œuvre)
│   │   ├── auth.py              # Authentification (login, register)
│   │   ├── user.py              # Pages utilisateur (profil, upload)
│   │   ├── admin.py             # Routes admin (modération, gestion comptes)
│   ├── static/                   # Fichiers statiques (JS, CSS, images)
│   │   ├── css/
│   │   ├── js/
│   │   │   ├── charts.js        # Intégration Chart.js
│   │   │   └── ajax.js          # AJAX pour votes/commentaires
│   │   └── uploads/             # Images uploadées par les artistes
│   ├── templates/                # Fichiers HTML Jinja2
│   │   ├── base.html            # Template de base (header, footer, etc.)
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── artwork.html         # Page œuvre individuelle
│   │   └── admin/
│   │       ├── dashboard.html
│   │       └── moderation.html
│   ├── utils/
│   │   ├── emotion_analysis.py  # Module d’analyse NLP (émotions + mots-clés)
│   │   ├── image_processing.py  # Gestion images (compression, redimensionnement)
│   │   └── security.py          # Fonctions utilitaires de sécurité
│
├── config.py                     # Fichier de configuration (dev, prod, DB, clés API)
├── run.py                        # Script de lancement de l'application
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation projet
└── instance/
    └── config.py                 # Configuration privée (clé secrète, DB locale)
```

---

## 🛠️ Technologies recommandées à installer dans `requirements.txt`

```txt
Flask
Flask-Login
Flask-WTF
Flask-SQLAlchemy
Flask-Migrate
psycopg2-binary
email-validator
Pillow
transformers
torch
spacy
python-dotenv
```

---