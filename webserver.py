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



@app.route('/set_status', methods=['POST'])
def set_status():
    global status, expiration_time
    #checking if correct token is recieved in req
    if request.headers.get('token') != "jay_is_the_big_dawg":
        return "Unauthorized Token", 401
    #get status & duration from req
    req_status = request.json.get('status')
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
    if request.headers.get('token') != "jay_is_the_big_dawg":
        return "Unauthorized Token", 401

    file_path = "grabbed_config.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            json_data = file.read()
            return json_data
    else:
        pass

    config = configparser.ConfigParser()
    config.read('config.ini')

    db_host = config.get('database', 'host')
    db_port = config.getint('database', 'port')
    db_title = config.get('database', 'title')
    
    user_name = config.get('user', 'name')
    
    calendar_links = config.get('calendar', 'links')#.split(',')

    return jsonify({
        'database': {
            'host' : db_host,
            'port' : db_port,
            'user' : db_title,
        },
        'user': {
            'name' : user_name
        },
        'calendar': {
            'links': calendar_links
        }
    })

if __name__ == '__main__':
    global key
    global database
    # I have to find a better way to do this? some sort of json grabbing way of doing it? so it isnt parsed.
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = config.get('database','host')
    port = config.get('database','port')
    debug = config.get('server', 'debug')
    database = config.get('database', 'title')
    key = config.get('user', 'key')
    url = "http://REDACTED:8000/get_config"

    grabbed_config = requests.get(url, headers = key)
    with open("config_grabbed.json", "w") as file:
        file.write(grabbed_config.content.decode())
    get_status() #does this mean that global status and expiration now exist?

    app.run(host=host, debug=debug, port = port)
