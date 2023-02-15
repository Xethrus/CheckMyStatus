from threading import Thread
from icalendar import Calendar, Event, vDDDTypes
from datetime import datetime

import schedule
import pytz
import datetime
import requests
import time
import json


from config import create_config
config = create_config()

from database_interaction_functions import modulate_status
from database_interaction_functions import get_metadata_from_db

def configure_timezone_to_UTC_if_naive(unknown_datetime): 
    print("running config timzone")
    if unknown_datetime.tzinfo is not pytz.UTC:
        utc_timezone = pytz.timezone("UTC")
        unknown_datetime = unknown_datetime.astimezone(utc_timezone)
        return unknown_datetime
    return unknown_datetime

def test_timezone_configurer():
    naive_datetime = datetime.datetime(2023,2,13,10,30,0)
    utc_datetime = datetime.datetime(2023,2,13,10,30,0, tzinfo=pytz.utc)
    test_naive_to_utc = configure_timezone_to_UTC_if_naive(naive_datetime)
    if naive_datetime != utc_datetime:
        raise TypeError("same value, change not viable")
    if test_naive_to_utc == utc_datetime:
        print ("naive to utc test passed")
    test_no_change = configure_timezone_to_UTC_if_naive(utc_datetime)
    if test_no_change == utc_datetime:
        print ("no change utc to utc test passed")
    return

def attempt_convert_to_datetime_if_not(dt_time):
    print("running convert datetime")
    print("dt_time:", dt_time)
    if isinstance(dt_time, datetime.datetime):
        return configure_timezone_to_UTC_if_naive(dt_time)
    elif isinstance(dt_time, str):
        try:
            date_with_time = '%Y-%m-%d %H:%M:%S.%f %Z'
            datetime.strptime(dt_time, date_with_time)
            return configure_timezone_to_UTC_if_naive(datetime.strptime(dt_time, date_with_time))
        except ValueError:
            print("string not matching \'%Y-%m-%d %H:%M:%S.%f %Z\' format")
            return dt_time
    else:
        print("unsupported dt_time format for VEVENT")
        return dt_time

def test_convert_string_to_datetime():
    datetime_string_utc = "2023-02-13 17:21:03.123456 UTC"
    datetime_string_naive = "2023-02-13 17:21:03.123456" 
    datetime_expected = datetime.datetime(2023,2,13,17,21,3,123456, tzinfo=pytz.utc)
    datetime_utc_converted = configure_timezone_to_UTC_if_naive(datetime_string_utc)
    datetime_naive_converted = configure_timezone_to_UTC_if_naive(datetime_string_naive)
    
    if datetime_utc_converted == datetime_expected:
        print("utc datetime string to utc datetime test passed")
    else:
        print("utc datetime string to utc datetime test failed")

    if datetime_naive_converted == datetime_expected:
        print("naive datetime string to utc datetime test passed")
    else:
        print("naive datetime string to utc datetime test failed")


def check_events(calendar, get_metadata_from_db, modulate_status):
    print("running check events")
    event_found = False
    now = datetime.datetime.now()
    now = configure_timezone_to_UTC_if_naive(now)
    for component in calendar.walk():
        if component.name != "VEVENT":
            continue
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        ##could make function for this for readability
        start = dtstart.dt
        end = dtend.dt
        start = attempt_convert_to_datetime_if_not(start)
        end = attempt_convert_to_datetime_if_not(end)
        #all of these should now be UTC plspls
        if not isinstance(start, datetime.datetime) and isinstance(end, datetime.datetime):
            continue
        if not start <= now <= end:
            continue
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
        event_found = True
        break
    #do nothing because no status updates needed
    if not event_found:
        print("no event at current time")
    return event_found

def test_event_checker():
    test_calendar = Calendar()
    test_calendar.add('prodid', 'test_calendar')
    test_calendar.add('version', '2.0')

    event = Event()

    event.add('summary', 'test event')
    event.add('dtstart', datetime.datetime.now(pytz.utc))
    dt_end = datetime.datetime.now() + datetime.timedelta(minutes=1)
    event.add('dtend', dt_end)
    event.add('dtstamp', datetime.datetime.now(pytz.utc))
    event['uid'] = 'test-uid-123'

    test_calendar.add_component(event)

    event_found = check_events(test_calendar, get_metadata_from_db, modulate_status)
    if event_found:
        print("event found, test found")
    else:
        print("event not found, test failed")


def event_thread_wrapper():
    print(" in wrap calendar thread running")
    def event_checker_thread(config):
        print("in thread calendar thread running")
        running = True
        try:
            #issue making multi configs
            ics_download_link = config.calendar['calendar_at']
        except:
            print("failed to retrieve from config object a:")
            print("'calendar','calendar_at'")
        try:
            response_from_ical_request = requests.get(ics_download_link)
            calendar = Calendar.from_ical(response_from_ical_request.text)
            check_events(calendar, get_metadata_from_db, modulate_status)
        except requests.exceptions.RequestException as err:
            print("Error fetching calendar:", err)
        finally:
            time.sleep(60)
            event_checker_thread(config)
#
    event_checker_thread(config)

#test_event_checker()


