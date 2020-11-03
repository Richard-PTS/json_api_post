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
with open('config.json', 'r') as config_file_data:
    config_data = json.load(config_file_data)
    auth = HTTPBasicAuth('apikey', config_data['auth-key'])
    api_url = config_data['apiURL']
    json_file = config_data['jsonFile']
    log_file = config_data['logFile']

# Load the json data to send in the request
with open(json_file, 'r') as json_file_data:
    json_data = json.load(json_file_data)

# Confirm critical information has been provided in the configuration file
if (auth == "" or api_url == "" or json_file == ""):
    # Log an error if something is missing
    LogWrite("Critical Information has not been defined in config.json. Request not sent!")
else:
    # Execute request
    SendRequest()

# Functions    
def LogAttempt(result):
    LogWrite(result['elapsed'] + "s | " + result['status_code'] + "\n")

def LogWrite(log_message):
    if (log_file == ""):return
    now = datetime.now()
    with open(log_file, "a") as logFile:
        logFile.write(now + " | " + log_message)

def SendRequest():
    # retry up to 5 times
    tries = 1
    result = MakeRequest()
    while result['status_code'] != requests.codes.ok:
        if tries > 4:
            break
        tries = tries + 1
        result = MakeRequest()

def MakeRequest():
    try:
        startTime = time.time()
        r = requests.post(api_url, json=json_data, auth=auth, timeout=15)
        endTime = time.time()
        elapsed = round(endTime - startTime, 5)
        res = {'status_code' : r.status_code, "elapsed":elapsed}
    except:
        res = {'status_code' : 0, "elapsed" : 0}
        LogWrite("There was an error sending the request!")

    LogAttempt(res) # Log the results of the request
    return res