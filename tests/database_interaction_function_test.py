import sys
#sys.path.append('/home/xethrus/paidProject/AvaliablilityProgram')
import unittest
import sqlite3
from database_interaction_functions import get_metadata_from_db, Metadata

class TestGetMetadataFromDB(unittest.TestCase):
    def setUp(self):
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
    def tearDown(self):
        self.connection.close()

    def test_get_metadata_from_db(self):
        metadata = get_metadata_from_db(self.connection)
        self.assertIsInstanc(metadata, Metadata)
        self.assertEqual(metadata.status, 'busy')
        self.assertEqual(metadata.expiration,'2022-02-22 22:22:22')

if __name__ == '__main__':
    unittest.main()
