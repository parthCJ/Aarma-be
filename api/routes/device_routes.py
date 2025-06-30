from fastapi import APIRouter, HTTPException
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from uuid import uuid4
from database import db  # assumes your MongoDB connection is in database/db.py

router = APIRouter()

# ------------ Models ------------
class SensorModel(BaseModel):
    sensor_id: str
    sensor_name: str
    sensor_specification: str
    location_id: str

class DeviceCreate(BaseModel):
    device_id: str = Field(..., example="DEV001")
    location_id: str
    location_mark: str
    device_name: str
    sensors: List[SensorModel]

class DeviceUpdate(BaseModel):
    location_id: Optional[str] = None
    location_mark: Optional[str] = None
    device_name: Optional[str] = None
    sensors: Optional[List[SensorModel]] = None

# ------------ Routes ------------

@router.post("/")
def create_device(device: DeviceCreate):
    if db.devices.find_one({"_id": device.device_id}):
        raise HTTPException(status_code=400, detail="Device ID already exists")

    doc = device.model_dump()
    doc["_id"] = device.device_id
    doc["created_at"] = datetime.now(timezone.utc)
    doc["is_deleted"] = False
    db.devices.insert_one(doc)
    return {"message": "Device created", "device": doc}


@router.get("/{device_id}")
def get_device(device_id: str):
    device = db.devices.find_one({"_id": device_id, "is_deleted": False}, {"_id": 0})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.patch("/{device_id}")
def update_device(device_id: str, updates: DeviceUpdate):
    existing = db.devices.find_one({"_id": device_id, "is_deleted": False})
    if not existing:
        raise HTTPException(status_code=404, detail="Device not found")

    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")

    old_data = {k: existing.get(k) for k in update_data.keys()}

    db.devices.update_one({"_id": device_id}, {"$set": update_data})

    db.device_update_history.insert_one({
        "_id": uuid4().hex,
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc),
        "old_data": old_data,
        "updated_fields": update_data
    })

    return {"message": "Device updated", "old_data": old_data, "new_data": update_data}


@router.delete("/{device_id}")
def soft_delete_device(device_id: str):
    result = db.devices.update_one(
        {"_id": device_id, "is_deleted": False},
        {"$set": {"is_deleted": True, "deleted_at": datetime.now(timezone.utc)}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Device not found or already deleted")

    return {"message": "Device soft-deleted successfully"}




@router.get("/filter")
def filter_devices(
    device_id: Optional[str] = None,
    location_id: Optional[str] = None,
    location_mark: Optional[str] = None,
    device_name: Optional[str] = None,
    sensor_id: Optional[str] = None,
    sensor_name: Optional[str] = None,
    created_from: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS"),
    created_to: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS")
):
    query = {"is_deleted": False}

    if device_id:
        query["_id"] = device_id
    if location_id:
        query["location_id"] = location_id
    if location_mark:
        query["location_mark"] = {"$regex": location_mark, "$options": "i"}
    if device_name:
        query["device_name"] = {"$regex": device_name, "$options": "i"}
    if created_from or created_to:
        query["created_at"] = {}
        if created_from:
            query["created_at"]["$gte"] = datetime.fromisoformat(created_from)
        if created_to:
            query["created_at"]["$lte"] = datetime.fromisoformat(created_to)

    devices = list(db.devices.find(query, {"_id": 0}))

    # Filter inside sensors array if sensor_id or sensor_name given
    if sensor_id or sensor_name:
        filtered = []
        for d in devices:
            matched_sensors = []
            for s in d.get("sensors", []):
                if sensor_id and s.get("sensor_id") == sensor_id:
                    matched_sensors.append(s)
                elif sensor_name and sensor_name.lower() in s.get("sensor_name", "").lower():
                    matched_sensors.append(s)
            if matched_sensors:
                d["sensors"] = matched_sensors
                filtered.append(d)
        return jsonable_encoder(filtered)

    return jsonable_encoder(devices)
