from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import bcrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "votre_cle_secrete"

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password, user[0]):
        session['username'] = username
        return jsonify({'success': True, 'message': 'Connexion réussie'})
    else:
        return jsonify({'success': False, 'message': 'Identifiants incorrects'})

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    return jsonify({'logged_in': False})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({'success': True, 'message': 'Utilisateur créé avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})
    finally:
        conn.close()

@app.route('/update_user', methods=['POST'])
def update_user():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Utilisateur non connecté'})

    data = request.get_json()
    new_username = data.get('username')
    new_password = data.get('password')

    conn = connect_db()
    cursor = conn.cursor()

    try:
        current_username = session['username']  # Sauvegarde du nom actuel

        if new_username:
            cursor.execute("UPDATE users SET username=? WHERE username=?", (new_username, current_username))
            session['username'] = new_username  # Mettre à jour la session immédiatement
            current_username = new_username  # Mise à jour du nom pour la requête suivante

        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, current_username))

        conn.commit()
        return jsonify({'success': True, 'message': 'Informations mises à jour avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
