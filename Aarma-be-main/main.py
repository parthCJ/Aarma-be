
# import subprocess
# import time

# # Run FastAPI app
# api_process = subprocess.Popen(["uvicorn", "api.main:app", "--reload"])

# # Small delay to let API start before MQTT receiver connects
# time.sleep(3)

# # Run MQTT Receiver (adjust path if needed)
# mqtt_process = subprocess.Popen(["python", "mqtt_receiver/mqtt_receiver.py"])

# try:
#     # Wait for both processes
#     api_process.wait()
#     mqtt_process.wait()
# except KeyboardInterrupt:
#     print("\n[!] Stopping processes...")
#     api_process.terminate()
#     mqtt_process.terminate()

import subprocess
import time
import requests

def wait_for_api(url, timeout=15):
    """Ping the FastAPI server until it's up or timeout is reached."""
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    return False

# Start FastAPI server
api_process = subprocess.Popen(["uvicorn", "api.main:app", "--reload"])

# Wait until server is reachable
if wait_for_api("http://localhost:5000/docs"):
    print("[✓] FastAPI is up. Starting MQTT receiver...")
    mqtt_process = subprocess.Popen(["python", "mqtt_receiver/mqtt_receiver.py"])
else:
    print("[!] FastAPI did not start in time.")
    api_process.terminate()
    exit(1)

try:
    api_process.wait()
    mqtt_process.wait()
except KeyboardInterrupt:
    print("\n[!] Stopping processes...")
    api_process.terminate()
    mqtt_process.terminate()

