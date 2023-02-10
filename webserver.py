from flask import Flask, request, jsonify
from threading import Thread
from icalendar import Calendar, Event

from calendar_event_checker import event_checker_thread
from status_expiration_task import status_expiration
from database_interaction_functions import Metadata
from database_interaction_functions import modulate_status
from database_interaction_functions import get_metadata_from_db
from config import config


import schedule
import datetime
import http.server
import socketserver
import time
import atexit
import subprocess
import os
import json
import requests
import threading
import file_to_run 



app = Flask(__name__)

status = "available"
expiration_time = datetime.datetime.now()


#print(config.calendar['calendar_at'])
#print(config.database['db_host'])
#print(config.database['db_file_title'])
#print(config.server['server_host'])
#print(config.server['server_port'])
#print(config.server['server_debug'])
#print(config.user['user_name'])
#print(config.user['user_key'])


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


def thread_runner(thread_function):
    thread = threading.Thread(target=thread_function)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    
    thread_runner(status_expiration)
    thread_runner(event_checker_thread)

    server_host = config.server['server_host']
    server_debug = config.server['server_debug']
    server_port = config.server['server_port']
    app.run(host=server_host, debug=server_debug, port = server_port)
