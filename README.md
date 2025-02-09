```markdown
# Projet d'Authentification avec Flask et JavaScript

## Description
Ce projet est une application web simple qui permet aux utilisateurs de s'inscrire, de se connecter et de gérer leur session à l'aide de Flask (backend) et JavaScript (frontend). La base de données SQLite est utilisée pour stocker les informations des utilisateurs.

## Technologies utilisées
- **Backend** : Flask (Python)
- **Frontend** : HTML, CSS, JavaScript
- **Base de données** : SQLite
- **Sécurité** : Sessions Flask, CORS

## Installation et Configuration
### Prérequis
Assurez-vous d'avoir Python installé sur votre machine.

### Étapes d'installation
1. **Cloner le projet**
   ```bash
   git clone https://github.com/batrivieredev/site_web.git
   cd site_web
   ```

2. **Créer un environnement virtuel et l'activer**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Mac/Linux
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install flask flask-cors
   ```

4. **Créer et configurer la base de données SQLite**
   ```bash
   python
   >>> import sqlite3
   >>> conn = sqlite3.connect('data.db')
   >>> cursor = conn.cursor()
   >>> cursor.execute("""
   CREATE TABLE users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL
   );
   """)
   >>> cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123');")
   >>> cursor.execute("DELETE FROM users WHERE id = 1;")
   >>> conn.commit()
   >>> conn.close()
   ```

5. **Lancer le serveur Flask**
   ```bash
   python server.py
   ```

6. **Ouvrir l'interface web**
   Ouvrez `index.html` dans un navigateur.

## Structure du projet
```
/
│── server.py              # Backend Flask
│── data.db                # Base de données SQLite
│── index.html             # Page de connexion et d'inscription
│── welcome.html           # Page d'accueil après connexion
│── script.js              # Logique frontend (connexion, inscription, session...)
│── style.css              # Styles CSS pour les pages HTML
│── images/
│   └── icone.png          # Icône utilisateur
```

## Fonctionnalités
### Backend (Flask)
- **/login** : Authentifie un utilisateur avec un nom d'utilisateur et un mot de passe.
- **/register** : Crée un compte utilisateur avec un nom d'utilisateur unique.
- **/check_session** : Vérifie si un utilisateur est connecté.
- **/logout** : Déconnecte l'utilisateur en supprimant la session.

### Frontend (JavaScript)
- Formulaire d'inscription et de connexion avec gestion des erreurs.
- Redirection automatique après connexion vers `welcome.html`.
- Vérification de session pour empêcher l'accès non autorisé.
- Déconnexion avec redirection vers `index.html`.

## Améliorations possibles
- Ajout d'un système de récupération de mot de passe.

## Auteur
- **Nom** : Baptiste RIVIERE
- **Email** : baptiste.rivierefr@gmail.com


