from urllib import request, parse
from env import DBHUB_URL
import json

profiles = None
last_load_time = 0

request_body = parse.urlencode({
    "operation": "getFullProfiles",
    "body": {}
}).encode()
req = request.Request(f'{DBHUB_URL}/operate', data=request_body) # this will make the method "POST"
response = request.urlopen(req)
profiles = json.loads(response.read())

def get_profile_from_name(full_name):
  global profiles
  filtered_profiles = [ profile for profile in profiles if f"{profile['first-name']} {profile['last-name']}" == full_name ]
  return filtered_profiles[0]