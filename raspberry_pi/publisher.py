import time
import json
import ssl
import paho.mqtt.client as mqtt
from Adafruit_ADS1x15 import ADS1115
from RPLCD.i2c import CharLCD

# === MQTT CONFIG ===
ENDPOINT = "your-endpoint.iot.region.amazonaws.com"  # << replace with your AWS IoT Core endpoint
PORT = 8883
TOPIC = "iot/adc_data"
CLIENT_ID = "mqtt_publisher"

CA_PATH = "../certs/AmazonRootCA1.pem"
CERT_PATH = "../certs/your-certificate.pem.crt"
KEY_PATH = "../certs/your-private.pem.key"

# === MQTT SETUP ===
client = mqtt.Client(client_id=CLIENT_ID)
client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect(ENDPOINT, PORT)
client.loop_start()

# === ADC + LCD SETUP ===
adc = ADS1115()
lcd = CharLCD('PCF8574', 0x27)
GAIN = 1  # +/- 4.096V

def read_adc_values():
    try:
        while True:
            # Read raw ADC values
            ch_values = [adc.read_adc(i, gain=GAIN) for i in range(4)]
            voltages = [round(v * 4.096 / 32768.0, 3) for v in ch_values]

            # Display on LCD
            lcd.clear()
            lcd.write_string(f"CH0:{voltages[0]:.2f}V CH1:{voltages[1]:.2f}V")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"CH2:{voltages[2]:.2f}V CH3:{voltages[3]:.2f}V")

            # Prepare JSON payload
            payload = {
                "ch0": voltages[0],
                "ch1": voltages[1],
                "ch2": voltages[2],
                "ch3": voltages[3],
                "sent_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Publish to MQTT
            client.publish(TOPIC, json.dumps(payload))
            print("[Publisher] Sent:", payload)

            time.sleep(2)

    except KeyboardInterrupt:
        print("Exiting...")
        lcd.clear()
        lcd.write_string("Stopped...")
        time.sleep(2)
        lcd.clear()
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    read_adc_values()
