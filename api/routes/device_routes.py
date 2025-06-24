from fastapi import APIRouter, HTTPException
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

@router.post("/devices")
def create_device(device: DeviceCreate):
    if db.devices.find_one({"_id": device.device_id}):
        raise HTTPException(status_code=400, detail="Device ID already exists")

    doc = device.dict()
    doc["_id"] = device.device_id
    doc["created_at"] = datetime.now(timezone.utc)
    doc["is_deleted"] = False
    db.devices.insert_one(doc)
    return {"message": "Device created", "device": doc}


@router.get("/devices/{device_id}")
def get_device(device_id: str):
    device = db.devices.find_one({"_id": device_id, "is_deleted": False}, {"_id": 0})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.patch("/devices/{device_id}")
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


@router.delete("/devices/{device_id}")
def soft_delete_device(device_id: str):
    result = db.devices.update_one(
        {"_id": device_id, "is_deleted": False},
        {"$set": {"is_deleted": True, "deleted_at": datetime.now(timezone.utc)}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Device not found or already deleted")

    return {"message": "Device soft-deleted successfully"}
