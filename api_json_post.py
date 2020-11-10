from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime
import time
import jsonlines # `pip install jsonlines`

# Configuration variables, do not modify. Use config.json
auth = ""
api_url = ""
jsonL_file = ""
json_data = ""
log_file = ""

showDebug = True

# Functions
def LogAttempt(result):
    LogWrite(str(result['elapsed']) + "s | " + str(result['status_code']) + "\n")

def LogWrite(log_message):
    if (log_file == ""):return
    now = datetime.now()
    with open(log_file, "a") as logFile:
        mes = now.strftime("%m/%d/%y, %H:%M:%s") + " | " + log_message
        logFile.write(mes + '\n')
        if showDebug: print(mes)

def SendRequest():
    # retry up to 5 times
    tries = 4 #to force only 1 attempt during testing
    LogWrite('Starting Attempt with test json data')
    with jsonlines.open(jsonL_file, "r") as reader:
        for obj in reader:
            jsonD = '[' + json.dumps(obj) + ']'
            print('\nJSON Data Start\n')
            print(jsonD)
            print('\nJSON Data End\n')
            result = MakeRequest(jsonD)
            break

    while result['status_code'] != requests.codes.ok:
        if tries > 4:
            break
        tries = tries + 1
        time.sleep(tries*tries)
        LogWrite('Starting Attempt with no data sent')
        result = MakeRequest(json_data)

def MakeRequest(request_data):
    res = {'status_code':"", 'elapsed':""}
    startTime = time.time()
    headers = {'Auth-key': auth}

    try:
        r = requests.post(api_url, headers=headers, json="[{'data':'stuff'}]")
        res['status_code'] = r.status_code
        print('\nResponse Headers\n')
        print(r.headers)
        print('\n\nRequest Headers\n')
        print(r.request.headers)
        print('\n')
        LogWrite(r.text)
    except:
        LogWrite("EXCEPTION: Unknown exemption")

    endTime = time.time()
    elapsed = round(endTime - startTime, 5)
    res['elapsed'] = elapsed

    LogAttempt(res) # Log the results of the request
    return res

# Load config from config.json
with open('config.json', 'r') as config_file_data:
    config_data = json.load(config_file_data)
    auth = config_data[0]['auth-key']
    api_url = config_data[0]['apiURL']
    jsonL_file = config_data[0]['jsonFile']
    log_file = config_data[0]['logFile']

# Debug view
LogWrite('SET: api_url:\t' + api_url)
LogWrite('SET: jsonL_file:\t' + jsonL_file)
LogWrite('SET: log_file:\t' + log_file + '\n')

# with jsonlines.open(jsonL_file, "r") as reader:
#     for obj in reader:
#         print('\n')
#         print(obj)
#         print('\n')
#         print(obj['dellOrder'])
#         print('\n')
#         jsonD = json.dumps(obj)
#         print(jsonD)
#         break

# Load the json data to send in the request
# with jsonlines.open(jsonL_file) as json_file_data:
    # for line in json_file_data:
        # json_data = json_data + line

# Confirm critical information has been provided in the configuration file
if (auth == "" or api_url == "" or jsonL_file == ""):
    # Log an error if something is missing
    LogWrite("Critical Information has not been defined in config.json. Request not sent!")
else:
    # Execute request
    SendRequest()
