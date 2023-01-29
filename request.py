import json
import requests

headers = {'token' : 'jay_is_the_big_dawg', 'content-type' : 'application/json'}
just_token = {'token' : 'jay_is_the_big_dawg'}

data = json.dumps({'status' : 'busy', 'duration' : 60})



#set_status = requests.post('http://REDACTED:8000/set_status', headers = headers, data = data)
get_status = requests.get('http://REDACTED:8000/get_status')
get_config = requests.get('http://REDACTED:8000/get_config', headers = just_token)

config_response = requests.get('http://REDACTED:8000/get_config', headers = just_token)
if config_response.status_code == 200:
    config_data = config_response.json()
    print(config_data)
else:
    print(f"Request failed with status code {config_response.status_code}")




print(get_status.status_code)
print(get_status.text)

#print(response2.status_code)
#print(response2.text)
