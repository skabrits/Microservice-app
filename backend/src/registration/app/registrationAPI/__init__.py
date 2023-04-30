from flask import Flask

app = Flask(__name__)

CORS(app)

from registration.API import views