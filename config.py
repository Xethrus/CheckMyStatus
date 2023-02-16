import configparser
import sqlite3
from dataclasses import dataclass

@dataclass
class Configuration:
    db_host: str
    db_file_title: str
    server_host: str
    server_port: str
    server_debug: str
    user_name: str
    user_key: str
    calendar_at: str

def create_config():
    current_config = configparser.ConfigParser()
    current_config.read('config.ini')
    config = Configuration(
        db_host = current_config.get('database', 'db_host')
        db_file_title = current_config.get('database', 'db_file_title')
        server_host = current_config.get('server', 'server_host')
        server_port = current_config.get('server', 'server_port')
        server_debug = current_config.get('server', 'server_debug')
        user_name = current_config.get('user', 'user_name')
        user_key = current_config.get('user', 'user_key')
        calendar_at = current_config.get('calendar', 'calendar_at')
    )
    return config
config = create_config()

def get_config():
    return config

def generate_database_connection(): 
    database_connection = sqlite3.connect(config.database['db_file_title'])
    return database_connection


