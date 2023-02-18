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

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
    def __init__(self, config_file_path):
        current_config = configparser.ConfigParser()
        current_config.read(config_file_path)
        self.db_host = current_config.get('database', 'db_host'),
        self.db_file_title = current_config.get('database', 'db_file_title'),
        self.server_host = current_config.get('server', 'server_host'),
        self.server_port = current_config.get('server', 'server_port'),
        self.server_debug = current_config.get('server', 'server_debug'),
        self.user_name = current_config.get('user', 'user_name'),
        self.user_key = current_config.get('user', 'user_key'),
        self.calendar_at = current_config.get('calendar', 'calendar_at')
    @classmethod
    def get_instance(cls, config_file_path):
        if not cls.instance:
            cls.instance = Configuration(config_file_path)
        return cls.instance

def generate_database_connection(config): 
    database_connection = sqlite3.connect(config.db_file_title)
    return database_connection


