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
def registr_view():
    response = {"status": 400}
    if request.method == 'POST':
        print("registr attempt")
        username = request.form["login"]
        password = request.form["password"]
        try:
            user_id = user.register(username, password)
            response = {"status": 200, "ID": user_id}
        except Exception as e:
            print("ERROR: %s" % (e,))
            response = {"status": 401}
        
    return json.dumps(response)
    
@app.route("/api/login", methods=['POST'])
def login_view():
    response = {"status": 400}
    if request.method == 'POST':
        print("login attempt")
        username = request.form["login"]
        password = request.form["password"]
        user_id = user.login(username, password)
        if user_id is None:
            response = {"status": 401}
        else:
            response = {"status": 200, "ID": user_id}
        
    return json.dumps(response)