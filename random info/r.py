import json
import random
import ssl
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
    
# MQTT Config
ENDPOINT = "d002332310q6wvd4iri8x-ats.iot.ap-south-1.amazonaws.com"
PORT     = 8883
TOPIC    = "iot/adc_data"

CA_PATH   = "AmazonRootCA1.pem"
CERT_PATH = "8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-certificate.pem.crt"
KEY_PATH  = "8805dbe759dbb5b938494f05b7c2712546d9ef678ba719f4cf40f330b4d290de-private.pem.key"

# MongoDB Config
MONGO_URI = "mongodb://localhost:27017"  # Change to your Mongo URI if hosted elsewhere
DB_NAME = "iot_db"
COLLECTION_NAME = "adc_data"

# Setup MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def on_connect(client, userdata, flags, rc):
    print(f"[Receiver] Connected with result code {rc}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[Receiver] CH Data Received: {payload}")

        # Add timestamp if needed
        payload['received_at'] = datetime.utcnow()

        # Insert into MongoDB
        collection.insert_one(payload)
        print("[Receiver] Data inserted into MongoDB.")

    except Exception as e:
        print("[Error] Failed to process message:", e)

client = mqtt.Client(client_id="mqtt_receiver", protocol=mqtt.MQTTv311)
client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, tls_version=ssl.PROTOCOL_TLSv1_2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(ENDPOINT, PORT)
client.loop_forever()
