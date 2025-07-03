import json
import ssl
import time
import random
import paho.mqtt.client as mqtt
import requests

# === MQTT CONFIG ===
ENDPOINT = "d002332310q6wvd4iri8x-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
TOPIC = "iot/adc_data"
CLIENT_ID = "mqtt_sender"

# === Certificate Paths ===

CA_PATH   = "../certs/AmazonRootCA1.pem"
CERT_PATH = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-certificate.pem.crt"
KEY_PATH  = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-private.pem.key"

# === Local API Endpoint (that saves to MongoDB) ===
SERVICE_URL = "http://127.0.0.1:5000/sensors/sensor-data"

# === IDs for device/sensor ===
DEVICE_ID = "DEV001"
SENSOR_ID = "SENS001"

# === Connect & Authenticate ===
client = mqtt.Client(client_id=CLIENT_ID)
client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[✅ MQTT Sender] Connected to AWS IoT Core.")
    else:
        print(f"[❌ MQTT Sender] Connection failed with code {rc}")

client.on_connect = on_connect
print("[🔄 MQTT Sender] Connecting...")
client.connect(ENDPOINT, PORT)
client.loop_start()


# === Function to Generate Mock Sensor Data and Send to API ===
def generate_mock_data():
    return {
        "sensor_id": SENSOR_ID,
        "device_id": DEVICE_ID,
        "readings": [
            {
                "sensor_name": "temperature",
                "status": "active",
                "reading": round(random.uniform(15.0, 35.0), 2),
                "unit": "°C",
                "note": "mock temperature",
                "sensor_health": "good",
                "sensor_specification": "Simulated"
            },
            {
                "sensor_name": "humidity",
                "status": "active",
                "reading": round(random.uniform(30.0, 80.0), 2),
                "unit": "%",
                "note": "mock humidity",
                "sensor_health": "good",
                "sensor_specification": "Simulated"
            }
        ]
    }

# === Loop to Send via MQTT + API ===
try:
    while True:
        mock_data = generate_mock_data()
        payload = json.dumps(mock_data)

        # Send via MQTT
        result = client.publish(TOPIC, payload)
        if result[0] == 0:
            print(f"[📤 MQTT Sent] {payload}")
        else:
            print("[⚠️ MQTT Failed] Could not send message")

        # Also send to local API (which stores in MongoDB)
        try:
            api_response = requests.post(SERVICE_URL, json=mock_data)
            print(f"[🌐 API Sent] Status: {api_response.status_code}")
        except Exception as api_err:
            print(f"[❌ API Error] {api_err}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n[🔌 MQTT Sender] Disconnected by user.")
finally:
    client.loop_stop()
    client.disconnect()
