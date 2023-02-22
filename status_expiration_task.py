from database_interaction_functions import get_metadata_from_db
from database_interaction_functions import modulate_status
from config import generate_database_connection, Configuration

import time
import datetime

def status_thread_wrapper(config: Configuration) -> None:
    def status_expiration(config: Configuration) -> None:
        print("status expiration process running")
        with generate_database_connection(config) as connection:
            retrieved_metadata = get_metadata_from_db(connection, config)
            status = retrieved_metadata.status
            if status == "busy":
                expiration_time = retrieved_metadata.expiration
                datetime_format = '%Y-%m-%d %H:%M:%S.%f'
                expiration_time = datetime.datetime.strptime(expiration_time, datetime_format)
                if expiration_time <= datetime.datetime.now():
                    modulate_status("available", 1, connection, config)

    while True:
        status_expiration(config)
        time.sleep(60)

