from dateutil.parser import parse

from tools.database_interaction_functions import get_metadata_from_db, modulate_status, Metadata
from config.config import generate_database_connection, Configuration

import sys
import time
import datetime
import sqlite3

def status_expiration(config: Configuration, connection: sqlite3.Connection) -> None:
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
        connection = sqlite3.connect(config.db_file_path)
        status_expiration(config, connection)

