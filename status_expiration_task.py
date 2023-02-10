from database_interaction_functions import get_metadata_from_db
from database_interaction_functions import modulate_status
from datetime import datetime

import schedule
import time
import datetime


def status_expiration():
    print("running mf")
    retrieved_metadata = get_metadata_from_db()
    status = retrieved_metadata.status
    if status == "busy":
        expiration_time = retrieved_metadata.expiration
        datetime_format = '%Y-%m-%d %H:%M:%S.%f'
        try:
            expiration_time = datetime.datetime.strptime(expiration_time, datetime_format)
        except Exception as error:
            print("couldnt convert expiration time, error:", error)
        if expiration_time <= datetime.datetime.now():
            modulate_status(status, 1)

schedule.every(1).minutes.do(status_expiration)
while True:
    schedule.run_pending()
    time.sleep(1)

