import requests
import json

key = {'token' : 'password'}
headers = {'Content-Type': 'application/json'}
headers.update(key)

url = "http://REDACTED:8000/set_status"

data = {
  "status" : "busy",
  "duration" : 2
}
json_data = json.dumps(data)
print("making req")
request_response = requests.post(url, headers=headers, data=json_data)
print(request_response.status_code)
print("supplying:", data['status'].strip())


request_response = requests.get("http://REDACTED:8000/get_status")
print(request_response)
