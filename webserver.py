from flask import Flask, request, jsonify
from threading import Thread
from icalendar import Calendar, Event

#from calendar_event_checker import event_checker_thread
#from calendar_event_checker import stop_event_checker_thread
#from status_expiration_task import status_expiration
from config import generate_database_connection
from database_interaction_functions import Metadata, validate_duration
from database_interaction_functions import modulate_status
from database_interaction_functions import get_metadata_from_db, validate_status
from config import Configuration
from typing import Union
from flask.typing import ResponseReturnValue

import status_expiration_task
import calendar_event_checker
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



app = Flask(__name__)


class UnauthorizedTokenError(Exception):
    pass

def key_validation(key: str, recieved_key: str) -> None:
    if key != recieved_key:
        raise UnauthorizedTokenError("Unauthorized token")

@app.route('/set_status', methods=['POST'])
def set_status() -> ResponseReturnValue:
    #phase this out soon
    #global status, expiration_time
    
    config = Configuration.get_instance("config.ini")
    current_user_key = config.user_name
    token = request.headers.get('token')

    if token:
        try:
            key_validation(current_user_key, token)
        except UnauthorizedTokenError:
            return "Unauthorized token", 401
    else:
        return "missing token", 401

    req_status = request.json.get('status')
    req_duration = request.json.get('duration', 30)
    with generate_database_connection(config) as connection:
        modulate_status(req_status, req_duration, connection)
    return "Status Updated", 200 



@app.route('/get_status', methods=['GET'])
def get_status() -> ResponseReturnValue:
    config = Configuration.get_instance("config.ini")
    retrieved_metadata = get_metadata_from_db(generate_database_connection(config), config)
    #status validation
    print(retrieved_metadata.status)
    return jsonify({"status": retrieved_metadata.status, "expiration_time": retrieved_metadata.expiration})


#def thread_runner(thread_function):
#    thread = threading.Thread(target=thread_function)
#    thread.daemon = True
#    thread.start()

if __name__ == '__main__':
    main()
    #pass configuration object
def main() -> None:
    config = Configuration.get_instance('/home/xethrus/paidProject/AvaliablilityProgram/config.ini')
    server_host = config.server_host
    server_debug = config.server_debug

    server_port = config.server_port
    try:
        status_thread = threading.Thread(target=status_expiration_task.status_thread_wrapper, args=(config,))
        status_thread.start()
    except Exception as error:
        print("webserver.py- Error starting status thread:", error)
    try:
        event_thread = threading.Thread(target=calendar_event_checker.event_thread_wrapper, args=(config,))
        event_thread.start()
    except Exception as error:
        print("webserver.py- Error starting event thread:", error)
    app.run(host=server_host, debug=server_debug, port = server_port)
    
