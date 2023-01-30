import sqlite3
import json
import requests
import datetime

header_token = {'token' : 'jay_is_the_big_dawg'}

status_response = requests.get('http://REDACTED:8000/get_status')
if status_response.status_code == 200:
  status_data = status_response.json()
  current_status = status_data["status"]
  current_status_duration = status_data["expiration_time"]
else:
  print(f"Request failed with status code {status_response.status_code}")

config_response = requests.get('http://REDACTED:8000/get_config',headers = header_token)
if config_response.status_code == 200:
  config_data = config_response.json()
  print("current_user is being set")
  print(config_data["user"]["name"])
  print("current_calendar is being set")
  print(config_data["calendar"]["links"])
  try:
    current_user = config_data["user"]["name"]
    current_calendar_link = config_data["calendar"]["links"]
  except KeyError:
      print("KEY ERROR")
  
else:
  print(f"Request failed with status code {config_response.status_code}")


connection = sqlite3.connect('stored_state.db')
cursor = connection.cursor()
if status_response.status_code == 200 and config_response.status_code == 200:
    cursor.execute('''
      INSERT INTO savedState (
        user,
        status,
        expiration,
        calendar)
      VALUES (?, ?, ?, ?)
      ''', (
        current_user,
        current_status,
        current_status_duration,
        current_calendar_link
        ))
else:
    print("FAILED TO RECIEVE WORKING STATUS CODES FROM STATUS AND CONFIG")

connection.commit()
connection.close()

