from threading import Thread
from icalendar import Calendar, Event
import schedule
import datetime
import requests

from webserver import current_json_config, status, expiration_time

try:
    url = current_json_config.get('calendar','calendar_links')
except:
    print("failed to retrieve url at location:")
    print("'calendar','calendar_links'")
try:
    response = requests.get(url)
    print(response)
except requests.exceptions.RequestException as err:
    print("Error fetching calendar:", err)
 

calendar = Calendar.from_ical(response.content)
def check_events():
    now = datetime.now()
    for component in calendar.walk():
        if component.name == "VEVENT":
            start = component.get("dtstart").dt
            end = component.get("dtend").dt
            if start <= now <= end:
                duration = end - start
                print("Duration:", duration)
                #need to think of smartest way to set busy status, I think i have access to global status and expiration so maybe just a direct mod
                while True:
                    if status == "avaliable":
                        status = "busy"
                        expiration_time = now + duration
                    else:
                        pass
                    time.sleep(60)
                break
    else:
        #do nothing because no status updates needed
        print("No event at current time")

schedule.every(1).minutes.do(check_events)


while True:
    schedule.run_pending()
    time.sleep(1)
