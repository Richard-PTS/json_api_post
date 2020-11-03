from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime
import time

# Configuration variables, do not modify. Use config.json
auth = ""
api_url = ""
json_file = ""
json_data = ""
log_file = ""

# Load config from config.json
with open('config.json', 'r') as config_data:
    # ToDo: Error handeling
    auth = HTTPBasicAuth('apikey', config_data['auth-key'])
    api_url = config_data['apiURL']
    json_file = config_data['jsonFile']
    log_file = config_data['logFile']

# Load the json data to send in the request
with open(json_file, 'r') as json_file_data:
    # ToDo: Error handeling 
    json_data = json.load(json_file_data)

# Execute request, log results, retry up to 5 times
SendRequest()

# Functions    
def LogAttempt(result):
    if (log_file == ""):return
    # If no log file is specified, do not log anything
    with open(log_file, "a") as logFile:
        now = datetime.now()
        logFile.write(now + " | " + result['elapsed'] + "s | " + result['status_code'] + "\n")

def SendRequest():
    tries = 1
    result = MakeRequest()
    while result['status_code'] != requests.codes.ok:
        if tries > 4:
            break
        tries = tries + 1
        result = MakeRequest()

def MakeRequest():
    startTime = time.time()
    r = requests.post(api_url, json=json_data, auth=auth, timeout=15)
    # ToDo: Error handeling
    endTime = time.time()
    elapsed = round(endTime - startTime, 5)
    res = {'status_code' : r.status_code, "elapsed":elapsed}
    LogAttempt(res)
    return res