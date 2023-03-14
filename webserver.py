from flask import Flask, jsonify, render_template, send_from_directory, redirect, url_for, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy 
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
import csv



app = Flask(__name__)

##FLASK-LOGIN

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'secret_key'

class User:
    def __init_(self, username, email, id):
        self.username = username
        self.email = email
        self.authenticated = False
        self.active = False
        self.anonymous = False
        self.id = id
    def get_id():
        return self.id;


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class UnauthorizedTokenError(Exception):
    pass





@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as  {session["username"]}'
    else:
        print 'You are not logged in'
    return render_template('index.html')

def get_by_user(username):
    with open('user.csv')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('logged in successfully')
        next = request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        return redirect(next or url_for('home'))
    return render_template('login.html'), form=form)
#    if request.method == 'POST':
#        session['username'] = request.form['username']
#        return redirect(url_for('home')
#    return render_template('login.html')
@app.route('/logout')
def logout():
    logout_user()
    #session.pop('username', None)
    return redirect(url_for('index'))


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
