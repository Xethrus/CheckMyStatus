import os
import sys
import typing
import unittest
import sqlite3

from unittest.mock import patch
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from threads.status_expiration_task import status_expiration
from tools.database_interaction_functions import modulate_status, get_metadata_from_db, Metadata
from config.config import Configuration, generate_database_connection

class TestStatusThread(unittest.TestCase):
    def setUp(self) -> None:

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
            VALUES ('testuser', 'busy', '2022-02-22 22:22:22.22');
        ''')
    def test_status_expiration_thread(self) -> None:
        test_config = Configuration.get_instance('test_config.ini')
        status_expiration(test_config)
        self.connection = generate_database_connection(test_config)
        retrieved_metadata = get_metadata_from_db(self.connection, test_config)
        self.assertIsInstance(retrieved_metadata, Metadata)
        self.assertEqual(retrieved_metadata.status, 'available')
    def tearDown(self) -> None:
        self.connection.close()
        
if __name__ == '__main__':
    unittest.main()
        
