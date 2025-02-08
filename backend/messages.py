from flask import request, jsonify, session  # Import Flask modules for handling requests, JSON responses, and sessions
from app import app, socketio  # Import the Flask app and SocketIO instance
import sqlite3  # Import SQLite3 for database operations

DATABASE = "data.db"  # Define the database file

def connect_db():
    return sqlite3.connect(DATABASE)  # Function to connect to the SQLite database

@app.route('/send_message', methods=['POST'])  # Define a route for sending messages, accepting POST requests
def send_message():
    data = request.get_json()  # Get JSON data from the request
    sender = data.get('sender')  # Extract the sender from the JSON data
    receiver = data.get('receiver')  # Extract the receiver from the JSON data
    message = data.get('message')  # Extract the message from the JSON data

    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to execute SQL queries
    cursor.execute("INSERT INTO messages (sender_username, receiver_username, message) VALUES (?, ?, ?)",
                   (sender, receiver, message))  # Insert the message into the database
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

    socketio.emit('new_message', {'sender': sender, 'receiver': receiver, 'message': message}, broadcast=True)  # Emit the new message event via SocketIO
    return jsonify({'success': True, 'message': 'Message envoyé avec succès'})  # Return a success response

@app.route('/get_messages', methods=['POST'])  # Define a route for retrieving messages, accepting POST requests
def get_messages():
    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object to execute SQL queries
    cursor.execute("SELECT id, sender_username, receiver_username, message, timestamp FROM messages ORDER BY timestamp")  # Retrieve all messages ordered by timestamp
    messages = cursor.fetchall()  # Fetch all results from the executed query
    conn.close()  # Close the database connection

    return jsonify({'success': True, 'messages': [{'id': msg[0], 'sender': msg[1], 'receiver': msg[2], 'message': msg[3], 'timestamp': msg[4]} for msg in messages]})  # Return the messages in JSON format
