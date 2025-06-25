# send_garbage_data.py

import requests
import random
import time

API_URL = "http://localhost:8000/sensors/sensor-data"

sensor_device_pairs = [
    {"sensor_id": "sensor_001", "device_id": "device_001"},
    {"sensor_id": "sensor_002", "device_id": "device_002"},
    {"sensor_id": "sensor_003", "device_id": "device_003"},
]

def generate_garbage_reading():
    return {
        "sensor_name": "TemperatureSensor",
        "status": random.choice(["OK", "FAIL", "UNKNOWN"]),
        "reading": random.uniform(-9999, 9999),
        "unit": random.choice(["Kelvin", "Joules", "nonsense_unit"]),
        "note": "Test garbage data",
        "sensor_health": random.choice(["corrupted", "invalid", "undefined"]),
        "sensor_specification": "malformed_spec"
    }

try:
    while True:
        for pair in sensor_device_pairs:
            payload = {
                "sensor_id": pair["sensor_id"],
                "device_id": pair["device_id"],
                "readings": [generate_garbage_reading()]
            }

            response = requests.post(API_URL, json=payload)
            print(f"[{pair['sensor_id']}] Status {response.status_code} -", response.json())

        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopped sending sensor data.")
