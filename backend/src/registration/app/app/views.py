from flask import Flask
from flask import request
from registrationLogic import user
from app import app
import json

@app.route("/")
def index():
    response = {"status": 200, "msg": "hello"}
    return json.dumps(response)

@app.route("/api/registr", methods=['POST'])
def posted():
    response = {"status": 400}
    if request.method == 'POST':
        username = request.form["login"]
        password = request.form["password"]
        
    return json.dumps(response)