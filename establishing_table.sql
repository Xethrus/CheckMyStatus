import sqlite3

connection = sqlite3.connect("state.db")
cursor = connection.cursor()

cursor.excute("""
  CREATE TABLE state (
    user_name TEXT NOT NULL,
    current_status TEXT NOT NULL,
    status_duration TEXT NOT NULL
    current_calendar TEXT
  )
""")


connection.commit()
connection.close()
