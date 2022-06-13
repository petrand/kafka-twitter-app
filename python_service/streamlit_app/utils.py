import base64
import json
import time 
from datetime import datetime

def decode_message(msg):
    msg_string =msg.decode('utf-8')

    msg_json = json.loads(msg_string)
    return msg_json

def convert_to_datetime(timestamp):
    timestamp = timestamp.split('.')[0]
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    return timestamp

def compute_freshness(timestamp):
    timestamp = convert_to_datetime(timestamp)
    time_diff = (datetime.now() - timestamp).total_seconds()
    return time_diff
