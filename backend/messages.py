from flask import request, jsonify, session
from app import app, socketio
import sqlite3

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_username, receiver_username, message) VALUES (?, ?, ?)",
                   (sender, receiver, message))
    conn.commit()
    conn.close()

    socketio.emit('new_message', {'sender': sender, 'receiver': receiver, 'message': message}, broadcast=True)
    return jsonify({'success': True, 'message': 'Message envoyé avec succès'})

@app.route('/get_messages', methods=['POST'])
def get_messages():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, sender_username, receiver_username, message, timestamp FROM messages ORDER BY timestamp")
    messages = cursor.fetchall()
    conn.close()

    return jsonify({'success': True, 'messages': [{'id': msg[0], 'sender': msg[1], 'receiver': msg[2], 'message': msg[3], 'timestamp': msg[4]} for msg in messages]})

@app.route('/delete_message', methods=['POST'])
def delete_message():
    if 'username' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Accès refusé'})

    data = request.get_json()
    message_id = data.get('id')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id=?", (message_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Message supprimé avec succès'})

@socketio.on('send_message')
def handle_send_message_event(data):
    sender = data['sender']
    receiver = data['receiver']
    message = data['message']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_username, receiver_username, message) VALUES (?, ?, ?)",
                   (sender, receiver, message))
    conn.commit()
    conn.close()

    socketio.emit('new_message', {'sender': sender, 'receiver': receiver, 'message': message}, broadcast=True)
