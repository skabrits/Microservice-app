from flask import Flask
from flask import request, redirect
from registrationLogic import user, user_files
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory
import random
import json
import os

front_endpoint = os.getenv('FRONT_ENDPOINT')

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
            if user_id is None:
                response = {"status": 401}
            else:
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
    status = 400
    if request.method == 'POST':
        app.logger.info("upload attempt")
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            if 'file' not in request.files:
                status = 400
            file = request.files['file']
            if file.filename == '':
                status = 400
            if file:
                file_name = secure_filename(file.filename)
                file_name = file_name
                folderpath = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
                os.makedirs(folderpath, exist_ok = True)
                file_path = os.path.join(folderpath, file_name)
                if user_files.upload_file(user_id, file_name, file_path):
                    file.save(file_path)
                    status = 202
                else:
                    status = 401
        else:
            status = 405
        
    return redirect(front_endpoint+"?status=%s" % (status,))
    
@app.route("/api/file/delete", methods=['GET','POST'])
def delete_view():
    status = 400
    if request.method == 'POST':
        app.logger.info("delete attempt")
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            file_name = request.form["file_name"]
            try:
                file_path = user_files.get_filepath(user_id, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                user_files.delete_file(user_id, file_name)
                status = 200
            except Exception as e:
                app.logger.error("ERROR: %s" % (e,))
                status = 404
        else:
            status = 405
        
    return redirect(front_endpoint+"?status=%s" % (status,))
    
@app.route("/api/file/list", methods=['GET','POST'])
def list_view():
    response = {"status": 400}
    if request.method == 'POST':
        app.logger.info("list attempt")
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            user_files_list = user_files.list_files(user_id)
            response = {"status": 200, "files": user_files_list}
        else:
            response = {"status": 405}
        
    return json.dumps(response)
    
@app.route("/api/file/download", methods=['GET','POST'])
def download_view():
    response = {"status": 400}
    if request.method == 'POST':
        app.logger.info("download attempt")
        user_id = request.form["user_id"]
        if user.check_user(user_id):
            file_name = request.form["file_name"]
            try:
                file_path = user_files.get_filepath(user_id, file_name)
                if not os.path.exists(file_path):
                    return json.dumps({"status": 404})
                return send_from_directory(os.path.dirname(file_path), file_name, as_attachment=True)
            except Exception as e:
                app.logger.error("ERROR: %s" % (e,))
                response = {"status": 404}
        else:
            response = {"status": 405}
        
    return json.dumps(response)