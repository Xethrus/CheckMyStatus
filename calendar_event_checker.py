from threading import Thread
from icalendar import Calendar, Event
import schedule
import datetime
import requests

from webserver.py import current_json_config

url = current_json_config['calendar','calendar_links']

response = requests.get(url)

calendar = Calendar.from_ical(response.content)

now = datetime.now()

for component in calendar.walk():
    if component.name == "VEVENT":
        start = component.get("dtstart").dt
        end = component.get("dtend").dt
        if start <= now <= end:
            duration = end - start
            print("Duration:", duration)
            #need to think of smartest way to set busy status, I think i have access to global status and expiration so maybe just a direct mod
            break
else:
    #do nothing because no status updates needed
    print("No event at current time")

