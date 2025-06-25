from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import requests

app = FastAPI()

# Your API endpoint for sensor data
API_URL = "http://localhost:8000/sensor-data"

# Example hardcoded IDs (replace with dynamic if needed)
DEVICE_ID = "DEV001"
SENSOR_ID = "SENS001"

# Incoming raw ADC model
class RawADC(BaseModel):
    ch0: float
    ch1: float
    ch2: float
    ch3: float
    sent_at: str

@app.post("/process")
async def process_adc(data: RawADC):
    # Multiply ADC values by 2 and structure them as sensor readings
    readings = [
        {
            "sensor_name": "Channel 0",
            "status": "OK",
            "reading": data.ch0 * 2,
            "unit": "V",
            "note": "Auto reading",
            "sensor_health": "Good",
            "sensor_specification": "ADS1115"
        },
        {
            "sensor_name": "Channel 1",
            "status": "OK",
            "reading": data.ch1 * 2,
            "unit": "V",
            "note": "Auto reading",
            "sensor_health": "Good",
            "sensor_specification": "ADS1115"
        },
        {
            "sensor_name": "Channel 2",
            "status": "OK",
            "reading": data.ch2 * 2,
            "unit": "V",
            "note": "Auto reading",
            "sensor_health": "Good",
            "sensor_specification": "ADS1115"
        },
        {
            "sensor_name": "Channel 3",
            "status": "OK",
            "reading": data.ch3 * 2,
            "unit": "V",
            "note": "Auto reading",
            "sensor_health": "Good",
            "sensor_specification": "ADS1115"
        }
    ]

    payload = {
        "device_id": DEVICE_ID,
        "sensor_id": SENSOR_ID,
        "readings": readings
    }

    try:
        res = requests.post(API_URL, json=payload)
        print("[Service Layer] Sent to API:", res.status_code)
        return {"status": "forwarded", "response_code": res.status_code}
    except Exception as e:
        print("[Service Layer] Failed to send:", e)
        return {"status": "error", "detail": str(e)}
