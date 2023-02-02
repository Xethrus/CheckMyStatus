import requests
import json

key = {'token' : 'password'}
url = "http://REDACTED:8000/set_status"
data = {
  'status' : "busy",
  'duration' : 2
}
print("making req")
request_response = requests.post(url, headers = key, data=json.dumps(data))
print(request_response.status_code)
