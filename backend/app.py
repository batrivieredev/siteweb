from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True) # Permettre les requêtes CORS avec les cookies
app.secret_key = "votre_cle_secrete" # Clé secrète pour les sessions

# Importer les routes
import auth
import user
