import datetime
from google.oauth2 import service_account
import googleapiclient.discovery

# create the service object
credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
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
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
