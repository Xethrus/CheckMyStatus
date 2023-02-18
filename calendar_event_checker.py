from threading import Thread
from icalendar import Calendar, Event, vDDDTypes
from datetime import datetime
from config import generate_database_connection
from config import Configuration

import schedule
import pytz
import datetime
import requests
import time
import json


#from config import create_config
#config = create_config()

#from database_interaction_functions import modulate_status
#from database_interaction_functions import get_metadata_from_db

def configure_timezone_to_UTC_if_naive(unknown_datetime): 
    print("running config timzone")
    if unknown_datetime.tzinfo is not pytz.UTC:
        utc_timezone = pytz.timezone("UTC")
        unknown_datetime = unknown_datetime.astimezone(utc_timezone)
        return unknown_datetime
    return unknown_datetime

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

def check_events(calendar, get_metadata_from_db, modulate_status):
    print("running check events")
    event_found = False
    now = datetime.datetime.now()
    try:
        now = configure_timezone_to_UTC_if_naive(now)
    except:
        print("unable to configure the timezone of now")
    for component in calendar.walk():
        if component.name != "VEVENT":
            continue
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        ##could make function for this for readability
        start = dtstart.dt
        end = dtend.dt
        try:
            start = attempt_convert_to_datetime_if_not(start)
            end = attempt_convert_to_datetime_if_not(end)
        except:
            print("unable to convert to datetime")
        #all of these should now be UTC plspls
        if not isinstance(start, datetime.datetime) and isinstance(end, datetime.datetime):
            continue
        if not start <= now <= end:
            continue
        duration = end - start
        print("Duration:", duration)
        #need to think of smartest way to set busy status, I think i have access to global status and expiration so maybe just a direct mod
        while True:
            try:
                config = Configuration.get_instance('/home/xethrus/paidProject/AvaliablilityProgram')
                database_connection = generate_database_connection(config)
                retrieved_metadata = get_metadata_from_db(database_connection, config)
            except Exception as err:
                print("unable to get metadata")
            if retrieved_metadata.status == "avaliable":
                status = "busy"
                try:
                    modulate_status(status, duration, database_connection)
                except:
                    print("unable to modulate status")
            else:
                pass
            #time.sleep(60)
        event_found = True
        break
    #do nothing because no status updates needed
    if not event_found:
        print("no event at current time")
    return event_found

def test_event_checker():

    print("i am running the test")

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

    print("running here lol")
    event_found = check_events(test_calendar, get_metadata_from_db, modulate_status)
    print("running here too lol")
    if event_found:
        print("event found, test found")
    else:
        print("event not found, test failed")


def event_thread_wrapper(config):
    print(" in wrap calendar thread running")
    def event_checker_thread(config):
        print("in thread calendar thread running")
        running = True
        try:
            #issue making multi configs
            ics_download_link = config.calendar_at
        except:
            print("failed to retrieve from config object data:")
            print("'calendar_at'")
        try:
            response_from_ical_request = requests.get(ics_download_link)
            calendar = Calendar.from_ical(response_from_ical_request.text)
            check_events(calendar, get_metadata_from_db, modulate_status)
        except requests.exceptions.RequestException as err:
            print("Error fetching calendar:", err)
        finally:
            time.sleep(60)
#            event_checker_thread(config)
#
#    event_checker_thread(config)

#def main():
#    test_event_checker()
#if __name__ == "__main__":
#    main()
