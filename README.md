# AvaliablilityProgram (ONGOING)
Avaliablility Program
Overview
The AvaliablilityProgram is a web application that helps users manage their availability status and calendar events. The application features a web server, calendar event checking, and database interaction functionalities.

**Configuration**
The application uses a configuration file config.ini to store various settings such as database connection information, server settings, user credentials, and calendar details. The configuration file is organized into sections, and each section contains key-value pairs.

Configuration Sections
[database]: Contains the database configuration settings.

db_host: The database host address (in this case, it's redacted).
db_file_title: The name of the SQLite database file (e.g., stored_state.db).
[server]: Contains the web server configuration settings.

server_host: The server's host address (e.g., 0.0.0.0).
server_port: The server's port number (e.g., 8000).
server_debug: Debug mode for the server (e.g., True).
[user]: Contains the user credentials.

user_name: The username for accessing the application (e.g., username).
user_key: The password for accessing the application (e.g., password).
[calendar]: Contains the calendar configuration settings.

calendar_at: The calendar API token (in this case, it's redacted).
[config]: Contains the configuration file settings.

config_file_name: The name of the configuration file (e.g., config.ini).
config_path: The path to the configuration file (e.g., path/to/config).
Make sure to update the config.ini file with your own settings before running the application.

**Templates**
The application uses three HTML templates to display different views of the application:

index.html: The main page that displays the availability status to users.
home.html: The admin console page that allows the admin to change the availability status and log out.
login.html: The login page where users enter their username and password to access the admin console.
Index Template
index.html is the main page that shows the availability status to users. It contains a rectangle that changes color based on the current status (green for available and red for busy). The page also includes a script that periodically updates the color and status of the rectangle.

Home Template
home.html is the admin console page that allows the admin to change the availability status and log out. It contains a status rectangle similar to the one in index.html, a button to change the status, and a logout button. The page includes scripts to handle status change events and update the status rectangle.

Login Template
login.html is the login page where users enter their username and password to access the admin console. The form sends a POST request to the server with the entered credentials. The page also displays any flashed messages, such as login errors.

**Docker and Docker Compose**
The application uses Docker to create an isolated environment for running the project. The provided Dockerfile sets up a Python 3.10 environment, installs the required packages from requirements.txt, and runs the webserver.py script.

To set up the container using Docker Compose, a docker-compose.yml file is also provided. This file configures the service, maps the necessary ports, and sets up the required volumes for the application.

Dockerfile
The Dockerfile contains the following instructions:

Use the python:3.10-slim-buster image as the base image.
Set the working directory to /app.
Copy the application files to the /app directory.
Install the required packages from requirements.txt.
Expose port 8000.
Set the command to run the webserver.py script.
Docker Compose
The docker-compose.yml file defines the following configuration:

Use version 3 of the Docker Compose file format.
Define a service called myservice with the following properties:
Use a container named webserver_container.
Use the webserver:latest image.
Map port 80 on the host to port 8000 on the container.
Set up volumes to mount the config.ini, templates, and dist directories from the host to the container.
To start the application using Docker Compose, run the following command in the same directory as the docker-compose.yml file:

```
docker-compose up
```
**Calendar Event Checker**
The calendar_event_checker.py script is responsible for checking calendar events and updating the availability status accordingly. This script uses the icalendar library to parse calendar events and checks if there is an ongoing event.

The main functions in this script are:

configure_timezone_to_UTC_if_naive(): This function takes a datetime object and returns a datetime object in UTC timezone if the input datetime is naive (timezone-unaware).
attempt_convert_to_datetime_if_not(): This function takes a datetime object or a string and attempts to convert it to a datetime object if it is not already one.
check_events(): This function takes a calendar object, a configuration object, and a database connection. It checks if there is an ongoing event in the calendar, and if there is, it updates the availability status in the database.
event_thread_wrapper(): This function acts as a wrapper for the event_checker_thread(), which is executed every 60 seconds. The event_checker_thread() function is responsible for downloading the calendar events from the specified URL, parsing the calendar events, and calling the check_events() function to update the availability status.

**Configuration and Database Connection**
The config.py script is responsible for reading the configuration settings from a specified configuration file and storing them in a Configuration data class. It also provides a function to generate a connection to the SQLite database.

The main components in this script are:

Configuration: This is a data class that holds all the necessary configuration settings for the application. It reads the settings from the specified configuration file when an instance is created.
generate_database_connection(): This function takes a Configuration object as an argument and returns a connection to the SQLite database specified in the configuration.

Database Interaction Functions
The database_interaction_functions.py script contains functions for interacting with the SQLite database used by the application. The main components in this script are:

Metadata: A data class representing the metadata retrieved from the database.
get_metadata_from_db(): This function retrieves the metadata for the current user from the database and returns a Metadata object.
validate_status(): Validates the given status and raises a ValueError if it is invalid.
validate_duration(): Validates the given duration and raises a ValueError if it is invalid.
modulate_status(): Updates the status and/or expiration time for the current user in the database based on the given arguments.

Thank you for providing the database_interaction_functions.py and status_expiration_task.py files. I will add sections in the README to explain how these scripts work and how they interact with the rest of the application.

Database Interaction Functions
The database_interaction_functions.py script contains functions for interacting with the SQLite database used by the application. The main components in this script are:

Metadata: A data class representing the metadata retrieved from the database.
get_metadata_from_db(): This function retrieves the metadata for the current user from the database and returns a Metadata object.
validate_status(): Validates the given status and raises a ValueError if it is invalid.
validate_duration(): Validates the given duration and raises a ValueError if it is invalid.
modulate_status(): Updates the status and/or expiration time for the current user in the database based on the given arguments.
These functions can be imported and used in other parts of the application to interact with the SQLite database. For example:

python
Copy code
from config import Configuration, generate_database_connection
from database_interaction_functions import get_metadata_from_db, modulate_status

config = Configuration("config.ini")
database_connection = generate_database_connection(config)

metadata = get_metadata_from_db(database_connection, config)
print("Current status:", metadata.status)

modulate_status("busy", 30, database_connection, config)
Status Expiration Task
The status_expiration_task.py script contains a function and a thread wrapper for managing the status expiration process:

status_expiration(): This function checks the status and expiration time for the current user, and updates the status to "available" if the expiration time has passed.
status_thread_wrapper(): This is a wrapper function that runs status_expiration() in a loop with a 60-second sleep interval.

As for the requirements.txt file, I understand that it is currently inaccurate and a work in progress. When you finalize the list of dependencies for your project, please update the requirements.txt file accordingly. This will allow users to install the required packages by running:

```
pip install -r requirements.txt
```
or
```
pacman -S requirements.txt
```


