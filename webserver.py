from flask import Flask, jsonify, render_template, send_from_directory, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
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
app.secret_key = 'set_secret_key';


class UnauthorizedTokenError(Exception):
    pass

login_manager = LoginManager()
login_manager.init_app(app)
#user model
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'
users = [
        User(id=1, username='john', email='john@example.com', password='password'),
        User(id=2, username='jane', email='jane@example.com', password='password')
        
]

def get_user_by_id(user_id):
    for user in users:
        if user.id == user_id:
            return user

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = None
        for u in users:
            if u.username == username and u.password == password:
                user = u
                break
        if user is not None:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/dist/js/<path:path>")
def send_js(path):
    return send_from_directory('dist/js', path)

def key_validation(key: str, recieved_key: str) -> None:
    print(key, "different from:", recieved_key)
    if key != recieved_key:
        raise UnauthorizedTokenError("Unauthorized token")

@app.route('/set_status', methods=['POST'])
def set_status() -> ResponseReturnValue:
    config = Configuration.get_instance("config.ini")
    current_user_key = config.user_key
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
