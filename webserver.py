from flask import Flask, jsonify, render_template, send_from_directory, redirect, url_for, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy 
from threading import Thread
from icalendar import Calendar, Event

import sys
import os
from threads import *
from tools.database_interaction_functions import *
from templates import *
from tests import *

from typing import Union
from flask.typing import ResponseReturnValue
from queue import Queue


import datetime
import http.server
import time
import atexit
import subprocess
import os
import json
import requests
import threading
import csv



app = Flask(__name__)

##FLASK-LOGIN

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'secret_key'

class User:
    def __init__(self, username, email, password, id):
        self.username = username
        self.email = email
        self.password = password
        self.authenticated = False
        self.active = False
        self.anonymous = False
        self.id = id

def find_user(csv_file, username):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return row
    return None


class UnauthorizedTokenError(Exception):
    pass

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as  {session["username"]}'
    else:
        print("You are not logged in")
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #password is item 3 so row[0] and row[2]
        user_row = find_user("users.csv", username)
        #expects a user
        validating_user = User(row[0],row[1],row[2]);

        if validating_user.password == password and validating_user.username == username:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #session.pop('username', None)
    return redirect(url_for('index'))


@login_manger.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))



@app.route('/home')
@login_required
def home():
    print('LOGGED IN AS: ' + flask_login.current_user.id)
    return render_template('home.html')

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



def main() -> None:
    config = Configuration.get_instance("config.ini")

    print("testing name of config file:", config.config_file_name)

    server_host = config.server_host
    server_debug = config.server_debug
    server_port = config.server_port
    database_name = config.db_file_title
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
