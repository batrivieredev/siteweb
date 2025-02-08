from flask import request, jsonify, session
from app import app
import sqlite3

DATABASE = "data.db"

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/get_posts', methods=['GET'])
def get_posts():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, author, created_at FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()

    return jsonify({'success': True, 'posts': [{'id': post[0], 'title': post[1], 'content': post[2], 'author': post[3], 'created_at': post[4]} for post in posts]})

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Accès refusé'})

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    author = session['username']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Post créé avec succès'})

@app.route('/delete_post', methods=['POST'])
def delete_post():
    if 'username' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Accès refusé'})

    data = request.get_json()
    post_id = data.get('id')

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Post supprimé avec succès'})
