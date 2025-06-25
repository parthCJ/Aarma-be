import requests

# Corrected URL: /sensors/sensors
API_URL = "http://localhost:8000/sensors/sensors"

sensors_to_create = [
    {"sensor_id": "sensor_001", "devices": ["device_001"]},
    {"sensor_id": "sensor_002", "devices": ["device_002"]},
    {"sensor_id": "sensor_003", "devices": ["device_003"]},
]

for sensor in sensors_to_create:
    response = requests.post(API_URL, json=sensor)
    print(f"Creating {sensor['sensor_id']} => Status {response.status_code}: {response.json()}")
