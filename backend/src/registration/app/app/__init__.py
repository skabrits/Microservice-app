from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = '/app/files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views