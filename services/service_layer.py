import requests
from typing import Dict, Any

# ✅ Use your actual FastAPI endpoint, not Mongo URI
API_URL = "http://localhost:8000/sensors/sensor-data"
GET_LATEST_URL_TEMPLATE = "http://localhost:8000/sensors/{sensor_id}/last-data"

# Check if difference is significant
def is_significant_change(a: float, b: float, threshold: float = -2) -> bool:
    # return abs(a - b) >= threshold
    return True

# Main function to call from MQTT receiver
def add_sensor_data_if_changed_via_api(data: Dict[str, Any]) -> Dict[str, Any]:
    sensor_id = data.get("sensor_id")
    if not sensor_id:
        return {"error": "sensor_id missing in payload"}

    # Correctly build GET URL
    latest_url = GET_LATEST_URL_TEMPLATE.format(sensor_id=sensor_id)
    try:
        r = requests.get(latest_url)
    except Exception as e:
        return {"error": "Failed to connect to API", "exception": str(e)}

    # If no previous data exists
    if r.status_code == 404:
        res = requests.post(API_URL, json=data)
        return {
            "message": "First-time data sent",
            "status": res.status_code,
            "response": res.json()
        }

    if r.status_code != 200:
        return {
            "error": f"Failed to fetch latest data: {r.status_code}",
            "response": r.text
        }

    # Compare current vs latest data
    latest_data = r.json()
    old_readings = {
        reading["sensor_name"]: reading["reading"]
        for reading in latest_data.get("readings", [])
    }

    new_readings = [
        reading for reading in data.get("readings", [])
        if reading["sensor_name"] not in old_readings
        or is_significant_change(reading["reading"], old_readings[reading["sensor_name"]])
    ]

    if not new_readings:
        return {"message": "No significant change detected"}

    payload = {**data, "readings": new_readings}
    res = requests.post(API_URL, json=payload)
    return {
        "message": "Significant change detected and data sent",
        "status": res.status_code,
        "response": res.json()
    }
