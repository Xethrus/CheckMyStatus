from flask import Flask, request, jsonify
import configparser
import datetime
import http.server
import socketserver
import sqlite3
import atexit
import subprocess

app = Flask(__name__)

status = "available"
expiration_time = datetime.datetime.now()

#connection = sqlite3.connect("state.db")
#cursor = connection.cursor()

#current invalidated input
#sql = "INSERT INTO instance (instance_time, user_name, calendar_link) VALUES (?, ?, ?)"


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

    config = configparser.ConfigParser()
    config.read('config.ini')

    db_host = config.get('database', 'host')
    db_port = config.getint('database', 'port')
    db_title = config.get('database', 'title')
    
    user_name = config.get('user', 'name')
    
    
    calendar_links = config.get('calendar', 'links').split(',')
#fill placeholder for sql insertion
#cursor.execute(sql, (expiration_time, db_user, calendar_links))
#connection.commit()
#connection.close()

    return jsonify({
        'database': {
            'host' : db_host,
            'port' : db_port,
#            'user' : db_user,
#            'password' : db_password,
        },
        'user': {
            'name' : user_name
        }
#        'calendar': {
#            'links': calendar_links
#        }
    })

def save_state():
    subprocess.run(["python","saving_state.py"])

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port = 8000)

atexit.register(save_state)
