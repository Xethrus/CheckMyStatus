import configparser
from dataclasses import dataclass

@dataclass
class Configuration:
    def __init__(self, db_host, db_file_title, server_host, server_port, server_debug, user_name, user_key, calendar_at):
        self.database = {
            "db_host": db_host,
            "db_file_title": db_file_title
        }
        self.server = {
            "server_host": server_host,
            "server_port": server_port,
            "server_debug": server_debug
        }
        self.user = {
            "user_name": user_name,
            "user_key": user_key
        }
        self.calendar = {
            "calendar_at": calendar_at
        }

current_config = configparser.ConfigParser()
current_config.read('config.ini')
def create_config():
    config = Configuration(
        db_host = current_config.get('database', 'db_host'),
        db_file_title = current_config.get('database', 'db_file_title'),
        server_host = current_config.get('server', 'server_host'),
        server_port = current_config.get('server', 'server_port'),
        server_debug = current_config.get('server', 'server_debug'),
        user_name = current_config.get('user', 'user_name'),
        user_key = current_config.get('user', 'user_key'),
        calendar_at = current_config.get('calendar', 'calendar_at'),
    )
    return config

def test_create_config():
    config_test = create_config()
    print(config_test.database['db_host'])

#test_create_config()

