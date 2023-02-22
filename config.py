import configparser
import os
import sqlite3
from dataclasses import dataclass
from typing import Optional

@dataclass
class Configuration:
    db_host: str
    db_file_title: str
    server_host: str
    server_port: int 
    server_debug: bool
    user_name: str
    user_key: str
    calendar_at: str
    config_path: str
    config_file_name: str

    instance: "Configuration"

    def __init__(self, config_file_name: str) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, config_file_name)
        
        current_config = configparser.ConfigParser()
        current_config.read(config_path)

        self.cofig_path = current_config.set('config', 'config_path', config_path)
        self.config_file_name = current_config.set('config', 'config_path', config_file_name)

        with open(config_file_name, 'w') as config_file:
            config.write(config_file)

        self.db_host = current_config.get('database', 'db_host')
        self.db_file_title = current_config.get('database', 'db_file_title')
        self.server_host = current_config.get('server', 'server_host')
        self.server_port = current_config.getint('server', 'server_port')
        self.server_debug = current_config.getboolean('server', 'server_debug')
        self.user_name = current_config.get('user', 'user_name')
        self.user_key = current_config.get('user', 'user_key')
        self.calendar_at = current_config.get('calendar', 'calendar_at')

    @classmethod
    def get_instance(cls, config_name: str) -> "Configuration":
        if getattr(cls, "instance", None) is None:
            cls.instance = Configuration(config_name)
        return cls.instance

def generate_database_connection(config: Configuration) -> sqlite3.Connection: 
    database_connection = sqlite3.connect(config.db_file_title)
    print("attempting to connect to", config.db_file_title)
    if(database_connection):
        print("works")
    else:
        print("connection did not work")
    return database_connection


