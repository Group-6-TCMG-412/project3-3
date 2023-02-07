#Python 3 script to save log file and process HTTP request counts
#requires 'sudo apt install python3-pip' to be run first
#requires 'pip install requests' afterwards

import requests
from datetime import datetime

url = "https://s3.amazonaws.com/tcmg476/http_access_log"