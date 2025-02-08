from flask import request, jsonify, session
from app import app
import sqlite3
import bcrypt

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE) # Fonction pour se connecter à la base de données

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'username' in session: # Vérifier si l'utilisateur est connecté
        return jsonify({'logged_in': True, 'username': session['username'], 'is_admin': session['is_admin']})
    return jsonify({'logged_in': False})

@app.route('/update_user', methods=['POST'])
def update_user():
    if 'username' not in session: # Vérifier si l'utilisateur est connecté
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
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, current_username))

        conn.commit()
        return jsonify({'success': True, 'message': 'Informations mises à jour avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})
    finally:
        conn.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    if 'username' not in session or not session.get('is_admin'): # Vérifier si l'utilisateur est connecté et est admin
        return jsonify({'success': False, 'message': 'Accès refusé'})

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify({'success': True, 'users': [{'username': user[0], 'is_admin': user[1]} for user in users]})

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'username' not in session or not session.get('is_admin'): # Vérifier si l'utilisateur est connecté et est admin
        return jsonify({'success': False, 'message': 'Accès refusé'})

    data = request.get_json()
    username_to_delete = data.get('username')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username_to_delete,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Utilisateur supprimé avec succès'})

@app.route('/admin_update_user', methods=['POST'])
def admin_update_user():
    if 'username' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Accès refusé'})

    data = request.get_json()
    current_username = data.get('current_username')
    new_nom = data.get('new_nom')
    new_prenom = data.get('new_prenom')
    new_username = data.get('new_username')
    new_password = data.get('new_password')
    new_question_secrete = data.get('new_question_secrete')
    new_reponse_secrete = data.get('new_reponse_secrete')
    is_admin = data.get('is_admin')

    conn = connect_db()
    cursor = conn.cursor()

    try:
        if new_username:
            cursor.execute("UPDATE users SET username=? WHERE username=?", (new_username, current_username))
        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, new_username or current_username))
        if new_nom:
            cursor.execute("UPDATE users SET nom=? WHERE username=?", (new_nom, new_username or current_username))
        if new_prenom:
            cursor.execute("UPDATE users SET prenom=? WHERE username=?", (new_prenom, new_username or current_username))
        if new_question_secrete:
            cursor.execute("UPDATE users SET question_secrete=? WHERE username=?", (new_question_secrete, new_username or current_username))
        if new_reponse_secrete:
            hashed_reponse_secrete = bcrypt.hashpw(new_reponse_secrete.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET reponse_secrete=? WHERE username=?", (hashed_reponse_secrete, new_username or current_username))
        if is_admin is not None:
            cursor.execute("UPDATE users SET is_admin=? WHERE username=?", (is_admin, new_username or current_username))

        conn.commit()
        return jsonify({'success': True, 'message': 'Informations mises à jour avec succès'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Erreur lors de la mise à jour'})
    finally:
        conn.close()
