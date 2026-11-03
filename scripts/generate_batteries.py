import requests
import random
import sys
from app.schemas import Battery

locations = ["Austin", "Houston", "Dallas", "San Antonio"]
capacities = [10.0, 13.5, 20.0, 27.0]
powers = [3.0, 5.0, 7.0, 10.0]
API_URL = "http://localhost:8000/batteries"

def generate_battery() -> dict:
    return {
        "capacity_kwh": random.choice(capacities),
        "location": random.choice(locations),
        "max_charge_kw": random.choice(powers),
        "max_discharge_kw": random.choice(powers),
        "min_soc_percent": random.randint(15, 30)
    }

if __name__ == '__main__':
    n = 100
    count = 0

    for i in range(n):
        try:
            payload = generate_battery()
            response = requests.post(API_URL, json=payload, timeout=10.0)
        except requests.RequestException as err:
            print(f"{payload} failed with request error: {err}")
            sys.exit(1)

        if response.status_code == 201:
            data = response.json()
            print(f"Inserted Battery: {payload}")
            count += 1
        else:
            print(f"Failed to insert Battery ({payload})")
            print(f"Error code: {response.status_code}; {response.text}")

    print(f"Inserted {count} batteries!")

        