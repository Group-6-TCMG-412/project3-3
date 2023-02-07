#Python 3 script to save log file and process HTTP request counts
#requires 'sudo apt install python3-pip' to be run first
#requires 'pip install requests' afterwards

import requests
from datetime import datetime

url = "https://s3.amazonaws.com/tcmg476/http_access_log"

# Use requests library to fetch the data from the URL
response = requests.get(url)
data = response.text

# Split the data into individual lines
lines = data.split("\n")

# Keep track of the number of requests
total_requests = 0
total_6_month_requests = 0

# Iterate through each line
for line in lines:
    # Split each line into its components
    components = line.split(" ")
    if len(components) >= 11:
        # Extract information about each request
        remote_host = components[0]
        timestamp = components[3]
        request = components[5]
        status = components[8]
        size = components[9]
