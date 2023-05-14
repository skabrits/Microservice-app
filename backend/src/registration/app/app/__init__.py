from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = '/app/files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

from app import views