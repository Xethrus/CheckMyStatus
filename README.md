# AvaliablilityProgram
This code is a Flask web server that provides an API for setting and getting the status of a user. The status can be either "busy" or "available", and the status expiration time is managed by the server. Additionally, the server runs a background task that checks for events in a calendar and sets the status to "busy" if there is an event happening at the current time.

Key components
config.py: contains configuration information for the server, database, user, and calendar.
database_interaction_functions.py: contains functions for interacting with the database to get and set the status and status expiration time.
calendar_event_checker.py: contains the code for the background task that checks for events in the calendar and sets the status to "busy" if necessary.
status_expiration_task.py: contains the code for the background task that checks the expiration time of the status and sets the status to "available" if the time has passed.
main.py: the main file that runs the Flask web server and starts the background tasks.
API Endpoints
The server provides two API endpoints:

/set_status: a POST endpoint that sets the status and status expiration time. The request body should contain a JSON object with the following keys:
status: the status to set, either "busy" or "available".
duration: the duration in minutes to set the status for (optional, defaults to 30 minutes).
/get_status: a GET endpoint that returns the current status and status expiration time.
Setting up the server
To run the server, you'll need to install the required packages listed in requirements.txt. You can do this by running the following command:

Copy code
pip install -r requirements.txt
Next, you'll need to set up the configuration information in config.py. This includes information for the server, database, user, and calendar.

Finally, you can run the server by running the following command:

css
Copy code
python main.py
Note that the server is set up to run on localhost by default, so you'll need to access the API endpoints using http://localhost:5000/.
