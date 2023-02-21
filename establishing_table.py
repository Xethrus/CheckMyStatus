import sqlite3

def init_db() -> None:
    with sqlite3.connect("stored_state.db") as connection:
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
        print("Table state created")

init_db()
