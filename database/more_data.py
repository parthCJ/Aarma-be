from pymongo import MongoClient
from datetime import datetime, timezone
from connection import get_database


db = get_database()

now = datetime.now(timezone.utc)

# -----------------------------
# Seed 10 users
# -----------------------------
users = []
for i in range(10):
    uid = f"USER{i+1:03}"
    users.append({
        "_id": uid,
        "user_id": uid,
        "email": f"user{i+1}@example.com",
        "number": f"96497224{i+1:02}0",
        "location_ids": [f"LOC{i+1:03}"],
        "created_at": now,
        "updated_at": now,
        "is_deleted": False
    })
db.users.delete_many({})
db.users.insert_many(users)

# -----------------------------
# Seed 10 locations
# -----------------------------
locations = []
for i in range(10):
    lid = f"LOC{i+1:03}"
    locations.append({
        "_id": lid,
        "location_id": lid,
        "user_id": f"USER{i+1:03}",
        "address": {
            "street": f"Street {i+1}",
            "city": "Kota",
            "state": "Rajasthan",
            "country": "India",
            "zip_code": f"32400{i+1}"
        },
        "name": f"Location {i+1}",
        "coordinates": [26.9 + i*0.01, 75.7 + i*0.01],
        "description": f"Description {i+1}",
        "created_at": now,
        "updated_at": now,
        "is_deleted": False
    })
db.locations.delete_many({})
db.locations.insert_many(locations)

# -----------------------------
# Seed 10 devices
# -----------------------------
devices = []
for i in range(10):
    did = f"DEV{i+1:03}"
    devices.append({
        "_id": did,
        "device_id": did,
        "location_id": f"LOC{i+1:03}",
        "location_mark": f"Mark {i+1}",
        "device_name": f"Device {i+1}",
        "sensor_ids": [f"SENS{i+1:03}"],
        "created_at": now,
        "updated_at": now,
        "is_deleted": False
    })
db.devices.delete_many({})
db.devices.insert_many(devices)

# -----------------------------
# Seed 10 sensors
# -----------------------------
sensors = []
for i in range(10):
    sid = f"SENS{i+1:03}"
    sensors.append({
        "_id": sid,
        "sensor_id": sid,
        "devices": [f"DEV{i+1:03}"],
        "sensor_data_log": [],
        "created_at": now,
        "updated_at": now,
        "is_deleted": False
    })
db.sensors.delete_many({})
db.sensors.insert_many(sensors)

# -----------------------------
# Seed 10 sensor_data records
# -----------------------------
sensor_data_entries = []
for i in range(10):
    sensor_data_entries.append({
        "sensor_id": f"SENS{i+1:03}",
        "device_id": f"DEV{i+1:03}",
        "created_at": datetime(2025, 6, 21, 12, i, tzinfo=timezone.utc),
        "readings": [
            {
                "sensor_name": "Temperature",
                "status": "OK",
                "reading": 20 + i,
                "unit": "°C",
                "note": "Stable",
                "sensor_health": "Good",
                "sensor_specification": "DHT11"
            }
        ]
    })
db.sensor_data.delete_many({})
db.sensor_data.insert_many(sensor_data_entries)

# -----------------------------
# (Optional) Clear history tables for fresh start
# -----------------------------
db.user_update_history.delete_many({})
db.device_update_history.delete_many({})
db.location_update_history.delete_many({})
db.sensor_update_history.delete_many({})

print("✅ Seeded 10 records in each collection.")
