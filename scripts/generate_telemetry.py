import random
import sys
from datetime import datetime, timedelta, timezone
import requests

TELEMETRY_URL = "http://localhost:8000/telemetry"
BATTERY_URL = "http://localhost:8000/batteries"
TOTAL_READINGS = 10_000
BATCH_SIZE = 100

def generate_reading(timestamp: datetime) -> dict:
    battery_id = random.choice(battery_ids)
    return {
        "battery_id": battery_id,
        "recorded_at": timestamp.isoformat(),
        "power_kw": random.uniform(discharge[battery_id], charge[battery_id]),
        "temperature_c": random.uniform(20.0, 35.0),
        "soc_percent": random.uniform(min_soc[battery_id], 90.0)
    }

def send_batches():
    curr_time = datetime.now(timezone.utc) - timedelta(days=1)
    count = 0
    
    for i in range(TOTAL_READINGS // BATCH_SIZE):
        current_batch = []
        for j in range(BATCH_SIZE):
            current_batch.append(generate_reading(curr_time))
            curr_time = curr_time + timedelta(seconds=1)

        try:
            response = requests.post(TELEMETRY_URL, json=current_batch, timeout=10.0)
        except requests.RequestException as err:
            print(f"Failed to add batch {i + 1}")
            sys.exit(1)

        if response.status_code == 201:
            print(f"Added batch {i + 1}")
            count += BATCH_SIZE
        else:
            print(f"Failed to add batch {i + 1}")
            print(f"Error code: {response.status_code}; {response.text}")

    print(f"Inserted {count} telemetries!")

if __name__ == "__main__":
    try:
        response = requests.get(BATTERY_URL)
    except requests.RequestException as err:
        print(f"Getting all batteries failed with request error: {err}")

    if response.status_code == 200:
        batteries = response.json()
    else: 
        print(f"Failed to get batteries. Error Code; {response.status_code}; {response.text}")

    charge = {}
    discharge = {}
    min_soc = {}
    for each in batteries:
        charge[each["battery_id"]] = each["max_charge_kw"]
        discharge[each["battery_id"]] = -each["max_discharge_kw"]
        min_soc[each["battery_id"] ] = each["min_soc_percent"]
    battery_ids = list(charge.keys())

    send_batches()