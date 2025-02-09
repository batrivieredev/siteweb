# Projet d'Authentification avec Flask, JavaScript et Socket.IO

## 1. Description
Ce projet est une application web simple permettant aux utilisateurs de s'inscrire, de se connecter, de gérer leur session, d'envoyer des messages et de gérer des posts de blog à l'aide de Flask (backend) et JavaScript (frontend). La base de données SQLite est utilisée pour stocker les informations des utilisateurs et des messages.

## 2. Technologies utilisées
- **Backend** : Flask (Python), Flask-SocketIO
- **Frontend** : HTML, CSS, JavaScript
- **Base de données** : SQLite
- **Sécurité** : Sessions Flask, CORS

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
python -m venv venv
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
python backend/run.py
```

#### 3.2.6 Ouvrir l'interface web
Ouvrez `index.html` dans un navigateur.

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

## 6. Améliorations possibles
- Ajout d'un système de récupération de mot de passe.
- Amélioration de l'interface utilisateur.
- Ajout de notifications pour les nouveaux messages.

---

## 7. Auteur
- **Nom** : Baptiste RIVIERE
- **Email** : [baptiste.rivierefr@gmail.com](mailto:baptiste.rivierefr@gmail.com)

---

## Commits
- **41c467d1bef856d16ec3b5f2fa9eb6e006913e2c** : Site fonctionne correctement sans erreurs
