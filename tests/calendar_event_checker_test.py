import os
import sys
import typing 

import pytz
import unittest
import sqlite3


from datetime import datetime
from datetime import timedelta
from icalendar import Calendar, Event 
sys.path.append("AvailabilityProgram")
from threads.calendar_event_checker import check_events
from tools.database_interaction_functions import get_metadata_from_db, modulate_status, Metadata
from config.config import Configuration, generate_database_connection



class TestEventChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.test_calendar = Calendar()
        self.test_calendar.add('prodid', 'test_calendar')
        self.test_calendar.add('version', '2.0')
        self.event = Event()
        self.event.add('summary', 'test event')
        self.event.add('dtstart', datetime.now(pytz.utc))
        dt_end = datetime.now() + timedelta(minutes=1)
        self.event.add('dtend', dt_end)
        self.event.add('dtstamp', datetime.now(pytz.utc))
        self.event['uid'] = 'test-uid-123'
        self.test_calendar.add_component(self.event)
        
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
            VALUES ('testuser', 'busy', '2022-02-22 22:22:22');
        ''')

    def test_event_checker(self) -> None:
        test_config = Configuration.get_instance('test_config.ini')

        metadata = get_metadata_from_db(self.connection, test_config)

        event_found = check_events(self.test_calendar, test_config, self.connection)
        self.assertIsInstance(metadata, Metadata)
        self.assertEqual(event_found, True)
        self.assertEqual(metadata.status, 'busy')

    def tearDown(self) -> None:
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
