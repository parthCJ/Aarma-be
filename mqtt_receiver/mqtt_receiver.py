# === mqtt_receiver.py ===
import json
import ssl
import os
import paho.mqtt.client as mqtt
import random
import time
from pymongo import MongoClient
from datetime import datetime
from copy import deepcopy
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.service_layer import add_sensor_data_if_changed_via_api

# === MQTT CONFIG ===
ENDPOINT = "d002332310q6wvd4iri8x-ats.iot.ap-south-1.amazonaws.com" # <-- Replace with your real AWS IoT endpoint
PORT = 8883
TOPIC = "iot/adc_data" 

# === Certificate Paths (your actual files) ===

CA_PATH   = r"C:\Users\student.CL02045\Desktop\FINAL_IOT_PROJECT\Aarma-be\certs\AmazonRootCA1.pem"
CERT_PATH = r"C:\Users\student.CL02045\Desktop\FINAL_IOT_PROJECT\Aarma-be\certs\8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-certificate.pem.crt"
KEY_PATH  = r"C:\Users\student.CL02045\Desktop\FINAL_IOT_PROJECT\Aarma-be\certs\8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-private.pem.key"

# === MongoDB Setup ===
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["iot_project"]
sensor_data_collection = db["sensor_data"]

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

        # Save raw reading for backup purposes
        mongo_payload = deepcopy(payload)
        mongo_payload["received_at"] = datetime.utcnow()
        sensor_data_collection.insert_one(mongo_payload)
        print("[MongoDB] Raw data inserted")

        # Service logic to send only if significant change
        result = add_sensor_data_if_changed_via_api(payload)
        print("[Service Layer] Result:", result)

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

print("[MQTT Receiver] Connecting to AWS IoT...")
client.connect(ENDPOINT, PORT)
client.loop_forever()
