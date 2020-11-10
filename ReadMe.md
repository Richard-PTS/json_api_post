# Read Me: api_json_post.py

This script performs a single task, to submit JSON data to an API with an Authentication Key. The configuration file 'config.json' includes all the available options. These are:

* API URL
* authentication key
* the json file that is to be sent to the API
* log file where the script will log it's activity

## Requirements

* Requests <https://pypi.org/project/requests/>
* JSONLines <https://pypi.org/project/jsonlines/>
