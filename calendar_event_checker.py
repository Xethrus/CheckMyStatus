from threading import Thread
from icalendar import Calendar, Event, vDDDTypes
import schedule
import datetime
import requests
import time
import json

from webserver import current_json_config, status, expiration_time
try:
    ics_file_name = current_json_config.get('calendar','calendar_at')
except:
    print("failed to retrieve file at location:")
    print("'calendar','calendar_at'")
try:
    #should this be ical or ics
#    url = "REDACTED"

    ics_link_json = current_json_config.get('calendar','calendar_at')
    ics_download_link = ics_link_json["calendar_at"]
    response = requests.get(ics_download_link)
    calendar = Calendar.from_ical(response.text)
except requests.exceptions.RequestException as err:
    print("Error fetching calendar:", err)
 
def convert_icalender_date_to_datetime(dtstart):
    ical_even_start_time = dtstart
    start_datetime = vDDDTypes.from_ical(ical_even_start_time)
    return start_datetime

def check_events():
    now = datetime.datetime.now()
    for component in calendar.walk():
        if component.name == "VEVENT":
            start = convert_icalender_date_to_datetime(component.get("dtstart").dt)
            end = convert_icalender_date_to_datetime(component.get("dtend").dt)
            print("end:", end)
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
