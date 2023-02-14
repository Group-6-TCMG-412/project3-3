import re
import datetime
from collections import defaultdict
from urllib.request import urlretrieve

URL_PATH = "https://s3.amazonaws.com/tcmg476/http_access_log"
LOCAL_FILE = 'local_copy.log'

# Use urlretrieve() to fetch a remote copy and save into the local file path
local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE)

# Keep track of the number of requests
total_requests = 0

# Track the number of requests made on each day
day_count = defaultdict(int)

# Track the number of requests made each week
week_count = defaultdict(int)

# Track the number of requests made each month
month_count = defaultdict(int)

# Track the number of unsuccessful requests
unsuccessful_requests = 0

# Track the number of redirected requests
redirected_requests = 0

# Initialize a dictionary to track the items
files_dict = {}

# Track the most requested file
most_requested = defaultdict(int)

# Track the least requested file
least_requested = defaultdict(int)

# Track the requests made each month
monthly_requests = defaultdict(list)

# Loop through the file 
for line in open(LOCAL_FILE):
    pieces = re.split(r".* \[([\w:/]+)(\s[+\-]\d{4})\] \"(\S+)\s?(\S+)?\s?(\S+)?\" (\d{3}|-) (\d+|-)\s?\"?", line)
    
    if len(pieces) >= 7:
        remote_host = pieces[0]
        timestamp = pieces[1]
        timezone = pieces[2]
        request = pieces[3]
        file_name = pieces[4]
        version = pieces[5]
        status = pieces[6]
        size = pieces[7]

        # Increment the total number of requests
        total_requests +=1

        # Extract the date from the timestamp
        date_str = timestamp
        date = datetime.datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S").date()

        # Track the number of requests made on each day
        day_count[date] += 1

        # Track the number of requests made each week
        week_num = int(date.strftime("%U"))
        week_count[week_num] += 1
        sorted_week_count = dict(sorted(week_count.items()))

        # Track the number of requests made each month
        month_count[date.strftime("%B")] += 1

        # Add the request to the list of requests made in this month
        monthly_requests[date.strftime("%B")].append(line)

        # Track the number of unsuccessful requests
        if status.startswith("4"):
            unsuccessful_requests += 1

        # Track the number of redirected requests
        if status.startswith("3"):
            redirected_requests += 1

        # Check and see if a key that matches 'file_name' exists using the 'in' operator
        if file_name in files_dict :
        # So we've already added this file -- let's increment the counter
            files_dict[file_name] += 1
        else:
        # This is a new filename -- let's add it to the dictionary
            files_dict[file_name] = 1

# Calculate percentage of unsuccessful requests
unsuccessful_percent = unsuccessful_requests / total_requests * 100

# Calculate percentage of redirected requests
redirected_percent = redirected_requests / total_requests * 100

# Find the most requested file
most_requested = max(files_dict.keys(), key=(lambda k: files_dict[k]))

#Find the least requested file
least_requested = min(files_dict.keys(), key=(lambda k: files_dict[k]))

# Output total requests
print("Total Requests:", total_requests)

#Output how many requests were made on each day
print("\nRequests Made Each Day:")
for day, count in day_count.items():
    print(day, "=", count)

# Output how many requests were made on a week-by-week basis
print("\nRequests Made Each Week:")
for week, count in week_count.items():
    print("Week", week, "=", count)

# Output how many requests were made on a per month basis
print("\nRequests Made Each Month:")
for month, count in month_count.items():
    print(month, "=", count)

# Output percentage of the requests were not successful (any 4xx status code)    
print("\nUnsuccessful Requests:", unsuccessful_requests, "({:.2f}%)".format(unsuccessful_percent))
# Output percentage of the requests were redirected elsewhere (any 3xx codes)
print("Redirected Requests:", redirected_requests, "({:.2f}%)".format(redirected_percent))

# Output most and least requested file
print("\nMost Requested File:", most_requested)
print("Least Requested File:", least_requested)
