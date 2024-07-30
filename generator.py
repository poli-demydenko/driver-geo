import requests
import json
import time
import random

with open('settings.json') as f:
    settings = json.load(f)

url = "http://api:8000/api/v1/driver-geo"
num_drivers = settings["num_drivers"]
interval = settings["interval"]

def generate_random_data(driver_id):
    return {
        "driver_id": driver_id,
        "latitude": random.uniform(49.795, 49.832),
        "longitude": random.uniform(23.950, 24.030),
        "speed": random.uniform(0, 120),
        "altitude": random.uniform(0, 1500)
    }

def send_data_to_endpoint(data):
    for i in range(10): 
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return
        except requests.ConnectionError:
            print(f"Connection refused, retrying in 5 seconds... ({i+1}/10)")
            time.sleep(5)
    raise Exception("Failed to connect to API after multiple retries")

while True:
    data = [generate_random_data(i) for i in range(num_drivers)]
    send_data_to_endpoint(data)
    time.sleep(interval)