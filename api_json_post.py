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
    tries = 1
    LogWrite('Starting Attempt ' + str(tries))
    result = MakeRequest()
    while result['status_code'] != requests.codes.ok:
        if tries > 4:
            break
        tries = tries + 1
        time.sleep(tries*tries)
        LogWrite('Starting Attempt ' + str(tries))
        result = MakeRequest()

def MakeRequest():
    res = {'status_code':"", 'elapsed':""}
    startTime = time.time()

    try:
        r = requests.post(api_url, auth=auth)
        res['status_code'] = r.status_code
        LogWrite(r.text)
    except urllib3.exceptions.ProtocolError:
        LogWrite('EXCEPTION: urllib3.exceptions.ProtocolError')
        res['status_code'] = 0
    except requests.exceptions.HTTPError:
        res['status_code'] = 0
        LogWrite("EXCEPTION: request.exceptions.HTTPError")
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
    auth = HTTPBasicAuth("apikey", config_data[0]['auth-key'])
    api_url = config_data[0]['apiURL']
    json_file = config_data[0]['jsonFile']
    log_file = config_data[0]['logFile']

# Debug view
LogWrite('SET: api_url:\t' + api_url)
LogWrite('SET: json_file:\t' + json_file)
LogWrite('SET: log_file:\t' + log_file + '\n')

# Load the json data to send in the request
with open(json_file, 'r') as json_file_data:
    for line in json_file_data:
        json_data = json_data + line

# Confirm critical information has been provided in the configuration file
if (auth == "" or api_url == "" or json_file == ""):
    # Log an error if something is missing
    LogWrite("Critical Information has not been defined in config.json. Request not sent!")
else:
    # Execute request
    SendRequest()
