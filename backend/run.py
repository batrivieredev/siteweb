from app import socketio, app
import eventlet

if __name__ == '__main__':
    socketio.run(app, debug=True)
