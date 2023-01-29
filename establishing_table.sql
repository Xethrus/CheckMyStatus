import sqlite3

connection = sqlite3.connect("information.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM state WHERE type='table' AND name='state'")
result = cursor.fetchone()

if not result:
    cursor.execute("""
    CREATE TABLE state (
        user_name TEXT NOT NULL,
        current_status TEXT NOT NULL,
        status_duration TEXT NOT NULL
        current_calendar TEXT NOT NULL
    )
    """)
    connection.commit()
    print("Table state created")
else:
    print("Table state already exists")

connection.close()
