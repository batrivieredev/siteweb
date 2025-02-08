# Importing the socketio and app instances from the app module
from app import socketio, app

# Importing the eventlet library, which is used for asynchronous networking
import eventlet

# If this script is run directly (not imported as a module), start the socketio server
if __name__ == '__main__':
    # Running the socketio server with the Flask app in debug mode
    socketio.run(app, debug=True)
