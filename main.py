#Python 3 script to save log file and process HTTP request counts
#Code adapted from tyscript.py written by group member Ty Hawkins and tested by other members
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
        # Each component divided by a space delimiter stored in a different variable
        remote_host = components[0]
        timestamp = components[3]
        request = components[5]
        status = components[8]
        size = components[9]
 #  Increment the total number of requests
        total_requests +=1
   
 #  Extract the date from the timestamp
        date_str = timestamp[1:]
 # Remove the time component from the stamp, identify date format
        date = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S").date()
    
  # Check if the date is within the 6 month period
        if date > datetime(1995, 6, 1).date() and date <= datetime(1995, 12, 1).date():
        # Increment the number of requests within the 6 month period
            total_6_month_requests += 1
        
  # Print the total number of requests made in the time period represented by the log and in the last 6 months
print("Total Requests:", total_requests)
print("Total Requests in Last 6 Months:", total_6_month_requests) 
