from flask import request, jsonify, session
from app import app
import sqlite3
import bcrypt
import random
import string

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE) # Fonction pour se connecter à la base de données

def generate_temp_password(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

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
        return jsonify({'success': True, 'message': 'Connexion réussie', 'is_admin': user[1]})
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

@app.route('/recover_password', methods=['POST'])
def recover_password():
    data = request.get_json()
    username = data.get('username')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        temp_password = generate_temp_password()
        hashed_password = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Mot de passe temporaire généré', 'temp_password': temp_password})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur non trouvé'})
