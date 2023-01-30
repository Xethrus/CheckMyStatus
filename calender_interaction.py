import datetime
from google.oauth2 import service_account
import googleapiclient.discovery
import sqlite3
import json
import requests

# create the service object
credentials = service_account.Credentials.from_service_account_file('/home/xethrus/paidProject/AvaliabilityProgram/client_secret_960001777617-48ec3tekc4tso2nhdecmkibqfv2gap34.apps.googleusercontent.com')
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

# define the calendar id and the time range to check
calendar_id = 'primary'
time_min = datetime.datetime.utcnow().isoformat() + 'Z'  # current time in UTC
time_max = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'  # next hour in UTC

# get the events
events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

# check if there are any events happening now
if not events:
    print("No events happening now.")
else:
    print("status set")
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    end_time = event['end'].get('dateTime', event['end'].get('date'))
    end_time = datetime.fromisoformat(end_time)
    start_time = datetime.fromisoformat(start_time)
    duration = int((end_time - start_time).total_seconds())
    duration = duration / 60

    header_token = {'token' : 'jay_is_the_big_dawg'}
    data = {'status' : 'busy', 'duration': duration}
    status_response = requests.post('http://REDACTED:8000/get_status', headers = header_token, json=data)
    if status_response.status_code == 200:
        print("status updated")
    elif status_response.status_code == 401:
        print("unauthorized token")
    elif status_response.status_code == 200:
        print("invalid status")
    else:
        print("something went awry")

        
    print("busy until ", end_time)

