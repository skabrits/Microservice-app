from flask import Flask
from flask import request
from registrationLogic import user
from app import app
import random
import json

@app.route("/")
def index():
    response = {"status": 200, "msg": "hello"}
    return json.dumps(response)

@app.route("/api/registr", methods=['POST'])
def posted():
    response = {"status": 400}
    if request.method == 'POST':
        print("registr attempt")
        username = request.form["login"]
        password = request.form["password"]
        user_id = register(username, password)
        response = {"status": 200, "ID": user_id}
        
    return json.dumps(response)