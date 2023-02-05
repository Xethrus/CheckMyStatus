from flask import Flask, request, jsonify
from threading import Thread
from icalendar import Calendar, Event
from dataclasses import dataclass
import schedule
import configparser
import datetime
import http.server
import socketserver
import sqlite3
import time
import atexit
import subprocess
import os
import json
import requests

@dataclass
class Metadata:
    status: str
    expiration: str
@dataclass
class Configuration:
    def __init__(self, db_host, db_file_title, server_host, server_port, server_debug, user_name, user_key, calendar_at):
        self.database = {
            "db_host": db_host,
            "db_file_title": db_file_title
        }
        self.server = {
            "server_host": server_host,
            "server_port": server_port,
            "server_debug": server_debug
        }
        self.user = {
            "user_name": user_name,
            "user_key": user_key
        }
        self.calendar = {
            "calendar_at": calendar_at
        }
app = Flask(__name__)

status = "available"
expiration_time = datetime.datetime.now()

##load in config from ini
current_config = configparser.ConfigParser()
current_config.read('config.ini')
config = Configuration(
    db_host = current_config.get('database', 'db_host'),
    db_file_title = current_config.get('database', 'db_file_title'),
    server_host = current_config.get('server', 'server_host'),
    server_port = current_config.get('server', 'server_port'),
    server_debug = current_config.get('server', 'server_debug'),
    user_name = current_config.get('user', 'user_name'),
    user_key = current_config.get('user', 'user_key'),
    calendar_at = current_config.get('calendar', 'calendar_at'),
)
print(config.calendar['calendar_at'])
print(config.database['db_host'])
print(config.database['db_file_title'])
print(config.server['server_host'])
print(config.server['server_port'])
print(config.server['server_debug'])
print(config.user['user_name'])
print(config.user['user_key'])

#global config_json_file_name
#global current_config
#global current_json_config
#config = configparser.ConfigParser()
#config.read('config.ini')
#current_config = config
###need to check that these things exist i think lol TODO
#config_json_file_name = 'config.json'
#with open(config_json_file_name, 'w') as json_file:
#    json.dump(config_dict, json_file)
###read for use
#with open(config_json_file_name, 'r') as json_file:
#    config_json = json.load(json_file)
#    current_json_config = config_json
#
##key checker
def status_validation(key, recieved_key):
    if key != recieved_key:
        print("failed key")
        return "Unauthorized Token", 401
    else: 
        pass
        print("key accepted")


@app.route('/set_status', methods=['POST'])
def set_status():
    #phase this out soon
    #global status, expiration_time
    
    #checking if correct token is recieved in req
    current_user_key = config.user['user_key']
    status_validation(current_user_key, request.headers.get('token'))

    req_status = request.json.get('status')

    ##make this make sure that the time is atleast 5 minutes or so
    duration = request.json.get('duration', 30)

    #validate status

    #currently rejecting what is being sent from test
    if req_status.strip() not in ["busy", "available"]:
        return "Invalid Status", 400
    
    status = req_status
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    user_from_config = config.user['user_name']
    try:
        retrieved_metadata = get_metadata_from_db()
        current_db_file_title = config.database['db_file_title']
        connection = sqlite3.connect(current_db_file_title)
        cursor = connection.cursor()
        result = cursor.execute('''
            UPDATE savedState SET status = (?), expiration = (?)
            WHERE user = (?)
        ''', retrieved_metadata.status, retrieved_metadata.expiration_time, user_from_config)
        connection.commit()
    except sqlite3.Error as error:
        print("failed to update savedState table", error)

    finally:
        if(connection):
            connection.close()
    return "Status Updated", 200

@app.route('/get_status', methods=['GET'])
def get_status():
    retrieved_metadata = get_metadata_from_db()
    #status validation
    print(retrieved_metadata.status)
    return jsonify({"status": retrieved_metadata.status, "expiration_time": retrieved_metadata.expiration})

##background status process
def status_expiration():
    #metadata = get_metadata_from_db()
    #status = metadata[0]
    while "status" in locals():
        if status == "busy":
            if expiration_time <= datetime.datetime.now():
                status = "available"
        time.sleep(60)

def get_metadata_from_db():
    #connection works
    try:
        current_db_file_title = config.database['db_file_title']
        connection = sqlite3.connect(current_db_file_title)
        current_user_from_config = config.user['user_name']
    except: 
        print("user was unable to retrieved from config object")
    try:
        cursor = connection.cursor()
        result = cursor.execute('''
            SELECT status, expiration FROM savedState
            WHERE user = (?)
                                ''', current_user_from_config)
        fetched_data = result.fetchone()
        metadata_return = Metadata(status = fetched_data[0], expiration = fetched_data[1])
        connection.commit()
    except sqlite3.Error as error:
        print("failed to retrieve status", error)
    finally:
        if(connection):
            connection.close()
            return metadata_return

    
    
if __name__ == '__main__':
    status_checker_thread = Thread(target=status_expiration)
    status_checker_thread.start()
    server_host = config.server['server_host']
    server_debug = config.server['server_debug']
    server_port = config.server['server_port']
    app.run(host=server_host, debug=server_debug, port = server_port)
