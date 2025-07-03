# sensor_api.py
from fastapi import APIRouter, HTTPException
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from fastapi.responses import StreamingResponse
import csv
import io






client = MongoClient("mongodb+srv://mahanshgaur:Mahansh%40123@arma.soyopa5.mongodb.net/?retryWrites=true&w=majority&appName=ARMA")
db = client["iot_project"]

router = APIRouter()

# -------------------------- SCHEMAS --------------------------
class SensorCreate(BaseModel):
    sensor_id: str = Field(...)
    devices: List[str] = Field(...)

class SensorUpdate(BaseModel):
    devices: Optional[List[str]] = None

class SensorReading(BaseModel):
    sensor_name: str
    status: str
    reading: float
    unit: str
    note: Optional[str] = ""
    sensor_health: Optional[str] = None
    sensor_specification: Optional[str] = None

class SensorDataIn(BaseModel):
    device_id: str
    sensor_id: str
    readings: List[SensorReading]

class SensorResponse(BaseModel):
    sensor_id: str
    devices: List[str]
    is_deleted: bool = False

class SensorUpdateHistory(BaseModel):
    history_id: str
    sensor_id: str
    timestamp: datetime
    old_data: Dict[str, Any]
    updated_fields: Dict[str, Any]

# -------------------------- ROUTES --------------------------

@router.post("/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate):
    if db.sensors.find_one({"_id": sensor.sensor_id}):
        raise HTTPException(status_code=400, detail="Sensor already exists")
    db.sensors.insert_one({
        "_id": sensor.sensor_id,
        "sensor_id": sensor.sensor_id,
        "devices": sensor.devices,
        "sensor_data_log": [],
        "is_deleted": False
    })
    return {"sensor_id": sensor.sensor_id, "devices": sensor.devices, "is_deleted": False}


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: str):
    sensor = db.sensors.find_one({"_id": sensor_id, "is_deleted": False})
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {
        "sensor_id": sensor["sensor_id"],
        "devices": sensor["devices"],
        "is_deleted": sensor.get("is_deleted", False)
    }


@router.patch("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: str, update: SensorUpdate):
    sensor = db.sensors.find_one({"_id": sensor_id})
    if not sensor or sensor.get("is_deleted"):
        raise HTTPException(status_code=404, detail="Sensor not found")

    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.sensors.update_one({"_id": sensor_id}, {"$set": update_data})

    history_doc = {
        "id": f"SENS_HIST{ObjectId()}",
        "sensor_id": sensor_id,
        "timestamp": datetime.now(timezone.utc),
        "old_data": {k: sensor.get(k) for k in update_data},
        "updated_fields": update_data
    }
    db.sensor_update_history.insert_one(history_doc)

    sensor.update(update_data)
    return {
        "sensor_id": sensor["sensor_id"],
        "devices": sensor["devices"],
        "is_deleted": sensor.get("is_deleted", False)
    }


@router.delete("/{sensor_id}")
def soft_delete_sensor(sensor_id: str):
    result = db.sensors.update_one(
        {"_id": sensor_id, "is_deleted": {"$ne": True}},
        {"$set": {"is_deleted": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sensor not found or already deleted")
    return {"message": "Sensor soft-deleted successfully."}


@router.post("/sensor-data")
def add_sensor_data(data: SensorDataIn):
    sensor = db.sensors.find_one({"_id": data.sensor_id})
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    document = {
        "sensor_id": data.sensor_id,
        "device_id": data.device_id,
        "created_at": datetime.now(timezone.utc),
        "readings": [reading.model_dump() for reading in data.readings]
    }
    db.sensor_data.insert_one(document)
    return {"message": "Sensor data added."}

@router.get("/{sensor_id}/last-data")
def get_last_sensor_data(sensor_id: str):
    """
    Return the latest sensor_data document for the given sensor_id.
    """
    result = db.sensor_data.find_one(
        {"sensor_id": sensor_id},
        sort=[("created_at", -1)],
        projection={"_id": 0}
    )
    if not result:
        raise HTTPException(status_code=404, detail="No sensor data found")
    return result



@router.get("/sensor-data/filter")
def filter_sensor_data(
    sensor_id: Optional[str] = None,
    device_id: Optional[str] = None,
    sensor_name: Optional[str] = None,
    start_date: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS"),
    end_date: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS")
):
    query = {}

    # Main filters
    if sensor_id:
        query["sensor_id"] = sensor_id
    if device_id:
        query["device_id"] = device_id
    if start_date or end_date:
        query["created_at"] = {}
        if start_date:
            query["created_at"]["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            query["created_at"]["$lte"] = datetime.fromisoformat(end_date)

    # Query MongoDB
    raw_data = db.sensor_data.find(query, {"_id": 0})

    filtered_results = []

    for doc in raw_data:
        if sensor_name:
            # Filter readings inside the document
            filtered_readings = [
                r for r in doc["readings"]
                if r["sensor_name"].lower() == sensor_name.lower()
            ]
            if filtered_readings:
                doc["readings"] = filtered_readings
                filtered_results.append(doc)
        else:
            filtered_results.append(doc)

    return {"count": len(filtered_results), "results": jsonable_encoder(filtered_results)}




# # ----------------------------- #
# # Export ALL sensor data to CSV
# # ----------------------------- #
# @router.get("/data/export/csv")
# def export_all_sensor_data_csv():
#     cursor = db.sensor_data.find({}, {"_id": 0})
#     return generate_csv_response(cursor, filename="all_sensor_data.csv")


# # ------------------------------------------ #
# # Export data for a specific sensor_id to CSV
# # ------------------------------------------ #
# @router.get("/data/export/csv/{sensor_id}")
# def export_sensor_data_by_id_csv(sensor_id: str):
#     cursor = db.sensor_data.find({"sensor_id": sensor_id}, {"_id": 0})
#     return generate_csv_response(cursor, filename=f"{sensor_id}_data.csv")


# # ---------------------- #
# # Shared CSV generator
# # ---------------------- #
# def generate_csv_response(cursor, filename="data.csv"):
#     data = list(cursor)
#     # print(data)
#     output = io.StringIO()
#     writer = csv.writer(output)

#     # Header row
#     header = ["sensor_id", "device_id", "created_at", "sensor_name", "status", "reading", "unit", "note", "sensor_health", "sensor_specification"]
#     writer.writerow(header)

#     for doc in data:
#         # print(doc)
#         for reading in doc.get("readings", []):
#             # print(reading)
#             writer.writerow([
#                 doc.get("sensor_id", ""),
#                 doc.get("device_id", ""),
#                 doc.get("created_at", ""),
#                 reading.get("sensor_name", ""),
#                 reading.get("status", ""),
#                 reading.get("reading", ""),
#                 reading.get("unit", ""),
#                 reading.get("note", ""),
#                 reading.get("sensor_health", ""),
#                 reading.get("sensor_specification", "")
#             ])

#     output.seek(0)
#     return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})

from fastapi.responses import StreamingResponse
import io
import csv

# ----------------------------- #
# Export ALL flat sensor data
# ----------------------------- #
@router.get("/data/export/flat-csv")
def export_all_flat_sensor_data_csv():
    cursor = db.sensor_data.find({}, {"_id": 0})
    return generate_flat_csv_response(cursor, "flat_sensor_data.csv")


# -------------------------------------------- #
# Export flat sensor data for specific sensor
# -------------------------------------------- #
@router.get("/data/export/flat-csv/{sensor_id}")
def export_flat_sensor_data_by_id_csv(sensor_id: str):
    cursor = db.sensor_data.find({"sensor_id": sensor_id}, {"_id": 0})
    return generate_flat_csv_response(cursor, f"{sensor_id}_flat_data.csv")


# ----------------------------- #
# Flat CSV Generator
# ----------------------------- #
def generate_flat_csv_response(cursor, filename: str):
    data = list(cursor)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    output = io.StringIO()
    writer = csv.writer(output)

    # Use keys from first doc as headers
    header = list(data[0].keys())
    writer.writerow(header)

    for doc in data:
        row = [doc.get(col, "") for col in header]
        writer.writerow(row)

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
