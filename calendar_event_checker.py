from threading import Thread
from icalendar import Calendar, Event, vDDDTypes
from datetime import datetime

import schedule
import pytz
import datetime
import requests
import time
import json


from config import config
from database_interaction_functions import modulate_status
from database_interaction_functions import get_metadata_from_db


def event_checker_thread():
    print("running mf")
    try:
        #issue making multi configs
        config = config.create_config_object()
        ics_download_link = config.calendar['calendar_at']
    except:
        print("failed to retrieve from config object a:")
        print("'calendar','calendar_at'")
    try:
        response_from_ical_request = requests.get(ics_download_link)
        calendar = Calendar.from_ical(response_from_ical_request.text)
    except requests.exceptions.RequestException as err:
        print("Error fetching calendar:", err)

    def configure_timezone_to_UTC_if_naive(unknown_datetime): 
        if unknown_datetime.tzinfo is not pytz.UTC:
            utc_timezone = pytz.timezone("UTC")
            unknown_datetime = unknown_datetime.astimezone(utc_timezone)
            return unknown_datetime
        return unknown_datetime

    def attempt_convert_to_datetime_if_not(dt_time):
        print("dt_time:", dt_time)
        if isinstance(dt_time, datetime.datetime):
            return configure_timezone_to_UTC_if_naive(dt_time)
        elif isinstance(dt_time, str):
            try:
                date_with_time = '%Y%m%dT%H%M%S'
                datetime.strptime(dt_time, date_with_time)
                return configure_timezone_to_UTC_if_naive(datetime.strptime(dt_time, date_with_time))
            except ValueError:
                print("string not matching \'%Y%m%dT%H%M%S\' format")
                return dt_time
        else:
            print("unsupported dt_time format for VEVENT")
            return dt_time

    def check_events():
        now = datetime.datetime.now()
        now = configure_timezone_to_UTC_if_naive(now)
        for component in calendar.walk():
            if component.name == "VEVENT":
                dtstart = component.get("dtstart")
                dtend = component.get("dtend")
                ##could make function for this for readability
                start = dtstart.dt
                end = dtend.dt
                start = attempt_convert_to_datetime_if_not(start)
                end = attempt_convert_to_datetime_if_not(end)
                #all of these should now be UTC plspls
                if isinstance(start, datetime.datetime) and isinstance(end, datetime.datetime):
                    if start <= now <= end:
                        duration = end - start
                        print("Duration:", duration)
                        #need to think of smartest way to set busy status, I think i have access to global status and expiration so maybe just a direct mod
                        while True:
                            retrieved_metadata = get_metadata_from_db()
                            if retrieved_metadata.status == "avaliable":
                                status = "busy"
                                modulate_status(status, duration)
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
