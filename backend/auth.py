from flask import request, jsonify, session
from app import app
import sqlite3
import bcrypt

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE) # Fonction pour se connecter à la base de données

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() # Récupérer les données JSON de la requête
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password, is_admin FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password, user[0].encode('utf-8')): # Vérifier le mot de passe
        session['username'] = username
        session['is_admin'] = user[1]
        return jsonify({'success': True, 'message': 'Connexion réussie'})
    else:
        return jsonify({'success': False, 'message': 'Identifiants incorrects'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # Supprimer les informations de session
    session.pop('is_admin', None)
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')
    is_admin = data.get('is_admin', False)
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, hashed_password, is_admin))
        conn.commit()
        return jsonify({'success': True, 'message': 'Utilisateur créé avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})
    finally:
        conn.close()
