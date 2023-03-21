import datetime
import sqlite3

from config.config import Configuration, generate_database_connection
import data


from math import ceil
from dataclasses import dataclass
from typing import Union

@dataclass
class Metadata:
    status: str
    expiration: str

def get_metadata_from_db(database_connection: sqlite3.Connection, config: Configuration) -> Metadata:
    current_user_from_config = config.user_name
    print("current_user_from_config:", config.user_name, "from database:", config.db_file_title, "from connection:", database_connection)
    metadata_return = None
    cursor = database_connection.cursor()
    cursor.execute('''
        SELECT status, expiration FROM savedState
        WHERE user = (?)
    ''', (current_user_from_config,))
    fetched_data = cursor.fetchone()
    if fetched_data:
        status, expiration = fetched_data
        metadata_return = Metadata(status=status, expiration=expiration)
    else:
        raise ValueError(f"No data found for user '{current_user_from_config}'")
    if metadata_return is None:
        raise ValueError(f"No metadata was found for user '{current_user_from_config}'")
    return metadata_return


def validate_status(status: str) -> str:
    print("attempting to validate status:", status)
    if status.strip() not in ["busy", "available"]:
        raise ValueError(f"invalid status, status supplied: {status}")
    print("validated status")
    return status

def validate_duration(duration: Union[int, datetime.timedelta]) -> int:
    if isinstance(duration, str):
        duration = int(duration)
    if isinstance(duration, datetime.timedelta):
        duration = ceil(duration.seconds/60)
    if duration <= 0:
        raise ValueError(f"invalid duration, duration supplied: {duration}")
    return duration

def modulate_status(wanted_status: str, wanted_duration: Union[int, datetime.timedelta], database_connection: sqlite3.Connection, config: Configuration) -> None:
    wanted_status = validate_status(wanted_status)
    wanted_duration = validate_duration(wanted_duration)
    if isinstance(wanted_duration, datetime.timedelta):
        wanted_expiration_time = datetime.datetime.now() + wanted_duration
    else:
        wanted_expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=wanted_duration)
    user_from_config = config.user_name
    retrieved_metadata = get_metadata_from_db(database_connection, config)
    current_status = retrieved_metadata.status
    current_expiration = retrieved_metadata.expiration
    current_db_file_title = config.db_file_title
    status_difference = wanted_status != current_status
    expiration_difference = wanted_expiration_time != current_expiration
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
