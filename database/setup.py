from pymongo import MongoClient
from datetime import datetime, timezone
from connection import get_database


db = get_database()


def seed_users():
    db.users.replace_one(
        {"_id": "USER001"},
        {
            "_id": "USER001",
            "user_id": "USER001",
            "email": "krishna@example.com",
            "number": "9649722470",
            "location_ids": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_deleted": False
        },
        upsert=True
    )

def seed_locations():
    db.locations.replace_one(
        {"_id": "LOC001"},
        {
            "_id": "LOC001",
            "location_id": "LOC001",
            "user_id": "USER001",
            "address": {
                "street": "123 Tech St",
                "city": "Kota",
                "state": "Rajasthan",
                "country": "India",
                "zip_code": "324005"
            },
            "name": "Home Lab",
            "coordinates": [26.9124, 75.7873],
            "description": "Test IoT Setup",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_deleted": False
        },
        upsert=True
    )

def seed_devices():
    db.devices.replace_one(
        {"_id": "DEV001"},
        {
            "_id": "DEV001",
            "device_id": "DEV001",
            "location_id": "LOC001",
            "location_mark": "Lab 1",
            "device_name": "EnvMonitor",
            "sensor_ids": ["SENS001"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_deleted": False
        },
        upsert=True
    )

def seed_sensors():
    db.sensors.replace_one(
        {"_id": "SENS001"},
        {
            "_id": "SENS001",
            "sensor_id": "SENS001",
            "devices": ["DEV001"],
            "sensor_data_log": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "is_deleted": False
        },
        upsert=True
    )

def seed_sensor_data():
    db.sensor_data.replace_one(
        {
            "sensor_id": "SENS001",
            "created_at": datetime(2025, 6, 21, tzinfo=timezone.utc)
        },
        {
            "device_id": "DEV001",
            "sensor_id": "SENS001",
            "created_at": datetime(2025, 6, 21, tzinfo=timezone.utc),
            "readings": [
                {
                    "sensor_name": "Temperature",
                    "status": "OK",
                    "reading": 23.5,
                    "unit": "°C",
                    "note": "Stable",
                    "sensor_health": "Good",
                    "sensor_specification": "DHT11"
                }
            ]
        },
        upsert=True
    )

def seed_update_history():
    now = datetime.now(timezone.utc)

    db.user_update_history.replace_one(
        {"_id": "UHIST001"},
        {
            "_id": "UHIST001",
            "user_id": "USER001",
            "timestamp": now,
            "old_data": {
                "email": "krishna@example.com",
                "number": "9649722470"
            },
            "updated_fields": {
                "email": "krishna_new@example.com"
            }
        },
        upsert=True
    )

    db.device_update_history.replace_one(
        {"_id": "DHIST001"},
        {
            "_id": "DHIST001",
            "device_id": "DEV001",
            "timestamp": now,
            "old_data": {
                "device_name": "EnvMonitor",
                "location_mark": "Lab 1"
            },
            "updated_fields": {
                "device_name": "EnvMonitor Updated"
            }
        },
        upsert=True
    )

    db.location_update_history.replace_one(
        {"_id": "LHIST001"},
        {
            "_id": "LHIST001",
            "location_id": "LOC001",
            "timestamp": now,
            "old_data": {
                "name": "Home Lab",
                "description": "Test IoT Setup"
            },
            "updated_fields": {
                "description": "Updated Description"
            }
        },
        upsert=True
    )

    db.sensor_update_history.replace_one(
        {"_id": "SHIST001"},
        {
            "_id": "SHIST001",
            "sensor_id": "SENS001",
            "timestamp": now,
            "old_data": {
                "sensor_id": "SENS001"
            },
            "updated_fields": {
                "sensor_specification": "DHT22"
            }
        },
        upsert=True
    )

def create_indexes():
    db.users.create_index("email", unique=True)
    db.users.create_index("number", unique=True)
    db.users.create_index("user_id", unique=True)

    db.devices.create_index("device_id", unique=True)
    db.devices.create_index("location_id")

    db.locations.create_index("location_id", unique=True)
    db.locations.create_index("user_id")

    db.sensors.create_index("sensor_id", unique=True)

    db.sensor_data.create_index([("sensor_id", 1), ("created_at", 1)], unique=True)

    db.user_update_history.create_index("user_id")
    db.device_update_history.create_index("device_id")
    db.location_update_history.create_index("location_id")
    db.sensor_update_history.create_index("sensor_id")

# Run all seeds and index setups
seed_users()
seed_locations()
seed_devices()
seed_sensors()
seed_sensor_data()
seed_update_history()
create_indexes()
