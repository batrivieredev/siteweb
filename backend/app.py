from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "votre_cle_secrete"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Importer les routes
import auth
import user
import blog
import messages
