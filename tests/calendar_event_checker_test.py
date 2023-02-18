import sys
sys.path.append('/home/xethrus/paidProject/AvaliablilityProgram')
import icalendar
import datetime
import pytz

from calendar_event_checker import configure_timezone_to_UTC_if_naive
from calendar_event_checker import attempt_convert_to_datetime_if_not
from calendar_event_checker import check_events

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

