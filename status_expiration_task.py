from database_interaction_functions import get_metadata_from_db
from database_interaction_functions import modulate_status
from datetime import datetime
from config import generate_database_connection

import schedule
import time
import datetime

def status_thread_wrapper(config):
    def status_expiration(config):
        print("status expiration process running")
        connection = generate_database_connection(config)
        retrieved_metadata = get_metadata_from_db(connection, config)
        status = retrieved_metadata.status
        if status == "busy":
            expiration_time = retrieved_metadata.expiration
            datetime_format = '%Y-%m-%d %H:%M:%S.%f'
            try:
                expiration_time = datetime.datetime.strptime(expiration_time, datetime_format)
            except Exception as error:
                print("couldnt convert expiration time, error:", error)
            if expiration_time <= datetime.datetime.now():
                modulate_status("available", 1)

    while True:
        status_expiration(config)
        time.sleep(60)

