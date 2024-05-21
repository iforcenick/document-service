from urllib import request, parse
from env import DBHUB_URL
import json

profiles = None
last_load_time = 0

def get_social_profiles():
    request_body = parse.urlencode({
        "operation": "getFullProfiles",
        "body": {}
    }).encode()
    req = request.Request(f'{DBHUB_URL}/operate', data=request_body) # this will make the method "POST"
    response = request.urlopen(req)
    response_json = json.loads(response.read())
    return response_json["data"]