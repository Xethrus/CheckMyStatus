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
#print(config.calendar['calendar_at'])
#print(config.database['db_host'])
#print(config.database['db_file_title'])
#print(config.server['server_host'])
#print(config.server['server_port'])
#print(config.server['server_debug'])
#print(config.user['user_name'])
#print(config.user['user_key'])

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
def key_validation(key, recieved_key):
    if key != recieved_key:
        print("failed key")
        return "Unauthorized Token", 401
    else: 
        print("key accepted")
        pass

def validate_status(status):
    if status.strip() not in ["busy", "available"]:
        return "Invalid Status", 400
    else: 
        return status
def validate_duration(duration):
    if duration <= 0:
        return "Invalid duration", 400
    else: 
        return duration

##set status generic
def modulate_status(wanted_status, wanted_duration):
    try:
        wanted_status = validate_status(wanted_status)
        wanted_duration = validate_duration(wanted_duration)
    except:
        print("invalid status or duration, not set")
        #how can i just make this all stop if the status and duration fail, or does it with the error code returns 400

    wanted_expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=wanted_duration)
    user_from_config = config.user['user_name']
    try:
        retrieved_metadata = get_metadata_from_db()
        current_status = retrieved_metadata.status
        current_expiration = retrieved_metadata.expiration
        current_db_file_title = config.database['db_file_title']
        status_difference, expiration_difference = False
        if wanted_status != current_status:
            status_difference = True
        
        if wanted_expiration_time != current_expiration:
            expiration_difference = True
        
        connection = sqlite3.connect(current_db_file_title)
        cursor = connection.cursor()
        if(status_difference and expiration_difference):
            result = cursor.execute('''
                UPDATE savedState SET status = (?), expiration = (?)
                WHERE user = (?)
            ''', (wanted_status, wanted_expiration_time, user_from_config))

        elif(status_difference):
            result = cursor.execute('''
                UPDATE savedState SET status = (?)
                WHERE user = (?)
            ''', (wanted_status, user_from_config))

        elif(expiration_difference):
            result = cursor.execute('''
                UPDATE savedState SET expiration = (?)
                WHERE user = (?)
            ''', (wanted_expiration_time, user_from_config))
        else:
            print("no changes were requested")

        connection.commit()
    except sqlite3.Error as error:
        print("failed to update savedState table", error)

    finally:
        if(connection):
            connection.close()
    return "Status Updated", 200



@app.route('/set_status', methods=['POST'])
def set_status():
    #phase this out soon
    #global status, expiration_time
    
    #checking if correct token is recieved in req
    current_user_key = config.user['user_key']
    key_validation(current_user_key, request.headers.get('token'))

    req_status = request.json.get('status')

    ##make this make sure that the time is atleast 5 minutes or so
    req_duration = request.json.get('duration', 30)
    try:
        modulate_status(req_status, req_duration)
        return
    except:
        return "failed to modulate status"



@app.route('/get_status', methods=['GET'])
def get_status():
    retrieved_metadata = get_metadata_from_db()
    #status validation
    print(retrieved_metadata.status)
    return jsonify({"status": retrieved_metadata.status, "expiration_time": retrieved_metadata.expiration})

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
   #     print(type(current_user_from_config))
   #     print(f"asdf'{current_user_from_config}'lalala")
        result = cursor.execute('''
            SELECT status, expiration FROM savedState
            WHERE user = (?)
                                ''', (current_user_from_config,))
        fetched_data = result.fetchone()
        metadata_return = Metadata(status = fetched_data[0], expiration = fetched_data[1])
        connection.commit()
    except sqlite3.Error as error:
            print("failed to retrieve status", error)
    finally:
        if(connection):
            connection.close()
            return metadata_return
def log_and_thread_binder(log_file_name, thread_file_name):
    try:
        with open(log_file_name, "w") as logfile:
            process = subprocess.Popen(["python", thread_file_name], stdout=logfile, stderr=logfile)
            process.wait()
    except Exception as error:
        print("unable to run, error:", str(error))


if __name__ == '__main__':
    log_and_thread_binder("logfile_calendar.txt", "calendar_event_checker.py")
    log_and_thread_binder("logfile_status.txt", "status_expiration_task.py")
    server_host = config.server['server_host']
    server_debug = config.server['server_debug']
    server_port = config.server['server_port']
    app.run(host=server_host, debug=server_debug, port = server_port)
