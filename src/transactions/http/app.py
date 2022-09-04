from flask import Flask
from flask_cors import CORS

from transactions.http.routes import register_routes

app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = False
app.config["CORS_HEADERS"] = "Content-Type"
