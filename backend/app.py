from flask import Flask  # Importation de la classe Flask du module flask
from flask_cors import CORS  # Importation de la classe CORS du module flask_cors pour gérer les requêtes cross-origin
from flask_socketio import SocketIO  # Importation de la classe SocketIO du module flask_socketio pour gérer les WebSockets
from flasgger import Swagger  # Importation de la classe Swagger du module flasgger

app = Flask(__name__)  # Création d'une instance de l'application Flask
CORS(app, supports_credentials=True)  # Activation de CORS pour l'application Flask avec support des credentials
app.secret_key = "votre_cle_secrete"  # Définition de la clé secrète pour les sessions Flask
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')  # Initialisation de SocketIO avec l'application Flask, autorisant toutes les origines et utilisant le mode asynchrone 'eventlet'

swagger = Swagger(app)  # Initialisation de Swagger avec l'application Flask

# Importer les routes
import auth  # Importation du module auth contenant les routes d'authentification
import user  # Importation du module user contenant les routes liées aux utilisateurs
import blog  # Importation du module blog contenant les routes liées aux blogs
import messages  # Importation du module messages contenant les routes liées aux messages
