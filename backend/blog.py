from flask import request, jsonify, session  # Import Flask modules for handling requests, JSON responses, and sessions
from app import app  # Import the Flask app instance from the app module
import sqlite3  # Import the sqlite3 module for database operations
import subprocess

DATABASE = "data.db"  # Define the database file name

def connect_db():
    return sqlite3.connect(DATABASE)  # Function to connect to the SQLite database

@app.route('/get_posts', methods=['GET'])  # Define a route for getting posts with the GET method
def get_posts():
    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to interact with the database
    cursor.execute("SELECT id, title, content, author, created_at FROM posts ORDER BY created_at DESC")  # Execute a SQL query to select all posts ordered by creation date
    posts = cursor.fetchall()  # Fetch all results from the executed query
    conn.close()  # Close the database connection

    # Return a JSON response with the fetched posts
    return jsonify({'success': True, 'posts': [{'id': post[0], 'title': post[1], 'content': post[2], 'author': post[3], 'created_at': post[4]} for post in posts]})

@app.route('/create_post', methods=['POST'])  # Define a route for creating a post with the POST method
def create_post():
    if 'username' not in session or not session.get('is_admin'):  # Check if the user is logged in and is an admin
        return jsonify({'success': False, 'message': 'Accès refusé'})  # Return a JSON response indicating access is denied

    data = request.get_json()  # Get the JSON data from the request
    title = data.get('title')  # Extract the title from the JSON data
    content = data.get('content')  # Extract the content from the JSON data
    author = session['username']  # Get the username from the session

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to interact with the database
    cursor.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))  # Execute a SQL query to insert a new post
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

    return jsonify({'success': True, 'message': 'Post créé avec succès'})  # Return a JSON response indicating the post was created successfully

@app.route('/delete_post', methods=['POST'])  # Define a route for deleting a post with the POST method
def delete_post():
    if 'username' not in session or not session.get('is_admin'):  # Check if the user is logged in and is an admin
        return jsonify({'success': False, 'message': 'Accès refusé'})  # Return a JSON response indicating access is denied

    data = request.get_json()  # Get the JSON data from the request
    post_id = data.get('id')  # Extract the post ID from the JSON data

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to interact with the database
    cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))  # Execute a SQL query to delete the post with the given ID
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

    return jsonify({'success': True, 'message': 'Post supprimé avec succès'})  # Return a JSON response indicating the post was deleted successfully

@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        logs = subprocess.check_output(['tail', '-n', '100', '/var/log/syslog']).decode('utf-8')
        return jsonify({'success': True, 'logs': logs})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_post', methods=['POST'])
def update_post():
    data = request.get_json()
    post_id = data.get('id')
    title = data.get('title')
    content = data.get('content')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Post mis à jour avec succès'})
