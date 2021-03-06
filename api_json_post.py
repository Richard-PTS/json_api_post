import requests
import json
from datetime import datetime
import time
import jsonlines # `pip install jsonlines`

# Configuration variables, do not modify. Use config.json
auth = ""
api_url = ""
jsonL_file = ""
log_file = ""

showDebug = True

# Functions
def LogAttempt(result):
    LogWrite(str(result['elapsed']) + "s | " + str(result['status_code']) + "\n")

def LogWrite(log_message):
    if (log_file == ""):return
    now = datetime.now()
    with open(log_file, "a") as logFile:
        mes = now.strftime("%m/%d/%Y, %H:%M:%S") + " | " + log_message
        logFile.write(mes + '\n')
        if showDebug: print(mes)

def SendRequest():
    LogWrite('Starting Request')
    with jsonlines.open(jsonL_file, "r") as reader:
        records = []
        for json_obj in reader:
            LogWrite("Adding Dell Order#: " + json_obj['dellOrder'])
            records.append(json_obj)
        if len(records) > 0:
            LogWrite("Sending Total Orders: " + str(len(records)))
            MakeRequest(records)
    LogWrite('Requests Completed')

def MakeRequest(request_data):
    startTime = time.time()
    headers = {'auth-key': auth}
    r = requests.post(api_url, headers=headers, json=request_data)
    endTime = time.time()
    elapsed = round(endTime - startTime, 5)
    res = {'status_code': r.status_code, 'elapsed':elapsed}
    LogAttempt(res) # Log the results of the request
    return res

# Load config from config.json
with open('/home/rpeterson/json_api_post/config.json', 'r') as config_file_data:
    config_data = json.load(config_file_data)
    #print(config_data)
    auth = config_data['auth-key']
    api_url = config_data['apiURL']
    jsonL_file = config_data['jsonFile']
    log_file = config_data['logFile']

# Debug view
LogWrite('SET: api_url:\t' + api_url)
LogWrite('SET: jsonL_file:\t' + jsonL_file)
LogWrite('SET: log_file:\t' + log_file + '\n')

# Confirm critical information has been provided in the configuration file
if (auth == "" or api_url == "" or jsonL_file == ""):
    # Log an error if something is missing
    LogWrite("Critical Information has not been defined in config.json. Request not sent!")
else:
    # Execute request
    SendRequest()
