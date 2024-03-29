import os
import sys
import typing 
import unittest
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.database_interaction_functions import get_metadata_from_db, Metadata
from config.config import Configuration

class TestGetMetadataFromDB(unittest.TestCase):
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
            VALUES ('testuser', 'busy', '2022-02-22 22:22:22');
        ''')
    def tearDown(self) -> None:
        self.connection.close()

    def test_get_metadata_from_db(self) -> None:
        test_config = Configuration.get_instance('test_config.ini')
        metadata = get_metadata_from_db(self.connection, test_config)
        self.assertIsInstance(metadata, Metadata)
        self.assertEqual(metadata.status, 'busy')
        self.assertEqual(metadata.expiration,'2022-02-22 22:22:22')

if __name__ == '__main__':
    unittest.main()
