from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
login = LoginManager(app)
db = MongoEngine(app)
CORS(app)

from app import routes