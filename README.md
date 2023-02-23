# AvaliablilityProgram
webserver.py
This is the main Flask server that runs the web application. It provides endpoints for updating and retrieving user status. Additionally, it starts two threads: one that checks for events in the user's calendar and another that checks for status expiration.

config.py
This file contains the configuration class that represents the configuration file that the web server reads from. The generate_database_connection function establishes a connection to the SQLite database.

database_interaction_functions.py
This file contains various functions related to database interaction, such as get_metadata_from_db and modulate_status, which retrieves and modifies the status of a user from the database.

config.ini
This is the configuration file that contains various settings for the web server, such as server host, port, and debug settings.

calendar_event_checker.py
This file contains the check_events function that checks for events in the user's calendar.

status_expiration_task.py
This file contains the status_expiration function that checks if a user's status has expired and updates it accordingly.

The code uses icalendar library to work with calendar data and flask library to run a web server. It also uses sqlite3 library to connect to a database and requests library to make HTTP requests.
