import configparser
import os
import sqlite3
from dataclasses import dataclass
from typing import Optional, Union

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
    config_path: Optional[str] = None
    config_file_name: Optional[str] = None

    ##type issue for expectation of return from configuration
    instance: Optional["Configuration"] = None
    def __init__(self, config_file_name: str) -> None:
        current_dir = os.getcwd()
        print("the current directory is:", current_dir)
        config_dir_path = os.path.join(current_dir, 'config')
        config_path = os.path.join(config_dir_path, config_file_name)
        
        #enables use on windows-typed file paths lol
#        raw_config_path = "%r"%config_path
#        config_path = raw_config_path
        
        print("the current path is:", config_path)
        
        current_config = configparser.ConfigParser()
        current_config.read(config_path)
        print("the current path is:", config_path)
        self.config_path = config_path
        self.config_file_name = config_file_name

        self.config_path = current_config.get('config', 'config_path')
        self.config_file_name = current_config.get('config', 'config_file_name')
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
        config_instance = cls.instance
        assert config_instance is not None
        return config_instance

def generate_database_connection(config: Configuration) -> sqlite3.Connection: 
    database_connection = sqlite3.connect(config.db_file_title)
    if(database_connection):
        print("connection established with", config.db_file_title)
    else:
        print("connection could not be established with", config.db_file_title)

    return database_connection


