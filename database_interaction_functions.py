import datetime
import sqlite3

from dataclasses import dataclass
from config import Configuration 

@dataclass
class Metadata:
    status: str
    expiration: str


def get_metadata_from_db(database_connection, config):
    connection = database_connection
    current_user_from_config = config.user_name
    try:
        cursor = connection.cursor()
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

def modulate_status(wanted_status, wanted_duration, database_connection):
    print("currently supplying status, duration:", wanted_status, wanted_duration)
    try:
        config = Configuration.get_instance('/home/xethrus/paidProject/AvaliablilityProgram/config.ini')
    except:
        print("failed to retreive configuration from singleton")
    try:
        wanted_status = validate_status(wanted_status)
        wanted_duration = validate_duration(wanted_duration)
    except:
        print("invalid status or duration, not set")
        #how can i just make this all stop if the status and duration fail, or does it with the error code returns 400

    wanted_expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=wanted_duration)
    user_from_config = config.user_name
    try:
        retrieved_metadata = get_metadata_from_db(database_connection, config)
        current_status = retrieved_metadata.status
        current_expiration = retrieved_metadata.expiration
        current_db_file_title = config.db_file_title
        status_difference = False
        expiration_difference = False

        if wanted_status != current_status:
            status_difference = True
        
        if wanted_expiration_time != current_expiration:
            expiration_difference = True
        
        connection = database_connection
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

