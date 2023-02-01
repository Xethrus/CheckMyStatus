import schedule 
import requests
import time
import datetime
import json


def check_status():
    get_status = requests.get('http://REDACTED:8000/get_status')
    if get_status.status_code == 200:
        status_data = get_status.json()
        expiration_str = status_data['expiration_time']
        expiration = datetime.datetime.strptime(expiration_str, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.datetime.now()
        print(type(expiration))
        print(type(current_time))
#        print(expiration)
#        print(current_time)
        if current_time > expiration:
            token = {'token' : 'jay_is_the_big_dawg'}
            data = {
                "status": "available",
                "duration": 10000
            }
            status_response = requests.post('http://REDACTED:8000/set_status', headers = token, data=json.dumps(data))
            if status_response.status_code == 200:
                print("status updated")
            else:
                print("error occurred while updating status")

        else:
            pass
    else:
        print(f"Request failed with status code {config_response.status_code}")

check_status()
