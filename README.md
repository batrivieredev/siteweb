# Projet d'Authentification avec Flask, JavaScript et Socket.IO

## 1. Description
Ce projet est une application web simple permettant aux utilisateurs de s'inscrire, de se connecter, de gérer leur session, d'envoyer des messages et de gérer des posts de blog à l'aide de Flask (backend) et JavaScript (frontend). La base de données SQLite est utilisée pour stocker les informations des utilisateurs et des messages.

## 2. Technologies utilisées
- **Backend** : Flask (Python), Flask-SocketIO
- **Frontend** : HTML, CSS, JavaScript
- **Base de données** : SQLite
- **Sécurité** : Sessions Flask, CORS, bcrypt

## 3. Installation et Configuration

### 3.1 Prérequis
Assurez-vous d'avoir Python installé sur votre machine.

### 3.2 Étapes d'installation

#### 3.2.1 Cloner le projet
```bash
git clone https://github.com/batrivieredev/site_web.git
cd site_web
```

#### 3.2.2 Créer un environnement virtuel et l'activer
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Mac/Linux
venv\Scripts\activate  # Sur Windows
```

#### 3.2.3 Installer les dépendances
```bash
pip install flask flask-cors flask-socketio eventlet bcrypt
```

#### 3.2.4 Créer et configurer la base de données SQLite
```python
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    nom TEXT,
    prenom TEXT,
    question_secrete TEXT,
    reponse_secrete TEXT
);
""")

cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_username TEXT NOT NULL,
    receiver_username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin123', 1);")

conn.commit()
conn.close()
```

#### 3.2.5 Lancer le serveur Flask avec Socket.IO
```bash
python3 backend/run.py
```

#### 3.2.6 Ouvrir l'interface web
- Ouvrez `index.html` dans un navigateur.

---

#### 3.2.7 Obtenir les versions des dépendances installées
- Pour pouvoir utiliser le projet avec les memes versions de dépendances, il faut uliliser la commande `pip install -r requirements.txt`
- Pour obtenir les versions de toutes les bibliothèques installées dans votre environnement Python, utilisez la commande suivante :
`pip freeze`
- Et pour les ajouter directement dans un fichier requirements.txt, déja créer au préalable `pip freeze > requirements.txt`


---

## 4. Structure du projet

```
├── backend/
│   ├── __init__.py
│   ├── app.py              # Configuration de l'application Flask et Socket.IO
│   ├── auth.py             # Routes d'authentification
│   ├── blog.py             # Routes pour les posts de blog
│   ├── messages.py         # Routes pour la messagerie
│   ├── run.py              # Script pour démarrer le serveur Flask avec Socket.IO
│   └── user.py             # Routes pour la gestion des utilisateurs
├── frontend/
│   ├── index.html          # Page de connexion et d'inscription
│   ├── welcome_user.html   # Page d'accueil pour les utilisateurs
│   ├── welcome_admin.html  # Page d'accueil pour les administrateurs
│   ├── script.js           # Logique frontend (connexion, inscription, session, messagerie...)
│   └── style.css           # Styles CSS pour les pages HTML
├── images/
│   ├── background1.jpeg    # Image de fond page accueil index.html
│   └── background.jpg      # Image de fond
├── requirements.txt        # Fichier de requirements
└── data.db                 # Base de données SQLite
```

---

## 5. Fonctionnalités

### 5.1 Backend (Flask)
- **/login** : Authentifie un utilisateur avec un nom d'utilisateur et un mot de passe.
- **/logout** : Déconnecte l'utilisateur en supprimant la session.
- **/register** : Crée un compte utilisateur avec un nom d'utilisateur unique.
- **/check_session** : Vérifie si un utilisateur est connecté.
- **/update_user** : Met à jour les informations de l'utilisateur connecté.
- **/get_users** : Récupère la liste des utilisateurs (admin uniquement).
- **/delete_user** : Supprime un utilisateur (admin uniquement).
- **/admin_update_user** : Met à jour les informations d'un utilisateur (admin uniquement).
- **/send_message** : Envoie un message entre utilisateurs.
- **/get_messages** : Récupère tous les messages.
- **/get_posts** : Récupère tous les posts de blog.
- **/create_post** : Crée un nouveau post de blog (admin uniquement).
- **/delete_post** : Supprime un post de blog (admin uniquement).
- **/get_logs** : Récupère les logs du système (admin uniquement).

### 5.2 Frontend (JavaScript)
- Formulaire d'inscription et de connexion avec gestion des erreurs.
- Redirection automatique après connexion vers `welcome_user.html` ou `welcome_admin.html`.
- Vérification de session pour empêcher l'accès non autorisé.
- Déconnexion avec redirection vers `index.html`.
- Envoi et réception de messages en temps réel avec Socket.IO.
- Gestion des posts de blog pour les administrateurs.

---

## 6. Idées Améliorations possibles qui vont êtres mises à jour plus tard sur le site
- Minification des fichiers Javascript et CSS, réduire leur taille et en faire plusieurs pour améliorer la vitesse de chargement.
- Ajout de notifications pour les nouveaux messages et les nouveaux posts en tant réel
- Voir pour une gestion par Https
- Limitation de tentative de connexion
- verification que le site s'adapte bien à tout type d'appareil
- Amélioration du Css et du site avec Bootstrap
- Ajout d'une barre de recherche pour les posts
- Ajout d'un systeme de commentaire pour les posts du blog
- Ajout de role suplémentaires comme modérateur, éditeurs...
- Rédiger une documentation complète pour les administrateurs et les utilisateurs.

---

## 7. Auteur
- **Nom** : Baptiste RIVIERE
- **Email** : [baptiste.rivierefr@gmail.com](mailto:baptiste.rivierefr@gmail.com)

---

## Commits
- **4e3c610132276cb315c22de96e8777ed7d858a4e** : Site fonctionne correctement sans erreurs
