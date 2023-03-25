from flask import Flask
from flask import request
from flask import jsonify
import json
from flask_cors import CORS

@app.route("/")
def index():
    return jsonify("hello")

@app.get("/info")
def get_info():
    return jsonify("%s hello %f" % (request.args.to_dict().get("info"), 1.44))

@app.get("/info/<data>")
def get_data(data):
    return jsonify("%s hello %f" % (data, 2.56))

@app.route("/api/registr", methods=['POST'])
def posted():
    print("hello %s" % (request.method,))
    if request.method == 'POST':
        print("test")
        username = request.form["login"]
        print({'ID': ("%s data" % (username,))})
        print(jsonify({'ID': ("%s data" % (username,))}))
    return json.dumps({'ID': ("%s data" % (username,)), "status": 200})