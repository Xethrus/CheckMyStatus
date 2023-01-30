import sqlite3

connection = sqlite3.connect("stored_state.db")
cursor = connection.cursor()
"""
cursor.execute('''
    CREATE TABLE users (
        user TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        expiration TEXT NULL,
        calendar TEXT NOT NULL
    )
''')
"""
#cursor.execute("ALTER TABLE users RENAME TO savedState")
cursor.execute('''
ALTER TABLE savedState
MODIFY expiration TEXT NULL''')
connection.commit()
print("Table state created")

connection.close()
