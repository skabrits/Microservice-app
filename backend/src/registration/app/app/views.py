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
        app.logger.info("registr attempt")
        username = request.form["login"]
        password = request.form["password"]
        try:
            user_id = user.register(username, password)
            response = {"status": 200, "ID": user_id}
        except Exception as e:
            app.logger.error("ERROR: %s" % (e,))
            response = {"status": 404}
        
    return json.dumps(response)
    
@app.route("/api/login", methods=['POST'])
def login_view():
    response = {"status": 400}
    if request.method == 'POST':
        app.logger.info("login attempt")
        username = request.form["login"]
        password = request.form["password"]
        try:
            user_id = user.login(username, password)
            response = {"status": 200, "ID": user_id}
        except KeyError as e:
            app.logger.error("ERROR: %s" % (e,))
            response = {"status": 405}
        except Exception as e:
            app.logger.error("ERROR: %s" % (e,))
            response = {"status": 404}
        
    return json.dumps(response)