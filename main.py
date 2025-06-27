
import subprocess
import time

# Run FastAPI app
api_process = subprocess.Popen(["uvicorn", "api.main:app", "--reload"])

# Small delay to let API start before MQTT receiver connects
time.sleep(3)

# Run MQTT Receiver (adjust path if needed)
mqtt_process = subprocess.Popen(["python", "mqtt_receiver/mqtt_receiver.py"])

try:
    # Wait for both processes
    api_process.wait()
    mqtt_process.wait()
except KeyboardInterrupt:
    print("\n[!] Stopping processes...")
    api_process.terminate()
    mqtt_process.terminate()
=======
import random

