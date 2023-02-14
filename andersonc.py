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

        # Track the most requested file
        most_requested[file_name] += 1

        # Track the least requested file
        if request not in least_requested:
            least_requested[file_name] = 1
        else:
            least_requested[file_name] += 1

# Calculate percentage of unsuccessful requests
unsuccessful_percent = unsuccessful_requests / total_requests * 100

# Calculate percentage of redirected requests
redirected_percent = redirected_requests / total_requests * 100

# Find the most requested file
most_requested_file = max(most_requested, key=most_requested.get)

#Find the least requested file
least_requested_file = least_requested_file = min(least_requested, key=least_requested.get)

print("Total Requests:", total_requests)
print("\nRequests Made Each Day:")
for day, count in day_count.items():
    print(day, "=", count)
print("\nRequests Made Each Week:")
for week, count in week_count.items():
    print("Week", week, "=", count)
print("\nRequests Made Each Month:")
for month, count in month_count.items():
    print(month, "=", count)
print("\nUnsuccessful Requests:", unsuccessful_requests, "({:.2f}%)".format(unsuccessful_percent))
print("Redirected Requests:", redirected_requests, "({:.2f}%)".format(redirected_percent))
print("\nMost Requested File:", most_requested_file)
print("Least Requested File:", least_requested_file)
