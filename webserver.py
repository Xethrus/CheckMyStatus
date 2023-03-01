from flask import Flask, request, jsonify, render_template
from threading import Thread
from icalendar import Calendar, Event

from config import generate_database_connection
from database_interaction_functions import Metadata, validate_duration
from database_interaction_functions import modulate_status
from database_interaction_functions import get_metadata_from_db, validate_status
from config import Configuration, generate_database_connection
from typing import Union
from flask.typing import ResponseReturnValue
from queue import Queue
#from influxdb import InfluxDBClient


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
#def record_runtime(client: InfluxDBClient, database_name: str) -> None:
#    timestamp = int(time.time() * 1000000000)
#    uptime = int(open('/proc/uptime').read().split()[0])
#    data = [
#        {
#            'measurement' : 'server_runtime',
#            'time': timestamp,
#            'fields': {
#                'uptime': uptime
#            }
#        }
#    ]
#    client.write_points(data, database=database_name)
@app.route('/')
def index():
    return render_template('templates/index.html')

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
        modulate_status(req_status, req_duration, connection, config)
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

def main() -> None:
    config = Configuration.get_instance("config.ini")

    print("testing name of config file:", config.config_file_name)

    server_host = config.server_host
    server_debug = config.server_debug
    server_port = config.server_port
    database_name = config.db_file_title

#    max_connections: int = 2
#    connection_pool= Queue(maxsize=max_connections)
#    for _ in range(max_connections):
#        connection_pool.put(sqlite3.connect(config.config_file_name))
#    def get_connection_from_pool():
#        return connection_pool.get()
#    def release_connection_to_pool(connection):
#        connection_pool.put(connection)
    
#    influx_db_url = "https://us-east-1-1.aws.cloud2.influxdata.com"
#    token = "onboarding-pythonWizard-token-1677212867129"
#    org = "Availability"
#
#    client = InfluxDBClient(
#        url=influx_db_url,
#        token=token,
#        org=org
#    )
#    client.create_database('server_metrics')
#    record_runtime(client, 'server_metrics')
#    write_api = client.write_api(write_options=SYNCHRONOUS)
#    data_point = influxdb_client.Point("run_time").tag("time", "time_in_minute").field("minutes", up_time_minutes)
#    write_api.write(bucket=bucket, org=org, record=data_point)

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
    
if __name__ == '__main__':
    main()
    #pass configuration object
