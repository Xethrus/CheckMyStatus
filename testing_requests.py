import requests
import json
import time
from typing import TypedDict

key = {'token' : 'password'}
headers = {'Content-Type': 'application/json'}
headers.update(key)

url = "http://REDACTED:8000/set_status"

class Data(TypedDict):
    status: str
    duration: int
data: Data = {
  "status" : "busy",
  "duration" : 1
}

json_data = json.dumps(data)
print("making req")
request_response = requests.post(url, headers=headers, data=json_data)
print(request_response.status_code)
print("supplying:", data['status'].strip())


request_response = requests.get("http://REDACTED:8000/get_status")
print(request_response)

time.sleep(60)

request_response = requests.get("http://REDACTED:8000/get_status")
print(request_response)


