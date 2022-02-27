import requests
import json

url = 'https://discord-bot-post-office.herokuapp.com/user_data' # <<<
payload = {'name': '', 
           'id': '', 
           'create_date': '',
           'has_nitro' : '', 
           'is_in_servers' : ''
          }
response = requests.get(
    url, params=payload,
    headers={'Content-Type': 'application/json'} # Using JSON here for readability in the response
)
