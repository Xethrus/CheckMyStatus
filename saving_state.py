import sqlite3
import json
import requests
import datetime



status_response = requests.get('http://REDACTED:8000/get_status')
if status_response.status_code == 200:
  status_data = status_response.json()
  current_status = status_data["status"]
  current_status_duration = status_data["expiration_time"]
else:
  print(f"Request failed with status code {status_response.status_code}")

config_response = requests.get('http://REDACTED:8000/get_config')
if config_response.status_code == 200:
  config_data = config_response.json()
  current_user = config_data["user"]["name"]
  current_calendar_link = config_data["calendar"]["links"]
else:
  print(f"Request failed with status code {config_response.status_code}")


connection = sqlite3.connect('state.db')
cursor = connection.cursor()

cursor.execute("""
  INSERT INTO instance (
    user_name,
    current_status,
    status_duration,
    current_calendar)
  VALUES (?, ?, ?, ?)
  """, ("""
    current_user,
    current_status,
    current_status_duration
    current_calendar_link
  """))

connection.commit()
connection.close()

