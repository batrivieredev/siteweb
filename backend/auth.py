# Import necessary modules from Flask and other libraries
from flask import request, jsonify, session
from app import app
import sqlite3
import bcrypt
import random
import string

# Define the database file
DATABASE = "data.db"

# Function to connect to the database
def connect_db():
    return sqlite3.connect(DATABASE)

# Function to generate a temporary password
def generate_temp_password(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')  # Extract username
    password = data.get('password').encode('utf-8')  # Extract and encode password

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT password, is_admin FROM users WHERE username=?", (username,))  # Query the database for the user
    user = cursor.fetchone()  # Fetch the result
    conn.close()  # Close the database connection

    # Check if user exists and password matches
    if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
        session['username'] = username  # Set session username
        session['is_admin'] = user[1]  # Set session admin status
        return jsonify({'success': True, 'message': 'Connexion réussie', 'is_admin': user[1]})  # Return success response
    else:
        return jsonify({'success': False, 'message': 'Identifiants incorrects'})  # Return failure response

# Route for user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove username from session
    session.pop('is_admin', None)  # Remove admin status from session
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})  # Return success response

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')  # Extract username
    password = data.get('password').encode('utf-8')  # Extract and encode password
    nom = data.get('nom')  # Extract last name
    prenom = data.get('prenom')  # Extract first name
    question_secrete = data.get('question_secrete')  # Extract secret question
    reponse_secrete = data.get('reponse_secrete')  # Extract secret answer

    # Check if secret answer is provided
    if not reponse_secrete:
        return jsonify({'success': False, 'message': 'La réponse à la question secrète est requise.'}), 400

    reponse_secrete = reponse_secrete.encode('utf-8')  # Encode secret answer
    is_admin = data.get('is_admin', False)  # Extract admin status, default to False
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')  # Hash the password
    hashed_reponse_secrete = bcrypt.hashpw(reponse_secrete, bcrypt.gensalt()).decode('utf-8')  # Hash the secret answer

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    try:
        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password, is_admin, nom, prenom, question_secrete, reponse_secrete) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (username, hashed_password, is_admin, nom, prenom, question_secrete, hashed_reponse_secrete))
        conn.commit()  # Commit the transaction
        return jsonify({'success': True, 'message': 'Utilisateur créé avec succès'})  # Return success response
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur déjà pris'})  # Return failure response if username is taken
    finally:
        conn.close()  # Close the database connection

# Route to get the secret question for a user
@app.route('/get_secret_question', methods=['POST'])
def get_secret_question():
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')  # Extract username

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT question_secrete FROM users WHERE username=?", (username,))  # Query the database for the secret question
    user = cursor.fetchone()  # Fetch the result
    conn.close()  # Close the database connection

    # Check if user exists
    if user:
        return jsonify({'success': True, 'question_secrete': user[0]})  # Return success response with secret question
    else:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur non trouvé'})  # Return failure response if user not found

# Route to reset the password
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')  # Extract username
    reponse_secrete = data.get('reponse_secrete')  # Extract secret answer

    # Check if secret answer is provided
    if not reponse_secrete:
        return jsonify({'success': False, 'message': 'La réponse à la question secrète est requise.'}), 400

    reponse_secrete = reponse_secrete.encode('utf-8')  # Encode secret answer

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT reponse_secrete FROM users WHERE username=?", (username,))  # Query the database for the secret answer
    user = cursor.fetchone()  # Fetch the result

    # Check if user exists and secret answer matches
    if user and bcrypt.checkpw(reponse_secrete, user[0].encode('utf-8')):
        temp_password = generate_temp_password()  # Generate a temporary password
        hashed_password = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hash the temporary password
        cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))  # Update the user's password in the database
        conn.commit()  # Commit the transaction
        conn.close()  # Close the database connection
        return jsonify({'success': True, 'message': 'Mot de passe temporaire généré', 'temp_password': temp_password})  # Return success response with temporary password
    else:
        conn.close()  # Close the database connection
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur ou réponse secrète incorrecte'})  # Return failure response if user not found or secret answer incorrect
