import sys
sys.path.append('/home/xethrus/paidProject/AvaliablilityProgram')
import icalendar
import datetime
import pytz

from calendar_event_checker import configure_timezone_to_UTC_if_naive
from calendar_event_checker import attempt_convert_to_datetime_if_not
from calendar_event_checker import check_events
from database_interaction_functions import get_metadata_from_db
from database_interaction_functions import modulate_status
from config import Configuration


class TestEventChecker(unittest.TestCase):

    def setUp(self):
        self.test_calendar = Calendar()
        self.test_event_checker.add('prodid', 'test_calendar')
        self.test_event_checker.add('version', '2.0')
        self.event = Event()
        self.event.add('summary', 'test event')
        self.event.add('dtstart', datetime.datetime.now(pytz.utc))
        self.event.add('dtend', dt_end)
        self.event.add('dtstamp', datetime.datetime.now(pytz.utc))
        self.event['uid'] = 'test-uid-123'
        self.test_calendar.add_component(event)
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE savedState (
                user TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                expiration TEXT NOT NULL
            );
        ''')
        self.cursor.execute('''
            INSERT INTO savedState (user, status, expiration)
            VALUES ('testuser', 'avaliable', '2025-02-22 22:22:22');
        ''')

    def tearDown(self):
        self.test_calendar.remove_component(self.event)
        self.test_calendar = None
        self.connection.close()

    def test_event_checker(self):
        event_found = False
        config_path = '/home/xethrus/paidProject/AvaliablilityProgram/tests/test_config.ini'
        test_config = Configuration.get_instance(config_path)
        event_found = check_events(self.test_calendar, get_metadata_from_db, modulate_status, config_path)
        metadata = get_metadata_from_db(self.connection, test_config)
        self.assertEqual(self.event_found, True)
        self.assertEqual(metadata.status, 'busy')

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

if __name__ == '__main__':
    unittest.main()
