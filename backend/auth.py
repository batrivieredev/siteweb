from flask import request, jsonify, session
from app import app
import sqlite3
import bcrypt
import random
import string

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_temp_password(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password, is_admin FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
        session['username'] = username
        session['is_admin'] = user[1]
        return jsonify({'success': True, 'message': 'Connexion réussie', 'is_admin': user[1]})
    else:
        return jsonify({'success': False, 'message': 'Identifiants incorrects'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')
    nom = data.get('nom')
    prenom = data.get('prenom')
    question_secrete = data.get('question_secrete')
    reponse_secrete = data.get('reponse_secrete')

    if not reponse_secrete:
        return jsonify({'success': False, 'message': 'La réponse à la question secrète est requise.'}), 400

    reponse_secrete = reponse_secrete.encode('utf-8')
    is_admin = data.get('is_admin', False)
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    hashed_reponse_secrete = bcrypt.hashpw(reponse_secrete, bcrypt.gensalt()).decode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, is_admin, nom, prenom, question_secrete, reponse_secrete) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (username, hashed_password, is_admin, nom, prenom, question_secrete, hashed_reponse_secrete))
        conn.commit()
        return jsonify({'success': True, 'message': 'Utilisateur créé avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})
    finally:
        conn.close()

@app.route('/get_secret_question', methods=['POST'])
def get_secret_question():
    data = request.get_json()
    username = data.get('username')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT question_secrete FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'success': True, 'question_secrete': user[0]})
    else:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur non trouvé'})

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    reponse_secrete = data.get('reponse_secrete')

    if not reponse_secrete:
        return jsonify({'success': False, 'message': 'La réponse à la question secrète est requise.'}), 400

    reponse_secrete = reponse_secrete.encode('utf-8')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT reponse_secrete FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(reponse_secrete, user[0].encode('utf-8')):
        temp_password = generate_temp_password()
        hashed_password = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Mot de passe temporaire généré', 'temp_password': temp_password})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur ou réponse secrète incorrecte'})
