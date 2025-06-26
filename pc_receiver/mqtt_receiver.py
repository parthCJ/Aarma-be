import json
import ssl
import os
import paho.mqtt.client as mqtt
import requests
import random
import time

# === MQTT CONFIG ===
ENDPOINT = "d002332310q6wvd4iri8x-ats.iot.ap-south-1.amazonaws.com" # <-- Replace with your real AWS IoT endpoint
PORT = 8883
TOPIC = "iot/adc_data" 

# === Certificate Paths (your actual files) ===
CA_PATH   = "../certs/AmazonRootCA1.pem"
CERT_PATH = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-certificate.pem.crt"
KEY_PATH  = "../certs/8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-private.pem.key"

# === Local service layer URL ===
SERVICE_URL = "http://localhost:9000/process"

# === MQTT Callbacks ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT Receiver] Connected successfully.")
        client.subscribe(TOPIC)
    else:
        print(f"[MQTT Receiver] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("[MQTT Receiver] Received:", payload)

        response = requests.post(SERVICE_URL, json=payload)
        print("[MQTT Receiver] Forwarded to service layer:", response.status_code)

    except Exception as e:
        print("[MQTT Receiver] Error:", e)

# === MQTT Setup ===
client = mqtt.Client(client_id="mqtt_receiver")
client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.on_connect = on_connect
client.on_message = on_message

# === Connect to AWS and Start Loop ===
print("[MQTT Receiver] Connecting to AWS IoT...")
client.connect(ENDPOINT, PORT)
client.loop_forever()
