from flask import Flask, request, jsonify
import configparser
import datetime
import http.server
import socketserver
import sqlite3
import atexit
import subprocess
import os
import json
import requests
app = Flask(__name__)

status = "available"
expiration_time = datetime.datetime.now()

##load in config from ini
global config_json_file_name
global current_config
global current_json_config
config = configparser.ConfigParser()
config.read('config.ini')
current_config = config
##need to check that these things exist i think lol TODO
##write config to a json for use
config_dict = {section: {option: config.get(section, option) for option in config.option(section)} for section in config.sections()}
config_json_file_name = 'config.json'
with open(config_json_file_name, 'w') as json_file:
    json.dump(config_dict, json_file)
##read for use
with open(config_json_file_name, 'r') as json_file:
    config_json = json.load(json_file)
    current_json_config = config_json

##key checker
def status_validation(key, recieved_key):
    if key != recieved_key:
        return "Unauthorized Token", 401
    else: 
        pass

@app.route('/set_status', methods=['POST'])
def set_status():

    global status, expiration_time

    #checking if correct token is recieved in req
    status_validation(current_config.get('key'), request.headers.get('token'))

    req_status = request.json.get('status')

    ##make this make sure that the time is atleast 5 minutes or so
    duration = request.json.get('duration', 30)

    #validate status

    if req_status not in ["busy", "available"]:
        return "Invalid Status", 400
    
    status = req_status
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=duration)

    return "Status Updated", 200

@app.route('/get_status', methods=['GET'])
def get_status():
    global status, expiration_time
    #status validation
    if datetime.datetime.now() > expiration_time:
        status = "available"
    return jsonify({"status": status, "expiration_time": str(expiration_time)})

@app.route('/get_config', methods=['GET'])
def get_config():
    print(current_json_config)
    return
    
if __name__ == '__main__':

    server_host = current_config.get('server','host')
    server_debug = current_config.get('server','debug')
    server_port = current_config.get('server','port')
    app.run(host=server_host, debug=server_debug, port = server_port)
