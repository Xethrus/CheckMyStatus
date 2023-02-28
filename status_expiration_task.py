from database_interaction_functions import get_metadata_from_db
from database_interaction_functions import modulate_status
from config import generate_database_connection, Configuration
from dateutil.parser import parse

import time
import datetime
import sqlite3

def status_expiration(config: Configuration) -> None:
    connection = generate_database_connection(config)
    print("status expiration process running")
    with connection as connection:
        retrieved_metadata = get_metadata_from_db(connection, config)
        status = retrieved_metadata.status
        if status == "busy":
            expiration_time = retrieved_metadata.expiration
#            if not isinstance(expiration_time, datetime.dateime):
#                raise ValueError("expiration time was not a datetime")
            datetime_format = "%Y-%m-%d %H:%M:%S.%f"

            expiration_time_dt = parse(expiration_time)

            if expiration_time_dt <= datetime.datetime.now():
                modulate_status("available", 1, connection, config)

def status_thread_wrapper(config: Configuration) -> None:
    while True:
        time.sleep(60)
        status_expiration(config)

