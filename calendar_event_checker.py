from threading import Thread
from icalendar import Calendar, Event, vDDDTypes
from datetime import datetime
import schedule
import pytz
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
    print("ICS file retrieved")
    print("ICS file retrieved")
    print("ICS file retrieved")
    print("ICS file retrieved")
    print("ICS file retrieved")
    print("ICS file retrieved")
    calendar = Calendar.from_ical(response.text)
except requests.exceptions.RequestException as err:
    print("Error fetching calendar:", err)

def configure_timezone_to_UTC_if_naive(unknown_datetime): 
    if unknown_datetime.tzinfo is None:
        pytz.UTC.localize(naive_datetime)
    return naive_datetime

def convert_icalender_date_to_datetime(dt_time):
    print("dt_time:", dt_time)
    if isinstance(dt_time, datetime.datetime):
        return dt_time
    elif isinstance(dt_time, str):
        try:
            date_with_time = '%Y%m%dT%H%M%S'
            datetime.strptime(dt_time, date_with_time)
            return configure_timezone_to_UTC_if_naive(datetime.strptime(dt_time, date_with_time))

        except ValueError:
            #no longer useful this data is no longer pushing into this function
            print("Need more specific time clarification")
    else:
        raise ValueError("unsupported dt_time format for VEVENT")

def check_events():
    now = datetime.datetime.now()
    now = configure_timezone_to_UTC_if_naive(now)
    for component in calendar.walk():
        if component.name == "VEVENT":
            dtstart = component.get("dtstart")
            dtend = component.get("dtend")
            ##could make function for this for readability
            if isinstance(dtstart.dt, datetime.datetime) and isinstance(dtend.dt, datetime.datetime):
                start = dtstart.dt
                end = dtend.dt
                start = convert_icalender_date_to_datetime(start)
                end = convert_icalender_date_to_datetime(end)
                print("end:", end)
                #all of these should now be UTC plspls
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
