import datetime
import sqlite3

from dataclasses import dataclass
from config import config

@dataclass
class Metadata:
    status: str
    expiration: str

def get_metadata_from_db():
    #connection works
    try:
        current_db_file_title = config.database['db_file_title']
        connection = sqlite3.connect(current_db_file_title)
        current_user_from_config = config.user['user_name']
    except: 
        print("user was unable to retrieved from config object")
    try:
        cursor = connection.cursor()
   #     print(type(current_user_from_config))
   #     print(f"asdf'{current_user_from_config}'lalala")
        result = cursor.execute('''
            SELECT status, expiration FROM savedState
            WHERE user = (?)
                                ''', (current_user_from_config,))
        fetched_data = result.fetchone()
        metadata_return = Metadata(status = fetched_data[0], expiration = fetched_data[1])
        connection.commit()
    except sqlite3.Error as error:
            print("failed to retrieve status", error)
    finally:
        if(connection):
            connection.close()
            return metadata_return

def validate_status(status):
    print("attempting to validate status:", status)
    if status.strip() not in ["busy", "available"]:
        return "Invalid Status", 400
    else: 
        print("validated status")
        return status

def validate_duration(duration):
    if duration <= 0:
        return "Invalid duration", 400
    else: 
        return duration

def modulate_status(wanted_status, wanted_duration):
    print("currently supplying status, duration:", wanted_status, wanted_duration)
    try:
        wanted_status = validate_status(wanted_status)
        wanted_duration = validate_duration(wanted_duration)
    except:
        print("invalid status or duration, not set")
        #how can i just make this all stop if the status and duration fail, or does it with the error code returns 400

    wanted_expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=wanted_duration)
    user_from_config = config.user['user_name']
    try:
        retrieved_metadata = get_metadata_from_db()
        current_status = retrieved_metadata.status
        current_expiration = retrieved_metadata.expiration
        current_db_file_title = config.database['db_file_title']
        status_difference = False
        expiration_difference = False

        if wanted_status != current_status:
            status_difference = True
        
        if wanted_expiration_time != current_expiration:
            expiration_difference = True
        
        connection = sqlite3.connect(current_db_file_title)
        cursor = connection.cursor()
        if(status_difference and expiration_difference):
            result = cursor.execute('''
                UPDATE savedState SET status = (?), expiration = (?)
                WHERE user = (?)
            ''', (wanted_status, wanted_expiration_time, user_from_config))

        elif(status_difference):
            result = cursor.execute('''
                UPDATE savedState SET status = (?)
                WHERE user = (?)
            ''', (wanted_status, user_from_config))

        elif(expiration_difference):
            result = cursor.execute('''
                UPDATE savedState SET expiration = (?)
                WHERE user = (?)
            ''', (wanted_expiration_time, user_from_config))
        else:
            print("no changes were requested")

        connection.commit()
    except sqlite3.Error as error:
        print("failed to update savedState table", error)

    finally:
        if(connection):
            connection.close()
    return "Status Updated", 200
