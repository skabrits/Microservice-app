from flask import Flask
from flask import request
from registrationLogic import user, user_files
from app import app
from werkzeug.utils import secure_filename
import random
import json
import os

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
        except TypeError as e:
            app.logger.error("ERROR: %s" % (e,))
            response = {"status": 405}
        except Exception as e:
            app.logger.error("ERROR: %s" % (e,))
            response = {"status": 404}
        
    return json.dumps(response)
    
    
@app.route("/api/file/upload", methods=['GET','POST'])
def upload_view():
    response = {"status": 400}
    if request.method == 'POST':
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            if 'file' not in request.files:
                response = {"status": 400}
            file = request.files['file']
            if file.filename == '':
                response = {"status": 400}
            if file:
                file_name = secure_filename(file.filename)
                file_name = file_name
                folderpath = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
                os.makedirs(folderpath, exist_ok = True)
                file_path = os.path.join(folderpath, file_name)
                file.save(file_path)
                user_files.upload_file(user_id, file_name, file_path)
                response = {"status": 202}
        else:
            response = {"status": 405}
        
    return json.dumps(response)
    
@app.route("/api/file/delete", methods=['GET','POST'])
def delete_view():
    response = {"status": 400}
    if request.method == 'POST':
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            file_name = request.form["file_name"]
            try:
                file_path = get_file_path(user_id, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                user_files.delete_file(user_id, file_name)
                response = {"status": 200}
            except Exception as e:
                app.logger.error("ERROR: %s" % (e,))
                response = {"status": 404}
        else:
            response = {"status": 405}
        
    return json.dumps(response)
    
@app.route("/api/file/list", methods=['GET','POST'])
def list_view():
    response = {"status": 400}
    if request.method == 'POST':
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            user_files_list = user_files.list_files(user_id)
            response = {"status": 200, "files": user_files_list}
        else:
            response = {"status": 405}
        
    return json.dumps(response)